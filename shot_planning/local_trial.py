"""本地文本小模型镜头规划试验，保留原始输出且不自动重试。"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import time
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from .contracts import (
    PLANNER_CONTEXT_PROMPT_CONTRACT_VERSION,
    PLANNER_OBSERVABLE_PROMPT_CONTRACT_VERSION,
    PLANNER_PAYLOAD_PROMPT_CONTRACT_VERSION,
    PLANNER_PROMPT_CONTRACT_VERSION,
    PLANNER_STAGED_PROMPT_CONTRACT_VERSION,
    PLANNER_SEMANTIC_PROMPT_CONTRACT_VERSION,
    PLANNER_TOKENIZED_CONTEXT_PROMPT_CONTRACT_VERSION,
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
    build_local_planner_context_stage_prompt,
    build_local_planner_observable_stage_prompt,
    build_local_planner_payload_prompt,
    build_local_planner_prompt,
    build_local_planner_stage_prompt,
    build_local_planner_tokenized_context_stage_prompt,
)
from .stability import observe_stability
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
STAGED_TRIAL_SCHEMA_VERSIONS = frozenset(
    {
        TRIAL_SCHEMA_VERSION_V3,
        TRIAL_SCHEMA_VERSION_V4,
        TRIAL_SCHEMA_VERSION_V5,
        TRIAL_SCHEMA_VERSION_V6,
        TRIAL_SCHEMA_VERSION_V7,
    }
)
CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS = frozenset(
    {TRIAL_SCHEMA_VERSION_V5, TRIAL_SCHEMA_VERSION_V6, TRIAL_SCHEMA_VERSION_V7}
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
    elif schema_version in CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
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
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V7:
        return PLANNER_TOKENIZED_CONTEXT_PROMPT_CONTRACT_VERSION
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V6:
        return PLANNER_CONTEXT_PROMPT_CONTRACT_VERSION
    if contract["schema_version"] in CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
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
        shots.append(
            {
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
                "emotion": item.get("emotion"),
                "lighting": item.get("lighting"),
                "continuity_in": item.get("continuity_in"),
                "continuity_out": item.get("continuity_out"),
                "observable_checks": item.get("observable_checks"),
            }
        )
    return {
        "schema_version": "shot-planning-proposal.v1",
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
) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    expected_keys = STAGE_KEYS[stage]
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
    allowed_fields = {
        key: tuple(values)
        for key, values in STRUCTURED_STAGE_ALLOWED_VALUES.get(stage, {}).items()
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
    if stage in STRUCTURED_STAGE_ALLOWED_VALUES and stage != "shot_core" and isinstance(
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
    if contract["schema_version"] in CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
        write_json(evidence_dir / "compiler_contract.json", compiler_contract())
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V7:
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
            if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V7:
                prompt = build_local_planner_tokenized_context_stage_prompt(
                    request, stage
                )
            elif contract["schema_version"] == TRIAL_SCHEMA_VERSION_V6:
                prompt = build_local_planner_context_stage_prompt(request, stage)
            elif contract["schema_version"] == TRIAL_SCHEMA_VERSION_V5:
                prompt = build_local_planner_observable_stage_prompt(request, stage)
            else:
                prompt = build_local_planner_stage_prompt(request, stage)
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
                payload, parse_observation = strict_parse_model_output(raw_output)
            else:
                payload = raw_output
                parse_observation = {
                    "parsed": False,
                    "generation_error": generation_error,
                    "automatic_repair_attempted": False,
                }
            payload_observations = observe_stage_payload(
                stage,
                payload,
                request=(
                    request
                    if contract["schema_version"]
                    in CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS
                    else None
                ),
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
        all_stage_contracts_observable = all_stages_present and not stage_observations
        if all_stages_present and (
            contract["schema_version"]
            not in CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS
            or all_stage_contracts_observable
        ):
            if (
                contract["schema_version"]
                in CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS
            ):
                if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V7:
                    proposal: Any = compile_tokenized_context_stages_to_proposal(
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
        combined_observations = [*stage_observations, *binding_observations]
        if combined_observations:
            proposal_observation["observations"].extend(combined_observations)
            proposal_observation["observation_count"] += len(combined_observations)
            proposal_observation["blocking_observation_count"] += len(combined_observations)
        stability_inputs.append(proposal if not combined_observations else raw_outputs)
        if contract["schema_version"] in CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
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
    if contract["schema_version"] in CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
        controlled_stability = observe_controlled_semantic_stability(
            controlled_stability_inputs
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
        "shot_planning/local_trial.py",
        "shot_planning/prompting.py",
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


def verify_evidence(evidence_dir: Path) -> dict[str, Any]:
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
    if contract["schema_version"] in CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
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
    if contract["schema_version"] == TRIAL_SCHEMA_VERSION_V7:
        context_compiler_path = evidence_dir / "context_compiler_contract.json"
        if not context_compiler_path.is_file():
            raise LocalTrialError("第七版证据缺少上下文编译合同。")
        observed_context_compiler = json.loads(
            context_compiler_path.read_text(encoding="utf-8")
        )
        if observed_context_compiler.get("schema_version") != contract[
            "prompt_strategy"
        ]["context_compiler_contract_version"]:
            raise LocalTrialError("第七版上下文编译合同版本不一致。")
        if canonical_sha256(observed_context_compiler) != contract[
            "prompt_strategy"
        ]["context_compiler_contract_sha256"]:
            raise LocalTrialError("第七版上下文编译合同摘要不一致。")
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
    for run in summary["runs"]:
        run_index = run["run_index"]
        if staged:
            stage_records = run.get("stages")
            if not isinstance(stage_records, list) or [
                item.get("stage") for item in stage_records if isinstance(item, dict)
            ] != contract["prompt_strategy"]["stages"]:
                raise LocalTrialError("逐运行阶段顺序与固定合同不一致。")
            for stage_record in run["stages"]:
                stage = stage_record["stage"]
                if stage_record.get("model_call_index") != expected_call_index:
                    raise LocalTrialError("阶段模型调用编号不连续。")
                expected_call_index += 1
                prompt_path = evidence_dir / f"prompt_{run_index:03d}_{stage}.json"
                raw_path = evidence_dir / f"raw_output_{run_index:03d}_{stage}.txt"
                observation_path = (
                    evidence_dir / f"stage_observation_{run_index:03d}_{stage}.json"
                )
                if not prompt_path.is_file() or not observation_path.is_file():
                    raise LocalTrialError("缺少阶段提示或阶段观察文件。")
                prompt = json.loads(prompt_path.read_text(encoding="utf-8"))
                if (
                    prompt.get("stage") != stage
                    or prompt.get("prompt_contract_version")
                    != prompt_contract_version(contract)
                ):
                    raise LocalTrialError("阶段提示与固定合同不一致。")
                if sha256_file(raw_path) != stage_record["raw_output_sha256"]:
                    raise LocalTrialError("阶段原始输出摘要不一致。")
                parse_observation = stage_record.get("parse_observation", {})
                if (
                    parse_observation.get("parsed") is True
                    and parse_observation.get("root_type") == "dict"
                    and not (
                        evidence_dir / f"payload_{run_index:03d}_{stage}.json"
                    ).is_file()
                ):
                    raise LocalTrialError("缺少已解析阶段载荷文件。")
        else:
            raw_path = evidence_dir / f"raw_output_{run_index:03d}.txt"
            if sha256_file(raw_path) != run["raw_output_sha256"]:
                raise LocalTrialError("运行原始输出摘要不一致。")
        if not (evidence_dir / f"proposal_observation_{run_index:03d}.json").is_file():
            raise LocalTrialError("缺少逐运行规划观察。")
    if staged and expected_call_index - 1 != contract["resource_budget"]["maximum_model_calls"]:
        raise LocalTrialError("证据中的阶段模型调用总数不一致。")
    if contract["schema_version"] in CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS and not (
        evidence_dir / "environment.json"
    ).is_file():
        raise LocalTrialError("受控可观察试验证据缺少运行环境记录。")
    if contract["schema_version"] in CONTROLLED_OBSERVABILITY_TRIAL_SCHEMA_VERSIONS:
        controlled_path = evidence_dir / "controlled_semantic_stability_observation.json"
        if not controlled_path.is_file():
            raise LocalTrialError("第五版证据缺少受控语义一致性观察。")
        controlled = json.loads(controlled_path.read_text(encoding="utf-8"))
        if controlled.get("formal_decision_created") is not False:
            raise LocalTrialError("受控语义一致性观察越权声明正式裁决。")
        if summary.get("controlled_semantic_comparison_performed") != controlled.get(
            "comparison_performed"
        ):
            raise LocalTrialError("摘要与受控语义一致性观察不一致。")
        if summary.get(
            "largest_exact_controlled_semantic_group_ratio"
        ) != controlled.get("largest_exact_controlled_semantic_group_ratio"):
            raise LocalTrialError("摘要中的受控语义一致率不一致。")
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
