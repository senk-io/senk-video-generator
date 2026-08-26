"""多句本地镜头规划评测套件，只汇总观察，不创建质量裁决。"""

from __future__ import annotations

import json
import re
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

from .contracts import canonical_sha256, validate_request
from .generalized_observability import GENERALIZED_STAGE_ALLOWED_VALUES
from .local_trial import (
    LocalTrialError,
    TRIAL_SCHEMA_VERSION_V8,
    TRIAL_SCHEMA_VERSION_V9,
    TRIAL_SCHEMA_VERSION_V10,
    TRIAL_SCHEMA_VERSION_V11,
    TRIAL_SCHEMA_VERSION_V12,
    environment_record,
    run_trial,
    sha256_file,
    utc_now,
    validate_request_binding,
    validate_trial_contract,
    verify_evidence,
    write_json,
    write_manifest,
)


SUITE_SCHEMA_VERSION = "local-shot-planner-evaluation-suite.v1"
SUITE_OBSERVATION_SCHEMA_VERSION = "local-shot-planner-suite-observation.v1"
SUITE_MANIFEST_SCHEMA_VERSION = "local-shot-planner-suite-manifest.v1"
CASE_ID_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9_]{2,63}")
SUITE_ID_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9-]{2,95}")
SUITE_NON_GOALS = frozenset(
    {
        "formal_shot_spec_creation",
        "formal_quality_acceptance",
        "provider_prompt_compilation",
        "video_generation",
        "automatic_retry",
        "creative_acceptance",
        "cross_case_quality_ranking",
    }
)
EXPECTED_CONTROLLED_PATHS = frozenset(
    {
        "scene_context.location",
        "scene_context.time",
        "scene_context.environment",
        "scene_context.continuity_anchor",
        "beat_purpose.purpose",
        "shot_core.primary_purpose",
        "shot_core.framing",
        "shot_core.action_class",
        "shot_core.camera_movement",
        "shot_core.camera_direction",
        "shot_core.camera_speed",
        *(
            f"{stage}.{field}"
            for stage, fields in GENERALIZED_STAGE_ALLOWED_VALUES.items()
            if stage != "shot_core"
            for field in fields
        ),
    }
)


def _nonempty_unique_strings(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value)
        and len(value) == len(set(value))
    )


def _safe_repo_path(repo_root: Path, relative: Any) -> Path:
    if not isinstance(relative, str) or not relative:
        raise ValueError("套件绑定路径必须是非空仓库相对路径。")
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError("套件绑定路径不得越出仓库。")
    resolved_root = repo_root.resolve()
    resolved = (resolved_root / candidate).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError("套件绑定路径不得越出仓库。") from exc
    if not resolved.is_file():
        raise ValueError("套件绑定文件不存在。")
    return resolved


