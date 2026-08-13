"""本地文本小模型镜头规划试验，保留原始输出且不自动重试。"""

from __future__ import annotations

import hashlib
import json
import platform
import re
import subprocess
import time
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from .contracts import (
    PLANNER_CONTEXT_PROMPT_CONTRACT_VERSION,
    PLANNER_GENERALIZED_OBSERVABILITY_PROMPT_CONTRACT_VERSION,
    PLANNER_HYBRID_SOURCE_FACT_PROMPT_CONTRACT_VERSION,
    PLANNER_OBSERVABLE_PROMPT_CONTRACT_VERSION,
    PLANNER_PAYLOAD_PROMPT_CONTRACT_VERSION,
    PLANNER_PROMPT_CONTRACT_VERSION,
    PLANNER_STAGED_PROMPT_CONTRACT_VERSION,
    PLANNER_SEMANTIC_PROMPT_CONTRACT_VERSION,
    PLANNER_TOKENIZED_CONTEXT_PROMPT_CONTRACT_VERSION,
    PLANNER_SCALAR_CHOICE_PROMPT_CONTRACT_VERSION,
    PLANNER_SEMANTIC_GLOSS_PROMPT_CONTRACT_VERSION,
    PROPOSAL_SCHEMA_VERSION,
    PROPOSAL_SCHEMA_VERSION_V2,
    REQUEST_SCHEMA_VERSION_V2,
    canonical_sha256,
    validate_request,
)
from .controlled_context import (
    TOKENIZED_CONTEXT_ALLOWED_VALUES,
    TOKENIZED_CONTEXT_COMPILER_VERSION,
    TOKENIZED_CONTEXT_STAGE_KEYS,
    TOKENIZED_CONTEXT_STAGE_ORDER,
    describe_context_token,
    tokenized_context_compiler_contract,
    tokenized_context_compiler_contract_sha256,
)
from .prompting import (
    build_local_planner_generalized_stage_prompt,
    build_local_planner_hybrid_stage_prompt,
    build_local_planner_context_stage_prompt,
    build_local_planner_observable_stage_prompt,
    build_local_planner_payload_prompt,
    build_local_planner_prompt,
    build_local_planner_stage_prompt,
    build_local_planner_tokenized_context_stage_prompt,
    build_local_planner_scalar_choice_stage_prompt,
    build_local_planner_semantic_gloss_stage_prompt,
)
from .generalized_observability import (
    GENERALIZED_OBSERVABILITY_COMPILER_VERSION,
    GENERALIZED_STAGE_ALLOWED_VALUES,
    GENERALIZED_STAGE_ORDER,
    GENERALIZED_STAGE_REQUIRED_KEYS,
    build_generalized_payload,
    generalized_compiler_contract,
    generalized_compiler_contract_sha256,
    observe_generalized_semantic_stability,
    observe_generalized_stage_consistency,
)
from .stability import observe_stability
from .semantic_choice import (
    SEMANTIC_CHOICE_GLOSSARY_VERSION,
    semantic_choice_glossary_contract,
    semantic_choice_glossary_sha256,
)
from .source_facts import (
    HYBRID_MERGE_CONTRACT_VERSION,
    SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION,
    extract_source_facts,
    field_ownership_view,
    hybrid_merge_contract,
    hybrid_merge_contract_sha256,
    merge_hybrid_stage_payload,
    source_fact_extractor_contract,
    source_fact_extractor_contract_sha256,
)
from .structured_observability import (
    CONTROLLED_OBSERVABILITY_COMPILER_VERSION,
    OBSERVABLE_STAGE_ORDER,
    STRUCTURED_STAGE_ALLOWED_VALUES,
    STRUCTURED_STAGE_REQUIRED_KEYS,
    compiler_contract,
    compiler_contract_sha256,
    describe_token,
    observe_controlled_semantic_stability,
)
from .validation import observe_proposal


TRIAL_SCHEMA_VERSION_V1 = "local-shot-planner-trial.v1"
TRIAL_SCHEMA_VERSION_V2 = "local-shot-planner-trial.v2"
TRIAL_SCHEMA_VERSION_V3 = "local-shot-planner-trial.v3"
TRIAL_SCHEMA_VERSION_V4 = "local-shot-planner-trial.v4"
TRIAL_SCHEMA_VERSION_V5 = "local-shot-planner-trial.v5"
TRIAL_SCHEMA_VERSION_V6 = "local-shot-planner-trial.v6"
TRIAL_SCHEMA_VERSION_V7 = "local-shot-planner-trial.v7"
TRIAL_SCHEMA_VERSION_V8 = "local-shot-planner-trial.v8"
TRIAL_SCHEMA_VERSION_V9 = "local-shot-planner-trial.v9"
TRIAL_SCHEMA_VERSION_V10 = "local-shot-planner-trial.v10"
TRIAL_SCHEMA_VERSION_V11 = "local-shot-planner-trial.v11"
STAGED_TRIAL_SCHEMA_VERSIONS = frozenset(
    {
        TRIAL_SCHEMA_VERSION_V3,
        TRIAL_SCHEMA_VERSION_V4,
        TRIAL_SCHEMA_VERSION_V5,
        TRIAL_SCHEMA_VERSION_V6,
        TRIAL_SCHEMA_VERSION_V7,
        TRIAL_SCHEMA_VERSION_V8,
        TRIAL_SCHEMA_VERSION_V9,
        TRIAL_SCHEMA_VERSION_V10,
        TRIAL_SCHEMA_VERSION_V11,
    }
)
CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS = frozenset(
    {TRIAL_SCHEMA_VERSION_V5, TRIAL_SCHEMA_VERSION_V6, TRIAL_SCHEMA_VERSION_V7}
)
GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS = frozenset(
    {
        TRIAL_SCHEMA_VERSION_V8,
        TRIAL_SCHEMA_VERSION_V9,
        TRIAL_SCHEMA_VERSION_V10,
        TRIAL_SCHEMA_VERSION_V11,
    }
)
SEMANTIC_STABILITY_TRIAL_SCHEMA_VERSIONS = frozenset(
    CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS
    | GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS
)
MODEL_ID = "Qwen/Qwen3-0.6B"
MODEL_REVISION = "c1899de289a04d12100db370d81485cdf75e47ca"
MODEL_WEIGHT_BYTES = 1_503_300_328
NON_GOALS = frozenset(
    {
        "formal_shot_spec_creation",
        "formal_quality_acceptance",
        "provider_prompt_compilation",
        "video_generation",
        "automatic_retry",
        "creative_acceptance",
    }
)


