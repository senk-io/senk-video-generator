#!/usr/bin/env python3
"""将五个显式关键帧平滑展开为四十帧空间调整候选。"""

from __future__ import annotations

import argparse
import json
import math
import platform
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

import imageio.v2 as imageio
import imageio_ffmpeg
import numpy as np
from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.render_manual_frame_adjustments import (
    EXECUTION_ID_PATTERN,
    EXPECTED_SOURCE,
    REVIEW_STATUSES,
    adjustment_summary,
    apply_adjustments,
    git_value,
    write_adjusted_frames_and_mapping,
    write_before_after_contact_sheet,
)
from tools.run_provider_compatibility_trial import (
    sha256_file,
    utc_now,
    write_json,
    write_manifest,
)
from tools.stabilize_cogvideox_candidate import read_video


DEFAULT_CONTRACT = (
    REPO_ROOT
    / "experiments/postprocessing/cogvideox_shot_002_keyframe_adjustment_v2.json"
)
DEFAULT_EVIDENCE_ROOT = REPO_ROOT / "evidence/runtime"
EXPECTED_CONTRACT_ID = "CR-0026-SHOT-002-KEYFRAME-ADJUSTMENT-DRAFT-001"
EXPECTED_KEYFRAME_NUMBERS = [1, 10, 20, 30, 40]
PARAMETERS = ("x_pixels", "y_pixels", "scale", "rotation_degrees")
REQUIRED_NON_GOALS = {
    "model_generation",
    "automatic_retry",
    "source_evidence_modification",
    "cross_frame_pixel_mixing",
    "automatic_keyframe_selection",
    "automatic_visual_quality_acceptance",
    "formal_ground_truth_creation",
    "selection_decision",
    "timeline_binding",
    "thirty_second_timeline_creation",
}


def _finite_number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} 必须是有限数值")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{field} 必须是有限数值")
    return number


def _simple_filename(value: Any, field: str) -> str:
    filename = str(value)
    if not filename or Path(filename).name != filename:
        raise ValueError(f"{field} 必须是单层文件名")
    return filename


def _validate_transform_values(
    record: dict[str, Any],
    bounds: dict[str, Any],
    label: str,
) -> None:
    x_pixels = _finite_number(record.get("x_pixels"), f"{label}.x_pixels")
    y_pixels = _finite_number(record.get("y_pixels"), f"{label}.y_pixels")
    scale = _finite_number(record.get("scale"), f"{label}.scale")
    rotation = _finite_number(
        record.get("rotation_degrees"), f"{label}.rotation_degrees"
    )
    maximum_translation = float(bounds["maximum_absolute_translation_pixels"])
    if abs(x_pixels) > maximum_translation or abs(y_pixels) > maximum_translation:
        raise ValueError(f"{label} 平移超过合同上限")
    if not float(bounds["minimum_scale"]) <= scale <= float(bounds["maximum_scale"]):
        raise ValueError(f"{label} 缩放超过合同边界")
    if abs(rotation) > float(bounds["maximum_absolute_rotation_degrees"]):
        raise ValueError(f"{label} 旋转超过合同上限")


def _validate_review(record: dict[str, Any], label: str) -> None:
    status = record.get("review_status")
    if status not in REVIEW_STATUSES:
        raise ValueError(f"{label} 人工审阅状态无效")
    if not str(record.get("adjustment_reason", "")).strip():
        raise ValueError(f"{label} 必须填写调整原因")
    if status in {"HUMAN_APPROVED", "HUMAN_REJECTED"}:
        if not str(record.get("reviewer", "")).strip() or not str(
            record.get("reviewed_at", "")
        ).strip():
            raise ValueError(f"{label} 人工裁决必须记录评审者和时间")


def validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("contract_id") != EXPECTED_CONTRACT_ID:
        raise ValueError("关键帧合同标识无效")
    if contract.get("contract_status") != "DRAFT_KEYFRAME_AUTOMATION_PENDING_REVIEW":
        raise ValueError("关键帧合同必须保持待人工审阅草案状态")
    if contract.get("contract_version") != 2 or contract.get("shot_id") != "SHOT-002":
        raise ValueError("关键帧合同版本或镜头绑定无效")
    if not REQUIRED_NON_GOALS.issubset(set(contract.get("non_goals", []))):
        raise ValueError("关键帧合同缺少非目标边界")

    policy = contract.get("policy_context", {})
    if policy.get("action") != "DERIVE_EXISTING_CANDIDATE":
        raise ValueError("关键帧策略行动无效")
    if int(policy.get("maximum_model_runs", -1)) != 0:
        raise ValueError("关键帧合同不得授权模型运行")
    if int(policy.get("maximum_derivation_runs_per_execution_id", 0)) != 1:
        raise ValueError("每个执行标识只允许一次关键帧派生")
    if contract.get("source") != EXPECTED_SOURCE:
        raise ValueError("关键帧来源必须与固定 Shot 002 候选完全一致")

    semantics = contract.get("transform_semantics", {})
    expected_semantics = {
        "coordinate_system": "IMAGE_X_RIGHT_Y_DOWN",
        "positive_rotation_direction": "CLOCKWISE_IN_IMAGE_COORDINATES",
        "origin": "FRAME_CENTER",
        "operation_order": "SCALE_ROTATE_TRANSLATE",
        "interpolation": "BICUBIC",
        "edge_fill": "EDGE_REPLICATION",
        "temporal_mix": "NONE",
        "local_adjustment_support": "RESERVED_EMPTY_ONLY_V2",
    }
    for key, expected in expected_semantics.items():
        if semantics.get(key) != expected:
            raise ValueError(f"关键帧空间变换语义无效：{key}")
    if int(semantics.get("edge_replication_padding_pixels", 0)) < 256:
        raise ValueError("边缘复制填充不得小于 256 像素")

    interpolation = contract.get("interpolation", {})
    expected_interpolation = {
        "strategy": "MONOTONE_CUBIC_HERMITE",
        "frame_domain_start": 1,
        "frame_domain_end": 40,
        "parameters": list(PARAMETERS),
        "precision_decimal_places": 6,
        "exact_keyframe_preservation": True,
        "segment_overshoot": "PROHIBITED",
        "manual_override_order": "AFTER_INTERPOLATION",
    }
    if interpolation != expected_interpolation:
        raise ValueError("关键帧插值合同无效")

    bounds = contract.get("bounds", {})
    maximum_translation = _finite_number(
        bounds.get("maximum_absolute_translation_pixels"),
        "bounds.maximum_absolute_translation_pixels",
    )
    minimum_scale = _finite_number(bounds.get("minimum_scale"), "bounds.minimum_scale")
    maximum_scale = _finite_number(bounds.get("maximum_scale"), "bounds.maximum_scale")
    maximum_rotation = _finite_number(
        bounds.get("maximum_absolute_rotation_degrees"),
        "bounds.maximum_absolute_rotation_degrees",
    )
    if not (0 <= maximum_translation <= 192):
        raise ValueError("关键帧平移上限无效")
    if not (0.85 <= minimum_scale <= 1 <= maximum_scale <= 1.15):
        raise ValueError("关键帧缩放边界无效")
    if not (0 <= maximum_rotation <= 8):
        raise ValueError("关键帧旋转上限无效")
    if int(bounds.get("maximum_manual_overrides", -1)) != 40:
        raise ValueError("单帧覆盖数量上限无效")
    if int(bounds.get("maximum_local_adjustments_per_frame", -1)) != 0:
        raise ValueError("v2 不允许局部像素修正")

    keyframes = contract.get("keyframes")
    if not isinstance(keyframes, list) or [
        item.get("frame_number") for item in keyframes
    ] != EXPECTED_KEYFRAME_NUMBERS:
        raise ValueError("关键帧必须固定为第 1、10、20、30、40 帧")
    for keyframe in keyframes:
        label = f"关键帧 {keyframe['frame_number']}"
        _validate_transform_values(keyframe, bounds, label)
        _validate_review(keyframe, label)

    overrides = contract.get("manual_overrides")
    if not isinstance(overrides, list) or len(overrides) > 40:
        raise ValueError("单帧覆盖列表无效")
    override_numbers = [item.get("frame_number") for item in overrides]
    if override_numbers != sorted(set(override_numbers)):
        raise ValueError("单帧覆盖必须按帧号升序且不得重复")
    if set(override_numbers).intersection(EXPECTED_KEYFRAME_NUMBERS):
        raise ValueError("关键帧必须直接修改，不得再由单帧覆盖替换")
    for override in overrides:
        number = override.get("frame_number")
        if not isinstance(number, int) or isinstance(number, bool) or not 1 <= number <= 40:
            raise ValueError("单帧覆盖帧号无效")
        label = f"单帧覆盖 {number}"
        _validate_transform_values(override, bounds, label)
        _validate_review(override, label)

    output = contract.get("output", {})
    if (
        int(output.get("decoded_frame_count", 0)) != 40
        or float(output.get("fps", 0)) != 8.0
        or abs(float(output.get("duration_seconds", 0)) - 5.0) > 0.001
    ):
        raise ValueError("关键帧输出帧数、帧率或时长无效")
    _simple_filename(output.get("filename"), "output.filename")
    if output.get("codec") != "libx264" or output.get("pixel_format") != "yuv420p":
        raise ValueError("关键帧输出编码合同无效")
    review_artifacts = contract.get("review_artifacts", {})
    _simple_filename(
        review_artifacts.get("before_after_contact_sheet_filename"),
        "review_artifacts.before_after_contact_sheet_filename",
    )
    if int(review_artifacts.get("contact_sheet_columns", 0)) <= 0:
        raise ValueError("关键帧联系图列数无效")
    if int(review_artifacts.get("thumbnail_width_pixels", 0)) <= 0:
        raise ValueError("关键帧联系图缩略图尺寸无效")
    review = contract.get("review", {})
    if review.get("authority") != "EXPLICIT_HUMAN_REVIEW_REQUIRED":
        raise ValueError("关键帧人工审阅权威边界无效")
    if review.get("overall_status") != "PENDING_REVIEW":
        raise ValueError("关键帧整体审阅状态不得预先升级")


