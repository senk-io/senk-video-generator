from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np

from tools.render_keyframe_adjustments import (
    expand_keyframes,
    interpolation_observation,
    monotone_cubic_interpolate,
    validate_contract,
)


CONTRACT_PATH = Path(
    "experiments/postprocessing/cogvideox_shot_002_keyframe_adjustment_v2.json"
)


class KeyframeAdjustmentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def test_contract_uses_five_fixed_keyframes_and_no_model_runs(self) -> None:
        validate_contract(self.contract)
        self.assertEqual(
            [item["frame_number"] for item in self.contract["keyframes"]],
            [1, 10, 20, 30, 40],
        )
        self.assertEqual(self.contract["policy_context"]["maximum_model_runs"], 0)
        self.assertEqual(self.contract["manual_overrides"], [])

    def test_identity_keyframes_expand_to_forty_reviewable_frames(self) -> None:
        expanded = expand_keyframes(self.contract)
        self.assertEqual(len(expanded), 40)
        self.assertEqual(
            [item["parameter_source"] for item in expanded].count("EXPLICIT_KEYFRAME"),
            5,
        )
        self.assertEqual(
            [item["parameter_source"] for item in expanded].count(
                "INTERPOLATED_MONOTONE_CUBIC"
            ),
            35,
        )
        self.assertTrue(all(item["x_pixels"] == 0 for item in expanded))
        self.assertTrue(all(item["y_pixels"] == 0 for item in expanded))
        self.assertTrue(all(item["scale"] == 1 for item in expanded))
        self.assertTrue(all(item["rotation_degrees"] == 0 for item in expanded))
        observation = interpolation_observation(self.contract, expanded)
        self.assertFalse(observation["cross_frame_pixel_mixing"])
        self.assertFalse(observation["segment_overshoot_observed"])

    def test_monotone_cubic_interpolation_preserves_keyframes_without_overshoot(self) -> None:
        keyframe_numbers = np.asarray([1, 10, 20, 30, 40], dtype=float)
        keyframe_values = np.asarray([0, 12, 24, 12, 18], dtype=float)
        frame_numbers = np.arange(1, 41, dtype=float)
        values = monotone_cubic_interpolate(
            keyframe_numbers, keyframe_values, frame_numbers
        )
        for number, value in zip(keyframe_numbers.astype(int), keyframe_values, strict=True):
            self.assertAlmostEqual(values[number - 1], value)
        for start, end in zip(
            keyframe_numbers.astype(int)[:-1],
            keyframe_numbers.astype(int)[1:],
            strict=True,
        ):
            segment = values[start - 1 : end]
            low = min(values[start - 1], values[end - 1])
            high = max(values[start - 1], values[end - 1])
            self.assertGreaterEqual(float(segment.min()), low - 1e-9)
            self.assertLessEqual(float(segment.max()), high + 1e-9)

    def test_changed_keyframes_expand_and_preserve_exact_values(self) -> None:
        changed = json.loads(json.dumps(self.contract))
        x_values = [0, 12, 24, 12, 18]
        scale_values = [1.0, 1.02, 1.04, 1.01, 1.0]
        for keyframe, x_pixels, scale in zip(
            changed["keyframes"], x_values, scale_values, strict=True
        ):
            keyframe["x_pixels"] = x_pixels
            keyframe["scale"] = scale
            keyframe["adjustment_reason"] = "测试关键帧轨迹"
        expanded = expand_keyframes(changed)
        for number, x_pixels, scale in zip(
            [1, 10, 20, 30, 40], x_values, scale_values, strict=True
        ):
            self.assertEqual(expanded[number - 1]["x_pixels"], x_pixels)
            self.assertEqual(expanded[number - 1]["scale"], scale)
        self.assertGreater(expanded[4]["x_pixels"], 0)
        self.assertLess(expanded[4]["x_pixels"], 12)

    def test_manual_override_wins_after_interpolation(self) -> None:
        overridden = json.loads(json.dumps(self.contract))
        overridden["keyframes"][1]["x_pixels"] = 12
        overridden["keyframes"][1]["adjustment_reason"] = "测试关键帧"
        overridden["manual_overrides"] = [
            {
                "frame_number": 5,
                "x_pixels": -7,
                "y_pixels": 2,
                "scale": 1.01,
                "rotation_degrees": 0.5,
                "review_status": "ADJUSTED_PENDING_REVIEW",
                "adjustment_reason": "覆盖异常帧"
            }
        ]
        expanded = expand_keyframes(overridden)
        frame = expanded[4]
        self.assertEqual(frame["x_pixels"], -7)
        self.assertEqual(frame["y_pixels"], 2)
        self.assertEqual(frame["parameter_source"], "EXPLICIT_MANUAL_OVERRIDE")
        self.assertIsNone(frame["interpolation_keyframes"])

    def test_contract_fails_closed_on_keyframe_and_override_mutation(self) -> None:
        moved_keyframe = json.loads(json.dumps(self.contract))
        moved_keyframe["keyframes"][1]["frame_number"] = 11
        with self.assertRaisesRegex(ValueError, "第 1、10、20、30、40 帧"):
            validate_contract(moved_keyframe)

        unbounded = json.loads(json.dumps(self.contract))
        unbounded["keyframes"][0]["scale"] = 1.2
        with self.assertRaisesRegex(ValueError, "缩放超过合同边界"):
            validate_contract(unbounded)

        rebound = json.loads(json.dumps(self.contract))
        rebound["source"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "固定 Shot 002 候选"):
            validate_contract(rebound)

        duplicate_override = json.loads(json.dumps(self.contract))
        override = {
            "frame_number": 5,
            "x_pixels": 0,
            "y_pixels": 0,
            "scale": 1.0,
            "rotation_degrees": 0.0,
            "review_status": "PENDING_REVIEW",
            "adjustment_reason": "测试覆盖",
        }
        duplicate_override["manual_overrides"] = [override, dict(override)]
        with self.assertRaisesRegex(ValueError, "不得重复"):
            validate_contract(duplicate_override)

        keyframe_override = json.loads(json.dumps(self.contract))
        keyframe_override["manual_overrides"] = [{**override, "frame_number": 10}]
        with self.assertRaisesRegex(ValueError, "关键帧必须直接修改"):
            validate_contract(keyframe_override)


if __name__ == "__main__":
    unittest.main()
