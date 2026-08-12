"""MiniMax H3 开放平台 V2 视频生成适配器。"""

from __future__ import annotations

import hashlib
import json
import re
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen


MINIMAX_H3_API_BASE = "https://api.minimax.io"
MINIMAX_H3_API_KEY_ENV = "MINIMAX_API_KEY"
MINIMAX_H3_MODEL_ID = "MiniMax-H3"
MINIMAX_H3_PROVIDER_KEY = "minimax_h3"
EXECUTION_ID_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9._-]{2,127}")
TASK_ID_PATTERN = re.compile(r"[A-Za-z0-9_-]{1,128}")
TERMINAL_STATUSES = frozenset({"succeeded", "failed", "cancelled"})
REQUIRED_NON_GOALS = frozenset(
    {
        "visual_quality_acceptance",
        "formal_selection_decision",
        "timeline_binding",
        "production_readiness",
        "automatic_retry",
        "institution_freeze",
        "cross_provider_contract_creation",
        "real_person_representation",
    }
)


class AdapterError(RuntimeError):
    """提供者调用失败，且错误内容已经限制为可公开观察。"""

    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}

    def observation(self) -> dict[str, Any]:
        return {"code": self.code, "message": self.message, "details": self.details}


class MiniMaxH3Transport(Protocol):
    def create(self, payload: dict[str, Any]) -> dict[str, Any]: ...

    def query(self, task_id: str) -> dict[str, Any]: ...

    def cancel(self, task_id: str) -> dict[str, Any]: ...

    def download(self, url: str, destination: Path, max_bytes: int) -> dict[str, Any]: ...


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def write_manifest(evidence_dir: Path) -> dict[str, Any]:
    entries = []
    for path in sorted(evidence_dir.rglob("*")):
        if not path.is_file() or path.name == "manifest.json":
            continue
        entries.append(
            {
                "path": str(path.relative_to(evidence_dir)),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    manifest = {"created_at": utc_now(), "file_count": len(entries), "files": entries}
    write_json(evidence_dir / "manifest.json", manifest)
    return manifest


def _integer(value: Any, field: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field} 必须是整数")
    try:
        normalized = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} 必须是整数") from exc
    if not minimum <= normalized <= maximum:
        raise ValueError(f"{field} 必须位于 {minimum} 至 {maximum}")
    return normalized


def validate_trial_contract(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("试验合同必须是对象")
    if value.get("contract_status") != "BOUNDED_REMOTE_TRIAL_ONLY":
        raise ValueError("试验合同状态必须固定为 BOUNDED_REMOTE_TRIAL_ONLY")
    if value.get("provider_key") != MINIMAX_H3_PROVIDER_KEY:
        raise ValueError("试验合同提供者必须是 minimax_h3")
    provider = value.get("provider")
    if not isinstance(provider, dict):
        raise ValueError("试验合同缺少提供者配置")
    if provider.get("provider_identity") != "MiniMax":
        raise ValueError("提供者身份必须固定为 MiniMax")
    if provider.get("model_id") != MINIMAX_H3_MODEL_ID:
        raise ValueError("模型标识必须固定为 MiniMax-H3")
    if provider.get("api_version") != "v2":
        raise ValueError("接口版本必须固定为 v2")
    if provider.get("execution_backend") != "remote_api":
        raise ValueError("H3 试验必须使用 remote_api 后端")

    prompt = value.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("试验合同必须包含非空提示词")
    if len(prompt) > 7000:
        raise ValueError("提示词不能超过 7000 个字符")

    generation = value.get("generation")
    if not isinstance(generation, dict):
        raise ValueError("试验合同缺少生成参数")
    resolution = generation.get("resolution")
    if resolution not in {"768P", "2K"}:
        raise ValueError("分辨率只允许 768P 或 2K")
    duration = _integer(generation.get("duration"), "duration", 4, 15)
    ratio = generation.get("ratio")
    if ratio not in {"21:9", "16:9", "4:3", "1:1", "3:4", "9:16"}:
        raise ValueError("文生视频必须使用明确的受支持画幅比")

    timeout_seconds = _integer(value.get("timeout_seconds"), "timeout_seconds", 300, 7200)
    poll_interval_seconds = _integer(
        value.get("poll_interval_seconds"), "poll_interval_seconds", 2, 60
    )
    max_download_bytes = _integer(
        value.get("max_download_bytes"), "max_download_bytes", 1024 * 1024, 2 * 1024**3
    )
    non_goals = value.get("non_goals")
    if not isinstance(non_goals, list) or not REQUIRED_NON_GOALS.issubset(set(non_goals)):
        raise ValueError("试验合同缺少强制非目标边界")
    if value.get("paid_remote_request_requires_execute_flag") is not True:
        raise ValueError("计费远端请求必须要求显式执行标志")

    normalized = json.loads(json.dumps(value))
    normalized["prompt"] = prompt.strip()
    normalized["generation"] = {
        "resolution": resolution,
        "duration": duration,
        "ratio": ratio,
    }
    normalized["timeout_seconds"] = timeout_seconds
    normalized["poll_interval_seconds"] = poll_interval_seconds
    normalized["max_download_bytes"] = max_download_bytes
    return normalized


def build_generation_payload(contract: dict[str, Any]) -> dict[str, Any]:
    normalized = validate_trial_contract(contract)
    generation = normalized["generation"]
    return {
        "model": MINIMAX_H3_MODEL_ID,
        "content": [{"type": "text", "text": normalized["prompt"]}],
        "resolution": generation["resolution"],
        "duration": generation["duration"],
        "ratio": generation["ratio"],
    }


def public_task_observation(response: dict[str, Any]) -> dict[str, Any]:
    task = response.get("task")
    if not isinstance(task, dict):
        raise AdapterError("INVALID_QUERY_RESPONSE", "查询响应缺少 task 对象")
    content = task.get("content") if isinstance(task.get("content"), dict) else {}
    return {
        "id": task.get("id"),
        "model": task.get("model"),
        "status": task.get("status"),
        "created_at": task.get("created_at"),
        "updated_at": task.get("updated_at"),
        "resolution": task.get("resolution"),
        "duration": task.get("duration"),
        "ratio": task.get("ratio"),
        "task_type": task.get("task_type"),
        "modality": task.get("modality"),
        "usage": task.get("usage"),
        "error": task.get("error"),
        "output_url_present": isinstance(content.get("url"), str) and bool(content["url"]),
    }


class UrllibMiniMaxH3Transport:
    """仅连接固定开放平台来源，且从不持久化授权头。"""

    def __init__(
        self,
        api_key: str,
        api_base: str = MINIMAX_H3_API_BASE,
        request_timeout_seconds: int = 60,
    ) -> None:
        if not api_key.strip():
            raise ValueError("MiniMax 接口密钥不能为空")
        parsed = urlparse(api_base)
        if parsed.scheme != "https" or parsed.netloc != "api.minimax.io" or parsed.path.rstrip("/"):
            raise ValueError("MiniMax 接口来源必须固定为 https://api.minimax.io")
        self.api_key = api_key
        self.api_base = api_base.rstrip("/")
        self.request_timeout_seconds = request_timeout_seconds

    def _json_request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
        request = Request(
            f"{self.api_base}{path}",
            data=body,
            method=method,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "senk-video-generator/minimax-h3-adapter-v1",
            },
        )
        try:
            with urlopen(request, timeout=self.request_timeout_seconds) as response:
                raw = response.read(1024 * 1024)
        except HTTPError as exc:
            raw = exc.read(64 * 1024)
            details: dict[str, Any] = {"http_status": exc.code}
            try:
                value = json.loads(raw)
                if isinstance(value, dict):
                    details["provider_error"] = value.get("error") or value.get("base_resp") or value
            except (UnicodeDecodeError, json.JSONDecodeError):
                details["response_body_available"] = bool(raw)
            raise AdapterError("REMOTE_HTTP_ERROR", "MiniMax 接口返回错误状态", details) from exc
        except (TimeoutError, URLError) as exc:
            raise AdapterError("REMOTE_NETWORK_ERROR", "MiniMax 接口网络请求失败", {"type": type(exc).__name__}) from exc
        try:
            value = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise AdapterError("INVALID_JSON_RESPONSE", "MiniMax 接口返回无效 JSON") from exc
        if not isinstance(value, dict):
            raise AdapterError("INVALID_JSON_RESPONSE", "MiniMax 接口响应必须是对象")
        return value

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._json_request("POST", "/v2/video_generation", payload)

    def query(self, task_id: str) -> dict[str, Any]:
        if not TASK_ID_PATTERN.fullmatch(task_id):
            raise AdapterError("INVALID_TASK_ID", "提供者任务标识格式无效")
        return self._json_request("GET", f"/v2/query/video_generation/{quote(task_id, safe='')}")

    def cancel(self, task_id: str) -> dict[str, Any]:
        if not TASK_ID_PATTERN.fullmatch(task_id):
            raise AdapterError("INVALID_TASK_ID", "提供者任务标识格式无效")
        return self._json_request("DELETE", f"/v2/video_generation/{quote(task_id, safe='')}")

    def download(self, url: str, destination: Path, max_bytes: int) -> dict[str, Any]:
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise AdapterError("INVALID_OUTPUT_URL", "输出下载地址必须是 HTTPS 地址")
        request = Request(url, method="GET", headers={"User-Agent": "senk-video-generator/minimax-h3-adapter-v1"})
        temporary = destination.with_suffix(destination.suffix + ".partial")
        total = 0
        digest = hashlib.sha256()
        try:
            with urlopen(request, timeout=self.request_timeout_seconds) as response, temporary.open("xb") as handle:
                content_type = response.headers.get_content_type()
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    total += len(block)
                    if total > max_bytes:
                        raise AdapterError("OUTPUT_TOO_LARGE", "提供者输出超过下载预算", {"max_bytes": max_bytes})
                    digest.update(block)
                    handle.write(block)
        except AdapterError:
            temporary.unlink(missing_ok=True)
            raise
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            temporary.unlink(missing_ok=True)
            raise AdapterError("OUTPUT_DOWNLOAD_FAILED", "提供者输出下载失败", {"type": type(exc).__name__}) from exc
        if total == 0:
            temporary.unlink(missing_ok=True)
            raise AdapterError("EMPTY_OUTPUT", "提供者返回了空输出")
        temporary.replace(destination)
        return {"bytes": total, "sha256": digest.hexdigest(), "content_type": content_type}


def run_trial(
    contract: dict[str, Any],
    execution_id: str,
    evidence_dir: Path,
    transport: MiniMaxH3Transport,
    *,
    sleep: Callable[[float], None] = time.sleep,
    monotonic: Callable[[], float] = time.monotonic,
    media_probe: Callable[[Path], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    normalized = validate_trial_contract(contract)
    if not EXECUTION_ID_PATTERN.fullmatch(execution_id):
        raise ValueError("执行标识格式无效")
    if evidence_dir.exists():
        raise ValueError("证据目录已经存在，拒绝覆盖")
    evidence_dir.mkdir(parents=True)
    payload = build_generation_payload(normalized)
    request_record = {
        "execution_id": execution_id,
        "created_at": utc_now(),
        "contract_id": normalized["contract_id"],
        "contract_status": normalized["contract_status"],
        "provider_key": MINIMAX_H3_PROVIDER_KEY,
        "provider_identity": "MiniMax",
        "model_id": MINIMAX_H3_MODEL_ID,
        "api_version": "v2",
        "execution_backend": "remote_api",
        "credential_env": MINIMAX_H3_API_KEY_ENV,
        "credential_recorded": False,
        "request_payload": payload,
        "candidate_observations": normalized["candidate_observations"],
        "non_goals": normalized["non_goals"],
    }
    write_json(evidence_dir / "request.json", request_record)

    started = monotonic()
    task_id: str | None = None
    output_path = evidence_dir / "output.mp4"
    output_download: dict[str, Any] | None = None
    output_metadata: dict[str, Any] | None = None
    final_observation: dict[str, Any] | None = None
    try:
        created = transport.create(payload)
        task_id = str(created.get("task_id", ""))
        if not TASK_ID_PATTERN.fullmatch(task_id):
            raise AdapterError("INVALID_CREATE_RESPONSE", "创建响应缺少有效 task_id")
        write_json(
            evidence_dir / "provider_submission.json",
            {"task_id": task_id, "model": MINIMAX_H3_MODEL_ID, "submitted_at": utc_now()},
        )

        final_response: dict[str, Any] | None = None
        poll_path = evidence_dir / "provider_poll.jsonl"
        while monotonic() - started <= normalized["timeout_seconds"]:
            response = transport.query(task_id)
            observation = public_task_observation(response)
            if observation["id"] != task_id:
                raise AdapterError("TASK_ID_MISMATCH", "查询响应的任务标识不一致")
            if observation["model"] != MINIMAX_H3_MODEL_ID:
                raise AdapterError("MODEL_ID_MISMATCH", "查询响应的模型标识不一致")
            with poll_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps({"observed_at": utc_now(), **observation}, ensure_ascii=False, sort_keys=True) + "\n")
            if observation["status"] in TERMINAL_STATUSES:
                final_response = response
                break
            if observation["status"] not in {"queued", "running"}:
                raise AdapterError("UNKNOWN_TASK_STATUS", "查询响应包含未知任务状态")
            sleep(normalized["poll_interval_seconds"])
        if final_response is None:
            raise AdapterError("REMOTE_TIMEOUT", "远端任务在合同时间内没有进入终态")

        final_observation = public_task_observation(final_response)
        write_json(evidence_dir / "provider_final_task.json", final_observation)
        if final_observation["status"] != "succeeded":
            raise AdapterError(
                "REMOTE_TASK_NOT_SUCCEEDED",
                "远端任务没有成功完成",
                {"status": final_observation["status"], "error": final_observation.get("error")},
            )
        expected_generation = normalized["generation"]
        if final_observation.get("resolution") != expected_generation["resolution"]:
            raise AdapterError("PROVIDER_RESOLUTION_MISMATCH", "提供者终态分辨率与请求不一致")
        if final_observation.get("duration") != expected_generation["duration"]:
            raise AdapterError("PROVIDER_DURATION_MISMATCH", "提供者终态时长与请求不一致")
        if final_observation.get("ratio") != expected_generation["ratio"]:
            raise AdapterError("PROVIDER_RATIO_MISMATCH", "提供者终态画幅比与请求不一致")
        task = final_response["task"]
        content = task.get("content") if isinstance(task.get("content"), dict) else {}
        output_url = content.get("url")
        if not isinstance(output_url, str) or not output_url:
            raise AdapterError("OUTPUT_URL_MISSING", "成功任务缺少输出下载地址")
        output_download = transport.download(output_url, output_path, normalized["max_download_bytes"])
        output_metadata = media_probe(output_path) if media_probe else None
        if output_metadata is not None:
            if output_metadata.get("decoded_frame_count", 0) <= 0:
                raise AdapterError("OUTPUT_VIDEO_INVALID", "下载输出没有可解码视频帧")
            if not output_metadata.get("audio_stream_present"):
                raise AdapterError("OUTPUT_AUDIO_MISSING", "H3 输出缺少预期的原生音频流")

        summary = {
            "execution_id": execution_id,
            "finished_at": utc_now(),
            "observation": "OBSERVED_OUTPUT_AVAILABLE",
            "provider_key": MINIMAX_H3_PROVIDER_KEY,
            "provider_identity": "MiniMax",
            "model_id": MINIMAX_H3_MODEL_ID,
            "api_version": "v2",
            "execution_backend": "remote_api",
            "provider_task_id": task_id,
            "provider_status": final_observation["status"],
            "provider_usage": final_observation.get("usage"),
            "elapsed_seconds": round(monotonic() - started, 3),
            "output_export_completed": True,
            "output_sha256": output_download["sha256"],
            "output_bytes": output_download["bytes"],
            "output_content_type": output_download.get("content_type"),
            "output_metadata": output_metadata,
            "visual_quality_acceptance": "REQUIRES_REVIEW",
            "semantic_review": "REQUIRES_REVIEW",
            "formal_fact_created": False,
            "formal_selection_decision_created": False,
            "timeline_binding_created": False,
            "cross_provider_contract_created": False,
            "institution_freeze_created": False,
        }
        write_json(evidence_dir / "summary.json", summary)
        write_manifest(evidence_dir)
        return summary
    except BaseException as exc:
        observation = exc.observation() if isinstance(exc, AdapterError) else {
            "code": type(exc).__name__,
            "message": str(exc),
            "details": {},
        }
        if task_id and (final_observation is None or final_observation.get("status") in {"queued", "running"}):
            cancellation: dict[str, Any]
            try:
                response = transport.cancel(task_id)
                cancellation = {
                    "attempted_at": utc_now(),
                    "task_id": task_id,
                    "result": "PROVIDER_RESPONSE_RECEIVED",
                    "action": response.get("action"),
                    "status": response.get("status"),
                }
            except BaseException as cancellation_exc:
                cancellation_observation = (
                    cancellation_exc.observation()
                    if isinstance(cancellation_exc, AdapterError)
                    else {
                        "code": type(cancellation_exc).__name__,
                        "message": str(cancellation_exc),
                        "details": {},
                    }
                )
                cancellation = {
                    "attempted_at": utc_now(),
                    "task_id": task_id,
                    "result": "CANCELLATION_NOT_CONFIRMED",
                    "error": cancellation_observation,
                }
            write_json(evidence_dir / "cancellation_attempt.json", cancellation)
        write_json(evidence_dir / "error.json", observation)
        output_exists = output_path.is_file()
        if output_exists and output_download is None:
            output_download = {
                "sha256": sha256_file(output_path),
                "bytes": output_path.stat().st_size,
                "content_type": None,
            }
        summary = {
            "execution_id": execution_id,
            "finished_at": utc_now(),
            "observation": (
                "OBSERVED_OUTPUT_WITH_TECHNICAL_GAP"
                if output_exists
                else "OBSERVED_REMOTE_EXECUTION_FAILURE"
            ),
            "provider_key": MINIMAX_H3_PROVIDER_KEY,
            "provider_identity": "MiniMax",
            "model_id": MINIMAX_H3_MODEL_ID,
            "api_version": "v2",
            "execution_backend": "remote_api",
            "provider_task_id": task_id,
            "elapsed_seconds": round(monotonic() - started, 3),
            "provider_status": final_observation.get("status") if final_observation else None,
            "provider_usage": final_observation.get("usage") if final_observation else None,
            "output_export_completed": output_exists,
            "output_sha256": output_download.get("sha256") if output_download else None,
            "output_bytes": output_download.get("bytes") if output_download else None,
            "output_content_type": output_download.get("content_type") if output_download else None,
            "output_metadata": output_metadata,
            "error": observation,
            "visual_quality_acceptance": "UNKNOWN",
            "semantic_review": "UNKNOWN",
            "formal_fact_created": False,
            "formal_selection_decision_created": False,
            "timeline_binding_created": False,
            "cross_provider_contract_created": False,
            "institution_freeze_created": False,
        }
        write_json(evidence_dir / "summary.json", summary)
        write_manifest(evidence_dir)
        raise
