#!/usr/bin/env python3
"""从既有五秒候选资产派生非权威时序稳定观察。"""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import time
from pathlib import Path
from typing import Any

import imageio.v2 as imageio
import imageio_ffmpeg
import numpy as np

from tools.run_provider_compatibility_trial import sha256_file, utc_now, write_json, write_manifest


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = REPO_ROOT / "experiments/postprocessing/cogvideox_temporal_stability_v1.json"
DEFAULT_EVIDENCE_ROOT = REPO_ROOT / "evidence/runtime"
EXECUTION_ID_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9._-]{2,127}")


def git_value(*args: str) -> str | None:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.stdout.strip() or None if result.returncode == 0 else None


def read_video(path: Path) -> tuple[np.ndarray, dict[str, Any]]:
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


def subject_observation(frames: np.ndarray, measurement: dict[str, Any]) -> dict[str, Any]:
    centroids: list[list[float] | None] = []
    areas: list[int] = []
    red_minimum = int(measurement["red_minimum"])
    green_numerator = int(measurement["red_to_green_ratio_numerator"])
    green_denominator = int(measurement["red_to_green_ratio_denominator"])
    blue_numerator = int(measurement["red_to_blue_ratio_numerator"])
    blue_denominator = int(measurement["red_to_blue_ratio_denominator"])
    for frame in frames:
        rgb = frame.astype(np.int32)
        mask = (
            (rgb[..., 0] > red_minimum)
            & (rgb[..., 0] * green_denominator > rgb[..., 1] * green_numerator)
            & (rgb[..., 0] * blue_denominator > rgb[..., 2] * blue_numerator)
        )
        ys, xs = np.nonzero(mask)
        areas.append(int(mask.sum()))
        centroids.append([float(xs.mean()), float(ys.mean())] if len(xs) else None)
    retained = [
        area >= int(measurement["minimum_subject_area_pixels"]) and centroid is not None
        for area, centroid in zip(areas, centroids, strict=True)
    ]
    valid_centroids = np.asarray([centroid for centroid in centroids if centroid is not None])
    if len(valid_centroids) != len(frames):
        adjacent_jumps = np.asarray([], dtype=float)
    else:
        adjacent_jumps = np.linalg.norm(np.diff(valid_centroids, axis=0), axis=1)
    area_array = np.asarray(areas, dtype=float)
    area_changes = (
        np.abs(np.diff(area_array)) / np.maximum(area_array[:-1], 1.0) * 100.0
        if len(area_array) > 1
        else np.asarray([], dtype=float)
    )
    adjacent_mad = (
        np.abs(np.diff(frames.astype(np.int16), axis=0)).mean(axis=(1, 2, 3))
        if len(frames) > 1
        else np.asarray([], dtype=float)
    )
    return {
        "all_frames_retain_subject": all(retained),
        "retained_subject_by_frame": retained,
        "subject_area_pixels_by_frame": areas,
        "subject_centroid_by_frame": centroids,
        "minimum_subject_area_pixels": min(areas) if areas else 0,
        "maximum_subject_area_pixels": max(areas) if areas else 0,
        "maximum_adjacent_centroid_jump_pixels": float(adjacent_jumps.max()) if len(adjacent_jumps) else None,
        "mean_adjacent_centroid_jump_pixels": float(adjacent_jumps.mean()) if len(adjacent_jumps) else None,
        "maximum_adjacent_subject_area_change_percent": float(area_changes.max()) if len(area_changes) else None,
        "mean_adjacent_subject_area_change_percent": float(area_changes.mean()) if len(area_changes) else None,
        "maximum_adjacent_frame_mad": float(adjacent_mad.max()) if len(adjacent_mad) else None,
        "mean_adjacent_frame_mad": float(adjacent_mad.mean()) if len(adjacent_mad) else None,
    }


