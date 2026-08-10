#!/usr/bin/env python3
"""按显式逐帧合同渲染 Shot 002 的非权威手工调整候选。"""

from __future__ import annotations

import argparse
import json
import math
import platform
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

import imageio.v2 as imageio
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.run_provider_compatibility_trial import (
    sha256_file,
    utc_now,
    write_json,
    write_manifest,
)
from tools.stabilize_cogvideox_candidate import read_video


DEFAULT_CONTRACT = (
    REPO_ROOT
    / "experiments/postprocessing/cogvideox_shot_002_manual_frame_adjustment_v1.json"
)
DEFAULT_EVIDENCE_ROOT = REPO_ROOT / "evidence/runtime"
EXECUTION_ID_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9._-]{2,127}")
REVIEW_STATUSES = {
    "PENDING_REVIEW",
    "ADJUSTED_PENDING_REVIEW",
    "HUMAN_APPROVED",
    "HUMAN_REJECTED",
}
REQUIRED_NON_GOALS = {
    "model_generation",
    "automatic_retry",
    "source_evidence_modification",
    "cross_frame_pixel_mixing",
    "automatic_trajectory_interpolation",
    "formal_visual_quality_acceptance",
    "selection_decision",
    "timeline_binding",
    "thirty_second_timeline_creation",
}
EXPECTED_CONTRACT_ID = "CR-0025-SHOT-002-MANUAL-FRAME-ADJUSTMENT-DRAFT-001"
EXPECTED_SOURCE = {
    "execution_id": "LM-COGVIDEOX-SHOT-002-5S-RIGHTWARD-BOUND-20260810T033318Z",
    "filename": "direction_controlled_5s.mp4",
    "sha256": "73278576b53bff3126582cd630f3a3c3a907f6f78b6e25ebde99159eb6a49616",
    "decoded_frame_count": 40,
    "fps": 8,
    "duration_seconds": 5.0,
}


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


def validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("contract_id") != EXPECTED_CONTRACT_ID:
        raise ValueError("逐帧调整合同标识无效")
    if contract.get("contract_status") != "DRAFT_MANUAL_GROUND_TRUTH_PENDING_REVIEW":
        raise ValueError("逐帧调整合同必须保持待人工审阅草案状态")
    if contract.get("shot_id") != "SHOT-002":
        raise ValueError("逐帧调整合同只允许绑定 SHOT-002")
    if not REQUIRED_NON_GOALS.issubset(set(contract.get("non_goals", []))):
        raise ValueError("逐帧调整合同缺少非目标边界")

    policy = contract.get("policy_context", {})
    if policy.get("action") != "DERIVE_EXISTING_CANDIDATE":
        raise ValueError("逐帧调整策略行动无效")
    if int(policy.get("maximum_model_runs", -1)) != 0:
        raise ValueError("逐帧调整合同不得授权模型运行")
    if int(policy.get("maximum_derivation_runs_per_execution_id", 0)) != 1:
        raise ValueError("每个执行标识只允许一次派生")

    source = contract.get("source", {})
    if source != EXPECTED_SOURCE:
        raise ValueError("逐帧调整来源必须与固定 Shot 002 候选完全一致")
    frame_count = int(source.get("decoded_frame_count", 0))
    if frame_count != 40 or float(source.get("fps", 0)) != 8.0:
        raise ValueError("来源必须固定为 40 帧、8 fps")
    if abs(float(source.get("duration_seconds", 0)) - 5.0) > 0.001:
        raise ValueError("来源必须固定为精确 5 秒")
    if not re.fullmatch(r"[0-9a-f]{64}", str(source.get("sha256", ""))):
        raise ValueError("来源摘要无效")
    _simple_filename(source.get("filename"), "source.filename")

    semantics = contract.get("transform_semantics", {})
    expected_semantics = {
        "origin": "FRAME_CENTER",
        "operation_order": "SCALE_ROTATE_TRANSLATE",
        "interpolation": "BICUBIC",
        "edge_fill": "EDGE_REPLICATION",
        "temporal_mix": "NONE",
        "local_adjustment_support": "RESERVED_EMPTY_ONLY_V1",
    }
    for key, expected in expected_semantics.items():
        if semantics.get(key) != expected:
            raise ValueError(f"逐帧变换语义无效：{key}")
    padding = int(semantics.get("edge_replication_padding_pixels", 0))
    if padding < 256:
        raise ValueError("边缘复制填充不得小于 256 像素")

    bounds = contract.get("bounds", {})
    max_translation = _finite_number(
        bounds.get("maximum_absolute_translation_pixels"),
        "bounds.maximum_absolute_translation_pixels",
    )
    min_scale = _finite_number(bounds.get("minimum_scale"), "bounds.minimum_scale")
    max_scale = _finite_number(bounds.get("maximum_scale"), "bounds.maximum_scale")
    max_rotation = _finite_number(
        bounds.get("maximum_absolute_rotation_degrees"),
        "bounds.maximum_absolute_rotation_degrees",
    )
    if not (0 <= max_translation <= 192):
        raise ValueError("逐帧平移上限无效")
    if not (0.85 <= min_scale <= 1.0 <= max_scale <= 1.15):
        raise ValueError("逐帧缩放边界无效")
    if not (0 <= max_rotation <= 8):
        raise ValueError("逐帧旋转上限无效")
    if int(bounds.get("maximum_local_adjustments_per_frame", -1)) != 0:
        raise ValueError("v1 不允许局部修正执行")

    output = contract.get("output", {})
    if int(output.get("decoded_frame_count", 0)) != frame_count:
        raise ValueError("输出帧数必须与来源一致")
    if float(output.get("fps", 0)) != 8.0:
        raise ValueError("输出帧率必须固定为 8 fps")
    if abs(float(output.get("duration_seconds", 0)) - 5.0) > 0.001:
        raise ValueError("输出时长必须固定为 5 秒")
    _simple_filename(output.get("filename"), "output.filename")
    if output.get("codec") != "libx264" or output.get("pixel_format") != "yuv420p":
        raise ValueError("输出编码合同无效")

    frames = contract.get("frames")
    if not isinstance(frames, list) or len(frames) != frame_count:
        raise ValueError("逐帧调整合同必须显式包含 40 帧")
    expected_numbers = list(range(1, frame_count + 1))
    observed_numbers = [frame.get("frame_number") for frame in frames]
    if observed_numbers != expected_numbers:
        raise ValueError("逐帧编号必须从 1 到 40 连续且唯一")

    for frame in frames:
        number = frame["frame_number"]
        expected_source_frame = f"frames/frame_{number:03d}.png"
        if frame.get("source_frame") != expected_source_frame:
            raise ValueError(f"第 {number} 帧来源映射无效")
        x_pixels = _finite_number(frame.get("x_pixels"), f"frames[{number}].x_pixels")
        y_pixels = _finite_number(frame.get("y_pixels"), f"frames[{number}].y_pixels")
        scale = _finite_number(frame.get("scale"), f"frames[{number}].scale")
        rotation = _finite_number(
            frame.get("rotation_degrees"), f"frames[{number}].rotation_degrees"
        )
        if abs(x_pixels) > max_translation or abs(y_pixels) > max_translation:
            raise ValueError(f"第 {number} 帧平移超过合同上限")
        if not min_scale <= scale <= max_scale:
            raise ValueError(f"第 {number} 帧缩放超过合同边界")
        if abs(rotation) > max_rotation:
            raise ValueError(f"第 {number} 帧旋转超过合同上限")
        if frame.get("local_adjustments") != []:
            raise ValueError(f"第 {number} 帧 v1 局部修正必须为空")
        status = frame.get("review_status")
        if status not in REVIEW_STATUSES:
            raise ValueError(f"第 {number} 帧人工审阅状态无效")
        changed = any((x_pixels, y_pixels, rotation)) or scale != 1.0
        reason = str(frame.get("adjustment_reason", "")).strip()
        if changed and not reason:
            raise ValueError(f"第 {number} 帧发生调整时必须填写原因")
        if status in {"HUMAN_APPROVED", "HUMAN_REJECTED"}:
            if not str(frame.get("reviewer", "")).strip() or not str(
                frame.get("reviewed_at", "")
            ).strip():
                raise ValueError(f"第 {number} 帧人工裁决必须记录评审者和时间")

    review = contract.get("review", {})
    if review.get("authority") != "EXPLICIT_HUMAN_REVIEW_REQUIRED":
        raise ValueError("逐帧审阅权威边界无效")
    if review.get("overall_status") != "PENDING_REVIEW":
        raise ValueError("整体审阅状态不得预先升级")