def monotone_cubic_interpolate(
    keyframe_numbers: np.ndarray,
    keyframe_values: np.ndarray,
    frame_numbers: np.ndarray,
) -> np.ndarray:
    """使用不越过单调区间端点的分段三次 Hermite 插值。"""
    x = np.asarray(keyframe_numbers, dtype=float)
    y = np.asarray(keyframe_values, dtype=float)
    query = np.asarray(frame_numbers, dtype=float)
    if len(x) != len(y) or len(x) < 2 or np.any(np.diff(x) <= 0):
        raise ValueError("关键帧插值输入无效")
    if query.min() < x[0] or query.max() > x[-1]:
        raise ValueError("插值查询超出关键帧范围")

    h = np.diff(x)
    delta = np.diff(y) / h
    slopes = np.zeros_like(y)
    if len(x) == 2:
        slopes[:] = delta[0]
    else:
        for index in range(1, len(x) - 1):
            before = delta[index - 1]
            after = delta[index]
            if before == 0 or after == 0 or np.sign(before) != np.sign(after):
                slopes[index] = 0
            else:
                weight_before = 2 * h[index] + h[index - 1]
                weight_after = h[index] + 2 * h[index - 1]
                slopes[index] = (weight_before + weight_after) / (
                    weight_before / before + weight_after / after
                )
        slopes[0] = _endpoint_slope(h[0], h[1], delta[0], delta[1])
        slopes[-1] = _endpoint_slope(h[-1], h[-2], delta[-1], delta[-2])

    result = np.empty_like(query)
    for query_index, value in enumerate(query):
        segment = min(int(np.searchsorted(x, value, side="right") - 1), len(x) - 2)
        segment = max(segment, 0)
        normalized = (value - x[segment]) / h[segment]
        h00 = 2 * normalized**3 - 3 * normalized**2 + 1
        h10 = normalized**3 - 2 * normalized**2 + normalized
        h01 = -2 * normalized**3 + 3 * normalized**2
        h11 = normalized**3 - normalized**2
        result[query_index] = (
            h00 * y[segment]
            + h10 * h[segment] * slopes[segment]
            + h01 * y[segment + 1]
            + h11 * h[segment] * slopes[segment + 1]
        )
    return result


