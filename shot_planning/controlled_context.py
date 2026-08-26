"""第七版场景角色标记与确定性上下文编译合同。"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Final


TOKENIZED_CONTEXT_COMPILER_VERSION: Final[str] = "tokenized-context-compiler.v1"
TOKENIZED_CONTEXT_STAGE_ORDER: Final[tuple[str, ...]] = (
    "scene_context",
    "beat_purpose",
    "shot_core",
    "composition",
    "performance",
    "lighting",
    "continuity",
)
TOKENIZED_CONTEXT_STAGE_KEYS: Final[dict[str, frozenset[str]]] = {
    "scene_context": frozenset(
        {"location", "time", "environment", "continuity_anchor"}
    ),
    "beat_purpose": frozenset({"purpose"}),
}
TOKENIZED_CONTEXT_ALLOWED_VALUES: Final[dict[str, dict[str, tuple[str, ...]]]] = {
    "scene_context": {
        "location": ("UNSPECIFIED_LOCATION", "INDOOR_LOCATION", "OUTDOOR_LOCATION"),
        "time": ("UNSPECIFIED_TIME", "DAY", "NIGHT"),
        "environment": ("CONTINUOUS_RAIN", "STABLE_ENVIRONMENT"),
        "continuity_anchor": (
            "SAME_SUBJECT_AND_CONTINUOUS_RAIN",
            "SAME_SUBJECT_AND_ENVIRONMENT",
        ),
    }
}
TOKENIZED_CONTEXT_DESCRIPTIONS: Final[dict[str, dict[str, str]]] = {
    "location": {
        "UNSPECIFIED_LOCATION": "未明确地点",
        "INDOOR_LOCATION": "室内地点",
        "OUTDOOR_LOCATION": "室外地点",
    },
    "time": {
        "UNSPECIFIED_TIME": "未明确时间",
        "DAY": "白天",
        "NIGHT": "夜晚",
    },
    "environment": {
        "CONTINUOUS_RAIN": "持续降雨",
        "STABLE_ENVIRONMENT": "环境状态保持稳定",
    },
    "continuity_anchor": {
        "SAME_SUBJECT_AND_CONTINUOUS_RAIN": "同一主体与持续降雨",
        "SAME_SUBJECT_AND_ENVIRONMENT": "同一主体与同一环境状态",
    },
}


def describe_context_token(field: str, token: str) -> str:
    return TOKENIZED_CONTEXT_DESCRIPTIONS.get(field, {}).get(token, token)


def tokenized_context_compiler_contract() -> dict[str, Any]:
    return {
        "schema_version": TOKENIZED_CONTEXT_COMPILER_VERSION,
        "stage_order": list(TOKENIZED_CONTEXT_STAGE_ORDER),
        "required_keys": {
            stage: sorted(keys) for stage, keys in TOKENIZED_CONTEXT_STAGE_KEYS.items()
        },
        "allowed_values": {
            stage: {field: list(values) for field, values in fields.items()}
            for stage, fields in TOKENIZED_CONTEXT_ALLOWED_VALUES.items()
        },
        "token_descriptions": TOKENIZED_CONTEXT_DESCRIPTIONS,
        "beat_action_derivation": "reuse_shot_core_action_description",
        "automatic_repair": False,
        "creative_fact_defaulting": False,
        "formal_decision_created": False,
    }


def tokenized_context_compiler_contract_sha256() -> str:
    encoded = json.dumps(
        tokenized_context_compiler_contract(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