class LocalTrialError(RuntimeError):
    """本地试验无法满足固定合同或证据边界。"""


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def validate_trial_contract(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("本地规划试验合同必须是对象。")
    schema_version = value.get("schema_version")
    if schema_version not in {
        TRIAL_SCHEMA_VERSION_V1,
        TRIAL_SCHEMA_VERSION_V2,
        TRIAL_SCHEMA_VERSION_V3,
        TRIAL_SCHEMA_VERSION_V4,
        TRIAL_SCHEMA_VERSION_V5,
        TRIAL_SCHEMA_VERSION_V6,
        TRIAL_SCHEMA_VERSION_V7,
        TRIAL_SCHEMA_VERSION_V8,
        TRIAL_SCHEMA_VERSION_V9,
        TRIAL_SCHEMA_VERSION_V10,
        TRIAL_SCHEMA_VERSION_V11,
    }:
        raise ValueError("本地规划试验合同版本无效。")
    if value.get("status") != "BOUNDED_NON_AUTHORITATIVE_TRIAL":
        raise ValueError("本地规划试验必须保持非权威有界状态。")
    model = value.get("model")
    if model != {
        "model_id": MODEL_ID,
        "revision": MODEL_REVISION,
        "expected_weight_bytes": MODEL_WEIGHT_BYTES,
    }:
        raise ValueError("模型标识、修订或权重大小不符合固定合同。")
    execution = value.get("execution")
    if execution != {
        "backend": "transformers_mps",
        "dtype": "float16",
        "run_count": 3,
        "max_new_tokens": 3072,
        "do_sample": False,
        "temperature": 0.0,
        "seed": 20260811,
        "enable_thinking": False,
    }:
        raise ValueError("本地规划执行参数不符合固定三次贪心解码合同。")
    budget = value.get("resource_budget")
    expected_budget = {
        "maximum_model_weight_bytes": 1_600_000_000,
        "maximum_runs": 3,
        "retry_count": 0,
    }
    if schema_version in {TRIAL_SCHEMA_VERSION_V3, TRIAL_SCHEMA_VERSION_V4}:
        expected_budget["maximum_model_calls"] = 9
    elif schema_version in SEMANTIC_STABILITY_TRIAL_SCHEMA_VERSIONS:
        expected_budget["maximum_model_calls"] = 21
    if budget != expected_budget:
        raise ValueError("本地规划资源预算无效。")
    evidence = value.get("evidence")
    if evidence != {
        "retain_environment": True,
        "retain_prompt_per_run": True,
        "retain_raw_output_per_run": True,
        "write_manifest": True,
    }:
        raise ValueError("本地规划证据保留合同不完整。")
    if set(value.get("non_goals", [])) != NON_GOALS:
        raise ValueError("本地规划试验非目标不完整。")
    if schema_version == TRIAL_SCHEMA_VERSION_V2:
        if value.get("prompt_strategy") != {
            "assistant_prefill": "{",
            "model_output_scope": "creative_payload_only",
            "prompt_contract_version": PLANNER_PAYLOAD_PROMPT_CONTRACT_VERSION,
            "system_owned_envelope": True,
        }:
            raise ValueError("第二版提示策略必须固定为系统封装和 JSON 首字符预填充。")
        strategy_context = value.get("strategy_context")
        if (
            not isinstance(strategy_context, dict)
            or strategy_context.get("change")
            != "SYSTEM_OWNED_ENVELOPE_AND_ASSISTANT_JSON_PREFILL"
            or not isinstance(strategy_context.get("previous_execution_id"), str)
            or not strategy_context.get("previous_observations")
        ):
            raise ValueError("第二版试验必须引用上一轮观察和变更依据。")
    if schema_version == TRIAL_SCHEMA_VERSION_V3:
        if value.get("prompt_strategy") != {
            "assistant_prefill": "{",
            "model_output_scope": "three_flat_creative_stages",
            "prompt_contract_version": PLANNER_STAGED_PROMPT_CONTRACT_VERSION,
            "stages": ["scene", "beat", "shot"],
            "system_owned_envelope": True,
        }:
            raise ValueError("第三版提示策略必须固定为三个单职责扁平阶段。")
        strategy_context = value.get("strategy_context")
        if (
            not isinstance(strategy_context, dict)
            or strategy_context.get("change") != "THREE_FLAT_SINGLE_RESPONSIBILITY_STAGES"
            or not isinstance(strategy_context.get("previous_execution_id"), str)
            or not strategy_context.get("previous_observations")
        ):
            raise ValueError("第三版试验必须引用第二版观察和变更依据。")
    if schema_version == TRIAL_SCHEMA_VERSION_V4:
        if value.get("prompt_strategy") != {
            "assistant_prefill": "{",
            "model_output_scope": "three_flat_creative_stages",
            "prompt_contract_version": PLANNER_SEMANTIC_PROMPT_CONTRACT_VERSION,
            "semantic_constraints_enforced": True,
            "stages": ["scene", "beat", "shot"],
            "system_owned_envelope": True,
        }:
            raise ValueError("第四版提示策略必须固定为带显式语义约束的三个阶段。")
        strategy_context = value.get("strategy_context")
        if (
            not isinstance(strategy_context, dict)
            or strategy_context.get("change") != "EXPLICIT_SEMANTIC_CONSTRAINTS"
            or not isinstance(strategy_context.get("previous_execution_id"), str)
            or not strategy_context.get("previous_observations")
        ):
            raise ValueError("第四版试验必须引用第三版语义观察和变更依据。")
    if schema_version == TRIAL_SCHEMA_VERSION_V5:
        if value.get("prompt_strategy") != {
            "assistant_prefill": "{",
            "compiler_contract_sha256": compiler_contract_sha256(),
            "compiler_contract_version": CONTROLLED_OBSERVABILITY_COMPILER_VERSION,
            "model_output_scope": "seven_flat_structured_observability_stages",
            "prompt_contract_version": PLANNER_OBSERVABLE_PROMPT_CONTRACT_VERSION,
            "semantic_constraints_enforced": True,
            "stages": list(OBSERVABLE_STAGE_ORDER),
            "system_owned_envelope": True,
            "system_owned_observable_text_compilation": True,
        }:
            raise ValueError("第五版提示策略必须固定为七个结构化可观察阶段。")
        strategy_context = value.get("strategy_context")
        if (
            not isinstance(strategy_context, dict)
            or strategy_context.get("change")
            != "STRUCTURED_OBSERVABILITY_STAGES_AND_DETERMINISTIC_TEXT_COMPILATION"
            or not isinstance(strategy_context.get("previous_execution_id"), str)
            or not strategy_context.get("previous_observations")
        ):
            raise ValueError("第五版试验必须引用第四版可观察性差异和变更依据。")
    if schema_version == TRIAL_SCHEMA_VERSION_V6:
        if value.get("prompt_strategy") != {
            "assistant_prefill": "{",
            "camera_constraints_enforced": True,
            "compiler_contract_sha256": compiler_contract_sha256(),
            "compiler_contract_version": CONTROLLED_OBSERVABILITY_COMPILER_VERSION,
            "context_role_constraints_enforced": True,
            "model_output_scope": "seven_flat_controlled_context_stages",
            "prompt_contract_version": PLANNER_CONTEXT_PROMPT_CONTRACT_VERSION,
            "semantic_constraints_enforced": True,
            "stages": list(OBSERVABLE_STAGE_ORDER),
            "system_owned_envelope": True,
            "system_owned_observable_text_compilation": True,
        }:
            raise ValueError("第六版提示策略必须固定场景角色和相机组合约束。")
        strategy_context = value.get("strategy_context")
        if (
            not isinstance(strategy_context, dict)
            or strategy_context.get("change")
            != "CONTROLLED_SCENE_ROLES_AND_UNSPECIFIED_CAMERA_POLICY"
            or not isinstance(strategy_context.get("previous_execution_id"), str)
            or not strategy_context.get("previous_observations")
        ):
            raise ValueError("第六版试验必须引用第五版上下文角色和相机观察。")
    if schema_version == TRIAL_SCHEMA_VERSION_V7:
        if value.get("prompt_strategy") != {
            "assistant_prefill": "{",
            "camera_constraints_enforced": True,
            "compiler_contract_sha256": compiler_contract_sha256(),
            "compiler_contract_version": CONTROLLED_OBSERVABILITY_COMPILER_VERSION,
            "context_compiler_contract_sha256": (
                tokenized_context_compiler_contract_sha256()
            ),
            "context_compiler_contract_version": TOKENIZED_CONTEXT_COMPILER_VERSION,
            "context_role_constraints_enforced": True,
            "model_output_scope": "seven_flat_tokenized_context_stages",
            "prompt_contract_version": (
                PLANNER_TOKENIZED_CONTEXT_PROMPT_CONTRACT_VERSION
            ),
            "semantic_constraints_enforced": True,
            "stages": list(TOKENIZED_CONTEXT_STAGE_ORDER),
            "system_owned_beat_action_reuse": True,
            "system_owned_envelope": True,
            "system_owned_observable_text_compilation": True,
        }:
            raise ValueError("第七版提示策略必须固定标记化上下文和动作复用。")
        strategy_context = value.get("strategy_context")
        if (
            not isinstance(strategy_context, dict)
            or strategy_context.get("change")
            != "TOKENIZED_SCENE_CONTEXT_AND_REUSED_CORE_ACTION"
            or not isinstance(strategy_context.get("previous_execution_id"), str)
            or not strategy_context.get("previous_observations")
        ):
            raise ValueError("第七版试验必须引用第六版自然语言缩写观察。")
    if schema_version == TRIAL_SCHEMA_VERSION_V8:
        if value.get("prompt_strategy") != {
            "assistant_prefill": "{",
            "camera_constraints_enforced": True,
            "compiler_contract_sha256": generalized_compiler_contract_sha256(),
            "compiler_contract_version": GENERALIZED_OBSERVABILITY_COMPILER_VERSION,
            "context_compiler_contract_sha256": (
                tokenized_context_compiler_contract_sha256()
            ),
            "context_compiler_contract_version": TOKENIZED_CONTEXT_COMPILER_VERSION,
            "context_role_constraints_enforced": True,
            "cross_stage_consistency_enforced": True,
            "model_output_scope": "seven_flat_generalized_observability_stages",
            "prompt_contract_version": (
                PLANNER_GENERALIZED_OBSERVABILITY_PROMPT_CONTRACT_VERSION
            ),
            "semantic_constraints_enforced": True,
            "stages": list(GENERALIZED_STAGE_ORDER),
            "system_owned_beat_action_reuse": True,
            "system_owned_envelope": True,
            "system_owned_observable_text_compilation": True,
        }:
            raise ValueError("第八版提示策略必须固定通用可观察词表与跨阶段约束。")
        strategy_context = value.get("strategy_context")
        if (
            not isinstance(strategy_context, dict)
            or strategy_context.get("change")
            != "GENERALIZED_SUBJECT_OBSERVABILITY_AND_CROSS_STAGE_CONSISTENCY"
            or not isinstance(strategy_context.get("previous_execution_id"), str)
            or not strategy_context.get("previous_observations")
        ):
            raise ValueError("第八版试验必须引用第七版单请求词表绑定观察。")
    if schema_version == TRIAL_SCHEMA_VERSION_V9:
        if value.get("prompt_strategy") != {
            "assistant_prefill": "{",
            "camera_constraints_enforced": True,
            "compiler_contract_sha256": generalized_compiler_contract_sha256(),
            "compiler_contract_version": GENERALIZED_OBSERVABILITY_COMPILER_VERSION,
            "context_compiler_contract_sha256": (
                tokenized_context_compiler_contract_sha256()
            ),
            "context_compiler_contract_version": TOKENIZED_CONTEXT_COMPILER_VERSION,
            "context_role_constraints_enforced": True,
            "cross_stage_consistency_enforced": True,
            "model_output_scope": "seven_flat_scalar_choice_stages",
            "prompt_contract_version": PLANNER_SCALAR_CHOICE_PROMPT_CONTRACT_VERSION,
            "scalar_choice_encoding": "pipe_delimited_strings",
            "semantic_constraints_enforced": True,
            "stages": list(GENERALIZED_STAGE_ORDER),
            "system_owned_beat_action_reuse": True,
            "system_owned_envelope": True,
            "system_owned_observable_text_compilation": True,
        }:
            raise ValueError("第九版提示策略必须固定标量候选编码。")
        strategy_context = value.get("strategy_context")
        if (
            not isinstance(strategy_context, dict)
            or strategy_context.get("change") != "SCALAR_CHOICE_PROMPT_ENCODING"
            or not isinstance(strategy_context.get("previous_execution_id"), str)
            or not strategy_context.get("previous_observations")
        ):
            raise ValueError("第九版试验必须引用第八版数组输出观察。")
    if schema_version == TRIAL_SCHEMA_VERSION_V10:
        if value.get("prompt_strategy") != {
            "assistant_prefill": "{",
            "camera_constraints_enforced": True,
            "choice_glossary_contract_sha256": semantic_choice_glossary_sha256(),
            "choice_glossary_contract_version": SEMANTIC_CHOICE_GLOSSARY_VERSION,
            "compiler_contract_sha256": generalized_compiler_contract_sha256(),
            "compiler_contract_version": GENERALIZED_OBSERVABILITY_COMPILER_VERSION,
            "context_compiler_contract_sha256": (
                tokenized_context_compiler_contract_sha256()
            ),
            "context_compiler_contract_version": TOKENIZED_CONTEXT_COMPILER_VERSION,
            "context_role_constraints_enforced": True,
            "cross_stage_consistency_enforced": True,
            "model_output_scope": "seven_flat_glossed_scalar_choice_stages",
            "prompt_contract_version": PLANNER_SEMANTIC_GLOSS_PROMPT_CONTRACT_VERSION,
            "scalar_choice_encoding": "pipe_delimited_strings",
            "semantic_choice_glossary_enforced": True,
            "semantic_constraints_enforced": True,
            "stages": list(GENERALIZED_STAGE_ORDER),
            "subject_camera_direction_disambiguation": True,
            "system_owned_beat_action_reuse": True,
            "system_owned_envelope": True,
            "system_owned_observable_text_compilation": True,
        }:
            raise ValueError("第十版提示策略必须固定候选释义和主体/相机方向边界。")
        strategy_context = value.get("strategy_context")
        if (
            not isinstance(strategy_context, dict)
            or strategy_context.get("change")
            != "SEMANTIC_CHOICE_GLOSSARY_AND_SUBJECT_CAMERA_DISAMBIGUATION"
            or not isinstance(strategy_context.get("previous_execution_id"), str)
            or not strategy_context.get("previous_observations")
        ):
            raise ValueError("第十版试验必须引用第九版候选位置偏置观察。")
    if schema_version == TRIAL_SCHEMA_VERSION_V11:
        if value.get("prompt_strategy") != {
            "assistant_prefill": "{",
            "camera_constraints_enforced": True,
            "choice_glossary_contract_sha256": semantic_choice_glossary_sha256(),
            "choice_glossary_contract_version": SEMANTIC_CHOICE_GLOSSARY_VERSION,
            "compiler_contract_sha256": generalized_compiler_contract_sha256(),
            "compiler_contract_version": GENERALIZED_OBSERVABILITY_COMPILER_VERSION,
            "context_compiler_contract_sha256": (
                tokenized_context_compiler_contract_sha256()
            ),
            "context_compiler_contract_version": TOKENIZED_CONTEXT_COMPILER_VERSION,
            "context_role_constraints_enforced": True,
            "cross_stage_consistency_enforced": True,
            "field_ownership_enforced": True,
            "held_out_observation_input": False,
            "hybrid_merge_contract_sha256": hybrid_merge_contract_sha256(),
            "hybrid_merge_contract_version": HYBRID_MERGE_CONTRACT_VERSION,
            "model_may_write_locked_fields": False,
            "model_output_scope": "seven_flat_hybrid_residual_stages",
            "prompt_contract_version": (
                PLANNER_HYBRID_SOURCE_FACT_PROMPT_CONTRACT_VERSION
            ),
            "scalar_choice_encoding": "pipe_delimited_strings",
            "semantic_choice_glossary_enforced": True,
            "semantic_constraints_enforced": True,
            "source_fact_extractor_contract_sha256": (
                source_fact_extractor_contract_sha256()
            ),
            "source_fact_extractor_contract_version": (
                SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION
            ),
            "source_fact_provenance_required": True,
            "stages": list(GENERALIZED_STAGE_ORDER),
            "subject_camera_direction_disambiguation": True,
            "system_owned_beat_action_reuse": True,
            "system_owned_envelope": True,
            "system_owned_observable_text_compilation": True,
        }:
            raise ValueError("第十一版提示策略必须固定原句事实所有权和混合合并。")
        strategy_context = value.get("strategy_context")
        if (
            not isinstance(strategy_context, dict)
            or strategy_context.get("change")
            != "DETERMINISTIC_SOURCE_FACT_OWNERSHIP_AND_RESIDUAL_MODEL_OUTPUT"
            or not isinstance(strategy_context.get("previous_execution_id"), str)
            or not strategy_context.get("previous_observations")
        ):
            raise ValueError("第十一版试验必须引用第十版语义容量观察。")
    binding = value.get("request_binding")
    if (
        not isinstance(binding, dict)
        or not isinstance(binding.get("request_file"), str)
        or not isinstance(binding.get("request_sha256"), str)
        or len(binding["request_sha256"]) != 64
    ):
        raise ValueError("规划请求绑定无效。")
    return deepcopy(value)


def prompt_contract_version(contract: dict[str, Any]) -> str:
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V11:
        return PLANNER_HYBRID_SOURCE_FACT_PROMPT_CONTRACT_VERSION
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V10:
        return PLANNER_SEMANTIC_GLOSS_PROMPT_CONTRACT_VERSION
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V9:
        return PLANNER_SCALAR_CHOICE_PROMPT_CONTRACT_VERSION
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V8:
        return PLANNER_GENERALIZED_OBSERVABILITY_PROMPT_CONTRACT_VERSION
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V7:
        return PLANNER_TOKENIZED_CONTEXT_PROMPT_CONTRACT_VERSION
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V6:
        return PLANNER_CONTEXT_PROMPT_CONTRACT_VERSION
    if contract["schema_version"] in SEMANTIC_STABILITY_TRIAL_SCHEMA_VERSIONS:
        return PLANNER_OBSERVABLE_PROMPT_CONTRACT_VERSION
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V4:
        return PLANNER_SEMANTIC_PROMPT_CONTRACT_VERSION
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V3:
        return PLANNER_STAGED_PROMPT_CONTRACT_VERSION
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V2:
        return PLANNER_PAYLOAD_PROMPT_CONTRACT_VERSION
    return PLANNER_PROMPT_CONTRACT_VERSION


def validate_request_binding(
    contract: dict[str, Any],
    request: dict[str, Any],
    request_relative_path: str,
) -> None:
    generalized_request = request.get("schema_version") == REQUEST_SCHEMA_VERSION_V2
    generalized_trial = (
        contract.get("schema_version")
        in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS
    )
    if generalized_request != generalized_trial:
        raise LocalTrialError("规划请求版本与本地试验版本边界不一致。")
    binding = contract["request_binding"]
    if binding["request_file"] != request_relative_path:
        raise LocalTrialError("规划请求路径与固定合同不一致。")
    if binding["request_sha256"] != canonical_sha256(request):
        raise LocalTrialError("规划请求内容摘要与固定合同不一致。")


def _binding_observations(
    proposal: Any,
    *,
    expected_proposal_id: str,
    expected_run_id: str,
    contract: dict[str, Any],
) -> list[dict[str, Any]]:
    if not isinstance(proposal, dict):
        return []
    planner = proposal.get("planner") if isinstance(proposal.get("planner"), dict) else {}
    expected = {
        "proposal_id": expected_proposal_id,
        "planner.model_id": contract["model"]["model_id"],
        "planner.model_version": contract["model"]["revision"],
        "planner.prompt_contract_version": prompt_contract_version(contract),
        "planner.run_id": expected_run_id,
        "planner.sampling": {
            "temperature": contract["execution"]["temperature"],
            "seed": contract["execution"]["seed"],
        },
    }
    observed = {
        "proposal_id": proposal.get("proposal_id"),
        "planner.model_id": planner.get("model_id"),
        "planner.model_version": planner.get("model_version"),
        "planner.prompt_contract_version": planner.get("prompt_contract_version"),
        "planner.run_id": planner.get("run_id"),
        "planner.sampling": planner.get("sampling"),
    }
    return [
        {
            "code": "EXECUTION_BINDING_MISMATCH",
            "category": "EVIDENCE",
            "path": f"$.{field}",
            "expected": expected_value,
            "observed": observed[field],
        }
        for field, expected_value in expected.items()
        if observed[field] != expected_value
    ]


def strict_parse_model_output(raw_output: str) -> tuple[Any, dict[str, Any]]:
    try:
        value = json.loads(raw_output.strip())
    except json.JSONDecodeError as exc:
        return raw_output, {
            "parsed": False,
            "error": {
                "line": exc.lineno,
                "column": exc.colno,
                "message": exc.msg,
            },
            "automatic_repair_attempted": False,
        }
    return value, {
        "parsed": True,
        "root_type": type(value).__name__,
        "automatic_repair_attempted": False,
    }


def compile_payload_to_proposal(
    payload: Any,
    request: dict[str, Any],
    contract: dict[str, Any],
    *,
    proposal_id: str,
    run_id: str,
) -> Any:
    """只编译标识、引用和证据封装，不修补模型遗漏的创意字段。"""

    if not isinstance(payload, dict):
        return payload
    subject_ids = request["required_subject_ids"] or ["SUBJECT-001"]
    source_text = request["source_text"]
    raw_scenes = payload.get("scenes") if isinstance(payload.get("scenes"), list) else []
    raw_beats = (
        payload.get("narrative_beats")
        if isinstance(payload.get("narrative_beats"), list)
        else []
    )
    raw_shots = payload.get("shots") if isinstance(payload.get("shots"), list) else []
    generalized_request = request["schema_version"] == REQUEST_SCHEMA_VERSION_V2
    scenes = []
    for index, raw in enumerate(raw_scenes, start=1):
        item = raw if isinstance(raw, dict) else {}
        scenes.append(
            {
                "scene_id": f"SCENE-{index:03d}",
                "ordinal": index,
                "location": item.get("location"),
                "time": item.get("time"),
                "environment": item.get("environment"),
                "continuity_anchors": item.get("continuity_anchors"),
            }
        )
    beats = []
    for index, raw in enumerate(raw_beats, start=1):
        item = raw if isinstance(raw, dict) else {}
        scene_ordinal = item.get("scene_ordinal")
        beats.append(
            {
                "beat_id": f"BEAT-{index:03d}",
                "ordinal": index,
                "scene_id": (
                    f"SCENE-{scene_ordinal:03d}"
                    if isinstance(scene_ordinal, int) and not isinstance(scene_ordinal, bool)
                    else None
                ),
                "source_span": item.get("source_span"),
                "purpose": item.get("purpose"),
                "subject_ids": subject_ids,
                "action": item.get("action"),
            }
        )
    shots = []
    for index, raw in enumerate(raw_shots, start=1):
        item = raw if isinstance(raw, dict) else {}
        scene_ordinal = item.get("scene_ordinal")
        beat_ordinals = item.get("beat_ordinals")
        beat_ids = (
            [
                f"BEAT-{ordinal:03d}"
                for ordinal in beat_ordinals
                if isinstance(ordinal, int) and not isinstance(ordinal, bool)
            ]
            if isinstance(beat_ordinals, list)
            else beat_ordinals
        )
        compiled_shot = {
                "shot_id": f"SHOT-{index:03d}",
                "ordinal": index,
                "scene_id": (
                    f"SCENE-{scene_ordinal:03d}"
                    if isinstance(scene_ordinal, int) and not isinstance(scene_ordinal, bool)
                    else None
                ),
                "beat_ids": beat_ids,
                "script_segment": source_text,
                "primary_purpose": item.get("primary_purpose"),
                "target_duration_seconds": item.get("target_duration_seconds"),
                "framing": item.get("framing"),
                "subject_ids": subject_ids,
                "action": {
                    "class": item.get("action_class"),
                    "description": item.get("action_description"),
                },
                "composition": item.get("composition"),
                "camera": {
                    "movement": item.get("camera_movement"),
                    "direction": item.get("camera_direction"),
                    "speed": item.get("camera_speed"),
                },
                "lighting": item.get("lighting"),
                "continuity_in": item.get("continuity_in"),
                "continuity_out": item.get("continuity_out"),
                "observable_checks": item.get("observable_checks"),
            }
        if generalized_request:
            compiled_shot["performance"] = item.get("performance")
        else:
            compiled_shot["emotion"] = item.get("emotion")
        shots.append(compiled_shot)
    return {
        "schema_version": (
            PROPOSAL_SCHEMA_VERSION_V2 if generalized_request else PROPOSAL_SCHEMA_VERSION
        ),
        "proposal_id": proposal_id,
        "request_id": request["request_id"],
        "source_text_sha256": canonical_sha256(source_text),
        "status": "DRAFT_NON_AUTHORITATIVE",
        "planner": {
            "model_id": contract["model"]["model_id"],
            "model_version": contract["model"]["revision"],
            "prompt_contract_version": prompt_contract_version(contract),
            "run_id": run_id,
            "sampling": {
                "temperature": contract["execution"]["temperature"],
                "seed": contract["execution"]["seed"],
            },
        },
        "scenes": scenes,
        "narrative_beats": beats,
        "shots": shots,
    }


STAGE_KEYS: dict[str, frozenset[str]] = {
    "scene": frozenset({"location", "time", "environment", "continuity_anchor"}),
    "beat": frozenset({"purpose", "action"}),
    "shot": frozenset(
        {
            "primary_purpose",
            "framing",
            "action_class",
            "action_description",
            "composition",
            "camera_movement",
            "camera_direction",
            "camera_speed",
            "emotion",
            "lighting",
            "continuity_in",
            "continuity_out",
            "observable_check",
        }
    ),
    **STRUCTURED_STAGE_REQUIRED_KEYS,
    **TOKENIZED_CONTEXT_STAGE_KEYS,
}


def observe_stage_payload(
    stage: str,
    payload: Any,
    *,
    request: dict[str, Any] | None = None,
    compiler_version: str | None = None,
) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    generalized = compiler_version == GENERALIZED_OBSERVABILITY_COMPILER_VERSION
    expected_keys = (
        GENERALIZED_STAGE_REQUIRED_KEYS[stage]
        if generalized and stage in GENERALIZED_STAGE_REQUIRED_KEYS
        else STAGE_KEYS[stage]
    )
    if not isinstance(payload, dict):
        return [
            {
                "code": "STAGE_PAYLOAD_NOT_OBJECT",
                "category": "STRUCTURE",
                "path": f"$.stages.{stage}",
                "expected": "object",
                "observed": type(payload).__name__,
            }
        ]
    if set(payload) != expected_keys:
        observations.append(
            {
                "code": "STAGE_KEYS_MISMATCH",
                "category": "STRUCTURE",
                "path": f"$.stages.{stage}",
                "expected": sorted(expected_keys),
                "observed": sorted(payload),
            }
        )
    for key in expected_keys & set(payload):
        if not isinstance(payload[key], str) or not payload[key].strip():
            observations.append(
                {
                    "code": "STAGE_VALUE_NOT_NONEMPTY_STRING",
                    "category": "STRUCTURE",
                    "path": f"$.stages.{stage}.{key}",
                    "expected": "non-empty string",
                    "observed": payload[key],
                }
            )
    stage_allowed_dictionary = (
        GENERALIZED_STAGE_ALLOWED_VALUES
        if generalized
        else STRUCTURED_STAGE_ALLOWED_VALUES
    )
    allowed_fields = {
        key: tuple(values)
        for key, values in stage_allowed_dictionary.get(stage, {}).items()
    }
    constraints = request.get("semantic_constraints") if isinstance(request, dict) else None
    request_controlled_values = (
        request.get("controlled_stage_allowed_values")
        if isinstance(request, dict)
        else None
    )
    request_context_values = (
        request.get("controlled_context_allowed_values")
        if isinstance(request, dict)
        else None
    )
    request_context_token_values = (
        request.get("controlled_context_token_values")
        if isinstance(request, dict)
        else None
    )
    if stage == "scene_context" and isinstance(request_context_token_values, dict):
        allowed_fields.update(
            {
                key: tuple(values)
                for key, values in request_context_token_values[stage].items()
            }
        )
    if stage == "beat_purpose" and isinstance(constraints, dict):
        allowed_fields["purpose"] = tuple(constraints["allowed_primary_purposes"])
    if stage in {"scene", "beat"} and isinstance(request_context_values, dict):
        allowed_fields.update(
            {
                key: tuple(values)
                for key, values in request_context_values[stage].items()
            }
        )
    if stage in stage_allowed_dictionary and stage != "shot_core" and isinstance(
        request_controlled_values, dict
    ):
        allowed_fields = {
            key: tuple(values)
            for key, values in request_controlled_values[stage].items()
        }
    if isinstance(constraints, dict):
        if stage == "beat":
            allowed_fields["purpose"] = tuple(constraints["allowed_primary_purposes"])
        elif stage == "shot_core":
            allowed_fields["primary_purpose"] = tuple(
                constraints["allowed_primary_purposes"]
            )
            allowed_fields["framing"] = tuple(constraints["allowed_framings"])
            allowed_fields["action_class"] = tuple(constraints["allowed_action_classes"])
            optional_camera_constraints = {
                "camera_movement": "allowed_camera_movements",
                "camera_direction": "allowed_camera_directions",
                "camera_speed": "allowed_camera_speeds",
            }
            for stage_field, constraint_field in optional_camera_constraints.items():
                if constraint_field in constraints:
                    allowed_fields[stage_field] = tuple(constraints[constraint_field])
    for key, allowed_values in allowed_fields.items():
        if key in payload and payload[key] not in allowed_values:
            observations.append(
                {
                    "code": "STAGE_ENUM_VALUE_INVALID",
                    "category": "SEMANTIC",
                    "path": f"$.stages.{stage}.{key}",
                    "expected": list(allowed_values),
                    "observed": payload[key],
                }
            )
    if isinstance(constraints, dict):
        required_terms: list[str] = []
        observed_field: str | None = None
        if stage == "scene":
            required_terms = constraints["required_environment_terms"]
            observed_field = "environment"
        elif stage == "beat":
            required_terms = constraints["required_action_terms"]
            observed_field = "action"
        elif stage == "shot_core":
            required_terms = constraints["required_action_terms"]
            observed_field = "action_description"
        if observed_field is not None:
            observed_text = str(payload.get(observed_field, ""))
            for term in required_terms:
                if term not in observed_text:
                    observations.append(
                        {
                            "code": "STAGE_REQUIRED_TERM_MISSING",
                            "category": "SEMANTIC",
                            "path": f"$.stages.{stage}.{observed_field}",
                            "expected": term,
                            "observed": observed_text,
                        }
                    )
    if stage == "shot_core" and payload.get("camera_movement") == "STATIC" and (
        payload.get("camera_direction") != "NONE"
        or payload.get("camera_speed") != "NONE"
    ):
        observations.append(
            {
                "code": "STAGE_STATIC_CAMERA_HAS_MOTION",
                "category": "CAMERA",
                "path": "$.stages.shot_core",
                "expected": {"camera_direction": "NONE", "camera_speed": "NONE"},
                "observed": {
                    "camera_direction": payload.get("camera_direction"),
                    "camera_speed": payload.get("camera_speed"),
                },
            }
        )
    camera_direction_compatibility = {
        "PAN": {"LEFT", "RIGHT"},
        "TILT": {"UP", "DOWN"},
        "DOLLY": {"IN", "OUT"},
        "TRUCK": {"LEFT", "RIGHT"},
        "PEDESTAL": {"UP", "DOWN"},
        "ZOOM": {"IN", "OUT"},
        "ARC": {"LEFT", "RIGHT"},
        "HANDHELD": {"NONE", "LEFT", "RIGHT", "UP", "DOWN", "IN", "OUT"},
    }
    movement = payload.get("camera_movement")
    if stage == "shot_core" and movement in camera_direction_compatibility and payload.get(
        "camera_direction"
    ) not in camera_direction_compatibility[movement]:
        observations.append(
            {
                "code": "STAGE_CAMERA_DIRECTION_INCOMPATIBLE",
                "category": "CAMERA",
                "path": "$.stages.shot_core.camera_direction",
                "expected": sorted(camera_direction_compatibility[movement]),
                "observed": payload.get("camera_direction"),
            }
        )
    if stage == "shot_core" and movement != "STATIC" and payload.get("camera_speed") == "NONE":
        observations.append(
            {
                "code": "STAGE_MOVING_CAMERA_SPEED_NONE",
                "category": "CAMERA",
                "path": "$.stages.shot_core.camera_speed",
                "expected": ["SLOW", "MODERATE", "FAST"],
                "observed": "NONE",
            }
        )
    return observations


def _prepare_stage_payload(
    contract: dict[str, Any],
    request: dict[str, Any],
    stage: str,
    model_payload: Any,
    source_extraction: dict[str, Any] | None,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]], dict[str, Any] | None]:
    """把模型原始阶段载荷转换为可观察的规范阶段载荷。"""

    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V11:
        if source_extraction is None:
            raise LocalTrialError("第十一版运行缺少原句事实提取。")
        merged, merge_observations, merge_document = merge_hybrid_stage_payload(
            stage, model_payload, source_extraction
        )
        observations = list(merge_observations)
        if isinstance(merged, dict):
            observations.extend(
                observe_stage_payload(
                    stage,
                    merged,
                    request=request,
                    compiler_version=contract["prompt_strategy"].get(
                        "compiler_contract_version"
                    ),
                )
            )
        return merged, observations, merge_document
    observations = observe_stage_payload(
        stage,
        model_payload,
        request=(
            request
            if contract["schema_version"] in SEMANTIC_STABILITY_TRIAL_SCHEMA_VERSIONS
            else None
        ),
        compiler_version=contract["prompt_strategy"].get(
            "compiler_contract_version"
        ),
    )
    return model_payload if isinstance(model_payload, dict) else None, observations, None


