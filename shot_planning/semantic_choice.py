"""第十版标量候选的通用中文释义合同。"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Final

from .controlled_context import TOKENIZED_CONTEXT_DESCRIPTIONS
from .generalized_observability import GENERALIZED_TOKEN_DESCRIPTIONS


SEMANTIC_CHOICE_GLOSSARY_VERSION: Final[str] = "semantic-choice-glossary.v1"

CORE_TOKEN_DESCRIPTIONS: Final[dict[str, dict[str, str]]] = {
    "primary_purpose": {
        "ESTABLISH_CONTEXT": "建立地点、时间或环境",
        "DEVELOP_ACTION": "推进主体的主要动作",
        "EMPHASIZE_EMOTION": "强调主体的情绪或表情",
        "REVEAL_INFORMATION": "揭示新的可见信息",
        "TRANSITION": "连接前后场景或动作",
        "CLOSE_SEQUENCE": "结束当前动作段落",
    },
    "framing": {
        "EXTREME_WIDE": "大远景",
        "WIDE": "全景",
        "MEDIUM_WIDE": "中全景",
        "MEDIUM": "中景",
        "MEDIUM_CLOSE_UP": "中近景",
        "CLOSE_UP": "特写",
        "EXTREME_CLOSE_UP": "极近特写",
    },
    "action_class": {
        "STATIC": "主体基本静止",
        "MOVE": "主体发生位置移动",
        "PERFORM": "主体执行可见表演动作",
        "EXPRESS": "主体呈现情绪或表情",
        "INTERACT": "主体与人或物互动",
        "TRANSITION": "主体或画面进入过渡状态",
    },
    "camera_movement": {
        "STATIC": "相机固定不动",
        "PAN": "相机水平摇摄；不是主体水平移动",
        "TILT": "相机垂直摇摄",
        "DOLLY": "相机向前或向后移动",
        "TRUCK": "相机向左或向右平移",
        "PEDESTAL": "相机整体升高或降低",
        "ZOOM": "镜头光学推近或拉远",
        "ARC": "相机绕主体弧形移动",
        "HANDHELD": "相机手持运动",
    },
    "camera_direction": {
        "NONE": "相机没有运动方向",
        "LEFT": "相机向左运动",
        "RIGHT": "相机向右运动；不是主体向右移动",
        "UP": "相机向上运动",
        "DOWN": "相机向下运动",
        "IN": "相机向内推近",
        "OUT": "相机向外拉远",
    },
    "camera_speed": {
        "NONE": "相机没有运动速度",
        "SLOW": "相机缓慢运动",
        "MODERATE": "相机中速运动",
        "FAST": "相机快速运动",
    },
}


def semantic_choice_glossary_contract() -> dict[str, Any]:
    return {
        "schema_version": SEMANTIC_CHOICE_GLOSSARY_VERSION,
        "scene_context_token_descriptions": TOKENIZED_CONTEXT_DESCRIPTIONS,
        "core_token_descriptions": CORE_TOKEN_DESCRIPTIONS,
        "generalized_token_descriptions": GENERALIZED_TOKEN_DESCRIPTIONS,
        "interpretation_rules": [
            "choose_by_source_meaning_not_candidate_position",
            "explicit_framing_word_maps_to_framing_token",
            "subject_motion_does_not_imply_camera_motion",
            "camera_motion_requires_explicit_camera_or_lens_motion_language",
            "entry_state_describes_beginning_and_exit_state_describes_end",
        ],
        "held_out_expected_values_in_prompt": False,
        "automatic_repair": False,
        "formal_decision_created": False,
    }


def semantic_choice_glossary_sha256() -> str:
    encoded = json.dumps(
        semantic_choice_glossary_contract(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def choice_glossary_for_stage(
    stage: str,
    allowed_choices: dict[str, str],
) -> dict[str, dict[str, str]]:
    """只返回当前提示已允许候选的释义，不泄漏保留答案。"""

    if stage == "scene_context":
        descriptions = TOKENIZED_CONTEXT_DESCRIPTIONS
    elif stage == "beat_purpose":
        descriptions = {"purpose": CORE_TOKEN_DESCRIPTIONS["primary_purpose"]}
    elif stage == "shot_core":
        descriptions = CORE_TOKEN_DESCRIPTIONS
    else:
        descriptions = GENERALIZED_TOKEN_DESCRIPTIONS[stage]
    result: dict[str, dict[str, str]] = {}
    for field, encoded_values in allowed_choices.items():
        tokens = [token.strip() for token in encoded_values.split("|")]
        result[field] = {}
        for token in tokens:
            description = descriptions.get(field, {}).get(token)
            if (
                not isinstance(description, str)
                or not description.strip()
                or description == token
            ):
                raise ValueError(
                    f"候选释义合同缺少 {stage}.{field}.{token} 的明确释义。"
                )
            result[field][token] = description
    return result
