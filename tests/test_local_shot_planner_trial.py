from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from shot_planning.local_trial import (
    LocalTrialError,
    compile_observable_stages_to_proposal,
    compile_tokenized_context_stages_to_proposal,
    compile_payload_to_proposal,
    observe_stage_payload,
    run_trial,
    strict_parse_model_output,
    validate_request_binding,
    validate_trial_contract,
    verify_evidence,
    write_json,
    write_manifest,
)
from shot_planning.prompting import (
    build_local_planner_context_stage_prompt,
    build_local_planner_observable_stage_prompt,
    build_local_planner_tokenized_context_stage_prompt,
)
from shot_planning.controlled_context import TOKENIZED_CONTEXT_STAGE_ORDER
from shot_planning.structured_observability import (
    OBSERVABLE_STAGE_ORDER,
    observe_controlled_semantic_stability,
)
from shot_planning.validation import observe_proposal


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    ROOT / "experiments" / "shot_planning" / "qwen3_0_6b_three_run_trial_v1.json"
)
V2_CONTRACT_PATH = (
    ROOT / "experiments" / "shot_planning" / "qwen3_0_6b_system_envelope_trial_v2.json"
)
V3_CONTRACT_PATH = (
    ROOT / "experiments" / "shot_planning" / "qwen3_0_6b_staged_trial_v3.json"
)
V4_CONTRACT_PATH = (
    ROOT / "experiments" / "shot_planning" / "qwen3_0_6b_semantic_trial_v4.json"
)
V5_CONTRACT_PATH = (
    ROOT / "experiments" / "shot_planning" / "qwen3_0_6b_observable_trial_v5.json"
)
V6_CONTRACT_PATH = (
    ROOT
    / "experiments"
    / "shot_planning"
    / "qwen3_0_6b_controlled_context_trial_v6.json"
)
V7_CONTRACT_PATH = (
    ROOT
    / "experiments"
    / "shot_planning"
    / "qwen3_0_6b_tokenized_context_trial_v7.json"
)
REQUEST_PATH = (
    ROOT
    / "experiments"
    / "shot_planning"
    / "foreign_child_crying_closeup_request_v1.json"
)
V5_REQUEST_PATH = (
    ROOT
    / "experiments"
    / "shot_planning"
    / "foreign_child_crying_closeup_request_v3.json"
)
V6_REQUEST_PATH = (
    ROOT
    / "experiments"
    / "shot_planning"
    / "foreign_child_crying_closeup_request_v4.json"
)
V7_REQUEST_PATH = (
    ROOT
    / "experiments"
    / "shot_planning"
    / "foreign_child_crying_closeup_request_v5.json"
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def proposal_from_prompt(prompt: dict) -> dict:
    return json.loads(prompt["user"])["required_output_shape"]


def observable_stage_outputs() -> dict[str, dict[str, str]]:
    return {
        "scene": {
            "location": "雨中的室外",
            "time": "未明确",
            "environment": "持续降雨",
            "continuity_anchor": "同一孩子与持续降雨",
        },
        "beat": {
            "purpose": "EMPHASIZE_EMOTION",
            "action": "孩子在雨中持续哭泣",
        },
        "shot_core": {
            "primary_purpose": "EMPHASIZE_EMOTION",
            "framing": "EXTREME_CLOSE_UP",
            "action_class": "EXPRESS",
            "action_description": "孩子在雨中持续哭泣",
            "camera_movement": "STATIC",
            "camera_direction": "NONE",
            "camera_speed": "NONE",
        },
        "composition": {
            "subject_placement": "CENTER",
            "face_coverage": "FACE_MOST_OF_FRAME",
            "focus_target": "EYES_AND_TEARS",
            "background_visibility": "RAIN_SOFTLY_BLURRED",
        },
        "performance": {
            "eye_state": "TEARS_WELLING",
            "tear_state": "ONE_TEAR_ROLLING",
            "mouth_state": "LOWER_LIP_TREMBLING",
            "expression_intensity": "RESTRAINED",
        },
        "lighting": {
            "light_source": "OVERCAST_DAYLIGHT",
            "light_quality": "SOFT_DIFFUSED",
            "face_readability": "FULLY_READABLE",
            "tear_highlight": "VISIBLE",
        },
        "continuity": {
            "entry_subject_state": "FACE_WET_AND_CRYING",
            "entry_environment_state": "CONTINUOUS_RAIN",
            "exit_subject_state": "SAME_FACE_WITH_VISIBLE_TEARS",
            "exit_environment_state": "CONTINUOUS_RAIN",
        },
    }


def controlled_context_stage_outputs() -> dict[str, dict[str, str]]:
    outputs = observable_stage_outputs()
    outputs["scene"] = {
        "location": "未明确地点",
        "time": "未明确时间",
        "environment": "持续降雨",
        "continuity_anchor": "同一主体与持续降雨",
    }
    outputs["beat"]["action"] = "孩子在雨中哭泣"
    outputs["shot_core"].update(
        {
            "camera_movement": "STATIC",
            "camera_direction": "NONE",
            "camera_speed": "NONE",
        }
    )
    return outputs


def tokenized_context_stage_outputs() -> dict[str, dict[str, str]]:
    base = controlled_context_stage_outputs()
    return {
        "scene_context": {
            "location": "UNSPECIFIED_LOCATION",
            "time": "UNSPECIFIED_TIME",
            "environment": "CONTINUOUS_RAIN",
            "continuity_anchor": "SAME_SUBJECT_AND_CONTINUOUS_RAIN",
        },
        "beat_purpose": {"purpose": "EMPHASIZE_EMOTION"},
        "shot_core": base["shot_core"],
        "composition": base["composition"],
        "performance": base["performance"],
        "lighting": base["lighting"],
        "continuity": base["continuity"],
    }


class LocalShotPlannerTrialTest(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = load(CONTRACT_PATH)
        self.v2_contract = load(V2_CONTRACT_PATH)
        self.v3_contract = load(V3_CONTRACT_PATH)
        self.v4_contract = load(V4_CONTRACT_PATH)
        self.v5_contract = load(V5_CONTRACT_PATH)
        self.v6_contract = load(V6_CONTRACT_PATH)
        self.v7_contract = load(V7_CONTRACT_PATH)
        self.request = load(REQUEST_PATH)
        self.v5_request = load(V5_REQUEST_PATH)
        self.v6_request = load(V6_REQUEST_PATH)
        self.v7_request = load(V7_REQUEST_PATH)

    def test_fixed_contract_rejects_more_runs_retry_or_model_drift(self) -> None:
        validate_trial_contract(self.contract)
        mutated = deepcopy(self.contract)
        mutated["execution"]["run_count"] = 4
        with self.assertRaisesRegex(ValueError, "固定三次"):
            validate_trial_contract(mutated)

        mutated = deepcopy(self.contract)
        mutated["resource_budget"]["retry_count"] = 1
        with self.assertRaisesRegex(ValueError, "资源预算"):
            validate_trial_contract(mutated)

        mutated = deepcopy(self.contract)
        mutated["model"]["revision"] = "main"
        with self.assertRaisesRegex(ValueError, "固定合同"):
            validate_trial_contract(mutated)

    def test_request_binding_rejects_changed_path_or_content(self) -> None:
        validate_request_binding(
            self.contract,
            self.request,
            "experiments/shot_planning/foreign_child_crying_closeup_request_v1.json",
        )
        with self.assertRaisesRegex(LocalTrialError, "路径"):
            validate_request_binding(self.contract, self.request, "other.json")
        changed = deepcopy(self.request)
        changed["source_text"] += "。"
        with self.assertRaisesRegex(LocalTrialError, "摘要"):
            validate_request_binding(
                self.contract,
                changed,
                "experiments/shot_planning/foreign_child_crying_closeup_request_v1.json",
            )

    def test_strict_parser_does_not_repair_markdown_fence(self) -> None:
        value, observation = strict_parse_model_output('```json\n{"value": 1}\n```')
        self.assertIsInstance(value, str)
        self.assertFalse(observation["parsed"])
        self.assertFalse(observation["automatic_repair_attempted"])

    def test_second_version_requires_system_envelope_strategy(self) -> None:
        validate_trial_contract(self.v2_contract)
        mutated = deepcopy(self.v2_contract)
        mutated["prompt_strategy"]["assistant_prefill"] = ""
        with self.assertRaisesRegex(ValueError, "系统封装"):
            validate_trial_contract(mutated)

    def test_payload_compiler_only_adds_system_owned_envelope(self) -> None:
        payload = {
            "scenes": [
                {
                    "location": "雨中的室外",
                    "time": "未明确",
                    "environment": "下雨",
                    "continuity_anchors": ["同一孩子", "持续降雨"],
                }
            ],
            "narrative_beats": [
                {
                    "scene_ordinal": 1,
                    "source_span": {
                        "start": 0,
                        "end": len(self.request["source_text"]),
                        "quote": self.request["source_text"],
                    },
                    "purpose": "EMPHASIZE_EMOTION",
                    "action": "孩子在雨中哭泣",
                }
            ],
            "shots": [
                {
                    "scene_ordinal": 1,
                    "beat_ordinals": [1],
                    "primary_purpose": "EMPHASIZE_EMOTION",
                    "target_duration_seconds": 6,
                    "framing": "CLOSE_UP",
                    "action_class": "EXPRESS",
                    "action_description": "孩子持续哭泣",
                    "composition": "面部占据画面主要区域",
                    "camera_movement": "STATIC",
                    "camera_direction": "NONE",
                    "camera_speed": "NONE",
                    "emotion": "悲伤",
                    "lighting": "阴天柔光",
                    "continuity_in": "孩子已经在雨中",
                    "continuity_out": "以泪水滑落结束",
                    "observable_checks": ["只有一个主要孩子"],
                }
            ],
        }
        proposal = compile_payload_to_proposal(
            payload,
            self.request,
            self.v2_contract,
            proposal_id="PROPOSAL-TEST-001",
            run_id="RUN-TEST-001",
        )
        self.assertEqual(proposal["proposal_id"], "PROPOSAL-TEST-001")
        self.assertEqual(proposal["scenes"][0]["location"], "雨中的室外")
        self.assertEqual(proposal["shots"][0]["shot_id"], "SHOT-001")
        self.assertEqual(
            proposal["planner"]["prompt_contract_version"],
            "local-shot-planner-payload.v2",
        )

    def test_third_version_fixes_three_stages_and_nine_calls(self) -> None:
        validate_trial_contract(self.v3_contract)
        mutated = deepcopy(self.v3_contract)
        mutated["resource_budget"]["maximum_model_calls"] = 10
        with self.assertRaisesRegex(ValueError, "资源预算"):
            validate_trial_contract(mutated)
        self.assertEqual(
            observe_stage_payload(
                "beat",
                {"purpose": "EMPHASIZE_EMOTION", "action": "孩子哭泣", "extra": "x"},
            )[0]["code"],
            "STAGE_KEYS_MISMATCH",
        )

    def test_fourth_version_requires_explicit_semantic_strategy(self) -> None:
        validate_trial_contract(self.v4_contract)
        mutated = deepcopy(self.v4_contract)
        mutated["prompt_strategy"]["semantic_constraints_enforced"] = False
        with self.assertRaisesRegex(ValueError, "显式语义约束"):
            validate_trial_contract(mutated)

    def test_fifth_version_fixes_seven_stages_twenty_one_calls_and_compiler(self) -> None:
        validate_trial_contract(self.v5_contract)
        self.assertEqual(
            self.v5_contract["prompt_strategy"]["stages"],
            list(OBSERVABLE_STAGE_ORDER),
        )
        for invalid_call_count in (20, 22):
            mutated = deepcopy(self.v5_contract)
            mutated["resource_budget"]["maximum_model_calls"] = invalid_call_count
            with self.assertRaisesRegex(ValueError, "资源预算"):
                validate_trial_contract(mutated)
        mutated = deepcopy(self.v5_contract)
        mutated["prompt_strategy"]["stages"] = list(reversed(OBSERVABLE_STAGE_ORDER))
        with self.assertRaisesRegex(ValueError, "七个结构化"):
            validate_trial_contract(mutated)

    def test_sixth_version_fixes_context_roles_and_camera_policy(self) -> None:
        validate_trial_contract(self.v6_contract)
        mutated = deepcopy(self.v6_contract)
        mutated["prompt_strategy"]["camera_constraints_enforced"] = False
        with self.assertRaisesRegex(ValueError, "场景角色和相机"):
            validate_trial_contract(mutated)

        scene_prompt = build_local_planner_context_stage_prompt(
            self.v6_request, "scene"
        )
        scene_contract = json.loads(scene_prompt["user"])["stage_contract"]
        self.assertEqual(
            scene_prompt["prompt_contract_version"],
            "local-shot-planner-controlled-context.v6",
        )
        self.assertEqual(scene_contract["allowed_values"]["location"], ["未明确地点"])
        self.assertEqual(scene_contract["allowed_values"]["time"], ["未明确时间"])

        core_prompt = build_local_planner_context_stage_prompt(
            self.v6_request, "shot_core"
        )
        core_allowed = json.loads(core_prompt["user"])["stage_contract"][
            "allowed_values"
        ]
        self.assertEqual(core_allowed["camera_movement"], ["STATIC"])
        self.assertEqual(core_allowed["camera_direction"], ["NONE"])
        self.assertEqual(core_allowed["camera_speed"], ["NONE"])

    def test_sixth_version_observer_rejects_wrong_context_roles(self) -> None:
        outputs = controlled_context_stage_outputs()
        wrong_scene = deepcopy(outputs["scene"])
        wrong_scene.update({"location": "一个外国小孩子", "time": "在雨中"})
        observations = observe_stage_payload(
            "scene", wrong_scene, request=self.v6_request
        )
        invalid_paths = {
            item["path"]
            for item in observations
            if item["code"] == "STAGE_ENUM_VALUE_INVALID"
        }
        self.assertIn("$.stages.scene.location", invalid_paths)
        self.assertIn("$.stages.scene.time", invalid_paths)

    def test_seventh_version_tokenizes_scene_and_reuses_core_action(self) -> None:
        validate_trial_contract(self.v7_contract)
        self.assertEqual(
            self.v7_contract["prompt_strategy"]["stages"],
            list(TOKENIZED_CONTEXT_STAGE_ORDER),
        )
        prompt = build_local_planner_tokenized_context_stage_prompt(
            self.v7_request, "scene_context"
        )
        body = json.loads(prompt["user"])
        self.assertEqual(
            prompt["prompt_contract_version"],
            "local-shot-planner-tokenized-context.v7",
        )
        self.assertEqual(
            body["stage_contract"]["allowed_values"]["environment"],
            ["CONTINUOUS_RAIN"],
        )
        beat_prompt = build_local_planner_tokenized_context_stage_prompt(
            self.v7_request, "beat_purpose"
        )
        beat_keys = json.loads(beat_prompt["user"])["stage_contract"]["required_keys"]
        self.assertEqual(beat_keys, ["purpose"])

        proposal = compile_tokenized_context_stages_to_proposal(
            tokenized_context_stage_outputs(),
            self.v7_request,
            self.v7_contract,
            proposal_id="PROPOSAL-V7-TEST-001",
            run_id="RUN-V7-TEST-001",
        )
        self.assertEqual(proposal["scenes"][0]["location"], "未明确地点")
        self.assertEqual(proposal["scenes"][0]["time"], "未明确时间")
        self.assertEqual(proposal["scenes"][0]["environment"], "持续降雨")
        self.assertEqual(
            proposal["narrative_beats"][0]["action"],
            proposal["shots"][0]["action"]["description"],
        )
        self.assertEqual(
            observe_proposal(self.v7_request, proposal)["blocking_observation_count"],
            0,
        )

    def test_camera_direction_compatibility_is_observed_independently(self) -> None:
        core = observable_stage_outputs()["shot_core"]
        core.update(
            {
                "camera_movement": "ZOOM",
                "camera_direction": "LEFT",
                "camera_speed": "FAST",
            }
        )
        observations = observe_stage_payload("shot_core", core)
        self.assertIn(
            "STAGE_CAMERA_DIRECTION_INCOMPATIBLE",
            {item["code"] for item in observations},
        )
        mutated = deepcopy(self.v5_contract)
        mutated["prompt_strategy"]["compiler_contract_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "七个结构化"):
            validate_trial_contract(mutated)

    def test_fifth_version_prompts_expose_only_stage_specific_flat_contracts(self) -> None:
        for stage in OBSERVABLE_STAGE_ORDER:
            prompt = build_local_planner_observable_stage_prompt(self.v5_request, stage)
            body = json.loads(prompt["user"])
            self.assertEqual(prompt["stage"], stage)
            self.assertEqual(prompt["assistant_prefill"], "{")
            self.assertEqual(
                prompt["prompt_contract_version"],
                "local-shot-planner-structured-observability.v5",
            )
            required_keys = body["stage_contract"]["required_keys"]
            self.assertEqual(set(required_keys), set(observable_stage_outputs()[stage]))
            self.assertNotIn("proposal_id", prompt["user"])
            self.assertNotIn("formal_quality_acceptance", prompt["user"])

    def test_fifth_version_stage_observer_rejects_enum_and_camera_conflicts(self) -> None:
        invalid = observable_stage_outputs()["shot_core"]
        invalid["framing"] = "MEDIUM_WIDE"
        invalid["camera_direction"] = "LEFT"
        invalid["camera_speed"] = "SLOW"
        observations = observe_stage_payload(
            "shot_core", invalid, request=self.v5_request
        )
        codes = {item["code"] for item in observations}
        self.assertIn("STAGE_ENUM_VALUE_INVALID", codes)
        self.assertIn("STAGE_STATIC_CAMERA_HAS_MOTION", codes)

    def test_fifth_version_compiler_expands_selected_tokens_without_lowering_checks(self) -> None:
        proposal = compile_observable_stages_to_proposal(
            observable_stage_outputs(),
            self.v5_request,
            self.v5_contract,
            proposal_id="PROPOSAL-V5-TEST-001",
            run_id="RUN-V5-TEST-001",
        )
        report = observe_proposal(self.v5_request, proposal)
        self.assertEqual(report["blocking_observation_count"], 0)
        shot = proposal["shots"][0]
        self.assertIn("面部占据画面大部分区域", shot["composition"])
        self.assertIn("一滴泪沿面颊滑落", shot["emotion"])
        self.assertIn("背景保持持续降雨", shot["continuity_in"])
        self.assertEqual(len(shot["observable_checks"]), 5)
        self.assertEqual(proposal["status"], "DRAFT_NON_AUTHORITATIVE")
        self.assertTrue(report["creative_review_required"])

    def test_controlled_semantic_stability_is_separate_from_structure(self) -> None:
        runs = [observable_stage_outputs(), observable_stage_outputs(), observable_stage_outputs()]
        runs[2]["composition"]["subject_placement"] = "LEFT_THIRD"
        observation = observe_controlled_semantic_stability(runs)
        self.assertEqual(observation["comparable_run_count"], 3)
        self.assertEqual(
            observation["largest_exact_controlled_semantic_group_ratio"], 0.6667
        )
        self.assertEqual(
            observation["field_consistency"]["composition.subject_placement"][
                "largest_group_ratio"
            ],
            0.6667,
        )
        self.assertFalse(observation["formal_decision_created"])

    def test_three_unique_runs_are_retained_and_compared(self) -> None:
        calls: list[int] = []

        def generate(prompt: dict, run_index: int) -> str:
            calls.append(run_index)
            return json.dumps(proposal_from_prompt(prompt), ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-PLAN-TEST-001"
            summary = run_trial(
                self.contract,
                self.request,
                "LOCAL-PLAN-TEST-001",
                evidence_dir,
                generate,
            )
            self.assertEqual(calls, [1, 2, 3])
            self.assertEqual(summary["run_count_observed"], 3)
            self.assertEqual(summary["parsed_run_count"], 3)
            self.assertEqual(summary["structurally_observable_run_count"], 3)
            self.assertTrue(summary["comparison_performed"])
            self.assertEqual(summary["largest_exact_structure_group_ratio"], 1.0)
            self.assertEqual(summary["automatic_retry_count"], 0)
            self.assertTrue((evidence_dir / "raw_output_003.txt").is_file())
            stability = load(evidence_dir / "stability_observation.json")
            self.assertEqual(stability["comparable_run_count"], 3)
            manifest = write_manifest(evidence_dir)
            self.assertGreaterEqual(len(manifest["files"]), 15)
            verification = verify_evidence(evidence_dir)
            self.assertEqual(
                verification["package_integrity_observation"],
                "COMPLETE_AND_DIGEST_MATCHED",
            )

            with self.assertRaisesRegex(LocalTrialError, "不得覆盖"):
                run_trial(
                    self.contract,
                    self.request,
                    "LOCAL-PLAN-TEST-001",
                    evidence_dir,
                    generate,
                )

    def test_evidence_verification_detects_tampered_raw_output(self) -> None:
        def generate(prompt: dict, _run_index: int) -> str:
            return json.dumps(proposal_from_prompt(prompt), ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-PLAN-TAMPER-001"
            run_trial(
                self.contract,
                self.request,
                "LOCAL-PLAN-TAMPER-001",
                evidence_dir,
                generate,
            )
            write_manifest(evidence_dir)
            (evidence_dir / "raw_output_001.txt").write_text("tampered", encoding="utf-8")
            with self.assertRaisesRegex(LocalTrialError, "摘要"):
                verify_evidence(evidence_dir)

    def test_scheduled_runs_continue_after_one_error_without_retry(self) -> None:
        calls: list[int] = []

        def generate(prompt: dict, run_index: int) -> str:
            calls.append(run_index)
            if run_index == 2:
                raise RuntimeError("固定测试错误")
            return json.dumps(proposal_from_prompt(prompt), ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            summary = run_trial(
                self.contract,
                self.request,
                "LOCAL-PLAN-TEST-002",
                Path(temporary) / "LOCAL-PLAN-TEST-002",
                generate,
            )
        self.assertEqual(calls, [1, 2, 3])
        self.assertEqual(summary["run_count_observed"], 3)
        self.assertEqual(summary["parsed_run_count"], 2)
        self.assertEqual(summary["automatic_retry_count"], 0)
        self.assertTrue(summary["comparison_performed"])

    def test_second_version_compiles_three_payloads_before_comparison(self) -> None:
        def generate(prompt: dict, _run_index: int) -> str:
            self.assertEqual(prompt["assistant_prefill"], "{")
            payload = json.loads(prompt["user"])["required_payload_shape"]
            return json.dumps(payload, ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-PLAN-V2-TEST-001"
            summary = run_trial(
                self.v2_contract,
                self.request,
                "LOCAL-PLAN-V2-TEST-001",
                evidence_dir,
                generate,
            )
            self.assertEqual(summary["parsed_run_count"], 3)
            self.assertEqual(summary["structurally_observable_run_count"], 3)
            self.assertEqual(summary["largest_exact_structure_group_ratio"], 1.0)
            self.assertTrue((evidence_dir / "payload_003.json").is_file())
            proposal = load(evidence_dir / "proposal_001.json")
            self.assertEqual(proposal["status"], "DRAFT_NON_AUTHORITATIVE")
            self.assertEqual(
                proposal["planner"]["prompt_contract_version"],
                "local-shot-planner-payload.v2",
            )

    def test_third_version_runs_nine_fixed_flat_stage_calls(self) -> None:
        stage_outputs = {
            "scene": {
                "location": "雨中的室外",
                "time": "未明确",
                "environment": "持续降雨",
                "continuity_anchor": "同一孩子与持续降雨",
            },
            "beat": {
                "purpose": "EMPHASIZE_EMOTION",
                "action": "孩子在雨中哭泣",
            },
            "shot": {
                "primary_purpose": "EMPHASIZE_EMOTION",
                "framing": "CLOSE_UP",
                "action_class": "EXPRESS",
                "action_description": "孩子持续哭泣",
                "composition": "面部占据画面主要区域",
                "camera_movement": "STATIC",
                "camera_direction": "NONE",
                "camera_speed": "NONE",
                "emotion": "悲伤",
                "lighting": "阴天柔光",
                "continuity_in": "孩子已经在雨中",
                "continuity_out": "以哭泣状态结束",
                "observable_check": "只有一个主要孩子且泪水可见",
            },
        }
        calls: list[tuple[int, str]] = []

        def generate(prompt: dict, call_index: int) -> str:
            calls.append((call_index, prompt["stage"]))
            return json.dumps(stage_outputs[prompt["stage"]], ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-PLAN-V3-TEST-001"
            summary = run_trial(
                self.v3_contract,
                self.request,
                "LOCAL-PLAN-V3-TEST-001",
                evidence_dir,
                generate,
            )
            self.assertEqual(len(calls), 9)
            self.assertEqual(summary["model_call_count_observed"], 9)
            self.assertEqual(summary["parsed_run_count"], 3)
            self.assertEqual(summary["structurally_observable_run_count"], 3)
            self.assertTrue(summary["comparison_performed"])
            self.assertEqual(summary["largest_exact_structure_group_ratio"], 1.0)
            self.assertTrue((evidence_dir / "raw_output_003_shot.txt").is_file())
            proposal = load(evidence_dir / "proposal_001.json")
            self.assertEqual(len(proposal["scenes"]), 1)
            self.assertEqual(len(proposal["narrative_beats"]), 1)
            self.assertEqual(len(proposal["shots"]), 1)

    def test_fifth_version_runs_twenty_one_calls_and_verifies_full_evidence(self) -> None:
        outputs = observable_stage_outputs()
        calls: list[tuple[int, str]] = []

        def generate(prompt: dict, call_index: int) -> str:
            calls.append((call_index, prompt["stage"]))
            return json.dumps(outputs[prompt["stage"]], ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-PLAN-V5-TEST-001"
            summary = run_trial(
                self.v5_contract,
                self.v5_request,
                "LOCAL-PLAN-V5-TEST-001",
                evidence_dir,
                generate,
            )
            self.assertEqual(len(calls), 21)
            self.assertEqual(
                [stage for _index, stage in calls[:7]], list(OBSERVABLE_STAGE_ORDER)
            )
            self.assertEqual(summary["model_call_count_observed"], 21)
            self.assertEqual(summary["parsed_run_count"], 3)
            self.assertEqual(summary["structurally_observable_run_count"], 3)
            self.assertEqual(
                summary["largest_exact_controlled_semantic_group_ratio"], 1.0
            )
            self.assertTrue((evidence_dir / "raw_output_003_continuity.txt").is_file())
            self.assertTrue((evidence_dir / "compiler_contract.json").is_file())
            write_json(evidence_dir / "environment.json", {"test_environment": True})
            write_manifest(evidence_dir)
            verification = verify_evidence(evidence_dir)
            self.assertEqual(
                verification["package_integrity_observation"],
                "COMPLETE_AND_DIGEST_MATCHED",
            )

    def test_fifth_version_invalid_token_fails_closed_without_extra_calls(self) -> None:
        outputs = observable_stage_outputs()
        calls: list[int] = []

        def generate(prompt: dict, call_index: int) -> str:
            calls.append(call_index)
            payload = deepcopy(outputs[prompt["stage"]])
            if call_index == 4:
                payload["subject_placement"] = "UNSUPPORTED"
            return json.dumps(payload, ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-PLAN-V5-INVALID-001"
            summary = run_trial(
                self.v5_contract,
                self.v5_request,
                "LOCAL-PLAN-V5-INVALID-001",
                evidence_dir,
                generate,
            )
            self.assertEqual(calls, list(range(1, 22)))
            self.assertEqual(summary["automatic_retry_count"], 0)
            self.assertFalse((evidence_dir / "proposal_001.json").exists())
            observation = load(evidence_dir / "proposal_observation_001.json")
            self.assertIn(
                "STAGE_ENUM_VALUE_INVALID",
                {item["code"] for item in observation["observations"]},
            )
            controlled = load(
                evidence_dir / "controlled_semantic_stability_observation.json"
            )
            self.assertEqual(controlled["excluded_run_indices"], [1])

    def test_sixth_version_runs_fixed_context_without_blocking_observations(self) -> None:
        outputs = controlled_context_stage_outputs()
        calls: list[int] = []

        def generate(prompt: dict, call_index: int) -> str:
            calls.append(call_index)
            return json.dumps(outputs[prompt["stage"]], ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-PLAN-V6-TEST-001"
            summary = run_trial(
                self.v6_contract,
                self.v6_request,
                "LOCAL-PLAN-V6-TEST-001",
                evidence_dir,
                generate,
            )
            self.assertEqual(calls, list(range(1, 22)))
            self.assertEqual(summary["structurally_observable_run_count"], 3)
            proposal = load(evidence_dir / "proposal_001.json")
            self.assertEqual(proposal["scenes"][0]["location"], "未明确地点")
            self.assertEqual(proposal["scenes"][0]["time"], "未明确时间")
            self.assertEqual(
                proposal["shots"][0]["camera"],
                {"movement": "STATIC", "direction": "NONE", "speed": "NONE"},
            )
            write_json(evidence_dir / "environment.json", {"test_environment": True})
            write_manifest(evidence_dir)
            verification = verify_evidence(evidence_dir)
            self.assertEqual(
                verification["package_integrity_observation"],
                "COMPLETE_AND_DIGEST_MATCHED",
            )

    def test_seventh_version_runs_twenty_one_tokenized_context_calls(self) -> None:
        outputs = tokenized_context_stage_outputs()
        calls: list[tuple[int, str]] = []

        def generate(prompt: dict, call_index: int) -> str:
            calls.append((call_index, prompt["stage"]))
            return json.dumps(outputs[prompt["stage"]], ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-PLAN-V7-TEST-001"
            summary = run_trial(
                self.v7_contract,
                self.v7_request,
                "LOCAL-PLAN-V7-TEST-001",
                evidence_dir,
                generate,
            )
            self.assertEqual(len(calls), 21)
            self.assertEqual(
                [stage for _index, stage in calls[:7]],
                list(TOKENIZED_CONTEXT_STAGE_ORDER),
            )
            self.assertEqual(summary["structurally_observable_run_count"], 3)
            self.assertEqual(
                summary["largest_exact_controlled_semantic_group_ratio"], 1.0
            )
            self.assertTrue(
                (evidence_dir / "context_compiler_contract.json").is_file()
            )
            write_json(evidence_dir / "environment.json", {"test_environment": True})
            write_manifest(evidence_dir)
            verification = verify_evidence(evidence_dir)
            self.assertEqual(
                verification["package_integrity_observation"],
                "COMPLETE_AND_DIGEST_MATCHED",
            )

    def test_controlled_compiler_does_not_leak_crying_trial_terms(self) -> None:
        request = deepcopy(self.v5_request)
        request["request_id"] = "PLAN-ACTOR-SMILE-001"
        request["source_text"] = "一位演员微笑的中景镜头"
        stages = observable_stage_outputs()
        stages["scene"] = {
            "location": "室内",
            "time": "未明确",
            "environment": "安静背景",
            "continuity_anchor": "同一演员与同一背景",
        }
        stages["beat"] = {"purpose": "EMPHASIZE_EMOTION", "action": "演员保持微笑"}
        stages["shot_core"].update(
            {
                "framing": "MEDIUM",
                "action_description": "演员保持微笑",
            }
        )
        stages["composition"].update(
            {
                "face_coverage": "UPPER_BODY_AND_FACE_VISIBLE",
                "focus_target": "FACE",
                "background_visibility": "BACKGROUND_SOFTLY_BLURRED",
            }
        )
        stages["performance"] = {
            "eye_state": "EYES_RELAXED",
            "tear_state": "NO_VISIBLE_TEARS",
            "mouth_state": "MOUTH_SMILING",
            "expression_intensity": "NEUTRAL",
        }
        stages["continuity"] = {
            "entry_subject_state": "SAME_SUBJECT_STATE",
            "entry_environment_state": "SAME_ENVIRONMENT",
            "exit_subject_state": "SUBJECT_STATE_CONTINUES",
            "exit_environment_state": "SAME_ENVIRONMENT",
        }
        proposal = compile_observable_stages_to_proposal(
            stages,
            request,
            self.v5_contract,
            proposal_id="PROPOSAL-NEUTRAL-001",
            run_id="RUN-NEUTRAL-001",
        )
        compiled_text = json.dumps(proposal["shots"][0], ensure_ascii=False)
        self.assertNotIn("孩子", compiled_text)
        self.assertNotIn("持续降雨", compiled_text)
        self.assertNotIn("正在哭泣", compiled_text)
        self.assertIn("嘴角保持可见微笑", compiled_text)


if __name__ == "__main__":
    unittest.main()
