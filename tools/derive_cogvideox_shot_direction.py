#!/usr/bin/env python3
"""从既有九帧候选派生非权威镜头方向观察。"""

from __future__ import annotations

import argparse
import hashlib
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
from tools.stabilize_cogvideox_candidate import read_video, subject_observation


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = (
    REPO_ROOT / "experiments/postprocessing/cogvideox_shot_002_rightward_direction_v1.json"
)
DEFAULT_EVIDENCE_ROOT = REPO_ROOT / "evidence/runtime"
EXECUTION_ID_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9._-]{2,127}")
FIXED_CONTRACT_CANONICAL_SHA256S = {
    "87ae5059953af3a6139388a1a188fc7a7822d187908be0a693bc5ef2250a8f42",
    "a5e3e1dccaefec7842e990f86a9a3327fae6fea05af25fa987361148008c3ad4",
    "dc53f062a51ae38c303fa035d5f726f00e1ac0aa393eb5d39dc7538dca896095",
}
UNBOUND_FIVE_SECOND_DIRECTION_DESIGN_CANONICAL_SHA256 = (
    "d2fdf60144d57b06dcf480a7f09e0297c56f533c8451117268c5f2f1a19e1524"
)


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


def translate_frames_to_direction(
    frames: np.ndarray,
    observation: dict[str, Any],
    trajectory: dict[str, Any],
) -> tuple[np.ndarray, list[list[int]], list[list[float]]]:
    if not observation["all_frames_retain_subject"]:
        raise ValueError("源视频并非每帧都保留可测量红色主体")
    centroids = np.asarray(observation["subject_centroid_by_frame"], dtype=float)
    target_x = np.linspace(
        centroids[0, 0],
        centroids[0, 0] + float(trajectory["target_horizontal_displacement_pixels"]),
        len(frames),
    )
    target_y = np.linspace(centroids[0, 1], centroids[-1, 1], len(frames))
    targets = np.column_stack((target_x, target_y))
    shifts = np.rint(targets - centroids).astype(int)
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

    return np.stack(aligned), shifts.tolist(), targets.tolist()


def derive_direction_frames(
    frames: np.ndarray,
    observation: dict[str, Any],
    trajectory: dict[str, Any],
    temporal_filter: dict[str, Any],
) -> tuple[np.ndarray, list[list[int]], list[list[float]]]:
    aligned, shifts, targets = translate_frames_to_direction(frames, observation, trajectory)
    aligned_array = aligned.astype(np.float32)
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
    return np.stack(mixed), shifts, targets


def derive_spatial_only_frames(
    frames: np.ndarray,
    observation: dict[str, Any],
    trajectory: dict[str, Any],
) -> tuple[np.ndarray, list[list[int]], list[list[float]]]:
    return translate_frames_to_direction(frames, observation, trajectory)


def direction_observation(frames: np.ndarray, measurement: dict[str, Any]) -> dict[str, Any]:
    observation = subject_observation(frames, measurement)
    centroids = observation["subject_centroid_by_frame"]
    if observation["all_frames_retain_subject"]:
        centroid_array = np.asarray(centroids, dtype=float)
        horizontal_steps = np.diff(centroid_array[:, 0])
        observation["adjacent_horizontal_displacement_pixels"] = horizontal_steps.tolist()
        observation["minimum_adjacent_horizontal_displacement_pixels"] = float(horizontal_steps.min())
        observation["net_horizontal_displacement_pixels"] = float(
            centroid_array[-1, 0] - centroid_array[0, 0]
        )
    else:
        observation["adjacent_horizontal_displacement_pixels"] = []
        observation["minimum_adjacent_horizontal_displacement_pixels"] = None
        observation["net_horizontal_displacement_pixels"] = None
    return observation


