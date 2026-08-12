#!/usr/bin/env python3
"""预检或执行固定三用例的 Qwen3 本地镜头规划通用性套件。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUITE = (
    REPO_ROOT
    / "experiments"
    / "shot_planning"
    / "qwen3_0_6b_generalization_suite_v1.json"
)
DEFAULT_EVIDENCE_ROOT = REPO_ROOT / "evidence" / "runtime"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shot_planning.evaluation_suite import (
    load_suite_cases,
    run_suite,
    verify_suite_evidence,
)
from tools.run_local_shot_planner_trial import (
    build_lazy_generator,
    local_preflight,
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    parser.add_argument("--execution-id")
    parser.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="使用一次模型加载依次执行三用例、九轮、六十三次固定阶段调用",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    suite_path = args.suite.resolve()
    suite, loaded_cases = load_suite_cases(load_json(suite_path), REPO_ROOT)
    first_trial = loaded_cases[0]["trial"]
    preflight = local_preflight(first_trial)
    ready = (
        preflight["observed_revision"] == first_trial["model"]["revision"]
        and preflight["observed_weight_bytes"]
        == first_trial["model"]["expected_weight_bytes"]
        and preflight["weight_within_budget"]
        and preflight["mps_available"]
    )
    preflight.update(
        {
            "suite_id": suite["suite_id"],
            "case_count": len(loaded_cases),
            "total_run_count": suite["resource_budget"]["maximum_runs"],
            "total_model_call_count": suite["resource_budget"][
                "maximum_model_calls"
            ],
            "model_load_count_maximum": suite["resource_budget"][
                "maximum_model_loads"
            ],
            "preflight": "ready" if ready else "blocked",
            "execute_flag_present": args.execute,
            "formal_fact_creation": False,
        }
    )
    if not args.execute or not ready:
        print(json.dumps(preflight, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if ready else 2
    if not args.execution_id:
        print("执行本地模型套件时必须提供 --execution-id", file=sys.stderr)
        return 2

    evidence_dir = args.evidence_root.resolve() / args.execution_id
    generator = build_lazy_generator(first_trial)
    observation = run_suite(
        suite,
        repo_root=REPO_ROOT,
        suite_contract_path=suite_path,
        runner_path=Path(__file__),
        execution_id=args.execution_id,
        evidence_dir=evidence_dir,
        generate=generator,
        model_load_count_observed=1,
    )
    verification = verify_suite_evidence(evidence_dir)
    print(
        json.dumps(
            {"observation": observation, "verification": verification},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
