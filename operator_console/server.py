#!/usr/bin/env python3
"""SENKNET 本地视频作业控制服务。"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import re
import secrets
import subprocess
import sys
import threading
import webbrowser
from datetime import UTC, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

import psutil

from observatory.server import ObservatoryConfig, ObservatoryState, sanitize_text
from operator_console.contracts import (
    JOB_ID_PATTERN,
    PROVIDER_PROFILES,
    public_catalog,
    validate_job_request,
    validate_persisted_job,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = Path(__file__).resolve().parent / "web"
DEFAULT_STATE_ROOT = REPO_ROOT / ".senknet" / "operator"
DEFAULT_EVIDENCE_ROOT = REPO_ROOT / "evidence" / "runtime"
DEFAULT_CACHE_ROOT = Path.home() / ".cache" / "huggingface" / "hub"
RUNNER_PATH = REPO_ROOT / "tools" / "run_provider_compatibility_trial.py"
MAX_REQUEST_BYTES = 64 * 1024
MAX_LAUNCHER_LOG_BYTES = 64 * 1024
ACTIVE_STATES = frozenset({"STARTING", "RUNNING", "STOP_REQUESTED"})


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_tail(path: Path, repo_root: Path) -> str:
    if not path.is_file():
        return ""
    try:
        size = path.stat().st_size
        with path.open("rb") as handle:
            if size > MAX_LAUNCHER_LOG_BYTES:
                handle.seek(-MAX_LAUNCHER_LOG_BYTES, os.SEEK_END)
                handle.readline()
            data = handle.read(MAX_LAUNCHER_LOG_BYTES)
    except OSError:
        return ""
    return sanitize_text(data.decode("utf-8", errors="replace"), repo_root)


class ControlError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status: HTTPStatus = HTTPStatus.BAD_REQUEST,
        details: Any = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.details = details


class JobManager:
    """登记不可变作业请求，并通过显式确认控制本地执行进程。"""

    def __init__(
        self,
        repo_root: Path = REPO_ROOT,
        state_root: Path = DEFAULT_STATE_ROOT,
        evidence_root: Path = DEFAULT_EVIDENCE_ROOT,
        cache_root: Path = DEFAULT_CACHE_ROOT,
        python_executable: str | None = None,
        runner_path: Path = RUNNER_PATH,
    ) -> None:
        self.repo_root = repo_root.resolve()
        self.state_root = state_root.resolve()
        self.jobs_root = self.state_root / "jobs"
        self.evidence_root = evidence_root.resolve()
        self.cache_root = cache_root.resolve()
        self.python_executable = python_executable or sys.executable
        self.runner_path = runner_path.resolve()
        self.jobs_root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._processes: dict[str, subprocess.Popen[bytes]] = {}
        self.observer = ObservatoryState(
            ObservatoryConfig(
                repo_root=self.repo_root,
                evidence_root=self.evidence_root,
                cache_root=self.cache_root,
                web_root=WEB_ROOT,
            )
        )

    def overview(self) -> dict[str, Any]:
        system = self.observer.system_status()
        processes = self.observer.active_processes()
        return {
            "schema_version": "operator-console.v1",
            "generated_at": utc_now(),
            "mode": "LOCAL_CONTROLLED_EXECUTION",
            "catalog": public_catalog(),
            "system": system,
            "models": self.observer.model_statuses(),
            "active_generation_processes": processes,
            "jobs": self.list_jobs(),
            "observatory_url": "http://127.0.0.1:4319/",
            "control_boundary": {
                "local_only": True,
                "requires_preflight": True,
                "requires_exact_execution_id_confirmation": True,
                "creates_formal_fact": False,
                "creates_selection_decision": False,
                "creates_institution_freeze": False,
            },
        }

    def preflight(self, raw_request: Any) -> dict[str, Any]:
        normalized, errors = validate_job_request(raw_request)
        checks: list[dict[str, Any]] = []
        if errors:
            checks.append(
                self._check(
                    "REQUEST_VALID",
                    "请求字段完整",
                    False,
                    f"发现 {len(errors)} 个字段问题。",
                    {"errors": errors},
                )
            )
            return self._preflight_result(None, checks, errors)
        assert normalized is not None
        checks.extend(self._dynamic_checks(normalized))
        return self._preflight_result(normalized, checks, [])

    def create_job(self, raw_request: Any) -> dict[str, Any]:
        with self._lock:
            preflight = self.preflight(raw_request)
            if not preflight["passed"]:
                raise ControlError(
                    "PREFLIGHT_BLOCKED",
                    "作业预检未通过，拒绝登记。",
                    HTTPStatus.CONFLICT,
                    preflight,
                )
            normalized = preflight["normalized_request"]
            assert normalized is not None
            job_id = self._new_job_id()
            created_at = utc_now()
            request = {
                **normalized,
                "job_id": job_id,
                "created_at": created_at,
                "request_authority": "LOCAL_HUMAN_OPERATOR",
                "request_immutability": "APPEND_ONLY_CORRECTIONS_ONLY",
            }
            job_dir = self.jobs_root / job_id
            job_dir.mkdir()
            request_path = job_dir / "request.json"
            atomic_write_json(request_path, request)
            status = {
                "job_id": job_id,
                "execution_id": request["execution_id"],
                "state": "REGISTERED",
                "created_at": created_at,
                "updated_at": created_at,
                "request_sha256": file_sha256(request_path),
                "pid": None,
                "process_create_time": None,
                "exit_code": None,
                "terminal_reason": None,
            }
            atomic_write_json(job_dir / "status.json", status)
            self._append_event(job_dir, "JOB_REGISTERED", {"request_sha256": status["request_sha256"]})
            return self.job_detail(job_id)

    def start_job(self, job_id: str, confirmation_execution_id: str) -> dict[str, Any]:
        with self._lock:
            job_dir = self._job_dir(job_id)
            request, status = self._load_job(job_dir)
            if status["state"] != "REGISTERED":
                raise ControlError("INVALID_JOB_STATE", "只有已登记且尚未启动的作业可以启动。", HTTPStatus.CONFLICT)
            if confirmation_execution_id != request["execution_id"]:
                raise ControlError("CONFIRMATION_MISMATCH", "二次确认必须完整输入执行标识。", HTTPStatus.CONFLICT)
            checks = self._dynamic_checks(request, current_job_id=job_id)
            preflight = self._preflight_result(request, checks, [])
            if not preflight["passed"]:
                self._append_event(job_dir, "START_BLOCKED", {"checks": checks})
                raise ControlError("PREFLIGHT_BLOCKED", "启动前复检未通过。", HTTPStatus.CONFLICT, preflight)

            status.update({"state": "STARTING", "updated_at": utc_now(), "started_at": utc_now()})
            atomic_write_json(job_dir / "status.json", status)
            self._append_event(job_dir, "START_AUTHORIZED", {"confirmation_execution_id": confirmation_execution_id})
            command = [
                self.python_executable,
                str(self.runner_path),
                "--provider",
                request["provider_key"],
                "--execution-id",
                request["execution_id"],
                "--job-spec",
                str(job_dir / "request.json"),
                "--evidence-root",
                str(self.evidence_root),
            ]
            launcher_log = (job_dir / "launcher.log").open("ab", buffering=0)
            try:
                process = subprocess.Popen(
                    command,
                    cwd=self.repo_root,
                    stdin=subprocess.DEVNULL,
                    stdout=launcher_log,
                    stderr=subprocess.STDOUT,
                )
            except OSError as exc:
                launcher_log.close()
                status.update(
                    {
                        "state": "FAILED",
                        "updated_at": utc_now(),
                        "finished_at": utc_now(),
                        "terminal_reason": f"LAUNCH_FAILED_{type(exc).__name__}",
                    }
                )
                atomic_write_json(job_dir / "status.json", status)
                self._append_event(job_dir, "LAUNCH_FAILED", {"error_type": type(exc).__name__})
                raise ControlError("LAUNCH_FAILED", "执行进程无法启动。", HTTPStatus.INTERNAL_SERVER_ERROR) from exc
            finally:
                launcher_log.close()

            try:
                process_create_time = psutil.Process(process.pid).create_time()
            except psutil.NoSuchProcess:
                status["exit_code"] = process.poll()
                atomic_write_json(job_dir / "status.json", status)
                self._append_event(
                    job_dir,
                    "PROCESS_EXITED_BEFORE_TRACKING",
                    {"pid": process.pid, "exit_code": process.poll()},
                )
                return self.job_detail(job_id)
            status.update(
                {
                    "state": "RUNNING",
                    "updated_at": utc_now(),
                    "pid": process.pid,
                    "process_create_time": process_create_time,
                }
            )
            atomic_write_json(job_dir / "status.json", status)
            self._append_event(job_dir, "PROCESS_STARTED", {"pid": process.pid})
            self._processes[job_id] = process
            threading.Thread(target=self._monitor_process, args=(job_id, process), daemon=True).start()
            return self.job_detail(job_id)

    def stop_job(self, job_id: str) -> dict[str, Any]:
        with self._lock:
            job_dir = self._job_dir(job_id)
            request, status = self._load_job(job_dir)
            if status["state"] not in {"STARTING", "RUNNING"}:
                raise ControlError("INVALID_JOB_STATE", "只有正在启动或运行的作业可以停止。", HTTPStatus.CONFLICT)
            process = self._matching_process(request, status)
            if process is None:
                self._refresh_terminal_state(job_dir, request, status)
                raise ControlError("PROCESS_NOT_FOUND", "对应执行进程已经不存在，状态已重新核对。", HTTPStatus.CONFLICT)
            status.update({"state": "STOP_REQUESTED", "updated_at": utc_now(), "stop_requested_at": utc_now()})
            atomic_write_json(job_dir / "status.json", status)
            self._append_event(job_dir, "STOP_REQUESTED", {"pid": status.get("pid")})
            try:
                self._terminate_process_tree(process)
            except psutil.Error as exc:
                raise ControlError("STOP_FAILED", "无法向对应进程发送停止信号。", HTTPStatus.CONFLICT) from exc
            return self.job_detail(job_id)

    def list_jobs(self) -> list[dict[str, Any]]:
        values = []
        if not self.jobs_root.is_dir():
            return values
        for job_dir in self.jobs_root.iterdir():
            if not job_dir.is_dir() or not JOB_ID_PATTERN.fullmatch(job_dir.name):
                continue
            try:
                values.append(self.job_detail(job_dir.name, include_events=False))
            except ControlError:
                continue
        return sorted(values, key=lambda item: item["created_at"], reverse=True)

    def job_detail(self, job_id: str, include_events: bool = True) -> dict[str, Any]:
        with self._lock:
            job_dir = self._job_dir(job_id)
            request, status = self._load_job(job_dir)
            if status["state"] in ACTIVE_STATES and self._matching_process(request, status) is None:
                status = self._refresh_terminal_state(job_dir, request, status)
            evidence_summary = read_json(self.evidence_root / request["execution_id"] / "summary.json")
            value = {
                "job_id": job_id,
                "execution_id": request["execution_id"],
                "provider_key": request["provider_key"],
                "model_id": request["model_id"],
                "task_type": request["task_type"],
                "generation_profile_key": request["generation_profile_key"],
                "execution_strategy": request["execution_strategy"],
                "prompt": request["prompt"],
                "parameters": request["parameters"],
                "resource_budget": request["resource_budget"],
                "created_at": request["created_at"],
                "state": status["state"],
                "updated_at": status.get("updated_at"),
                "started_at": status.get("started_at"),
                "finished_at": status.get("finished_at"),
                "pid": status.get("pid"),
                "exit_code": status.get("exit_code"),
                "terminal_reason": status.get("terminal_reason"),
                "evidence_observation": evidence_summary.get("observation") if evidence_summary else None,
                "evidence_available": evidence_summary is not None,
                "launcher_log_tail": read_tail(job_dir / "launcher.log", self.repo_root),
            }
            if include_events:
                value["events"] = self._read_events(job_dir)
            return value

    def _dynamic_checks(
        self,
        request: dict[str, Any],
        current_job_id: str | None = None,
    ) -> list[dict[str, Any]]:
        models = {item["key"]: item for item in self.observer.model_statuses()}
        model = models.get(request["provider_key"], {})
        profile = PROVIDER_PROFILES[request["provider_key"]]
        system = self.observer.system_status()
        active = self.observer.active_processes()
        execution_id = request["execution_id"]
        duplicate_job = self._find_job_by_execution_id(execution_id)
        execution_id_unused = (
            not (self.evidence_root / execution_id).exists()
            and (duplicate_job is None or duplicate_job == current_job_id)
        )
        checks = [
            self._check("PROVIDER_RUNTIME", "提供者运行性已观察", profile["startable"], profile["risk_message"]),
            self._check(
                "MODEL_REVISION_READY",
                "精确模型快照完整",
                model.get("state") == "ready" and model.get("observed_revision_present") is True,
                f"缓存状态：{model.get('state', 'unknown')}，未完成文件：{model.get('incomplete_file_count', 'unknown')}",
            ),
            self._check(
                "NO_ACTIVE_GENERATION",
                "没有其他生成进程",
                not active,
                "当前没有提供者生成进程。" if not active else f"检测到 {len(active)} 个生成进程。",
            ),
            self._check(
                "EXECUTION_ID_UNUSED",
                "执行标识未被使用",
                execution_id_unused,
                "执行标识可用。" if execution_id_unused else "证据目录或既有作业已使用该标识。",
            ),
            self._check(
                "AVAILABLE_MEMORY",
                "可用内存达到启动预算",
                system["memory"]["available_bytes"] >= request["resource_budget"]["preflight_min_available_memory_bytes"],
                f"当前可用 {system['memory']['available_bytes']} 字节，要求至少 {request['resource_budget']['preflight_min_available_memory_bytes']} 字节。",
            ),
            self._check(
                "MPS_MEMORY_LIMIT_CONFIGURED",
                "MPS 进程内存上限已固定",
                0.5 <= request["resource_budget"]["mps_memory_fraction"] <= 0.9,
                f"当前上限为设备建议工作集的 {request['resource_budget']['mps_memory_fraction']:.0%}。",
                {
                    "execution_strategy": request["execution_strategy"],
                    "mps_memory_fraction": request["resource_budget"]["mps_memory_fraction"],
                },
            ),
            self._check(
                "DISK_FREE",
                "磁盘空间充足",
                system["disk"]["free_bytes"] >= 5 * 1024**3,
                f"当前可用磁盘 {system['disk']['free_bytes']} 字节，最低要求 5368709120 字节。",
            ),
            self._check(
                "RISK_ACKNOWLEDGED",
                "高内存风险已确认",
                request.get("risk_acknowledged") is True,
                profile["risk_message"],
            ),
        ]
        return checks

    @staticmethod
    def _check(
        check_id: str,
        label: str,
        passed: bool,
        message: str,
        details: Any = None,
    ) -> dict[str, Any]:
        return {
            "id": check_id,
            "label": label,
            "status": "passed" if passed else "blocked",
            "message": message,
            "details": details,
        }

    @staticmethod
    def _preflight_result(
        normalized: dict[str, Any] | None,
        checks: list[dict[str, Any]],
        errors: list[dict[str, str]],
    ) -> dict[str, Any]:
        blocked = [check for check in checks if check["status"] == "blocked"]
        return {
            "passed": not errors and not blocked,
            "blocking_count": len(errors) + len(blocked),
            "checks": checks,
            "errors": errors,
            "normalized_request": normalized,
            "checked_at": utc_now(),
        }

    def _find_job_by_execution_id(self, execution_id: str) -> str | None:
        if not self.jobs_root.is_dir():
            return None
        for job_dir in self.jobs_root.iterdir():
            request = read_json(job_dir / "request.json") if job_dir.is_dir() else None
            if request and request.get("execution_id") == execution_id:
                return job_dir.name
        return None

    def _new_job_id(self) -> str:
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        while True:
            value = f"JOB-{stamp}-{secrets.token_hex(4).upper()}"
            if not (self.jobs_root / value).exists():
                return value

    def _job_dir(self, job_id: str) -> Path:
        if not JOB_ID_PATTERN.fullmatch(job_id):
            raise ControlError("INVALID_JOB_ID", "作业标识无效。")
        path = (self.jobs_root / job_id).resolve()
        if not path.is_relative_to(self.jobs_root) or not path.is_dir():
            raise ControlError("JOB_NOT_FOUND", "找不到对应作业。", HTTPStatus.NOT_FOUND)
        return path

    def _load_job(self, job_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
        raw_request = read_json(job_dir / "request.json")
        request, errors = validate_persisted_job(raw_request)
        status = read_json(job_dir / "status.json")
        if errors or request is None or status is None:
            raise ControlError("JOB_CORRUPTED", "作业记录无法验证。", HTTPStatus.CONFLICT, errors)
        request_path = job_dir / "request.json"
        if status.get("request_sha256") != file_sha256(request_path):
            raise ControlError("REQUEST_DIGEST_MISMATCH", "不可变作业请求摘要不匹配。", HTTPStatus.CONFLICT)
        self._read_events(job_dir, limit=None)
        return request, status

    def _append_event(self, job_dir: Path, event_type: str, payload: dict[str, Any]) -> None:
        events = self._read_events(job_dir, limit=None)
        previous = events[-1]["record_sha256"] if events else None
        event = {
            "sequence": len(events) + 1,
            "event_type": event_type,
            "recorded_at": utc_now(),
            "previous_record_sha256": previous,
            "payload": payload,
        }
        canonical = json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        event["record_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        with (job_dir / "events.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())

    @staticmethod
    def _read_events(job_dir: Path, limit: int | None = 100) -> list[dict[str, Any]]:
        path = job_dir / "events.jsonl"
        if not path.is_file():
            return []
        values: list[dict[str, Any]] = []
        previous: str | None = None
        try:
            for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ValueError("事件不是对象")
                record_sha256 = value.get("record_sha256")
                unsigned = {key: item for key, item in value.items() if key != "record_sha256"}
                canonical = json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                expected = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
                if (
                    value.get("sequence") != index
                    or value.get("previous_record_sha256") != previous
                    or not isinstance(record_sha256, str)
                    or not secrets.compare_digest(record_sha256, expected)
                ):
                    raise ValueError("事件摘要链不匹配")
                values.append(value)
                previous = record_sha256
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            raise ControlError("EVENT_CHAIN_INVALID", "作业事件摘要链无法验证。", HTTPStatus.CONFLICT) from None
        except ValueError:
            raise ControlError("EVENT_CHAIN_INVALID", "作业事件摘要链无法验证。", HTTPStatus.CONFLICT) from None
        return values[-limit:] if limit else values

    @staticmethod
    def _terminate_process_tree(process: psutil.Process) -> None:
        children = process.children(recursive=True)
        for child in children:
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                continue
        try:
            process.terminate()
        except psutil.NoSuchProcess:
            pass
        _, alive = psutil.wait_procs([*children, process], timeout=8)
        for item in alive:
            try:
                item.kill()
            except psutil.NoSuchProcess:
                continue

    def _matching_process(
        self,
        request: dict[str, Any],
        status: dict[str, Any],
    ) -> psutil.Process | None:
        pid = status.get("pid")
        create_time = status.get("process_create_time")
        if not isinstance(pid, int) or not isinstance(create_time, (int, float)):
            return None
        try:
            process = psutil.Process(pid)
            if abs(process.create_time() - float(create_time)) > 0.1:
                return None
            command = process.cmdline()
            if "run_provider_compatibility_trial.py" not in " ".join(command):
                return None
            index = command.index("--execution-id")
            if command[index + 1] != request["execution_id"]:
                return None
            return process
        except (psutil.Error, ValueError, IndexError):
            return None

    def _monitor_process(self, job_id: str, process: subprocess.Popen[bytes]) -> None:
        exit_code = process.wait()
        with self._lock:
            try:
                job_dir = self._job_dir(job_id)
                request, status = self._load_job(job_dir)
            except ControlError:
                return
            previous_state = status["state"]
            summary = read_json(self.evidence_root / request["execution_id"] / "summary.json") or {}
            if previous_state in {"STOP_REQUESTED", "STOPPED"} or status.get("stop_requested_at"):
                terminal_state = "STOPPED"
                reason = "LOCAL_OPERATOR_STOP"
            elif exit_code == 0 and summary.get("observation") == "OBSERVED_OUTPUT_AVAILABLE":
                terminal_state = "COMPLETED"
                reason = "OBSERVED_OUTPUT_AVAILABLE"
            else:
                terminal_state = "FAILED"
                reason = summary.get("safety_abort_reason") or summary.get("observation") or "PROCESS_EXITED_WITHOUT_SUMMARY"
            status.update(
                {
                    "state": terminal_state,
                    "updated_at": utc_now(),
                    "finished_at": utc_now(),
                    "exit_code": exit_code,
                    "terminal_reason": reason,
                }
            )
            atomic_write_json(job_dir / "status.json", status)
            self._append_event(
                job_dir,
                "PROCESS_FINISHED",
                {"exit_code": exit_code, "state": terminal_state, "terminal_reason": reason},
            )
            self._processes.pop(job_id, None)

    def _refresh_terminal_state(
        self,
        job_dir: Path,
        request: dict[str, Any],
        status: dict[str, Any],
    ) -> dict[str, Any]:
        summary = read_json(self.evidence_root / request["execution_id"] / "summary.json") or {}
        if status["state"] == "STOP_REQUESTED":
            state = "STOPPED"
            reason = "LOCAL_OPERATOR_STOP"
        elif summary.get("observation") == "OBSERVED_OUTPUT_AVAILABLE":
            state = "COMPLETED"
            reason = summary["observation"]
        else:
            state = "FAILED"
            reason = summary.get("safety_abort_reason") or summary.get("observation") or "PROCESS_NOT_FOUND"
        status.update(
            {
                "state": state,
                "updated_at": utc_now(),
                "finished_at": status.get("finished_at") or utc_now(),
                "terminal_reason": reason,
            }
        )
        atomic_write_json(job_dir / "status.json", status)
        self._append_event(job_dir, "STATE_RECONCILED", {"state": state, "terminal_reason": reason})
        return status


class OperatorHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(
        self,
        address: tuple[str, int],
        manager: JobManager,
        web_root: Path = WEB_ROOT,
    ) -> None:
        self.manager = manager
        self.web_root = web_root.resolve()
        self.csrf_token = secrets.token_urlsafe(32)
        super().__init__(address, OperatorHandler)


class OperatorHandler(BaseHTTPRequestHandler):
    server_version = "SenknetOperator/1.0"

    @property
    def control_server(self) -> OperatorHTTPServer:
        return self.server  # type: ignore[return-value]

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlsplit(self.path)
        if parsed.path == "/api/v1/health":
            self._json({"status": "ok", "mode": "LOCAL_CONTROLLED_EXECUTION", "generated_at": utc_now()})
            return
        if parsed.path == "/api/v1/operator":
            value = self.control_server.manager.overview()
            value["csrf_token"] = self.control_server.csrf_token
            self._json(value)
            return
        match = re.fullmatch(r"/api/v1/jobs/(JOB-[A-Z0-9-]+)", parsed.path)
        if match:
            self._execute(lambda: self.control_server.manager.job_detail(match.group(1)))
            return
        self._serve_static(parsed.path)

    def do_POST(self) -> None:  # noqa: N802
        if self.headers.get("X-Senknet-CSRF") != self.control_server.csrf_token:
            self._json(
                {"error": {"code": "CSRF_REJECTED", "message": "控制令牌缺失或不匹配。"}},
                HTTPStatus.FORBIDDEN,
            )
            return
        body = self._read_body()
        if body is None:
            return
        path = urlsplit(self.path).path
        if path == "/api/v1/preflight":
            self._execute(lambda: self.control_server.manager.preflight(body))
            return
        if path == "/api/v1/jobs":
            self._execute(lambda: self.control_server.manager.create_job(body), HTTPStatus.CREATED)
            return
        start = re.fullmatch(r"/api/v1/jobs/(JOB-[A-Z0-9-]+)/start", path)
        if start:
            confirmation = str(body.get("confirmation_execution_id", ""))
            self._execute(lambda: self.control_server.manager.start_job(start.group(1), confirmation))
            return
        stop = re.fullmatch(r"/api/v1/jobs/(JOB-[A-Z0-9-]+)/stop", path)
        if stop:
            self._execute(lambda: self.control_server.manager.stop_job(stop.group(1)))
            return
        self._json({"error": {"code": "NOT_FOUND", "message": "接口不存在。"}}, HTTPStatus.NOT_FOUND)

    def _read_body(self) -> dict[str, Any] | None:
        if self.headers.get_content_type() != "application/json":
            self._json(
                {"error": {"code": "CONTENT_TYPE_REQUIRED", "message": "请求必须使用 application/json。"}},
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            )
            return None
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_REQUEST_BYTES:
            self._json(
                {"error": {"code": "INVALID_BODY_SIZE", "message": "请求正文为空或超过限制。"}},
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            )
            return None
        try:
            value = json.loads(self.rfile.read(length))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._json({"error": {"code": "INVALID_JSON", "message": "请求不是有效 JSON。"}}, HTTPStatus.BAD_REQUEST)
            return None
        if not isinstance(value, dict):
            self._json({"error": {"code": "INVALID_BODY", "message": "请求正文必须是对象。"}}, HTTPStatus.BAD_REQUEST)
            return None
        return value

    def _execute(self, action: Any, success_status: HTTPStatus = HTTPStatus.OK) -> None:
        try:
            value = action()
        except ControlError as exc:
            self._json(
                {"error": {"code": exc.code, "message": exc.message, "details": exc.details}},
                exc.status,
            )
            return
        self._json(value, success_status)

    def _serve_static(self, raw_path: str) -> None:
        relative = "index.html" if raw_path in {"", "/"} else unquote(raw_path.lstrip("/"))
        candidate = (self.control_server.web_root / relative).resolve()
        if not candidate.is_relative_to(self.control_server.web_root) or not candidate.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        body = candidate.read_bytes()
        self.send_response(HTTPStatus.OK)
        self._security_headers()
        self.send_header("Content-Type", mimetypes.guess_type(candidate.name)[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, value: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self._security_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "img-src 'self' data:; connect-src 'self'; object-src 'none'; "
            "frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
        )

    def log_message(self, format_string: str, *args: Any) -> None:
        print(f"[{self.log_date_time_string()}] {self.client_address[0]} {format_string % args}")


def create_server(
    host: str = "127.0.0.1",
    port: int = 4320,
    manager: JobManager | None = None,
    web_root: Path = WEB_ROOT,
) -> OperatorHTTPServer:
    if host not in {"127.0.0.1", "::1", "localhost"}:
        raise ValueError("作业控制台只允许绑定本机回环地址")
    return OperatorHTTPServer((host, port), manager or JobManager(), web_root)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="启动 SENKNET 本地视频作业控制台")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4320)
    parser.add_argument("--state-root", type=Path, default=DEFAULT_STATE_ROOT)
    parser.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    parser.add_argument("--cache-root", type=Path, default=DEFAULT_CACHE_ROOT)
    parser.add_argument("--open", action="store_true", help="启动后打开默认浏览器")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manager = JobManager(
        repo_root=REPO_ROOT,
        state_root=args.state_root,
        evidence_root=args.evidence_root,
        cache_root=args.cache_root,
        python_executable=sys.executable,
        runner_path=RUNNER_PATH,
    )
    try:
        server = create_server(args.host, args.port, manager)
    except (OSError, ValueError) as exc:
        print(f"无法启动作业控制台：{exc}")
        return 2
    host = "127.0.0.1" if args.host == "localhost" else args.host
    url = f"http://{host}:{server.server_address[1]}"
    print(f"SENKNET 本地作业控制台已启动：{url}")
    print("受控执行模式；按 Ctrl+C 停止控制服务，不会自动启动作业。")
    if args.open:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever(poll_interval=0.3)
    except KeyboardInterrupt:
        print("\n正在停止作业控制台……")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