def threshold_comparisons(observation: dict[str, Any], thresholds: dict[str, Any]) -> dict[str, Any]:
    comparisons = {
        "all_frames_retain_subject": {
            "expected": bool(thresholds["all_frames_retain_subject"]),
            "observed": bool(observation["all_frames_retain_subject"]),
        },
        "net_horizontal_displacement_pixels": {
            "minimum": float(thresholds["minimum_net_horizontal_displacement_pixels"]),
            "observed": observation["net_horizontal_displacement_pixels"],
        },
        "minimum_adjacent_horizontal_displacement_pixels": {
            "minimum": float(thresholds["minimum_adjacent_horizontal_displacement_pixels"]),
            "observed": observation["minimum_adjacent_horizontal_displacement_pixels"],
        },
        "maximum_adjacent_centroid_jump_pixels": {
            "maximum": float(thresholds["maximum_adjacent_centroid_jump_pixels"]),
            "observed": observation["maximum_adjacent_centroid_jump_pixels"],
        },
        "mean_adjacent_centroid_jump_pixels": {
            "maximum": float(thresholds["maximum_mean_adjacent_centroid_jump_pixels"]),
            "observed": observation["mean_adjacent_centroid_jump_pixels"],
        },
    }
    if "maximum_adjacent_subject_area_change_percent" in thresholds:
        comparisons["maximum_adjacent_subject_area_change_percent"] = {
            "maximum": float(thresholds["maximum_adjacent_subject_area_change_percent"]),
            "observed": observation["maximum_adjacent_subject_area_change_percent"],
        }
    comparisons["all_frames_retain_subject"]["within_threshold"] = (
        comparisons["all_frames_retain_subject"]["observed"]
        == comparisons["all_frames_retain_subject"]["expected"]
    )
    for key in ("net_horizontal_displacement_pixels", "minimum_adjacent_horizontal_displacement_pixels"):
        comparisons[key]["within_threshold"] = (
            comparisons[key]["observed"] is not None
            and comparisons[key]["observed"] >= comparisons[key]["minimum"]
        )
    maximum_keys = [
        "maximum_adjacent_centroid_jump_pixels",
        "mean_adjacent_centroid_jump_pixels",
    ]
    if "maximum_adjacent_subject_area_change_percent" in comparisons:
        maximum_keys.append("maximum_adjacent_subject_area_change_percent")
    for key in maximum_keys:
        comparisons[key]["within_threshold"] = (
            comparisons[key]["observed"] is not None
            and comparisons[key]["observed"] <= comparisons[key]["maximum"]
        )
    return comparisons