def compile_stages_to_proposal(
    stages: dict[str, dict[str, Any]],
    request: dict[str, Any],
    contract: dict[str, Any],
    *,
    proposal_id: str,
    run_id: str,
) -> dict[str, Any]:
    scene = stages["scene"]
    beat = stages["beat"]
    shot = stages["shot"]
    payload = {
        "scenes": [
            {
                "location": scene.get("location"),
                "time": scene.get("time"),
                "environment": scene.get("environment"),
                "continuity_anchors": [scene.get("continuity_anchor")],
            }
        ],
        "narrative_beats": [
            {
                "scene_ordinal": 1,
                "source_span": {
                    "start": 0,
                    "end": len(request["source_text"]),
                    "quote": request["source_text"],
                },
                "purpose": beat.get("purpose"),
                "action": beat.get("action"),
            }
        ],
        "shots": [
            {
                "scene_ordinal": 1,
                "beat_ordinals": [1],
                "primary_purpose": shot.get("primary_purpose"),
                "target_duration_seconds": request["target_duration_seconds"],
                "framing": shot.get("framing"),
                "action_class": shot.get("action_class"),
                "action_description": shot.get("action_description"),
                "composition": shot.get("composition"),
                "camera_movement": shot.get("camera_movement"),
                "camera_direction": shot.get("camera_direction"),
                "camera_speed": shot.get("camera_speed"),
                "emotion": shot.get("emotion"),
                "lighting": shot.get("lighting"),
                "continuity_in": shot.get("continuity_in"),
                "continuity_out": shot.get("continuity_out"),
                "observable_checks": [shot.get("observable_check")],
            }
        ],
    }
    return compile_payload_to_proposal(
        payload,
        request,
        contract,
        proposal_id=proposal_id,
        run_id=run_id,
    )


