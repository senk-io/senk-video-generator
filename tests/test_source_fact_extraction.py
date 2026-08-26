from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from shot_planning.prompting import build_local_planner_hybrid_stage_prompt
from shot_planning.source_facts import (
    SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V1,
    SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
    extract_source_facts,
    merge_hybrid_stage_payload,
    source_fact_extractor_contract,
    source_fact_extractor_contract_sha256,
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

    def test_v2_rejects_additional_negations_and_camera_subject_crossovers(self) -> None:
        base = load_request("smile")
        negative_cases = (
            (
                "演员从未微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员未微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员不曾微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员没微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员不要再微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员不想微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员不愿继续微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员拒绝微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员停止微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员不要转为微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "不让演员微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "不许演员微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "不允许演员微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员不应微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员不露出微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员不需要微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "莫要微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员并非微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            ("别用特写镜头", {"shot_core.framing"}),
            ("不要再用特写镜头", {"shot_core.framing"}),
            ("不要改用特写镜头", {"shot_core.framing"}),
            ("并非特写镜头", {"shot_core.framing"}),
            ("不允许使用特写镜头", {"shot_core.framing"}),
            ("不应使用特写镜头", {"shot_core.framing"}),
            ("特写镜头禁止使用", {"shot_core.framing"}),
            ("无需特写镜头", {"shot_core.framing"}),
            ("无须使用特写镜头", {"shot_core.framing"}),
            (
                "勿让相机向右摇摄",
                {"shot_core.camera_movement", "shot_core.camera_direction"},
            ),
            (
                "相机不要向右摇摄",
                {"shot_core.camera_movement", "shot_core.camera_direction"},
            ),
            (
                "相机没有向右摇摄",
                {"shot_core.camera_movement", "shot_core.camera_direction"},
            ),
            (
                "相机没有保持静止",
                {
                    "shot_core.camera_movement",
                    "shot_core.camera_direction",
                    "shot_core.camera_speed",
                },
            ),
            (
                "不要为了画面节奏而改用特写镜头",
                {"shot_core.framing"},
            ),
            (
                "演员不要为了讨好观众而转为微笑",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "不应为了画面节奏而改用特写镜头",
                {"shot_core.framing"},
            ),
            (
                "没必要为了画面节奏而改用特写镜头",
                {"shot_core.framing"},
            ),
            (
                "摄影机不要向右摇摄",
                {"shot_core.camera_movement", "shot_core.camera_direction"},
            ),
            (
                "不要让摄影机向右摇摄",
                {"shot_core.camera_movement", "shot_core.camera_direction"},
            ),
            (
                "不要面向摄影机",
                {"performance.orientation_state"},
            ),
            (
                "相机向右摇摄禁止使用",
                {"shot_core.camera_movement", "shot_core.camera_direction"},
            ),
            (
                "不要使用“特写镜头”",
                {"shot_core.framing"},
            ),
            (
                "演员不要“微笑”",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员不要微笑着面对镜头",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "演员从未哭泣过",
                {"performance.visible_action_state", "shot_core.action_class"},
            ),
            (
                "不要使用特写构图",
                {"shot_core.framing"},
            ),
            (
                "并非中景构图",
                {"shot_core.framing"},
            ),
        )
        for source_text, forbidden_fields in negative_cases:
            extraction = extract_source_facts(
                with_source(base, source_text),
                contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
            )
            self.assertTrue(
                forbidden_fields.isdisjoint(extraction["locked_fields"]),
                source_text,
            )
            self.assertGreater(extraction["blocking_issue_count"], 0, source_text)
            self.assertTrue(
                {
                    "NEGATED",
                    "UNRESOLVED",
                }
                & {item["polarity"] for item in extraction["match_decisions"]},
                source_text,
            )

        boundary_cases = (
            (
                "演员身后的相机从左向右移动",
                {"performance.orientation_state", "shot_core.action_class"},
            ),
            (
                "演员身后的摄影机从左向右移动",
                {"performance.orientation_state", "shot_core.action_class"},
            ),
            (
                "固定相机参数后，演员微笑",
                {
                    "shot_core.camera_movement",
                    "shot_core.camera_direction",
                    "shot_core.camera_speed",
                },
            ),
        )
        for source_text, forbidden_fields in boundary_cases:
            extraction = extract_source_facts(
                with_source(base, source_text),
                contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
            )
            self.assertTrue(
                forbidden_fields.isdisjoint(extraction["locked_fields"]),
                source_text,
            )
            self.assertEqual(extraction["blocking_issue_count"], 0, source_text)

        quoted_direction = extract_source_facts(
            with_source(
                load_request("bicycle"),
                "文案写“自行车从左向右行驶”，实际方向未说明",
            ),
            contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
        )
        self.assertNotIn(
            "performance.orientation_state", quoted_direction["locked_fields"]
        )
        self.assertIn(
            "IGNORED_QUOTED",
            {item["polarity"] for item in quoted_direction["match_decisions"]},
        )

        for source_text in (
            "非常自然地微笑",
            "莫妮卡微笑",
            "无锡演员微笑",
            "不但微笑",
            "演员不禁微笑",
            "演员不由自主地微笑",
            "演员忍不住微笑",
            "演员不得不微笑",
            "演员情不自禁地微笑",
            "演员不由得微笑",
            "演员没忍住微笑",
            "演员不能不微笑",
            "演员从未停止微笑",
            "演员不得已微笑",
            "未婚演员微笑",
            "未来演员微笑",
            "没有哭泣而是微笑",
            "没有哭泣反而微笑",
        ):
            extraction = extract_source_facts(
                with_source(base, source_text),
                contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
            )
            self.assertEqual(
                extraction["locked_fields"].get(
                    "performance.visible_action_state"
                ),
                "SMILING",
                source_text,
            )
            self.assertEqual(extraction["blocking_issue_count"], 0, source_text)

        for source_text in (
            "不要特写而改用中景镜头",
            "不要特写改用中景镜头",
            "不要使用特写，改用中景镜头",
            "非特写镜头而是中景镜头",
        ):
            corrected_framing = extract_source_facts(
                with_source(base, source_text),
                contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
            )
            self.assertEqual(
                corrected_framing["locked_fields"].get("shot_core.framing"),
                "MEDIUM",
                source_text,
            )
            self.assertEqual(
                corrected_framing["blocking_issue_count"], 0, source_text
            )

        for source_text in (
            "演员不由得不微笑",
            "并非不能不微笑",
            "演员从未真正停止微笑",
        ):
            unresolved = extract_source_facts(
                with_source(base, source_text),
                contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
            )
            self.assertGreater(unresolved["blocking_issue_count"], 0, source_text)
            self.assertNotIn(
                "performance.visible_action_state",
                unresolved["locked_fields"],
                source_text,
            )

        for source_text, field in (
            ("不要特写改用特写镜头", "shot_core.framing"),
            ("没有微笑反而微笑", "performance.visible_action_state"),
            ("并非白天而是白天", "scene_context.time"),
        ):
            contradiction = extract_source_facts(
                with_source(base, source_text),
                contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
            )
            self.assertGreater(
                contradiction["blocking_issue_count"], 0, source_text
            )
            self.assertNotIn(field, contradiction["locked_fields"], source_text)
            self.assertIn(
                "SOURCE_FACT_POLARITY_CONFLICT",
                {item["code"] for item in contradiction["issues"]},
                source_text,
            )

        for source_text in (
            "演员“并非微笑",
            "“不要特写镜头",
        ):
            unclosed_quote = extract_source_facts(
                with_source(base, source_text),
                contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
            )
            self.assertGreater(
                unclosed_quote["blocking_issue_count"], 0, source_text
            )
            self.assertIn(
                "UNRESOLVED",
                {item["polarity"] for item in unclosed_quote["match_decisions"]},
                source_text,
            )

        moving_request = load_request("bicycle")
        negated_subject_motion = extract_source_facts(
            with_source(moving_request, "自行车没有从左向右行驶"),
            contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
        )
        self.assertTrue(
            {
                "performance.orientation_state",
                "shot_core.action_class",
            }.isdisjoint(negated_subject_motion["locked_fields"])
        )
        self.assertGreater(negated_subject_motion["blocking_issue_count"], 0)

        non_direction = extract_source_facts(
            with_source(moving_request, "自行车并非从左向右行驶"),
            contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
        )
        self.assertGreater(non_direction["blocking_issue_count"], 0)
        self.assertNotIn(
            "performance.orientation_state", non_direction["locked_fields"]
        )

        subject_motion = extract_source_facts(
            with_source(moving_request, "自行车沿街道从左向右行驶"),
            contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
        )
        self.assertEqual(
            subject_motion["locked_fields"].get(
                "performance.orientation_state"
            ),
            "MOVING_LEFT_TO_RIGHT",
        )

    def test_v1_contract_remains_frozen_for_historical_v11_evidence(self) -> None:
        self.assertEqual(
            source_fact_extractor_contract_sha256(
                SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V1
            ),
            "e7e80ae9c924c933e0b95c6ee14b0c93f53c969bde6e218826ed8242261ea0f1",
        )
        self.assertEqual(
            source_fact_extractor_contract()["schema_version"],
            SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V1,
        )
        self.assertEqual(
            source_fact_extractor_contract(
                SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2
            )["schema_version"],
            SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
        )
        v2_policy = source_fact_extractor_contract(
            SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2
        )["matching_policy"]["polarity_policy"]
        self.assertEqual(
            v2_policy["negative_without_asserted_replacement"], "BLOCK"
        )
        self.assertFalse(v2_policy["last_mention_wins"])
        self.assertIn("拒绝", source_fact_extractor_contract(
            SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2
        )["matching_policy"]["negation_markers"])
        self.assertIn("停止", source_fact_extractor_contract(
            SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2
        )["matching_policy"]["negation_markers"])

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
        original_v2 = extract_source_facts(
            request,
            contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
        )
        changed_v2 = extract_source_facts(
            reordered,
            contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
        )
        self.assertEqual(original_v2["facts"], changed_v2["facts"])
        self.assertEqual(
            original_v2["match_decisions"], changed_v2["match_decisions"]
        )

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