def validate_contract(contract: dict[str, Any]) -> None:
    canonical = json.dumps(
        contract,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    if hashlib.sha256(canonical).hexdigest() not in FIXED_CONTRACT_CANONICAL_SHA256S:
        raise ValueError("镜头方向派生合同与固定合同不一致")
    required_non_goals = {
        "source_evidence_modification",
        "model_generation",
        "automatic_retry",
        "visual_quality_acceptance",
        "selection_decision",
        "forty_one_frame_expansion",
        "timeline_binding",
        "operator_console_enablement",
        "thirty_second_timeline_creation",
        "institution_freeze",
    }
    if not required_non_goals.issubset(set(contract.get("non_goals", []))):
        raise ValueError("镜头方向派生合同缺少非目标边界")


def validate_unbound_five_second_direction_design(design: dict[str, Any]) -> None:
    canonical = json.dumps(
        design,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    if (
        hashlib.sha256(canonical).hexdigest()
        != UNBOUND_FIVE_SECOND_DIRECTION_DESIGN_CANONICAL_SHA256
    ):
        raise ValueError("五秒方向派生设计与固定设计不一致")
    if design.get("design_status") != "UNBOUND_SOURCE_NOT_EXECUTABLE":
        raise ValueError("未绑定五秒方向派生设计状态无效")
    source_binding = design.get("source_binding", {})
    if source_binding.get("execution_id") != "MUST_BIND_AFTER_SOURCE_EXECUTION":
        raise ValueError("五秒方向派生设计不得预造来源执行标识")
    if source_binding.get("sha256") != "MUST_BIND_AFTER_SOURCE_EXECUTION":
        raise ValueError("五秒方向派生设计不得预造来源摘要")


def write_review_frames(evidence_dir: Path, frames: np.ndarray) -> str:
    frames_dir = evidence_dir / "frames"
    frames_dir.mkdir()
    for index, frame in enumerate(frames, start=1):
        imageio.imwrite(frames_dir / f"frame_{index:03d}.png", frame)
    height, width = frames.shape[1:3]
    gap = 4
    sheet = np.zeros((height * 3 + gap * 4, width * 3 + gap * 4, 3), dtype=np.uint8)
    for index, frame in enumerate(frames):
        row, column = divmod(index, 3)
        y0 = gap + row * (height + gap)
        x0 = gap + column * (width + gap)
        sheet[y0 : y0 + height, x0 : x0 + width] = frame
    contact_sheet_path = evidence_dir / "contact_sheet_9_frames.png"
    imageio.imwrite(contact_sheet_path, sheet)
    return sha256_file(contact_sheet_path)


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
    write_json(
        evidence_dir / "request.json",
        {
            "execution_id": args.execution_id,
            "created_at": started_at,
            "contract": contract,
            "formal_fact_creation": "PROHIBITED",
            "selection_decision_creation": "PROHIBITED",
            "timeline_binding_creation": "PROHIBITED",
        },
    )
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
        source_observation = direction_observation(frames, contract["subject_measurement"])
        if contract.get("frame_processing", {}).get("strategy") == "SPATIAL_TRANSLATION_ONLY":
            derived, shifts, targets = derive_spatial_only_frames(
                frames,
                source_observation,
                contract["trajectory"],
            )
        else:
            derived, shifts, targets = derive_direction_frames(
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
            for frame in derived:
                writer.append_data(frame)
        finally:
            writer.close()
        output_frames, output_metadata = read_video(output_path)
        output_contract = contract["output"]
        if output_metadata["decoded_frame_count"] != output_contract["decoded_frame_count"]:
            raise ValueError("方向派生视频帧数不符合合同")
        if output_metadata["fps"] != float(output_contract["fps"]):
            raise ValueError("方向派生视频帧率不符合合同")
        if abs(output_metadata["duration_seconds"] - float(output_contract["duration_seconds"])) > 0.001:
            raise ValueError("方向派生视频时长不符合合同")
        output_observation = direction_observation(output_frames, contract["subject_measurement"])
        comparisons = threshold_comparisons(output_observation, contract["observation_thresholds"])
        contact_sheet_sha256 = write_review_frames(evidence_dir, output_frames)
        write_json(
            evidence_dir / "frame_metrics.json",
            {
                "source_metadata": source_metadata,
                "source_observation": source_observation,
                "target_centroid_by_frame": targets,
                "translation_by_frame": shifts,
                "output_metadata": output_metadata,
                "output_observation": output_observation,
                "threshold_comparisons": comparisons,
            },
        )
        summary.update(
            {
                "observation": "OBSERVED_OUTPUT_AVAILABLE",
                "output_export_completed": True,
                "output_sha256": sha256_file(output_path),
                "output_bytes": output_path.stat().st_size,
                "contact_sheet_sha256": contact_sheet_sha256,
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
        summary["error_observation"] = {"type": type(exc).__name__, "message": str(exc)}
    summary["elapsed_seconds"] = round(time.perf_counter() - started, 3)
    summary["finished_at"] = utc_now()
    write_json(evidence_dir / "summary.json", summary)
    manifest = write_manifest(evidence_dir)
    print(json.dumps({**summary, "manifest_file_count": manifest["file_count"]}, ensure_ascii=False, indent=2))
    return 0 if summary["output_export_completed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