def _compiled_stage_text(
    stage: str,
    payload: dict[str, Any],
    fields: tuple[str, ...],
) -> str:
    return "，".join(
        describe_token(stage, field, str(payload.get(field, ""))) for field in fields
    )


def _compiled_camera_check(core: dict[str, Any]) -> str:
    if (
        core.get("camera_movement") == "STATIC"
        and core.get("camera_direction") == "NONE"
        and core.get("camera_speed") == "NONE"
    ):
        return "相机保持静止，方向和速度均不发生漂移"
    return (
        f"相机运动保持 {core.get('camera_movement')}，"
        f"方向保持 {core.get('camera_direction')}，"
        f"速度保持 {core.get('camera_speed')}"
    )


def _compiled_framing_check(
    core: dict[str, Any], composition: dict[str, Any]
) -> str:
    framing = {
        "CLOSE_UP": "特写",
        "EXTREME_CLOSE_UP": "极近特写",
    }.get(str(core.get("framing")), str(core.get("framing")))
    face_coverage = describe_token(
        "composition", "face_coverage", str(composition.get("face_coverage", ""))
    )
    return f"景别保持为{framing}，{face_coverage}"


def _compiled_action_check(
    core: dict[str, Any], performance: dict[str, Any]
) -> str:
    action = str(core.get("action_description", ""))
    tear_state = describe_token(
        "performance", "tear_state", str(performance.get("tear_state", ""))
    )
    return f"主要动作保持为{action}，同时可观察到{tear_state}"


def _compiled_environment_check(
    scene: dict[str, Any], continuity: dict[str, Any]
) -> str:
    entry = describe_token(
        "continuity",
        "entry_environment_state",
        str(continuity.get("entry_environment_state", "")),
    )
    exit_state = describe_token(
        "continuity",
        "exit_environment_state",
        str(continuity.get("exit_environment_state", "")),
    )
    return f"场景环境保持{scene.get('environment')}，{entry}并且{exit_state}"


def compile_observable_stages_to_proposal(
    stages: dict[str, dict[str, Any]],
    request: dict[str, Any],
    contract: dict[str, Any],
    *,
    proposal_id: str,
    run_id: str,
) -> dict[str, Any]:
    """只展开模型选出的受控语义，不自动修补或新增创作事实。"""

    scene = stages["scene"]
    beat = stages["beat"]
    core = stages["shot_core"]
    composition = stages["composition"]
    performance = stages["performance"]
    lighting = stages["lighting"]
    continuity = stages["continuity"]
    payload = {
        "scenes": [
            {
                "location": scene.get("location"),
                "time": scene.get("time"),
                "environment": scene.get("environment"),
                "continuity_anchors": [scene.get("continuity_anchor")],
            }
        ],
        "narrative_beats": [
            {
                "scene_ordinal": 1,
                "source_span": {
                    "start": 0,
                    "end": len(request["source_text"]),
                    "quote": request["source_text"],
                },
                "purpose": beat.get("purpose"),
                "action": beat.get("action"),
            }
        ],
        "shots": [
            {
                "scene_ordinal": 1,
                "beat_ordinals": [1],
                "primary_purpose": core.get("primary_purpose"),
                "target_duration_seconds": request["target_duration_seconds"],
                "framing": core.get("framing"),
                "action_class": core.get("action_class"),
                "action_description": core.get("action_description"),
                "composition": _compiled_stage_text(
                    "composition",
                    composition,
                    (
                        "subject_placement",
                        "face_coverage",
                        "focus_target",
                        "background_visibility",
                    ),
                ),
                "camera_movement": core.get("camera_movement"),
                "camera_direction": core.get("camera_direction"),
                "camera_speed": core.get("camera_speed"),
                "emotion": _compiled_stage_text(
                    "performance",
                    performance,
                    ("eye_state", "tear_state", "mouth_state", "expression_intensity"),
                ),
                "lighting": _compiled_stage_text(
                    "lighting",
                    lighting,
                    ("light_source", "light_quality", "face_readability", "tear_highlight"),
                ),
                "continuity_in": "进入镜头时，"
                + _compiled_stage_text(
                    "continuity",
                    continuity,
                    ("entry_subject_state", "entry_environment_state"),
                ),
                "continuity_out": "离开镜头时，"
                + _compiled_stage_text(
                    "continuity",
                    continuity,
                    ("exit_subject_state", "exit_environment_state"),
                ),
                "observable_checks": [
                    "主体 "
                    + "、".join(request["required_subject_ids"] or ["SUBJECT-001"])
                    + " 始终保持同一可见身份与面部连续性",
                    _compiled_framing_check(core, composition),
                    _compiled_action_check(core, performance),
                    _compiled_environment_check(scene, continuity),
                    _compiled_camera_check(core),
                ],
            }
        ],
    }
    return compile_payload_to_proposal(
        payload,
        request,
        contract,
        proposal_id=proposal_id,
        run_id=run_id,
    )


def compile_tokenized_context_stages_to_proposal(
    stages: dict[str, dict[str, Any]],
    request: dict[str, Any],
    contract: dict[str, Any],
    *,
    proposal_id: str,
    run_id: str,
) -> dict[str, Any]:
    """展开场景标记，并复用镜头核心阶段的完整动作描述。"""

    context = stages["scene_context"]
    core = stages["shot_core"]
    normalized_stages = {
        "scene": {
            field: describe_context_token(field, str(context.get(field, "")))
            for field in TOKENIZED_CONTEXT_STAGE_KEYS["scene_context"]
        },
        "beat": {
            "purpose": stages["beat_purpose"].get("purpose"),
            "action": core.get("action_description"),
        },
        "shot_core": core,
        "composition": stages["composition"],
        "performance": stages["performance"],
        "lighting": stages["lighting"],
        "continuity": stages["continuity"],
    }
    return compile_observable_stages_to_proposal(
        normalized_stages,
        request,
        contract,
        proposal_id=proposal_id,
        run_id=run_id,
    )


