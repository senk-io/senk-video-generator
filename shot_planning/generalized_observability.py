"""第八版通用可观察阶段的受控词汇与确定性编译合同。"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Final

from .controlled_context import (
    TOKENIZED_CONTEXT_ALLOWED_VALUES,
    describe_context_token,
)
from .structured_observability import STRUCTURED_STAGE_ALLOWED_VALUES


GENERALIZED_OBSERVABILITY_COMPILER_VERSION: Final[str] = (
    "structured-observability-compiler.v2"
)
GENERALIZED_STAGE_ORDER: Final[tuple[str, ...]] = (
    "scene_context",
    "beat_purpose",
    "shot_core",
    "composition",
    "performance",
    "lighting",
    "continuity",
)
GENERALIZED_STAGE_REQUIRED_KEYS: Final[dict[str, frozenset[str]]] = {
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
            "subject_scale",
            "focus_target",
            "background_visibility",
        }
    ),
    "performance": frozenset(
        {
            "orientation_state",
            "visible_action_state",
            "detail_state",
            "performance_intensity",
        }
    ),
    "lighting": frozenset(
        {
            "light_source",
            "light_quality",
            "subject_readability",
            "highlight_state",
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

GENERALIZED_STAGE_ALLOWED_VALUES: Final[dict[str, dict[str, tuple[str, ...]]]] = {
    "shot_core": STRUCTURED_STAGE_ALLOWED_VALUES["shot_core"],
    "composition": {
        "subject_placement": ("CENTER", "LEFT_THIRD", "RIGHT_THIRD"),
        "subject_scale": (
            "FACE_DOMINANT",
            "UPPER_BODY_VISIBLE",
            "FULL_SUBJECT_VISIBLE",
            "SUBJECT_SMALL_IN_ENVIRONMENT",
        ),
        "focus_target": ("EYES_AND_TEARS", "FACE", "SUBJECT", "SUBJECT_ACTION"),
        "background_visibility": (
            "RAIN_SOFTLY_BLURRED",
            "BACKGROUND_SOFTLY_BLURRED",
            "ENVIRONMENT_VISIBLE_BEHIND_SUBJECT",
            "STREET_VISIBLE_AROUND_SUBJECT",
        ),
    },
    "performance": {
        "orientation_state": (
            "FACING_CAMERA",
            "NATURAL_FORWARD",
            "MOVING_LEFT_TO_RIGHT",
        ),
        "visible_action_state": ("CRYING", "SMILING", "FORWARD_MOTION"),
        "detail_state": (
            "TEARS_VISIBLE",
            "RELAXED_FACE_VISIBLE",
            "MOTION_DETAIL_VISIBLE",
        ),
        "performance_intensity": ("RESTRAINED", "GENTLE", "MODERATE"),
    },
    "lighting": {
        "light_source": (
            "OVERCAST_DAYLIGHT",
            "INTERIOR_SOFT_LIGHT",
            "NIGHT_STREET_LIGHT",
        ),
        "light_quality": ("SOFT_DIFFUSED", "LOW_CONTRAST", "DIRECTIONAL_LOW_KEY"),
        "subject_readability": (
            "FACE_FULLY_READABLE",
            "SUBJECT_FULLY_READABLE",
            "MOTION_FULLY_READABLE",
        ),
        "highlight_state": (
            "TEAR_HIGHLIGHT_VISIBLE",
            "NATURAL_FACE_HIGHLIGHT",
            "SUBJECT_EDGE_HIGHLIGHT",
            "NO_SPECIAL_HIGHLIGHT",
        ),
    },
    "continuity": {
        "entry_subject_state": (
            "SUBJECT_ALREADY_CRYING",
            "SUBJECT_ALREADY_SMILING",
            "SUBJECT_ENTERING_FROM_LEFT",
        ),
        "entry_environment_state": (
            "CONTINUOUS_RAIN",
            "SAME_INDOOR_ENVIRONMENT",
            "SAME_NIGHT_STREET",
        ),
        "exit_subject_state": (
            "CRYING_CONTINUES",
            "SMILE_CONTINUES",
            "SUBJECT_EXITS_RIGHT",
        ),
        "exit_environment_state": (
            "CONTINUOUS_RAIN",
            "SAME_INDOOR_ENVIRONMENT",
            "SAME_NIGHT_STREET",
        ),
    },
}

GENERALIZED_TOKEN_DESCRIPTIONS: Final[dict[str, dict[str, dict[str, str]]]] = {
    "composition": {
        "subject_placement": {
            "CENTER": "主体位于画面中央",
            "LEFT_THIRD": "主体位于画面左侧三分线",
            "RIGHT_THIRD": "主体位于画面右侧三分线",
        },
        "subject_scale": {
            "FACE_DOMINANT": "主体面部占据画面大部分区域",
            "UPPER_BODY_VISIBLE": "主体上半身保持完整可见",
            "FULL_SUBJECT_VISIBLE": "主体整体保持完整可见",
            "SUBJECT_SMALL_IN_ENVIRONMENT": "主体在环境中保持较小画面占比",
        },
        "focus_target": {
            "EYES_AND_TEARS": "焦点落在眼睛与可见泪水",
            "FACE": "焦点落在主体面部",
            "SUBJECT": "焦点落在主体整体",
            "SUBJECT_ACTION": "焦点落在主体的可见动作",
        },
        "background_visibility": {
            "RAIN_SOFTLY_BLURRED": "主体后方雨景柔化可见",
            "BACKGROUND_SOFTLY_BLURRED": "主体后方背景柔化可见",
            "ENVIRONMENT_VISIBLE_BEHIND_SUBJECT": "主体后方环境保持可见",
            "STREET_VISIBLE_AROUND_SUBJECT": "主体周围街道环境保持可见",
        },
    },
    "performance": {
        "orientation_state": {
            "FACING_CAMERA": "主体朝向相机",
            "NATURAL_FORWARD": "主体保持自然朝前",
            "MOVING_LEFT_TO_RIGHT": "主体从画面左侧向右侧移动",
        },
        "visible_action_state": {
            "CRYING": "哭泣状态清楚可见",
            "SMILING": "微笑状态清楚可见",
            "FORWARD_MOTION": "向前运动状态清楚可见",
        },
        "detail_state": {
            "TEARS_VISIBLE": "面部泪水清楚可见",
            "RELAXED_FACE_VISIBLE": "放松的面部细节清楚可见",
            "MOTION_DETAIL_VISIBLE": "运动细节清楚可见",
        },
        "performance_intensity": {
            "RESTRAINED": "可见动作强度保持克制",
            "GENTLE": "可见动作强度保持轻柔",
            "MODERATE": "可见动作强度保持适中",
        },
    },
    "lighting": {
        "light_source": {
            "OVERCAST_DAYLIGHT": "阴天自然光照亮主体",
            "INTERIOR_SOFT_LIGHT": "室内柔和光照亮主体",
            "NIGHT_STREET_LIGHT": "夜间街道光照亮主体",
        },
        "light_quality": {
            "SOFT_DIFFUSED": "光线保持柔和漫射",
            "LOW_CONTRAST": "画面对比度保持柔和",
            "DIRECTIONAL_LOW_KEY": "定向低调光保持环境层次",
        },
        "subject_readability": {
            "FACE_FULLY_READABLE": "主体面部细节清晰可读",
            "SUBJECT_FULLY_READABLE": "主体整体细节清晰可读",
            "MOTION_FULLY_READABLE": "主体运动轮廓清晰可读",
        },
        "highlight_state": {
            "TEAR_HIGHLIGHT_VISIBLE": "泪水高光保持可见",
            "NATURAL_FACE_HIGHLIGHT": "面部自然高光保持可见",
            "SUBJECT_EDGE_HIGHLIGHT": "主体边缘高光保持可见",
            "NO_SPECIAL_HIGHLIGHT": "主体不依赖特殊高光辨识",
        },
    },
    "continuity": {
        "entry_subject_state": {
            "SUBJECT_ALREADY_CRYING": "主体进入镜头时已经哭泣",
            "SUBJECT_ALREADY_SMILING": "主体进入镜头时已经微笑",
            "SUBJECT_ENTERING_FROM_LEFT": "主体从画面左侧进入",
        },
        "entry_environment_state": {
            "CONTINUOUS_RAIN": "进入镜头时背景保持持续降雨",
            "SAME_INDOOR_ENVIRONMENT": "进入镜头时室内环境保持连续",
            "SAME_NIGHT_STREET": "进入镜头时夜间街道环境保持连续",
        },
        "exit_subject_state": {
            "CRYING_CONTINUES": "主体离开镜头时继续哭泣",
            "SMILE_CONTINUES": "主体离开镜头时继续微笑",
            "SUBJECT_EXITS_RIGHT": "主体从画面右侧离开",
        },
        "exit_environment_state": {
            "CONTINUOUS_RAIN": "离开镜头时背景仍保持持续降雨",
            "SAME_INDOOR_ENVIRONMENT": "离开镜头时室内环境继续保持连续",
            "SAME_NIGHT_STREET": "离开镜头时夜间街道环境继续保持连续",
        },
    },
}


def describe_generalized_token(stage: str, field: str, token: str) -> str:
    return GENERALIZED_TOKEN_DESCRIPTIONS.get(stage, {}).get(field, {}).get(token, token)


def generalized_compiler_contract() -> dict[str, Any]:
    return {
        "schema_version": GENERALIZED_OBSERVABILITY_COMPILER_VERSION,
        "stage_order": list(GENERALIZED_STAGE_ORDER),
        "required_keys": {
            stage: sorted(keys) for stage, keys in GENERALIZED_STAGE_REQUIRED_KEYS.items()
        },
        "allowed_values": {
            stage: {field: list(values) for field, values in fields.items()}
            for stage, fields in GENERALIZED_STAGE_ALLOWED_VALUES.items()
        },
        "token_descriptions": GENERALIZED_TOKEN_DESCRIPTIONS,
        "observable_check_derivation": [
            "request_subject_identity_and_selected_continuity",
            "selected_framing_and_subject_scale",
            "selected_action_and_visible_performance",
            "selected_scene_environment_and_continuity",
            "selected_camera_contract",
        ],
        "cross_stage_consistency_rules": [
            "eyes_and_tears_focus_requires_visible_tears",
            "tear_highlight_requires_visible_tears",
            "visible_action_requires_matching_entry_and_exit_subject_state",
            "scene_environment_requires_matching_continuity_environment",
            "scene_environment_requires_matching_continuity_anchor",
            "left_to_right_motion_requires_left_entry_and_right_exit",
        ],
        "automatic_repair": False,
        "creative_fact_defaulting": False,
        "formal_decision_created": False,
    }


def generalized_compiler_contract_sha256() -> str:
    encoded = json.dumps(
        generalized_compiler_contract(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _compiled_text(stage: str, payload: dict[str, Any], fields: tuple[str, ...]) -> str:
    return "，".join(
        describe_generalized_token(stage, field, str(payload.get(field, "")))
        for field in fields
    )


def _framing_text(value: Any) -> str:
    return {
        "EXTREME_WIDE": "大远景",
        "WIDE": "全景",
        "MEDIUM_WIDE": "中全景",
        "MEDIUM": "中景",
        "MEDIUM_CLOSE_UP": "中近景",
        "CLOSE_UP": "特写",
        "EXTREME_CLOSE_UP": "极近特写",
    }.get(str(value), str(value))


def _camera_check(core: dict[str, Any]) -> str:
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


def build_generalized_payload(
    stages: dict[str, dict[str, Any]], request: dict[str, Any]
) -> dict[str, Any]:
    """只把模型选中的通用标记展开为提案载荷，不注入创作默认值。"""

    context = stages["scene_context"]
    core = stages["shot_core"]
    composition = stages["composition"]
    performance = stages["performance"]
    lighting = stages["lighting"]
    continuity = stages["continuity"]
    environment = describe_context_token("environment", str(context["environment"]))
    entry_environment = describe_generalized_token(
        "continuity", "entry_environment_state", str(continuity["entry_environment_state"])
    )
    exit_environment = describe_generalized_token(
        "continuity", "exit_environment_state", str(continuity["exit_environment_state"])
    )
    visible_action = describe_generalized_token(
        "performance", "visible_action_state", str(performance["visible_action_state"])
    )
    subject_scale = describe_generalized_token(
        "composition", "subject_scale", str(composition["subject_scale"])
    )
    subject_ids = request["required_subject_ids"]
    return {
        "scenes": [
            {
                "location": describe_context_token("location", str(context["location"])),
                "time": describe_context_token("time", str(context["time"])),
                "environment": environment,
                "continuity_anchors": [
                    describe_context_token(
                        "continuity_anchor", str(context["continuity_anchor"])
                    )
                ],
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
                "purpose": stages["beat_purpose"]["purpose"],
                "action": core["action_description"],
            }
        ],
        "shots": [
            {
                "scene_ordinal": 1,
                "beat_ordinals": [1],
                "primary_purpose": core["primary_purpose"],
                "target_duration_seconds": request["target_duration_seconds"],
                "framing": core["framing"],
                "action_class": core["action_class"],
                "action_description": core["action_description"],
                "composition": _compiled_text(
                    "composition",
                    composition,
                    (
                        "subject_placement",
                        "subject_scale",
                        "focus_target",
                        "background_visibility",
                    ),
                ),
                "camera_movement": core["camera_movement"],
                "camera_direction": core["camera_direction"],
                "camera_speed": core["camera_speed"],
                "performance": _compiled_text(
                    "performance",
                    performance,
                    (
                        "orientation_state",
                        "visible_action_state",
                        "detail_state",
                        "performance_intensity",
                    ),
                ),
                "lighting": _compiled_text(
                    "lighting",
                    lighting,
                    (
                        "light_source",
                        "light_quality",
                        "subject_readability",
                        "highlight_state",
                    ),
                ),
                "continuity_in": "进入镜头时，"
                + _compiled_text(
                    "continuity",
                    continuity,
                    ("entry_subject_state", "entry_environment_state"),
                ),
                "continuity_out": "离开镜头时，"
                + _compiled_text(
                    "continuity",
                    continuity,
                    ("exit_subject_state", "exit_environment_state"),
                ),
                "observable_checks": [
                    "主体 " + "、".join(subject_ids) + " 始终保持同一可见身份",
                    f"景别保持为{_framing_text(core['framing'])}，{subject_scale}",
                    f"主要动作保持为{core['action_description']}，同时{visible_action}",
                    f"场景环境保持{environment}，{entry_environment}并且{exit_environment}",
                    _camera_check(core),
                ],
            }
        ],
    }


def observe_generalized_stage_consistency(
    stages: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    observations: list[dict[str, Any]] = []
    composition = stages.get("composition", {})
    performance = stages.get("performance", {})
    lighting = stages.get("lighting", {})
    continuity = stages.get("continuity", {})
    context = stages.get("scene_context", {})
    tears_visible = performance.get("detail_state") == "TEARS_VISIBLE"
    if composition.get("focus_target") == "EYES_AND_TEARS" and not tears_visible:
        observations.append(
            {
                "code": "GENERALIZED_TEAR_FOCUS_WITHOUT_VISIBLE_TEARS",
                "category": "CROSS_STAGE_SEMANTIC",
                "path": "$.stages.composition.focus_target",
                "expected": "performance.detail_state=TEARS_VISIBLE",
                "observed": performance.get("detail_state"),
            }
        )
    if lighting.get("highlight_state") == "TEAR_HIGHLIGHT_VISIBLE" and not tears_visible:
        observations.append(
            {
                "code": "GENERALIZED_TEAR_HIGHLIGHT_WITHOUT_VISIBLE_TEARS",
                "category": "CROSS_STAGE_SEMANTIC",
                "path": "$.stages.lighting.highlight_state",
                "expected": "performance.detail_state=TEARS_VISIBLE",
                "observed": performance.get("detail_state"),
            }
        )
    if performance.get("orientation_state") == "MOVING_LEFT_TO_RIGHT" and (
        continuity.get("entry_subject_state") != "SUBJECT_ENTERING_FROM_LEFT"
        or continuity.get("exit_subject_state") != "SUBJECT_EXITS_RIGHT"
    ):
        observations.append(
            {
                "code": "GENERALIZED_LEFT_TO_RIGHT_CONTINUITY_MISMATCH",
                "category": "CROSS_STAGE_CONTINUITY",
                "path": "$.stages.continuity",
                "expected": {
                    "entry_subject_state": "SUBJECT_ENTERING_FROM_LEFT",
                    "exit_subject_state": "SUBJECT_EXITS_RIGHT",
                },
                "observed": {
                    "entry_subject_state": continuity.get("entry_subject_state"),
                    "exit_subject_state": continuity.get("exit_subject_state"),
                },
            }
        )
    visible_action_state = performance.get("visible_action_state")
    expected_subject_continuity = {
        "CRYING": ("SUBJECT_ALREADY_CRYING", "CRYING_CONTINUES"),
        "SMILING": ("SUBJECT_ALREADY_SMILING", "SMILE_CONTINUES"),
        "FORWARD_MOTION": ("SUBJECT_ENTERING_FROM_LEFT", "SUBJECT_EXITS_RIGHT"),
    }.get(visible_action_state if isinstance(visible_action_state, str) else None)
    if expected_subject_continuity is not None and (
        continuity.get("entry_subject_state") != expected_subject_continuity[0]
        or continuity.get("exit_subject_state") != expected_subject_continuity[1]
    ):
        observations.append(
            {
                "code": "GENERALIZED_ACTION_CONTINUITY_MISMATCH",
                "category": "CROSS_STAGE_CONTINUITY",
                "path": "$.stages.continuity",
                "expected": {
                    "entry_subject_state": expected_subject_continuity[0],
                    "exit_subject_state": expected_subject_continuity[1],
                },
                "observed": {
                    "entry_subject_state": continuity.get("entry_subject_state"),
                    "exit_subject_state": continuity.get("exit_subject_state"),
                },
            }
        )
    environment = context.get("environment")
    environment_key = environment if isinstance(environment, str) else None
    expected_anchor = {
        "CONTINUOUS_RAIN": "SAME_SUBJECT_AND_CONTINUOUS_RAIN",
        "STABLE_ENVIRONMENT": "SAME_SUBJECT_AND_ENVIRONMENT",
    }.get(environment_key)
    if context.get("continuity_anchor") != expected_anchor:
        observations.append(
            {
                "code": "GENERALIZED_CONTEXT_ANCHOR_MISMATCH",
                "category": "CROSS_STAGE_CONTINUITY",
                "path": "$.stages.scene_context.continuity_anchor",
                "expected": expected_anchor,
                "observed": context.get("continuity_anchor"),
            }
        )
    expected_environment_states = {
        "CONTINUOUS_RAIN": ("CONTINUOUS_RAIN", "CONTINUOUS_RAIN"),
        "STABLE_ENVIRONMENT": {
            ("SAME_INDOOR_ENVIRONMENT", "SAME_INDOOR_ENVIRONMENT"),
            ("SAME_NIGHT_STREET", "SAME_NIGHT_STREET"),
        },
    }
    entry_environment = continuity.get("entry_environment_state")
    exit_environment = continuity.get("exit_environment_state")
    if environment_key == "CONTINUOUS_RAIN":
        expected_entry, expected_exit = expected_environment_states[environment_key]
        environment_matches = (
            entry_environment == expected_entry and exit_environment == expected_exit
        )
        expected_environment: Any = {
            "entry_environment_state": expected_entry,
            "exit_environment_state": expected_exit,
        }
    else:
        allowed_pairs = expected_environment_states.get(environment_key, set())
        environment_matches = (entry_environment, exit_environment) in allowed_pairs
        expected_environment = [
            {
                "entry_environment_state": entry,
                "exit_environment_state": exit_state,
            }
            for entry, exit_state in sorted(allowed_pairs)
        ]
    if not environment_matches:
        observations.append(
            {
                "code": "GENERALIZED_ENVIRONMENT_CONTINUITY_MISMATCH",
                "category": "CROSS_STAGE_CONTINUITY",
                "path": "$.stages.continuity",
                "expected": expected_environment,
                "observed": {
                    "entry_environment_state": entry_environment,
                    "exit_environment_state": exit_environment,
                },
            }
        )
    return observations


def observe_generalized_semantic_stability(
    runs: list[dict[str, dict[str, Any]] | None],
) -> dict[str, Any]:
    allowed_values_by_stage: dict[str, dict[str, tuple[str, ...]]] = {
        "scene_context": TOKENIZED_CONTEXT_ALLOWED_VALUES["scene_context"],
        "beat_purpose": {
            "purpose": GENERALIZED_STAGE_ALLOWED_VALUES["shot_core"][
                "primary_purpose"
            ]
        },
        **GENERALIZED_STAGE_ALLOWED_VALUES,
    }
    fields = {
        stage: tuple(sorted(stage_fields))
        for stage, stage_fields in allowed_values_by_stage.items()
    }
    comparable: list[tuple[int, dict[str, str]]] = []
    excluded_run_indices: list[int] = []
    for run_index, stages in enumerate(runs, start=1):
        if not isinstance(stages, dict):
            excluded_run_indices.append(run_index)
            continue
        flattened: dict[str, str] = {}
        valid = True
        for stage, names in fields.items():
            payload = stages.get(stage)
            if not isinstance(payload, dict):
                valid = False
                break
            for name in names:
                value = payload.get(name)
                if value not in allowed_values_by_stage[stage][name]:
                    valid = False
                    break
                flattened[f"{stage}.{name}"] = value
            if not valid:
                break
        if valid:
            comparable.append((run_index, flattened))
        else:
            excluded_run_indices.append(run_index)

    field_consistency: dict[str, dict[str, Any]] = {}
    all_fields = sorted(
        f"{stage}.{name}" for stage, names in fields.items() for name in names
    )
    for field in all_fields:
        groups: dict[str, list[int]] = {}
        for run_index, flattened in comparable:
            groups.setdefault(flattened[field], []).append(run_index)
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
    for run_index, flattened in comparable:
        fingerprint = json.dumps(
            flattened, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        fingerprints.setdefault(fingerprint, []).append(run_index)
    largest_group_size = max((len(indices) for indices in fingerprints.values()), default=0)
    return {
        "schema_version": "controlled-semantic-stability-observation.v2",
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
