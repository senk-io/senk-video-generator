from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import imageio.v2 as imageio
import numpy as np

from tools.derive_cogvideox_shot_direction import (
    derive_direction_frames,
    derive_spatial_only_frames,
    direction_observation,
    threshold_comparisons,
    validate_contract,
    validate_unbound_five_second_direction_design,
    write_review_frames,
)


class CogVideoXDirectionDerivationTest(unittest.TestCase):
    def test_fixed_contract_is_fail_closed(self) -> None:
        contract_path = Path(
            "experiments/postprocessing/cogvideox_shot_002_rightward_direction_v1.json"
        )
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        validate_contract(contract)
        mutated = json.loads(json.dumps(contract))
        mutated["trajectory"]["target_horizontal_displacement_pixels"] = 16
        with self.assertRaisesRegex(ValueError, "固定合同"):
            validate_contract(mutated)

    def test_direction_derivation_creates_bounded_rightward_path(self) -> None:
        frames = np.full((9, 48, 96, 3), 230, dtype=np.uint8)
        for index, x in enumerate((32, 36, 31, 37, 29, 33, 28, 31, 27)):
            frames[index, 18:34, x : x + 24] = (230, 20, 20)
        measurement = {
            "red_minimum": 150,
            "red_to_green_ratio_numerator": 3,
            "red_to_green_ratio_denominator": 2,
            "red_to_blue_ratio_numerator": 3,
            "red_to_blue_ratio_denominator": 2,
            "minimum_subject_area_pixels": 100,
        }
        source = direction_observation(frames, measurement)
        derived, shifts, targets = derive_direction_frames(
            frames,
            source,
            {
                "target_horizontal_displacement_pixels": 32,
                "maximum_translation_pixels": 64,
            },
            {"weights": [1, 4, 1]},
        )
        observed = direction_observation(derived, measurement)
        comparisons = threshold_comparisons(
            observed,
            {
                "all_frames_retain_subject": True,
                "minimum_net_horizontal_displacement_pixels": 24.0,
                "minimum_adjacent_horizontal_displacement_pixels": 0.5,
                "maximum_adjacent_centroid_jump_pixels": 5.5,
                "maximum_mean_adjacent_centroid_jump_pixels": 4.5,
                "maximum_adjacent_subject_area_change_percent": 13.0,
            },
        )
        self.assertEqual(len(shifts), 9)
        self.assertEqual(len(targets), 9)
        self.assertTrue(observed["all_frames_retain_subject"])
        self.assertTrue(all(item["within_threshold"] for item in comparisons.values()))

    def test_spatial_only_contract_and_direction_path_are_fail_closed(self) -> None:
        contract_path = Path(
            "experiments/postprocessing/cogvideox_shot_002_rightward_spatial_only_v2.json"
        )
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        validate_contract(contract)
        mutated = json.loads(json.dumps(contract))
        mutated["frame_processing"]["temporal_mix"] = "SYMMETRIC_THREE_FRAME_WEIGHTED_MIX"
        with self.assertRaisesRegex(ValueError, "固定合同"):
            validate_contract(mutated)

        frames = np.full((9, 48, 96, 3), 230, dtype=np.uint8)
        for index, x in enumerate((32, 36, 31, 37, 29, 33, 28, 31, 27)):
            frames[index, 18:34, x : x + 24] = (230, 20, 20)
        measurement = {
            "red_minimum": 150,
            "red_to_green_ratio_numerator": 3,
            "red_to_green_ratio_denominator": 2,
            "red_to_blue_ratio_numerator": 3,
            "red_to_blue_ratio_denominator": 2,
            "minimum_subject_area_pixels": 100,
        }
        source = direction_observation(frames, measurement)
        derived, shifts, targets = derive_spatial_only_frames(
            frames,
            source,
            {
                "target_horizontal_displacement_pixels": 32,
                "maximum_translation_pixels": 64,
            },
        )
        observed = direction_observation(derived, measurement)
        comparisons = threshold_comparisons(
            observed,
            contract["observation_thresholds"],
        )
        self.assertEqual(len(shifts), 9)
        self.assertEqual(len(targets), 9)
        self.assertTrue(np.array_equal(frames[0], derived[0]))
        self.assertTrue(all(item["within_threshold"] for item in comparisons.values()))

        reduced_speed_contract_path = Path(
            "experiments/postprocessing/cogvideox_shot_002_rightward_spatial_only_24px_v3.json"
        )
        reduced_speed_contract = json.loads(
            reduced_speed_contract_path.read_text(encoding="utf-8")
        )
        validate_contract(reduced_speed_contract)
        self.assertEqual(
            reduced_speed_contract["trajectory"]["target_horizontal_displacement_pixels"],
            24,
        )
        self.assertEqual(
            reduced_speed_contract["observation_thresholds"],
            contract["observation_thresholds"],
        )
        mutated_reduced_speed = json.loads(json.dumps(reduced_speed_contract))
        mutated_reduced_speed["observation_thresholds"]["maximum_adjacent_centroid_jump_pixels"] = 6.2
        with self.assertRaisesRegex(ValueError, "固定合同"):
            validate_contract(mutated_reduced_speed)

    def test_five_second_direction_design_remains_unbound_and_non_executable(self) -> None:
        design_path = Path(
            "experiments/postprocessing/cogvideox_shot_002_five_second_direction_design_v1.json"
        )
        design = json.loads(design_path.read_text(encoding="utf-8"))
        validate_unbound_five_second_direction_design(design)
        self.assertEqual(design["design_status"], "UNBOUND_SOURCE_NOT_EXECUTABLE")
        self.assertEqual(
            design["trajectory_design"]["target_horizontal_displacement_pixels"],
            117,
        )
        mutated = json.loads(json.dumps(design))
        mutated["source_binding"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "固定设计"):
            validate_unbound_five_second_direction_design(mutated)

        bound_contract_path = Path(
            "experiments/postprocessing/cogvideox_shot_002_five_second_rightward_bound_v1.json"
        )
        bound_contract = json.loads(bound_contract_path.read_text(encoding="utf-8"))
        validate_contract(bound_contract)
        self.assertEqual(
            bound_contract["source"]["sha256"],
            "06efd281e3fca0037f4c0aafb94f8683e255563681c55d5377e05a0391643825",
        )
        self.assertEqual(bound_contract["output"]["decoded_frame_count"], 40)
        mutated_bound = json.loads(json.dumps(bound_contract))
        mutated_bound["source"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "固定合同"):
            validate_contract(mutated_bound)

    def test_forty_frame_review_artifacts_use_contract_layout(self) -> None:
        frames = np.zeros((40, 8, 12, 3), dtype=np.uint8)
        with tempfile.TemporaryDirectory() as directory:
            evidence_dir = Path(directory)
            filename, digest = write_review_frames(
                evidence_dir,
                frames,
                {
                    "frames_directory": "frames",
                    "contact_sheet_filename": "contact_sheet_40_frames.png",
                    "contact_sheet_columns": 5,
                },
            )
            self.assertEqual(filename, "contact_sheet_40_frames.png")
            self.assertEqual(len(list((evidence_dir / "frames").glob("frame_*.png"))), 40)
            self.assertEqual(len(digest), 64)
            contact_sheet = np.asarray(imageio.imread(evidence_dir / filename))
            self.assertEqual(contact_sheet.shape[:2], (100, 84))


if __name__ == "__main__":
    unittest.main()
