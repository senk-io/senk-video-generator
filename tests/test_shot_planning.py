from __future__ import annotations

import json
import unittest
from copy import deepcopy

from shot_planning.contracts import ShotPlanningContractError, canonical_sha256, validate_request
from shot_planning.prompting import build_local_planner_payload_prompt, build_local_planner_prompt
from shot_planning.stability import collect_local_proposals, observe_stability
from shot_planning.structured_observability import STRUCTURED_STAGE_ALLOWED_VALUES
from shot_planning.validation import observe_proposal


def planning_request() -> dict:
    return {
        "schema_version": "shot-planning-request.v1",
        "request_id": "PLAN-CHILD-CRYING-001",
        "status": "DRAFT_NON_AUTHORITATIVE",
        "source_text": "一个外国小孩子在雨中哭泣的特写镜头",
        "target_duration_seconds": 6,
        "duration_tolerance_seconds": 0,
        "shot_count_bounds": {"minimum": 1, "maximum": 4},
        "required_subject_ids": ["SUBJECT-001"],
        "expected_scene_count": 1,
    }


def semantic_planning_request() -> dict:
    request = planning_request()
    request["request_id"] = "PLAN-CHILD-CRYING-002"
    request["semantic_constraints"] = {
        "allowed_action_classes": ["EXPRESS"],
        "allowed_framings": ["CLOSE_UP", "EXTREME_CLOSE_UP"],
        "allowed_primary_purposes": ["EMPHASIZE_EMOTION"],
        "required_environment_terms": ["雨"],
        "required_action_terms": ["哭"],
        "forbidden_placeholder_values": ["none", "yes", "无", "未知", "n/a"],
        "minimum_free_text_characters": 3,
    }
    return request


def planning_proposal(proposal_id: str = "PROPOSAL-001") -> dict:
    request = planning_request()
    source = request["source_text"]
    return {
        "schema_version": "shot-planning-proposal.v1",
        "proposal_id": proposal_id,
        "request_id": request["request_id"],
        "source_text_sha256": canonical_sha256(source),
        "status": "DRAFT_NON_AUTHORITATIVE",
        "planner": {
            "model_id": "local-text-model",
            "model_version": "test-version",
            "prompt_contract_version": "local-shot-planner.v1",
            "run_id": f"RUN-{proposal_id}",
            "sampling": {"temperature": 0.0, "seed": 42},
        },
        "scenes": [
            {
                "scene_id": "SCENE-001",
                "ordinal": 1,
                "location": "雨中的室外",
                "time": "未由原句明确",
                "environment": "下雨",
                "continuity_anchors": ["同一孩子", "持续降雨"],
            }
        ],
        "narrative_beats": [
            {
                "beat_id": "BEAT-001",
                "ordinal": 1,
                "scene_id": "SCENE-001",
                "source_span": {"start": 0, "end": len(source), "quote": source},
                "purpose": "EMPHASIZE_EMOTION",
                "subject_ids": ["SUBJECT-001"],
                "action": "孩子在雨中哭泣",
            }
        ],
        "shots": [
            {
                "shot_id": "SHOT-001",
                "ordinal": 1,
                "scene_id": "SCENE-001",
                "beat_ids": ["BEAT-001"],
                "script_segment": source,
                "primary_purpose": "ESTABLISH_CONTEXT",
                "target_duration_seconds": 1.5,
                "framing": "MEDIUM_CLOSE_UP",
                "subject_ids": ["SUBJECT-001"],
                "action": {"class": "EXPRESS", "description": "孩子开始哭泣"},
                "composition": "孩子居中，雨线可见",
                "camera": {"movement": "STATIC", "direction": "NONE", "speed": "NONE"},
                "emotion": "悲伤表情开始形成",
                "lighting": "阴天柔光",
                "continuity_in": "起始时孩子已在雨中",
                "continuity_out": "保持同一面部与湿发状态",
                "observable_checks": ["画面中只有一个主要孩子", "雨线可见"],
            },
            {
                "shot_id": "SHOT-002",
                "ordinal": 2,
                "scene_id": "SCENE-001",
                "beat_ids": ["BEAT-001"],
                "script_segment": source,
                "primary_purpose": "DEVELOP_ACTION",
                "target_duration_seconds": 2,
                "framing": "CLOSE_UP",
                "subject_ids": ["SUBJECT-001"],
                "action": {"class": "EXPRESS", "description": "孩子持续哭泣"},
                "composition": "面部占据画面主要区域",
                "camera": {"movement": "DOLLY", "direction": "IN", "speed": "SLOW"},
                "emotion": "哭泣强度增加",
                "lighting": "保持阴天柔光",
                "continuity_in": "继承湿发和面部方向",
                "continuity_out": "泪水留在同一侧面颊",
                "observable_checks": ["推进方向为靠近主体", "主体身份不变"],
            },
            {
                "shot_id": "SHOT-003",
                "ordinal": 3,
                "scene_id": "SCENE-001",
                "beat_ids": ["BEAT-001"],
                "script_segment": source,
                "primary_purpose": "EMPHASIZE_EMOTION",
                "target_duration_seconds": 2.5,
                "framing": "EXTREME_CLOSE_UP",
                "subject_ids": ["SUBJECT-001"],
                "action": {"class": "EXPRESS", "description": "泪水沿面颊滑落"},
                "composition": "眼睛与泪水成为视觉中心",
                "camera": {"movement": "STATIC", "direction": "NONE", "speed": "NONE"},
                "emotion": "强烈悲伤",
                "lighting": "保持阴天柔光并保留泪水高光",
                "continuity_in": "继承同一面部方向和泪水位置",
                "continuity_out": "以泪水滑落状态结束",
                "observable_checks": ["泪水沿连续路径滑落", "没有新增人物"],
            },
        ],
    }


