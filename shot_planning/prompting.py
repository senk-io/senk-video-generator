"""把中立规划请求编译为本地文本模型提示，不包含视频提供者语法。"""

from __future__ import annotations

import json
from typing import Any

from .contracts import (
    PLANNER_CONTEXT_PROMPT_CONTRACT_VERSION,
    PLANNER_GENERALIZED_OBSERVABILITY_PROMPT_CONTRACT_VERSION,
    PLANNER_HYBRID_SOURCE_FACT_PROMPT_CONTRACT_VERSION,
    PLANNER_OBSERVABLE_PROMPT_CONTRACT_VERSION,
    PLANNER_PROMPT_CONTRACT_VERSION,
    PLANNER_STAGED_PROMPT_CONTRACT_VERSION,
    PLANNER_SEMANTIC_PROMPT_CONTRACT_VERSION,
    PLANNER_TOKENIZED_CONTEXT_PROMPT_CONTRACT_VERSION,
    PLANNER_SCALAR_CHOICE_PROMPT_CONTRACT_VERSION,
    PLANNER_SEMANTIC_GLOSS_PROMPT_CONTRACT_VERSION,
    PLANNER_PAYLOAD_PROMPT_CONTRACT_VERSION,
    PROPOSAL_SCHEMA_VERSION,
    REQUEST_SCHEMA_VERSION_V2,
    ShotPlanningContractError,
    canonical_sha256,
    validate_request,
)
from .controlled_context import (
    TOKENIZED_CONTEXT_STAGE_KEYS,
    TOKENIZED_CONTEXT_STAGE_ORDER,
)
from .generalized_observability import (
    GENERALIZED_OBSERVABILITY_COMPILER_VERSION,
    GENERALIZED_STAGE_ALLOWED_VALUES,
    GENERALIZED_STAGE_ORDER,
    GENERALIZED_STAGE_REQUIRED_KEYS,
)
from .structured_observability import (
    OBSERVABLE_STAGE_ORDER,
    STRUCTURED_STAGE_ALLOWED_VALUES,
    STRUCTURED_STAGE_REQUIRED_KEYS,
)
from .semantic_choice import choice_glossary_for_stage
from .source_facts import (
    extract_source_facts,
    locked_fields_for_stage,
    residual_fields_for_stage,
)


