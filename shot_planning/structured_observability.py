"""小模型结构化可观察阶段的受控词汇与确定性文本映射。"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Final


OBSERVABLE_STAGE_ORDER: Final[tuple[str, ...]] = (
    "scene",
    "beat",
    "shot_core",
    "composition",
    "performance",
    "lighting",
    "continuity",
)

CONTROLLED_OBSERVABILITY_COMPILER_VERSION: Final[str] = (
    "structured-observability-compiler.v1"
)

STRUCTURED_STAGE_REQUIRED_KEYS: Final[dict[str, frozenset[str]]] = {
    "shot_core": frozenset(
        {
            "primary_purpose",
            "framing",
            "action_class",
            "action_description",
            "camera_movement",
            "camera_direction",
            "camera_speed",
        }
    ),
    "composition": frozenset(
        {
            "subject_placement",
            "face_coverage",
            "focus_target",
            "background_visibility",
        }
    ),
    "performance": frozenset(
        {
            "eye_state",
            "tear_state",
            "mouth_state",
            "expression_intensity",
        }
    ),
    "lighting": frozenset(
        {
            "light_source",
            "light_quality",
            "face_readability",
            "tear_highlight",
        }
    ),
    "continuity": frozenset(
        {
            "entry_subject_state",
            "entry_environment_state",
            "exit_subject_state",
            "exit_environment_state",
        }
    ),
}

STRUCTURED_STAGE_ALLOWED_VALUES: Final[dict[str, dict[str, tuple[str, ...]]]] = {
    "shot_core": {
        "primary_purpose": (
            "ESTABLISH_CONTEXT",
            "DEVELOP_ACTION",
            "EMPHASIZE_EMOTION",
            "REVEAL_INFORMATION",
            "TRANSITION",
            "CLOSE_SEQUENCE",
        ),
        "framing": (
            "EXTREME_WIDE",
            "WIDE",
            "MEDIUM_WIDE",
            "MEDIUM",
            "MEDIUM_CLOSE_UP",
            "CLOSE_UP",
            "EXTREME_CLOSE_UP",
        ),
        "action_class": (
            "STATIC",
            "MOVE",
            "PERFORM",
            "EXPRESS",
            "INTERACT",
            "TRANSITION",
        ),
        "camera_movement": (
            "STATIC",
            "PAN",
            "TILT",
            "DOLLY",
            "TRUCK",
            "PEDESTAL",
            "ZOOM",
            "ARC",
            "HANDHELD",
        ),
        "camera_direction": ("NONE", "LEFT", "RIGHT", "UP", "DOWN", "IN", "OUT"),
        "camera_speed": ("NONE", "SLOW", "MODERATE", "FAST"),
    },
    "composition": {
        "subject_placement": ("CENTER", "LEFT_THIRD", "RIGHT_THIRD"),
        "face_coverage": (
            "FACE_MOST_OF_FRAME",
            "EYES_AND_FACE_TIGHT",
            "UPPER_BODY_AND_FACE_VISIBLE",
        ),
        "focus_target": ("EYES_AND_TEARS", "FACE_AND_TEARS", "FACE", "EYES"),
        "background_visibility": (
            "RAIN_SOFTLY_BLURRED",
            "RAIN_VISIBLE_BEHIND_FACE",
            "BACKGROUND_SOFTLY_BLURRED",
            "ENVIRONMENT_VISIBLE_BEHIND_SUBJECT",
        ),
    },
    "performance": {
        "eye_state": ("TEARS_WELLING", "EYES_SQUEEZED_BY_CRYING", "EYES_RELAXED"),
        "tear_state": (
            "ONE_TEAR_ROLLING",
            "TEARS_STREAMING_DOWN_CHEEKS",
            "NO_VISIBLE_TEARS",
        ),
        "mouth_state": (
            "LOWER_LIP_TREMBLING",
            "MOUTH_TIGHT_WITH_SOBS",
            "MOUTH_RELAXED",
            "MOUTH_SMILING",
        ),
        "expression_intensity": ("RESTRAINED", "STRONG", "NEUTRAL"),
    },
    "lighting": {
        "light_source": ("OVERCAST_DAYLIGHT", "SOFT_AMBIENT_DAYLIGHT"),
        "light_quality": ("SOFT_DIFFUSED", "LOW_CONTRAST"),
        "face_readability": ("FULLY_READABLE",),
        "tear_highlight": ("VISIBLE",),
    },
    "continuity": {
        "entry_subject_state": (
            "FACE_WET_AND_CRYING",
            "TEARS_ALREADY_VISIBLE",
            "SAME_SUBJECT_STATE",
        ),
        "entry_environment_state": ("CONTINUOUS_RAIN", "SAME_ENVIRONMENT"),
        "exit_subject_state": (
            "SAME_FACE_WITH_VISIBLE_TEARS",
            "CRYING_CONTINUES",
            "SUBJECT_STATE_CONTINUES",
        ),
        "exit_environment_state": ("CONTINUOUS_RAIN", "SAME_ENVIRONMENT"),
    },
}

TOKEN_DESCRIPTIONS: Final[dict[str, dict[str, dict[str, str]]]] = {
    "composition": {
        "subject_placement": {
            "CENTER": "主体位于画面中央",
            "LEFT_THIRD": "主体位于画面左侧三分线",
            "RIGHT_THIRD": "主体位于画面右侧三分线",
        },
        "face_coverage": {
            "FACE_MOST_OF_FRAME": "面部占据画面大部分区域",
            "EYES_AND_FACE_TIGHT": "眼睛与面部紧贴画面边界",
            "UPPER_BODY_AND_FACE_VISIBLE": "上半身与面部均保持可见",
        },
        "focus_target": {
            "EYES_AND_TEARS": "焦点落在眼睛和泪水",
            "FACE_AND_TEARS": "焦点落在面部与可见泪水",
            "FACE": "焦点落在面部",
            "EYES": "焦点落在眼睛",
        },
        "background_visibility": {
            "RAIN_SOFTLY_BLURRED": "雨景在面部后方柔化可见",
            "RAIN_VISIBLE_BEHIND_FACE": "面部后方仍可看见持续降雨",
            "BACKGROUND_SOFTLY_BLURRED": "主体后方背景保持柔化可见",
            "ENVIRONMENT_VISIBLE_BEHIND_SUBJECT": "主体后方环境保持可见",
        },
    },
    "performance": {
        "eye_state": {
            "TEARS_WELLING": "眼中蓄满泪水",
            "EYES_SQUEEZED_BY_CRYING": "双眼因哭泣而收紧",
            "EYES_RELAXED": "双眼保持自然放松",
        },
        "tear_state": {
            "ONE_TEAR_ROLLING": "一滴泪沿面颊滑落",
            "TEARS_STREAMING_DOWN_CHEEKS": "泪水持续沿面颊流下",
            "NO_VISIBLE_TEARS": "面部没有可见泪水",
        },
        "mouth_state": {
            "LOWER_LIP_TREMBLING": "下唇轻微颤抖",
            "MOUTH_TIGHT_WITH_SOBS": "嘴角因抽泣而收紧",
            "MOUTH_RELAXED": "嘴部保持自然放松",
            "MOUTH_SMILING": "嘴角保持可见微笑",
        },
        "expression_intensity": {
            "RESTRAINED": "哭泣表演强度克制",
            "STRONG": "哭泣表演强度明显",
            "NEUTRAL": "表演强度保持自然",
        },
    },
    "lighting": {
        "light_source": {
            "OVERCAST_DAYLIGHT": "阴天自然光",
            "SOFT_AMBIENT_DAYLIGHT": "柔和环境日光",
        },
        "light_quality": {
            "SOFT_DIFFUSED": "光线柔和漫射",
            "LOW_CONTRAST": "画面对比度柔和",
        },
        "face_readability": {"FULLY_READABLE": "面部细节清晰可读"},
        "tear_highlight": {"VISIBLE": "泪水高光保持可见"},
    },
    "continuity": {
        "entry_subject_state": {
            "FACE_WET_AND_CRYING": "同一孩子面部已被雨水打湿并正在哭泣",
            "TEARS_ALREADY_VISIBLE": "同一孩子面部已有可见泪水并正在哭泣",
            "SAME_SUBJECT_STATE": "同一主体保持进入镜头时的可见状态",
        },
        "entry_environment_state": {
            "CONTINUOUS_RAIN": "背景保持持续降雨",
            "SAME_ENVIRONMENT": "背景环境保持连续",
        },
        "exit_subject_state": {
            "SAME_FACE_WITH_VISIBLE_TEARS": "同一孩子面部、哭泣状态和可见泪水保持连续",
            "CRYING_CONTINUES": "同一孩子继续哭泣且泪水保持可见",
            "SUBJECT_STATE_CONTINUES": "同一主体的可见状态保持连续",
        },
        "exit_environment_state": {
            "CONTINUOUS_RAIN": "背景仍保持持续降雨",
            "SAME_ENVIRONMENT": "背景环境继续保持连续",
        },
    },
}


def describe_token(stage: str, field: str, token: str) -> str:
    """把受控标记确定性映射为可观察文本；未知值原样保留供观察器报告。"""

    return TOKEN_DESCRIPTIONS.get(stage, {}).get(field, {}).get(token, token)


def compiler_contract() -> dict[str, Any]:
    """返回可被证据包摘要绑定的版本化编译合同。"""

    return {
        "schema_version": CONTROLLED_OBSERVABILITY_COMPILER_VERSION,
        "stage_order": list(OBSERVABLE_STAGE_ORDER),
        "required_keys": {
            stage: sorted(keys) for stage, keys in STRUCTURED_STAGE_REQUIRED_KEYS.items()
        },
        "allowed_values": {
            stage: {field: list(values) for field, values in fields.items()}
            for stage, fields in STRUCTURED_STAGE_ALLOWED_VALUES.items()
        },
        "token_descriptions": TOKEN_DESCRIPTIONS,
        "observable_check_derivation": [
            "request_subject_identity_and_selected_continuity",
            "selected_framing_and_face_coverage",
            "selected_action_and_performance",
            "selected_scene_environment_and_continuity",
            "selected_camera_contract",
        ],
        "automatic_repair": False,
        "creative_fact_defaulting": False,
        "formal_decision_created": False,
    }


def compiler_contract_sha256() -> str:
    encoded = json.dumps(
        compiler_contract(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


CONTROLLED_STAGE_FIELDS: Final[dict[str, tuple[str, ...]]] = {
    stage: tuple(sorted(fields))
    for stage, fields in STRUCTURED_STAGE_ALLOWED_VALUES.items()
}


def observe_controlled_semantic_stability(
    runs: list[dict[str, dict[str, Any]] | None],
) -> dict[str, Any]:
    """观察受控字段的一致性，不把观察结果升级为质量裁决。"""

    comparable: list[dict[str, str]] = []
    excluded_run_indices: list[int] = []
    for run_index, stages in enumerate(runs, start=1):
        if not isinstance(stages, dict):
            excluded_run_indices.append(run_index)
            continue
        flattened: dict[str, str] = {}
        valid = True
        for stage, fields in CONTROLLED_STAGE_FIELDS.items():
            payload = stages.get(stage)
            if not isinstance(payload, dict):
                valid = False
                break
            for field in fields:
                value = payload.get(field)
                if value not in STRUCTURED_STAGE_ALLOWED_VALUES[stage][field]:
                    valid = False
                    break
                flattened[f"{stage}.{field}"] = value
            if not valid:
                break
        if valid:
            comparable.append(flattened)
        else:
            excluded_run_indices.append(run_index)

    field_consistency: dict[str, dict[str, Any]] = {}
    for field in sorted(
        field for stage, fields in CONTROLLED_STAGE_FIELDS.items() for field in (
            f"{stage}.{name}" for name in fields
        )
    ):
        groups: dict[str, list[int]] = {}
        comparable_position = 0
        for run_index, stages in enumerate(runs, start=1):
            if run_index in excluded_run_indices:
                continue
            value = comparable[comparable_position][field]
            comparable_position += 1
            groups.setdefault(value, []).append(run_index)
        largest = max((len(indices) for indices in groups.values()), default=0)
        field_consistency[field] = {
            "distinct_value_count": len(groups),
            "largest_group_ratio": (
                round(largest / len(comparable), 4) if comparable else None
            ),
            "groups": [
                {"value": value, "run_indices": indices}
                for value, indices in sorted(groups.items())
            ],
        }

    fingerprints: dict[str, list[int]] = {}
    comparable_position = 0
    for run_index in range(1, len(runs) + 1):
        if run_index in excluded_run_indices:
            continue
        fingerprint = json.dumps(
            comparable[comparable_position],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        comparable_position += 1
        fingerprints.setdefault(fingerprint, []).append(run_index)
    largest_group_size = max((len(indices) for indices in fingerprints.values()), default=0)
    return {
        "schema_version": "controlled-semantic-stability-observation.v1",
        "run_count": len(runs),
        "comparable_run_count": len(comparable),
        "excluded_run_indices": excluded_run_indices,
        "comparison_performed": len(comparable) >= 2,
        "exact_controlled_semantic_group_count": len(fingerprints),
        "largest_exact_controlled_semantic_group_ratio": (
            round(largest_group_size / len(comparable), 4) if comparable else None
        ),
        "field_consistency": field_consistency,
        "formal_decision_created": False,
        "creative_review_required": True,
    }
