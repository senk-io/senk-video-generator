#!/usr/bin/env python3
"""独立校验 CogVideoX 潜变量重解码证据包。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from tools.run_provider_compatibility_trial import sha256_file
except ModuleNotFoundError:
    from run_provider_compatibility_trial import sha256_file


PRIVATE_TEXT_PATTERNS = (
    re.compile(r"/Users/[^/\s]+"),
    re.compile(r"/home/[^/\s]+"),
    re.compile(r"Serial Number", re.IGNORECASE),
    re.compile(r"Hardware UUID", re.IGNORECASE),
    re.compile(r"Provisioning UDID", re.IGNORECASE),
)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON 根值不是对象：{path.name}")
    return value


def read_metrics(path: Path) -> list[dict[str, Any]]:
    metrics = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"资源采样第 {line_number} 行不是对象")
        metrics.append(value)
    if not metrics:
        raise ValueError("资源采样为空")
    return metrics


def verify(evidence_dir: Path) -> dict[str, Any]:
    evidence_dir = evidence_dir.resolve()
    request = read_json(evidence_dir / "request.json")
    summary = read_json(evidence_dir / "summary.json")
    manifest = read_json(evidence_dir / "manifest.json")
    metrics = read_metrics(evidence_dir / "process_metrics.jsonl")

    if request.get("schema_version") != "cogvideox-latent-decode.v2":
        raise ValueError("潜变量重解码合同版本不受支持")
    if {request.get("execution_id"), summary.get("execution_id"), evidence_dir.name} != {evidence_dir.name}:
        raise ValueError("执行标识不一致")
    if request.get("source_execution_id") != summary.get("source_execution_id"):
        raise ValueError("来源执行标识不一致")

    expected_paths = {entry["path"] for entry in manifest.get("files", [])}
    actual_paths = {
        str(path.relative_to(evidence_dir))
        for path in evidence_dir.rglob("*")
        if path.is_file() and path.name != "manifest.json"
    }
    required_paths = {"request.json", "summary.json", "process_metrics.jsonl", "output.mp4", "thumbnail.png"}
    if expected_paths != actual_paths or not required_paths.issubset(actual_paths):
        raise ValueError("证据文件闭包与清单不一致")
    if manifest.get("file_count") != len(expected_paths):
        raise ValueError("清单文件数量不一致")
    for entry in manifest["files"]:
        path = evidence_dir / entry["path"]
        if path.stat().st_size != entry["bytes"] or sha256_file(path) != entry["sha256"]:
            raise ValueError(f"证据文件摘要不一致：{entry['path']}")

    source_root = (evidence_dir.parent / request["source_execution_id"]).resolve()
    if not source_root.is_relative_to(evidence_dir.parent):
        raise ValueError("来源证据目录越界")
    source_summary = read_json(source_root / "summary.json")
    checkpoint = source_summary.get("latent_checkpoint") or {}
    latent_path = source_root / "denoised_latents.safetensors"
    if (
        checkpoint.get("path") != "denoised_latents.safetensors"
        or checkpoint.get("sha256") != request.get("source_latent_sha256")
        or not latent_path.is_file()
        or sha256_file(latent_path) != request.get("source_latent_sha256")
    ):
        raise ValueError("来源潜变量摘要不一致")

    output_path = evidence_dir / "output.mp4"
    if summary.get("observation") != "OBSERVED_OUTPUT_AVAILABLE":
        raise ValueError("重解码没有形成可用输出观察")
    if summary.get("error_observation") is not None or summary.get("safety_abort_reason") is not None:
        raise ValueError("成功摘要仍包含错误或资源停止原因")
    if summary.get("output_sha256") != sha256_file(output_path):
        raise ValueError("视频输出摘要不一致")
    metadata = summary.get("output_metadata") or {}
    if metadata.get("decoded_frame_count", 0) <= 0 or metadata.get("duration_seconds", 0) <= 0:
        raise ValueError("视频输出元数据无效")

    resource_budget = request.get("resource_budget") or {}
    start_swap = summary.get("system_start_swap_used_bytes")
    peak_swap = max([start_swap, *(sample["swap_used_bytes"] for sample in metrics)])
    peak_rss = max(sample["process_rss_bytes"] for sample in metrics)
    if summary.get("system_peak_swap_used_bytes") != peak_swap:
        raise ValueError("换页峰值与资源采样不一致")
    if summary.get("process_peak_rss_bytes") != peak_rss:
        raise ValueError("进程内存峰值与资源采样不一致")
    if peak_swap - start_swap > resource_budget.get("max_swap_growth_bytes", 0):
        raise ValueError("换页增长超过资源合同")

    max_preflight_swap = resource_budget.get("preflight_max_swap_used_bytes")
    override_applied = resource_budget.get("historical_swap_residue_override_applied")
    if override_applied != (start_swap > max_preflight_swap):
        raise ValueError("历史换页残留判定与启动观察不一致")
    if override_applied and resource_budget.get("observed_memory_pressure_level") != resource_budget.get(
        "preflight_swap_residue_override_requires_memory_pressure_level"
    ):
        raise ValueError("历史换页残留放行时的内存压力不符合合同")

    if summary.get("formal_fact_created") or summary.get("quality_acceptance_created") or summary.get(
        "institution_freeze_created"
    ):
        raise ValueError("兼容性重解码不得创建正式结论")

    public_text_file_count = 0
    for path in evidence_dir.rglob("*"):
        if not path.is_file() or path.suffix not in {".json", ".jsonl", ".log", ".md", ".txt"}:
            continue
        public_text_file_count += 1
        content = path.read_text(encoding="utf-8", errors="replace")
        for pattern in PRIVATE_TEXT_PATTERNS:
            if pattern.search(content):
                raise ValueError(f"公开证据包含禁止的机器身份或用户路径：{path.name}")

    return {
        "execution_id": evidence_dir.name,
        "source_execution_id": request["source_execution_id"],
        "manifest_file_count": manifest["file_count"],
        "public_text_file_count": public_text_file_count,
        "output_digest_verified": True,
        "source_latent_digest_verified": True,
        "resource_metrics_verified": True,
        "exact_file_closure": True,
        "sensitive_path_scan": "CLEAR",
        "quality_acceptance_created": False,
        "verification_result": "VERIFIED_COGVIDEOX_DECODE_OBSERVATION_PACKAGE",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_dir")
    args = parser.parse_args()
    try:
        result = verify(Path(args.evidence_dir))
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