def stabilize_frames(
    frames: np.ndarray,
    observation: dict[str, Any],
    trajectory: dict[str, Any],
    temporal_filter: dict[str, Any],
) -> tuple[np.ndarray, list[list[int]]]:
    if not observation["all_frames_retain_subject"]:
        raise ValueError("源视频并非每帧都保留可测量红色主体")
    centroids = np.asarray(observation["subject_centroid_by_frame"], dtype=float)
    target_x = np.linspace(centroids[0, 0], centroids[-1, 0], len(frames))
    target_y = np.linspace(centroids[0, 1], centroids[-1, 1], len(frames))
    shifts = np.rint(np.column_stack((target_x, target_y)) - centroids).astype(int)
    maximum_translation = int(trajectory["maximum_translation_pixels"])
    if int(np.abs(shifts).max()) > maximum_translation:
        raise ValueError("所需主体平移超过合同上限")
    height, width = frames.shape[1:3]
    aligned = []
    for frame, (dx, dy) in zip(frames, shifts, strict=True):
        padded = np.pad(
            frame,
            ((maximum_translation, maximum_translation), (maximum_translation, maximum_translation), (0, 0)),
            mode="edge",
        )
        y0 = maximum_translation - int(dy)
        x0 = maximum_translation - int(dx)
        aligned.append(padded[y0 : y0 + height, x0 : x0 + width].copy())
    aligned_array = np.stack(aligned).astype(np.float32)
    weights = np.asarray(temporal_filter["weights"], dtype=np.float32)
    if len(weights) != 3 or weights.sum() <= 0:
        raise ValueError("时域混合权重无效")
    mixed = []
    for index in range(len(aligned_array)):
        previous = aligned_array[max(0, index - 1)]
        current = aligned_array[index]
        following = aligned_array[min(len(aligned_array) - 1, index + 1)]
        frame = (previous * weights[0] + current * weights[1] + following * weights[2]) / weights.sum()
        mixed.append(np.clip(frame, 0, 255).round().astype(np.uint8))
    return np.stack(mixed), shifts.tolist()


def threshold_comparisons(observation: dict[str, Any], thresholds: dict[str, Any]) -> dict[str, Any]:
    comparisons = {
        "all_frames_retain_subject": {
            "expected": bool(thresholds["all_frames_retain_subject"]),
            "observed": bool(observation["all_frames_retain_subject"]),
        },
        "maximum_adjacent_centroid_jump_pixels": {
            "maximum": float(thresholds["maximum_adjacent_centroid_jump_pixels"]),
            "observed": observation["maximum_adjacent_centroid_jump_pixels"],
        },
        "mean_adjacent_centroid_jump_pixels": {
            "maximum": float(thresholds["mean_adjacent_centroid_jump_pixels"]),
            "observed": observation["mean_adjacent_centroid_jump_pixels"],
        },
        "maximum_adjacent_subject_area_change_percent": {
            "maximum": float(thresholds["maximum_adjacent_subject_area_change_percent"]),
            "observed": observation["maximum_adjacent_subject_area_change_percent"],
        },
    }
    comparisons["all_frames_retain_subject"]["within_threshold"] = (
        comparisons["all_frames_retain_subject"]["observed"]
        == comparisons["all_frames_retain_subject"]["expected"]
    )
    for key in (
        "maximum_adjacent_centroid_jump_pixels",
        "mean_adjacent_centroid_jump_pixels",
        "maximum_adjacent_subject_area_change_percent",
    ):
        comparisons[key]["within_threshold"] = (
            comparisons[key]["observed"] is not None
            and comparisons[key]["observed"] <= comparisons[key]["maximum"]
        )
    return comparisons


def validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("contract_id") != "CR-0020-COGVIDEOX-TEMPORAL-STABILITY-DERIVATION-001":
        raise ValueError("时序稳定合同标识无效")
    if contract.get("contract_status") != "BOUNDED_DERIVATION_ONLY":
        raise ValueError("时序稳定合同状态无效")
    expected_source = {
        "execution_id": "LM-COGVIDEOX-5S-16STEP-20260809T190026Z",
        "filename": "derived_5s.mp4",
        "sha256": "0276303f4eb31da3167e9a23d94e0a472f5d35b58834323a3ecc9d157357b8cd",
        "decoded_frame_count": 40,
        "fps": 8,
        "duration_seconds": 5.0,
    }
    if contract.get("source") != expected_source:
        raise ValueError("时序稳定来源合同无效")
    expected_measurement = {
        "red_minimum": 150,
        "red_to_green_ratio_numerator": 3,
        "red_to_green_ratio_denominator": 2,
        "red_to_blue_ratio_numerator": 3,
        "red_to_blue_ratio_denominator": 2,
        "minimum_subject_area_pixels": 10000,
    }
    if contract.get("subject_measurement") != expected_measurement:
        raise ValueError("时序稳定主体测量合同无效")
    expected_trajectory = {
        "strategy": "LINEAR_CENTROID_FIRST_TO_LAST",
        "rounding": "NEAREST_INTEGER_PIXEL",
        "maximum_translation_pixels": 128,
        "edge_fill": "EDGE_REPLICATION",
    }
    if contract.get("trajectory") != expected_trajectory:
        raise ValueError("时序稳定轨迹合同无效")
    expected_filter = {
        "strategy": "SYMMETRIC_THREE_FRAME_WEIGHTED_MIX",
        "weights": [1, 4, 1],
        "endpoint_behavior": "CLAMP",
    }
    if contract.get("temporal_filter") != expected_filter:
        raise ValueError("时序混合权重或边界合同无效")
    expected_output = {
        "filename": "stabilized_5s.mp4",
        "decoded_frame_count": 40,
        "fps": 8,
        "duration_seconds": 5.0,
        "codec": "libx264",
        "pixel_format": "yuv420p",
    }
    if contract.get("output") != expected_output:
        raise ValueError("时序稳定输出合同无效")
    expected_thresholds = {
        "maximum_adjacent_centroid_jump_pixels": 5.0,
        "mean_adjacent_centroid_jump_pixels": 2.0,
        "maximum_adjacent_subject_area_change_percent": 13.0,
        "all_frames_retain_subject": True,
    }
    if contract.get("observation_thresholds") != expected_thresholds:
        raise ValueError("时序稳定观察阈值合同无效")
    required_non_goals = {
        "source_evidence_modification",
        "model_generation",
        "visual_quality_acceptance",
        "selection_decision",
        "timeline_binding",
        "operator_console_enablement",
        "thirty_second_timeline_creation",
        "institution_freeze",
    }
    if not required_non_goals.issubset(set(contract.get("non_goals", []))):
        raise ValueError("时序稳定合同缺少非目标边界")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execution-id", required=True)
    parser.add_argument("--contract", default=str(DEFAULT_CONTRACT))
    parser.add_argument("--evidence-root", default=str(DEFAULT_EVIDENCE_ROOT))
    args = parser.parse_args()
    if not EXECUTION_ID_PATTERN.fullmatch(args.execution_id):
        parser.error("execution-id 只能包含大写字母、数字、点、下划线和连字符")
    contract_path = Path(args.contract).resolve()
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    validate_contract(contract)
    evidence_root = Path(args.evidence_root).resolve()
    evidence_dir = evidence_root / args.execution_id
    if evidence_dir.exists():
        raise SystemExit(f"证据目录已经存在，拒绝覆盖：{evidence_dir}")
    evidence_dir.mkdir(parents=True)
    started_at = utc_now()
    started = time.perf_counter()
    source = contract["source"]
    request = {
        "execution_id": args.execution_id,
        "created_at": started_at,
        "contract": contract,
        "formal_fact_creation": "PROHIBITED",
        "selection_decision_creation": "PROHIBITED",
        "timeline_binding_creation": "PROHIBITED",
    }
    write_json(evidence_dir / "request.json", request)
    write_json(
        evidence_dir / "environment.json",
        {
            "execution_id": args.execution_id,
            "recorded_at": utc_now(),
            "operating_system": platform.system(),
            "operating_system_version": platform.mac_ver()[0],
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "imageio_version": imageio.__version__ if hasattr(imageio, "__version__") else None,
            "bundled_ffmpeg_version": imageio_ffmpeg.get_ffmpeg_version(),
            "git_head": git_value("rev-parse", "HEAD"),
            "git_status_porcelain": git_value("status", "--porcelain") or "",
            "harness_sha256": sha256_file(Path(__file__)),
            "contract_sha256": sha256_file(contract_path),
            "sensitive_machine_identifiers_recorded": False,
        },
    )
    summary: dict[str, Any] = {
        "execution_id": args.execution_id,
        "started_at": started_at,
        "contract_id": contract["contract_id"],
        "contract_status": contract["contract_status"],
        "source_execution_id": source["execution_id"],
        "source_filename": source["filename"],
        "source_sha256": source["sha256"],
        "observation": "OBSERVED_EXECUTION_WITHOUT_OUTPUT",
        "output_export_completed": False,
        "formal_fact_created": False,
        "selection_decision_created": False,
        "timeline_binding_created": False,
    }
    try:
        source_path = evidence_root / source["execution_id"] / source["filename"]
        if not source_path.is_file() or sha256_file(source_path) != source["sha256"]:
            raise ValueError("来源视频不存在或摘要不匹配")
        frames, source_metadata = read_video(source_path)
        if source_metadata["decoded_frame_count"] != source["decoded_frame_count"]:
            raise ValueError("来源视频帧数不符合合同")
        if source_metadata["fps"] != float(source["fps"]):
            raise ValueError("来源视频帧率不符合合同")
        if abs(source_metadata["duration_seconds"] - float(source["duration_seconds"])) > 0.001:
            raise ValueError("来源视频时长不符合合同")
        source_observation = subject_observation(frames, contract["subject_measurement"])
        stabilized, shifts = stabilize_frames(
            frames,
            source_observation,
            contract["trajectory"],
            contract["temporal_filter"],
        )
        output_path = evidence_dir / contract["output"]["filename"]
        writer = imageio.get_writer(
            output_path,
            fps=contract["output"]["fps"],
            codec=contract["output"]["codec"],
            pixelformat=contract["output"]["pixel_format"],
        )
        try:
            for frame in stabilized:
                writer.append_data(frame)
        finally:
            writer.close()
        output_frames, output_metadata = read_video(output_path)
        output_contract = contract["output"]
        if output_metadata["decoded_frame_count"] != output_contract["decoded_frame_count"]:
            raise ValueError("稳定派生视频帧数不符合合同")
        if output_metadata["fps"] != float(output_contract["fps"]):
            raise ValueError("稳定派生视频帧率不符合合同")
        if abs(output_metadata["duration_seconds"] - float(output_contract["duration_seconds"])) > 0.001:
            raise ValueError("稳定派生视频时长不符合合同")
        output_observation = subject_observation(output_frames, contract["subject_measurement"])
        comparisons = threshold_comparisons(output_observation, contract["observation_thresholds"])
        write_json(
            evidence_dir / "frame_metrics.json",
            {
                "source_metadata": source_metadata,
                "source_observation": source_observation,
                "translation_by_frame": shifts,
                "output_metadata": output_metadata,
                "output_observation": output_observation,
                "threshold_comparisons": comparisons,
            },
        )
        imageio.imwrite(evidence_dir / "thumbnail.png", output_frames[0])
        summary.update(
            {
                "observation": "OBSERVED_OUTPUT_AVAILABLE",
                "output_export_completed": True,
                "output_sha256": sha256_file(output_path),
                "output_bytes": output_path.stat().st_size,
                "thumbnail_sha256": sha256_file(evidence_dir / "thumbnail.png"),
                "source_metadata": source_metadata,
                "source_observation": source_observation,
                "output_metadata": output_metadata,
                "output_observation": output_observation,
                "threshold_comparisons": comparisons,
                "all_observation_thresholds_met": all(
                    item["within_threshold"] for item in comparisons.values()
                ),
            }
        )
    except BaseException as exc:
        summary["error_observation"] = {
            "type": type(exc).__name__,
            "message": str(exc),
        }
    summary["elapsed_seconds"] = round(time.perf_counter() - started, 3)
    summary["finished_at"] = utc_now()
    write_json(evidence_dir / "summary.json", summary)
    manifest = write_manifest(evidence_dir)
    print(json.dumps({**summary, "manifest_file_count": manifest["file_count"]}, ensure_ascii=False, indent=2))
    return 0 if summary["output_export_completed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
