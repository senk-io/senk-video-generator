from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import imageio.v2 as imageio
import numpy as np

from tools.render_manual_frame_adjustments import (
    adjustment_summary,
    apply_adjustments,
    transform_frame,
    validate_contract,
    write_adjusted_frames_and_mapping,
    write_before_after_contact_sheet,
)


CONTRACT_PATH = Path(
    "experiments/postprocessing/cogvideox_shot_002_manual_frame_adjustment_v1.json"
)


class ManualFrameAdjustmentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def test_draft_contract_explicitly_maps_all_forty_pending_frames(self) -> None:
        validate_contract(self.contract)
        self.assertEqual(len(self.contract["frames"]), 40)
        self.assertEqual(
            [frame["frame_number"] for frame in self.contract["frames"]],
            list(range(1, 41)),
        )
        self.assertEqual(
            {frame["review_status"] for frame in self.contract["frames"]},
            {"PENDING_REVIEW"},
        )
        summary = adjustment_summary(self.contract["frames"])
        self.assertEqual(summary["identity_frame_count"], 40)
        self.assertEqual(summary["changed_frame_count"], 0)
        self.assertFalse(summary["all_frames_human_approved"])

    def test_contract_rejects_implicit_or_unbounded_adjustments(self) -> None:
        missing_frame = json.loads(json.dumps(self.contract))
        missing_frame["frames"].pop()
        with self.assertRaisesRegex(ValueError, "显式包含 40 帧"):
            validate_contract(missing_frame)

        duplicate_frame = json.loads(json.dumps(self.contract))
        duplicate_frame["frames"][1]["frame_number"] = 1
        with self.assertRaisesRegex(ValueError, "连续且唯一"):
            validate_contract(duplicate_frame)

        unbounded = json.loads(json.dumps(self.contract))
        unbounded["frames"][0]["x_pixels"] = 193
        unbounded["frames"][0]["adjustment_reason"] = "测试越界"
        with self.assertRaisesRegex(ValueError, "超过合同上限"):
            validate_contract(unbounded)

        unexplained = json.loads(json.dumps(self.contract))
        unexplained["frames"][0]["rotation_degrees"] = 1
        with self.assertRaisesRegex(ValueError, "必须填写原因"):
            validate_contract(unexplained)

        local_edit = json.loads(json.dumps(self.contract))
        local_edit["frames"][0]["local_adjustments"] = [{"type": "UNDEFINED"}]
        with self.assertRaisesRegex(ValueError, "局部修正必须为空"):
            validate_contract(local_edit)

        rebound_source = json.loads(json.dumps(self.contract))
        rebound_source["source"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "固定 Shot 002 候选"):
            validate_contract(rebound_source)

        model_run = json.loads(json.dumps(self.contract))
        model_run["policy_context"]["maximum_model_runs"] = 1
        with self.assertRaisesRegex(ValueError, "不得授权模型运行"):
            validate_contract(model_run)

    def test_human_decision_requires_reviewer_and_timestamp(self) -> None:
        approved = json.loads(json.dumps(self.contract))
        approved["frames"][0]["review_status"] = "HUMAN_APPROVED"
        with self.assertRaisesRegex(ValueError, "评审者和时间"):
            validate_contract(approved)
        approved["frames"][0]["reviewer"] = "human-reviewer"
        approved["frames"][0]["reviewed_at"] = "2026-08-10T12:00:00+09:00"
        validate_contract(approved)

    def test_identity_transform_preserves_pixels_before_encoding(self) -> None:
        rng = np.random.default_rng(42)
        frame = rng.integers(0, 256, size=(24, 32, 3), dtype=np.uint8)
        adjustment = self.contract["frames"][0]
        transformed = transform_frame(frame, adjustment, padding=256)
        self.assertTrue(np.array_equal(frame, transformed))

    def test_translation_moves_subject_without_cross_frame_mix(self) -> None:
        frames = np.full((2, 32, 48, 3), 210, dtype=np.uint8)
        frames[0, 12:20, 10:18] = (230, 10, 10)
        frames[1, 12:20, 20:28] = (10, 20, 230)
        adjustments = [
            {
                **self.contract["frames"][0],
                "x_pixels": 5,
                "adjustment_reason": "测试右移",
            },
            self.contract["frames"][1],
        ]
        adjusted = apply_adjustments(frames, adjustments, padding=256)
        red_mask = adjusted[0, :, :, 0] > 220
        red_x = np.where(red_mask)[1]
        self.assertGreaterEqual(int(red_x.min()), 15)
        self.assertTrue(np.array_equal(frames[1], adjusted[1]))

    def test_review_artifacts_include_mapping_and_all_frames(self) -> None:
        frames = np.zeros((2, 12, 16, 3), dtype=np.uint8)
        adjustments = self.contract["frames"][:2]
        with tempfile.TemporaryDirectory() as directory:
            evidence_dir = Path(directory)
            mapping = write_adjusted_frames_and_mapping(
                evidence_dir, frames, frames.copy(), adjustments
            )
            self.assertEqual(len(mapping), 2)
            self.assertEqual(mapping[0]["source_frame"], "frames/frame_001.png")
            self.assertTrue((evidence_dir / "adjusted_frames/frame_002.png").is_file())
            sheet_path = evidence_dir / "before_after.png"
            write_before_after_contact_sheet(
                sheet_path, frames, frames.copy(), columns=2, thumbnail_width=16
            )
            sheet = np.asarray(imageio.imread(sheet_path))
            self.assertGreater(sheet.shape[0], 12)
            self.assertGreater(sheet.shape[1], 64)


if __name__ == "__main__":
    unittest.main()