def compile_generalized_stages_to_proposal(
    stages: dict[str, dict[str, Any]],
    request: dict[str, Any],
    contract: dict[str, Any],
    *,
    proposal_id: str,
    run_id: str,
) -> dict[str, Any]:
    """把第八版通用受控标记编译成第二版非权威提案。"""

    return compile_payload_to_proposal(
        build_generalized_payload(stages, request),
        request,
        contract,
        proposal_id=proposal_id,
        run_id=run_id,
    )


def _build_staged_prompt(
    contract: dict[str, Any],
    request: dict[str, Any],
    stage: str,
) -> dict[str, Any]:
    """按试验版本确定性重建阶段提示，供运行器和校验器共用。"""

    schema_version = contract["schema_version"]
    if schema_version == TRIAL_SCHEMA_VERSION_V11:
        return build_local_planner_hybrid_stage_prompt(request, stage)
    if schema_version == TRIAL_SCHEMA_VERSION_V10:
        return build_local_planner_semantic_gloss_stage_prompt(request, stage)
    if schema_version == TRIAL_SCHEMA_VERSION_V9:
        return build_local_planner_scalar_choice_stage_prompt(request, stage)
    if schema_version == TRIAL_SCHEMA_VERSION_V8:
        return build_local_planner_generalized_stage_prompt(request, stage)
    if schema_version == TRIAL_SCHEMA_VERSION_V7:
        return build_local_planner_tokenized_context_stage_prompt(request, stage)
    if schema_version == TRIAL_SCHEMA_VERSION_V6:
        return build_local_planner_context_stage_prompt(request, stage)
    if schema_version == TRIAL_SCHEMA_VERSION_V5:
        return build_local_planner_observable_stage_prompt(request, stage)
    return build_local_planner_stage_prompt(request, stage)


def _run_staged_trial(
    contract: dict[str, Any],
    request: dict[str, Any],
    execution_id: str,
    evidence_dir: Path,
    generate: Callable[[dict[str, Any], int], str],
) -> dict[str, Any]:
    if evidence_dir.exists():
        raise LocalTrialError("证据目录已经存在，不得覆盖历史运行。")
    evidence_dir.mkdir(parents=True)
    write_json(evidence_dir / "trial_contract.json", contract)
    write_json(evidence_dir / "planning_request.json", request)
    source_extraction = (
        extract_source_facts(request)
        if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V11
        else None
    )
    if source_extraction is not None:
        if source_extraction["blocking_issue_count"]:
            raise LocalTrialError("原句事实提取存在阻断问题，不能启动第十一版运行。")
        write_json(
            evidence_dir / "source_fact_extractor_contract.json",
            source_fact_extractor_contract(),
        )
        write_json(
            evidence_dir / "hybrid_merge_contract.json",
            hybrid_merge_contract(),
        )
        write_json(
            evidence_dir / "source_fact_extraction.json",
            source_extraction,
        )
        write_json(
            evidence_dir / "field_ownership.json",
            field_ownership_view(source_extraction),
        )
    if contract["schema_version"] in CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
        write_json(evidence_dir / "compiler_contract.json", compiler_contract())
    elif contract["schema_version"] in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
        write_json(
            evidence_dir / "compiler_contract.json", generalized_compiler_contract()
        )
    if contract["schema_version"] in {
        TRIAL_SCHEMA_VERSION_V10,
        TRIAL_SCHEMA_VERSION_V11,
    }:
        write_json(
            evidence_dir / "choice_glossary_contract.json",
            semantic_choice_glossary_contract(),
        )
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V7 or contract[
        "schema_version"
    ] in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
        write_json(
            evidence_dir / "context_compiler_contract.json",
            tokenized_context_compiler_contract(),
        )

    stability_inputs: list[Any] = []
    controlled_stability_inputs: list[dict[str, dict[str, Any]] | None] = []
    run_records: list[dict[str, Any]] = []
    model_call_count = 0
    for run_index in range(1, contract["execution"]["run_count"] + 1):
        proposal_id = f"PROPOSAL-{execution_id}-{run_index:03d}"
        run_id = f"{execution_id}-RUN-{run_index:03d}"
        started_at = utc_now()
        started = time.monotonic()
        stages: dict[str, dict[str, Any]] = {}
        stage_records: list[dict[str, Any]] = []
        stage_observations: list[dict[str, Any]] = []
        raw_outputs: dict[str, str] = {}
        for stage in contract["prompt_strategy"]["stages"]:
            prompt = _build_staged_prompt(contract, request, stage)
            write_json(evidence_dir / f"prompt_{run_index:03d}_{stage}.json", prompt)
            model_call_count += 1
            stage_started = time.monotonic()
            try:
                raw_output = generate(prompt, model_call_count)
                generation_error = None
            except Exception as exc:  # 固定阶段失败不触发额外调用。
                raw_output = ""
                generation_error = {"type": type(exc).__name__, "message": str(exc)}
            raw_outputs[stage] = raw_output
            (evidence_dir / f"raw_output_{run_index:03d}_{stage}.txt").write_text(
                raw_output,
                encoding="utf-8",
            )
            if generation_error is None:
                model_payload, parse_observation = strict_parse_model_output(raw_output)
            else:
                model_payload = raw_output
                parse_observation = {
                    "parsed": False,
                    "generation_error": generation_error,
                    "automatic_repair_attempted": False,
                }
            if (
                contract["schema_version"] == TRIAL_SCHEMA_VERSION_V11
                and isinstance(model_payload, dict)
            ):
                write_json(
                    evidence_dir
                    / f"model_residual_payload_{run_index:03d}_{stage}.json",
                    model_payload,
                )
            payload, payload_observations, merge_document = _prepare_stage_payload(
                contract,
                request,
                stage,
                model_payload,
                source_extraction,
            )
            if merge_document is not None:
                write_json(
                    evidence_dir
                    / f"merge_observation_{run_index:03d}_{stage}.json",
                    merge_document,
                )
            stage_observations.extend(payload_observations)
            if isinstance(payload, dict):
                stages[stage] = payload
                write_json(evidence_dir / f"payload_{run_index:03d}_{stage}.json", payload)
            stage_record = {
                "stage": stage,
                "model_call_index": model_call_count,
                "elapsed_seconds": round(time.monotonic() - stage_started, 6),
                "raw_output_sha256": hashlib.sha256(raw_output.encode("utf-8")).hexdigest(),
                "parse_observation": parse_observation,
                "stage_observation_count": len(payload_observations),
                "generation_error": generation_error,
            }
            stage_records.append(stage_record)
            write_json(
                evidence_dir / f"stage_observation_{run_index:03d}_{stage}.json",
                {
                    "stage": stage,
                    "parse_observation": parse_observation,
                    "observations": payload_observations,
                    "formal_decision_created": False,
                },
            )
        all_stages_present = set(stages) == set(contract["prompt_strategy"]["stages"])
        cross_stage_observations = (
            observe_generalized_stage_consistency(stages)
            if contract["schema_version"]
            in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS
            and all_stages_present
            and not stage_observations
            else []
        )
        if contract["schema_version"] in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
            write_json(
                evidence_dir / f"cross_stage_observation_{run_index:03d}.json",
                {
                    "observations": cross_stage_observations,
                    "formal_decision_created": False,
                },
            )
        all_stage_contracts_observable = (
            all_stages_present
            and not stage_observations
            and not cross_stage_observations
        )
        if all_stages_present and (
            contract["schema_version"]
            not in SEMANTIC_STABILITY_TRIAL_SCHEMA_VERSIONS
            or all_stage_contracts_observable
        ):
            if (
                contract["schema_version"]
                in SEMANTIC_STABILITY_TRIAL_SCHEMA_VERSIONS
            ):
                if contract["schema_version"] in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
                    proposal = compile_generalized_stages_to_proposal(
                        stages,
                        request,
                        contract,
                        proposal_id=proposal_id,
                        run_id=run_id,
                    )
                elif contract["schema_version"] == TRIAL_SCHEMA_VERSION_V7:
                    proposal = compile_tokenized_context_stages_to_proposal(
                        stages,
                        request,
                        contract,
                        proposal_id=proposal_id,
                        run_id=run_id,
                    )
                else:
                    proposal = compile_observable_stages_to_proposal(
                        stages,
                        request,
                        contract,
                        proposal_id=proposal_id,
                        run_id=run_id,
                    )
            else:
                proposal = compile_stages_to_proposal(
                    stages,
                    request,
                    contract,
                    proposal_id=proposal_id,
                    run_id=run_id,
                )
        else:
            proposal = json.dumps(raw_outputs, ensure_ascii=False, sort_keys=True)
        proposal_observation = observe_proposal(request, proposal)
        binding_observations = _binding_observations(
            proposal,
            expected_proposal_id=proposal_id,
            expected_run_id=run_id,
            contract=contract,
        )
        combined_observations = [
            *stage_observations,
            *cross_stage_observations,
            *binding_observations,
        ]
        if combined_observations:
            proposal_observation["observations"].extend(combined_observations)
            proposal_observation["observation_count"] += len(combined_observations)
            proposal_observation["blocking_observation_count"] += len(combined_observations)
        stability_inputs.append(proposal if not combined_observations else raw_outputs)
        if contract["schema_version"] in SEMANTIC_STABILITY_TRIAL_SCHEMA_VERSIONS:
            controlled_stability_inputs.append(
                deepcopy(stages) if all_stage_contracts_observable else None
            )
        write_json(
            evidence_dir / f"proposal_observation_{run_index:03d}.json",
            proposal_observation,
        )
        if isinstance(proposal, dict):
            write_json(evidence_dir / f"proposal_{run_index:03d}.json", proposal)
        run_records.append(
            {
                "run_index": run_index,
                "proposal_id": proposal_id,
                "run_id": run_id,
                "started_at": started_at,
                "elapsed_seconds": round(time.monotonic() - started, 6),
                "stages": stage_records,
                "all_stages_parsed": all(
                    item["parse_observation"]["parsed"] for item in stage_records
                ),
                "all_stage_contracts_observable": all_stage_contracts_observable,
                "stage_contract_observation_count": len(stage_observations),
                "cross_stage_observation_count": len(cross_stage_observations),
                "proposal_blocking_observation_count": proposal_observation[
                    "blocking_observation_count"
                ],
                "structural_observation_count": proposal_observation[
                    "blocking_observation_count"
                ],
            }
        )

    stability = observe_stability(request, stability_inputs)
    write_json(evidence_dir / "stability_observation.json", stability)
    controlled_stability: dict[str, Any] | None = None
    if contract["schema_version"] in SEMANTIC_STABILITY_TRIAL_SCHEMA_VERSIONS:
        controlled_stability = (
            observe_generalized_semantic_stability(controlled_stability_inputs)
            if contract["schema_version"]
            in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS
            else observe_controlled_semantic_stability(controlled_stability_inputs)
        )
        write_json(
            evidence_dir / "controlled_semantic_stability_observation.json",
            controlled_stability,
        )
    summary = {
        "schema_version": "local-shot-planner-trial-observation.v1",
        "execution_id": execution_id,
        "model_id": contract["model"]["model_id"],
        "model_revision": contract["model"]["revision"],
        "prompt_contract_version": prompt_contract_version(contract),
        "run_count_requested": contract["execution"]["run_count"],
        "run_count_observed": len(run_records),
        "model_call_count_requested": contract["resource_budget"]["maximum_model_calls"],
        "model_call_count_observed": model_call_count,
        "parsed_run_count": sum(item["all_stages_parsed"] for item in run_records),
        "structurally_observable_run_count": sum(
            item["structural_observation_count"] == 0 for item in run_records
        ),
        "comparison_performed": stability["comparison_performed"],
        "largest_exact_structure_group_ratio": stability[
            "largest_exact_structure_group_ratio"
        ],
        "runs": run_records,
        "formal_shot_spec_created": False,
        "formal_quality_acceptance_created": False,
        "creative_review_required": True,
        "automatic_retry_count": 0,
    }
    if controlled_stability is not None:
        summary["controlled_semantic_comparison_performed"] = controlled_stability[
            "comparison_performed"
        ]
        summary[
            "largest_exact_controlled_semantic_group_ratio"
        ] = controlled_stability["largest_exact_controlled_semantic_group_ratio"]
    write_json(evidence_dir / "summary.json", summary)
    return summary


