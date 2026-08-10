#!/usr/bin/env python3
"""校验关键帧自动展开证据的参数、来源、输出和治理边界。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.render_keyframe_adjustments import expand_keyframes, validate_contract
from tools.run_provider_compatibility_trial import sha256_file
from tools.stabilize_cogvideox_candidate import read_video


REQUIRED_FILES = {
    "request.json",
    "environment.json",
    "summary.json",
    "manifest.json",
    "adjustment_summary.json",
    "expanded_frame_adjustments.json",
    "frame_mapping.json",
    "review_record.json",
    "before_after_keyframe_contact_sheet_40_frames.png",
    "keyframe_adjusted_5s.mp4",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_manifest(evidence_dir: Path, manifest: dict[str, Any]) -> None:
    expected_entries = {
        item["path"]: (item["bytes"], item["sha256"])
        for item in manifest.get("files", [])
    }
    actual_paths = {
        str(path.relative_to(evidence_dir))
        for path in evidence_dir.rglob("*")
        if path.is_file() and path.name != "manifest.json"
    }
    if set(expected_entries) != actual_paths:
        raise ValueError("证据清单文件集合与实际目录不一致")
    if manifest.get("file_count") != len(actual_paths):
        raise ValueError("证据清单文件数量不一致")
    for relative_path, (expected_bytes, expected_sha256) in expected_entries.items():
        path = evidence_dir / relative_path
        if path.stat().st_size != expected_bytes:
            raise ValueError(f"证据文件大小不一致：{relative_path}")
        if sha256_file(path) != expected_sha256:
            raise ValueError(f"证据文件摘要不一致：{relative_path}")


def verify_evidence(evidence_dir: Path) -> dict[str, Any]:
    if not evidence_dir.is_dir():
        raise ValueError("证据目录不存在")
    actual_files = {
        str(path.relative_to(evidence_dir))
        for path in evidence_dir.rglob("*")
        if path.is_file()
    }
    if not REQUIRED_FILES.issubset(actual_files):
        raise ValueError(f"证据包缺少必需文件：{sorted(REQUIRED_FILES - actual_files)}")

    manifest = read_json(evidence_dir / "manifest.json")
    verify_manifest(evidence_dir, manifest)
    request = read_json(evidence_dir / "request.json")
    contract = request.get("contract")
    if not isinstance(contract, dict):
        raise ValueError("请求记录缺少关键帧合同快照")
    validate_contract(contract)
    recorded_expanded = read_json(evidence_dir / "expanded_frame_adjustments.json")
    recomputed_expanded = expand_keyframes(contract)
    if recorded_expanded != recomputed_expanded:
        raise ValueError("展开后的逐帧参数无法由关键帧合同重建")
    expanded_sha256 = sha256_file(evidence_dir / "expanded_frame_adjustments.json")
    if expanded_sha256 != request.get("expanded_frame_adjustments_sha256"):
        raise ValueError("展开后的逐帧参数摘要与请求不一致")

    summary = read_json(evidence_dir / "summary.json")
    adjustment_summary = read_json(evidence_dir / "adjustment_summary.json")
    review_record = read_json(evidence_dir / "review_record.json")
    mapping = read_json(evidence_dir / "frame_mapping.json")
    if request.get("execution_id") != evidence_dir.name:
        raise ValueError("请求执行标识与证据目录不一致")
    if summary.get("execution_id") != evidence_dir.name:
        raise ValueError("摘要执行标识与证据目录不一致")
    if summary.get("contract_sha256") != request.get("contract_sha256"):
        raise ValueError("请求与摘要的合同摘要不一致")
    if summary.get("expanded_frame_adjustments_sha256") != expanded_sha256:
        raise ValueError("执行摘要与逐帧参数摘要不一致")
    if summary.get("source_sha256") != contract["source"]["sha256"]:
        raise ValueError("摘要与合同的来源摘要不一致")
    if not summary.get("output_export_completed"):
        raise ValueError("证据包未观察到输出导出完成")
    if summary.get("model_run_count") != 0:
        raise ValueError("关键帧派生不得包含模型运行")

    prohibited_facts = (
        "formal_ground_truth_created",
        "formal_visual_quality_acceptance_created",
        "selection_decision_created",
        "timeline_binding_created",
    )
    for field in prohibited_facts:
        if summary.get(field) is not False or review_record.get(field) is not False:
            raise ValueError(f"关键帧派生非法创建正式事实：{field}")

    source = contract["source"]
    source_path = evidence_dir.parent / source["execution_id"] / source["filename"]
    if not source_path.is_file() or sha256_file(source_path) != source["sha256"]:
        raise ValueError("外部来源视频不存在或摘要不匹配")
    output_path = evidence_dir / contract["output"]["filename"]
    if sha256_file(output_path) != summary.get("output_sha256"):
        raise ValueError("输出视频摘要与执行摘要不一致")
    _, output_metadata = read_video(output_path)
    if output_metadata != summary.get("output_metadata"):
        raise ValueError("输出视频元数据与执行摘要不一致")

    if len(mapping) != 40 or [item.get("frame_number") for item in mapping] != list(
        range(1, 41)
    ):
        raise ValueError("关键帧派生逐帧映射不完整")
    if len(list((evidence_dir / "adjusted_frames").glob("frame_*.png"))) != 40:
        raise ValueError("关键帧派生调整帧数量不完整")
    for mapping_item, expanded_item in zip(mapping, recorded_expanded, strict=True):
        if mapping_item.get("parameter_source") != expanded_item.get("parameter_source"):
            raise ValueError("逐帧映射的参数来源与展开记录不一致")
        if mapping_item.get("interpolation_keyframes") != expanded_item.get(
            "interpolation_keyframes"
        ):
            raise ValueError("逐帧映射的关键帧区间与展开记录不一致")

    interpolation = adjustment_summary.get("interpolation_observation", {})
    if interpolation != summary.get("interpolation_observation"):
        raise ValueError("插值观察与执行摘要不一致")
    if interpolation.get("expanded_frame_count") != 40:
        raise ValueError("插值未展开为完整 40 帧")
    if interpolation.get("cross_frame_pixel_mixing") is not False:
        raise ValueError("关键帧派生不得执行跨帧像素混合")
    if interpolation.get("segment_overshoot_observed") is not False:
        raise ValueError("关键帧插值观察到区间越界")
    parameter_observation = adjustment_summary.get("parameter_observation", {})
    if parameter_observation != summary.get("parameter_observation"):
        raise ValueError("参数观察与执行摘要不一致")
    if review_record.get("expanded_frame_review_status_counts") != parameter_observation.get(
        "review_status_counts"
    ):
        raise ValueError("审阅记录与展开帧状态不一致")

    return {
        "observation": "KEYFRAME_EVIDENCE_PACKAGE_INTERNALLY_CONSISTENT",
        "execution_id": evidence_dir.name,
        "manifest_file_count": manifest["file_count"],
        "source_binding_verified": True,
        "output_binding_verified": True,
        "keyframe_count": interpolation.get("keyframe_count"),
        "interpolated_frame_count": interpolation.get("parameter_source_counts", {}).get(
            "INTERPOLATED_MONOTONE_CUBIC", 0
        ),
        "manual_override_count": interpolation.get("manual_override_count"),
        "frame_mapping_count": len(mapping),
        "model_run_count": 0,
        "ground_truth_status": summary.get("ground_truth_status"),
        "formal_fact_created": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_dir")
    args = parser.parse_args()
    try:
        observation = verify_evidence(Path(args.evidence_dir).resolve())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(
            json.dumps(
                {"observation": "KEYFRAME_EVIDENCE_PACKAGE_INVALID", "error": str(exc)},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1
    print(json.dumps(observation, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