def build_local_planner_prompt(
    request_value: Any,
    *,
    proposal_id: str = "由调用方注入或本次运行唯一标识",
    planner_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    request = validate_request(request_value)
    if request["schema_version"] == REQUEST_SCHEMA_VERSION_V2:
        raise ShotPlanningContractError(
            "REQUEST_V2_REQUIRES_STAGED_PROMPT",
            "第二版规划请求必须使用第八版至第十版的七阶段提示合同。",
            "$.schema_version",
        )
    planner = planner_metadata or {
        "model_id": "实际本地模型标识",
        "model_version": "实际模型版本",
        "prompt_contract_version": PLANNER_PROMPT_CONTRACT_VERSION,
        "run_id": "实际运行标识",
        "sampling": {"temperature": 0.0, "seed": None},
    }
    proposal_shape = {
        "schema_version": PROPOSAL_SCHEMA_VERSION,
        "proposal_id": proposal_id,
        "request_id": request["request_id"],
        "source_text_sha256": canonical_sha256(request["source_text"]),
        "status": "DRAFT_NON_AUTHORITATIVE",
        "planner": planner,
        "scenes": [
            {
                "scene_id": "SCENE-001",
                "ordinal": 1,
                "location": "具体地点",
                "time": "具体时间",
                "environment": "环境状态",
                "continuity_anchors": ["跨镜头不得无理由变化的锚点"],
            }
        ],
        "narrative_beats": [
            {
                "beat_id": "BEAT-001",
                "ordinal": 1,
                "scene_id": "SCENE-001",
                "source_span": {"start": 0, "end": len(request["source_text"]), "quote": request["source_text"]},
                "purpose": "EMPHASIZE_EMOTION",
                "subject_ids": request["required_subject_ids"] or ["SUBJECT-001"],
                "action": "原句中可见的主要动作",
            }
        ],
        "shots": [
            {
                "shot_id": "SHOT-001",
                "ordinal": 1,
                "scene_id": "SCENE-001",
                "beat_ids": ["BEAT-001"],
                "script_segment": request["source_text"],
                "primary_purpose": "EMPHASIZE_EMOTION",
                "target_duration_seconds": request["target_duration_seconds"],
                "framing": "CLOSE_UP",
                "subject_ids": request["required_subject_ids"] or ["SUBJECT-001"],
                "action": {"class": "EXPRESS", "description": "单一主要动作"},
                "composition": "可观察构图",
                "camera": {"movement": "STATIC", "direction": "NONE", "speed": "NONE"},
                "emotion": "可观察表演状态",
                "lighting": "可观察灯光状态",
                "continuity_in": "进入镜头时必须保持的状态；首镜头写明起始状态",
                "continuity_out": "离开镜头时必须传递的状态；末镜头写明结束状态",
                "observable_checks": ["可由后续观察器核对的具体项目"],
            }
        ],
    }
    system_instruction = """你是非权威镜头规划器，只把输入原句映射为结构化草案。
不得增加原句未授权的人物、地点变化、时间变化或剧情结果。
先按地点、时间或主要叙事目标变化识别场景，再按单一画面用途拆镜头。
每个镜头只能有一个 primary_purpose 和一个 action；不能写质量通过、批准、选择或验证结论。
所有 source_span 使用 Python 字符串下标并与原句逐字匹配；全部非标点内容必须被节拍覆盖。
只输出一个 JSON 对象，不输出 Markdown、解释或提供者专属提示语法。"""
    return {
        "prompt_contract_version": PLANNER_PROMPT_CONTRACT_VERSION,
        "recommended_sampling": {"temperature": 0.0, "seed": "fixed_when_supported"},
        "system": system_instruction,
        "user": json.dumps(
            {
                "request": request,
                "allowed_purpose_values": [
                    "ESTABLISH_CONTEXT",
                    "DEVELOP_ACTION",
                    "EMPHASIZE_EMOTION",
                    "REVEAL_INFORMATION",
                    "TRANSITION",
                    "CLOSE_SEQUENCE",
                ],
                "allowed_action_class_values": [
                    "STATIC",
                    "MOVE",
                    "PERFORM",
                    "EXPRESS",
                    "INTERACT",
                    "TRANSITION",
                ],
                "required_output_shape": proposal_shape,
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
    }


def build_local_planner_payload_prompt(request_value: Any) -> dict[str, Any]:
    """只让小模型表达创意载荷；标识、证据和状态由系统编译。"""

    request = validate_request(request_value)
    if request["schema_version"] == REQUEST_SCHEMA_VERSION_V2:
        raise ShotPlanningContractError(
            "REQUEST_V2_REQUIRES_STAGED_PROMPT",
            "第二版规划请求必须使用第八版至第十版的七阶段提示合同。",
            "$.schema_version",
        )
    payload_shape = {
        "scenes": [
            {
                "location": "原句明确的地点；未知则写未明确",
                "time": "原句明确的时间；未知则写未明确",
                "environment": "原句明确的环境状态",
                "continuity_anchors": ["不得无理由变化的可见锚点"],
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
                "purpose": "EMPHASIZE_EMOTION",
                "action": "原句中可见的主要动作",
            }
        ],
        "shots": [
            {
                "scene_ordinal": 1,
                "beat_ordinals": [1],
                "primary_purpose": "EMPHASIZE_EMOTION",
                "target_duration_seconds": request["target_duration_seconds"],
                "framing": "CLOSE_UP",
                "action_class": "EXPRESS",
                "action_description": "单一主要动作",
                "composition": "可观察构图",
                "camera_movement": "STATIC",
                "camera_direction": "NONE",
                "camera_speed": "NONE",
                "emotion": "可观察表演状态",
                "lighting": "可观察灯光状态",
                "continuity_in": "进入镜头时必须保持的状态",
                "continuity_out": "离开镜头时必须传递的状态",
                "observable_checks": ["可由后续观察器核对的具体项目"],
            }
        ],
    }
    system_instruction = """你只负责把一句话拆成场景、叙事节拍和镜头创意载荷。
不要输出 proposal_id、request_id、schema_version、status、planner 或任何通过、批准、选择、验证结论。
地点、时间或主要叙事目标变化才新增场景；没有变化时只用一个场景。
每个镜头只有一个主要用途和一个主要动作，不增加原句未授权的人物、地点变化或剧情结果。
source_span 使用 Python 字符串下标并逐字匹配原句，全部非标点内容必须被覆盖。
只续写已经开始的 JSON 对象；不要代码围栏、Markdown 或解释。"""
    return {
        "prompt_contract_version": PLANNER_PAYLOAD_PROMPT_CONTRACT_VERSION,
        "recommended_sampling": {"temperature": 0.0, "seed": "fixed_when_supported"},
        "assistant_prefill": "{",
        "system": system_instruction,
        "user": json.dumps(
            {
                "request": {
                    "source_text": request["source_text"],
                    "target_duration_seconds": request["target_duration_seconds"],
                    "shot_count_bounds": request["shot_count_bounds"],
                    "expected_scene_count": request.get("expected_scene_count"),
                },
                "allowed_values": {
                    "purpose": [
                        "ESTABLISH_CONTEXT",
                        "DEVELOP_ACTION",
                        "EMPHASIZE_EMOTION",
                        "REVEAL_INFORMATION",
                        "TRANSITION",
                        "CLOSE_SEQUENCE",
                    ],
                    "action_class": [
                        "STATIC",
                        "MOVE",
                        "PERFORM",
                        "EXPRESS",
                        "INTERACT",
                        "TRANSITION",
                    ],
                    "framing": [
                        "EXTREME_WIDE",
                        "WIDE",
                        "MEDIUM_WIDE",
                        "MEDIUM",
                        "MEDIUM_CLOSE_UP",
                        "CLOSE_UP",
                        "EXTREME_CLOSE_UP",
                    ],
                    "camera_movement": [
                        "STATIC",
                        "PAN",
                        "TILT",
                        "DOLLY",
                        "TRUCK",
                        "PEDESTAL",
                        "ZOOM",
                        "ARC",
                        "HANDHELD",
                    ],
                    "camera_direction": [
                        "NONE",
                        "LEFT",
                        "RIGHT",
                        "UP",
                        "DOWN",
                        "IN",
                        "OUT",
                    ],
                    "camera_speed": ["NONE", "SLOW", "MODERATE", "FAST"],
                },
                "required_payload_shape": payload_shape,
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
    }


def build_local_planner_stage_prompt(request_value: Any, stage: str) -> dict[str, Any]:
    """为六亿参数模型建立单职责扁平 JSON 阶段。"""

    request = validate_request(request_value)
    common = {
        "source_text": request["source_text"],
        "target_duration_seconds": request["target_duration_seconds"],
    }
    semantic_constraints = request.get("semantic_constraints")
    if semantic_constraints is not None:
        common["explicit_semantic_constraints"] = semantic_constraints
    stage_contracts = {
        "scene": {
            "required_keys": [
                "location",
                "time",
                "environment",
                "continuity_anchor",
            ],
            "instruction": "只描述原句中的单一场景。未知的地点或时间写未明确；连续性锚点必须是可见对象或环境状态。",
        },
        "beat": {
            "required_keys": ["purpose", "action"],
            "instruction": "只描述覆盖整句的单一叙事节拍；动作不得增加原句不存在的剧情结果。",
            "allowed_purpose": [
                "ESTABLISH_CONTEXT",
                "DEVELOP_ACTION",
                "EMPHASIZE_EMOTION",
                "REVEAL_INFORMATION",
                "TRANSITION",
                "CLOSE_SEQUENCE",
            ],
        },
        "shot": {
            "required_keys": [
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
            ],
            "instruction": "只设计一个覆盖整句和全部目标时长的镜头；镜头必须只有一个主要用途和一个主要动作。",
            "allowed_primary_purpose": [
                "ESTABLISH_CONTEXT",
                "DEVELOP_ACTION",
                "EMPHASIZE_EMOTION",
                "REVEAL_INFORMATION",
                "TRANSITION",
                "CLOSE_SEQUENCE",
            ],
            "allowed_framing": [
                "EXTREME_WIDE",
                "WIDE",
                "MEDIUM_WIDE",
                "MEDIUM",
                "MEDIUM_CLOSE_UP",
                "CLOSE_UP",
                "EXTREME_CLOSE_UP",
            ],
            "allowed_action_class": [
                "STATIC",
                "MOVE",
                "PERFORM",
                "EXPRESS",
                "INTERACT",
                "TRANSITION",
            ],
            "allowed_camera_movement": [
                "STATIC",
                "PAN",
                "TILT",
                "DOLLY",
                "TRUCK",
                "PEDESTAL",
                "ZOOM",
                "ARC",
                "HANDHELD",
            ],
            "allowed_camera_direction": [
                "NONE",
                "LEFT",
                "RIGHT",
                "UP",
                "DOWN",
                "IN",
                "OUT",
            ],
            "allowed_camera_speed": ["NONE", "SLOW", "MODERATE", "FAST"],
        },
    }
    if stage not in stage_contracts:
        raise ValueError("不受支持的本地规划阶段。")
    if semantic_constraints is not None:
        if stage == "scene":
            stage_contracts[stage]["required_environment_terms"] = semantic_constraints[
                "required_environment_terms"
            ]
        elif stage == "beat":
            stage_contracts[stage]["allowed_purpose"] = semantic_constraints[
                "allowed_primary_purposes"
            ]
            stage_contracts[stage]["required_action_terms"] = semantic_constraints[
                "required_action_terms"
            ]
        elif stage == "shot":
            stage_contracts[stage]["allowed_primary_purpose"] = semantic_constraints[
                "allowed_primary_purposes"
            ]
            stage_contracts[stage]["allowed_framing"] = semantic_constraints[
                "allowed_framings"
            ]
            stage_contracts[stage]["allowed_action_class"] = semantic_constraints[
                "allowed_action_classes"
            ]
            stage_contracts[stage]["required_action_terms"] = semantic_constraints[
                "required_action_terms"
            ]
    system_instruction = """你是单职责镜头规划阶段，只输出一个扁平 JSON 对象。
必须包含且仅包含 required_keys 中的字段，字段名和枚举值不得翻译。
字符串值必须结合 source_text 填写，不能照抄 instruction 文本。
只续写已经开始的 JSON 对象；不要代码围栏、Markdown、解释、嵌套对象或额外字段。"""
    return {
        "prompt_contract_version": (
            PLANNER_SEMANTIC_PROMPT_CONTRACT_VERSION
            if semantic_constraints is not None
            else PLANNER_STAGED_PROMPT_CONTRACT_VERSION
        ),
        "stage": stage,
        "assistant_prefill": "{",
        "recommended_sampling": {"temperature": 0.0, "seed": "fixed_when_supported"},
        "system": system_instruction,
        "user": json.dumps(
            {"input": common, "stage_contract": stage_contracts[stage]},
            ensure_ascii=False,
            sort_keys=True,
        ),
    }


def build_local_planner_observable_stage_prompt(
    request_value: Any,
    stage: str,
) -> dict[str, Any]:
    """把自由描述拆成受控的构图、表演、灯光、连续性和检查阶段。"""

    request = validate_request(request_value)
    if stage not in OBSERVABLE_STAGE_ORDER:
        raise ValueError("不受支持的结构化可观察规划阶段。")
    constraints = request["semantic_constraints"]
    common = {
        "source_text": request["source_text"],
        "target_duration_seconds": request["target_duration_seconds"],
        "explicit_semantic_constraints": constraints,
    }
    if stage == "scene":
        stage_contract: dict[str, Any] = {
            "required_keys": [
                "location",
                "time",
                "environment",
                "continuity_anchor",
            ],
            "instruction": "只描述原句中的单一场景；环境必须包含显式要求词，连续性锚点必须可见。",
            "required_environment_terms": constraints["required_environment_terms"],
        }
    elif stage == "beat":
        stage_contract = {
            "required_keys": ["purpose", "action"],
            "instruction": "只描述覆盖整句的单一叙事节拍；动作不得增加原句不存在的剧情结果。",
            "allowed_values": {
                "purpose": constraints["allowed_primary_purposes"],
            },
            "required_action_terms": constraints["required_action_terms"],
        }
    else:
        required_keys = sorted(STRUCTURED_STAGE_REQUIRED_KEYS[stage])
        request_controlled_values = request.get("controlled_stage_allowed_values")
        if stage != "shot_core" and not isinstance(request_controlled_values, dict):
            raise ValueError("结构化可观察提示要求请求绑定受控阶段允许值。")
        allowed_values = {
            field: list(values)
            for field, values in (
                STRUCTURED_STAGE_ALLOWED_VALUES[stage]
                if stage == "shot_core"
                else request_controlled_values[stage]
            ).items()
        }
        if stage == "shot_core":
            allowed_values["primary_purpose"] = constraints[
                "allowed_primary_purposes"
            ]
            allowed_values["framing"] = constraints["allowed_framings"]
            allowed_values["action_class"] = constraints["allowed_action_classes"]
            stage_instruction = (
                "只选择一个镜头的核心用途、景别、主要动作和相机状态；"
                "action_description 是唯一自由文本字段并必须包含 required_action_terms。"
            )
        elif stage == "composition":
            stage_instruction = "只选择主体位置、面部覆盖、焦点和背景可见性。"
        elif stage == "performance":
            stage_instruction = "只选择眼睛、泪水、嘴部和表演强度的可见状态。"
        elif stage == "lighting":
            stage_instruction = "只选择光源、光质、面部可读性和泪水高光状态。"
        elif stage == "continuity":
            stage_instruction = "只选择进入与离开镜头时主体和环境必须保持的状态。"
        else:
            stage_instruction = "只选择后续观察器分别核对主体、景别、动作、环境和相机的项目。"
        stage_contract = {
            "required_keys": required_keys,
            "instruction": stage_instruction,
            "allowed_values": allowed_values,
        }
        if stage == "shot_core":
            stage_contract["required_action_terms"] = constraints[
                "required_action_terms"
            ]

    system_instruction = """你是单职责结构化镜头规划阶段，只输出一个扁平 JSON 对象。
必须包含且仅包含 required_keys 中的字段，字段名不得翻译。
凡字段出现在 allowed_values 中，其值必须逐字选择对应数组中的一个枚举，不得改写或翻译。
没有 allowed_values 的字符串字段必须结合 source_text 填写，不能照抄 instruction。
只续写已经开始的 JSON 对象；不要代码围栏、Markdown、解释、嵌套对象或额外字段。"""
    return {
        "prompt_contract_version": PLANNER_OBSERVABLE_PROMPT_CONTRACT_VERSION,
        "stage": stage,
        "assistant_prefill": "{",
        "recommended_sampling": {"temperature": 0.0, "seed": "fixed_when_supported"},
        "system": system_instruction,
        "user": json.dumps(
            {"input": common, "stage_contract": stage_contract},
            ensure_ascii=False,
            sort_keys=True,
        ),
    }


def build_local_planner_context_stage_prompt(
    request_value: Any,
    stage: str,
) -> dict[str, Any]:
    """第六版提示：固定场景字段角色，并约束未声明运镜的相机组合。"""

    request = validate_request(request_value)
    context_values = request.get("controlled_context_allowed_values")
    constraints = request.get("semantic_constraints")
    if not isinstance(context_values, dict) or not isinstance(constraints, dict):
        raise ValueError("受控上下文提示要求请求绑定场景、节拍与相机约束。")
    required_camera_fields = (
        "allowed_camera_movements",
        "allowed_camera_directions",
        "allowed_camera_speeds",
    )
    if any(field not in constraints for field in required_camera_fields):
        raise ValueError("受控上下文提示缺少相机允许值约束。")

    prompt = build_local_planner_observable_stage_prompt(request, stage)
    body = json.loads(prompt["user"])
    stage_contract = body["stage_contract"]
    allowed_values = stage_contract.setdefault("allowed_values", {})
    if stage == "scene":
        allowed_values.update(context_values["scene"])
    elif stage == "beat":
        allowed_values["action"] = context_values["beat"]["action"]
    elif stage == "shot_core":
        allowed_values["camera_movement"] = constraints["allowed_camera_movements"]
        allowed_values["camera_direction"] = constraints["allowed_camera_directions"]
        allowed_values["camera_speed"] = constraints["allowed_camera_speeds"]
    prompt["prompt_contract_version"] = PLANNER_CONTEXT_PROMPT_CONTRACT_VERSION
    prompt["user"] = json.dumps(body, ensure_ascii=False, sort_keys=True)
    return prompt


def build_local_planner_tokenized_context_stage_prompt(
    request_value: Any,
    stage: str,
) -> dict[str, Any]:
    """第七版提示：场景用受控标记，节拍动作复用完整镜头动作。"""

    request = validate_request(request_value)
    if stage not in TOKENIZED_CONTEXT_STAGE_ORDER:
        raise ValueError("不受支持的标记化上下文规划阶段。")
    constraints = request["semantic_constraints"]
    if stage in {"scene_context", "beat_purpose"}:
        if stage == "scene_context":
            token_values = request.get("controlled_context_token_values")
            if not isinstance(token_values, dict):
                raise ValueError("标记化上下文提示要求请求绑定场景标记允许值。")
            stage_contract: dict[str, Any] = {
                "required_keys": sorted(TOKENIZED_CONTEXT_STAGE_KEYS[stage]),
                "instruction": "只选择地点、时间、环境和连续性锚点的语义标记。",
                "allowed_values": token_values[stage],
            }
        else:
            stage_contract = {
                "required_keys": sorted(TOKENIZED_CONTEXT_STAGE_KEYS[stage]),
                "instruction": "只选择覆盖整句的单一叙事用途；动作由系统复用镜头核心阶段的完整动作描述。",
                "allowed_values": {
                    "purpose": constraints["allowed_primary_purposes"]
                },
            }
        system_instruction = """你是单职责结构化镜头规划阶段，只输出一个扁平 JSON 对象。
必须包含且仅包含 required_keys 中的字段，字段名不得翻译。
字段值必须逐字选择 allowed_values 对应数组中的一个枚举，不得改写、缩写或翻译。
只续写已经开始的 JSON 对象；不要代码围栏、Markdown、解释、嵌套对象或额外字段。"""
        prompt = {
            "stage": stage,
            "assistant_prefill": "{",
            "recommended_sampling": {
                "temperature": 0.0,
                "seed": "fixed_when_supported",
            },
            "system": system_instruction,
            "user": json.dumps(
                {
                    "input": {
                        "source_text": request["source_text"],
                        "target_duration_seconds": request[
                            "target_duration_seconds"
                        ],
                    },
                    "stage_contract": stage_contract,
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
        }
    else:
        prompt = build_local_planner_observable_stage_prompt(request, stage)
        body = json.loads(prompt["user"])
        if stage == "shot_core":
            allowed_values = body["stage_contract"]["allowed_values"]
            allowed_values["camera_movement"] = constraints[
                "allowed_camera_movements"
            ]
            allowed_values["camera_direction"] = constraints[
                "allowed_camera_directions"
            ]
            allowed_values["camera_speed"] = constraints["allowed_camera_speeds"]
        prompt["user"] = json.dumps(body, ensure_ascii=False, sort_keys=True)
    prompt[
        "prompt_contract_version"
    ] = PLANNER_TOKENIZED_CONTEXT_PROMPT_CONTRACT_VERSION
    return prompt


def build_local_planner_generalized_stage_prompt(
    request_value: Any,
    stage: str,
) -> dict[str, Any]:
    """第八版提示：通用主体尺度、行为、灯光和连续性标记。"""

    request = validate_request(request_value)
    if (
        request.get("controlled_observability_compiler_version")
        != GENERALIZED_OBSERVABILITY_COMPILER_VERSION
    ):
        raise ValueError("通用可观察提示要求请求绑定第二版编译词表。")
    if stage not in GENERALIZED_STAGE_ORDER:
        raise ValueError("不受支持的通用可观察规划阶段。")
    if stage in {"scene_context", "beat_purpose", "shot_core"}:
        prompt = build_local_planner_tokenized_context_stage_prompt(request, stage)
        if stage == "shot_core":
            body = json.loads(prompt["user"])
            constraints = request["semantic_constraints"]
            body["input"]["explicit_semantic_constraints"] = {
                "allowed_action_classes": constraints["allowed_action_classes"],
                "allowed_camera_directions": constraints[
                    "allowed_camera_directions"
                ],
                "allowed_camera_movements": constraints[
                    "allowed_camera_movements"
                ],
                "allowed_camera_speeds": constraints["allowed_camera_speeds"],
                "allowed_framings": constraints["allowed_framings"],
                "allowed_primary_purposes": constraints[
                    "allowed_primary_purposes"
                ],
                "required_action_terms": constraints["required_action_terms"],
            }
            prompt["user"] = json.dumps(body, ensure_ascii=False, sort_keys=True)
        prompt[
            "prompt_contract_version"
        ] = PLANNER_GENERALIZED_OBSERVABILITY_PROMPT_CONTRACT_VERSION
        return prompt

    request_controlled_values = request.get("controlled_stage_allowed_values")
    if not isinstance(request_controlled_values, dict):
        raise ValueError("通用可观察提示要求请求绑定受控阶段允许值。")
    if set(request_controlled_values[stage]) != set(
        GENERALIZED_STAGE_ALLOWED_VALUES[stage]
    ):
        raise ValueError("通用可观察阶段字段与第二版编译词表不一致。")
    stage_instructions = {
        "composition": "只选择主体位置、主体尺度、焦点和背景可见性。",
        "performance": "只选择主体朝向、可见动作、可见细节和动作强度。",
        "lighting": "只选择光源、光质、主体可读性和高光状态。",
        "continuity": "只选择进入与离开镜头时主体和环境的可见状态。",
    }
    stage_contract = {
        "required_keys": sorted(GENERALIZED_STAGE_REQUIRED_KEYS[stage]),
        "instruction": stage_instructions[stage],
        "allowed_values": request_controlled_values[stage],
    }
    system_instruction = """你是单职责结构化镜头规划阶段，只输出一个扁平 JSON 对象。
必须包含且仅包含 required_keys 中的字段，字段名不得翻译。
字段值必须逐字选择 allowed_values 对应数组中的一个枚举，不得改写、缩写或翻译。
只续写已经开始的 JSON 对象；不要代码围栏、Markdown、解释、嵌套对象或额外字段。"""
    return {
        "prompt_contract_version": (
            PLANNER_GENERALIZED_OBSERVABILITY_PROMPT_CONTRACT_VERSION
        ),
        "stage": stage,
        "assistant_prefill": "{",
        "recommended_sampling": {
            "temperature": 0.0,
            "seed": "fixed_when_supported",
        },
        "system": system_instruction,
        "user": json.dumps(
            {
                "input": {
                    "source_text": request["source_text"],
                    "target_duration_seconds": request["target_duration_seconds"],
                },
                "stage_contract": stage_contract,
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
    }


def build_local_planner_scalar_choice_stage_prompt(
    request_value: Any,
    stage: str,
) -> dict[str, Any]:
    """第九版提示：用分隔字符串表达候选，禁止把选中值包装成数组。"""

    prompt = build_local_planner_generalized_stage_prompt(request_value, stage)
    body = json.loads(prompt["user"])
    stage_contract = body["stage_contract"]
    allowed_values = stage_contract.pop("allowed_values", {})
    stage_contract["allowed_scalar_choices"] = {
        field: " | ".join(values) for field, values in allowed_values.items()
    }
    stage_contract["selection_rule"] = (
        "每个字段只输出一个 JSON 字符串标量；从竖线分隔候选中逐字选择一个值。"
    )
    stage_contract["value_type"] = "JSON_STRING_SCALAR_ONLY"
    prompt["system"] = """你是单职责结构化镜头规划阶段，只输出一个扁平 JSON 对象。
必须包含且仅包含 required_keys 中的字段，字段名不得翻译。
每个字段值必须是一个 JSON 字符串标量，形如 \"VALUE\"；严禁输出数组、方括号、对象、数字或布尔值。
凡字段出现在 allowed_scalar_choices 中，只能从竖线分隔候选里逐字选择一个值，不能输出多个值。
没有候选的字符串字段必须结合 source_text 填写。
只续写已经开始的 JSON 对象；不要代码围栏、Markdown、解释、嵌套对象或额外字段。"""
    prompt["user"] = json.dumps(body, ensure_ascii=False, sort_keys=True)
    prompt["prompt_contract_version"] = PLANNER_SCALAR_CHOICE_PROMPT_CONTRACT_VERSION
    return prompt


def build_local_planner_semantic_gloss_stage_prompt(
    request_value: Any,
    stage: str,
) -> dict[str, Any]:
    """第十版提示：为允许候选增加通用释义，不注入保留答案。"""

    prompt = build_local_planner_scalar_choice_stage_prompt(request_value, stage)
    body = json.loads(prompt["user"])
    stage_contract = body["stage_contract"]
    allowed_choices = stage_contract["allowed_scalar_choices"]
    stage_contract["choice_glossary"] = choice_glossary_for_stage(
        stage, allowed_choices
    )
    stage_contract["interpretation_rules"] = [
        "按 source_text 的含义选择，不按候选在字符串中的先后位置选择。",
        "原句出现特写、中景或全景时，选择对应的 framing。",
        "主体从左向右移动只描述主体动作与连续性，不代表相机向右摇摄。",
        "只有原句明确说相机摇、推、拉、平移或手持运动时，才选择非 STATIC 相机运动。",
        "entry 表示镜头开始状态，exit 表示镜头结束状态。",
    ]
    prompt["system"] = """你是单职责结构化镜头规划阶段，只输出一个扁平 JSON 对象。
必须包含且仅包含 required_keys 中的字段，字段名不得翻译。
每个字段值必须是一个 JSON 字符串标量，形如 \"VALUE\"；严禁输出数组、方括号、对象、数字或布尔值。
凡字段出现在 allowed_scalar_choices 中，只能从竖线分隔候选里逐字选择一个值，不能输出多个值。
阅读 choice_glossary 理解候选语义；依据 source_text 选择，不能依据候选顺序猜测。
主体的运动方向不是相机运动方向；只有原句明确声明相机或镜头运动，才选择非 STATIC 相机。
没有候选的字符串字段必须结合 source_text 填写。
只续写已经开始的 JSON 对象；不要代码围栏、Markdown、解释、嵌套对象或额外字段。"""
    prompt["user"] = json.dumps(body, ensure_ascii=False, sort_keys=True)
    prompt["prompt_contract_version"] = PLANNER_SEMANTIC_GLOSS_PROMPT_CONTRACT_VERSION
    return prompt


def build_local_planner_hybrid_stage_prompt(
    request_value: Any,
    stage: str,
) -> dict[str, Any]:
    """第十一版提示：模型只填写未被原句事实锁定的残余字段。"""

    request = validate_request(request_value)
    extraction = extract_source_facts(request)
    if extraction["blocking_issue_count"]:
        raise ValueError("原句事实提取存在冲突或歧义，不能构建混合提示。")
    prompt = build_local_planner_semantic_gloss_stage_prompt(request, stage)
    body = json.loads(prompt["user"])
    stage_contract = body["stage_contract"]
    residual_fields = residual_fields_for_stage(extraction, stage)
    locked_fields = locked_fields_for_stage(extraction, stage)
    stage_contract["required_keys"] = residual_fields
    stage_contract["allowed_scalar_choices"] = {
        field: encoded
        for field, encoded in stage_contract.get(
            "allowed_scalar_choices", {}
        ).items()
        if field in residual_fields
    }
    stage_contract["choice_glossary"] = {
        field: descriptions
        for field, descriptions in stage_contract.get(
            "choice_glossary", {}
        ).items()
        if field in residual_fields
    }
    stage_contract.pop("required_action_terms", None)
    body["input"].pop("explicit_semantic_constraints", None)
    if residual_fields:
        stage_contract["instruction"] = (
            "只为 required_keys 中列出的残余字段选择一个受控字符串值；"
            "不得填写其他字段。"
        )
    else:
        stage_contract["instruction"] = (
            "required_keys 为空；只输出空 JSON 对象，不得写入任何字段。"
        )
    interpretation_rules = [
        "按 source_text 的含义选择，不按候选在字符串中的先后位置选择。",
        "只提议 required_keys 的残余字段；已锁定字段不属于模型职责。",
    ]
    residual_set = set(residual_fields)
    if "framing" in residual_set:
        interpretation_rules.append(
            "原句明确出现特写、中景或全景时，选择对应的 framing。"
        )
    if residual_set & {"camera_movement", "camera_direction", "camera_speed"}:
        interpretation_rules.extend(
            [
                "主体的运动方向不是相机运动方向。",
                "只有原句明确声明相机或镜头运动，才选择非 STATIC 相机。",
            ]
        )
    if stage == "performance" and "orientation_state" in residual_set:
        interpretation_rules.append(
            "主体从左向右移动只描述主体方向，不代表相机向右摇摄。"
        )
    if stage == "continuity":
        interpretation_rules.append(
            "entry 表示镜头开始状态，exit 表示镜头结束状态。"
        )
    stage_contract["interpretation_rules"] = interpretation_rules
    stage_contract["field_ownership_rule"] = (
        "只输出 required_keys；system_locked_source_facts 由系统持有，"
        "模型不得重复、覆盖或改写。"
    )
    body["input"]["system_locked_source_facts"] = [
        {
            "field": fact["field"],
            "value": fact["value"],
            "provenance": fact["provenance"],
            "rule_ids": fact["rule_ids"],
            "source_spans": fact["source_spans"],
        }
        for fact in extraction["facts"]
        if fact["field"].startswith(f"{stage}.")
    ]
    body["input"]["locked_field_values"] = locked_fields
    body["input"]["held_out_observation_used"] = False
    prompt["system"] = """你是单职责结构化镜头规划阶段，只输出一个扁平 JSON 对象。
必须包含且仅包含 required_keys 中的字段，字段名不得翻译。
system_locked_source_facts 是系统从 source_text 提取的只读事实；严禁输出、重复、覆盖或改写这些字段。
每个 required_keys 字段值必须是一个 JSON 字符串标量，形如 "VALUE"；严禁输出数组、方括号、对象、数字或布尔值。
凡字段出现在 allowed_scalar_choices 中，只能从竖线分隔候选里逐字选择一个值，不能输出多个值。
阅读 choice_glossary 理解候选语义；依据 source_text 与只读事实选择，不能依据候选顺序猜测。
只续写已经开始的 JSON 对象；不要代码围栏、Markdown、解释、嵌套对象或额外字段。"""
    prompt["user"] = json.dumps(body, ensure_ascii=False, sort_keys=True)
    prompt[
        "prompt_contract_version"
    ] = PLANNER_HYBRID_SOURCE_FACT_PROMPT_CONTRACT_VERSION
    return prompt