def run_trial(
    contract_value: Any,
    request_value: Any,
    execution_id: str,
    evidence_dir: Path,
    generate: Callable[[dict[str, Any], int], str],
) -> dict[str, Any]:
    contract = validate_trial_contract(contract_value)
    request = validate_request(request_value)
    if canonical_sha256(request) != contract["request_binding"]["request_sha256"]:
        raise LocalTrialError("规划请求内容摘要与固定合同不一致。")
    if contract["schema_version"] in STAGED_TRIAL_SCHEMA_VERSIONS:
        return _run_staged_trial(
            contract,
            request,
            execution_id,
            evidence_dir,
            generate,
        )
    if evidence_dir.exists():
        raise LocalTrialError("证据目录已经存在，不得覆盖历史运行。")
    evidence_dir.mkdir(parents=True)
    write_json(evidence_dir / "trial_contract.json", contract)
    write_json(evidence_dir / "planning_request.json", request)

    stability_inputs: list[Any] = []
    run_records: list[dict[str, Any]] = []
    for run_index in range(1, contract["execution"]["run_count"] + 1):
        proposal_id = f"PROPOSAL-{execution_id}-{run_index:03d}"
        run_id = f"{execution_id}-RUN-{run_index:03d}"
        planner_metadata = {
            "model_id": contract["model"]["model_id"],
            "model_version": contract["model"]["revision"],
            "prompt_contract_version": prompt_contract_version(contract),
            "run_id": run_id,
            "sampling": {
                "temperature": contract["execution"]["temperature"],
                "seed": contract["execution"]["seed"],
            },
        }
        if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V2:
            prompt = build_local_planner_payload_prompt(request)
        else:
            prompt = build_local_planner_prompt(
                request,
                proposal_id=proposal_id,
                planner_metadata=planner_metadata,
            )
        write_json(evidence_dir / f"prompt_{run_index:03d}.json", prompt)
        started_at = utc_now()
        started = time.monotonic()
        try:
            raw_output = generate(prompt, run_index)
            generation_error = None
        except Exception as exc:  # 单次失败形成观察；下一编号运行不是重试。
            raw_output = ""
            generation_error = {"type": type(exc).__name__, "message": str(exc)}
        elapsed_seconds = round(time.monotonic() - started, 6)
        (evidence_dir / f"raw_output_{run_index:03d}.txt").write_text(
            raw_output,
            encoding="utf-8",
        )
        if generation_error is None:
            parsed_output, parse_observation = strict_parse_model_output(raw_output)
            if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V2:
                if isinstance(parsed_output, dict):
                    write_json(evidence_dir / f"payload_{run_index:03d}.json", parsed_output)
                proposal = compile_payload_to_proposal(
                    parsed_output,
                    request,
                    contract,
                    proposal_id=proposal_id,
                    run_id=run_id,
                )
            else:
                proposal = parsed_output
        else:
            proposal = raw_output
            parse_observation = {
                "parsed": False,
                "generation_error": generation_error,
                "automatic_repair_attempted": False,
            }
        proposal_observation = observe_proposal(request, proposal)
        binding_observations = _binding_observations(
            proposal,
            expected_proposal_id=proposal_id,
            expected_run_id=run_id,
            contract=contract,
        )
        if binding_observations:
            proposal_observation["observations"].extend(binding_observations)
            proposal_observation["observation_count"] += len(binding_observations)
            proposal_observation["blocking_observation_count"] += len(binding_observations)
        stability_inputs.append(proposal if not binding_observations else raw_output)
        write_json(
            evidence_dir / f"proposal_observation_{run_index:03d}.json",
            proposal_observation,
        )
        if isinstance(proposal, dict):
            write_json(evidence_dir / f"proposal_{run_index:03d}.json", proposal)
        run_records.append(
            {
                "run_index": run_index,
                "proposal_id": proposal_id,
                "run_id": run_id,
                "started_at": started_at,
                "elapsed_seconds": elapsed_seconds,
                "raw_output_sha256": hashlib.sha256(raw_output.encode("utf-8")).hexdigest(),
                "parse_observation": parse_observation,
                "structural_observation_count": proposal_observation["blocking_observation_count"],
                "generation_error": generation_error,
            }
        )

    stability = observe_stability(request, stability_inputs)
    write_json(evidence_dir / "stability_observation.json", stability)
    summary = {
        "schema_version": "local-shot-planner-trial-observation.v1",
        "execution_id": execution_id,
        "model_id": contract["model"]["model_id"],
        "model_revision": contract["model"]["revision"],
        "prompt_contract_version": prompt_contract_version(contract),
        "run_count_requested": contract["execution"]["run_count"],
        "run_count_observed": len(run_records),
        "parsed_run_count": sum(item["parse_observation"]["parsed"] for item in run_records),
        "structurally_observable_run_count": sum(
            item["structural_observation_count"] == 0 for item in run_records
        ),
        "comparison_performed": stability["comparison_performed"],
        "largest_exact_structure_group_ratio": stability[
            "largest_exact_structure_group_ratio"
        ],
        "runs": run_records,
        "formal_shot_spec_created": False,
        "formal_quality_acceptance_created": False,
        "creative_review_required": True,
        "automatic_retry_count": 0,
    }
    write_json(evidence_dir / "summary.json", summary)
    return summary


def environment_record(
    *,
    execution_id: str,
    repo_root: Path,
    contract_path: Path,
    request_path: Path,
    runner_path: Path,
) -> dict[str, Any]:
    def git_value(*args: str) -> str | None:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return result.stdout.strip() or None if result.returncode == 0 else None

    implementation_relative_paths = (
        "shot_planning/contracts.py",
        "shot_planning/controlled_context.py",
        "shot_planning/evaluation_suite.py",
        "shot_planning/generalized_observability.py",
        "shot_planning/local_trial.py",
        "shot_planning/prompting.py",
        "shot_planning/semantic_choice.py",
        "shot_planning/source_facts.py",
        "shot_planning/stability.py",
        "shot_planning/structured_observability.py",
        "shot_planning/validation.py",
    )
    implementation_sha256 = {
        relative: sha256_file(repo_root / relative)
        for relative in implementation_relative_paths
        if (repo_root / relative).is_file()
    }
    return {
        "execution_id": execution_id,
        "recorded_at": utc_now(),
        "operating_system": platform.system(),
        "operating_system_version": platform.mac_ver()[0],
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "git_head": git_value("rev-parse", "HEAD"),
        "git_status_porcelain": git_value("status", "--porcelain") or "",
        "contract_sha256": sha256_file(contract_path),
        "request_sha256": sha256_file(request_path),
        "runner_sha256": sha256_file(runner_path),
        "implementation_sha256": implementation_sha256,
        "model_id": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "remote_inference_used": False,
        "model_download_may_use_network": True,
        "paid_request": False,
        "formal_fact_creation": "PROHIBITED",
    }


