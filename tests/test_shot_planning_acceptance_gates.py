from __future__ import annotations

import ast
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

from shot_planning.contracts import canonical_sha256, validate_request
from shot_planning.diagnosis_report import (
    REQUIRED_DIAGNOSIS_REPORT_FIELDS,
    DiagnosisReportError,
    validate_diagnosis_report,
)
from shot_planning.evaluation_suite import load_suite_cases
from shot_planning.local_trial import validate_request_binding, validate_trial_contract
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
HELD_OUT_V12_TRIALS = (
    "qwen3_0_6b_guarded_source_facts_held_out_library_reader_trial_v12.json",
    "qwen3_0_6b_guarded_source_facts_held_out_snow_courtyard_cat_trial_v12.json",
)
V12_SUITE = "qwen3_0_6b_guarded_source_facts_generalization_suite_v12.json"
V12_POSITIVE_TRIALS = (
    "qwen3_0_6b_guarded_source_facts_crying_trial_v12.json",
    "qwen3_0_6b_guarded_source_facts_smile_trial_v12.json",
    "qwen3_0_6b_guarded_source_facts_bicycle_trial_v12.json",
)
WEIGHT_LIBRARY_ROOTS = frozenset({"torch", "transformers", "safetensors"})
GUARD_ENTRY_MODULES = (
    ROOT / "shot_planning" / "pre_model_guard.py",
    ROOT / "shot_planning" / "diagnosis_report.py",
)


def load_json(relative_name: str) -> dict:
    return json.loads((EXPERIMENT_ROOT / relative_name).read_text(encoding="utf-8"))


def _weight_library_modules() -> frozenset[str]:
    return frozenset(
        name
        for name in sys.modules
        if name.split(".", 1)[0] in WEIGHT_LIBRARY_ROOTS
    )


def _local_import_targets(node: ast.AST, source_path: Path) -> list[Path]:
    package_dir = source_path.parent
    targets: list[Path] = []
    if isinstance(node, ast.ImportFrom) and node.level:
        base = package_dir
        for _ in range(node.level - 1):
            base = base.parent
        module_name = node.module or ""
        relative = Path(*module_name.split(".")) if module_name else base
        candidate = (base / relative).with_suffix(".py") if module_name else None
        if candidate is not None:
            targets.append(candidate)
        elif node.module is None:
            for alias in node.names:
                targets.append((base / alias.name).with_suffix(".py"))
    elif isinstance(node, ast.ImportFrom) and node.module:
        parts = node.module.split(".")
        if parts[0] == "shot_planning":
            targets.append(ROOT.joinpath(*parts).with_suffix(".py"))
    elif isinstance(node, ast.Import):
        for alias in node.names:
            parts = alias.name.split(".")
            if parts[0] == "shot_planning":
                targets.append(ROOT.joinpath(*parts).with_suffix(".py"))
    return targets


def _absolute_import_roots(source: str) -> set[str]:
    tree = ast.parse(source)
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                roots.add(alias.name.split(".", 1)[0])
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            roots.add(node.module.split(".", 1)[0])
    return roots


def collect_guard_import_roots(entry_paths: tuple[Path, ...]) -> set[str]:
    pending = [path.resolve() for path in entry_paths]
    seen: set[Path] = set()
    roots: set[str] = set()
    while pending:
        path = pending.pop()
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        source = path.read_text(encoding="utf-8")
        roots.update(_absolute_import_roots(source))
        tree = ast.parse(source)
        for node in ast.walk(tree):
            pending.extend(_local_import_targets(node, path))
    return roots


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
        import_roots = collect_guard_import_roots(GUARD_ENTRY_MODULES)
        self.assertTrue({"json", "re", "pathlib"}.issubset(import_roots))
        self.assertTrue(WEIGHT_LIBRARY_ROOTS.isdisjoint(import_roots))
        loaded_before = _weight_library_modules()
        summary = evaluate_adversarial_set(
            ADVERSARIAL_SET,
            experiment_root=EXPERIMENT_ROOT,
        )
        loaded_after = _weight_library_modules()
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
        self.assertEqual(
            loaded_after,
            loaded_before,
            "对抗拦截路径不得新导入 torch/transformers/safetensors",
        )

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

    def test_v12_suite_and_held_out_trials_load_without_claiming_planning_gate(
        self,
    ) -> None:
        suite, cases = load_suite_cases(load_json(V12_SUITE), ROOT)
        self.assertEqual(len(cases), 3)
        self.assertEqual(
            {loaded["trial"]["schema_version"] for loaded in cases},
            {"local-shot-planner-trial.v12"},
        )
        bound_trial_files = {
            loaded["case"]["trial_binding"]["trial_contract_file"].rsplit("/", 1)[-1]
            for loaded in cases
        }
        self.assertEqual(bound_trial_files, set(V12_POSITIVE_TRIALS))
        for filename in V12_POSITIVE_TRIALS:
            trial = validate_trial_contract(load_json(filename))
            self.assertEqual(trial["status"], "BOUNDED_NON_AUTHORITATIVE_TRIAL")
            self.assertIn("formal_shot_spec_creation", trial["non_goals"])
            self.assertNotIn("planning_gate_passed", trial)
        self.assertNotIn("planning_gate_passed", suite)
        self.assertFalse(suite.get("planning_gate_passed", False))
        self.assertEqual(suite["status"], "BOUNDED_NON_AUTHORITATIVE_EVALUATION")

        for filename in HELD_OUT_V12_TRIALS:
            trial = validate_trial_contract(load_json(filename))
            request = validate_request(
                load_json(Path(trial["request_binding"]["request_file"]).name)
            )
            validate_request_binding(
                trial,
                request,
                trial["request_binding"]["request_file"],
            )
            self.assertEqual(
                trial["request_binding"]["request_sha256"],
                canonical_sha256(request),
            )
            self.assertEqual(trial["draft_status"], "DRAFT_NON_AUTHORITATIVE")
            self.assertEqual(request["status"], "DRAFT_NON_AUTHORITATIVE")
            self.assertFalse(trial["counts_toward_acceptance_gates"])
            self.assertFalse(trial["real_local_suite_executed"])
            self.assertFalse(request["counts_toward_acceptance_gates"])
            self.assertFalse(request["real_local_suite_executed"])
            self.assertIn("does not count toward the planning gate", trial["acceptance_gate_note"])
            self.assertIn("DRAFT_NON_AUTHORITATIVE", trial["acceptance_gate_note"])
            self.assertEqual(trial["schema_version"], "local-shot-planner-trial.v12")
            self.assertEqual(
                trial["prompt_strategy"]["prompt_contract_version"],
                "local-shot-planner-guarded-source-facts.v12",
            )
            report = evaluate_pre_model_guard(request)
            self.assertTrue(report["model_invocation_allowed"], filename)
            self.assertEqual(report["blocks"], [], filename)


if __name__ == "__main__":
    unittest.main()
