#!/usr/bin/env python3
"""独立校验 MiniMax H3 远端试验证据包。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


PRIVATE_TEXT_PATTERNS = (
    re.compile(r"/Users/[^/\s]+"),
    re.compile(r"/home/[^/\s]+"),
    re.compile(r"Authorization\s*:", re.IGNORECASE),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]+", re.IGNORECASE),
    re.compile(r"MINIMAX_API_KEY\s*=\s*\S+"),
)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} 必须是对象")
    return value


def sha256_file(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify(evidence_dir: Path) -> dict[str, Any]:
    manifest = read_json(evidence_dir / "manifest.json")
    request = read_json(evidence_dir / "request.json")
    summary = read_json(evidence_dir / "summary.json")
    environment = read_json(evidence_dir / "environment.json")
    expected_paths = {entry["path"] for entry in manifest["files"]}
    actual_paths = {
        str(path.relative_to(evidence_dir))
        for path in evidence_dir.rglob("*")
        if path.is_file() and path.name != "manifest.json"
    }
    if expected_paths != actual_paths:
        raise ValueError("证据文件闭包与清单不一致")
    for entry in manifest["files"]:
        path = evidence_dir / entry["path"]
        if path.stat().st_size != entry["bytes"] or sha256_file(path) != entry["sha256"]:
            raise ValueError(f"证据文件摘要或大小不一致：{entry['path']}")

    identities = {
        evidence_dir.name,
        request.get("execution_id"),
        summary.get("execution_id"),
        environment.get("execution_id"),
    }
    if len(identities) != 1:
        raise ValueError("执行标识不一致")
    if request.get("model_id") != "MiniMax-H3" or summary.get("model_id") != "MiniMax-H3":
        raise ValueError("模型标识不是 MiniMax-H3")
    if request.get("execution_backend") != "remote_api" or summary.get("execution_backend") != "remote_api":
        raise ValueError("执行后端不是 remote_api")
    payload = request.get("request_payload") or {}
    if payload.get("model") != "MiniMax-H3":
        raise ValueError("请求载荷模型标识不一致")
    if payload.get("resolution") != "768P" or payload.get("duration") != 5 or payload.get("ratio") != "16:9":
        raise ValueError("请求载荷偏离固定生成合同")
    for field in (
        "formal_fact_created",
        "formal_selection_decision_created",
        "timeline_binding_created",
        "cross_provider_contract_created",
        "institution_freeze_created",
    ):
        if summary.get(field) is not False:
            raise ValueError(f"远端试验不得创建状态：{field}")
    output_path = evidence_dir / "output.mp4"
    if summary.get("output_export_completed"):
        if not output_path.is_file() or summary.get("output_sha256") != sha256_file(output_path):
            raise ValueError("输出文件或摘要不一致")
        final_task = read_json(evidence_dir / "provider_final_task.json")
        if final_task.get("status") != "succeeded":
            raise ValueError("输出存在但提供者任务未成功")
        if final_task.get("id") != summary.get("provider_task_id"):
            raise ValueError("提供者任务标识不一致")
        if summary.get("observation") == "OBSERVED_OUTPUT_AVAILABLE":
            metadata = summary.get("output_metadata") or {}
            if metadata.get("decoded_frame_count", 0) <= 0:
                raise ValueError("输出缺少可解码视频帧")
            if metadata.get("audio_stream_present") is not True:
                raise ValueError("输出缺少原生音频流")
            if metadata.get("audio_sample_rate_hz") != 32000 or metadata.get("audio_channels") != "stereo":
                raise ValueError("输出音频不符合 32 kHz 双声道合同")
        elif summary.get("observation") != "OBSERVED_OUTPUT_WITH_TECHNICAL_GAP":
            raise ValueError("存在输出但观察状态不受支持")
    elif output_path.exists():
        raise ValueError("摘要未声明输出完成但视频文件存在")

    for path in evidence_dir.rglob("*"):
        if not path.is_file() or path.suffix not in {".json", ".jsonl", ".log", ".md", ".txt"}:
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        for pattern in PRIVATE_TEXT_PATTERNS:
            if pattern.search(content):
                raise ValueError(f"公开证据包含敏感路径或凭据：{path.name}")
    return {
        "execution_id": evidence_dir.name,
        "observation": summary.get("observation"),
        "output_digest_verified": bool(summary.get("output_export_completed")),
        "exact_file_closure": True,
        "sensitive_path_and_credential_scan": "CLEAR",
        "visual_quality_acceptance": summary.get("visual_quality_acceptance"),
        "verification_result": "VERIFIED_MINIMAX_H3_OBSERVATION_PACKAGE",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_dir")
    args = parser.parse_args()
    try:
        result = verify(Path(args.evidence_dir).resolve())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
