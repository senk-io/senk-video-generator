from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from shot_planning.contracts import canonical_sha256
from shot_planning.evaluation_suite import (
    load_suite_cases,
    run_suite,
    validate_suite_contract,
    verify_suite_evidence,
    write_suite_manifest,
)
from shot_planning.local_trial import LocalTrialError, write_json, write_manifest
from shot_planning.source_facts import SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2
from tests.test_generalized_shot_planner_trial import CASE_FILES, case_values


ROOT = Path(__file__).resolve().parents[1]
SUITE_PATH = (
    ROOT
    / "experiments"
    / "shot_planning"
    / "qwen3_0_6b_generalization_suite_v1.json"
)
SEMANTIC_GLOSS_SUITE_PATH = (
    ROOT
    / "experiments"
    / "shot_planning"
    / "qwen3_0_6b_semantic_gloss_generalization_suite_v1.json"
)
HYBRID_SOURCE_FACTS_SUITE_PATH = (
    ROOT
    / "experiments"
    / "shot_planning"
    / "qwen3_0_6b_hybrid_source_facts_generalization_suite_v1.json"
)
GUARDED_SOURCE_FACTS_SUITE_PATH = (
    ROOT
    / "experiments"
    / "shot_planning"
    / "qwen3_0_6b_guarded_source_facts_generalization_suite_v12.json"
)
V12_TRIAL_FILES = {
    "CRY_RAIN_CLOSEUP": "qwen3_0_6b_guarded_source_facts_crying_trial_v12.json",
    "SMILE_INDOOR_MEDIUM": "qwen3_0_6b_guarded_source_facts_smile_trial_v12.json",
    "BICYCLE_LEFT_TO_RIGHT_WIDE": (
        "qwen3_0_6b_guarded_source_facts_bicycle_trial_v12.json"
    ),
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def stage_outputs_by_source() -> dict[str, dict[str, dict[str, str]]]:
    outputs: dict[str, dict[str, dict[str, str]]] = {}
    for case_name in CASE_FILES:
        request, _contract, stages = case_values(case_name)
        outputs[request["source_text"]] = stages
    return outputs


class LocalShotPlannerSuiteTest(unittest.TestCase):
    def setUp(self) -> None:
        self.suite = load(SUITE_PATH)

    def test_suite_contract_binds_three_uniform_v8_cases(self) -> None:
        suite, cases = load_suite_cases(self.suite, ROOT)
        self.assertEqual(len(cases), 3)
        self.assertEqual(suite["resource_budget"]["maximum_model_calls"], 63)
        self.assertEqual(suite["resource_budget"]["maximum_runs"], 9)
        self.assertEqual(
            [loaded["case"]["case_id"] for loaded in cases], suite["case_order"]
        )

    def test_semantic_gloss_suite_binds_three_uniform_v10_cases(self) -> None:
        suite, cases = load_suite_cases(load(SEMANTIC_GLOSS_SUITE_PATH), ROOT)
        self.assertEqual(suite["suite_id"], "LOCAL-SHOT-PLANNER-SEMANTIC-GLOSS-001")
        self.assertEqual(len(cases), 3)
        self.assertEqual(
            {loaded["trial"]["schema_version"] for loaded in cases},
            {"local-shot-planner-trial.v10"},
        )
        self.assertEqual(
            {
                loaded["trial"]["prompt_strategy"]["prompt_contract_version"]
                for loaded in cases
            },
            {"local-shot-planner-semantic-gloss.v10"},
        )

    def test_hybrid_suite_binds_three_uniform_v11_cases(self) -> None:
        suite, cases = load_suite_cases(load(HYBRID_SOURCE_FACTS_SUITE_PATH), ROOT)
        self.assertEqual(
            suite["suite_id"], "LOCAL-SHOT-PLANNER-HYBRID-SOURCE-FACTS-001"
        )
        self.assertEqual(len(cases), 3)
        self.assertEqual(suite["resource_budget"]["maximum_model_calls"], 63)
        self.assertEqual(
            {loaded["trial"]["schema_version"] for loaded in cases},
            {"local-shot-planner-trial.v11"},
        )
        self.assertEqual(
            {
                loaded["trial"]["prompt_strategy"]["prompt_contract_version"]
                for loaded in cases
            },
            {"local-shot-planner-hybrid-source-facts.v11"},
        )

    def test_guarded_suite_binds_three_uniform_v12_cases(self) -> None:
        suite, cases = load_suite_cases(load(GUARDED_SOURCE_FACTS_SUITE_PATH), ROOT)
        self.assertEqual(
            suite["suite_id"], "LOCAL-SHOT-PLANNER-GUARDED-SOURCE-FACTS-001"
        )
        runner_source = (
            ROOT / "tools" / "run_local_shot_planner_suite.py"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "qwen3_0_6b_guarded_source_facts_generalization_suite_v12.json",
            runner_source,
        )
        self.assertNotIn(
            'qwen3_0_6b_generalization_suite_v1.json"\n)',
            runner_source,
        )
        self.assertEqual(len(cases), 3)
        self.assertEqual(suite["resource_budget"]["maximum_model_calls"], 63)
        self.assertEqual(suite["resource_budget"]["maximum_runs"], 9)
        self.assertEqual(suite["resource_budget"]["retry_count"], 0)
        self.assertEqual(suite["methodology_invariants"]["retry_count"], 0)
        self.assertEqual(
            {loaded["trial"]["schema_version"] for loaded in cases},
            {"local-shot-planner-trial.v12"},
        )
        self.assertEqual(
            {
                loaded["trial"]["prompt_strategy"]["prompt_contract_version"]
                for loaded in cases
            },
            {"local-shot-planner-guarded-source-facts.v12"},
        )
        self.assertEqual(
            {
                loaded["trial"]["prompt_strategy"][
                    "source_fact_extractor_contract_version"
                ]
                for loaded in cases
            },
            {SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2},
        )
        self.assertEqual(
            {loaded["trial"]["model"]["revision"] for loaded in cases},
            {"c1899de289a04d12100db370d81485cdf75e47ca"},
        )
        for loaded in cases:
            case_id = loaded["case"]["case_id"]
            trial_path = ROOT / "experiments" / "shot_planning" / V12_TRIAL_FILES[case_id]
            self.assertEqual(
                loaded["case"]["trial_binding"]["trial_contract_file"],
                trial_path.relative_to(ROOT).as_posix(),
            )
            self.assertEqual(
                loaded["case"]["trial_binding"]["trial_contract_sha256"],
                canonical_sha256(load(trial_path)),
            )
            self.assertEqual(
                loaded["case"]["request_binding"]["request_sha256"],
                canonical_sha256(loaded["request"]),
            )
        self.assertEqual(suite["status"], "BOUNDED_NON_AUTHORITATIVE_EVALUATION")
        self.assertIn("formal_shot_spec_creation", suite["non_goals"])
        self.assertIn("formal_quality_acceptance", suite["non_goals"])
        self.assertNotIn("planning_gate_passed", suite)
        self.assertFalse(suite.get("planning_gate_passed", False))
        self.assertEqual(
            [loaded["case"]["case_id"] for loaded in cases],
            ["CRY_RAIN_CLOSEUP", "SMILE_INDOOR_MEDIUM", "BICYCLE_LEFT_TO_RIGHT_WIDE"],
        )
        request_files = {
            loaded["case"]["request_binding"]["request_file"] for loaded in cases
        }
        self.assertTrue(
            all("held_out_" not in path for path in request_files),
            "held-out requests must not enter the 63-call suite",
        )

    def test_suite_rejects_order_path_digest_or_budget_drift(self) -> None:
        mutated = deepcopy(self.suite)
        mutated["case_order"].reverse()
        with self.assertRaisesRegex(ValueError, "固定顺序"):
            validate_suite_contract(mutated)

        mutated = deepcopy(self.suite)
        mutated["cases"][0]["request_binding"]["request_file"] = "../outside.json"
        with self.assertRaisesRegex(ValueError, "越出仓库"):
            load_suite_cases(mutated, ROOT)

        mutated = deepcopy(self.suite)
        mutated["cases"][0]["trial_binding"]["trial_contract_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "试验合同摘要漂移"):
            load_suite_cases(mutated, ROOT)

        mutated = deepcopy(self.suite)
        mutated["resource_budget"]["maximum_model_calls"] = 62
        with self.assertRaisesRegex(ValueError, "资源预算"):
            validate_suite_contract(mutated)

    def test_suite_runs_sixty_three_calls_with_one_shared_model_observation(self) -> None:
        outputs = stage_outputs_by_source()
        calls: list[tuple[int, str, str]] = []

        def generate(prompt: dict, global_call_index: int) -> str:
            body = json.loads(prompt["user"])
            source = body["input"]["source_text"]
            calls.append((global_call_index, source, prompt["stage"]))
            return json.dumps(outputs[source][prompt["stage"]], ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-SUITE-TEST-001"
            observation = run_suite(
                self.suite,
                repo_root=ROOT,
                suite_contract_path=SUITE_PATH,
                runner_path=Path(__file__),
                execution_id="LOCAL-SUITE-TEST-001",
                evidence_dir=evidence_dir,
                generate=generate,
                model_load_count_observed=1,
            )
            self.assertEqual(len(calls), 63)
            self.assertEqual([index for index, _source, _stage in calls], list(range(1, 64)))
            self.assertEqual(observation["run_count_observed"], 9)
            self.assertEqual(observation["held_out_observation_count"], 0)
            self.assertEqual(observation["exact_source_echo_run_count"], 9)
            self.assertEqual(
                observation["cross_case_controlled_fingerprint_groups"], []
            )
            self.assertFalse(observation["formal_decision_created"])
            verification = verify_suite_evidence(evidence_dir)
            self.assertEqual(
                verification["package_integrity_observation"],
                "COMPLETE_AND_DIGEST_MATCHED",
            )

    def test_suite_observes_cross_case_collapse_without_creating_a_verdict(self) -> None:
        crying_request, _contract, crying_stages = case_values("crying")

        def generate(prompt: dict, _global_call_index: int) -> str:
            return json.dumps(crying_stages[prompt["stage"]], ensure_ascii=False)

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-SUITE-COLLAPSE-001"
            observation = run_suite(
                self.suite,
                repo_root=ROOT,
                suite_contract_path=SUITE_PATH,
                runner_path=Path(__file__),
                execution_id="LOCAL-SUITE-COLLAPSE-001",
                evidence_dir=evidence_dir,
                generate=generate,
                model_load_count_observed=1,
            )
            self.assertGreater(observation["held_out_observation_count"], 0)
            self.assertEqual(observation["exact_source_echo_run_count"], 3)
            self.assertTrue(observation["cross_case_controlled_fingerprint_groups"])
            self.assertEqual(
                observation["cross_case_controlled_fingerprint_groups"][0][
                    "distinct_case_count"
                ],
                3,
            )
            self.assertFalse(observation["formal_quality_acceptance_created"])
            self.assertTrue(observation["creative_review_required"])
            self.assertEqual(
                verify_suite_evidence(evidence_dir)[
                    "package_integrity_observation"
                ],
                "COMPLETE_AND_DIGEST_MATCHED",
            )
            self.assertEqual(
                crying_request["source_text"],
                json.loads(
                    (
                        evidence_dir
                        / "cases/001-cry-rain-closeup/planning_request.json"
                    ).read_text(encoding="utf-8")
                )["source_text"],
            )

    def test_suite_detects_child_manifest_regeneration_after_tampering(self) -> None:
        outputs = stage_outputs_by_source()

        def generate(prompt: dict, _global_call_index: int) -> str:
            body = json.loads(prompt["user"])
            return json.dumps(
                outputs[body["input"]["source_text"]][prompt["stage"]],
                ensure_ascii=False,
            )

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-SUITE-TAMPER-001"
            run_suite(
                self.suite,
                repo_root=ROOT,
                suite_contract_path=SUITE_PATH,
                runner_path=Path(__file__),
                execution_id="LOCAL-SUITE-TAMPER-001",
                evidence_dir=evidence_dir,
                generate=generate,
                model_load_count_observed=1,
            )
            child_dir = evidence_dir / "cases/001-cry-rain-closeup"
            raw_path = child_dir / "raw_output_001_scene_context.txt"
            raw_path.write_text(raw_path.read_text(encoding="utf-8") + " ", encoding="utf-8")
            write_manifest(child_dir)
            with self.assertRaisesRegex(LocalTrialError, "子用例清单摘要"):
                verify_suite_evidence(evidence_dir)

    def test_suite_rederives_payload_from_raw_output_after_manifest_rebuild(self) -> None:
        outputs = stage_outputs_by_source()

        def generate(prompt: dict, _global_call_index: int) -> str:
            body = json.loads(prompt["user"])
            return json.dumps(
                outputs[body["input"]["source_text"]][prompt["stage"]],
                ensure_ascii=False,
            )

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-SUITE-DERIVATION-001"
            run_suite(
                self.suite,
                repo_root=ROOT,
                suite_contract_path=SUITE_PATH,
                runner_path=Path(__file__),
                execution_id="LOCAL-SUITE-DERIVATION-001",
                evidence_dir=evidence_dir,
                generate=generate,
                model_load_count_observed=1,
            )
            child_dir = evidence_dir / "cases/001-cry-rain-closeup"
            payload_path = child_dir / "payload_001_shot_core.json"
            payload = load(payload_path)
            payload["framing"] = "WIDE"
            write_json(payload_path, payload)
            write_manifest(child_dir)
            case_index = load(evidence_dir / "case_index.json")
            write_suite_manifest(evidence_dir, case_index)
            with self.assertRaisesRegex(LocalTrialError, "载荷文件无法由原始输出重算"):
                verify_suite_evidence(evidence_dir)

    def test_suite_rejects_environment_boundary_tampering_after_manifest_rebuild(self) -> None:
        outputs = stage_outputs_by_source()

        def generate(prompt: dict, _global_call_index: int) -> str:
            body = json.loads(prompt["user"])
            return json.dumps(
                outputs[body["input"]["source_text"]][prompt["stage"]],
                ensure_ascii=False,
            )

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-SUITE-ENVIRONMENT-001"
            run_suite(
                self.suite,
                repo_root=ROOT,
                suite_contract_path=SUITE_PATH,
                runner_path=Path(__file__),
                execution_id="LOCAL-SUITE-ENVIRONMENT-001",
                evidence_dir=evidence_dir,
                generate=generate,
                model_load_count_observed=1,
            )
            environment_path = evidence_dir / "suite_environment.json"
            environment = load(environment_path)
            environment["remote_inference_used"] = True
            write_json(environment_path, environment)
            case_index = load(evidence_dir / "case_index.json")
            write_suite_manifest(evidence_dir, case_index)
            with self.assertRaisesRegex(LocalTrialError, "套件运行环境"):
                verify_suite_evidence(evidence_dir)

    def test_hybrid_suite_runs_residual_calls_and_detects_extraction_tampering(self) -> None:
        suite = load(HYBRID_SOURCE_FACTS_SUITE_PATH)
        outputs = stage_outputs_by_source()
        calls: list[tuple[int, str, str, tuple[str, ...]]] = []

        def generate(prompt: dict, global_call_index: int) -> str:
            body = json.loads(prompt["user"])
            source = body["input"]["source_text"]
            required = tuple(body["stage_contract"]["required_keys"])
            calls.append((global_call_index, source, prompt["stage"], required))
            return json.dumps(
                {field: outputs[source][prompt["stage"]][field] for field in required},
                ensure_ascii=False,
            )

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-HYBRID-SUITE-TEST-001"
            observation = run_suite(
                suite,
                repo_root=ROOT,
                suite_contract_path=HYBRID_SOURCE_FACTS_SUITE_PATH,
                runner_path=Path(__file__),
                execution_id="LOCAL-HYBRID-SUITE-TEST-001",
                evidence_dir=evidence_dir,
                generate=generate,
                model_load_count_observed=1,
            )
            self.assertEqual(len(calls), 63)
            self.assertEqual([item[0] for item in calls], list(range(1, 64)))
            self.assertTrue(all(item[3] for item in calls))
            self.assertEqual(observation["run_count_observed"], 9)
            self.assertEqual(observation["held_out_observation_count"], 0)
            self.assertEqual(observation["exact_source_echo_run_count"], 9)
            self.assertEqual(observation["automatic_retry_count"], 0)
            expected_locked_counts = [9, 11, 9]
            case_index = load(evidence_dir / "case_index.json")
            for index_item, expected_count in zip(
                case_index, expected_locked_counts, strict=True
            ):
                case_dir = evidence_dir / index_item["evidence_path"]
                ownership = load(case_dir / "field_ownership.json")
                self.assertEqual(len(ownership["locked_fields"]), expected_count)
                self.assertEqual(
                    len(list(case_dir.glob("model_residual_payload_*.json"))), 21
                )
                self.assertEqual(
                    len(list(case_dir.glob("merge_observation_*.json"))), 21
                )
            self.assertEqual(
                verify_suite_evidence(evidence_dir)[
                    "package_integrity_observation"
                ],
                "COMPLETE_AND_DIGEST_MATCHED",
            )

            first_case = evidence_dir / case_index[0]["evidence_path"]
            extraction_path = first_case / "source_fact_extraction.json"
            extraction = load(extraction_path)
            extraction["locked_fields"]["shot_core.framing"] = "WIDE"
            write_json(extraction_path, extraction)
            write_manifest(first_case)
            write_suite_manifest(evidence_dir, case_index)
            with self.assertRaisesRegex(LocalTrialError, "原句事实提取无法"):
                verify_suite_evidence(evidence_dir)

    def test_guarded_suite_runs_residual_calls_without_claiming_planning_gate(
        self,
    ) -> None:
        suite = load(GUARDED_SOURCE_FACTS_SUITE_PATH)
        outputs = stage_outputs_by_source()
        calls: list[tuple[int, str, str, tuple[str, ...]]] = []

        def generate(prompt: dict, global_call_index: int) -> str:
            body = json.loads(prompt["user"])
            source = body["input"]["source_text"]
            required = tuple(body["stage_contract"]["required_keys"])
            calls.append((global_call_index, source, prompt["stage"], required))
            return json.dumps(
                {field: outputs[source][prompt["stage"]][field] for field in required},
                ensure_ascii=False,
            )

        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "LOCAL-GUARDED-SUITE-TEST-001"
            observation = run_suite(
                suite,
                repo_root=ROOT,
                suite_contract_path=GUARDED_SOURCE_FACTS_SUITE_PATH,
                runner_path=Path(__file__),
                execution_id="LOCAL-GUARDED-SUITE-TEST-001",
                evidence_dir=evidence_dir,
                generate=generate,
                model_load_count_observed=1,
            )
            self.assertEqual(len(calls), 63)
            self.assertEqual([item[0] for item in calls], list(range(1, 64)))
            self.assertTrue(all(item[3] for item in calls))
            self.assertEqual(observation["run_count_observed"], 9)
            self.assertEqual(observation["automatic_retry_count"], 0)
            self.assertFalse(observation["formal_shot_spec_created"])
            self.assertFalse(observation["formal_quality_acceptance_created"])
            self.assertFalse(observation["formal_decision_created"])
            self.assertTrue(observation["creative_review_required"])
            case_index = load(evidence_dir / "case_index.json")
            for index_item in case_index:
                case_dir = evidence_dir / index_item["evidence_path"]
                extraction = load(case_dir / "source_fact_extraction.json")
                self.assertEqual(
                    extraction["extractor"]["contract_version"],
                    SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
                )
            verification = verify_suite_evidence(evidence_dir)
            self.assertEqual(
                verification["package_integrity_observation"],
                "COMPLETE_AND_DIGEST_MATCHED",
            )
            self.assertFalse(verification["formal_shot_spec_created"])
            self.assertFalse(verification["formal_quality_acceptance_created"])


if __name__ == "__main__":
    unittest.main()
