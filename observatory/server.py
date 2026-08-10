#!/usr/bin/env python3
"""零额外依赖、只读、仅本机开放的视频构建观测服务。"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import subprocess
import threading
import webbrowser
from dataclasses import dataclass
from datetime import UTC, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qs, unquote, urlsplit

import psutil


REPO_ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = Path(__file__).resolve().parent / "web"
DEFAULT_EVIDENCE_ROOT = REPO_ROOT / "evidence" / "runtime"
DEFAULT_CACHE_ROOT = Path.home() / ".cache" / "huggingface" / "hub"
EXECUTION_ID_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9._-]{2,127}")
PRIVATE_PATH_PATTERNS = (
    re.compile(r"/Users/[^/\s]+"),
    re.compile(r"/home/[^/\s]+"),
)
MEDIA_FILES = frozenset({"output.mp4", "thumbnail.png"})
MAX_JSON_BYTES = 4 * 1024 * 1024
MAX_LOG_BYTES = 96 * 1024
MAX_METRIC_POINTS = 420
GIB = 1024**3

MODEL_SPECS = (
    {
        "key": "wan",
        "name": "Wan2.1-T2V-1.3B",
        "model_id": "Wan-AI/Wan2.1-T2V-1.3B-Diffusers",
        "cache_name": "models--Wan-AI--Wan2.1-T2V-1.3B-Diffusers",
        "observed_revision": "0fad780a534b6463e45facd96134c9f345acfa5b",
    },
    {
        "key": "cogvideox",
        "name": "CogVideoX-2B",
        "model_id": "zai-org/CogVideoX-2b",
        "cache_name": "models--zai-org--CogVideoX-2b",
        "observed_revision": "1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01",
    },
)

STAGE_DEFINITIONS = (
    ("registered", "执行登记", "固定请求与执行标识"),
    ("environment", "环境取证", "依赖、设备与版本上下文"),
    ("snapshot", "模型快照", "解析并固定模型修订"),
    ("pipeline", "管线装载", "构建提供者运行管线"),
    ("mps", "Metal 转移", "进入 MPS 执行上下文"),
    ("inference", "推理生成", "执行固定输入的模型推理"),
    ("export", "视频导出", "编码输出并提取缩略图"),
    ("evidence", "证据闭包", "形成摘要、清单与可审计载体"),
)

PHASE_TO_STAGE = {
    "WORKER_STARTED": "snapshot",
    "RESOLVING_MODEL_SNAPSHOT": "snapshot",
    "ENCODING_PROMPT": "pipeline",
    "LOADING_DENOISER_PIPELINE": "pipeline",
    "LOADING_PIPELINE": "pipeline",
    "TRANSFERRING_TO_MPS": "mps",
    "CONFIGURING_MPS_BUDGET": "mps",
    "ACTIVATING_MPS_STRATEGY": "mps",
    "RELEASING_MPS_MEMORY": "mps",
    "RUNNING_INFERENCE": "inference",
    "EXPORTING_VIDEO": "export",
    "WORKER_COMPLETED": "evidence",
}


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def classify_memory_pressure(total_bytes: int, available_bytes: int, swap_used_bytes: int) -> tuple[str, str]:
    """同时依据即时可用内存和换页残留判定本机资源状态。"""
    available_ratio = available_bytes / total_bytes if total_bytes else 0
    if available_ratio < 0.08:
        return "critical", "AVAILABLE_MEMORY_CRITICAL"
    if available_ratio < 0.18:
        return "elevated", "AVAILABLE_MEMORY_LOW"
    if swap_used_bytes >= 4 * GIB:
        return "recovering", "SWAP_RESIDUE_HIGH"
    return "healthy", "RESOURCE_READY"


def safe_json(path: Path) -> dict[str, Any] | None:
    try:
        if not path.is_file() or path.stat().st_size > MAX_JSON_BYTES:
            return None
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def sanitize_text(value: str, repo_root: Path) -> str:
    sanitized = value.replace(str(repo_root), "<repo>")
    sanitized = sanitized.replace(str(Path.home()), "<home>")
    for pattern in PRIVATE_PATH_PATTERNS:
        sanitized = pattern.sub("<private-user-path>", sanitized)
    return sanitized


def read_log_tail(path: Path, repo_root: Path) -> str:
    if not path.is_file():
        return ""
    try:
        size = path.stat().st_size
        with path.open("rb") as handle:
            if size > MAX_LOG_BYTES:
                handle.seek(-MAX_LOG_BYTES, os.SEEK_END)
                handle.readline()
            data = handle.read(MAX_LOG_BYTES)
        return sanitize_text(data.decode("utf-8", errors="replace"), repo_root)
    except OSError:
        return ""


def read_jsonl(path: Path, limit: int = MAX_METRIC_POINTS) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.is_file():
        return rows
    try:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(row, dict):
                    rows.append(row)
    except (OSError, UnicodeDecodeError):
        return []
    return downsample(rows, limit)


def downsample(rows: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    if len(rows) <= limit or limit < 2:
        return rows
    indexes = {round(index * (len(rows) - 1) / (limit - 1)) for index in range(limit)}
    return [rows[index] for index in sorted(indexes)]


def directory_size(path: Path) -> tuple[int, int]:
    total = 0
    count = 0
    try:
        for child in path.rglob("*"):
            if child.is_file() and not child.is_symlink():
                total += child.stat().st_size
                count += 1
    except OSError:
        pass
    return total, count


def git_value(repo_root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=2,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() or None if result.returncode == 0 else None


def classify_evidence_package(path: Path) -> str:
    names = {item.name for item in path.iterdir() if item.is_file()}
    if "worker_state.json" in names or "request.json" in names:
        return "provider_trial"
    if "write_attempts.jsonl" in names:
        return "protected_write"
    if "replay_summary.json" in names:
        return "correctness"
    if "migration_summary.json" in names:
        return "migration"
    return "evidence"


def extract_execution_id(command: list[str]) -> str | None:
    try:
        value = command[command.index("--execution-id") + 1]
    except (ValueError, IndexError):
        return None
    return value if EXECUTION_ID_PATTERN.fullmatch(value) else None


@dataclass(frozen=True)
class ObservatoryConfig:
    repo_root: Path = REPO_ROOT
    evidence_root: Path = DEFAULT_EVIDENCE_ROOT
    cache_root: Path = DEFAULT_CACHE_ROOT
    web_root: Path = WEB_ROOT


class ObservatoryState:
    """聚合只读事实，不创建运行、裁决或制度状态。"""

    def __init__(self, config: ObservatoryConfig | None = None) -> None:
        self.config = config or ObservatoryConfig()
        self._model_cache_lock = threading.Lock()
        self._model_cache_at = 0.0
        self._model_cache_value: list[dict[str, Any]] = []
        psutil.cpu_percent(interval=None)

    def dashboard(self, execution_id: str | None = None) -> dict[str, Any]:
        processes = self.active_processes()
        executions = self.provider_executions(processes)
        selected_id = self.select_execution(execution_id, processes, executions)
        system = self.system_status()
        selected = self.execution_detail(selected_id, processes, system) if selected_id else None
        return {
            "schema_version": "observatory.v1",
            "generated_at": utc_now(),
            "refresh_after_ms": 1000,
            "mode": "LOCAL_READ_ONLY",
            "project": self.project_status(),
            "system": system,
            "runtime": {
                "active": bool(processes),
                "process_count": len(processes),
                "processes": processes,
            },
            "models": self.model_statuses(),
            "executions": executions,
            "evidence_packages": self.evidence_packages(),
            "selected_execution": selected,
            "governance_boundary": {
                "observation_only": True,
                "can_start_generation": False,
                "can_create_formal_fact": False,
                "can_create_institution_freeze": False,
                "statement": "观测台只投影既有现实，不执行生成、不裁决通过、不建立正式事实。",
            },
        }

    def project_status(self) -> dict[str, Any]:
        head = git_value(self.config.repo_root, "rev-parse", "HEAD")
        status = git_value(self.config.repo_root, "status", "--porcelain") or ""
        return {
            "name": "SENK 视频生产治理引擎",
            "repository": "senk-io/senk-video-generator",
            "branch": git_value(self.config.repo_root, "branch", "--show-current"),
            "git_head": head[:12] if head else None,
            "worktree_dirty": bool(status),
            "license": "Apache-2.0" if (self.config.repo_root / "LICENSE").is_file() else None,
        }

    def system_status(self) -> dict[str, Any]:
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk = psutil.disk_usage(self.config.repo_root)
        pressure, pressure_reason = classify_memory_pressure(memory.total, memory.available, swap.used)
        return {
            "cpu_percent": round(psutil.cpu_percent(interval=None), 1),
            "logical_cpu_count": psutil.cpu_count(logical=True),
            "memory": {
                "total_bytes": memory.total,
                "used_bytes": memory.total - memory.available,
                "available_bytes": memory.available,
                "used_percent": round((memory.total - memory.available) / memory.total * 100, 1),
                "pressure": pressure,
                "pressure_reason": pressure_reason,
            },
            "swap": {
                "total_bytes": swap.total,
                "used_bytes": swap.used,
                "used_percent": round(swap.percent, 1),
            },
            "disk": {
                "total_bytes": disk.total,
                "used_bytes": disk.used,
                "free_bytes": disk.free,
                "used_percent": round(disk.percent, 1),
            },
        }

    def active_processes(self) -> list[dict[str, Any]]:
        found: list[dict[str, Any]] = []
        for process in psutil.process_iter(
            ["pid", "name", "cmdline", "create_time", "status", "memory_info"]
        ):
            try:
                command = process.info.get("cmdline") or []
                joined = " ".join(command)
                if "run_provider_compatibility_trial.py" not in joined:
                    continue
                if str(self.config.repo_root) not in joined and "--execution-id" not in command:
                    continue
                execution_id = extract_execution_id(command)
                memory_info = process.info.get("memory_info")
                found.append(
                    {
                        "pid": process.info["pid"],
                        "role": "worker" if "--worker" in command else "orchestrator",
                        "execution_id": execution_id,
                        "status": process.info.get("status"),
                        "rss_bytes": memory_info.rss if memory_info else 0,
                        "running_seconds": max(0, round(datetime.now().timestamp() - process.info["create_time"], 1)),
                    }
                )
            except (psutil.Error, OSError, KeyError, TypeError):
                continue
        return sorted(found, key=lambda item: (item["execution_id"] or "", item["role"]))

    def provider_executions(self, processes: list[dict[str, Any]]) -> list[dict[str, Any]]:
        active_ids = {item["execution_id"] for item in processes if item["execution_id"]}
        values: list[dict[str, Any]] = []
        if not self.config.evidence_root.is_dir():
            return values
        for path in self.config.evidence_root.iterdir():
            if not path.is_dir() or not EXECUTION_ID_PATTERN.fullmatch(path.name):
                continue
            request = safe_json(path / "request.json")
            worker = safe_json(path / "worker_state.json") or {}
            summary = safe_json(path / "summary.json") or {}
            if not request or not isinstance(request.get("provider"), dict):
                continue
            lifecycle = derive_lifecycle(path, worker, summary, path.name in active_ids)
            values.append(
                {
                    "execution_id": path.name,
                    "provider_key": request.get("provider_key"),
                    "model_id": request["provider"].get("model_id"),
                    "created_at": request.get("created_at"),
                    "finished_at": summary.get("finished_at") or worker.get("finished_at"),
                    "state": lifecycle["state"],
                    "phase": lifecycle["phase"],
                    "progress_percent": lifecycle["progress_percent"],
                    "active": path.name in active_ids,
                    "observation": summary.get("observation"),
                }
            )
        return sorted(
            values,
            key=lambda item: item["created_at"] or "",
            reverse=True,
        )

    def select_execution(
        self,
        requested: str | None,
        processes: list[dict[str, Any]],
        executions: list[dict[str, Any]],
    ) -> str | None:
        known = {item["execution_id"] for item in executions}
        if requested in known:
            return requested
        for process in processes:
            if process["execution_id"] in known:
                return process["execution_id"]
        return executions[0]["execution_id"] if executions else None

    def execution_detail(
        self,
        execution_id: str,
        processes: list[dict[str, Any]],
        system: dict[str, Any],
    ) -> dict[str, Any] | None:
        path = self.config.evidence_root / execution_id
        if not path.is_dir() or not EXECUTION_ID_PATTERN.fullmatch(execution_id):
            return None
        request = safe_json(path / "request.json") or {}
        environment = safe_json(path / "environment.json") or {}
        worker = safe_json(path / "worker_state.json") or {}
        summary = safe_json(path / "summary.json") or {}
        manifest = safe_json(path / "manifest.json") or {}
        active = any(item["execution_id"] == execution_id for item in processes)
        lifecycle = derive_lifecycle(path, worker, summary, active)
        process_metrics = read_jsonl(path / "process_metrics.jsonl")
        mps_metrics = read_jsonl(path / "mps_metrics.jsonl")
        files = evidence_files(path, manifest)
        warnings = derive_warnings(summary, lifecycle, system)
        provider = request.get("provider") if isinstance(request.get("provider"), dict) else {}
        output_metadata = summary.get("output_metadata") or worker.get("output_metadata") or {}
        return {
            "execution_id": execution_id,
            "provider_key": request.get("provider_key") or worker.get("provider_key") or summary.get("provider_key"),
            "provider_identity": provider.get("provider_identity") or summary.get("provider_identity"),
            "model_id": provider.get("model_id") or summary.get("model_id"),
            "snapshot_revision": worker.get("model_snapshot_revision") or summary.get("model_snapshot_revision"),
            "lifecycle": lifecycle,
            "warnings": warnings,
            "request": {
                "contract_id": request.get("contract_id"),
                "created_at": request.get("created_at"),
                "prompt": request.get("prompt"),
                "seed": request.get("seed"),
                "device": request.get("device"),
                "timeout_seconds": request.get("timeout_seconds"),
                "parameters": {
                    key: provider.get(key)
                    for key in (
                        "dtype",
                        "vae_dtype",
                        "height",
                        "width",
                        "num_frames",
                        "num_inference_steps",
                        "guidance_scale",
                        "fps",
                    )
                    if provider.get(key) is not None
                },
            },
            "environment": {
                key: environment.get(key)
                for key in (
                    "operating_system",
                    "operating_system_version",
                    "architecture",
                    "processor",
                    "physical_memory_bytes",
                    "python_version",
                    "torch_version",
                    "diffusers_version",
                    "transformers_version",
                    "mps_built",
                    "mps_available",
                    "mps_recommended_max_memory_bytes",
                    "git_head",
                )
                if environment.get(key) is not None
            },
            "observation": {
                "value": summary.get("observation"),
                "last_phase": summary.get("last_phase") or worker.get("phase"),
                "worker_exit_code": summary.get("worker_exit_code"),
                "timed_out": summary.get("timed_out"),
                "started_at": summary.get("started_at") or worker.get("started_at"),
                "finished_at": summary.get("finished_at") or worker.get("finished_at"),
                "elapsed_seconds": summary.get("elapsed_seconds") or latest_elapsed(process_metrics),
                "error": worker.get("error_observation") or summary.get("error_observation"),
            },
            "stage_elapsed_seconds": worker.get("stage_elapsed_seconds") or summary.get("stage_elapsed_seconds") or {},
            "resource_summary": resource_summary(summary, process_metrics, mps_metrics),
            "process_metrics": process_metrics,
            "mps_metrics": mps_metrics,
            "output": {
                "available": (path / "output.mp4").is_file(),
                "video_url": f"/media/{execution_id}/output.mp4" if (path / "output.mp4").is_file() else None,
                "thumbnail_url": f"/media/{execution_id}/thumbnail.png" if (path / "thumbnail.png").is_file() else None,
                "bytes": summary.get("output_bytes"),
                "sha256": summary.get("output_sha256"),
                "metadata": output_metadata,
            },
            "evidence": {
                "manifest_present": bool(manifest),
                "manifest_declared_file_count": manifest.get("file_count"),
                "actual_file_count": len(files),
                "files": files,
                "formal_fact_created": bool(summary.get("formal_fact_created")),
                "cross_provider_contract_created": bool(summary.get("cross_provider_contract_created")),
                "institution_freeze_created": bool(summary.get("institution_freeze_created")),
            },
            "log_tail": read_log_tail(path / "runtime.log", self.config.repo_root),
        }

    def evidence_packages(self) -> list[dict[str, Any]]:
        packages: list[dict[str, Any]] = []
        if not self.config.evidence_root.is_dir():
            return packages
        for path in self.config.evidence_root.iterdir():
            if not path.is_dir():
                continue
            summary = safe_json(path / "summary.json") or {}
            manifest = safe_json(path / "manifest.json") or {}
            try:
                modified_at = datetime.fromtimestamp(path.stat().st_mtime, UTC).isoformat()
            except OSError:
                modified_at = None
            packages.append(
                {
                    "execution_id": path.name,
                    "kind": classify_evidence_package(path),
                    "result": summary.get("observation") or summary.get("result") or "SUMMARY_UNAVAILABLE",
                    "manifest_present": bool(manifest),
                    "declared_file_count": manifest.get("file_count"),
                    "formal_fact_created": bool(summary.get("formal_fact_created")),
                    "institution_freeze_created": bool(summary.get("institution_freeze_created")),
                    "modified_at": modified_at,
                }
            )
        return sorted(packages, key=lambda item: item["modified_at"] or "", reverse=True)

    def model_statuses(self) -> list[dict[str, Any]]:
        import time

        now = time.monotonic()
        with self._model_cache_lock:
            if self._model_cache_value and now - self._model_cache_at < 15:
                return self._model_cache_value
            values = [self._model_status(spec) for spec in MODEL_SPECS]
            self._model_cache_value = values
            self._model_cache_at = now
            return values

    def _model_status(self, spec: dict[str, str]) -> dict[str, Any]:
        root = self.config.cache_root / spec["cache_name"]
        snapshots_root = root / "snapshots"
        revisions = []
        if snapshots_root.is_dir():
            revisions = sorted(item.name for item in snapshots_root.iterdir() if item.is_dir())
        incomplete_count = 0
        if root.is_dir():
            try:
                incomplete_count = sum(1 for _ in root.rglob("*.incomplete"))
            except OSError:
                incomplete_count = 0
        size_bytes, blob_file_count = directory_size(root / "blobs") if root.is_dir() else (0, 0)
        observed_present = spec["observed_revision"] in revisions
        if incomplete_count:
            state = "downloading"
        elif observed_present:
            state = "ready"
        elif revisions:
            state = "available_other_revision"
        else:
            state = "not_downloaded"
        snapshot_file_count = 0
        observed_path = snapshots_root / spec["observed_revision"]
        if observed_path.is_dir():
            try:
                snapshot_file_count = sum(1 for item in observed_path.rglob("*") if item.is_file())
            except OSError:
                snapshot_file_count = 0
        return {
            "key": spec["key"],
            "name": spec["name"],
            "model_id": spec["model_id"],
            "state": state,
            "observed_revision": spec["observed_revision"],
            "observed_revision_present": observed_present,
            "available_revisions": revisions,
            "cache_bytes": size_bytes,
            "blob_file_count": blob_file_count,
            "snapshot_file_count": snapshot_file_count,
            "incomplete_file_count": incomplete_count,
        }


def latest_elapsed(rows: list[dict[str, Any]]) -> float | None:
    value = rows[-1].get("elapsed_seconds") if rows else None
    return float(value) if isinstance(value, (int, float)) else None


def max_metric(rows: Iterable[dict[str, Any]], field: str) -> int | float | None:
    values = [row.get(field) for row in rows]
    numeric = [value for value in values if isinstance(value, (int, float))]
    return max(numeric) if numeric else None


def resource_summary(
    summary: dict[str, Any],
    process_metrics: list[dict[str, Any]],
    mps_metrics: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "process_tree_peak_rss_bytes": summary.get("process_tree_peak_rss_bytes")
        or max_metric(process_metrics, "process_tree_rss_bytes"),
        "system_peak_used_bytes": summary.get("system_peak_used_bytes")
        or max_metric(process_metrics, "system_used_bytes"),
        "system_peak_swap_used_bytes": summary.get("system_peak_swap_used_bytes")
        or max_metric(process_metrics, "swap_used_bytes"),
        "system_start_swap_used_bytes": summary.get("system_start_swap_used_bytes"),
        "mps_peak_current_allocated_bytes": summary.get("mps_peak_current_allocated_bytes")
        or max_metric(mps_metrics, "mps_current_allocated_bytes"),
        "mps_peak_driver_allocated_bytes": summary.get("mps_peak_driver_allocated_bytes")
        or max_metric(mps_metrics, "mps_driver_allocated_bytes"),
    }


def evidence_files(path: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    declared = {
        item.get("path"): item
        for item in manifest.get("files", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    values = []
    try:
        children = sorted(item for item in path.iterdir() if item.is_file())
    except OSError:
        return values
    for child in children:
        try:
            size = child.stat().st_size
        except OSError:
            continue
        declaration = declared.get(child.name, {})
        values.append(
            {
                "name": child.name,
                "bytes": size,
                "manifested": child.name == "manifest.json" or child.name in declared,
                "sha256": declaration.get("sha256"),
            }
        )
    return values


def derive_lifecycle(
    path: Path,
    worker: dict[str, Any],
    summary: dict[str, Any],
    active: bool,
) -> dict[str, Any]:
    completed = {
        "registered": (path / "request.json").is_file(),
        "environment": (path / "environment.json").is_file(),
        "snapshot": bool(worker.get("model_snapshot_resolved") or summary.get("model_snapshot_resolved")),
        "pipeline": bool(worker.get("pipeline_loaded") or summary.get("pipeline_loaded")),
        "mps": bool(worker.get("mps_transfer_completed") or summary.get("mps_transfer_completed")),
        "inference": bool(worker.get("inference_completed") or summary.get("inference_completed")),
        "export": bool(worker.get("output_export_completed") or summary.get("output_export_completed")),
        "evidence": (path / "summary.json").is_file() and (path / "manifest.json").is_file(),
    }
    phase = worker.get("phase") or summary.get("last_phase") or "NOT_STARTED"
    active_stage = PHASE_TO_STAGE.get(phase)
    if not active_stage:
        active_stage = next((stage_id for stage_id, _, _ in STAGE_DEFINITIONS if not completed[stage_id]), None)
    failed = phase == "WORKER_FAILED" or (
        bool(summary) and summary.get("observation") == "OBSERVED_EXECUTION_WITHOUT_OUTPUT"
    )
    if failed:
        state = "failed_observation"
    elif summary.get("observation") == "OBSERVED_OUTPUT_AVAILABLE":
        state = "completed_observation"
    elif active:
        state = "active"
    elif all(completed.values()):
        state = "completed_evidence"
    elif any(completed.values()):
        state = "interrupted_or_waiting"
    else:
        state = "unknown"
    stages = []
    for stage_id, label, description in STAGE_DEFINITIONS:
        if completed[stage_id]:
            status = "completed"
        elif failed and stage_id == active_stage:
            status = "failed"
        elif active and stage_id == active_stage:
            status = "active"
        else:
            status = "pending"
        stages.append(
            {
                "id": stage_id,
                "label": label,
                "description": description,
                "status": status,
            }
        )
    completed_count = sum(completed.values())
    progress = completed_count / len(STAGE_DEFINITIONS) * 100
    if active and active_stage and not completed[active_stage]:
        progress += 100 / len(STAGE_DEFINITIONS) * 0.35
    return {
        "state": state,
        "phase": phase,
        "active_stage": active_stage,
        "progress_percent": round(min(progress, 100), 1),
        "stages": stages,
    }


def derive_warnings(
    summary: dict[str, Any], lifecycle: dict[str, Any], system: dict[str, Any]
) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []
    pressure = system["memory"]["pressure"]
    if pressure in {"elevated", "critical"}:
        warnings.append(
            {
                "severity": pressure,
                "code": "LIVE_MEMORY_PRESSURE",
                "message": "当前系统可用内存偏低，请避免同时启动新的高内存生成。",
            }
        )
    if pressure == "recovering":
        warnings.append(
            {
                "severity": "elevated",
                "code": "LIVE_SWAP_RECOVERY",
                "message": "当前可用内存已经恢复，但换页残留仍高；新的高内存生成应保持阻断。",
            }
        )
    swap_start = summary.get("system_start_swap_used_bytes")
    swap_peak = summary.get("system_peak_swap_used_bytes")
    if isinstance(swap_start, (int, float)) and isinstance(swap_peak, (int, float)):
        delta = swap_peak - swap_start
        if delta > 1024**3:
            warnings.append(
                {
                    "severity": "elevated",
                    "code": "EXECUTION_SWAP_GROWTH",
                    "message": f"该次执行的交换空间峰值较启动时增加 {delta / 1024**3:.1f} GiB。",
                }
            )
    if lifecycle["state"] == "failed_observation":
        warnings.append(
            {
                "severity": "critical",
                "code": "EXECUTION_WITHOUT_OUTPUT",
                "message": "本次现实未形成可用输出；请查看失败观察和日志。",
            }
        )
    if lifecycle["state"] == "interrupted_or_waiting":
        warnings.append(
            {
                "severity": "elevated",
                "code": "EXECUTION_NOT_RUNNING",
                "message": "存在未闭合执行目录，但当前未检测到对应运行进程。",
            }
        )
    return warnings


class ObservatoryHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], state: ObservatoryState) -> None:
        self.observatory_state = state
        super().__init__(address, ObservatoryHandler)


class ObservatoryHandler(BaseHTTPRequestHandler):
    server_version = "SenknetObservatory/1.0"

    @property
    def state(self) -> ObservatoryState:
        return self.server.observatory_state  # type: ignore[attr-defined]

    def do_GET(self) -> None:  # noqa: N802
        self._route(send_body=True)

    def do_HEAD(self) -> None:  # noqa: N802
        self._route(send_body=False)

    def _route(self, send_body: bool) -> None:
        parsed = urlsplit(self.path)
        if parsed.path == "/api/v1/health":
            self._json_response(
                {"status": "ok", "mode": "LOCAL_READ_ONLY", "generated_at": utc_now()},
                send_body=send_body,
            )
            return
        if parsed.path == "/api/v1/dashboard":
            execution_id = parse_qs(parsed.query).get("execution_id", [None])[0]
            if execution_id is not None and not EXECUTION_ID_PATTERN.fullmatch(execution_id):
                self._json_response({"error": "invalid_execution_id"}, HTTPStatus.BAD_REQUEST, send_body)
                return
            self._json_response(self.state.dashboard(execution_id), send_body=send_body)
            return
        if parsed.path.startswith("/media/"):
            self._serve_media(parsed.path, send_body)
            return
        self._serve_static(parsed.path, send_body)

    def _serve_static(self, raw_path: str, send_body: bool) -> None:
        relative = "index.html" if raw_path in {"", "/"} else unquote(raw_path.lstrip("/"))
        root = self.state.config.web_root.resolve()
        candidate = (root / relative).resolve()
        if not candidate.is_relative_to(root) or not candidate.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        self._file_response(candidate, send_body, allow_range=False)

    def _serve_media(self, raw_path: str, send_body: bool) -> None:
        parts = [unquote(part) for part in raw_path.split("/") if part]
        if len(parts) != 3 or parts[0] != "media":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        _, execution_id, filename = parts
        if not EXECUTION_ID_PATTERN.fullmatch(execution_id) or filename not in MEDIA_FILES:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        root = self.state.config.evidence_root.resolve()
        candidate = (root / execution_id / filename).resolve()
        if not candidate.is_relative_to(root) or not candidate.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        self._file_response(candidate, send_body, allow_range=True)

    def _json_response(
        self,
        value: dict[str, Any],
        status: HTTPStatus = HTTPStatus.OK,
        send_body: bool = True,
    ) -> None:
        body = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self._security_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if send_body:
            self.wfile.write(body)

    def _file_response(self, path: Path, send_body: bool, allow_range: bool) -> None:
        size = path.stat().st_size
        start = 0
        end = size - 1
        status = HTTPStatus.OK
        range_header = self.headers.get("Range") if allow_range else None
        if range_header:
            match = re.fullmatch(r"bytes=(\d*)-(\d*)", range_header.strip())
            if not match:
                self.send_error(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                return
            left, right = match.groups()
            if left:
                start = int(left)
                end = int(right) if right else end
            elif right:
                length = int(right)
                start = max(0, size - length)
            if start > end or start >= size:
                self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return
            end = min(end, size - 1)
            status = HTTPStatus.PARTIAL_CONTENT
        length = max(0, end - start + 1)
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(status)
        self._security_headers()
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(length))
        self.send_header("Accept-Ranges", "bytes" if allow_range else "none")
        if status == HTTPStatus.PARTIAL_CONTENT:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Cache-Control", "no-store" if allow_range else "no-cache")
        self.end_headers()
        if not send_body:
            return
        with path.open("rb") as handle:
            handle.seek(start)
            remaining = length
            while remaining:
                chunk = handle.read(min(64 * 1024, remaining))
                if not chunk:
                    break
                self.wfile.write(chunk)
                remaining -= len(chunk)

    def _security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "img-src 'self' data:; media-src 'self'; connect-src 'self'; "
            "object-src 'none'; frame-ancestors 'none'; base-uri 'none'",
        )

    def log_message(self, format_string: str, *args: Any) -> None:
        message = format_string % args
        print(f"[{self.log_date_time_string()}] {self.client_address[0]} {message}")


def create_server(
    host: str = "127.0.0.1",
    port: int = 4319,
    state: ObservatoryState | None = None,
) -> ObservatoryHTTPServer:
    if host not in {"127.0.0.1", "::1", "localhost"}:
        raise ValueError("观测台只允许绑定本机回环地址")
    return ObservatoryHTTPServer((host, port), state or ObservatoryState())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="启动 SENKNET 本地视频构建观测台")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4319)
    parser.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    parser.add_argument("--cache-root", type=Path, default=DEFAULT_CACHE_ROOT)
    parser.add_argument("--open", action="store_true", help="启动后打开默认浏览器")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = ObservatoryConfig(
        repo_root=REPO_ROOT,
        evidence_root=args.evidence_root.resolve(),
        cache_root=args.cache_root.resolve(),
        web_root=WEB_ROOT,
    )
    state = ObservatoryState(config)
    try:
        server = create_server(args.host, args.port, state)
    except (OSError, ValueError) as exc:
        print(f"无法启动观测台：{exc}")
        return 2
    host = "127.0.0.1" if args.host == "localhost" else args.host
    url = f"http://{host}:{server.server_address[1]}"
    print(f"SENKNET 本地观测台已启动：{url}")
    print("只读模式；按 Ctrl+C 停止。")
    if args.open:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever(poll_interval=0.3)
    except KeyboardInterrupt:
        print("\n正在停止观测台……")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
