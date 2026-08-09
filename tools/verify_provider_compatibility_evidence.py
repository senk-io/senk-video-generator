#!/usr/bin/env python3
"""独立校验提供者兼容性观察证据包。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


PRIVATE_TEXT_PATTERNS = (
    re.compile(r"/Users/[^/\s]+"),
    re.compile(r"/home/[^/\s]+"),
    re.compile(r"Serial Number", re.IGNORECASE),
    re.compile(r"Hardware UUID", re.IGNORECASE),
    re.compile(r"Provisioning UDID", re.IGNORECASE),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_dir")
    args = parser.parse_args()
    evidence_dir = Path(args.evidence_dir).resolve()
    manifest = read_json(evidence_dir / "manifest.json")
    summary = read_json(evidence_dir / "summary.json")
    request = read_json(evidence_dir / "request.json")
    environment = read_json(evidence_dir / "environment.json")

    expected_paths = {entry["path"] for entry in manifest["files"]}
    actual_paths = {
        str(path.relative_to(evidence_dir))
        for path in evidence_dir.rglob("*")
        if path.is_file() and path.name != "manifest.json"
    }
    if expected_paths != actual_paths:
        raise SystemExit("证据文件闭包与清单不一致")

    for entry in manifest["files"]:
        path = evidence_dir / entry["path"]
        if path.stat().st_size != entry["bytes"]:
            raise SystemExit(f"文件大小不一致：{entry['path']}")
        if sha256_file(path) != entry["sha256"]:
            raise SystemExit(f"文件摘要不一致：{entry['path']}")

    execution_ids = {
        summary.get("execution_id"),
        request.get("execution_id"),
        environment.get("execution_id"),
        evidence_dir.name,
    }
    if len(execution_ids) != 1:
        raise SystemExit("执行标识不一致")

    if summary["formal_fact_created"]:
        raise SystemExit("兼容性试运行不得创建正式事实")
    if summary["cross_provider_contract_created"]:
        raise SystemExit("兼容性试运行不得创建跨提供方合同")
    if summary["institution_freeze_created"]:
        raise SystemExit("兼容性试运行不得创建制度冻结")

    output_path = evidence_dir / "output.mp4"
    if summary["output_export_completed"]:
        if not output_path.exists():
            raise SystemExit("摘要声称视频已导出，但文件不存在")
        if summary["output_sha256"] != sha256_file(output_path):
            raise SystemExit("视频输出摘要不一致")
    elif output_path.exists():
        raise SystemExit("摘要未声明导出完成，但视频文件存在")

    text_suffixes = {".json", ".jsonl", ".log", ".md", ".txt"}
    public_text_file_count = 0
    for path in evidence_dir.rglob("*"):
        if not path.is_file() or path.suffix not in text_suffixes:
            continue
        public_text_file_count += 1
        content = path.read_text(encoding="utf-8", errors="replace")
        for pattern in PRIVATE_TEXT_PATTERNS:
            if pattern.search(content):
                raise SystemExit(f"公开证据包含禁止的机器身份或用户路径：{path.name}")

    result = {
        "execution_id": evidence_dir.name,
        "observation": summary["observation"],
        "manifest_file_count": manifest["file_count"],
        "public_text_file_count": public_text_file_count,
        "output_digest_verified": bool(summary["output_export_completed"]),
        "exact_file_closure": True,
        "sensitive_path_scan": "CLEAR",
        "formal_fact_created": False,
        "cross_provider_contract_created": False,
        "institution_freeze_created": False,
        "verification_result": "VERIFIED_OBSERVATION_PACKAGE",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