def write_manifest(evidence_dir: Path) -> dict[str, Any]:
    files = []
    for path in sorted(evidence_dir.iterdir()):
        if path.is_file() and path.name != "manifest.json":
            files.append(
                {
                    "path": path.name,
                    "bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
    manifest = {
        "schema_version": "local-shot-planner-evidence-manifest.v1",
        "files": files,
        "formal_fact_creation": False,
    }
    write_json(evidence_dir / "manifest.json", manifest)
    return manifest


def _verify_environment_record(
    evidence_dir: Path,
    environment: Any,
    *,
    execution_id: str,
    contract: dict[str, Any],
    allow_test_environment: bool,
) -> None:
    """核对运行环境的边界字段；测试证据只允许显式最小占位。"""

    if environment == {"test_environment": True}:
        if allow_test_environment:
            return
        raise LocalTrialError("生产证据校验不接受测试环境占位。")
    base_fields = {
        "execution_id",
        "recorded_at",
        "operating_system",
        "operating_system_version",
        "architecture",
        "python_version",
        "git_head",
        "git_status_porcelain",
        "contract_sha256",
        "request_sha256",
        "runner_sha256",
        "model_id",
        "model_revision",
        "remote_inference_used",
        "model_download_may_use_network",
        "paid_request",
        "formal_fact_creation",
    }
    allowed_field_sets = {frozenset(base_fields), frozenset(base_fields | {"implementation_sha256"})}
    if not isinstance(environment, dict) or frozenset(environment) not in allowed_field_sets:
        raise LocalTrialError("运行环境记录字段集合无效。")
    if (
        environment.get("execution_id") != execution_id
        or not isinstance(environment.get("recorded_at"), str)
        or not environment["recorded_at"]
        or environment.get("contract_sha256")
        != sha256_file(evidence_dir / "trial_contract.json")
        or environment.get("request_sha256")
        != sha256_file(evidence_dir / "planning_request.json")
        or not isinstance(environment.get("runner_sha256"), str)
        or len(environment["runner_sha256"]) != 64
        or environment.get("model_id") != contract["model"]["model_id"]
        or environment.get("model_revision") != contract["model"]["revision"]
        or environment.get("remote_inference_used") is not False
        or environment.get("model_download_may_use_network") is not True
        or environment.get("paid_request") is not False
        or environment.get("formal_fact_creation") != "PROHIBITED"
    ):
        raise LocalTrialError("运行环境记录与固定执行边界不一致。")
    implementation = environment.get("implementation_sha256")
    if implementation is not None and (
        not isinstance(implementation, dict)
        or not implementation
        or any(
            not isinstance(path, str)
            or not isinstance(digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", digest)
            for path, digest in implementation.items()
        )
    ):
        raise LocalTrialError("运行环境实现摘要无效。")
    if contract["schema_version"] in {
        TRIAL_SCHEMA_VERSION_V10,
        TRIAL_SCHEMA_VERSION_V11,
    } and (
        not isinstance(implementation, dict)
        or "shot_planning/evaluation_suite.py" not in implementation
    ):
        raise LocalTrialError("第十版及以后运行环境缺少套件汇总器实现摘要。")
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V11 and (
        not isinstance(implementation, dict)
        or "shot_planning/source_facts.py" not in implementation
    ):
        raise LocalTrialError("第十一版运行环境缺少原句事实提取器实现摘要。")


def _observation_documents_equal(left: Any, right: Any) -> bool:
    """观察顺序不承载语义；按完整观察对象的规范 JSON 比较多重集合。"""

    if not isinstance(left, dict) or not isinstance(right, dict):
        return left == right
    left_value = deepcopy(left)
    right_value = deepcopy(right)
    for value in (left_value, right_value):
        observations = value.get("observations")
        if isinstance(observations, list):
            value["observations"] = sorted(
                observations,
                key=lambda item: json.dumps(
                    item, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                ),
            )
    return left_value == right_value


def verify_evidence(
    evidence_dir: Path,
    *,
    allow_test_environment: bool = False,
) -> dict[str, Any]:
    """重新计算本地规划证据包完整性，不创建镜头或质量裁决。"""

    manifest = json.loads((evidence_dir / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != "local-shot-planner-evidence-manifest.v1":
        raise LocalTrialError("证据清单版本无效。")
    if manifest.get("formal_fact_creation") is not False:
        raise LocalTrialError("证据清单不得声明正式事实。")
    listed_paths: set[str] = set()
    for item in manifest.get("files", []):
        relative = item.get("path")
        if not isinstance(relative, str) or Path(relative).name != relative:
            raise LocalTrialError("证据清单包含无效路径。")
        if relative in listed_paths:
            raise LocalTrialError("证据清单包含重复路径。")
        listed_paths.add(relative)
        path = evidence_dir / relative
        if not path.is_file():
            raise LocalTrialError("证据清单引用的文件不存在。")
        if path.stat().st_size != item.get("bytes") or sha256_file(path) != item.get("sha256"):
            raise LocalTrialError("证据文件大小或摘要不一致。")
    actual_paths = {
        path.name for path in evidence_dir.iterdir() if path.is_file() and path.name != "manifest.json"
    }
    if actual_paths != listed_paths:
        raise LocalTrialError("证据清单没有精确覆盖当前文件集合。")

    contract = validate_trial_contract(
        json.loads((evidence_dir / "trial_contract.json").read_text(encoding="utf-8"))
    )
    request = validate_request(
        json.loads((evidence_dir / "planning_request.json").read_text(encoding="utf-8"))
    )
    if canonical_sha256(request) != contract["request_binding"]["request_sha256"]:
        raise LocalTrialError("证据中的请求与试验合同摘要不一致。")
    source_extraction: dict[str, Any] | None = None
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V11:
        extractor_contract_path = (
            evidence_dir / "source_fact_extractor_contract.json"
        )
        merge_contract_path = evidence_dir / "hybrid_merge_contract.json"
        extraction_path = evidence_dir / "source_fact_extraction.json"
        ownership_path = evidence_dir / "field_ownership.json"
        if not all(
            path.is_file()
            for path in (
                extractor_contract_path,
                merge_contract_path,
                extraction_path,
                ownership_path,
            )
        ):
            raise LocalTrialError("第十一版证据缺少原句事实或字段所有权合同。")
        observed_extractor_contract = json.loads(
            extractor_contract_path.read_text(encoding="utf-8")
        )
        if (
            observed_extractor_contract != source_fact_extractor_contract()
            or canonical_sha256(observed_extractor_contract)
            != contract["prompt_strategy"][
                "source_fact_extractor_contract_sha256"
            ]
        ):
            raise LocalTrialError("原句事实提取合同无法由固定实现重建。")
        observed_merge_contract = json.loads(
            merge_contract_path.read_text(encoding="utf-8")
        )
        if (
            observed_merge_contract != hybrid_merge_contract()
            or canonical_sha256(observed_merge_contract)
            != contract["prompt_strategy"]["hybrid_merge_contract_sha256"]
        ):
            raise LocalTrialError("混合合并合同无法由固定实现重建。")
        source_extraction = extract_source_facts(request)
        if json.loads(extraction_path.read_text(encoding="utf-8")) != source_extraction:
            raise LocalTrialError("原句事实提取无法由内嵌请求独立重算。")
        if json.loads(ownership_path.read_text(encoding="utf-8")) != field_ownership_view(
            source_extraction
        ):
            raise LocalTrialError("字段所有权无法由原句事实独立重算。")
        if (
            source_extraction["blocking_issue_count"] != 0
            or source_extraction["held_out_observation_used"] is not False
            or source_extraction["formal_decision_created"] is not False
        ):
            raise LocalTrialError("第十一版原句事实越过非权威失败关闭边界。")
    if contract["schema_version"] in SEMANTIC_STABILITY_TRIAL_SCHEMA_VERSIONS:
        compiler_path = evidence_dir / "compiler_contract.json"
        if not compiler_path.is_file():
            raise LocalTrialError("受控可观察试验证据缺少编译合同。")
        observed_compiler_contract = json.loads(compiler_path.read_text(encoding="utf-8"))
        if observed_compiler_contract.get("schema_version") != contract[
            "prompt_strategy"
        ]["compiler_contract_version"]:
            raise LocalTrialError("受控可观察试验的编译合同版本不一致。")
        if canonical_sha256(observed_compiler_contract) != contract["prompt_strategy"][
            "compiler_contract_sha256"
        ]:
            raise LocalTrialError("受控可观察试验的编译合同摘要不一致。")
    if contract["schema_version"] in {
        TRIAL_SCHEMA_VERSION_V10,
        TRIAL_SCHEMA_VERSION_V11,
    }:
        glossary_path = evidence_dir / "choice_glossary_contract.json"
        if not glossary_path.is_file():
            raise LocalTrialError("第十版及以后证据缺少候选释义合同。")
        observed_glossary = json.loads(glossary_path.read_text(encoding="utf-8"))
        if observed_glossary.get("schema_version") != contract[
            "prompt_strategy"
        ]["choice_glossary_contract_version"]:
            raise LocalTrialError("第十版及以后候选释义合同版本不一致。")
        if canonical_sha256(observed_glossary) != contract["prompt_strategy"][
            "choice_glossary_contract_sha256"
        ]:
            raise LocalTrialError("第十版及以后候选释义合同摘要不一致。")
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V7 or contract[
        "schema_version"
    ] in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
        context_compiler_path = evidence_dir / "context_compiler_contract.json"
        if not context_compiler_path.is_file():
            raise LocalTrialError("标记化上下文证据缺少上下文编译合同。")
        observed_context_compiler = json.loads(
            context_compiler_path.read_text(encoding="utf-8")
        )
        if observed_context_compiler.get("schema_version") != contract[
            "prompt_strategy"
        ]["context_compiler_contract_version"]:
            raise LocalTrialError("标记化上下文编译合同版本不一致。")
        if canonical_sha256(observed_context_compiler) != contract[
            "prompt_strategy"
        ]["context_compiler_contract_sha256"]:
            raise LocalTrialError("标记化上下文编译合同摘要不一致。")
    summary = json.loads((evidence_dir / "summary.json").read_text(encoding="utf-8"))
    stability = json.loads(
        (evidence_dir / "stability_observation.json").read_text(encoding="utf-8")
    )
    if summary.get("run_count_requested") != contract["execution"]["run_count"]:
        raise LocalTrialError("摘要中的请求运行次数不一致。")
    if summary.get("run_count_observed") != len(summary.get("runs", [])):
        raise LocalTrialError("摘要中的实际运行次数不一致。")
    if summary.get("run_count_observed") != contract["execution"]["run_count"]:
        raise LocalTrialError("摘要中的实际运行次数没有满足固定合同。")
    if summary.get("model_id") != contract["model"]["model_id"]:
        raise LocalTrialError("摘要中的模型标识不一致。")
    if summary.get("model_revision") != contract["model"]["revision"]:
        raise LocalTrialError("摘要中的模型修订不一致。")
    observed_prompt_contract_version = summary.get(
        "prompt_contract_version",
        PLANNER_PROMPT_CONTRACT_VERSION
        if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V1
        else None,
    )
    if observed_prompt_contract_version != prompt_contract_version(contract):
        raise LocalTrialError("摘要中的提示合同版本不一致。")
    if summary.get("automatic_retry_count") != 0:
        raise LocalTrialError("证据包出现合同外自动重试。")
    if summary.get("formal_shot_spec_created") is not False:
        raise LocalTrialError("摘要越权声明正式镜头规格。")
    if summary.get("formal_quality_acceptance_created") is not False:
        raise LocalTrialError("摘要越权声明质量接受。")
    environment_path = evidence_dir / "environment.json"
    if environment_path.is_file():
        _verify_environment_record(
            evidence_dir,
            json.loads(environment_path.read_text(encoding="utf-8")),
            execution_id=summary.get("execution_id"),
            contract=contract,
            allow_test_environment=allow_test_environment,
        )
    if stability.get("formal_decision_created") is not False:
        raise LocalTrialError("稳定性观察越权声明正式裁决。")
    staged = contract["schema_version"] in STAGED_TRIAL_SCHEMA_VERSIONS
    if staged and summary.get("parsed_run_count") != sum(
        run.get("all_stages_parsed") is True for run in summary["runs"]
    ):
        raise LocalTrialError("摘要中的解析运行数量无法由逐运行记录重算。")
    if staged:
        expected_call_count = contract["resource_budget"]["maximum_model_calls"]
        if summary.get("model_call_count_requested") != expected_call_count:
            raise LocalTrialError("摘要中的模型调用预算不一致。")
        if summary.get("model_call_count_observed") != expected_call_count:
            raise LocalTrialError("摘要中的实际模型调用次数不一致。")
    expected_call_index = 1
    expected_run_indices = list(range(1, contract["execution"]["run_count"] + 1))
    if [run.get("run_index") for run in summary["runs"]] != expected_run_indices:
        raise LocalTrialError("摘要中的运行编号不连续。")
    recomputed_stability_inputs: list[Any] = []
    recomputed_controlled_inputs: list[dict[str, dict[str, Any]] | None] = []
    for run in summary["runs"]:
        run_index = run["run_index"]
        if staged:
            stage_records = run.get("stages")
            if not isinstance(stage_records, list) or [
                item.get("stage") for item in stage_records if isinstance(item, dict)
            ] != contract["prompt_strategy"]["stages"]:
                raise LocalTrialError("逐运行阶段顺序与固定合同不一致。")
            stages: dict[str, dict[str, Any]] = {}
            raw_outputs: dict[str, str] = {}
            combined_stage_observations: list[dict[str, Any]] = []
            for stage_record in run["stages"]:
                stage = stage_record["stage"]
                if set(stage_record) != {
                    "stage",
                    "model_call_index",
                    "elapsed_seconds",
                    "raw_output_sha256",
                    "parse_observation",
                    "stage_observation_count",
                    "generation_error",
                }:
                    raise LocalTrialError("阶段运行记录字段集合无效。")
                if stage_record.get("model_call_index") != expected_call_index:
                    raise LocalTrialError("阶段模型调用编号不连续。")
                if not isinstance(stage_record.get("elapsed_seconds"), (int, float)) or (
                    isinstance(stage_record.get("elapsed_seconds"), bool)
                    or stage_record["elapsed_seconds"] < 0
                ):
                    raise LocalTrialError("阶段耗时记录无效。")
                expected_call_index += 1
                prompt_path = evidence_dir / f"prompt_{run_index:03d}_{stage}.json"
                raw_path = evidence_dir / f"raw_output_{run_index:03d}_{stage}.txt"
                observation_path = (
                    evidence_dir / f"stage_observation_{run_index:03d}_{stage}.json"
                )
                if not prompt_path.is_file() or not observation_path.is_file():
                    raise LocalTrialError("缺少阶段提示或阶段观察文件。")
                prompt = json.loads(prompt_path.read_text(encoding="utf-8"))
                if prompt != _build_staged_prompt(contract, request, stage):
                    raise LocalTrialError("阶段提示与确定性固定合同不一致。")
                if not raw_path.is_file():
                    raise LocalTrialError("缺少阶段原始输出文件。")
                if sha256_file(raw_path) != stage_record["raw_output_sha256"]:
                    raise LocalTrialError("阶段原始输出摘要不一致。")
                raw_output = raw_path.read_text(encoding="utf-8")
                raw_outputs[stage] = raw_output
                generation_error = stage_record.get("generation_error")
                if generation_error is None:
                    model_payload, parse_observation = strict_parse_model_output(
                        raw_output
                    )
                else:
                    if not isinstance(generation_error, dict) or raw_output != "":
                        raise LocalTrialError("阶段生成错误记录与原始输出不一致。")
                    model_payload = raw_output
                    parse_observation = {
                        "parsed": False,
                        "generation_error": generation_error,
                        "automatic_repair_attempted": False,
                    }
                if stage_record.get("parse_observation") != parse_observation:
                    raise LocalTrialError("阶段解析观察无法由原始输出重算。")
                residual_path = (
                    evidence_dir
                    / f"model_residual_payload_{run_index:03d}_{stage}.json"
                )
                if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V11:
                    if isinstance(model_payload, dict):
                        if not residual_path.is_file() or json.loads(
                            residual_path.read_text(encoding="utf-8")
                        ) != model_payload:
                            raise LocalTrialError(
                                "模型残余载荷无法由原始输出重算。"
                            )
                    elif residual_path.exists():
                        raise LocalTrialError(
                            "未解析的模型输出不得保留残余载荷对象。"
                        )
                payload, payload_observations, merge_document = (
                    _prepare_stage_payload(
                        contract,
                        request,
                        stage,
                        model_payload,
                        source_extraction,
                    )
                )
                merge_path = (
                    evidence_dir
                    / f"merge_observation_{run_index:03d}_{stage}.json"
                )
                if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V11:
                    if (
                        merge_document is None
                        or not merge_path.is_file()
                        or not _observation_documents_equal(
                            json.loads(merge_path.read_text(encoding="utf-8")),
                            merge_document,
                        )
                    ):
                        raise LocalTrialError("混合合并观察无法独立重算。")
                elif merge_path.exists():
                    raise LocalTrialError("历史试验不得包含第十一版混合合并观察。")
                expected_stage_observation = {
                    "stage": stage,
                    "parse_observation": parse_observation,
                    "observations": payload_observations,
                    "formal_decision_created": False,
                }
                actual_stage_observation = json.loads(
                    observation_path.read_text(encoding="utf-8")
                )
                generalized_trial = (
                    contract["schema_version"]
                    in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS
                )
                if generalized_trial and not _observation_documents_equal(
                    actual_stage_observation, expected_stage_observation
                ):
                    raise LocalTrialError("阶段观察文件无法由原始输出重算。")
                if generalized_trial:
                    payload_observations = actual_stage_observation["observations"]
                if not generalized_trial:
                    if (
                        actual_stage_observation.get("stage") != stage
                        or actual_stage_observation.get("parse_observation")
                        != parse_observation
                        or not isinstance(
                            actual_stage_observation.get("observations"), list
                        )
                        or actual_stage_observation.get("formal_decision_created")
                        is not False
                    ):
                        raise LocalTrialError("历史阶段观察与解析证据不一致。")
                    payload_observations = actual_stage_observation["observations"]
                if stage_record.get("stage_observation_count") != len(
                    payload_observations
                ):
                    raise LocalTrialError("阶段观察数量与逐阶段证据不一致。")
                combined_stage_observations.extend(payload_observations)
                payload_path = evidence_dir / f"payload_{run_index:03d}_{stage}.json"
                if isinstance(payload, dict):
                    if not payload_path.is_file() or json.loads(
                        payload_path.read_text(encoding="utf-8")
                    ) != payload:
                        raise LocalTrialError("阶段载荷文件无法由原始输出重算。")
                    stages[stage] = payload
                elif payload_path.exists():
                    raise LocalTrialError("未解析为对象的阶段不得保留载荷文件。")
            all_stages_present = set(stages) == set(
                contract["prompt_strategy"]["stages"]
            )
            cross_stage_observations = (
                observe_generalized_stage_consistency(stages)
                if contract["schema_version"]
                in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS
                and all_stages_present
                and not combined_stage_observations
                else []
            )
            if contract["schema_version"] in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
                cross_stage_path = (
                    evidence_dir / f"cross_stage_observation_{run_index:03d}.json"
                )
                if not cross_stage_path.is_file():
                    raise LocalTrialError("第八版证据缺少跨阶段一致性观察。")
                cross_stage = json.loads(cross_stage_path.read_text(encoding="utf-8"))
                if not _observation_documents_equal(
                    cross_stage,
                    {
                        "observations": cross_stage_observations,
                        "formal_decision_created": False,
                    },
                ):
                    raise LocalTrialError("跨阶段观察无法由阶段载荷重算。")
                cross_stage_observations = cross_stage["observations"]
            all_stage_contracts_observable = (
                all_stages_present
                and not combined_stage_observations
                and not cross_stage_observations
            )
            proposal_id = f"PROPOSAL-{summary['execution_id']}-{run_index:03d}"
            run_id = f"{summary['execution_id']}-RUN-{run_index:03d}"
            if all_stages_present and (
                contract["schema_version"]
                not in SEMANTIC_STABILITY_TRIAL_SCHEMA_VERSIONS
                or all_stage_contracts_observable
            ):
                if contract["schema_version"] in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
                    proposal = compile_generalized_stages_to_proposal(
                        stages,
                        request,
                        contract,
                        proposal_id=proposal_id,
                        run_id=run_id,
                    )
                elif contract["schema_version"] == TRIAL_SCHEMA_VERSION_V7:
                    proposal = compile_tokenized_context_stages_to_proposal(
                        stages,
                        request,
                        contract,
                        proposal_id=proposal_id,
                        run_id=run_id,
                    )
                elif contract["schema_version"] in CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
                    proposal = compile_observable_stages_to_proposal(
                        stages,
                        request,
                        contract,
                        proposal_id=proposal_id,
                        run_id=run_id,
                    )
                else:
                    proposal = compile_stages_to_proposal(
                        stages,
                        request,
                        contract,
                        proposal_id=proposal_id,
                        run_id=run_id,
                    )
            else:
                proposal = json.dumps(raw_outputs, ensure_ascii=False, sort_keys=True)
            proposal_path = evidence_dir / f"proposal_{run_index:03d}.json"
            if isinstance(proposal, dict):
                if not proposal_path.is_file() or json.loads(
                    proposal_path.read_text(encoding="utf-8")
                ) != proposal:
                    raise LocalTrialError("提案文件无法由阶段原始输出重算。")
            elif proposal_path.exists():
                raise LocalTrialError("阻断运行不得保留可比较提案文件。")
            proposal_observation = observe_proposal(request, proposal)
            binding_observations = _binding_observations(
                proposal,
                expected_proposal_id=proposal_id,
                expected_run_id=run_id,
                contract=contract,
            )
            combined_observations = [
                *combined_stage_observations,
                *cross_stage_observations,
                *binding_observations,
            ]
            if combined_observations:
                proposal_observation["observations"].extend(combined_observations)
                proposal_observation["observation_count"] += len(
                    combined_observations
                )
                proposal_observation["blocking_observation_count"] += len(
                    combined_observations
                )
            proposal_observation_path = (
                evidence_dir / f"proposal_observation_{run_index:03d}.json"
            )
            if not proposal_observation_path.is_file():
                raise LocalTrialError("缺少逐运行提案观察。")
            stored_proposal_observation = json.loads(
                proposal_observation_path.read_text(encoding="utf-8")
            )
            if (
                contract["schema_version"]
                in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS
                and not _observation_documents_equal(
                    stored_proposal_observation, proposal_observation
                )
            ):
                raise LocalTrialError("提案观察无法由阶段原始输出重算。")
            recorded_blocking_count = (
                proposal_observation["blocking_observation_count"]
                if contract["schema_version"]
                in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS
                else stored_proposal_observation.get("blocking_observation_count")
            )
            if not isinstance(recorded_blocking_count, int):
                raise LocalTrialError("提案观察缺少阻断观察数量。")
            base_run_fields = {
                "run_index",
                "proposal_id",
                "run_id",
                "started_at",
                "elapsed_seconds",
                "stages",
                "all_stages_parsed",
                "structural_observation_count",
            }
            derived_run_fields = {
                "all_stage_contracts_observable",
                "stage_contract_observation_count",
                "proposal_blocking_observation_count",
            }
            cross_stage_run_fields = {"cross_stage_observation_count"}
            allowed_run_field_sets = {
                frozenset(base_run_fields),
                frozenset(base_run_fields | derived_run_fields),
                frozenset(
                    base_run_fields | derived_run_fields | cross_stage_run_fields
                ),
            }
            if frozenset(run) not in allowed_run_field_sets:
                raise LocalTrialError("逐运行摘要字段集合无效。")
            if (
                run.get("proposal_id") != proposal_id
                or run.get("run_id") != run_id
                or not isinstance(run.get("started_at"), str)
                or not run["started_at"]
                or not isinstance(run.get("elapsed_seconds"), (int, float))
                or isinstance(run.get("elapsed_seconds"), bool)
                or run["elapsed_seconds"] < 0
                or run.get("all_stages_parsed")
                != all(
                    item["parse_observation"]["parsed"] for item in stage_records
                )
                or (
                    "all_stage_contracts_observable" in run
                    and run["all_stage_contracts_observable"]
                    != all_stage_contracts_observable
                )
                or (
                    "stage_contract_observation_count" in run
                    and run["stage_contract_observation_count"]
                    != len(combined_stage_observations)
                )
                or (
                    "cross_stage_observation_count" in run
                    and run["cross_stage_observation_count"]
                    != len(cross_stage_observations)
                )
                or (
                    "proposal_blocking_observation_count" in run
                    and run["proposal_blocking_observation_count"]
                    != recorded_blocking_count
                )
                or run.get("structural_observation_count")
                != recorded_blocking_count
            ):
                raise LocalTrialError("逐运行摘要无法由原始输出重算。")
            recomputed_stability_inputs.append(
                proposal if not combined_observations else raw_outputs
            )
            if contract["schema_version"] in SEMANTIC_STABILITY_TRIAL_SCHEMA_VERSIONS:
                recomputed_controlled_inputs.append(
                    deepcopy(stages) if all_stage_contracts_observable else None
                )
        else:
            raw_path = evidence_dir / f"raw_output_{run_index:03d}.txt"
            if sha256_file(raw_path) != run["raw_output_sha256"]:
                raise LocalTrialError("运行原始输出摘要不一致。")
        if not (evidence_dir / f"proposal_observation_{run_index:03d}.json").is_file():
            raise LocalTrialError("缺少逐运行规划观察。")
    if staged and expected_call_index - 1 != contract["resource_budget"]["maximum_model_calls"]:
        raise LocalTrialError("证据中的阶段模型调用总数不一致。")
    if staged and contract["schema_version"] in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
        recomputed_stability = observe_stability(request, recomputed_stability_inputs)
        if stability != recomputed_stability:
            raise LocalTrialError("稳定性观察无法由阶段原始输出重算。")
    if contract["schema_version"] in SEMANTIC_STABILITY_TRIAL_SCHEMA_VERSIONS and not (
        evidence_dir / "environment.json"
    ).is_file():
        raise LocalTrialError("受控可观察试验证据缺少运行环境记录。")
    if contract["schema_version"] in SEMANTIC_STABILITY_TRIAL_SCHEMA_VERSIONS:
        controlled_path = evidence_dir / "controlled_semantic_stability_observation.json"
        if not controlled_path.is_file():
            raise LocalTrialError("第五版证据缺少受控语义一致性观察。")
        controlled = json.loads(controlled_path.read_text(encoding="utf-8"))
        recomputed_controlled = (
            observe_generalized_semantic_stability(recomputed_controlled_inputs)
            if contract["schema_version"]
            in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS
            else observe_controlled_semantic_stability(recomputed_controlled_inputs)
        )
        if controlled != recomputed_controlled:
            raise LocalTrialError("受控语义一致性观察无法由阶段原始输出重算。")
        if summary.get("controlled_semantic_comparison_performed") != controlled.get(
            "comparison_performed"
        ):
            raise LocalTrialError("摘要与受控语义一致性观察不一致。")
        if summary.get(
            "largest_exact_controlled_semantic_group_ratio"
        ) != controlled.get("largest_exact_controlled_semantic_group_ratio"):
            raise LocalTrialError("摘要中的受控语义一致率不一致。")
    if contract["schema_version"] in GENERALIZED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
        expected_summary_fields = {
            "schema_version",
            "execution_id",
            "model_id",
            "model_revision",
            "prompt_contract_version",
            "run_count_requested",
            "run_count_observed",
            "model_call_count_requested",
            "model_call_count_observed",
            "parsed_run_count",
            "structurally_observable_run_count",
            "comparison_performed",
            "largest_exact_structure_group_ratio",
            "runs",
            "formal_shot_spec_created",
            "formal_quality_acceptance_created",
            "creative_review_required",
            "automatic_retry_count",
            "controlled_semantic_comparison_performed",
            "largest_exact_controlled_semantic_group_ratio",
        }
        if set(summary) != expected_summary_fields:
            raise LocalTrialError("通用规划摘要字段集合无效。")
        if (
            summary.get("schema_version")
            != "local-shot-planner-trial-observation.v1"
            or summary.get("structurally_observable_run_count")
            != sum(
                run["structural_observation_count"] == 0
                for run in summary["runs"]
            )
            or summary.get("comparison_performed")
            != stability.get("comparison_performed")
            or summary.get("largest_exact_structure_group_ratio")
            != stability.get("largest_exact_structure_group_ratio")
            or summary.get("creative_review_required") is not True
        ):
            raise LocalTrialError("通用规划摘要无法由逐运行证据重算。")
    return {
        "schema_version": "local-shot-planner-evidence-verification.v1",
        "execution_id": summary["execution_id"],
        "observed_file_count": len(actual_paths),
        "run_count_observed": summary["run_count_observed"],
        "prompt_contract_version": summary.get(
            "prompt_contract_version", prompt_contract_version(contract)
        ),
        "package_integrity_observation": "COMPLETE_AND_DIGEST_MATCHED",
        "formal_shot_spec_created": False,
        "formal_quality_acceptance_created": False,
    }