def _endpoint_slope(
    current_width: float,
    adjacent_width: float,
    current_delta: float,
    adjacent_delta: float,
) -> float:
    slope = (
        (2 * current_width + adjacent_width) * current_delta
        - current_width * adjacent_delta
    ) / (current_width + adjacent_width)
    if np.sign(slope) != np.sign(current_delta):
        return 0.0
    if np.sign(current_delta) != np.sign(adjacent_delta) and abs(slope) > abs(
        3 * current_delta
    ):
        return 3 * current_delta
    return float(slope)


def expand_keyframes(contract: dict[str, Any]) -> list[dict[str, Any]]:
    validate_contract(contract)
    keyframes = contract["keyframes"]
    keyframe_numbers = np.asarray(EXPECTED_KEYFRAME_NUMBERS, dtype=float)
    frame_numbers = np.arange(1, 41, dtype=float)
    precision = int(contract["interpolation"]["precision_decimal_places"])
    parameter_values: dict[str, np.ndarray] = {}
    for parameter in PARAMETERS:
        keyframe_values = np.asarray(
            [float(item[parameter]) for item in keyframes], dtype=float
        )
        values = monotone_cubic_interpolate(
            keyframe_numbers, keyframe_values, frame_numbers
        )
        for keyframe_number, keyframe_value in zip(
            EXPECTED_KEYFRAME_NUMBERS, keyframe_values, strict=True
        ):
            values[keyframe_number - 1] = keyframe_value
        for start, end in zip(
            EXPECTED_KEYFRAME_NUMBERS[:-1], EXPECTED_KEYFRAME_NUMBERS[1:], strict=True
        ):
            low = min(values[start - 1], values[end - 1]) - 1e-9
            high = max(values[start - 1], values[end - 1]) + 1e-9
            if np.any(values[start - 1 : end] < low) or np.any(
                values[start - 1 : end] > high
            ):
                raise ValueError(f"{parameter} 插值越过关键帧区间")
        parameter_values[parameter] = np.round(values, precision)

    keyframe_by_number = {item["frame_number"]: item for item in keyframes}
    expanded = []
    for number in range(1, 41):
        keyframe = keyframe_by_number.get(number)
        if keyframe is None:
            left = max(item for item in EXPECTED_KEYFRAME_NUMBERS if item < number)
            right = min(item for item in EXPECTED_KEYFRAME_NUMBERS if item > number)
            review_status = "PENDING_REVIEW"
            reason = f"AUTO_INTERPOLATED_FROM_KEYFRAMES_{left}_{right}"
            parameter_source = "INTERPOLATED_MONOTONE_CUBIC"
        else:
            review_status = keyframe["review_status"]
            reason = keyframe["adjustment_reason"]
            parameter_source = "EXPLICIT_KEYFRAME"
        expanded.append(
            {
                "frame_number": number,
                "source_frame": f"frames/frame_{number:03d}.png",
                **{
                    parameter: float(parameter_values[parameter][number - 1])
                    for parameter in PARAMETERS
                },
                "local_adjustments": [],
                "parameter_source": parameter_source,
                "interpolation_keyframes": [number, number]
                if keyframe is not None
                else [left, right],
                "review_status": review_status,
                "adjustment_reason": reason,
                "reviewer": keyframe.get("reviewer") if keyframe else None,
                "reviewed_at": keyframe.get("reviewed_at") if keyframe else None,
            }
        )

    for override in contract["manual_overrides"]:
        number = override["frame_number"]
        expanded[number - 1].update(
            {
                **{parameter: float(override[parameter]) for parameter in PARAMETERS},
                "parameter_source": "EXPLICIT_MANUAL_OVERRIDE",
                "interpolation_keyframes": None,
                "review_status": override["review_status"],
                "adjustment_reason": override["adjustment_reason"],
                "reviewer": override.get("reviewer"),
                "reviewed_at": override.get("reviewed_at"),
            }
        )
    return expanded


