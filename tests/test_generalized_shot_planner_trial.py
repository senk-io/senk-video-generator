from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from shot_planning.contracts import (
    PLANNER_GUARDED_SOURCE_FACT_PROMPT_CONTRACT_VERSION,
    ShotPlanningContractError,
    canonical_sha256,
    validate_request,
)
from shot_planning.controlled_context import (
    TOKENIZED_CONTEXT_ALLOWED_VALUES,
    tokenized_context_compiler_contract_sha256,
)
from shot_planning.generalized_observability import (
    GENERALIZED_OBSERVABILITY_COMPILER_VERSION,
    GENERALIZED_STAGE_ALLOWED_VALUES,
    GENERALIZED_STAGE_REQUIRED_KEYS,
    generalized_compiler_contract_sha256,
    observe_generalized_semantic_stability,
    observe_generalized_stage_consistency,
)
from shot_planning.local_trial import (
    LocalTrialError,
    compile_generalized_stages_to_proposal,
    observe_stage_payload,
    run_trial,
    validate_request_binding,
    validate_trial_contract,
    verify_evidence,
    write_json,
    write_manifest,
)
from shot_planning.prompting import (
    build_local_planner_generalized_stage_prompt,
    build_local_planner_prompt,
)
from shot_planning.prompting import build_local_planner_scalar_choice_stage_prompt
from shot_planning.prompting import build_local_planner_semantic_gloss_stage_prompt
from shot_planning.prompting import build_local_planner_hybrid_stage_prompt
from shot_planning.prompting import (
    build_local_planner_guarded_source_fact_stage_prompt,
)
from shot_planning.semantic_choice import (
    SEMANTIC_CHOICE_GLOSSARY_VERSION,
    choice_glossary_for_stage,
    semantic_choice_glossary_sha256,
)
from shot_planning.source_facts import (
    SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V1,
    SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
    extract_source_facts,
    hybrid_merge_contract_sha256,
    source_fact_extractor_contract_sha256,
)
from shot_planning.structured_observability import (
    STRUCTURED_STAGE_ALLOWED_VALUES,
    compiler_contract_sha256,
)
from shot_planning.validation import observe_proposal


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_ROOT = ROOT / "experiments" / "shot_planning"
CASE_FILES = {
    "crying": (
        "generalized_child_crying_closeup_request_v1.json",
        "qwen3_0_6b_generalized_crying_trial_v8.json",
    ),
    "smile": (
        "generalized_actor_smile_medium_request_v1.json",
        "qwen3_0_6b_generalized_smile_trial_v8.json",
    ),
    "bicycle": (
        "generalized_bicycle_left_to_right_wide_request_v1.json",
        "qwen3_0_6b_generalized_bicycle_trial_v8.json",
    ),
}
V11_CASE_FILES = {
    "crying": "qwen3_0_6b_hybrid_source_facts_crying_trial_v11.json",
    "smile": "qwen3_0_6b_hybrid_source_facts_smile_trial_v11.json",
    "bicycle": "qwen3_0_6b_hybrid_source_facts_bicycle_trial_v11.json",
}
V12_SMILE_TRIAL_FILE = "qwen3_0_6b_guarded_source_facts_smile_trial_v12.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def case_values(case_name: str) -> tuple[dict, dict, dict[str, dict[str, str]]]:
    request_name, contract_name = CASE_FILES[case_name]
    request = load(EXPERIMENT_ROOT / request_name)
    contract = load(EXPERIMENT_ROOT / contract_name)
    common_core = {
        "action_description": request["source_text"],
        "camera_movement": "STATIC",
        "camera_direction": "NONE",
        "camera_speed": "NONE",
    }
    if case_name == "crying":
        stages = {
            "scene_context": {
                "location": "OUTDOOR_LOCATION",
                "time": "DAY",
                "environment": "CONTINUOUS_RAIN",
                "continuity_anchor": "SAME_SUBJECT_AND_CONTINUOUS_RAIN",
            },
            "beat_purpose": {"purpose": "EMPHASIZE_EMOTION"},
            "shot_core": {
                **common_core,
                "primary_purpose": "EMPHASIZE_EMOTION",
                "framing": "CLOSE_UP",
                "action_class": "EXPRESS",
            },
            "composition": {
                "subject_placement": "CENTER",
                "subject_scale": "FACE_DOMINANT",
                "focus_target": "EYES_AND_TEARS",
                "background_visibility": "RAIN_SOFTLY_BLURRED",
            },
            "performance": {
                "orientation_state": "FACING_CAMERA",
                "visible_action_state": "CRYING",
                "detail_state": "TEARS_VISIBLE",
                "performance_intensity": "RESTRAINED",
            },
            "lighting": {
                "light_source": "OVERCAST_DAYLIGHT",
                "light_quality": "SOFT_DIFFUSED",
                "subject_readability": "FACE_FULLY_READABLE",
                "highlight_state": "TEAR_HIGHLIGHT_VISIBLE",
            },
            "continuity": {
                "entry_subject_state": "SUBJECT_ALREADY_CRYING",
                "entry_environment_state": "CONTINUOUS_RAIN",
                "exit_subject_state": "CRYING_CONTINUES",
                "exit_environment_state": "CONTINUOUS_RAIN",
            },
        }
    elif case_name == "smile":
        stages = {
            "scene_context": {
                "location": "INDOOR_LOCATION",
                "time": "DAY",
                "environment": "STABLE_ENVIRONMENT",
                "continuity_anchor": "SAME_SUBJECT_AND_ENVIRONMENT",
            },
            "beat_purpose": {"purpose": "EMPHASIZE_EMOTION"},
            "shot_core": {
                **common_core,
                "primary_purpose": "EMPHASIZE_EMOTION",
                "framing": "MEDIUM",
                "action_class": "EXPRESS",
            },
            "composition": {
                "subject_placement": "CENTER",
                "subject_scale": "UPPER_BODY_VISIBLE",
                "focus_target": "FACE",
                "background_visibility": "BACKGROUND_SOFTLY_BLURRED",
            },
            "performance": {
                "orientation_state": "FACING_CAMERA",
                "visible_action_state": "SMILING",
                "detail_state": "RELAXED_FACE_VISIBLE",
                "performance_intensity": "GENTLE",
            },
            "lighting": {
                "light_source": "INTERIOR_SOFT_LIGHT",
                "light_quality": "LOW_CONTRAST",
                "subject_readability": "FACE_FULLY_READABLE",
                "highlight_state": "NATURAL_FACE_HIGHLIGHT",
            },
            "continuity": {
                "entry_subject_state": "SUBJECT_ALREADY_SMILING",
                "entry_environment_state": "SAME_INDOOR_ENVIRONMENT",
                "exit_subject_state": "SMILE_CONTINUES",
                "exit_environment_state": "SAME_INDOOR_ENVIRONMENT",
            },
        }
    else:
        stages = {
            "scene_context": {
                "location": "OUTDOOR_LOCATION",
                "time": "NIGHT",
                "environment": "STABLE_ENVIRONMENT",
                "continuity_anchor": "SAME_SUBJECT_AND_ENVIRONMENT",
            },
            "beat_purpose": {"purpose": "DEVELOP_ACTION"},
            "shot_core": {
                **common_core,
                "primary_purpose": "DEVELOP_ACTION",
                "framing": "WIDE",
                "action_class": "MOVE",
            },
            "composition": {
                "subject_placement": "LEFT_THIRD",
                "subject_scale": "FULL_SUBJECT_VISIBLE",
                "focus_target": "SUBJECT_ACTION",
                "background_visibility": "STREET_VISIBLE_AROUND_SUBJECT",
            },
            "performance": {
                "orientation_state": "MOVING_LEFT_TO_RIGHT",
                "visible_action_state": "FORWARD_MOTION",
                "detail_state": "MOTION_DETAIL_VISIBLE",
                "performance_intensity": "MODERATE",
            },
            "lighting": {
                "light_source": "NIGHT_STREET_LIGHT",
                "light_quality": "DIRECTIONAL_LOW_KEY",
                "subject_readability": "MOTION_FULLY_READABLE",
                "highlight_state": "SUBJECT_EDGE_HIGHLIGHT",
            },
            "continuity": {
                "entry_subject_state": "SUBJECT_ENTERING_FROM_LEFT",
                "entry_environment_state": "SAME_NIGHT_STREET",
                "exit_subject_state": "SUBJECT_EXITS_RIGHT",
                "exit_environment_state": "SAME_NIGHT_STREET",
            },
        }
    return request, contract, stages