def validate_suite_contract(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("本地规划评测套件必须是对象。")
    expected_top_level = {
        "aggregation_contract",
        "case_order",
        "cases",
        "methodology_invariants",
        "non_goals",
        "resource_budget",
        "schema_version",
        "status",
        "suite_id",
    }
    if set(value) != expected_top_level:
        raise ValueError("本地规划评测套件字段集合无效。")
    if value.get("schema_version") != SUITE_SCHEMA_VERSION:
        raise ValueError("本地规划评测套件版本无效。")
    if value.get("status") != "BOUNDED_NON_AUTHORITATIVE_EVALUATION":
        raise ValueError("本地规划评测套件必须保持非权威有界状态。")
    suite_id = value.get("suite_id")
    if not isinstance(suite_id, str) or not SUITE_ID_PATTERN.fullmatch(suite_id):
        raise ValueError("本地规划评测套件标识无效。")
    if set(value.get("non_goals", [])) != SUITE_NON_GOALS:
        raise ValueError("本地规划评测套件非目标不完整。")
    if value.get("methodology_invariants") != {
        "model_load_count_maximum": 1,
        "retry_count": 0,
        "runs_per_case": 3,
        "same_execution_parameters": True,
        "same_model_revision": True,
        "same_prompt_and_compiler_contracts": True,
    }:
        raise ValueError("本地规划评测套件方法学不变量无效。")
    if value.get("aggregation_contract") != {
        "average_stability_ratios": False,
        "create_quality_threshold": False,
        "observe_cross_case_fingerprints": True,
        "observe_exact_source_echo": True,
        "retain_per_case_observations": True,
    }:
        raise ValueError("本地规划评测套件汇总合同无效。")

    cases = value.get("cases")
    case_order = value.get("case_order")
    if not isinstance(cases, list) or not cases or not isinstance(case_order, list):
        raise ValueError("本地规划评测套件必须包含有序用例。")
    case_ids: list[str] = []
    for case in cases:
        if not isinstance(case, dict) or set(case) != {
            "case_id",
            "coverage_tags",
            "held_out_observation",
            "request_binding",
            "trial_binding",
        }:
            raise ValueError("评测用例字段集合无效。")
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or not CASE_ID_PATTERN.fullmatch(case_id):
            raise ValueError("评测用例标识无效。")
        case_ids.append(case_id)
        if not _nonempty_unique_strings(case.get("coverage_tags")):
            raise ValueError("评测用例覆盖标签无效。")
        request_binding = case.get("request_binding")
        trial_binding = case.get("trial_binding")
        if not isinstance(request_binding, dict) or set(request_binding) != {
            "request_file",
            "request_sha256",
        }:
            raise ValueError("评测用例请求绑定无效。")
        if not isinstance(trial_binding, dict) or set(trial_binding) != {
            "trial_contract_file",
            "trial_contract_sha256",
        }:
            raise ValueError("评测用例试验绑定无效。")
        for digest in (
            request_binding.get("request_sha256"),
            trial_binding.get("trial_contract_sha256"),
        ):
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise ValueError("评测用例绑定摘要无效。")
        held_out = case.get("held_out_observation")
        if not isinstance(held_out, dict) or set(held_out) != {
            "excluded_compiled_terms",
            "expected_controlled_values",
            "required_compiled_terms",
        }:
            raise ValueError("评测用例保留观察合同无效。")
        if not _nonempty_unique_strings(held_out.get("required_compiled_terms")):
            raise ValueError("评测用例必需编译词无效。")
        if not _nonempty_unique_strings(held_out.get("excluded_compiled_terms")):
            raise ValueError("评测用例禁入编译词无效。")
        if set(held_out["required_compiled_terms"]) & set(
            held_out["excluded_compiled_terms"]
        ):
            raise ValueError("评测用例必需词与禁入词不得重叠。")
        expected_values = held_out.get("expected_controlled_values")
        if not isinstance(expected_values, dict) or set(expected_values) != set(
            EXPECTED_CONTROLLED_PATHS
        ):
            raise ValueError("评测用例预期受控字段集合无效。")
        if any(not isinstance(item, str) or not item for item in expected_values.values()):
            raise ValueError("评测用例预期受控值无效。")
    if len(case_ids) != len(set(case_ids)) or case_order != case_ids:
        raise ValueError("评测用例标识必须唯一并严格遵守固定顺序。")

    expected_budget = {
        "maximum_cases": len(cases),
        "maximum_model_calls": len(cases) * 21,
        "maximum_model_loads": 1,
        "maximum_model_weight_bytes": 1_600_000_000,
        "maximum_runs": len(cases) * 3,
        "retry_count": 0,
    }
    if value.get("resource_budget") != expected_budget:
        raise ValueError("本地规划评测套件资源预算无效。")
    return deepcopy(value)


def _allowed_values_for_request(request: dict[str, Any]) -> dict[str, dict[str, list[str]]]:
    constraints = request["semantic_constraints"]
    return {
        "scene_context": request["controlled_context_token_values"]["scene_context"],
        "beat_purpose": {"purpose": constraints["allowed_primary_purposes"]},
        "shot_core": {
            "primary_purpose": constraints["allowed_primary_purposes"],
            "framing": constraints["allowed_framings"],
            "action_class": constraints["allowed_action_classes"],
            "camera_movement": constraints["allowed_camera_movements"],
            "camera_direction": constraints["allowed_camera_directions"],
            "camera_speed": constraints["allowed_camera_speeds"],
        },
        **request["controlled_stage_allowed_values"],
    }


def load_suite_cases(
    suite_value: Any,
    repo_root: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    suite = validate_suite_contract(suite_value)
    loaded: list[dict[str, Any]] = []
    model_fingerprints: set[str] = set()
    execution_fingerprints: set[str] = set()
    prompt_fingerprints: set[str] = set()
    for case in suite["cases"]:
        request_path = _safe_repo_path(
            repo_root, case["request_binding"]["request_file"]
        )
        trial_path = _safe_repo_path(
            repo_root, case["trial_binding"]["trial_contract_file"]
        )
        request = validate_request(
            json.loads(request_path.read_text(encoding="utf-8"))
        )
        trial = validate_trial_contract(
            json.loads(trial_path.read_text(encoding="utf-8"))
        )
        if trial["schema_version"] not in {
            TRIAL_SCHEMA_VERSION_V8,
            TRIAL_SCHEMA_VERSION_V9,
            TRIAL_SCHEMA_VERSION_V10,
            TRIAL_SCHEMA_VERSION_V11,
            TRIAL_SCHEMA_VERSION_V12,
        }:
            raise ValueError("通用性套件只允许第八版至第十二版单用例试验。")
        if canonical_sha256(request) != case["request_binding"]["request_sha256"]:
            raise ValueError("评测用例请求摘要漂移。")
        if canonical_sha256(trial) != case["trial_binding"][
            "trial_contract_sha256"
        ]:
            raise ValueError("评测用例试验合同摘要漂移。")
        validate_request_binding(
            trial,
            request,
            request_path.resolve().relative_to(repo_root.resolve()).as_posix(),
        )
        allowed_values = _allowed_values_for_request(request)
        for path, expected in case["held_out_observation"][
            "expected_controlled_values"
        ].items():
            stage, field = path.split(".", 1)
            if expected not in allowed_values[stage][field]:
                raise ValueError("保留观察预期值不在对应请求允许值中。")
        model_fingerprints.add(canonical_sha256(trial["model"]))
        execution_fingerprints.add(canonical_sha256(trial["execution"]))
        prompt_fingerprints.add(canonical_sha256(trial["prompt_strategy"]))
        loaded.append(
            {
                "case": case,
                "request": request,
                "request_path": request_path,
                "trial": trial,
                "trial_path": trial_path,
            }
        )
    if len(model_fingerprints) != 1:
        raise ValueError("评测用例模型修订不一致。")
    if len(execution_fingerprints) != 1:
        raise ValueError("评测用例执行参数不一致。")
    if len(prompt_fingerprints) != 1:
        raise ValueError("评测用例提示或编译合同不一致。")
    return suite, loaded


def _case_directory_name(index: int, case_id: str) -> str:
    return f"{index:03d}-{case_id.lower().replace('_', '-')}"


def _payload_value(case_dir: Path, run_index: int, path: str) -> Any:
    stage, field = path.split(".", 1)
    payload_path = case_dir / f"payload_{run_index:03d}_{stage}.json"
    if not payload_path.is_file():
        return None
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    return payload.get(field) if isinstance(payload, dict) else None


def observe_suite_case(
    case: dict[str, Any],
    case_dir: Path,
) -> dict[str, Any]:
    summary = json.loads((case_dir / "summary.json").read_text(encoding="utf-8"))
    request = json.loads(
        (case_dir / "planning_request.json").read_text(encoding="utf-8")
    )
    held_out = case["held_out_observation"]
    run_observations: list[dict[str, Any]] = []
    fingerprints: list[dict[str, Any]] = []
    observation_codes: Counter[str] = Counter()
    exact_source_echo_run_count = 0
    for run_index in range(1, summary["run_count_observed"] + 1):
        proposal_path = case_dir / f"proposal_{run_index:03d}.json"
        proposal = (
            json.loads(proposal_path.read_text(encoding="utf-8"))
            if proposal_path.is_file()
            else None
        )
        compiled_text = json.dumps(proposal, ensure_ascii=False) if proposal else ""
        missing_terms = [
            term
            for term in held_out["required_compiled_terms"]
            if term not in compiled_text
        ]
        present_excluded_terms = [
            term
            for term in held_out["excluded_compiled_terms"]
            if term in compiled_text
        ]
        controlled_mismatches: list[dict[str, Any]] = []
        flattened: dict[str, Any] = {}
        for path, expected in held_out["expected_controlled_values"].items():
            observed = _payload_value(case_dir, run_index, path)
            flattened[path] = observed
            if observed != expected:
                controlled_mismatches.append(
                    {"path": path, "expected": expected, "observed": observed}
                )
        fingerprint = (
            canonical_sha256(flattened)
            if all(value is not None for value in flattened.values())
            else None
        )
        fingerprints.append(
            {
                "run_index": run_index,
                "controlled_fingerprint_sha256": fingerprint,
            }
        )
        exact_source_echo = False
        if isinstance(proposal, dict):
            shots = proposal.get("shots")
            if isinstance(shots, list) and shots and isinstance(shots[0], dict):
                action = shots[0].get("action")
                exact_source_echo = (
                    isinstance(action, dict)
                    and action.get("description") == request["source_text"]
                )
        exact_source_echo_run_count += int(exact_source_echo)
        proposal_observation = json.loads(
            (case_dir / f"proposal_observation_{run_index:03d}.json").read_text(
                encoding="utf-8"
            )
        )
        observation_codes.update(
            item.get("code")
            for item in proposal_observation.get("observations", [])
            if isinstance(item, dict) and isinstance(item.get("code"), str)
        )
        run_observations.append(
            {
                "run_index": run_index,
                "required_compiled_terms_missing": missing_terms,
                "excluded_compiled_terms_present": present_excluded_terms,
                "controlled_value_mismatches": controlled_mismatches,
                "held_out_observation_count": (
                    len(missing_terms)
                    + len(present_excluded_terms)
                    + len(controlled_mismatches)
                ),
                "action_description_exact_source_echo": exact_source_echo,
                "controlled_fingerprint_sha256": fingerprint,
            }
        )
    return {
        "case_id": case["case_id"],
        "coverage_tags": case["coverage_tags"],
        "run_count_observed": summary["run_count_observed"],
        "model_call_count_observed": summary["model_call_count_observed"],
        "parsed_run_count": summary["parsed_run_count"],
        "structurally_observable_run_count": summary[
            "structurally_observable_run_count"
        ],
        "largest_exact_structure_group_ratio": summary[
            "largest_exact_structure_group_ratio"
        ],
        "largest_exact_controlled_semantic_group_ratio": summary.get(
            "largest_exact_controlled_semantic_group_ratio"
        ),
        "exact_source_echo_run_count": exact_source_echo_run_count,
        "held_out_observation_count": sum(
            run["held_out_observation_count"] for run in run_observations
        ),
        "proposal_observation_code_counts": dict(sorted(observation_codes.items())),
        "fingerprints": fingerprints,
        "runs": run_observations,
        "formal_decision_created": False,
        "creative_review_required": True,
    }


def observe_suite_evidence(
    suite: dict[str, Any],
    case_directories: dict[str, Path],
    *,
    execution_id: str,
    model_load_count_observed: int,
) -> dict[str, Any]:
    case_observations = [
        observe_suite_case(case, case_directories[case["case_id"]])
        for case in suite["cases"]
    ]
    fingerprint_groups: dict[str, list[dict[str, Any]]] = {}
    for case_observation in case_observations:
        for fingerprint in case_observation["fingerprints"]:
            digest = fingerprint["controlled_fingerprint_sha256"]
            if isinstance(digest, str):
                fingerprint_groups.setdefault(digest, []).append(
                    {
                        "case_id": case_observation["case_id"],
                        "run_index": fingerprint["run_index"],
                    }
                )
    cross_case_groups = [
        {
            "controlled_fingerprint_sha256": digest,
            "members": members,
            "distinct_case_count": len({member["case_id"] for member in members}),
        }
        for digest, members in sorted(fingerprint_groups.items())
        if len({member["case_id"] for member in members}) >= 2
    ]
    return {
        "schema_version": SUITE_OBSERVATION_SCHEMA_VERSION,
        "suite_id": suite["suite_id"],
        "execution_id": execution_id,
        "case_count_requested": suite["resource_budget"]["maximum_cases"],
        "case_count_observed": len(case_observations),
        "run_count_requested": suite["resource_budget"]["maximum_runs"],
        "run_count_observed": sum(
            case["run_count_observed"] for case in case_observations
        ),
        "model_call_count_requested": suite["resource_budget"][
            "maximum_model_calls"
        ],
        "model_call_count_observed": sum(
            case["model_call_count_observed"] for case in case_observations
        ),
        "model_load_count_observed": model_load_count_observed,
        "automatic_retry_count": 0,
        "held_out_observation_count": sum(
            case["held_out_observation_count"] for case in case_observations
        ),
        "exact_source_echo_run_count": sum(
            case["exact_source_echo_run_count"] for case in case_observations
        ),
        "cross_case_controlled_fingerprint_groups": cross_case_groups,
        "cases": case_observations,
        "formal_shot_spec_created": False,
        "formal_quality_acceptance_created": False,
        "formal_decision_created": False,
        "creative_review_required": True,
    }


def write_suite_manifest(
    evidence_dir: Path,
    case_index: list[dict[str, Any]],
) -> dict[str, Any]:
    root_files = []
    for name in (
        "suite_contract.json",
        "case_index.json",
        "suite_environment.json",
        "suite_observation.json",
    ):
        path = evidence_dir / name
        root_files.append(
            {"path": name, "bytes": path.stat().st_size, "sha256": sha256_file(path)}
        )
    case_manifests = []
    for case in case_index:
        relative = f"{case['evidence_path']}/manifest.json"
        path = evidence_dir / relative
        case_manifests.append(
            {
                "case_id": case["case_id"],
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    manifest = {
        "schema_version": SUITE_MANIFEST_SCHEMA_VERSION,
        "root_files": root_files,
        "case_manifests": case_manifests,
        "formal_decision_created": False,
    }
    write_json(evidence_dir / "manifest.json", manifest)
    return manifest


def run_suite(
    suite_value: Any,
    *,
    repo_root: Path,
    suite_contract_path: Path,
    runner_path: Path,
    execution_id: str,
    evidence_dir: Path,
    generate: Callable[[dict[str, Any], int], str],
    model_load_count_observed: int,
) -> dict[str, Any]:
    suite, loaded_cases = load_suite_cases(suite_value, repo_root)
    if evidence_dir.exists():
        raise LocalTrialError("套件证据目录已经存在，不得覆盖历史运行。")
    evidence_dir.mkdir(parents=True)
    cases_root = evidence_dir / "cases"
    cases_root.mkdir()
    write_json(evidence_dir / "suite_contract.json", suite)
    global_call_index = 0
    case_index: list[dict[str, Any]] = []
    case_directories: dict[str, Path] = {}

    for index, loaded in enumerate(loaded_cases, start=1):
        case = loaded["case"]
        case_id = case["case_id"]
        case_execution_id = f"{execution_id}-{index:03d}-{case_id}"
        relative_evidence = f"cases/{_case_directory_name(index, case_id)}"
        case_dir = evidence_dir / relative_evidence

        def case_generate(prompt: dict[str, Any], _case_call_index: int) -> str:
            nonlocal global_call_index
            global_call_index += 1
            return generate(prompt, global_call_index)

        run_trial(
            loaded["trial"],
            loaded["request"],
            case_execution_id,
            case_dir,
            case_generate,
            request_relative_path=loaded["request_path"]
            .resolve()
            .relative_to(repo_root.resolve())
            .as_posix(),
        )
        write_json(
            case_dir / "environment.json",
            environment_record(
                execution_id=case_execution_id,
                repo_root=repo_root,
                contract_path=loaded["trial_path"],
                request_path=loaded["request_path"],
                runner_path=runner_path,
            ),
        )
        write_manifest(case_dir)
        verify_evidence(case_dir)
        case_directories[case_id] = case_dir
        case_index.append(
            {
                "case_id": case_id,
                "ordinal": index,
                "execution_id": case_execution_id,
                "evidence_path": relative_evidence,
            }
        )

    write_json(evidence_dir / "case_index.json", case_index)
    suite_observation = observe_suite_evidence(
        suite,
        case_directories,
        execution_id=execution_id,
        model_load_count_observed=model_load_count_observed,
    )
    if global_call_index != suite["resource_budget"]["maximum_model_calls"]:
        raise LocalTrialError("套件实际模型调用次数与固定预算不一致。")
    write_json(evidence_dir / "suite_observation.json", suite_observation)
    first_case_environment = json.loads(
        (case_directories[suite["case_order"][0]] / "environment.json").read_text(
            encoding="utf-8"
        )
    )
    write_json(
        evidence_dir / "suite_environment.json",
        {
            "execution_id": execution_id,
            "recorded_at": utc_now(),
            "suite_contract_sha256": sha256_file(suite_contract_path),
            "runner_sha256": sha256_file(runner_path),
            "git_head": first_case_environment.get("git_head"),
            "git_status_porcelain": first_case_environment.get(
                "git_status_porcelain", ""
            ),
            "implementation_sha256": first_case_environment.get(
                "implementation_sha256", {}
            ),
            "model_id": loaded_cases[0]["trial"]["model"]["model_id"],
            "model_revision": loaded_cases[0]["trial"]["model"]["revision"],
            "model_load_count_observed": model_load_count_observed,
            "remote_inference_used": False,
            "paid_request": False,
            "formal_fact_creation": "PROHIBITED",
        },
    )
    write_suite_manifest(evidence_dir, case_index)
    return suite_observation


def verify_suite_evidence(evidence_dir: Path) -> dict[str, Any]:
    manifest = json.loads((evidence_dir / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != SUITE_MANIFEST_SCHEMA_VERSION:
        raise LocalTrialError("套件证据清单版本无效。")
    if manifest.get("formal_decision_created") is not False:
        raise LocalTrialError("套件证据清单越权声明正式裁决。")
    expected_root_names = {
        "suite_contract.json",
        "case_index.json",
        "suite_environment.json",
        "suite_observation.json",
    }
    root_entries = manifest.get("root_files")
    if not isinstance(root_entries, list) or {
        item.get("path") for item in root_entries if isinstance(item, dict)
    } != expected_root_names:
        raise LocalTrialError("套件根证据文件集合无效。")
    for item in root_entries:
        path = evidence_dir / item["path"]
        if (
            not path.is_file()
            or path.stat().st_size != item.get("bytes")
            or sha256_file(path) != item.get("sha256")
        ):
            raise LocalTrialError("套件根证据摘要不一致。")
    actual_root_files = {
        path.name
        for path in evidence_dir.iterdir()
        if path.is_file() and path.name != "manifest.json"
    }
    if actual_root_files != expected_root_names:
        raise LocalTrialError("套件清单没有精确覆盖根证据文件。")

    suite = validate_suite_contract(
        json.loads((evidence_dir / "suite_contract.json").read_text(encoding="utf-8"))
    )
    case_index = json.loads(
        (evidence_dir / "case_index.json").read_text(encoding="utf-8")
    )
    if not isinstance(case_index, list) or [item.get("case_id") for item in case_index] != suite[
        "case_order"
    ]:
        raise LocalTrialError("套件证据用例顺序无效。")
    case_manifest_entries = manifest.get("case_manifests")
    if not isinstance(case_manifest_entries, list) or [
        item.get("case_id") for item in case_manifest_entries if isinstance(item, dict)
    ] != suite["case_order"]:
        raise LocalTrialError("套件子用例清单顺序无效。")
    expected_case_directories = {item["evidence_path"] for item in case_index}
    actual_case_directories = {
        f"cases/{path.name}"
        for path in (evidence_dir / "cases").iterdir()
        if path.is_dir()
    }
    if actual_case_directories != expected_case_directories:
        raise LocalTrialError("套件子用例目录集合无效。")

    case_directories: dict[str, Path] = {}
    child_environments: list[dict[str, Any]] = []
    embedded_trials: list[dict[str, Any]] = []
    for case, index_item, manifest_item in zip(
        suite["cases"], case_index, case_manifest_entries, strict=True
    ):
        expected_manifest_path = f"{index_item['evidence_path']}/manifest.json"
        if manifest_item.get("path") != expected_manifest_path:
            raise LocalTrialError("套件子用例清单路径无效。")
        manifest_path = evidence_dir / expected_manifest_path
        if (
            not manifest_path.is_file()
            or manifest_path.stat().st_size != manifest_item.get("bytes")
            or sha256_file(manifest_path) != manifest_item.get("sha256")
        ):
            raise LocalTrialError("套件子用例清单摘要不一致。")
        case_dir = evidence_dir / index_item["evidence_path"]
        verification = verify_evidence(case_dir)
        if verification["execution_id"] != index_item["execution_id"]:
            raise LocalTrialError("套件子用例执行标识不一致。")
        embedded_request = json.loads(
            (case_dir / "planning_request.json").read_text(encoding="utf-8")
        )
        embedded_trial = json.loads(
            (case_dir / "trial_contract.json").read_text(encoding="utf-8")
        )
        if canonical_sha256(embedded_request) != case["request_binding"][
            "request_sha256"
        ]:
            raise LocalTrialError("套件子用例请求摘要不一致。")
        if canonical_sha256(embedded_trial) != case["trial_binding"][
            "trial_contract_sha256"
        ]:
            raise LocalTrialError("套件子用例试验合同摘要不一致。")
        embedded_trials.append(embedded_trial)
        child_environments.append(
            json.loads((case_dir / "environment.json").read_text(encoding="utf-8"))
        )
        case_directories[case["case_id"]] = case_dir

    environment = json.loads(
        (evidence_dir / "suite_environment.json").read_text(encoding="utf-8")
    )
    observation = json.loads(
        (evidence_dir / "suite_observation.json").read_text(encoding="utf-8")
    )
    implementation_bound_suite = all(
        trial.get("schema_version")
        in {
            TRIAL_SCHEMA_VERSION_V10,
            TRIAL_SCHEMA_VERSION_V11,
            TRIAL_SCHEMA_VERSION_V12,
        }
        for trial in embedded_trials
    )
    base_environment_fields = {
        "execution_id",
        "recorded_at",
        "suite_contract_sha256",
        "runner_sha256",
        "git_head",
        "git_status_porcelain",
        "model_id",
        "model_revision",
        "model_load_count_observed",
        "remote_inference_used",
        "paid_request",
        "formal_fact_creation",
    }
    allowed_environment_field_sets = (
        {frozenset(base_environment_fields | {"implementation_sha256"})}
        if implementation_bound_suite
        else {
            frozenset(base_environment_fields),
            frozenset(base_environment_fields | {"implementation_sha256"}),
        }
    )
    if not isinstance(environment, dict) or frozenset(environment) not in allowed_environment_field_sets:
        raise LocalTrialError("套件运行环境字段集合无效。")
    first_trial = embedded_trials[0]
    first_child_environment = child_environments[0]
    if (
        environment.get("execution_id") != observation.get("execution_id")
        or not isinstance(environment.get("recorded_at"), str)
        or not environment["recorded_at"]
        or environment.get("suite_contract_sha256")
        != sha256_file(evidence_dir / "suite_contract.json")
        or environment.get("runner_sha256")
        != first_child_environment.get("runner_sha256")
        or any(
            child.get("runner_sha256") != environment.get("runner_sha256")
            for child in child_environments
        )
        or environment.get("git_head") != first_child_environment.get("git_head")
        or environment.get("git_status_porcelain")
        != first_child_environment.get("git_status_porcelain")
        or environment.get("model_id") != first_trial["model"]["model_id"]
        or environment.get("model_revision") != first_trial["model"]["revision"]
        or environment.get("model_load_count_observed") != 1
        or environment.get("remote_inference_used") is not False
        or environment.get("paid_request") is not False
        or environment.get("formal_fact_creation") != "PROHIBITED"
    ):
        raise LocalTrialError("套件运行环境与子用例及固定边界不一致。")
    if implementation_bound_suite and (
        environment.get("implementation_sha256")
        != first_child_environment.get("implementation_sha256")
        or "shot_planning/evaluation_suite.py"
        not in environment.get("implementation_sha256", {})
        or any(
            child.get("implementation_sha256")
            != environment.get("implementation_sha256")
            for child in child_environments
        )
    ):
        raise LocalTrialError("第十版及以后套件实现摘要与子用例不一致。")
    if not implementation_bound_suite and "implementation_sha256" in environment and any(
        child.get("implementation_sha256") != environment["implementation_sha256"]
        for child in child_environments
    ):
        raise LocalTrialError("套件实现摘要与子用例不一致。")
    recomputed = observe_suite_evidence(
        suite,
        case_directories,
        execution_id=observation.get("execution_id"),
        model_load_count_observed=environment.get("model_load_count_observed"),
    )
    if canonical_sha256(recomputed) != canonical_sha256(observation):
        raise LocalTrialError("套件汇总观察无法由子用例证据重算。")
    if observation.get("model_call_count_observed") != suite["resource_budget"][
        "maximum_model_calls"
    ]:
        raise LocalTrialError("套件模型调用次数与固定预算不一致。")
    if observation.get("automatic_retry_count") != 0:
        raise LocalTrialError("套件出现合同外自动重试。")
    if environment.get("model_load_count_observed") != 1:
        raise LocalTrialError("套件没有满足单次模型加载合同。")
    for field in (
        "formal_shot_spec_created",
        "formal_quality_acceptance_created",
        "formal_decision_created",
    ):
        if observation.get(field) is not False:
            raise LocalTrialError("套件汇总观察越权声明正式事实或裁决。")
    return {
        "schema_version": "local-shot-planner-suite-verification.v1",
        "suite_id": suite["suite_id"],
        "execution_id": observation["execution_id"],
        "case_count_observed": observation["case_count_observed"],
        "model_call_count_observed": observation["model_call_count_observed"],
        "package_integrity_observation": "COMPLETE_AND_DIGEST_MATCHED",
        "formal_shot_spec_created": False,
        "formal_quality_acceptance_created": False,
    }