def interpolation_observation(
    contract: dict[str, Any], expanded: list[dict[str, Any]]
) -> dict[str, Any]:
    source_counts = Counter(item["parameter_source"] for item in expanded)
    return {
        "strategy": contract["interpolation"]["strategy"],
        "keyframe_numbers": EXPECTED_KEYFRAME_NUMBERS,
        "keyframe_count": len(contract["keyframes"]),
        "manual_override_count": len(contract["manual_overrides"]),
        "expanded_frame_count": len(expanded),
        "parameter_source_counts": dict(sorted(source_counts.items())),
        "cross_frame_pixel_mixing": False,
        "exact_keyframe_preservation": True,
        "segment_overshoot_observed": False,
    }


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
    expanded = expand_keyframes(contract)
    evidence_root = Path(args.evidence_root).resolve()
    evidence_dir = evidence_root / args.execution_id
    if evidence_dir.exists():
        raise SystemExit(f"证据目录已经存在，拒绝覆盖：{evidence_dir}")
    evidence_dir.mkdir(parents=True)

    started_at = utc_now()
    started = time.perf_counter()
    contract_sha256 = sha256_file(contract_path)
    write_json(evidence_dir / "expanded_frame_adjustments.json", expanded)
    expanded_sha256 = sha256_file(evidence_dir / "expanded_frame_adjustments.json")
    write_json(
        evidence_dir / "request.json",
        {
            "execution_id": args.execution_id,
            "created_at": started_at,
            "contract_sha256": contract_sha256,
            "expanded_frame_adjustments_sha256": expanded_sha256,
            "contract": contract,
            "model_generation": "PROHIBITED",
            "formal_ground_truth_creation": "PROHIBITED",
            "formal_visual_quality_acceptance": "PROHIBITED",
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
            "pillow_version": Image.__version__,
            "bundled_ffmpeg_version": imageio_ffmpeg.get_ffmpeg_version(),
            "git_head": git_value("rev-parse", "HEAD"),
            "git_status_porcelain": git_value("status", "--porcelain") or "",
            "harness_sha256": sha256_file(Path(__file__)),
            "contract_sha256": contract_sha256,
            "expanded_frame_adjustments_sha256": expanded_sha256,
            "sensitive_machine_identifiers_recorded": False,
        },
    )
    source = contract["source"]
    summary: dict[str, Any] = {
        "execution_id": args.execution_id,
        "started_at": started_at,
        "contract_id": contract["contract_id"],
        "contract_status": contract["contract_status"],
        "contract_sha256": contract_sha256,
        "expanded_frame_adjustments_sha256": expanded_sha256,
        "shot_id": contract["shot_id"],
        "source_execution_id": source["execution_id"],
        "source_filename": source["filename"],
        "source_sha256": source["sha256"],
        "observation": "OBSERVED_EXECUTION_WITHOUT_OUTPUT",
        "output_export_completed": False,
        "model_run_count": 0,
        "formal_ground_truth_created": False,
        "formal_visual_quality_acceptance_created": False,
        "selection_decision_created": False,
        "timeline_binding_created": False,
    }
    try:
        source_path = evidence_root / source["execution_id"] / source["filename"]
        if not source_path.is_file() or sha256_file(source_path) != source["sha256"]:
            raise ValueError("来源视频不存在或摘要不匹配")
        source_frames, source_metadata = read_video(source_path)
        if source_metadata["decoded_frame_count"] != 40:
            raise ValueError("来源视频帧数不符合合同")
        if source_metadata["fps"] != 8.0 or abs(source_metadata["duration_seconds"] - 5.0) > 0.001:
            raise ValueError("来源视频帧率或时长不符合合同")

        padding = int(contract["transform_semantics"]["edge_replication_padding_pixels"])
        adjusted_frames = apply_adjustments(source_frames, expanded, padding)
        output = contract["output"]
        output_path = evidence_dir / output["filename"]
        writer = imageio.get_writer(
            output_path,
            fps=output["fps"],
            codec=output["codec"],
            pixelformat=output["pixel_format"],
        )
        try:
            for frame in adjusted_frames:
                writer.append_data(frame)
        finally:
            writer.close()
        _, output_metadata = read_video(output_path)
        if output_metadata["decoded_frame_count"] != 40:
            raise ValueError("关键帧派生输出帧数不符合合同")
        if output_metadata["fps"] != 8.0 or abs(output_metadata["duration_seconds"] - 5.0) > 0.001:
            raise ValueError("关键帧派生输出帧率或时长不符合合同")

        mapping = write_adjusted_frames_and_mapping(
            evidence_dir, source_frames, adjusted_frames, expanded
        )
        for mapping_item, expanded_item in zip(mapping, expanded, strict=True):
            mapping_item["parameter_source"] = expanded_item["parameter_source"]
            mapping_item["interpolation_keyframes"] = expanded_item[
                "interpolation_keyframes"
            ]
        write_json(evidence_dir / "frame_mapping.json", mapping)
        review_artifacts = contract["review_artifacts"]
        contact_sheet_path = evidence_dir / review_artifacts[
            "before_after_contact_sheet_filename"
        ]
        write_before_after_contact_sheet(
            contact_sheet_path,
            source_frames,
            adjusted_frames,
            int(review_artifacts["contact_sheet_columns"]),
            int(review_artifacts["thumbnail_width_pixels"]),
        )
        parameter_observation = adjustment_summary(expanded)
        interpolation = interpolation_observation(contract, expanded)
        write_json(
            evidence_dir / "adjustment_summary.json",
            {
                "source_metadata": source_metadata,
                "output_metadata": output_metadata,
                "interpolation_observation": interpolation,
                "parameter_observation": parameter_observation,
                "pixel_identical_before_encoding_by_frame": [
                    bool(np.array_equal(source_frame, adjusted_frame))
                    for source_frame, adjusted_frame in zip(
                        source_frames, adjusted_frames, strict=True
                    )
                ],
            },
        )
        review_record = {
            "contract_id": contract["contract_id"],
            "contract_sha256": contract_sha256,
            "shot_id": contract["shot_id"],
            "authority": contract["review"]["authority"],
            "overall_status": contract["review"]["overall_status"],
            "keyframe_review_status_counts": dict(
                sorted(Counter(item["review_status"] for item in contract["keyframes"]).items())
            ),
            "manual_override_review_status_counts": dict(
                sorted(
                    Counter(
                        item["review_status"] for item in contract["manual_overrides"]
                    ).items()
                )
            ),
            "expanded_frame_review_status_counts": parameter_observation[
                "review_status_counts"
            ],
            "formal_ground_truth_created": False,
            "formal_visual_quality_acceptance_created": False,
            "selection_decision_created": False,
            "timeline_binding_created": False,
            "recorded_at": utc_now(),
        }
        write_json(evidence_dir / "review_record.json", review_record)
        summary.update(
            {
                "observation": "OBSERVED_OUTPUT_AVAILABLE",
                "output_export_completed": True,
                "output_filename": output["filename"],
                "output_sha256": sha256_file(output_path),
                "output_bytes": output_path.stat().st_size,
                "source_metadata": source_metadata,
                "output_metadata": output_metadata,
                "interpolation_observation": interpolation,
                "parameter_observation": parameter_observation,
                "before_after_contact_sheet_filename": contact_sheet_path.name,
                "before_after_contact_sheet_sha256": sha256_file(contact_sheet_path),
                "frame_mapping_filename": "frame_mapping.json",
                "expanded_frame_adjustments_filename": "expanded_frame_adjustments.json",
                "review_record_filename": "review_record.json",
                "ground_truth_status": "PENDING_HUMAN_REVIEW",
            }
        )
    except BaseException as exc:
        summary["error_observation"] = {"type": type(exc).__name__, "message": str(exc)}
    summary["elapsed_seconds"] = round(time.perf_counter() - started, 3)
    summary["finished_at"] = utc_now()
    write_json(evidence_dir / "summary.json", summary)
    manifest = write_manifest(evidence_dir)
    print(
        json.dumps(
            {**summary, "manifest_file_count": manifest["file_count"]},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if summary["output_export_completed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
