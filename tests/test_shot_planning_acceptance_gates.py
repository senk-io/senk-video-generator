from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

from shot_planning.contracts import validate_request
from shot_planning.diagnosis_report import (
    REQUIRED_DIAGNOSIS_REPORT_FIELDS,
    DiagnosisReportError,
    validate_diagnosis_report,
)
from shot_planning.pre_model_guard import (
    BLOCK_CATEGORIES,
    PreModelGuardError,
    evaluate_adversarial_set,
    evaluate_pre_model_guard,
)
from shot_planning.prompting import build_local_planner_guarded_source_fact_stage_prompt
from shot_planning.source_facts import (
    SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V1,
    SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
    source_fact_extractor_contract_sha256,
)


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_ROOT = ROOT / "experiments" / "shot_planning"
ADVERSARIAL_SET = EXPERIMENT_ROOT / "adversarial_pre_model_guard_set_v1.json"
POSITIVE_REQUESTS = {
    "crying": "generalized_child_crying_closeup_request_v1.json",
    "smile": "generalized_actor_smile_medium_request_v1.json",
    "bicycle": "generalized_bicycle_left_to_right_wide_request_v1.json",
}
HELD_OUT_REQUESTS = (
    "held_out_library_reader_medium_request_v1.json",
    "held_out_snow_courtyard_cat_wide_request_v1.json",
)
MODEL_MODULE_NAMES = ("torch", "transformers", "safetensors")


def load_json(relative_name: str) -> dict:
    return json.loads((EXPERIMENT_ROOT / relative_name).read_text(encoding="utf-8"))


class ShotPlanningAcceptanceGatesTest(unittest.TestCase):
    def test_v2_extractor_contract_sha256_remains_frozen(self) -> None:
        self.assertEqual(
            source_fact_extractor_contract_sha256(
                SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V1
            ),
            "e7e80ae9c924c933e0b95c6ee14b0c93f53c969bde6e218826ed8242261ea0f1",
        )
        self.assertEqual(
            source_fact_extractor_contract_sha256(
                SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2
            ),
            "b03b96b9d2d82f36e36677d8ccb0d2392c1368f92c2040b74d6d466dbfc9e16a",
        )

    def test_adversarial_set_covers_six_frozen_categories_and_at_least_20_items(
        self,
    ) -> None:
        payload = json.loads(ADVERSARIAL_SET.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(payload["items"]), 20)
        self.assertEqual(set(payload["categories"]), set(BLOCK_CATEGORIES))
        observed = {item["expected_block_category"] for item in payload["items"]}
        self.assertEqual(observed, set(BLOCK_CATEGORIES))
        self.assertFalse(payload["real_local_suite_executed"])
        self.assertFalse(payload["counts_toward_planning_gate"])
        for item in payload["items"]:
            self.assertTrue(item["source_text"].strip())
            self.assertIn(item["expected_block_category"], BLOCK_CATEGORIES)
            self.assertTrue((EXPERIMENT_ROOT / item["request_template"]).is_file())

    def test_fixed_adversarial_set_intercepts_20_of_20_without_model_weights(
        self,
    ) -> None:
        summary = evaluate_adversarial_set(
            ADVERSARIAL_SET,
            experiment_root=EXPERIMENT_ROOT,
        )
        self.assertEqual(summary["item_count"], 24)
        self.assertEqual(summary["intercepted_count"], 24)
        self.assertEqual(summary["expected_category_hit_count"], 24)
        self.assertEqual(summary["missed_ids"], [])
        self.assertFalse(summary["model_weight_loaded"])
        self.assertFalse(summary["formal_shot_spec_created"])
        self.assertFalse(summary["formal_quality_acceptance_created"])
        for result in summary["results"]:
            report = result["report"]
            validate_diagnosis_report(report)
            self.assertFalse(report["model_invoked"])
            self.assertFalse(report["model_invocation_allowed"])
            self.assertFalse(report["formal_shot_spec_created"])
            for field in REQUIRED_DIAGNOSIS_REPORT_FIELDS:
                self.assertIn(field, report)
            self.assertTrue(report["blocks"])
            self.assertTrue(report["cannot_approve_reasons"])
            self.assertIn(result["expected_block_category"], result["observed_categories"])
        for module_name in MODEL_MODULE_NAMES:
            self.assertNotIn(module_name, sys.modules)

    def test_adversarial_block_path_rejects_guarded_prompt_construction(self) -> None:
        request = load_json(POSITIVE_REQUESTS["smile"])
        request["source_text"] = "不要使用特写镜头"
        with self.assertRaises(PreModelGuardError) as raised:
            build_local_planner_guarded_source_fact_stage_prompt(request, "shot_core")
        report = raised.exception.report
        validate_diagnosis_report(report)
        self.assertFalse(report["model_invocation_allowed"])
        self.assertIn(
            "NEGATION_WITHOUT_REPLACEMENT",
            {item["category"] for item in report["blocks"]},
        )

    def test_positive_suite_requests_remain_allowed_to_reach_v12_prompt(self) -> None:
        for name, filename in POSITIVE_REQUESTS.items():
            request = load_json(filename)
            report = evaluate_pre_model_guard(request)
            self.assertTrue(report["model_invocation_allowed"], name)
            self.assertEqual(report["blocks"], [], name)
            prompt = build_local_planner_guarded_source_fact_stage_prompt(
                request, "shot_core"
            )
            self.assertEqual(
                prompt["prompt_contract_version"],
                "local-shot-planner-guarded-source-facts.v12",
            )

    def test_missing_diagnosis_fields_fail_closed(self) -> None:
        request = load_json(POSITIVE_REQUESTS["smile"])
        request["source_text"] = "演员从未微笑"
        report = evaluate_pre_model_guard(request)
        for field in REQUIRED_DIAGNOSIS_REPORT_FIELDS:
            mutated = deepcopy(report)
            del mutated[field]
            with self.assertRaises(DiagnosisReportError):
                validate_diagnosis_report(mutated)
        empty_reasons = deepcopy(report)
        empty_reasons["cannot_approve_reasons"] = []
        with self.assertRaises(DiagnosisReportError):
            validate_diagnosis_report(empty_reasons)
        unblocking = deepcopy(report)
        unblocking["blocks"][0]["blocking"] = False
        with self.assertRaises(DiagnosisReportError):
            validate_diagnosis_report(unblocking)

    def test_held_out_placeholders_are_valid_requests_and_do_not_count(self) -> None:
        for filename in HELD_OUT_REQUESTS:
            payload = load_json(filename)
            self.assertTrue(payload["held_out_observation_input"])
            self.assertFalse(payload["real_local_suite_executed"])
            self.assertFalse(payload["counts_toward_acceptance_gates"])
            self.assertIn("未跑真实套件", payload["acceptance_gate_note"])
            self.assertIn("不计入本刀过线", payload["acceptance_gate_note"])
            request = validate_request(payload)
            self.assertEqual(request["status"], "DRAFT_NON_AUTHORITATIVE")


if __name__ == "__main__":
    unittest.main()