class ShotPlanningTest(unittest.TestCase):
    def test_request_requires_non_authoritative_status_and_explicit_bounds(self) -> None:
        validate_request(planning_request())
        mutated = planning_request()
        mutated["status"] = "PLANNED"
        with self.assertRaisesRegex(ShotPlanningContractError, "非权威草案"):
            validate_request(mutated)

        mutated = planning_request()
        mutated["shot_count_bounds"] = {"minimum": 4, "maximum": 2}
        with self.assertRaisesRegex(ShotPlanningContractError, "正整数区间"):
            validate_request(mutated)

    def test_request_validates_controlled_stage_value_subsets(self) -> None:
        request = semantic_planning_request()
        request["controlled_stage_allowed_values"] = {
            stage: {field: [values[0]] for field, values in fields.items()}
            for stage, fields in STRUCTURED_STAGE_ALLOWED_VALUES.items()
            if stage != "shot_core"
        }
        validate_request(request)
        request["controlled_stage_allowed_values"]["composition"][
            "subject_placement"
        ] = ["UNSUPPORTED"]
        with self.assertRaisesRegex(ShotPlanningContractError, "全局词表"):
            validate_request(request)

    def test_complete_proposal_has_no_structural_observations(self) -> None:
        report = observe_proposal(planning_request(), planning_proposal())
        self.assertEqual(report["blocking_observation_count"], 0)
        self.assertEqual(report["observations"], [])
        self.assertFalse(report["formal_decision_created"])
        self.assertTrue(report["creative_review_required"])

    def test_v1_proposal_rejects_generalized_prompt_contract(self) -> None:
        proposal = planning_proposal()
        proposal["planner"]["prompt_contract_version"] = (
            "local-shot-planner-semantic-gloss.v10"
        )
        report = observe_proposal(planning_request(), proposal)
        self.assertIn(
            "PROMPT_CONTRACT_VERSION_MISMATCH",
            {item["code"] for item in report["observations"]},
        )

    def test_binding_coverage_duration_and_subject_differences_are_separate(self) -> None:
        proposal = planning_proposal()
        proposal["source_text_sha256"] = "0" * 64
        proposal["narrative_beats"][0]["source_span"]["end"] = 4
        proposal["narrative_beats"][0]["source_span"]["quote"] = proposal["narrative_beats"][0]["source_span"]["quote"][:4]
        proposal["shots"][2]["target_duration_seconds"] = 1
        for shot in proposal["shots"]:
            shot["subject_ids"] = ["SUBJECT-002"]

        report = observe_proposal(planning_request(), proposal)
        codes = {item["code"] for item in report["observations"]}
        self.assertIn("SOURCE_TEXT_SHA256_MISMATCH", codes)
        self.assertIn("SOURCE_CONTENT_NOT_COVERED", codes)
        self.assertIn("SHOT_DURATION_SUM_MISMATCH", codes)
        self.assertIn("REQUIRED_SUBJECT_NOT_COVERED", codes)

    def test_authority_claim_and_incompatible_static_camera_are_observed(self) -> None:
        proposal = planning_proposal()
        proposal["approved"] = True
        proposal["shots"][0]["camera"] = {
            "movement": "STATIC",
            "direction": "RIGHT",
            "speed": "SLOW",
        }
        report = observe_proposal(planning_request(), proposal)
        codes = {item["code"] for item in report["observations"]}
        self.assertIn("FORMAL_DECISION_FIELD_FORBIDDEN", codes)
        self.assertIn("STATIC_CAMERA_HAS_MOTION", codes)

    def test_camera_direction_must_match_non_static_movement(self) -> None:
        proposal = planning_proposal()
        proposal["shots"][0]["camera"] = {
            "movement": "ZOOM",
            "direction": "LEFT",
            "speed": "FAST",
        }
        report = observe_proposal(planning_request(), proposal)
        self.assertIn(
            "CAMERA_DIRECTION_INCOMPATIBLE_WITH_MOVEMENT",
            {item["code"] for item in report["observations"]},
        )

    def test_stability_observes_exact_and_per_field_consistency(self) -> None:
        first = planning_proposal("PROPOSAL-001")
        second = planning_proposal("PROPOSAL-002")
        third = planning_proposal("PROPOSAL-003")
        third["shots"][1]["framing"] = "MEDIUM_CLOSE_UP"

        report = observe_stability(planning_request(), [first, second, third])
        self.assertEqual(report["run_count"], 3)
        self.assertEqual(report["comparable_run_count"], 3)
        self.assertEqual(report["exact_structure_group_count"], 2)
        self.assertEqual(report["largest_exact_structure_group_ratio"], 0.6667)
        self.assertEqual(
            report["field_consistency"]["shot_count"]["largest_group_ratio"],
            1.0,
        )
        self.assertEqual(
            report["field_consistency"]["shot_framing_sequence"]["largest_group_ratio"],
            0.6667,
        )
        self.assertFalse(report["formal_decision_created"])

    def test_invalid_run_is_retained_but_excluded_from_structure_comparison(self) -> None:
        valid = planning_proposal("PROPOSAL-001")
        invalid = planning_proposal("PROPOSAL-002")
        invalid["shots"][0]["shot_id"] = "BROKEN"
        report = observe_stability(planning_request(), [valid, invalid])
        self.assertEqual(report["run_count"], 2)
        self.assertEqual(report["comparable_run_count"], 1)
        self.assertIn(
            "RUNS_EXCLUDED_FROM_COMPARISON",
            {item["code"] for item in report["run_observations"]},
        )
        self.assertEqual(len(report["proposal_observations"]), 2)

    def test_duplicate_run_identity_cannot_inflate_consistency(self) -> None:
        first = planning_proposal("PROPOSAL-001")
        duplicate = deepcopy(first)
        report = observe_stability(planning_request(), [first, duplicate])
        self.assertEqual(report["run_count"], 2)
        self.assertEqual(report["comparable_run_count"], 1)
        self.assertFalse(report["comparison_performed"])
        self.assertIsNone(report["largest_exact_structure_group_ratio"])
        self.assertEqual(report["field_consistency"], {})
        codes = {item["code"] for item in report["run_observations"]}
        self.assertIn("DUPLICATE_PROPOSAL_IDENTITIES_EXCLUDED", codes)
        self.assertIn("INSUFFICIENT_UNIQUE_COMPARABLE_RUNS", codes)

    def test_different_model_contexts_are_not_combined(self) -> None:
        first = planning_proposal("PROPOSAL-001")
        second = planning_proposal("PROPOSAL-002")
        second["planner"]["model_version"] = "different-version"
        report = observe_stability(planning_request(), [first, second])
        self.assertEqual(report["comparison_context_count"], 2)
        self.assertEqual(report["comparable_run_count"], 0)
        self.assertEqual(report["field_consistency"], {})
        self.assertIn(
            "COMPARISON_CONTEXTS_DIFFER",
            {item["code"] for item in report["run_observations"]},
        )

    def test_prompt_is_bound_to_source_and_requests_json_only(self) -> None:
        prompt = build_local_planner_prompt(planning_request())
        payload = json.loads(prompt["user"])
        self.assertEqual(prompt["prompt_contract_version"], "local-shot-planner.v1")
        self.assertEqual(
            payload["required_output_shape"]["source_text_sha256"],
            canonical_sha256(planning_request()["source_text"]),
        )
        self.assertIn("只输出一个 JSON 对象", prompt["system"])
        self.assertNotIn("MiniMax", prompt["system"] + prompt["user"])

    def test_payload_prompt_moves_governance_envelope_out_of_small_model(self) -> None:
        prompt = build_local_planner_payload_prompt(planning_request())
        payload = json.loads(prompt["user"])
        shape = payload["required_payload_shape"]
        self.assertEqual(prompt["assistant_prefill"], "{")
        self.assertEqual(prompt["prompt_contract_version"], "local-shot-planner-payload.v2")
        self.assertNotIn("proposal_id", shape)
        self.assertNotIn("planner", shape)
        self.assertNotIn("status", shape)

    def test_explicit_semantic_constraints_observe_stable_but_wrong_plan(self) -> None:
        request = semantic_planning_request()
        proposal = planning_proposal()
        proposal["request_id"] = request["request_id"]
        proposal["scenes"][0]["environment"] = "哭泣的特写镜头"
        proposal["shots"] = [proposal["shots"][0]]
        proposal["shots"][0].update(
            {
                "primary_purpose": "ESTABLISH_CONTEXT",
                "target_duration_seconds": 6,
                "framing": "MEDIUM_WIDE",
                "action": {"class": "STATIC", "description": "静止拍摄"},
                "continuity_in": "none",
                "continuity_out": "none",
                "observable_checks": ["yes"],
            }
        )
        report = observe_proposal(request, proposal)
        codes = {item["code"] for item in report["observations"]}
        self.assertIn("REQUIRED_ENVIRONMENT_TERM_MISSING", codes)
        self.assertIn("REQUIRED_SHOT_ACTION_TERM_MISSING", codes)
        self.assertIn("EXPLICIT_FRAMING_MISMATCH", codes)
        self.assertIn("EXPLICIT_ACTION_CLASS_MISMATCH", codes)
        self.assertIn("EXPLICIT_PURPOSE_MISMATCH", codes)
        self.assertIn("PLACEHOLDER_OR_UNOBSERVABLE_TEXT", codes)

    def test_semantically_constrained_plan_can_remain_a_reviewable_draft(self) -> None:
        request = semantic_planning_request()
        proposal = planning_proposal()
        proposal["request_id"] = request["request_id"]
        proposal["scenes"][0]["environment"] = "持续降雨"
        proposal["shots"] = [proposal["shots"][2]]
        proposal["shots"][0].update(
            {
                "shot_id": "SHOT-001",
                "ordinal": 1,
                "primary_purpose": "EMPHASIZE_EMOTION",
                "target_duration_seconds": 6,
                "framing": "CLOSE_UP",
                "action": {"class": "EXPRESS", "description": "孩子持续哭泣"},
                "composition": "面部占据主要画面",
                "emotion": "明显悲伤",
                "lighting": "阴天柔和侧光",
                "continuity_in": "孩子已经站在雨中",
                "continuity_out": "以泪水滑落状态结束",
                "observable_checks": ["泪水沿面颊连续滑落"],
            }
        )
        report = observe_proposal(request, proposal)
        self.assertEqual(report["blocking_observation_count"], 0)
        self.assertTrue(report["creative_review_required"])

    def test_extended_observability_terms_and_check_count_are_independent(self) -> None:
        request = semantic_planning_request()
        request["semantic_constraints"].update(
            {
                "minimum_observable_check_count": 3,
                "required_composition_terms": ["面部"],
                "required_emotion_terms": ["泪"],
                "required_continuity_in_terms": ["雨"],
                "required_continuity_out_terms": ["雨"],
                "required_observable_terms": ["相机"],
            }
        )
        proposal = planning_proposal()
        proposal["request_id"] = request["request_id"]
        proposal["shots"] = [proposal["shots"][2]]
        proposal["shots"][0].update(
            {
                "shot_id": "SHOT-001",
                "ordinal": 1,
                "primary_purpose": "EMPHASIZE_EMOTION",
                "target_duration_seconds": 6,
                "framing": "CLOSE_UP",
                "action": {"class": "EXPRESS", "description": "孩子持续哭泣"},
                "composition": "面部占据主要画面",
                "emotion": "悲伤但没有指定泪水状态",
                "continuity_in": "孩子已经站在雨中",
                "continuity_out": "孩子仍然站在雨中",
                "observable_checks": ["主体身份连续", "哭泣动作可见"],
            }
        )
        report = observe_proposal(request, proposal)
        codes = [item["code"] for item in report["observations"]]
        self.assertIn("REQUIRED_OBSERVABLE_TERM_MISSING", codes)
        self.assertIn("OBSERVABLE_CHECK_COUNT_BELOW_MINIMUM", codes)

    def test_collection_uses_exact_authorized_run_count_without_hidden_retry(self) -> None:
        calls: list[int] = []

        def planner(request: dict, run_index: int) -> dict:
            calls.append(run_index)
            proposal = deepcopy(planning_proposal(f"PROPOSAL-{run_index:03d}"))
            proposal["request_id"] = request["request_id"]
            return proposal

        proposals = collect_local_proposals(planning_request(), planner, 3)
        self.assertEqual(calls, [1, 2, 3])
        self.assertEqual(len(proposals), 3)


if __name__ == "__main__":
    unittest.main()
