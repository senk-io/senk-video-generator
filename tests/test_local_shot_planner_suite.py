from __future__ import annotations

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from shot_planning.evaluation_suite import (
    load_suite_cases,
    run_suite,
    validate_suite_contract,
    verify_suite_evidence,
    write_suite_manifest,
)
from shot_planning.local_trial import LocalTrialError, write_json, write_manifest
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


if __name__ == "__main__":
    unittest.main()