def transform_frame(frame: np.ndarray, adjustment: dict[str, Any], padding: int) -> np.ndarray:
    """围绕画面中心执行确定性的缩放、旋转、平移。"""
    x_pixels = float(adjustment["x_pixels"])
    y_pixels = float(adjustment["y_pixels"])
    scale = float(adjustment["scale"])
    rotation = float(adjustment["rotation_degrees"])
    if x_pixels == 0 and y_pixels == 0 and scale == 1 and rotation == 0:
        return frame.copy()

    height, width = frame.shape[:2]
    padded = np.pad(
        frame,
        ((padding, padding), (padding, padding), (0, 0)),
        mode="edge",
    )
    radians = math.radians(rotation)
    cosine = math.cos(radians) / scale
    sine = math.sin(radians) / scale
    inverse_a = cosine
    inverse_b = sine
    inverse_c = -sine
    inverse_d = cosine
    center_x = (width - 1) / 2.0
    center_y = (height - 1) / 2.0
    inverse_e = (
        center_x
        + padding
        - inverse_a * (center_x + x_pixels)
        - inverse_b * (center_y + y_pixels)
    )
    inverse_f = (
        center_y
        + padding
        - inverse_c * (center_x + x_pixels)
        - inverse_d * (center_y + y_pixels)
    )
    image = Image.fromarray(padded)
    transformed = image.transform(
        (width, height),
        Image.Transform.AFFINE,
        (inverse_a, inverse_b, inverse_e, inverse_c, inverse_d, inverse_f),
        resample=Image.Resampling.BICUBIC,
    )
    return np.asarray(transformed, dtype=np.uint8)


def apply_adjustments(
    frames: np.ndarray,
    adjustments: list[dict[str, Any]],
    padding: int,
) -> np.ndarray:
    if len(frames) != len(adjustments):
        raise ValueError("来源帧数与逐帧参数数量不一致")
    return np.stack(
        [
            transform_frame(frame, adjustment, padding)
            for frame, adjustment in zip(frames, adjustments, strict=True)
        ]
    )


