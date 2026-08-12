"""一句话镜头规划请求的固定合同。"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from typing import Any

from .controlled_context import TOKENIZED_CONTEXT_ALLOWED_VALUES
from .structured_observability import STRUCTURED_STAGE_ALLOWED_VALUES


REQUEST_SCHEMA_VERSION = "shot-planning-request.v1"
PROPOSAL_SCHEMA_VERSION = "shot-planning-proposal.v1"
PLANNER_PROMPT_CONTRACT_VERSION = "local-shot-planner.v1"
PLANNER_PAYLOAD_PROMPT_CONTRACT_VERSION = "local-shot-planner-payload.v2"
PLANNER_STAGED_PROMPT_CONTRACT_VERSION = "local-shot-planner-staged.v3"
PLANNER_SEMANTIC_PROMPT_CONTRACT_VERSION = "local-shot-planner-staged-semantic.v4"
PLANNER_OBSERVABLE_PROMPT_CONTRACT_VERSION = (
    "local-shot-planner-structured-observability.v5"
)
PLANNER_CONTEXT_PROMPT_CONTRACT_VERSION = "local-shot-planner-controlled-context.v6"
PLANNER_TOKENIZED_CONTEXT_PROMPT_CONTRACT_VERSION = (
    "local-shot-planner-tokenized-context.v7"
)
SUPPORTED_PLANNER_PROMPT_CONTRACT_VERSIONS = frozenset(
    {
        PLANNER_PROMPT_CONTRACT_VERSION,
        PLANNER_PAYLOAD_PROMPT_CONTRACT_VERSION,
        PLANNER_STAGED_PROMPT_CONTRACT_VERSION,
        PLANNER_SEMANTIC_PROMPT_CONTRACT_VERSION,
        PLANNER_OBSERVABLE_PROMPT_CONTRACT_VERSION,
        PLANNER_CONTEXT_PROMPT_CONTRACT_VERSION,
        PLANNER_TOKENIZED_CONTEXT_PROMPT_CONTRACT_VERSION,
    }
)
REQUEST_ID_PATTERN = re.compile(r"PLAN-[A-Z0-9][A-Z0-9-]{2,95}")
SUBJECT_ID_PATTERN = re.compile(r"SUBJECT-[0-9]{3}")


class ShotPlanningContractError(ValueError):
    """规划请求无法建立确定性验证边界。"""

    def __init__(self, code: str, message: str, path: str = "$") -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.path = path


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _positive_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def validate_request(value: Any) -> dict[str, Any]:
    """验证并复制非权威规划请求，不补造缺失创作事实。"""

    if not isinstance(value, dict):
        raise ShotPlanningContractError("REQUEST_NOT_OBJECT", "规划请求必须是对象。")
    if value.get("schema_version") != REQUEST_SCHEMA_VERSION:
        raise ShotPlanningContractError(
            "REQUEST_SCHEMA_UNSUPPORTED",
            "规划请求版本不受支持。",
            "$.schema_version",
        )

    request_id = value.get("request_id")
    if not isinstance(request_id, str) or not REQUEST_ID_PATTERN.fullmatch(request_id):
        raise ShotPlanningContractError(
            "REQUEST_ID_INVALID",
            "规划请求标识无效。",
            "$.request_id",
        )
    if value.get("status") != "DRAFT_NON_AUTHORITATIVE":
        raise ShotPlanningContractError(
            "REQUEST_STATUS_INVALID",
            "一句话规划请求只能是非权威草案。",
            "$.status",
        )

    source_text = value.get("source_text")
    if not isinstance(source_text, str) or not source_text.strip():
        raise ShotPlanningContractError(
            "SOURCE_TEXT_REQUIRED",
            "必须提供非空原句。",
            "$.source_text",
        )
    duration = value.get("target_duration_seconds")
    if not _positive_number(duration):
        raise ShotPlanningContractError(
            "TARGET_DURATION_INVALID",
            "目标时长必须是正数。",
            "$.target_duration_seconds",
        )
    tolerance = value.get("duration_tolerance_seconds")
    if (
        not isinstance(tolerance, (int, float))
        or isinstance(tolerance, bool)
        or tolerance < 0
        or tolerance >= duration
    ):
        raise ShotPlanningContractError(
            "DURATION_TOLERANCE_INVALID",
            "时长容差必须是小于目标时长的非负数。",
            "$.duration_tolerance_seconds",
        )

    bounds = value.get("shot_count_bounds")
    if not isinstance(bounds, dict):
        raise ShotPlanningContractError(
            "SHOT_COUNT_BOUNDS_REQUIRED",
            "必须声明镜头数量边界。",
            "$.shot_count_bounds",
        )
    minimum = bounds.get("minimum")
    maximum = bounds.get("maximum")
    if (
        not isinstance(minimum, int)
        or isinstance(minimum, bool)
        or not isinstance(maximum, int)
        or isinstance(maximum, bool)
        or minimum < 1
        or maximum < minimum
    ):
        raise ShotPlanningContractError(
            "SHOT_COUNT_BOUNDS_INVALID",
            "镜头数量边界必须是有效正整数区间。",
            "$.shot_count_bounds",
        )

    required_subject_ids = value.get("required_subject_ids")
    if not isinstance(required_subject_ids, list):
        raise ShotPlanningContractError(
            "REQUIRED_SUBJECT_IDS_INVALID",
            "必需主体标识必须是数组。",
            "$.required_subject_ids",
        )
    if any(not isinstance(item, str) for item in required_subject_ids) or len(
        required_subject_ids
    ) != len(set(required_subject_ids)) or any(
        not SUBJECT_ID_PATTERN.fullmatch(item) for item in required_subject_ids
    ):
        raise ShotPlanningContractError(
            "REQUIRED_SUBJECT_ID_INVALID",
            "必需主体标识必须唯一并使用 SUBJECT-000 格式。",
            "$.required_subject_ids",
        )

    expected_scene_count = value.get("expected_scene_count")
    if expected_scene_count is not None and (
        not isinstance(expected_scene_count, int)
        or isinstance(expected_scene_count, bool)
        or expected_scene_count < 1
    ):
        raise ShotPlanningContractError(
            "EXPECTED_SCENE_COUNT_INVALID",
            "预期场景数必须为空或正整数。",
            "$.expected_scene_count",
        )

    semantic_constraints = value.get("semantic_constraints")
    if semantic_constraints is not None:
        if not isinstance(semantic_constraints, dict):
            raise ShotPlanningContractError(
                "SEMANTIC_CONSTRAINTS_INVALID",
                "显式语义约束必须是对象。",
                "$.semantic_constraints",
            )
        list_fields = (
            "allowed_framings",
            "allowed_action_classes",
            "allowed_primary_purposes",
            "required_environment_terms",
            "required_action_terms",
            "forbidden_placeholder_values",
        )
        for field in list_fields:
            field_value = semantic_constraints.get(field)
            if (
                not isinstance(field_value, list)
                or not field_value
                or any(not isinstance(item, str) or not item.strip() for item in field_value)
                or len(field_value) != len(set(field_value))
            ):
                raise ShotPlanningContractError(
                    "SEMANTIC_CONSTRAINT_FIELD_INVALID",
                    "显式语义约束数组必须非空、唯一且只包含非空字符串。",
                    f"$.semantic_constraints.{field}",
                )
        optional_list_fields = (
            "allowed_camera_movements",
            "allowed_camera_directions",
            "allowed_camera_speeds",
            "required_composition_terms",
            "required_emotion_terms",
            "required_continuity_in_terms",
            "required_continuity_out_terms",
            "required_observable_terms",
        )
        for field in optional_list_fields:
            field_value = semantic_constraints.get(field)
            if field_value is None:
                continue
            if (
                not isinstance(field_value, list)
                or not field_value
                or any(not isinstance(item, str) or not item.strip() for item in field_value)
                or len(field_value) != len(set(field_value))
            ):
                raise ShotPlanningContractError(
                    "SEMANTIC_CONSTRAINT_FIELD_INVALID",
                    "可选显式语义约束数组必须非空、唯一且只包含非空字符串。",
                    f"$.semantic_constraints.{field}",
                )
        camera_constraint_fields = {
            "allowed_camera_movements": "camera_movement",
            "allowed_camera_directions": "camera_direction",
            "allowed_camera_speeds": "camera_speed",
        }
        for constraint_field, stage_field in camera_constraint_fields.items():
            values = semantic_constraints.get(constraint_field)
            if values is None:
                continue
            global_values = STRUCTURED_STAGE_ALLOWED_VALUES["shot_core"][stage_field]
            if any(item not in global_values for item in values):
                raise ShotPlanningContractError(
                    "SEMANTIC_CAMERA_VALUE_INVALID",
                    "相机显式约束包含不受支持的枚举值。",
                    f"$.semantic_constraints.{constraint_field}",
                )
        minimum_characters = semantic_constraints.get("minimum_free_text_characters")
        if (
            not isinstance(minimum_characters, int)
            or isinstance(minimum_characters, bool)
            or minimum_characters < 2
        ):
            raise ShotPlanningContractError(
                "SEMANTIC_MINIMUM_TEXT_INVALID",
                "自由文本最小字符数必须是不小于二的整数。",
                "$.semantic_constraints.minimum_free_text_characters",
            )
        minimum_check_count = semantic_constraints.get("minimum_observable_check_count")
        if minimum_check_count is not None and (
            not isinstance(minimum_check_count, int)
            or isinstance(minimum_check_count, bool)
            or minimum_check_count < 1
        ):
            raise ShotPlanningContractError(
                "SEMANTIC_MINIMUM_CHECK_COUNT_INVALID",
                "最小可观察检查项数量必须为空或正整数。",
                "$.semantic_constraints.minimum_observable_check_count",
            )

    controlled_stage_values = value.get("controlled_stage_allowed_values")
    if controlled_stage_values is not None:
        if not isinstance(controlled_stage_values, dict):
            raise ShotPlanningContractError(
                "CONTROLLED_STAGE_VALUES_INVALID",
                "受控阶段允许值必须是对象。",
                "$.controlled_stage_allowed_values",
            )
        expected_stages = set(STRUCTURED_STAGE_ALLOWED_VALUES) - {"shot_core"}
        if set(controlled_stage_values) != expected_stages:
            raise ShotPlanningContractError(
                "CONTROLLED_STAGE_SET_INVALID",
                "受控阶段集合必须精确覆盖构图、表演、灯光和连续性。",
                "$.controlled_stage_allowed_values",
            )
        for stage in sorted(expected_stages):
            stage_value = controlled_stage_values.get(stage)
            expected_fields = set(STRUCTURED_STAGE_ALLOWED_VALUES[stage])
            if not isinstance(stage_value, dict) or set(stage_value) != expected_fields:
                raise ShotPlanningContractError(
                    "CONTROLLED_STAGE_FIELD_SET_INVALID",
                    "受控阶段字段集合与编译词表不一致。",
                    f"$.controlled_stage_allowed_values.{stage}",
                )
            for field, values in stage_value.items():
                global_values = STRUCTURED_STAGE_ALLOWED_VALUES[stage][field]
                if (
                    not isinstance(values, list)
                    or not values
                    or any(not isinstance(item, str) for item in values)
                    or len(values) != len(set(values))
                    or any(item not in global_values for item in values)
                ):
                    raise ShotPlanningContractError(
                        "CONTROLLED_STAGE_FIELD_VALUES_INVALID",
                        "受控阶段允许值必须是全局词表的非空唯一子集。",
                        f"$.controlled_stage_allowed_values.{stage}.{field}",
                    )

    controlled_context_values = value.get("controlled_context_allowed_values")
    if controlled_context_values is not None:
        expected_context_fields = {
            "scene": {"location", "time", "environment", "continuity_anchor"},
            "beat": {"action"},
        }
        if not isinstance(controlled_context_values, dict) or set(
            controlled_context_values
        ) != set(expected_context_fields):
            raise ShotPlanningContractError(
                "CONTROLLED_CONTEXT_SET_INVALID",
                "受控上下文必须精确覆盖场景和节拍。",
                "$.controlled_context_allowed_values",
            )
        for stage, expected_fields in expected_context_fields.items():
            stage_value = controlled_context_values.get(stage)
            if not isinstance(stage_value, dict) or set(stage_value) != expected_fields:
                raise ShotPlanningContractError(
                    "CONTROLLED_CONTEXT_FIELD_SET_INVALID",
                    "受控上下文字段集合不完整。",
                    f"$.controlled_context_allowed_values.{stage}",
                )
            for field, values in stage_value.items():
                if (
                    not isinstance(values, list)
                    or not values
                    or any(not isinstance(item, str) or not item.strip() for item in values)
                    or len(values) != len(set(values))
                ):
                    raise ShotPlanningContractError(
                        "CONTROLLED_CONTEXT_VALUES_INVALID",
                        "受控上下文允许值必须是非空唯一字符串数组。",
                        f"$.controlled_context_allowed_values.{stage}.{field}",
                    )

    controlled_context_token_values = value.get("controlled_context_token_values")
    if controlled_context_token_values is not None:
        expected_stages = set(TOKENIZED_CONTEXT_ALLOWED_VALUES)
        if not isinstance(controlled_context_token_values, dict) or set(
            controlled_context_token_values
        ) != expected_stages:
            raise ShotPlanningContractError(
                "CONTROLLED_CONTEXT_TOKEN_SET_INVALID",
                "受控上下文标记必须精确覆盖场景上下文阶段。",
                "$.controlled_context_token_values",
            )
        for stage, global_fields in TOKENIZED_CONTEXT_ALLOWED_VALUES.items():
            stage_value = controlled_context_token_values.get(stage)
            if not isinstance(stage_value, dict) or set(stage_value) != set(global_fields):
                raise ShotPlanningContractError(
                    "CONTROLLED_CONTEXT_TOKEN_FIELD_SET_INVALID",
                    "受控上下文标记字段集合不完整。",
                    f"$.controlled_context_token_values.{stage}",
                )
            for field, values in stage_value.items():
                if (
                    not isinstance(values, list)
                    or not values
                    or any(not isinstance(item, str) for item in values)
                    or len(values) != len(set(values))
                    or any(item not in global_fields[field] for item in values)
                ):
                    raise ShotPlanningContractError(
                        "CONTROLLED_CONTEXT_TOKEN_VALUES_INVALID",
                        "受控上下文标记必须是全局词表的非空唯一子集。",
                        f"$.controlled_context_token_values.{stage}.{field}",
                    )

    return deepcopy(value)
