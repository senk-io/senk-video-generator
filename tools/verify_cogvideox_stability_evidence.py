#!/usr/bin/env python3
"""独立校验 CogVideoX 五秒候选的时序稳定派生证据。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import imageio.v2 as imageio
import numpy as np


PRIVATE_TEXT_PATTERNS = (
    re.compile(r"/Users/[^/\s]+"),
    re.compile(r"/home/[^/\s]+"),
    re.compile(r"Serial Number", re.IGNORECASE),
    re.compile(r"Hardware UUID", re.IGNORECASE),
)
REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATHS = {
    "CR-0020-COGVIDEOX-TEMPORAL-STABILITY-DERIVATION-001": (
        REPO_ROOT / "experiments/postprocessing/cogvideox_temporal_stability_v1.json"
    ),
    "CR-0020-COGVIDEOX-ORIGAMI-TEMPORAL-STABILITY-DERIVATION-001": (
        REPO_ROOT / "experiments/postprocessing/cogvideox_origami_temporal_stability_v1.json"
    ),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def decode_video(path: Path) -> tuple[np.ndarray, dict[str, Any]]:
    reader = imageio.get_reader(path)
    try:
        metadata = reader.get_meta_data()
        frames = np.stack([np.asarray(frame)[..., :3] for frame in reader])
    finally:
        reader.close()
    return frames, {
        "decoded_frame_count": int(len(frames)),
        "fps": float(metadata.get("fps") or 0.0),
        "duration_seconds": float(metadata.get("duration") or 0.0),
        "size": list(metadata.get("size", ())),
    }


def independently_measure(frames: np.ndarray, measurement: dict[str, Any]) -> dict[str, Any]:
    centroids = []
    areas = []
    for frame in frames:
        rgb = frame.astype(np.int64)
        mask = (
            (rgb[..., 0] > int(measurement["red_minimum"]))
            & (
                rgb[..., 0] * int(measurement["red_to_green_ratio_denominator"])
                > rgb[..., 1] * int(measurement["red_to_green_ratio_numerator"])
            )
            & (
                rgb[..., 0] * int(measurement["red_to_blue_ratio_denominator"])
                > rgb[..., 2] * int(measurement["red_to_blue_ratio_numerator"])
            )
        )
        y_coordinates, x_coordinates = np.where(mask)
        areas.append(int(len(x_coordinates)))
        centroids.append(
            [float(np.average(x_coordinates)), float(np.average(y_coordinates))]
            if len(x_coordinates)
            else None
        )
    all_retained = all(
        centroid is not None and area >= int(measurement["minimum_subject_area_pixels"])
        for centroid, area in zip(centroids, areas, strict=True)
    )
    centroid_array = np.asarray(centroids, dtype=float) if all_retained else np.empty((0, 2))
    jumps = np.sqrt(np.square(np.diff(centroid_array, axis=0)).sum(axis=1)) if all_retained else np.asarray([])
    area_array = np.asarray(areas, dtype=float)
    area_changes = np.abs(np.diff(area_array)) / np.maximum(area_array[:-1], 1.0) * 100.0
    return {
        "all_frames_retain_subject": all_retained,
        "minimum_subject_area_pixels": min(areas) if areas else 0,
        "maximum_subject_area_pixels": max(areas) if areas else 0,
        "maximum_adjacent_centroid_jump_pixels": float(jumps.max()) if len(jumps) else None,
        "mean_adjacent_centroid_jump_pixels": float(jumps.mean()) if len(jumps) else None,
        "maximum_adjacent_subject_area_change_percent": float(area_changes.max()) if len(area_changes) else None,
        "mean_adjacent_subject_area_change_percent": float(area_changes.mean()) if len(area_changes) else None,
    }


def assert_close(name: str, expected: float | None, observed: float | None, tolerance: float = 1e-6) -> None:
    if expected is None or observed is None or abs(float(expected) - float(observed)) > tolerance:
        raise SystemExit(f"独立重算指标与摘要不一致：{name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_dir")
    parser.add_argument("--evidence-root")
    args = parser.parse_args()
    evidence_dir = Path(args.evidence_dir).resolve()
    evidence_root = Path(args.evidence_root).resolve() if args.evidence_root else evidence_dir.parent
    manifest = read_json(evidence_dir / "manifest.json")
    request = read_json(evidence_dir / "request.json")
    summary = read_json(evidence_dir / "summary.json")
    contract = request["contract"]
    contract_path = CONTRACT_PATHS.get(contract.get("contract_id"))
    if contract_path is None or contract != read_json(contract_path):
        raise SystemExit("证据请求与固定时序稳定合同不一致")
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
        if path.stat().st_size != entry["bytes"] or sha256_file(path) != entry["sha256"]:
            raise SystemExit(f"证据文件大小或摘要不一致：{entry['path']}")
    execution_ids = {evidence_dir.name, request.get("execution_id"), summary.get("execution_id")}
    if len(execution_ids) != 1:
        raise SystemExit("执行标识不一致")
    if contract.get("contract_status") != "BOUNDED_DERIVATION_ONLY":
        raise SystemExit("时序稳定证据合同状态无效")
    if summary.get("formal_fact_created") or summary.get("selection_decision_created") or summary.get("timeline_binding_created"):
        raise SystemExit("时序稳定派生不得创建正式事实、选择或时间线绑定")
    source = contract["source"]
    source_path = evidence_root / source["execution_id"] / source["filename"]
    if not source_path.is_file() or sha256_file(source_path) != source["sha256"]:
        raise SystemExit("来源资产不存在或摘要不匹配")
    output_path = evidence_dir / contract["output"]["filename"]
    if not summary.get("output_export_completed") or not output_path.is_file():
        raise SystemExit("稳定派生输出未完成")
    if summary.get("output_sha256") != sha256_file(output_path):
        raise SystemExit("稳定派生输出摘要不一致")
    frames, metadata = decode_video(output_path)
    output_contract = contract["output"]
    if metadata["decoded_frame_count"] != output_contract["decoded_frame_count"]:
        raise SystemExit("稳定派生输出帧数不符合合同")
    if metadata["fps"] != float(output_contract["fps"]):
        raise SystemExit("稳定派生输出帧率不符合合同")
    if abs(metadata["duration_seconds"] - float(output_contract["duration_seconds"])) > 0.001:
        raise SystemExit("稳定派生输出时长不符合合同")
    observation = independently_measure(frames, contract["subject_measurement"])
    recorded = summary["output_observation"]
    if observation["all_frames_retain_subject"] != recorded["all_frames_retain_subject"]:
        raise SystemExit("独立重算的主体保留观察与摘要不一致")
    for field in (
        "maximum_adjacent_centroid_jump_pixels",
        "mean_adjacent_centroid_jump_pixels",
        "maximum_adjacent_subject_area_change_percent",
        "mean_adjacent_subject_area_change_percent",
    ):
        assert_close(field, recorded[field], observation[field])
    thresholds = contract["observation_thresholds"]
    independently_within_threshold = (
        observation["all_frames_retain_subject"] == bool(thresholds["all_frames_retain_subject"])
        and observation["maximum_adjacent_centroid_jump_pixels"]
        <= float(thresholds["maximum_adjacent_centroid_jump_pixels"])
        and observation["mean_adjacent_centroid_jump_pixels"]
        <= float(thresholds["mean_adjacent_centroid_jump_pixels"])
        and observation["maximum_adjacent_subject_area_change_percent"]
        <= float(thresholds["maximum_adjacent_subject_area_change_percent"])
    )
    if independently_within_threshold != bool(summary.get("all_observation_thresholds_met")):
        raise SystemExit("独立重算的阈值观察与摘要不一致")
    public_text_file_count = 0
    for path in evidence_dir.rglob("*"):
        if not path.is_file() or path.suffix not in {".json", ".jsonl", ".log", ".md", ".txt"}:
            continue
        public_text_file_count += 1
        content = path.read_text(encoding="utf-8", errors="replace")
        if any(pattern.search(content) for pattern in PRIVATE_TEXT_PATTERNS):
            raise SystemExit(f"公开证据包含禁止的机器身份或用户路径：{path.name}")
    print(
        json.dumps(
            {
                "execution_id": evidence_dir.name,
                "observation": summary["observation"],
                "manifest_file_count": manifest["file_count"],
                "public_text_file_count": public_text_file_count,
                "source_digest_verified": True,
                "output_digest_verified": True,
                "output_metadata_verified": True,
                "independent_metrics_verified": True,
                "all_observation_thresholds_met": independently_within_threshold,
                "formal_fact_created": False,
                "selection_decision_created": False,
                "timeline_binding_created": False,
                "verification_result": "VERIFIED_COGVIDEOX_STABILITY_OBSERVATION_PACKAGE",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
