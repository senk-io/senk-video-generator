from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from shot_planning.prompting import build_local_planner_hybrid_stage_prompt
from shot_planning.source_facts import (
    extract_source_facts,
    merge_hybrid_stage_payload,
    source_fact_extractor_contract,
)


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_ROOT = ROOT / "experiments" / "shot_planning"
REQUEST_FILES = {
    "crying": "generalized_child_crying_closeup_request_v1.json",
    "smile": "generalized_actor_smile_medium_request_v1.json",
    "bicycle": "generalized_bicycle_left_to_right_wide_request_v1.json",
}


def load_request(case_name: str) -> dict:
    return json.loads(
        (EXPERIMENT_ROOT / REQUEST_FILES[case_name]).read_text(encoding="utf-8")
    )


def with_source(request: dict, source_text: str) -> dict:
    mutated = deepcopy(request)
    mutated["source_text"] = source_text
    return mutated


class SourceFactExtractionTest(unittest.TestCase):
    def test_existing_cases_lock_only_direct_or_deterministic_fields(self) -> None:
        expected = {
            "crying": {
                "count": 9,
                "values": {
                    "scene_context.location": "OUTDOOR_LOCATION",
                    "scene_context.time": "DAY",
                    "shot_core.framing": "CLOSE_UP",
                    "shot_core.camera_movement": "STATIC",
                    "shot_core.camera_direction": "NONE",
                    "shot_core.camera_speed": "NONE",
                    "shot_core.action_class": "EXPRESS",
                    "performance.visible_action_state": "CRYING",
                },
            },
            "smile": {
                "count": 11,
                "values": {
                    "scene_context.location": "INDOOR_LOCATION",
                    "scene_context.time": "DAY",
                    "shot_core.framing": "MEDIUM",
                    "shot_core.camera_movement": "STATIC",
                    "shot_core.camera_direction": "NONE",
                    "shot_core.camera_speed": "NONE",
                    "shot_core.action_class": "EXPRESS",
                    "performance.orientation_state": "FACING_CAMERA",
                    "performance.visible_action_state": "SMILING",
                    "performance.performance_intensity": "GENTLE",
                },
            },
            "bicycle": {
                "count": 9,
                "values": {
                    "scene_context.location": "OUTDOOR_LOCATION",
                    "scene_context.time": "NIGHT",
                    "shot_core.framing": "WIDE",
                    "shot_core.camera_movement": "STATIC",
                    "shot_core.camera_direction": "NONE",
                    "shot_core.camera_speed": "NONE",
                    "shot_core.action_class": "MOVE",
                    "performance.orientation_state": "MOVING_LEFT_TO_RIGHT",
                },
            },
        }
        for case_name, expectation in expected.items():
            request = load_request(case_name)
            extraction = extract_source_facts(request)
            self.assertEqual(extraction["blocking_issue_count"], 0)
            self.assertEqual(len(extraction["locked_fields"]), expectation["count"])
            self.assertEqual(
                extraction["locked_fields"]["shot_core.action_description"],
                request["source_text"],
            )
            for field, value in expectation["values"].items():
                self.assertEqual(extraction["locked_fields"].get(field), value)
            self.assertFalse(
                any(
                    field.startswith(("composition.", "lighting.", "continuity."))
                    for field in extraction["locked_fields"]
                )
            )
            self.assertFalse(extraction["held_out_observation_used"])
            self.assertFalse(extraction["formal_decision_created"])

    def test_negation_compounds_quotes_and_camera_motion_are_not_mislocked(self) -> None:
        base = load_request("smile")
        cases = (
            ("演员并没有微笑", {"performance.visible_action_state", "shot_core.action_class"}),
            ("一只白天鹅游过湖面", {"scene_context.time"}),
            (
                "相机缓慢从左向右移动",
                {"performance.orientation_state", "shot_core.action_class"},
            ),
        )
        for source_text, forbidden_fields in cases:
            extraction = extract_source_facts(with_source(base, source_text))
            self.assertTrue(
                forbidden_fields.isdisjoint(extraction["locked_fields"]),
                source_text,
            )

        negative_pan = extract_source_facts(
            with_source(base, "相机不要向右摇摄，固定相机拍摄演员")
        )
        self.assertEqual(negative_pan["blocking_issue_count"], 0)
        self.assertEqual(
            negative_pan["locked_fields"].get("shot_core.camera_movement"),
            "STATIC",
        )
        self.assertEqual(
            negative_pan["locked_fields"].get("shot_core.camera_direction"),
            "NONE",
        )

        negative_closeup = extract_source_facts(
            with_source(base, "不要使用特写，改用中景镜头")
        )
        self.assertEqual(
            negative_closeup["locked_fields"].get("shot_core.framing"), "MEDIUM"
        )

        compound_location = extract_source_facts(
            with_source(base, "室内设计师在室外，演员微笑")
        )
        self.assertEqual(compound_location["blocking_issue_count"], 0)
        self.assertEqual(
            compound_location["locked_fields"].get("scene_context.location"),
            "OUTDOOR_LOCATION",
        )

        quoted_closeup = extract_source_facts(
            with_source(base, "文案写“特写镜头”，实际使用中景镜头")
        )
        self.assertEqual(quoted_closeup["blocking_issue_count"], 0)
        self.assertEqual(
            quoted_closeup["locked_fields"].get("shot_core.framing"), "MEDIUM"
        )

    def test_ambiguity_and_conflict_fail_closed_without_a_winner(self) -> None:
        base = load_request("smile")
        ambiguous = extract_source_facts(
            with_source(base, "白天或夜晚室外，演员微笑")
        )
        self.assertEqual(ambiguous["blocking_issue_count"], 1)
        self.assertEqual(
            ambiguous["clarification_required_fields"], ["scene_context.time"]
        )
        self.assertNotIn("scene_context.time", ambiguous["locked_fields"])
        self.assertEqual(ambiguous["issues"][0]["state"], "AMBIGUOUS")

        conflict = extract_source_facts(
            with_source(base, "固定相机，相机向右摇摄")
        )
        self.assertGreater(conflict["blocking_issue_count"], 0)
        self.assertIn(
            "shot_core.camera_movement", conflict["clarification_required_fields"]
        )
        self.assertNotIn("shot_core.camera_movement", conflict["locked_fields"])

    def test_derivation_requires_a_validated_base_fact(self) -> None:
        request = load_request("smile")
        request["controlled_stage_allowed_values"]["performance"][
            "visible_action_state"
        ] = ["CRYING"]
        extraction = extract_source_facts(request)
        self.assertIn(
            "performance.visible_action_state",
            extraction["clarification_required_fields"],
        )
        self.assertNotIn("performance.visible_action_state", extraction["locked_fields"])
        self.assertNotIn("shot_core.action_class", extraction["locked_fields"])
        fact_ids = {fact["fact_id"] for fact in extraction["facts"]}
        for fact in extraction["facts"]:
            self.assertTrue(set(fact["depends_on_fact_ids"]).issubset(fact_ids))

    def test_allowed_candidate_order_does_not_change_facts_or_ownership(self) -> None:
        request = load_request("smile")
        reordered = deepcopy(request)
        for values in reordered["semantic_constraints"].values():
            if isinstance(values, list):
                values.reverse()
        for values in reordered["controlled_context_token_values"][
            "scene_context"
        ].values():
            values.reverse()
        for fields in reordered["controlled_stage_allowed_values"].values():
            for values in fields.values():
                values.reverse()
        original = extract_source_facts(request)
        changed = extract_source_facts(reordered)
        self.assertEqual(original["facts"], changed["facts"])
        self.assertEqual(original["locked_fields"], changed["locked_fields"])
        self.assertEqual(original["field_resolutions"], changed["field_resolutions"])

    def test_hybrid_prompt_exposes_only_residual_field_metadata(self) -> None:
        request = load_request("smile")
        prompt = build_local_planner_hybrid_stage_prompt(request, "shot_core")
        body = json.loads(prompt["user"])
        stage_contract = body["stage_contract"]
        self.assertEqual(stage_contract["required_keys"], ["primary_purpose"])
        self.assertEqual(
            set(stage_contract["allowed_scalar_choices"]), {"primary_purpose"}
        )
        self.assertEqual(set(stage_contract["choice_glossary"]), {"primary_purpose"})
        self.assertNotIn("required_action_terms", stage_contract)
        self.assertNotIn("explicit_semantic_constraints", body["input"])
        self.assertNotIn("allowed_framings", prompt["user"])
        self.assertNotIn("expected_controlled_values", prompt["user"])
        self.assertFalse(body["input"]["held_out_observation_used"])

    def test_merge_blocks_model_writes_to_locked_fields(self) -> None:
        extraction = extract_source_facts(load_request("smile"))
        residual = {"primary_purpose": "EMPHASIZE_EMOTION"}
        merged, observations, document = merge_hybrid_stage_payload(
            "shot_core", residual, extraction
        )
        self.assertEqual(observations, [])
        self.assertEqual(merged["framing"], "MEDIUM")
        self.assertEqual(merged["primary_purpose"], "EMPHASIZE_EMOTION")
        self.assertFalse(document["automatic_repair_attempted"])

        injected = {**residual, "framing": "CLOSE_UP"}
        merged, observations, document = merge_hybrid_stage_payload(
            "shot_core", injected, extraction
        )
        self.assertEqual(merged["framing"], "MEDIUM")
        self.assertIn(
            "MODEL_WROTE_LOCKED_FIELD", {item["code"] for item in observations}
        )
        self.assertFalse(document["automatic_repair_attempted"])

    def test_extractor_contract_declares_matching_and_resolution_semantics(self) -> None:
        contract = source_fact_extractor_contract()
        self.assertEqual(
            contract["matching_policy"]["negation_scope"],
            "CLAUSE_START_THROUGH_MATCH_END_CONSERVATIVE",
        )
        self.assertEqual(
            contract["matching_policy"]["quoted_match_behavior"],
            "IGNORE_MATCH_INSIDE_BALANCED_QUOTES",
        )
        self.assertEqual(
            contract["derivation_dependency_requirement"],
            "SELECTED_VALID_BASE_FACT",
        )
        self.assertEqual(
            contract["request_passthrough_rules"][0]["field"],
            "shot_core.action_description",
        )


if __name__ == "__main__":
    unittest.main()