class GeneralizedShotPlannerTrialTest(unittest.TestCase):
    def test_old_compiler_digests_remain_frozen_and_v8_is_independent(self) -> None:
        self.assertEqual(
            compiler_contract_sha256(),
            "a3d718daa5858310eb80855df10e07cc9ea086a6486dce9d82f02aa235f72014",
        )
        self.assertEqual(
            tokenized_context_compiler_contract_sha256(),
            "9da95ac0bd954b3f6491a8a38bf6670d4096caf25ea26fad765c7f2fb5131067",
        )
        self.assertEqual(
            generalized_compiler_contract_sha256(),
            "e56d6777fab573f55aba8a8e264e8dbb9ccb9ab60aad671e2be4d743cab1c0b5",
        )
        self.assertEqual(
            semantic_choice_glossary_sha256(),
            "be4418dbca8a4f401c89a1d8e4d15c1d418dfc848dddb5e71b0b491e05da4fd7",
        )

    def test_all_v8_contracts_bind_v2_requests(self) -> None:
        for request_name, contract_name in CASE_FILES.values():
            request = validate_request(load(EXPERIMENT_ROOT / request_name))
            contract = validate_trial_contract(load(EXPERIMENT_ROOT / contract_name))
            validate_request_binding(
                contract,
                request,
                f"experiments/shot_planning/{request_name}",
            )
            self.assertEqual(contract["resource_budget"]["maximum_model_calls"], 21)

    def test_request_and_trial_schema_generations_cannot_cross_bind(self) -> None:
        v2_request, v8_contract, _stages = case_values("crying")
        v7_contract = load(
            EXPERIMENT_ROOT / "qwen3_0_6b_tokenized_context_trial_v7.json"
        )
        with self.assertRaisesRegex(LocalTrialError, "版本边界不一致"):
            validate_request_binding(
                v7_contract,
                v2_request,
                v7_contract["request_binding"]["request_file"],
            )
        v1_request = load(
            EXPERIMENT_ROOT / "foreign_child_crying_closeup_request_v5.json"
        )
        with self.assertRaisesRegex(LocalTrialError, "版本边界不一致"):
            validate_request_binding(
                v8_contract,
                v1_request,
                v8_contract["request_binding"]["request_file"],
            )

    def test_v2_request_requires_versioned_generalized_compiler(self) -> None:
        request, _contract, _stages = case_values("crying")
        mutated = deepcopy(request)
        mutated["schema_version"] = "shot-planning-request.v1"
        with self.assertRaises(ShotPlanningContractError):
            validate_request(mutated)
        mutated = deepcopy(request)
        del mutated["controlled_observability_compiler_version"]
        with self.assertRaises(ShotPlanningContractError):
            validate_request(mutated)
        mutated = deepcopy(request)
        mutated["required_subject_ids"] = []
        with self.assertRaisesRegex(
            ShotPlanningContractError, "系统不得补造主体"
        ):
            validate_request(mutated)
        with self.assertRaisesRegex(
            ShotPlanningContractError, "七阶段提示合同"
        ):
            build_local_planner_prompt(request)

    def test_v8_contract_rejects_stage_order_budget_or_digest_drift(self) -> None:
        _request, contract, _stages = case_values("crying")
        for mutate in (
            lambda value: value["prompt_strategy"]["stages"].reverse(),
            lambda value: value["resource_budget"].update(
                {"maximum_model_calls": 20}
            ),
            lambda value: value["prompt_strategy"].update(
                {"compiler_contract_sha256": "0" * 64}
            ),
        ):
            mutated = deepcopy(contract)
            mutate(mutated)
            with self.assertRaises(ValueError):
                validate_trial_contract(mutated)

    def test_v8_prompts_use_exact_generalized_fields_and_hide_held_out_terms(self) -> None:
        request, _contract, _stages = case_values("smile")
        for stage in ("composition", "performance", "lighting", "continuity"):
            prompt = build_local_planner_generalized_stage_prompt(request, stage)
            body = json.loads(prompt["user"])
            self.assertEqual(
                prompt["prompt_contract_version"],
                "local-shot-planner-generalized-observability.v8",
            )
            self.assertEqual(
                set(body["stage_contract"]["required_keys"]),
                set(GENERALIZED_STAGE_REQUIRED_KEYS[stage]),
            )
            self.assertNotIn("required_performance_terms", prompt["user"])
            self.assertNotIn("forbidden_output_terms", prompt["user"])
        core_prompt = build_local_planner_generalized_stage_prompt(
            request, "shot_core"
        )
        self.assertNotIn("required_performance_terms", core_prompt["user"])
        self.assertNotIn("forbidden_output_terms", core_prompt["user"])

    def test_generalized_stage_validation_uses_v2_keys_and_values(self) -> None:
        request, _contract, stages = case_values("smile")
        self.assertEqual(
            observe_stage_payload(
                "performance",
                stages["performance"],
                request=request,
                compiler_version=GENERALIZED_OBSERVABILITY_COMPILER_VERSION,
            ),
            [],
        )
        old_keys = {
            "eye_state": "EYES_RELAXED",
            "tear_state": "NO_VISIBLE_TEARS",
            "mouth_state": "MOUTH_SMILING",
            "expression_intensity": "NEUTRAL",
        }
        observations = observe_stage_payload(
            "performance",
            old_keys,
            request=request,
            compiler_version=GENERALIZED_OBSERVABILITY_COMPILER_VERSION,
        )
        self.assertIn("STAGE_KEYS_MISMATCH", {item["code"] for item in observations})

    def test_cross_stage_rules_reject_tear_pollution_and_motion_mismatch(self) -> None:
        _request, _contract, smile = case_values("smile")
        smile["lighting"]["highlight_state"] = "TEAR_HIGHLIGHT_VISIBLE"
        codes = {
            item["code"] for item in observe_generalized_stage_consistency(smile)
        }
        self.assertIn("GENERALIZED_TEAR_HIGHLIGHT_WITHOUT_VISIBLE_TEARS", codes)

        _request, _contract, bicycle = case_values("bicycle")
        bicycle["continuity"]["exit_subject_state"] = "CRYING_CONTINUES"
        codes = {
            item["code"] for item in observe_generalized_stage_consistency(bicycle)
        }
        self.assertIn("GENERALIZED_LEFT_TO_RIGHT_CONTINUITY_MISMATCH", codes)
        self.assertIn("GENERALIZED_ACTION_CONTINUITY_MISMATCH", codes)

    def test_non_string_enum_is_recorded_without_crashing_cross_stage_checks(self) -> None:
        request, contract, stages = case_values("crying")
        invalid_stages = deepcopy(stages)
        invalid_stages["performance"]["visible_action_state"] = ["CRYING"]
        observations = observe_stage_payload(
            "performance",
            invalid_stages["performance"],
            request=request,
            compiler_version=GENERALIZED_OBSERVABILITY_COMPILER_VERSION,
        )
        self.assertIn(
            "STAGE_VALUE_NOT_NONEMPTY_STRING",
            {item["code"] for item in observations},
        )
        observe_generalized_stage_consistency(invalid_stages)

        def generate(prompt: dict, _call_index: int) -> str:
            return json.dumps(invalid_stages[prompt["stage"]], ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            summary = run_trial(
                contract,
                request,
                "LOCAL-V8-NON-STRING-TEST",
                Path(temporary) / "LOCAL-V8-NON-STRING-TEST",
                generate,
            )
            self.assertEqual(summary["model_call_count_observed"], 21)
            self.assertEqual(summary["structurally_observable_run_count"], 0)
            self.assertEqual(
                [run["cross_stage_observation_count"] for run in summary["runs"]],
                [0, 0, 0],
            )

    def test_three_distinct_cases_compile_to_observable_v2_proposals(self) -> None:
        compiled_texts: dict[str, str] = {}
        for case_name in CASE_FILES:
            request, contract, stages = case_values(case_name)
            self.assertEqual(observe_generalized_stage_consistency(stages), [])
            proposal = compile_generalized_stages_to_proposal(
                stages,
                request,
                contract,
                proposal_id=f"PROPOSAL-{case_name.upper()}-001",
                run_id=f"RUN-{case_name.upper()}-001",
            )
            report = observe_proposal(request, proposal)
            self.assertEqual(report["blocking_observation_count"], 0)
            self.assertEqual(proposal["schema_version"], "shot-planning-proposal.v2")
            self.assertIn("performance", proposal["shots"][0])
            self.assertNotIn("emotion", proposal["shots"][0])
            compiled_texts[case_name] = json.dumps(
                proposal["shots"][0], ensure_ascii=False
            )
        self.assertNotIn("泪", compiled_texts["smile"])
        self.assertNotIn("泪", compiled_texts["bicycle"])
        self.assertNotIn("面部", compiled_texts["bicycle"])
        self.assertIn("微笑", compiled_texts["smile"])
        self.assertIn("自行车", compiled_texts["bicycle"])

    def test_v2_proposal_rejects_legacy_prompt_contract(self) -> None:
        request, contract, stages = case_values("crying")
        proposal = compile_generalized_stages_to_proposal(
            stages,
            request,
            contract,
            proposal_id="PROPOSAL-V2-PROMPT-BINDING-001",
            run_id="RUN-V2-PROMPT-BINDING-001",
        )
        proposal["planner"]["prompt_contract_version"] = "local-shot-planner.v1"
        report = observe_proposal(request, proposal)
        self.assertIn(
            "PROMPT_CONTRACT_VERSION_MISMATCH",
            {item["code"] for item in report["observations"]},
        )

    def test_generalized_stability_includes_context_and_beat_fields(self) -> None:
        _request, _contract, crying = case_values("crying")
        changed = deepcopy(crying)
        changed["scene_context"]["time"] = "NIGHT"
        observation = observe_generalized_semantic_stability(
            [crying, crying, changed]
        )
        self.assertEqual(
            observation["field_consistency"]["scene_context.time"][
                "largest_group_ratio"
            ],
            0.6667,
        )
        self.assertIn("beat_purpose.purpose", observation["field_consistency"])

    def test_v8_runner_makes_exactly_twenty_one_calls_and_verifies_evidence(self) -> None:
        request, contract, stages = case_values("crying")
        calls: list[tuple[int, str]] = []

        def generate(prompt: dict, call_index: int) -> str:
            calls.append((call_index, prompt["stage"]))
            return json.dumps(stages[prompt["stage"]], ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-V8-GENERALIZED-TEST"
            summary = run_trial(
                contract,
                request,
                "LOCAL-V8-GENERALIZED-TEST",
                evidence_dir,
                generate,
            )
            self.assertEqual(len(calls), 21)
            self.assertEqual(summary["structurally_observable_run_count"], 3)
            self.assertEqual(
                summary["largest_exact_controlled_semantic_group_ratio"], 1.0
            )
            self.assertEqual(
                [run["cross_stage_observation_count"] for run in summary["runs"]],
                [0, 0, 0],
            )
            self.assertTrue(
                (evidence_dir / "cross_stage_observation_003.json").is_file()
            )
            write_json(evidence_dir / "environment.json", {"test_environment": True})
            write_manifest(evidence_dir)
            verification = verify_evidence(
                evidence_dir, allow_test_environment=True
            )
            self.assertEqual(
                verification["package_integrity_observation"],
                "COMPLETE_AND_DIGEST_MATCHED",
            )

    def test_v9_encodes_candidates_as_scalar_choice_strings(self) -> None:
        request, _contract, _stages = case_values("crying")
        for stage in (
            "scene_context",
            "beat_purpose",
            "shot_core",
            "composition",
            "performance",
            "lighting",
            "continuity",
        ):
            prompt = build_local_planner_scalar_choice_stage_prompt(request, stage)
            body = json.loads(prompt["user"])
            stage_contract = body["stage_contract"]
            self.assertEqual(
                prompt["prompt_contract_version"],
                "local-shot-planner-scalar-choices.v9",
            )
            self.assertNotIn("allowed_values", stage_contract)
            self.assertEqual(
                stage_contract["value_type"], "JSON_STRING_SCALAR_ONLY"
            )
            self.assertTrue(
                all(
                    isinstance(value, str)
                    for value in stage_contract["allowed_scalar_choices"].values()
                )
            )
            self.assertIn("严禁输出数组", prompt["system"])

    def test_v9_contract_and_fake_runner_keep_v8_compiler_contract(self) -> None:
        request, _v8_contract, stages = case_values("crying")
        contract = load(
            EXPERIMENT_ROOT / "qwen3_0_6b_scalar_choice_crying_trial_v9.json"
        )
        validate_trial_contract(contract)
        self.assertEqual(
            contract["prompt_strategy"]["compiler_contract_sha256"],
            generalized_compiler_contract_sha256(),
        )
        prompts: list[dict] = []

        def generate(prompt: dict, _call_index: int) -> str:
            prompts.append(prompt)
            return json.dumps(stages[prompt["stage"]], ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-V9-SCALAR-TEST"
            summary = run_trial(
                contract,
                request,
                "LOCAL-V9-SCALAR-TEST",
                evidence_dir,
                generate,
            )
            self.assertEqual(len(prompts), 21)
            self.assertEqual(summary["structurally_observable_run_count"], 3)
            self.assertTrue(
                all(
                    prompt["prompt_contract_version"]
                    == "local-shot-planner-scalar-choices.v9"
                    for prompt in prompts
                )
            )
            write_json(evidence_dir / "environment.json", {"test_environment": True})
            write_manifest(evidence_dir)
            self.assertEqual(
                verify_evidence(
                    evidence_dir, allow_test_environment=True
                )["package_integrity_observation"],
                "COMPLETE_AND_DIGEST_MATCHED",
            )
            self.assertFalse((evidence_dir / "choice_glossary_contract.json").exists())
            prompt_path = evidence_dir / "prompt_001_shot_core.json"
            injected_prompt = load(prompt_path)
            injected_prompt["held_out_expected_answer_injected"] = "CLOSE_UP"
            write_json(prompt_path, injected_prompt)
            write_manifest(evidence_dir)
            with self.assertRaisesRegex(
                LocalTrialError, "阶段提示与确定性固定合同不一致"
            ):
                verify_evidence(evidence_dir, allow_test_environment=True)

    def test_v10_prompt_adds_candidate_glosses_without_held_out_observation(self) -> None:
        request, _contract, _stages = case_values("bicycle")
        for stage in (
            "scene_context",
            "beat_purpose",
            "shot_core",
            "composition",
            "performance",
            "lighting",
            "continuity",
        ):
            prompt = build_local_planner_semantic_gloss_stage_prompt(request, stage)
            body = json.loads(prompt["user"])
            stage_contract = body["stage_contract"]
            self.assertEqual(
                prompt["prompt_contract_version"],
                "local-shot-planner-semantic-gloss.v10",
            )
            self.assertEqual(
                set(stage_contract["choice_glossary"]),
                set(stage_contract["allowed_scalar_choices"]),
            )
            for field, encoded in stage_contract["allowed_scalar_choices"].items():
                self.assertEqual(
                    set(stage_contract["choice_glossary"][field]),
                    {item.strip() for item in encoded.split("|")},
                )
            self.assertNotIn("held_out_observation", prompt["user"])
            self.assertNotIn("expected_controlled_values", prompt["user"])
            self.assertNotIn("required_compiled_terms", prompt["user"])
            self.assertNotIn("forbidden_output_terms", prompt["user"])
            self.assertIn("主体的运动方向不是相机运动方向", prompt["system"])

    def test_v10_glossary_covers_every_global_allowed_token_and_fails_closed(self) -> None:
        stage_values = {
            "scene_context": TOKENIZED_CONTEXT_ALLOWED_VALUES["scene_context"],
            "beat_purpose": {
                "purpose": STRUCTURED_STAGE_ALLOWED_VALUES["shot_core"][
                    "primary_purpose"
                ]
            },
            "shot_core": STRUCTURED_STAGE_ALLOWED_VALUES["shot_core"],
            **{
                stage: fields
                for stage, fields in GENERALIZED_STAGE_ALLOWED_VALUES.items()
                if stage != "shot_core"
            },
        }
        for stage, fields in stage_values.items():
            encoded = {
                field: " | ".join(values) for field, values in fields.items()
            }
            glossary = choice_glossary_for_stage(stage, encoded)
            for field, values in fields.items():
                self.assertEqual(set(glossary[field]), set(values))
                self.assertTrue(
                    all(
                        isinstance(description, str)
                        and description
                        and description != token
                        for token, description in glossary[field].items()
                    )
                )
        with self.assertRaisesRegex(ValueError, "候选释义合同缺少"):
            choice_glossary_for_stage(
                "shot_core", {"framing": "CLOSE_UP | UNKNOWN_FRAMING"}
            )

    def test_v10_contract_rejects_glossary_or_disambiguation_drift(self) -> None:
        contract = load(
            EXPERIMENT_ROOT / "qwen3_0_6b_semantic_gloss_crying_trial_v10.json"
        )
        validate_trial_contract(contract)
        self.assertEqual(
            contract["prompt_strategy"]["choice_glossary_contract_version"],
            SEMANTIC_CHOICE_GLOSSARY_VERSION,
        )
        for key, value in (
            ("choice_glossary_contract_sha256", "0" * 64),
            ("semantic_choice_glossary_enforced", False),
            ("subject_camera_direction_disambiguation", False),
        ):
            mutated = deepcopy(contract)
            mutated["prompt_strategy"][key] = value
            with self.assertRaises(ValueError):
                validate_trial_contract(mutated)

    def test_v10_runner_retains_and_verifies_glossary_contract(self) -> None:
        request, _v8_contract, stages = case_values("crying")
        contract = load(
            EXPERIMENT_ROOT / "qwen3_0_6b_semantic_gloss_crying_trial_v10.json"
        )
        prompts: list[dict] = []

        def generate(prompt: dict, _call_index: int) -> str:
            prompts.append(prompt)
            return json.dumps(stages[prompt["stage"]], ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-V10-GLOSS-TEST"
            summary = run_trial(
                contract,
                request,
                "LOCAL-V10-GLOSS-TEST",
                evidence_dir,
                generate,
            )
            self.assertEqual(len(prompts), 21)
            self.assertEqual(summary["structurally_observable_run_count"], 3)
            self.assertTrue(
                all(
                    prompt["prompt_contract_version"]
                    == "local-shot-planner-semantic-gloss.v10"
                    for prompt in prompts
                )
            )
            glossary_path = evidence_dir / "choice_glossary_contract.json"
            self.assertTrue(glossary_path.is_file())
            self.assertEqual(
                load(glossary_path)["schema_version"],
                SEMANTIC_CHOICE_GLOSSARY_VERSION,
            )
            write_json(evidence_dir / "environment.json", {"test_environment": True})
            write_manifest(evidence_dir)
            self.assertEqual(
                verify_evidence(
                    evidence_dir, allow_test_environment=True
                )["package_integrity_observation"],
                "COMPLETE_AND_DIGEST_MATCHED",
            )
            prompt_path = evidence_dir / "prompt_001_shot_core.json"
            tampered_prompt = load(prompt_path)
            prompt_body = json.loads(tampered_prompt["user"])
            del prompt_body["stage_contract"]["choice_glossary"]
            tampered_prompt["user"] = json.dumps(
                prompt_body, ensure_ascii=False, sort_keys=True
            )
            write_json(prompt_path, tampered_prompt)
            write_manifest(evidence_dir)
            with self.assertRaisesRegex(
                LocalTrialError,
                "阶段提示与确定性固定合同不一致",
            ):
                verify_evidence(evidence_dir, allow_test_environment=True)

    def test_v11_contracts_and_prompts_bind_residual_field_ownership(self) -> None:
        expected_locked_counts = {"crying": 9, "smile": 11, "bicycle": 9}
        for case_name, contract_name in V11_CASE_FILES.items():
            request, _v8_contract, _stages = case_values(case_name)
            contract = validate_trial_contract(load(EXPERIMENT_ROOT / contract_name))
            validate_request_binding(
                contract,
                request,
                contract["request_binding"]["request_file"],
            )
            self.assertEqual(contract["schema_version"], "local-shot-planner-trial.v11")
            self.assertEqual(
                contract["prompt_strategy"]["source_fact_extractor_contract_sha256"],
                source_fact_extractor_contract_sha256(
                    SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V1
                ),
            )
            self.assertEqual(
                contract["prompt_strategy"]["hybrid_merge_contract_sha256"],
                hybrid_merge_contract_sha256(),
            )
            extraction = extract_source_facts(
                request,
                contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V1,
            )
            self.assertEqual(
                len(extraction["locked_fields"]), expected_locked_counts[case_name]
            )
            for stage in contract["prompt_strategy"]["stages"]:
                prompt = build_local_planner_hybrid_stage_prompt(request, stage)
                body = json.loads(prompt["user"])
                required = set(body["stage_contract"]["required_keys"])
                locked = set(body["input"]["locked_field_values"])
                self.assertTrue(required.isdisjoint(locked))
                self.assertEqual(
                    set(body["stage_contract"]["allowed_scalar_choices"]), required
                )
                self.assertEqual(set(body["stage_contract"]["choice_glossary"]), required)
                self.assertFalse(body["input"]["held_out_observation_used"])
                self.assertNotIn("expected_controlled_values", prompt["user"])

    def test_v11_runner_merges_residual_payload_and_recomputes_evidence(self) -> None:
        request, _v8_contract, stages = case_values("smile")
        contract = load(
            EXPERIMENT_ROOT / "qwen3_0_6b_hybrid_source_facts_smile_trial_v11.json"
        )
        prompts: list[dict] = []

        def generate(prompt: dict, _call_index: int) -> str:
            prompts.append(prompt)
            body = json.loads(prompt["user"])
            return json.dumps(
                {
                    field: stages[prompt["stage"]][field]
                    for field in body["stage_contract"]["required_keys"]
                },
                ensure_ascii=False,
            )

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-V11-HYBRID-TEST"
            with self.assertRaisesRegex(
                LocalTrialError,
                "混合试验直接调用必须提供请求相对路径",
            ):
                run_trial(
                    contract,
                    request,
                    "LOCAL-V11-HYBRID-TEST",
                    evidence_dir,
                    generate,
                )
            self.assertFalse(evidence_dir.exists())
            self.assertEqual(prompts, [])
            with self.assertRaisesRegex(
                LocalTrialError,
                "规划请求路径与固定合同不一致",
            ):
                run_trial(
                    contract,
                    request,
                    "LOCAL-V11-HYBRID-TEST",
                    evidence_dir,
                    generate,
                    request_relative_path="experiments/shot_planning/wrong.json",
                )
            self.assertFalse(evidence_dir.exists())
            self.assertEqual(prompts, [])
            summary = run_trial(
                contract,
                request,
                "LOCAL-V11-HYBRID-TEST",
                evidence_dir,
                generate,
                request_relative_path=contract["request_binding"]["request_file"],
            )
            self.assertEqual(len(prompts), 21)
            self.assertEqual(summary["structurally_observable_run_count"], 3)
            self.assertTrue((evidence_dir / "source_fact_extraction.json").is_file())
            self.assertTrue((evidence_dir / "field_ownership.json").is_file())
            self.assertEqual(
                len(list(evidence_dir.glob("model_residual_payload_*.json"))), 21
            )
            self.assertEqual(
                len(list(evidence_dir.glob("merge_observation_*.json"))), 21
            )
            merged_core = load(evidence_dir / "payload_001_shot_core.json")
            residual_core = load(
                evidence_dir / "model_residual_payload_001_shot_core.json"
            )
            self.assertEqual(residual_core, {"primary_purpose": "EMPHASIZE_EMOTION"})
            self.assertEqual(merged_core["framing"], "MEDIUM")
            self.assertEqual(merged_core["action_description"], request["source_text"])
            write_json(evidence_dir / "environment.json", {"test_environment": True})
            write_manifest(evidence_dir)
            with self.assertRaisesRegex(LocalTrialError, "不接受测试环境占位"):
                verify_evidence(evidence_dir)
            self.assertEqual(
                verify_evidence(
                    evidence_dir, allow_test_environment=True
                )["package_integrity_observation"],
                "COMPLETE_AND_DIGEST_MATCHED",
            )
            unexpected_path = evidence_dir / "unexpected-v11-artifact.json"
            write_json(unexpected_path, {"unexpected": True})
            write_manifest(evidence_dir)
            with self.assertRaisesRegex(
                LocalTrialError,
                "混合证据包文件集合与固定合同不一致",
            ):
                verify_evidence(evidence_dir, allow_test_environment=True)
            unexpected_path.unlink()
            write_manifest(evidence_dir)
            extraction_path = evidence_dir / "source_fact_extraction.json"
            tampered = load(extraction_path)
            tampered["locked_fields"]["shot_core.framing"] = "CLOSE_UP"
            write_json(extraction_path, tampered)
            write_manifest(evidence_dir)
            with self.assertRaisesRegex(LocalTrialError, "原句事实提取无法"):
                verify_evidence(evidence_dir, allow_test_environment=True)

    def test_v11_source_fact_conflict_fails_before_evidence_side_effects(self) -> None:
        request, _v8_contract, _stages = case_values("smile")
        request = deepcopy(request)
        request["source_text"] = "固定相机，相机向右摇摄"
        contract = load(
            EXPERIMENT_ROOT / "qwen3_0_6b_hybrid_source_facts_smile_trial_v11.json"
        )
        contract["request_binding"]["request_sha256"] = canonical_sha256(request)
        model_call_count = 0

        def generate(_prompt: dict, _call_index: int) -> str:
            nonlocal model_call_count
            model_call_count += 1
            return "{}"

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-V11-CONFLICT-TEST"
            with self.assertRaisesRegex(
                LocalTrialError,
                "原句事实提取存在阻断问题",
            ):
                run_trial(
                    contract,
                    request,
                    "LOCAL-V11-CONFLICT-TEST",
                    evidence_dir,
                    generate,
                    request_relative_path=contract["request_binding"][
                        "request_file"
                    ],
                )
            self.assertFalse(evidence_dir.exists())
            self.assertEqual(model_call_count, 0)

    def test_v12_binds_guarded_extractor_and_recomputes_fake_evidence(self) -> None:
        request, _v8_contract, stages = case_values("smile")
        contract = validate_trial_contract(
            load(EXPERIMENT_ROOT / V12_SMILE_TRIAL_FILE)
        )
        self.assertEqual(contract["schema_version"], "local-shot-planner-trial.v12")
        self.assertEqual(
            contract["prompt_strategy"]["source_fact_extractor_contract_sha256"],
            source_fact_extractor_contract_sha256(
                SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2
            ),
        )
        prompt = build_local_planner_guarded_source_fact_stage_prompt(
            request,
            "shot_core",
        )
        self.assertEqual(
            prompt["prompt_contract_version"],
            PLANNER_GUARDED_SOURCE_FACT_PROMPT_CONTRACT_VERSION,
        )

        v11_contract = load(
            EXPERIMENT_ROOT / V11_CASE_FILES["smile"]
        )
        v11_contract["prompt_strategy"][
            "source_fact_extractor_contract_version"
        ] = SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2
        v11_contract["prompt_strategy"][
            "source_fact_extractor_contract_sha256"
        ] = source_fact_extractor_contract_sha256(
            SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2
        )
        with self.assertRaisesRegex(ValueError, "第十一版提示策略"):
            validate_trial_contract(v11_contract)

        v12_with_v1 = deepcopy(contract)
        v12_with_v1["prompt_strategy"][
            "source_fact_extractor_contract_version"
        ] = SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V1
        v12_with_v1["prompt_strategy"][
            "source_fact_extractor_contract_sha256"
        ] = source_fact_extractor_contract_sha256(
            SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V1
        )
        with self.assertRaisesRegex(ValueError, "第十二版提示策略"):
            validate_trial_contract(v12_with_v1)

        def generate(stage_prompt: dict, _call_index: int) -> str:
            body = json.loads(stage_prompt["user"])
            return json.dumps(
                {
                    field: stages[stage_prompt["stage"]][field]
                    for field in body["stage_contract"]["required_keys"]
                },
                ensure_ascii=False,
            )

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-V12-GUARDED-TEST"
            summary = run_trial(
                contract,
                request,
                "LOCAL-V12-GUARDED-TEST",
                evidence_dir,
                generate,
                request_relative_path=contract["request_binding"]["request_file"],
            )
            self.assertEqual(summary["model_call_count_observed"], 21)
            self.assertEqual(
                load(evidence_dir / "source_fact_extraction.json")["extractor"][
                    "contract_version"
                ],
                SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
            )
            self.assertTrue(
                load(evidence_dir / "source_fact_extraction.json")[
                    "match_decisions"
                ]
            )
            write_json(evidence_dir / "environment.json", {"test_environment": True})
            write_manifest(evidence_dir)
            self.assertEqual(
                verify_evidence(
                    evidence_dir,
                    allow_test_environment=True,
                )["package_integrity_observation"],
                "COMPLETE_AND_DIGEST_MATCHED",
            )

        invalid_call_count = 0

        def generate_one_non_object(
            stage_prompt: dict,
            call_index: int,
        ) -> str:
            nonlocal invalid_call_count
            invalid_call_count += 1
            if invalid_call_count == 1:
                return "[]"
            return generate(stage_prompt, call_index)

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-V12-NON-OBJECT-TEST"
            run_trial(
                contract,
                request,
                "LOCAL-V12-NON-OBJECT-TEST",
                evidence_dir,
                generate_one_non_object,
                request_relative_path=contract["request_binding"]["request_file"],
            )
            self.assertFalse(
                (evidence_dir / "model_residual_payload_001_scene_context.json").exists()
            )
            self.assertFalse(
                (evidence_dir / "payload_001_scene_context.json").exists()
            )
            self.assertFalse((evidence_dir / "proposal_001.json").exists())
            write_json(evidence_dir / "environment.json", {"test_environment": True})
            write_manifest(evidence_dir)
            self.assertEqual(
                verify_evidence(
                    evidence_dir,
                    allow_test_environment=True,
                )["package_integrity_observation"],
                "COMPLETE_AND_DIGEST_MATCHED",
            )

    def test_v12_negation_blocks_before_evidence_or_model_call(self) -> None:
        request, _v8_contract, _stages = case_values("smile")
        request = deepcopy(request)
        request["source_text"] = "演员并非微笑"
        contract = load(EXPERIMENT_ROOT / V12_SMILE_TRIAL_FILE)
        contract["request_binding"]["request_sha256"] = canonical_sha256(request)
        model_call_count = 0

        def generate(_prompt: dict, _call_index: int) -> str:
            nonlocal model_call_count
            model_call_count += 1
            return "{}"

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-V12-NEGATION-TEST"
            with self.assertRaisesRegex(
                LocalTrialError,
                "原句事实提取存在阻断问题",
            ):
                run_trial(
                    contract,
                    request,
                    "LOCAL-V12-NEGATION-TEST",
                    evidence_dir,
                    generate,
                    request_relative_path=contract["request_binding"][
                        "request_file"
                    ],
                )
            self.assertFalse(evidence_dir.exists())
            self.assertEqual(model_call_count, 0)


if __name__ == "__main__":
    unittest.main()