def write_adjusted_frames_and_mapping(
    evidence_dir: Path,
    source_frames: np.ndarray,
    adjusted_frames: np.ndarray,
    adjustments: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    frames_dir = evidence_dir / "adjusted_frames"
    frames_dir.mkdir()
    mapping = []
    for source_frame, adjusted_frame, adjustment in zip(
        source_frames, adjusted_frames, adjustments, strict=True
    ):
        number = int(adjustment["frame_number"])
        filename = f"frame_{number:03d}.png"
        adjusted_path = frames_dir / filename
        imageio.imwrite(adjusted_path, adjusted_frame)
        mapping.append(
            {
                "frame_number": number,
                "source_frame": adjustment["source_frame"],
                "adjusted_frame": f"adjusted_frames/{filename}",
                "source_frame_pixel_sha256": _array_sha256(source_frame),
                "adjusted_frame_sha256": sha256_file(adjusted_path),
                "transform": {
                    "x_pixels": adjustment["x_pixels"],
                    "y_pixels": adjustment["y_pixels"],
                    "scale": adjustment["scale"],
                    "rotation_degrees": adjustment["rotation_degrees"],
                    "local_adjustments": adjustment["local_adjustments"],
                },
                "review_status": adjustment["review_status"],
                "adjustment_reason": adjustment.get("adjustment_reason", ""),
                "reviewer": adjustment.get("reviewer"),
                "reviewed_at": adjustment.get("reviewed_at"),
            }
        )
    return mapping


def _array_sha256(frame: np.ndarray) -> str:
    import hashlib

    return hashlib.sha256(frame.tobytes()).hexdigest()


def write_before_after_contact_sheet(
    path: Path,
    source_frames: np.ndarray,
    adjusted_frames: np.ndarray,
    columns: int,
    thumbnail_width: int,
) -> None:
    if columns <= 0 or thumbnail_width <= 0:
        raise ValueError("联系图布局无效")
    height, width = source_frames.shape[1:3]
    thumbnail_height = round(height * thumbnail_width / width)
    label_height = 22
    gap = 4
    cell_width = thumbnail_width * 2 + gap
    cell_height = thumbnail_height + label_height
    rows = math.ceil(len(source_frames) / columns)
    sheet = Image.new(
        "RGB",
        (
            gap + columns * (cell_width + gap),
            gap + rows * (cell_height + gap),
        ),
        "black",
    )
    draw = ImageDraw.Draw(sheet)
    for index, (source_frame, adjusted_frame) in enumerate(
        zip(source_frames, adjusted_frames, strict=True), start=1
    ):
        row, column = divmod(index - 1, columns)
        x0 = gap + column * (cell_width + gap)
        y0 = gap + row * (cell_height + gap)
        source_image = Image.fromarray(source_frame).resize(
            (thumbnail_width, thumbnail_height), Image.Resampling.LANCZOS
        )
        adjusted_image = Image.fromarray(adjusted_frame).resize(
            (thumbnail_width, thumbnail_height), Image.Resampling.LANCZOS
        )
        sheet.paste(source_image, (x0, y0 + label_height))
        sheet.paste(adjusted_image, (x0 + thumbnail_width + gap, y0 + label_height))
        draw.text((x0 + 4, y0 + 4), f"F{index:03d} SOURCE", fill="white")
        draw.text(
            (x0 + thumbnail_width + gap + 4, y0 + 4),
            f"F{index:03d} ADJUSTED",
            fill="white",
        )
    sheet.save(path)


def adjustment_summary(adjustments: list[dict[str, Any]]) -> dict[str, Any]:
    status_counts = Counter(frame["review_status"] for frame in adjustments)
    changed = [
        frame
        for frame in adjustments
        if any(
            (
                float(frame["x_pixels"]),
                float(frame["y_pixels"]),
                float(frame["rotation_degrees"]),
            )
        )
        or float(frame["scale"]) != 1.0
    ]
    return {
        "frame_count": len(adjustments),
        "identity_frame_count": len(adjustments) - len(changed),
        "changed_frame_count": len(changed),
        "changed_frame_numbers": [frame["frame_number"] for frame in changed],
        "maximum_absolute_x_pixels": max(abs(float(frame["x_pixels"])) for frame in adjustments),
        "maximum_absolute_y_pixels": max(abs(float(frame["y_pixels"])) for frame in adjustments),
        "minimum_scale": min(float(frame["scale"]) for frame in adjustments),
        "maximum_scale": max(float(frame["scale"]) for frame in adjustments),
        "maximum_absolute_rotation_degrees": max(
            abs(float(frame["rotation_degrees"])) for frame in adjustments
        ),
        "review_status_counts": dict(sorted(status_counts.items())),
        "all_frames_human_approved": status_counts.get("HUMAN_APPROVED", 0)
        == len(adjustments),
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
    evidence_root = Path(args.evidence_root).resolve()
    evidence_dir = evidence_root / args.execution_id
    if evidence_dir.exists():
        raise SystemExit(f"证据目录已经存在，拒绝覆盖：{evidence_dir}")
    evidence_dir.mkdir(parents=True)

    started_at = utc_now()
    started = time.perf_counter()
    source = contract["source"]
    contract_sha256 = sha256_file(contract_path)
    write_json(
        evidence_dir / "request.json",
        {
            "execution_id": args.execution_id,
            "created_at": started_at,
            "contract_sha256": contract_sha256,
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
            "sensitive_machine_identifiers_recorded": False,
        },
    )
    summary: dict[str, Any] = {
        "execution_id": args.execution_id,
        "started_at": started_at,
        "contract_id": contract["contract_id"],
        "contract_status": contract["contract_status"],
        "contract_sha256": contract_sha256,
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
        if source_metadata["decoded_frame_count"] != source["decoded_frame_count"]:
            raise ValueError("来源视频帧数不符合合同")
        if source_metadata["fps"] != float(source["fps"]):
            raise ValueError("来源视频帧率不符合合同")
        if abs(source_metadata["duration_seconds"] - float(source["duration_seconds"])) > 0.001:
            raise ValueError("来源视频时长不符合合同")

        adjustments = contract["frames"]
        padding = int(contract["transform_semantics"]["edge_replication_padding_pixels"])
        adjusted_frames = apply_adjustments(source_frames, adjustments, padding)
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
        if output_metadata["decoded_frame_count"] != output["decoded_frame_count"]:
            raise ValueError("输出视频帧数不符合合同")
        if output_metadata["fps"] != float(output["fps"]):
            raise ValueError("输出视频帧率不符合合同")
        if abs(output_metadata["duration_seconds"] - float(output["duration_seconds"])) > 0.001:
            raise ValueError("输出视频时长不符合合同")

        mapping = write_adjusted_frames_and_mapping(
            evidence_dir, source_frames, adjusted_frames, adjustments
        )
        write_json(evidence_dir / "frame_mapping.json", mapping)
        review_artifacts = contract["review_artifacts"]
        contact_sheet_path = evidence_dir / _simple_filename(
            review_artifacts["before_after_contact_sheet_filename"],
            "review_artifacts.before_after_contact_sheet_filename",
        )
        write_before_after_contact_sheet(
            contact_sheet_path,
            source_frames,
            adjusted_frames,
            int(review_artifacts["contact_sheet_columns"]),
            int(review_artifacts["thumbnail_width_pixels"]),
        )
        parameter_observation = adjustment_summary(adjustments)
        review_record = {
            "contract_id": contract["contract_id"],
            "contract_sha256": contract_sha256,
            "shot_id": contract["shot_id"],
            "authority": contract["review"]["authority"],
            "overall_status": contract["review"]["overall_status"],
            "frame_review_status_counts": parameter_observation["review_status_counts"],
            "all_frames_human_approved": parameter_observation["all_frames_human_approved"],
            "formal_ground_truth_created": False,
            "formal_visual_quality_acceptance_created": False,
            "selection_decision_created": False,
            "timeline_binding_created": False,
            "recorded_at": utc_now(),
        }
        write_json(evidence_dir / "review_record.json", review_record)
        write_json(
            evidence_dir / "adjustment_summary.json",
            {
                "source_metadata": source_metadata,
                "output_metadata": output_metadata,
                "parameter_observation": parameter_observation,
                "pixel_identical_before_encoding_by_frame": [
                    bool(np.array_equal(source_frame, adjusted_frame))
                    for source_frame, adjusted_frame in zip(
                        source_frames, adjusted_frames, strict=True
                    )
                ],
            },
        )
        summary.update(
            {
                "observation": "OBSERVED_OUTPUT_AVAILABLE",
                "output_export_completed": True,
                "output_filename": output["filename"],
                "output_sha256": sha256_file(output_path),
                "output_bytes": output_path.stat().st_size,
                "source_metadata": source_metadata,
                "output_metadata": output_metadata,
                "parameter_observation": parameter_observation,
                "before_after_contact_sheet_filename": contact_sheet_path.name,
                "before_after_contact_sheet_sha256": sha256_file(contact_sheet_path),
                "frame_mapping_filename": "frame_mapping.json",
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
