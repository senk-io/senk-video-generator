"""从一句中文镜头请求中提取可追溯的显式事实。

本模块只锁定原句能够直接证明或由已锁定事实确定性推出的字段。没有出现、存在
歧义或无法无损映射到现有枚举的内容继续保留给非权威模型草案或人工澄清。
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from typing import Any, Final

from .contracts import REQUEST_SCHEMA_VERSION_V2, canonical_sha256, validate_request
from .generalized_observability import GENERALIZED_STAGE_REQUIRED_KEYS


SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V1: Final[str] = (
    "shot-source-fact-extractor-contract.v1"
)
SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2: Final[str] = (
    "shot-source-fact-extractor-contract.v2"
)
SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION: Final[str] = (
    SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V1
)
SOURCE_FACT_EXTRACTION_VERSION_V1: Final[str] = "shot-source-fact-extraction.v1"
SOURCE_FACT_EXTRACTION_VERSION_V2: Final[str] = "shot-source-fact-extraction.v2"
SOURCE_FACT_EXTRACTION_VERSION: Final[str] = SOURCE_FACT_EXTRACTION_VERSION_V1
HYBRID_MERGE_CONTRACT_VERSION: Final[str] = "shot-planning-hybrid-merge.v1"

HYBRID_STAGE_ORDER: Final[tuple[str, ...]] = (
    "scene_context",
    "beat_purpose",
    "shot_core",
    "composition",
    "performance",
    "lighting",
    "continuity",
)
HYBRID_STAGE_REQUIRED_KEYS: Final[dict[str, frozenset[str]]] = {
    "scene_context": frozenset(
        {"location", "time", "environment", "continuity_anchor"}
    ),
    "beat_purpose": frozenset({"purpose"}),
    **GENERALIZED_STAGE_REQUIRED_KEYS,
}

CLAUSE_BOUNDARY_PATTERN: Final[str] = r"[，,。；;！？!?]"
NEGATION_MARKERS_V1: Final[tuple[str, ...]] = (
    "不",
    "没",
    "无",
    "非",
    "禁止",
    "避免",
    "取消",
    "去掉",
    "排除",
)
NEGATION_MARKERS_V2: Final[tuple[str, ...]] = (
    "并不是",
    "并没有",
    "并未",
    "并非",
    "不是",
    "没有",
    "从未",
    "尚未",
    "未曾",
    "绝不",
    "并不",
    "不再",
    "不曾",
    "不要",
    "不允许",
    "不许",
    "不让",
    "不得",
    "不应",
    "不该",
    "不准",
    "不可",
    "不必",
    "不需要",
    "没必要",
    "莫要",
    "不想",
    "不愿",
    "无需",
    "无须",
    "别",
    "勿",
    "禁止",
    "避免",
    "取消",
    "去掉",
    "排除",
    "拒绝",
    "停止",
    "不",
    "没",
    "未",
    "非",
    "无",
    "莫",
)
NEGATION_MARKERS: Final[tuple[str, ...]] = NEGATION_MARKERS_V1
ASSERTION_RESET_TOKENS_V2: Final[tuple[str, ...]] = (
    "而是",
    "反而",
    "反倒",
    "改用",
    "改为",
    "换成",
    "转为",
)
FACT_TERM_RIGHT_BOUNDARY_PATTERN_V2: Final[str] = (
    r"(?:而是|反而|反倒|而改用|而改为|而换成|而转为|"
    r"改用|改为|换成|转为)"
)
DIRECT_NEGATIVE_PREFIX_PATTERN_V2: Final[str] = (
    r"(?:"
    r"并不是|并没有|并未|并非|不是|没有|从未|未曾|尚未|绝不|并不|"
    r"不再|不曾|不要(?:再)?|不允许|不许|不让|不得(?!不|已)|"
    r"不应(?:该)?|不该|不准|不可|不必|不需要|没必要|莫要|"
    r"禁止|避免|取消|去掉|排除|拒绝|停止|"
    r"无需(?:使用|采用)?|无须(?:使用|采用)?|"
    r"别(?:再)?(?:用|使用|采用|让)?|勿(?:再)?(?:用|使用|采用|让)?|"
    r"不想(?:再|继续)?|不愿(?:再|继续)?|不|没|未|非|无|莫"
    r")(?:让|用|使用|采用|在|到|是|保持)?"
    r"(?:演员|人物|主体|小孩|行人|自行车|相机|镜头|摄像机|"
    r"摄影机|机位)?\s*\Z"
)
AFFIRMATIVE_IDIOM_PREFIX_PATTERN_V2: Final[str] = (
    r"(?:情不自禁(?:地)?|不由得|没忍住|忍不住|不能不|不得不|"
    r"不得已|从未停止(?:过)?|不禁|不由自主(?:地)?|不但|"
    r"不约而同(?:地)?)"
    r"\s*\Z"
)
AFFIRMATIVE_IDIOM_ANYWHERE_PATTERN_V2: Final[str] = (
    r"(?:情不自禁|不由得|没忍住|忍不住|不能不|不得不|"
    r"不得已|从未停止|不禁|不由自主|不但|不约而同)"
)
AFFIRMATIVE_NEGATOR_MASK_PATTERN_V2: Final[str] = (
    r"(?:情不自禁(?:地)?|不由得|没忍住|忍不住|不能不|不得不|"
    r"不得已|从未停止(?:过)?|不禁|不由自主(?:地)?|不但|"
    r"不约而同(?:地)?|非常|莫妮卡|无锡|未来|未婚)"
)
GENERIC_NEGATOR_PATTERN_V2: Final[str] = r"[不没未非无莫]"
UNRESOLVED_NEGATION_PATTERN_V2: Final[str] = (
    r"(?:并不是|并没有|并未|并非|不是|没有|从未|未曾|尚未|绝不|并不|"
    r"不再|不曾|不要|不允许|不许|不让|不得|不应|不该|不准|"
    r"不可|不必|不需要|没必要|莫要|禁止|避免|取消|"
    r"去掉|排除|拒绝|停止|无需|"
    r"无须|不想|不愿|不怎么|不太|不肯|不能|不会|不在|没在|"
    r"没能|未在|未能|别|勿)"
)
INLINE_CAMERA_NEGATOR_PATTERN_V2: Final[str] = (
    r"(?:并不是|并没有|并未|并非|不是|没有|从未|未曾|尚未|绝不|"
    r"并不|不再|不曾|不要(?:再)?|不允许|不许|不让|不得(?!不|已)|"
    r"不应(?:该)?|不该|不准|不可|不必|不需要|没必要|莫要|"
    r"禁止|避免|拒绝|停止|别|勿|"
    r"不|没|未|非|无)"
)
NEGATED_PURPOSE_SWITCH_PATTERN_V2: Final[str] = (
    r"(?P<starter>不要|别|勿|禁止|避免)(?:再)?为了"
    r"(?P<context>[^，,。；;！？!?]{1,24}?)[，,]?\s*而"
    r"(?P<switch>改用|改为|换成|转为)\s*"
)
NEGATED_DIRECT_SWITCH_PATTERN_V2: Final[str] = (
    r"(?P<starter>不要|别|勿|禁止|避免)(?:再)?\s*"
    r"(?P<switch>改用|改为|换成|转为)\s*"
)
UNRESOLVED_PURPOSE_PREFIX_PATTERN_V2: Final[str] = (
    r"(?:不要|别|勿|禁止|避免)(?:再)?为了"
)
TRAILING_NEGATION_PATTERN_V2: Final[str] = (
    r"\A(?:镜头|画面|构图)?(?:着|了|过)?\s*"
    r"(?:禁止使用|不要使用|不应使用|不该使用|不准使用|不可使用|"
    r"不允许使用|不再使用|无需使用|无须使用|应当避免|必须避免)"
    r"\s*\Z"
)
CONTROLLED_REPLACEMENT_LINK_PATTERN_V2: Final[str] = (
    r"\A(?:镜头|画面)?\s*[，,]?\s*(?:而是|反而|反倒|而?改用|而?改为|"
    r"而?换成|而?转为)\s*\Z"
)
CAMERA_TERMS_V2: Final[tuple[str, ...]] = (
    "相机",
    "镜头",
    "摄像机",
    "摄影机",
    "机位",
)
UNMATCHED_NEGATION_GUARD_RULE_IDS_V2: Final[tuple[str, ...]] = (
    "LOCATION-OUTDOOR-001",
    "LOCATION-INDOOR-001",
    "TIME-DAY-001",
    "TIME-NIGHT-001",
    "FRAMING-CLOSE-UP-001",
    "FRAMING-MEDIUM-001",
    "FRAMING-WIDE-001",
    "ACTION-CRYING-001",
    "ACTION-SMILING-001",
    "INTENSITY-GENTLE-001",
)
POLARITY_POLICY_V2: Final[dict[str, Any]] = {
    "schema_version": "shot-source-fact-polarity-policy.v2",
    "states": [
        "ASSERTED",
        "NEGATED",
        "CONTEXT_ONLY",
        "UNRESOLVED",
        "IGNORED_QUOTED",
    ],
    "soft_clause_boundaries": ["，", ","],
    "hard_clause_boundaries": ["。", "；", ";", "！", "!", "？", "?"],
    "fact_term_right_boundary_pattern": FACT_TERM_RIGHT_BOUNDARY_PATTERN_V2,
    "assertion_reset_tokens": list(ASSERTION_RESET_TOKENS_V2),
    "direct_negative_prefix_pattern": DIRECT_NEGATIVE_PREFIX_PATTERN_V2,
    "affirmative_idiom_prefix_pattern": AFFIRMATIVE_IDIOM_PREFIX_PATTERN_V2,
    "affirmative_idiom_anywhere_pattern": (
        AFFIRMATIVE_IDIOM_ANYWHERE_PATTERN_V2
    ),
    "affirmative_negator_mask_pattern": AFFIRMATIVE_NEGATOR_MASK_PATTERN_V2,
    "generic_negator_pattern": GENERIC_NEGATOR_PATTERN_V2,
    "unresolved_negation_pattern": UNRESOLVED_NEGATION_PATTERN_V2,
    "inline_camera_negator_pattern": INLINE_CAMERA_NEGATOR_PATTERN_V2,
    "negated_purpose_switch_pattern": NEGATED_PURPOSE_SWITCH_PATTERN_V2,
    "negated_direct_switch_pattern": NEGATED_DIRECT_SWITCH_PATTERN_V2,
    "unresolved_purpose_prefix_pattern": (
        UNRESOLVED_PURPOSE_PREFIX_PATTERN_V2
    ),
    "trailing_negation_pattern": TRAILING_NEGATION_PATTERN_V2,
    "controlled_replacement_link_pattern": (
        CONTROLLED_REPLACEMENT_LINK_PATTERN_V2
    ),
    "decision_rule_order": [
        "POLARITY-UNCLOSED-QUOTE-001",
        "POLARITY-QUOTED-EXTERNAL-NEGATION-001",
        "POLARITY-QUOTED-001",
        "POLARITY-CONTEXT-PURPOSE-001",
        "POLARITY-NEGATED-PURPOSE-SWITCH-001",
        "POLARITY-NEGATED-DIRECT-SWITCH-001",
        "POLARITY-UNRESOLVED-PURPOSE-001",
        "POLARITY-UNRESOLVED-RESET-SCOPE-001",
        "POLARITY-AFFIRMATIVE-IDIOM-001",
        "POLARITY-UNRESOLVED-OPERATOR-OVERLAP-001",
        "POLARITY-DIRECT-NEGATION-001",
        "POLARITY-UNRESOLVED-NEGATION-001",
        "POLARITY-TRAILING-NEGATION-001",
        "POLARITY-UNMATCHED-NEGATION-GUARD-001",
        "POLARITY-DEFAULT-ASSERTION-001",
    ],
    "blocking_issue_codes": [
        "SOURCE_FACT_POLARITY_UNRESOLVED",
        "SOURCE_FACT_NEGATION_UNREPRESENTABLE",
        "SOURCE_FACT_POLARITY_CONFLICT",
    ],
    "polarity_anchor_source": "lexical_rules[].polarity_anchor_pattern",
    "purpose_construction_semantics": {
        "facts_inside_context_group": "CONTEXT_ONLY",
        "first_fact_after_switch": "NEGATED",
        "malformed_or_nested_scope": "UNRESOLVED",
    },
    "assertion_reset_semantics": {
        "applies_after_latest_soft_or_hard_clause_boundary": True,
        "earlier_negation_requires_unquoted_fact_before_reset": True,
        "otherwise": "UNRESOLVED",
    },
    "controlled_replacement_semantics": {
        "direction": "NEGATED_THEN_ASSERTED",
        "same_field_required": True,
        "different_value_required": True,
        "link_must_fullmatch_pattern": True,
        "unlinked_negation": "BLOCK",
    },
    "match_decision_fields": [
        "decision_id",
        "lexical_rule_id",
        "field",
        "value",
        "source_span",
        "anchor_span",
        "polarity",
        "polarity_rule_ids",
        "operator_spans",
        "eligible_for_fact",
    ],
    "match_decision_sort_key": [
        "source_span.start",
        "source_span.end",
        "field",
        "value",
        "lexical_rule_id",
    ],
    "decision_id_format": "POLARITY-DECISION-%03d",
    "unmatched_negation_guard_rule_ids": list(
        UNMATCHED_NEGATION_GUARD_RULE_IDS_V2
    ),
    "unmatched_negation_guard_behavior": "UNRESOLVED_AND_BLOCK",
    "quote_semantics": {
        "balanced_without_external_negation": "IGNORED_QUOTED",
        "balanced_with_external_direct_negation": "NEGATED",
        "balanced_with_external_unresolved_negation": "UNRESOLVED",
        "unclosed_quote": "UNRESOLVED",
    },
    "maximum_purpose_code_points": 24,
    "replacement_link_maximum_soft_boundaries": 1,
    "operator_overlap_behavior": "BLOCK",
    "unsupported_negation_behavior": "BLOCK",
    "negative_without_asserted_replacement": "BLOCK",
    "last_mention_wins": False,
    "automatic_repair": False,
    "held_out_observation_input": False,
}
QUOTE_PAIRS: Final[tuple[tuple[str, str], ...]] = (
    ("“", "”"),
    ("「", "」"),
    ("『", "』"),
    ('"', '"'),
    ("'", "'"),
)
REQUEST_PASSTHROUGH_RULE: Final[dict[str, Any]] = {
    "rule_id": "REQUEST-SOURCE-TEXT-PASSTHROUGH-001",
    "field": "shot_core.action_description",
    "value_source": "request.source_text",
    "provenance": "REQUEST_PASSTHROUGH",
    "source_span": "FULL_SOURCE_TEXT",
}

LEXICAL_RULES_V1: Final[tuple[dict[str, Any], ...]] = (
    {
        "rule_id": "LOCATION-OUTDOOR-001",
        "kind": "REGEX",
        "pattern": (
            r"室外(?=[，,。；;！？!?]|街灯|街道|场景|环境|"
            r"或(?=室内)|$)"
        ),
        "field": "scene_context.location",
        "value": "OUTDOOR_LOCATION",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "LOCATION-INDOOR-001",
        "kind": "REGEX",
        "pattern": (
            r"室内(?=[，,。；;！？!?]|柔光|灯光|场景|环境|"
            r"或(?=室外)|$)"
        ),
        "field": "scene_context.location",
        "value": "INDOOR_LOCATION",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "TIME-DAY-001",
        "kind": "REGEX",
        "pattern": r"白天(?=室内|室外|[，,。；;！？!?]|或(?=夜晚|夜间)|$)",
        "field": "scene_context.time",
        "value": "DAY",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "TIME-NIGHT-001",
        "kind": "REGEX",
        "pattern": (
            r"(?:夜晚|夜间)(?=室内|室外|[，,。；;！？!?]|"
            r"或(?=白天)|$)"
        ),
        "field": "scene_context.time",
        "value": "NIGHT",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "FRAMING-CLOSE-UP-001",
        "kind": "REGEX",
        "pattern": r"特写(?=镜头|画面|[，,。；;！？!?]|或(?=中景|全景)|$)",
        "field": "shot_core.framing",
        "value": "CLOSE_UP",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "FRAMING-MEDIUM-001",
        "kind": "REGEX",
        "pattern": r"中景(?=镜头|画面|[，,。；;！？!?]|或(?=特写|全景)|$)",
        "field": "shot_core.framing",
        "value": "MEDIUM",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "FRAMING-WIDE-001",
        "kind": "REGEX",
        "pattern": r"全景(?=镜头|画面|[，,。；;！？!?]|或(?=特写|中景)|$)",
        "field": "shot_core.framing",
        "value": "WIDE",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "CAMERA-STATIC-001",
        "kind": "REGEX",
        "pattern": "固定相机|相机保持静止|镜头保持静止",
        "field": "shot_core.camera_movement",
        "value": "STATIC",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "CAMERA-PAN-RIGHT-MOVEMENT-001",
        "kind": "REGEX",
        "pattern": r"(?:相机向右摇摄|镜头向右摇摄)",
        "field": "shot_core.camera_movement",
        "value": "PAN",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "CAMERA-PAN-RIGHT-DIRECTION-001",
        "kind": "REGEX",
        "pattern": r"(?:相机向右摇摄|镜头向右摇摄)",
        "field": "shot_core.camera_direction",
        "value": "RIGHT",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "CAMERA-PAN-LEFT-MOVEMENT-001",
        "kind": "REGEX",
        "pattern": r"(?:相机向左摇摄|镜头向左摇摄)",
        "field": "shot_core.camera_movement",
        "value": "PAN",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "CAMERA-PAN-LEFT-DIRECTION-001",
        "kind": "REGEX",
        "pattern": r"(?:相机向左摇摄|镜头向左摇摄)",
        "field": "shot_core.camera_direction",
        "value": "LEFT",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "ORIENTATION-FACING-CAMERA-001",
        "kind": "REGEX",
        "pattern": r"面向相机",
        "field": "performance.orientation_state",
        "value": "FACING_CAMERA",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "SUBJECT-MOVING-LEFT-TO-RIGHT-001",
        "kind": "REGEX",
        "pattern": (
            r"(?:自行车|演员|人物|主体|小孩|行人)"
            r"[^，,。；;！？!?]{0,8}从左向右(?:穿过|移动|行驶|走|跑)"
        ),
        "field": "performance.orientation_state",
        "value": "MOVING_LEFT_TO_RIGHT",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "ACTION-CRYING-001",
        "kind": "REGEX",
        "pattern": r"哭泣(?=[，,。；;！？!?]|$)",
        "field": "performance.visible_action_state",
        "value": "CRYING",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "ACTION-SMILING-001",
        "kind": "REGEX",
        "pattern": r"微笑(?=[，,。；;！？!?]|$)",
        "field": "performance.visible_action_state",
        "value": "SMILING",
        "provenance": "NORMALIZED_LEXICAL",
    },
    {
        "rule_id": "INTENSITY-GENTLE-001",
        "kind": "REGEX",
        "pattern": r"轻轻微笑(?=[，,。；;！？!?]|$)",
        "field": "performance.performance_intensity",
        "value": "GENTLE",
        "provenance": "NORMALIZED_LEXICAL",
    },
)


def _build_v2_lexical_rules() -> tuple[dict[str, Any], ...]:
    """在保留第一版历史合同的前提下，收紧易越过语义边界的规则。"""

    rules = deepcopy(LEXICAL_RULES_V1)
    reset = FACT_TERM_RIGHT_BOUNDARY_PATTERN_V2
    camera_negator = INLINE_CAMERA_NEGATOR_PATTERN_V2
    replacements = {
        "LOCATION-OUTDOOR-001": (
            rf"室外(?=[，,。；;！？!?]|街灯|街道|场景|环境|"
            rf"或(?=室内)|{reset}|$)"
        ),
        "LOCATION-INDOOR-001": (
            rf"室内(?=[，,。；;！？!?]|柔光|灯光|场景|环境|"
            rf"或(?=室外)|{reset}|$)"
        ),
        "TIME-DAY-001": (
            rf"白天(?=室内|室外|[，,。；;！？!?]|"
            rf"或(?=夜晚|夜间)|{reset}|$)"
        ),
        "TIME-NIGHT-001": (
            rf"(?:夜晚|夜间)(?=室内|室外|[，,。；;！？!?]|"
            rf"或(?=白天)|{reset}|$)"
        ),
        "FRAMING-CLOSE-UP-001": (
            rf"特写(?=镜头|画面|[，,。；;！？!?]|"
            rf"或(?=中景|全景)|{reset}|$)"
        ),
        "FRAMING-MEDIUM-001": (
            rf"中景(?=镜头|画面|[，,。；;！？!?]|"
            rf"或(?=特写|全景)|{reset}|$)"
        ),
        "FRAMING-WIDE-001": (
            rf"全景(?=镜头|画面|[，,。；;！？!?]|"
            rf"或(?=特写|中景)|{reset}|$)"
        ),
        "CAMERA-STATIC-001": (
            r"(?:固定相机(?=拍摄|取景|机位|[，,。；;！？!?]|$)|"
            rf"(?:相机|镜头|摄像机|摄影机)(?:{camera_negator})?"
            r"\s*保持静止)"
        ),
        "CAMERA-PAN-RIGHT-MOVEMENT-001": (
            rf"(?:相机|镜头|摄像机|摄影机)(?:{camera_negator})?\s*向右摇摄"
        ),
        "CAMERA-PAN-RIGHT-DIRECTION-001": (
            rf"(?:相机|镜头|摄像机|摄影机)(?:{camera_negator})?\s*向右摇摄"
        ),
        "CAMERA-PAN-LEFT-MOVEMENT-001": (
            rf"(?:相机|镜头|摄像机|摄影机)(?:{camera_negator})?\s*向左摇摄"
        ),
        "CAMERA-PAN-LEFT-DIRECTION-001": (
            rf"(?:相机|镜头|摄像机|摄影机)(?:{camera_negator})?\s*向左摇摄"
        ),
        "ORIENTATION-FACING-CAMERA-001": (
            r"面向(?:相机|镜头|摄像机|摄影机)"
        ),
        "SUBJECT-MOVING-LEFT-TO-RIGHT-001": (
            r"(?:自行车|演员|人物|主体|小孩|行人)"
            r"(?:(?!(?:相机|镜头|摄像机|摄影机|机位))"
            r"[^，,。；;！？!?]){0,8}"
            r"从左向右(?:穿过|移动|行驶|走|跑)"
        ),
        "ACTION-CRYING-001": (
            rf"哭泣(?=[”」』\"'][，,。；;！？!?]?|[，,。；;！？!?]|{reset}|$)"
        ),
        "ACTION-SMILING-001": (
            rf"微笑(?=[”」』\"'][，,。；;！？!?]?|[，,。；;！？!?]|{reset}|$)"
        ),
        "INTENSITY-GENTLE-001": (
            rf"轻轻微笑(?=[”」』\"'][，,。；;！？!?]?|[，,。；;！？!?]|{reset}|$)"
        ),
    }
    polarity_anchors = {
        "LOCATION-OUTDOOR-001": r"室外",
        "LOCATION-INDOOR-001": r"室内",
        "TIME-DAY-001": r"白天",
        "TIME-NIGHT-001": r"(?:夜晚|夜间)",
        "FRAMING-CLOSE-UP-001": r"特写",
        "FRAMING-MEDIUM-001": r"中景",
        "FRAMING-WIDE-001": r"全景",
        "CAMERA-STATIC-001": r"(?:固定相机|保持静止)",
        "CAMERA-PAN-RIGHT-MOVEMENT-001": r"向右摇摄",
        "CAMERA-PAN-RIGHT-DIRECTION-001": r"向右摇摄",
        "CAMERA-PAN-LEFT-MOVEMENT-001": r"向左摇摄",
        "CAMERA-PAN-LEFT-DIRECTION-001": r"向左摇摄",
        "ORIENTATION-FACING-CAMERA-001": (
            r"面向(?:相机|镜头|摄像机|摄影机)"
        ),
        "SUBJECT-MOVING-LEFT-TO-RIGHT-001": (
            r"从左向右(?:穿过|移动|行驶|走|跑)"
        ),
        "ACTION-CRYING-001": r"哭泣",
        "ACTION-SMILING-001": r"微笑",
        "INTENSITY-GENTLE-001": r"轻轻微笑",
    }
    for rule in rules:
        replacement = replacements.get(rule["rule_id"])
        if replacement is not None:
            rule["pattern"] = replacement
        rule["polarity_anchor_pattern"] = polarity_anchors[rule["rule_id"]]
    return tuple(rules)


LEXICAL_RULES_V2: Final[tuple[dict[str, Any], ...]] = _build_v2_lexical_rules()
LEXICAL_RULES: Final[tuple[dict[str, Any], ...]] = LEXICAL_RULES_V1

DERIVATION_RULES: Final[tuple[dict[str, Any], ...]] = (
    {
        "rule_id": "STATIC-CAMERA-DIRECTION-NONE-001",
        "depends_on": {
            "field": "shot_core.camera_movement",
            "value": "STATIC",
        },
        "field": "shot_core.camera_direction",
        "value": "NONE",
    },
    {
        "rule_id": "STATIC-CAMERA-SPEED-NONE-001",
        "depends_on": {
            "field": "shot_core.camera_movement",
            "value": "STATIC",
        },
        "field": "shot_core.camera_speed",
        "value": "NONE",
    },
    {
        "rule_id": "CRYING-CLASS-EXPRESS-001",
        "depends_on": {
            "field": "performance.visible_action_state",
            "value": "CRYING",
        },
        "field": "shot_core.action_class",
        "value": "EXPRESS",
    },
    {
        "rule_id": "SMILING-CLASS-EXPRESS-001",
        "depends_on": {
            "field": "performance.visible_action_state",
            "value": "SMILING",
        },
        "field": "shot_core.action_class",
        "value": "EXPRESS",
    },
    {
        "rule_id": "LEFT-TO-RIGHT-CLASS-MOVE-001",
        "depends_on": {
            "field": "performance.orientation_state",
            "value": "MOVING_LEFT_TO_RIGHT",
        },
        "field": "shot_core.action_class",
        "value": "MOVE",
    },
)


class SourceFactExtractionError(ValueError):
    """原句事实无法安全进入混合规划。"""


def _sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _extractor_configuration(
    contract_version: str,
) -> tuple[tuple[dict[str, Any], ...], tuple[str, ...], str]:
    if contract_version == SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V1:
        return (
            LEXICAL_RULES_V1,
            NEGATION_MARKERS_V1,
            SOURCE_FACT_EXTRACTION_VERSION_V1,
        )
    if contract_version == SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2:
        return (
            LEXICAL_RULES_V2,
            NEGATION_MARKERS_V2,
            SOURCE_FACT_EXTRACTION_VERSION_V2,
        )
    raise SourceFactExtractionError("原句事实提取合同版本不受支持。")


def source_fact_extractor_contract(
    contract_version: str = SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION,
) -> dict[str, Any]:
    lexical_rules, negation_markers, _extraction_version = (
        _extractor_configuration(contract_version)
    )
    contract = {
        "schema_version": contract_version,
        "supported_request_schema_versions": [REQUEST_SCHEMA_VERSION_V2],
        "supported_language": "zh-Hans",
        "source_offset_unit": "UNICODE_CODE_POINT",
        "source_span_interval": "ZERO_BASED_HALF_OPEN",
        "request_passthrough_rules": [deepcopy(REQUEST_PASSTHROUGH_RULE)],
        "lexical_rules": deepcopy(list(lexical_rules)),
        "derivation_rules": deepcopy(list(DERIVATION_RULES)),
        "matching_policy": {
            "regex_engine": "python.re",
            "unicode_normalization": "NONE",
            "case_sensitive": True,
            "overlapping_matches": False,
            "clause_boundary_pattern": CLAUSE_BOUNDARY_PATTERN,
            "negation_scope": "CLAUSE_START_THROUGH_MATCH_END_CONSERVATIVE",
            "negation_markers": list(negation_markers),
            "quoted_match_behavior": "IGNORE_MATCH_INSIDE_BALANCED_QUOTES",
            "quote_pairs": [list(pair) for pair in QUOTE_PAIRS],
            "compound_word_boundaries": "RULE_SPECIFIC_POSITIVE_CONTEXT",
        },
        "candidate_resolution_order": [
            "MATCH_REQUEST_PASSTHROUGH_AND_LEXICAL_RULES",
            "FAIL_ON_MULTIPLE_DISTINCT_VALUES_PER_FIELD",
            "VALIDATE_BASE_FACT_AGAINST_REQUEST_ALLOWED_VALUES",
            "DERIVE_ONLY_FROM_VALIDATED_BASE_FACTS",
            "RESOLVE_AND_VALIDATE_COMBINED_FACTS",
            "ASSIGN_SORTED_FACT_IDENTIFIERS",
        ],
        "allowed_value_validation": "BEFORE_DERIVATION_AND_AFTER_COMBINATION",
        "derivation_dependency_requirement": "SELECTED_VALID_BASE_FACT",
        "provenance_types": [
            "EXACT_LEXICAL",
            "NORMALIZED_LEXICAL",
            "DETERMINISTIC_DERIVATION",
            "REQUEST_PASSTHROUGH",
        ],
        "conflict_behavior": "BLOCK_WITHOUT_WINNER",
        "ambiguous_behavior": "BLOCK_WITHOUT_WINNER",
        "unstated_behavior": "MODEL_PROPOSABLE_NON_AUTHORITATIVE",
        "lossy_enum_mapping": "PROHIBITED",
        "held_out_observation_input": False,
        "automatic_repair": False,
        "creative_fact_defaulting": False,
        "formal_decision_created": False,
    }
    if contract_version == SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2:
        contract["matching_policy"].update(
            {
                "negation_scope": "CONTROLLED_POLARITY_PER_LEXICAL_MATCH",
                "quoted_match_behavior": (
                    "RECORD_IGNORED_WHEN_POLARITY_ANCHOR_INSIDE_BALANCED_QUOTES"
                ),
                "polarity_policy": deepcopy(POLARITY_POLICY_V2),
                "subject_motion_camera_terms_excluded": list(CAMERA_TERMS_V2),
            }
        )
        contract["candidate_resolution_order"] = [
            "MATCH_REQUEST_PASSTHROUGH_AND_ALL_LEXICAL_RULES",
            "CLASSIFY_EACH_LEXICAL_MATCH_POLARITY",
            "RUN_UNMATCHED_NEGATION_GUARDS",
            "SORT_AND_ASSIGN_POLARITY_DECISION_IDENTIFIERS",
            "BLOCK_UNRESOLVED_OR_UNREPRESENTABLE_NEGATION",
            "SELECT_ONLY_ASSERTED_LEXICAL_MATCHES",
            "FAIL_ON_MULTIPLE_DISTINCT_VALUES_PER_FIELD",
            "VALIDATE_BASE_FACT_AGAINST_REQUEST_ALLOWED_VALUES",
            "DERIVE_ONLY_FROM_VALIDATED_BASE_FACTS",
            "RESOLVE_AND_VALIDATE_COMBINED_FACTS",
            "ASSIGN_SORTED_FACT_IDENTIFIERS",
        ]
    return contract


def source_fact_extractor_contract_sha256(
    contract_version: str = SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION,
) -> str:
    return _sha256(source_fact_extractor_contract(contract_version))


def hybrid_merge_contract() -> dict[str, Any]:
    return {
        "schema_version": HYBRID_MERGE_CONTRACT_VERSION,
        "stage_order": list(HYBRID_STAGE_ORDER),
        "stage_required_keys": {
            stage: sorted(fields)
            for stage, fields in HYBRID_STAGE_REQUIRED_KEYS.items()
        },
        "locked_field_precedence": "SYSTEM_SOURCE_FACT_ONLY",
        "model_locked_field_write_behavior": "BLOCK",
        "missing_residual_field_behavior": "BLOCK",
        "extra_residual_field_behavior": "BLOCK",
        "merge_is_deterministic": True,
        "automatic_repair": False,
        "formal_decision_created": False,
    }


def hybrid_merge_contract_sha256() -> str:
    return _sha256(hybrid_merge_contract())


def _allowed_values_by_path(request: dict[str, Any]) -> dict[str, tuple[str, ...]]:
    constraints = request["semantic_constraints"]
    values: dict[str, tuple[str, ...]] = {}
    for field, allowed in request["controlled_context_token_values"][
        "scene_context"
    ].items():
        values[f"scene_context.{field}"] = tuple(allowed)
    values["beat_purpose.purpose"] = tuple(
        constraints["allowed_primary_purposes"]
    )
    values.update(
        {
            "shot_core.primary_purpose": tuple(
                constraints["allowed_primary_purposes"]
            ),
            "shot_core.framing": tuple(constraints["allowed_framings"]),
            "shot_core.action_class": tuple(
                constraints["allowed_action_classes"]
            ),
            "shot_core.camera_movement": tuple(
                constraints["allowed_camera_movements"]
            ),
            "shot_core.camera_direction": tuple(
                constraints["allowed_camera_directions"]
            ),
            "shot_core.camera_speed": tuple(
                constraints["allowed_camera_speeds"]
            ),
        }
    )
    for stage, stage_fields in request[
        "controlled_stage_allowed_values"
    ].items():
        for field, allowed in stage_fields.items():
            values[f"{stage}.{field}"] = tuple(allowed)
    return values


def _span(text: str, start: int, end: int) -> dict[str, Any]:
    return {"start": start, "end": end, "quote": text[start:end]}


def _inside_balanced_quotes(text: str, start: int) -> bool:
    for opening, closing in QUOTE_PAIRS:
        prefix = text[:start]
        if opening == closing:
            if prefix.count(opening) % 2:
                return True
            continue
        if prefix.rfind(opening) > prefix.rfind(closing):
            return True
    return False


def _v2_quote_context(
    text: str,
    start: int,
) -> tuple[str, int, int] | None:
    """返回锚点所在引号的状态与范围；不复用第一版的历史启发式。"""

    for opening, closing in QUOTE_PAIRS:
        prefix = text[:start]
        if opening == closing:
            if prefix.count(opening) % 2 == 0:
                continue
            opening_start = prefix.rfind(opening)
            closing_start = text.find(closing, start)
        else:
            opening_start = prefix.rfind(opening)
            if opening_start <= prefix.rfind(closing):
                continue
            closing_start = text.find(closing, start)
        if closing_start < 0:
            return "UNCLOSED", opening_start, len(text)
        return "BALANCED", opening_start, closing_start + len(closing)
    return None


def _first_unmasked_negator(
    text: str,
    start: int,
    end: int,
) -> dict[str, Any] | None:
    fragment = text[start:end]
    masked = [False] * len(fragment)
    for match in re.finditer(AFFIRMATIVE_NEGATOR_MASK_PATTERN_V2, fragment):
        for index in range(match.start(), match.end()):
            masked[index] = True
    candidates = [
        *re.finditer(UNRESOLVED_NEGATION_PATTERN_V2, fragment),
        *re.finditer(GENERIC_NEGATOR_PATTERN_V2, fragment),
    ]
    candidates.sort(key=lambda item: (item.start(), -(item.end() - item.start())))
    for match in candidates:
        if any(masked[match.start() : match.end()]):
            continue
        return _span(text, start + match.start(), start + match.end())
    return None


def _negated(
    text: str,
    start: int,
    end: int,
    negation_markers: tuple[str, ...],
) -> bool:
    boundaries = list(re.finditer(CLAUSE_BOUNDARY_PATTERN, text[:start]))
    clause_start = boundaries[-1].end() if boundaries else 0
    evidence_scope = text[clause_start:end]
    return any(marker in evidence_scope for marker in negation_markers)


def _rule_matches(
    text: str,
    rule: dict[str, Any],
    negation_markers: tuple[str, ...],
) -> list[dict[str, Any]]:
    pattern = (
        re.escape(rule["phrase"])
        if rule["kind"] == "EXACT"
        else rule["pattern"]
    )
    return [
        _span(text, match.start(), match.end())
        for match in re.finditer(pattern, text)
        if not _inside_balanced_quotes(text, match.start())
        and not _negated(
            text,
            match.start(),
            match.end(),
            negation_markers,
        )
    ]


def _operator_span(text: str, match: re.Match[str]) -> dict[str, Any]:
    return _span(text, match.start(), match.end())


def _last_clause_start(text: str, start: int) -> int:
    boundaries = list(re.finditer(CLAUSE_BOUNDARY_PATTERN, text[:start]))
    return boundaries[-1].end() if boundaries else 0


def _latest_assertion_reset(prefix: str) -> re.Match[str] | None:
    token_pattern = "|".join(
        re.escape(token)
        for token in sorted(ASSERTION_RESET_TOKENS_V2, key=len, reverse=True)
    )
    matches = list(re.finditer(token_pattern, prefix))
    return matches[-1] if matches else None


def _contains_unquoted_v2_fact_anchor(text: str, start: int, end: int) -> bool:
    for rule in LEXICAL_RULES_V2:
        for match in re.finditer(rule["polarity_anchor_pattern"], text[start:end]):
            absolute_start = start + match.start()
            if _v2_quote_context(text, absolute_start) is None:
                return True
    return False


def _matching_construction(
    pattern: str,
    text: str,
    anchor_start: int,
) -> tuple[re.Match[str] | None, str | None]:
    for match in re.finditer(pattern, text):
        if "context" in match.groupdict():
            if match.start("context") <= anchor_start < match.end("context"):
                return match, "CONTEXT_ONLY"
        if match.end() <= anchor_start and not text[match.end() : anchor_start].strip():
            return match, "NEGATED"
    return None, None


def _v2_polarity_decision(
    text: str,
    rule: dict[str, Any],
    match: re.Match[str],
) -> dict[str, Any]:
    source_span = _span(text, match.start(), match.end())
    anchor_match = re.search(rule["polarity_anchor_pattern"], match.group(0))
    if anchor_match is None:
        raise SourceFactExtractionError("第二版词法规则缺少可重建的极性锚点。")
    anchor_start = match.start() + anchor_match.start()
    anchor_end = match.start() + anchor_match.end()
    anchor_span = _span(text, anchor_start, anchor_end)

    def decision(
        polarity: str,
        rule_ids: list[str],
        operator_spans: list[dict[str, Any]],
    ) -> dict[str, Any]:
        return {
            "lexical_rule_id": rule["rule_id"],
            "field": rule["field"],
            "value": rule["value"],
            "source_span": source_span,
            "anchor_span": anchor_span,
            "polarity": polarity,
            "polarity_rule_ids": rule_ids,
            "operator_spans": sorted(
                {
                    (span["start"], span["end"], span["quote"])
                    for span in operator_spans
                }
            ),
            "eligible_for_fact": polarity == "ASSERTED",
        }

    quote_context = _v2_quote_context(text, anchor_start)
    if quote_context is not None:
        quote_state, quote_start, quote_end = quote_context
        quote_span = _span(text, quote_start, quote_end)
        if quote_state == "UNCLOSED":
            return decision(
                "UNRESOLVED",
                ["POLARITY-UNCLOSED-QUOTE-001"],
                [quote_span],
            )
        quote_clause_start = _last_clause_start(text, quote_start)
        external_negator = _first_unmasked_negator(
            text,
            quote_clause_start,
            quote_start,
        )
        if external_negator is not None:
            external_prefix = text[quote_clause_start:quote_start]
            direct_external = re.search(
                DIRECT_NEGATIVE_PREFIX_PATTERN_V2,
                external_prefix,
            )
            return decision(
                "NEGATED" if direct_external is not None else "UNRESOLVED",
                ["POLARITY-QUOTED-EXTERNAL-NEGATION-001"],
                [external_negator, quote_span],
            )
        return decision(
            "IGNORED_QUOTED",
            ["POLARITY-QUOTED-001"],
            [quote_span],
        )

    purpose, purpose_state = _matching_construction(
        NEGATED_PURPOSE_SWITCH_PATTERN_V2,
        text,
        anchor_start,
    )
    if purpose is not None and purpose_state is not None:
        rule_id = (
            "POLARITY-CONTEXT-PURPOSE-001"
            if purpose_state == "CONTEXT_ONLY"
            else "POLARITY-NEGATED-PURPOSE-SWITCH-001"
        )
        return decision(purpose_state, [rule_id], [_operator_span(text, purpose)])

    direct_switch, direct_switch_state = _matching_construction(
        NEGATED_DIRECT_SWITCH_PATTERN_V2,
        text,
        anchor_start,
    )
    if direct_switch is not None and direct_switch_state == "NEGATED":
        return decision(
            "NEGATED",
            ["POLARITY-NEGATED-DIRECT-SWITCH-001"],
            [_operator_span(text, direct_switch)],
        )

    boundary = re.search(CLAUSE_BOUNDARY_PATTERN, text[anchor_end:])
    clause_end = (
        anchor_end + boundary.start() if boundary is not None else len(text)
    )
    suffix = text[anchor_end:clause_end]
    trailing = re.fullmatch(TRAILING_NEGATION_PATTERN_V2, suffix)
    if trailing is not None:
        return decision(
            "NEGATED",
            ["POLARITY-TRAILING-NEGATION-001"],
            [_span(text, anchor_end, clause_end)],
        )
    trailing_unresolved = _first_unmasked_negator(text, anchor_end, clause_end)
    if trailing_unresolved is not None:
        return decision(
            "UNRESOLVED",
            ["POLARITY-UNRESOLVED-NEGATION-001"],
            [trailing_unresolved],
        )

    clause_start = _last_clause_start(text, anchor_start)
    prefix = text[clause_start:anchor_start]
    unresolved_purpose = re.search(UNRESOLVED_PURPOSE_PREFIX_PATTERN_V2, prefix)
    if unresolved_purpose is not None:
        return decision(
            "UNRESOLVED",
            ["POLARITY-UNRESOLVED-PURPOSE-001"],
            [
                _span(
                    text,
                    clause_start + unresolved_purpose.start(),
                    clause_start + unresolved_purpose.end(),
                )
            ],
        )

    reset = _latest_assertion_reset(prefix)
    reset_span: dict[str, Any] | None = None
    effective_start = clause_start
    if reset is not None:
        reset_start = clause_start + reset.start()
        reset_end = clause_start + reset.end()
        reset_span = _span(text, reset_start, reset_end)
        earlier_negation = _first_unmasked_negator(
            text,
            clause_start,
            reset_start,
        )
        if earlier_negation is not None and not _contains_unquoted_v2_fact_anchor(
            text,
            earlier_negation["end"],
            reset_start,
        ):
            return decision(
                "UNRESOLVED",
                ["POLARITY-UNRESOLVED-RESET-SCOPE-001"],
                [
                    earlier_negation,
                    reset_span,
                ],
            )
        effective_start = reset_end

    effective_prefix = text[effective_start:anchor_start]
    affirmative = re.search(AFFIRMATIVE_IDIOM_PREFIX_PATTERN_V2, effective_prefix)
    if affirmative is not None:
        preceding = effective_prefix[: affirmative.start()]
        conflicting = _first_unmasked_negator(
            text,
            effective_start,
            effective_start + len(preceding),
        )
        if conflicting is not None:
            return decision(
                "UNRESOLVED",
                ["POLARITY-UNRESOLVED-OPERATOR-OVERLAP-001"],
                [
                    conflicting,
                    _span(
                        text,
                        effective_start + affirmative.start(),
                        effective_start + affirmative.end(),
                    ),
                ],
            )
        spans = [
            _span(
                text,
                effective_start + affirmative.start(),
                effective_start + affirmative.end(),
            )
        ]
        if reset_span is not None:
            spans.append(reset_span)
        return decision(
            "ASSERTED",
            ["POLARITY-AFFIRMATIVE-IDIOM-001"],
            spans,
        )

    direct_negative = re.search(DIRECT_NEGATIVE_PREFIX_PATTERN_V2, effective_prefix)
    if direct_negative is not None:
        earlier_idiom = re.search(
            AFFIRMATIVE_IDIOM_ANYWHERE_PATTERN_V2,
            effective_prefix[: direct_negative.start()],
        )
        earlier_negation = _first_unmasked_negator(
            text,
            effective_start,
            effective_start + direct_negative.start(),
        )
        if earlier_idiom is not None or earlier_negation is not None:
            earlier_operator_span = (
                _span(
                    text,
                    effective_start + earlier_idiom.start(),
                    effective_start + earlier_idiom.end(),
                )
                if earlier_idiom is not None
                else earlier_negation
            )
            assert earlier_operator_span is not None
            return decision(
                "UNRESOLVED",
                ["POLARITY-UNRESOLVED-OPERATOR-OVERLAP-001"],
                [
                    earlier_operator_span,
                    _span(
                        text,
                        effective_start + direct_negative.start(),
                        effective_start + direct_negative.end(),
                    ),
                ],
            )
        return decision(
            "NEGATED",
            ["POLARITY-DIRECT-NEGATION-001"],
            [
                _span(
                    text,
                    effective_start + direct_negative.start(),
                    effective_start + direct_negative.end(),
                )
            ],
        )

    unresolved = _first_unmasked_negator(
        text,
        effective_start,
        anchor_start,
    )
    if unresolved is not None:
        return decision(
            "UNRESOLVED",
            ["POLARITY-UNRESOLVED-NEGATION-001"],
            [
                unresolved
            ],
        )

    spans = [reset_span] if reset_span is not None else []
    return decision("ASSERTED", ["POLARITY-DEFAULT-ASSERTION-001"], spans)


def _v2_rule_decisions(
    text: str,
    lexical_rules: tuple[dict[str, Any], ...],
) -> list[dict[str, Any]]:
    decisions: list[dict[str, Any]] = []
    for rule in lexical_rules:
        pattern = (
            re.escape(rule["phrase"])
            if rule["kind"] == "EXACT"
            else rule["pattern"]
        )
        decisions.extend(
            _v2_polarity_decision(text, rule, match)
            for match in re.finditer(pattern, text)
        )
    covered = {
        (
            item["lexical_rule_id"],
            item["anchor_span"]["start"],
            item["anchor_span"]["end"],
        )
        for item in decisions
    }
    guarded_rule_ids = set(UNMATCHED_NEGATION_GUARD_RULE_IDS_V2)
    for rule in lexical_rules:
        if rule["rule_id"] not in guarded_rule_ids:
            continue
        for anchor in re.finditer(rule["polarity_anchor_pattern"], text):
            key = (rule["rule_id"], anchor.start(), anchor.end())
            if key in covered:
                continue
            anchor_span = _span(text, anchor.start(), anchor.end())
            quote_context = _v2_quote_context(text, anchor.start())
            polarity: str | None = None
            rule_id = "POLARITY-UNMATCHED-NEGATION-GUARD-001"
            operator_spans: list[dict[str, Any]] = []
            if quote_context is not None:
                quote_state, quote_start, quote_end = quote_context
                quote_span = _span(text, quote_start, quote_end)
                if quote_state == "UNCLOSED":
                    polarity = "UNRESOLVED"
                    rule_id = "POLARITY-UNCLOSED-QUOTE-001"
                    operator_spans = [quote_span]
                else:
                    clause_start = _last_clause_start(text, quote_start)
                    external = _first_unmasked_negator(
                        text,
                        clause_start,
                        quote_start,
                    )
                    if external is not None:
                        polarity = "UNRESOLVED"
                        rule_id = "POLARITY-QUOTED-EXTERNAL-NEGATION-001"
                        operator_spans = [external, quote_span]
                    else:
                        polarity = "IGNORED_QUOTED"
                        rule_id = "POLARITY-QUOTED-001"
                        operator_spans = [quote_span]
            else:
                clause_start = _last_clause_start(text, anchor.start())
                boundary = re.search(CLAUSE_BOUNDARY_PATTERN, text[anchor.end() :])
                clause_end = (
                    anchor.end() + boundary.start()
                    if boundary is not None
                    else len(text)
                )
                before = _first_unmasked_negator(
                    text,
                    clause_start,
                    anchor.start(),
                )
                after = _first_unmasked_negator(
                    text,
                    anchor.end(),
                    clause_end,
                )
                if before is not None or after is not None:
                    polarity = "UNRESOLVED"
                    operator_spans = [
                        item for item in (before, after) if item is not None
                    ]
            if polarity is None:
                continue
            decisions.append(
                {
                    "lexical_rule_id": rule["rule_id"],
                    "field": rule["field"],
                    "value": rule["value"],
                    "source_span": anchor_span,
                    "anchor_span": anchor_span,
                    "polarity": polarity,
                    "polarity_rule_ids": [rule_id],
                    "operator_spans": sorted(
                        {
                            (span["start"], span["end"], span["quote"])
                            for span in operator_spans
                        }
                    ),
                    "eligible_for_fact": False,
                }
            )
    decisions.sort(
        key=lambda item: (
            item["source_span"]["start"],
            item["source_span"]["end"],
            item["field"],
            item["value"],
            item["lexical_rule_id"],
        )
    )
    for index, item in enumerate(decisions, start=1):
        item["decision_id"] = f"POLARITY-DECISION-{index:03d}"
        item["operator_spans"] = [
            {"start": start, "end": end, "quote": quote}
            for start, end, quote in item["operator_spans"]
        ]
    return decisions


def _controlled_replacement_link(
    text: str,
    negated: dict[str, Any],
    asserted: dict[str, Any],
) -> bool:
    if negated["value"] == asserted["value"]:
        return False
    if negated["source_span"]["end"] > asserted["anchor_span"]["start"]:
        return False
    link = text[
        negated["source_span"]["end"] : asserted["anchor_span"]["start"]
    ]
    return re.fullmatch(CONTROLLED_REPLACEMENT_LINK_PATTERN_V2, link) is not None


def _resolve_v2_polarity(
    text: str,
    decisions: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], set[str]]:
    eligible: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    blocked_fields: set[str] = set()
    by_field: dict[str, list[dict[str, Any]]] = {}
    for item in decisions:
        by_field.setdefault(item["field"], []).append(item)

    for field in sorted(by_field):
        field_decisions = by_field[field]
        unresolved = [
            item for item in field_decisions if item["polarity"] == "UNRESOLVED"
        ]
        asserted = [
            item for item in field_decisions if item["polarity"] == "ASSERTED"
        ]
        negated = [
            item for item in field_decisions if item["polarity"] == "NEGATED"
        ]
        if unresolved:
            issues.append(
                {
                    "code": "SOURCE_FACT_POLARITY_UNRESOLVED",
                    "field": field,
                    "state": "UNRESOLVED",
                    "candidate_values": sorted(
                        {item["value"] for item in unresolved + asserted + negated}
                    ),
                    "source_spans": [
                        item["source_span"] for item in unresolved
                    ],
                    "polarity_decision_ids": [
                        item["decision_id"] for item in unresolved
                    ],
                    "blocking": True,
                }
            )
            blocked_fields.add(field)
            continue
        unlinked_negations = [
            item
            for item in negated
            if not any(
                _controlled_replacement_link(text, item, replacement)
                for replacement in asserted
            )
        ]
        if unlinked_negations:
            code = (
                "SOURCE_FACT_NEGATION_UNREPRESENTABLE"
                if not asserted
                else "SOURCE_FACT_POLARITY_CONFLICT"
            )
            issues.append(
                {
                    "code": code,
                    "field": field,
                    "state": (
                        "NEGATED_UNREPRESENTABLE" if not asserted else "CONFLICT"
                    ),
                    "candidate_values": sorted(
                        {item["value"] for item in unlinked_negations + asserted}
                    ),
                    "source_spans": [
                        item["source_span"] for item in unlinked_negations
                    ],
                    "polarity_decision_ids": [
                        item["decision_id"] for item in unlinked_negations
                    ],
                    "blocking": True,
                }
            )
            blocked_fields.add(field)
            continue
        eligible.extend(asserted)
    return eligible, issues, blocked_fields


def _issue_state(
    text: str, candidates: list[dict[str, Any]]
) -> tuple[str, str]:
    spans = [
        span
        for candidate in candidates
        for span in candidate.get("source_spans", [])
    ]
    if spans:
        start = min(item["start"] for item in spans)
        end = max(item["end"] for item in spans)
        if "或" in text[start:end]:
            return "AMBIGUOUS", "SOURCE_FACT_AMBIGUOUS"
    return "CONFLICT", "SOURCE_FACT_CONFLICT"


def _resolve_candidates(
    text: str,
    candidates: dict[str, list[dict[str, Any]]],
    allowed_values: dict[str, tuple[str, ...]],
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]], set[str]]:
    selected: dict[str, list[dict[str, Any]]] = {}
    issues: list[dict[str, Any]] = []
    blocked_fields: set[str] = set()
    for field in sorted(candidates):
        field_candidates = candidates[field]
        by_value: dict[str, list[dict[str, Any]]] = {}
        for candidate in field_candidates:
            by_value.setdefault(candidate["value"], []).append(candidate)
        source_spans = sorted(
            [
                span
                for candidate in field_candidates
                for span in candidate["source_spans"]
            ],
            key=lambda item: (item["start"], item["end"], item["quote"]),
        )
        if len(by_value) != 1:
            state, code = _issue_state(text, field_candidates)
            issues.append(
                {
                    "code": code,
                    "field": field,
                    "state": state,
                    "candidate_values": sorted(by_value),
                    "source_spans": source_spans,
                    "blocking": True,
                }
            )
            blocked_fields.add(field)
            continue
        value = next(iter(by_value))
        allowed = allowed_values.get(field)
        if allowed is not None and value not in allowed:
            issues.append(
                {
                    "code": "SOURCE_REQUEST_CONFLICT",
                    "field": field,
                    "state": "CONFLICT",
                    "candidate_values": [value],
                    "allowed_values": list(allowed),
                    "source_spans": source_spans,
                    "blocking": True,
                }
            )
            blocked_fields.add(field)
            continue
        selected[field] = field_candidates
    return selected, issues, blocked_fields


def extract_source_facts(
    request_value: Any,
    *,
    contract_version: str = SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION,
) -> dict[str, Any]:
    """提取原句事实；返回值不读取评测套件或保留观察。"""

    request = validate_request(request_value)
    if request["schema_version"] != REQUEST_SCHEMA_VERSION_V2:
        raise SourceFactExtractionError("原句事实提取器只支持第二版规划请求。")
    lexical_rules, negation_markers, extraction_version = (
        _extractor_configuration(contract_version)
    )
    text = request["source_text"]
    candidates: dict[str, list[dict[str, Any]]] = {}

    def add_candidate(
        *,
        field: str,
        value: str,
        rule_id: str,
        provenance: str,
        source_spans: list[dict[str, Any]],
        depends_on_fields: list[str] | None = None,
    ) -> None:
        candidates.setdefault(field, []).append(
            {
                "field": field,
                "value": value,
                "rule_id": rule_id,
                "provenance": provenance,
                "source_spans": source_spans,
                "depends_on_fields": depends_on_fields or [],
            }
        )

    add_candidate(
        field=REQUEST_PASSTHROUGH_RULE["field"],
        value=text,
        rule_id=REQUEST_PASSTHROUGH_RULE["rule_id"],
        provenance=REQUEST_PASSTHROUGH_RULE["provenance"],
        source_spans=[_span(text, 0, len(text))],
    )
    match_decisions: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    blocked_fields: set[str] = set()
    if contract_version == SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2:
        match_decisions = _v2_rule_decisions(text, lexical_rules)
        eligible_decisions, issues, blocked_fields = _resolve_v2_polarity(
            text,
            match_decisions,
        )
        for item in match_decisions:
            if item["field"] in blocked_fields:
                item["eligible_for_fact"] = False
        for item in eligible_decisions:
            add_candidate(
                field=item["field"],
                value=item["value"],
                rule_id=item["lexical_rule_id"],
                provenance=next(
                    rule["provenance"]
                    for rule in lexical_rules
                    if rule["rule_id"] == item["lexical_rule_id"]
                ),
                source_spans=[item["source_span"]],
            )
    else:
        for rule in lexical_rules:
            matches = _rule_matches(text, rule, negation_markers)
            if matches:
                add_candidate(
                    field=rule["field"],
                    value=rule["value"],
                    rule_id=rule["rule_id"],
                    provenance=rule["provenance"],
                    source_spans=matches,
                )

    for field in blocked_fields:
        candidates.pop(field, None)

    allowed_values = _allowed_values_by_path(request)
    selected_base, base_issues, base_blocked_fields = _resolve_candidates(
        text, candidates, allowed_values
    )
    issues.extend(base_issues)
    blocked_fields.update(base_blocked_fields)
    selected_base_values = {
        field: field_candidates[0]["value"]
        for field, field_candidates in selected_base.items()
    }
    combined_candidates = deepcopy(selected_base)
    for rule in DERIVATION_RULES:
        dependency = rule["depends_on"]
        if selected_base_values.get(dependency["field"]) == dependency["value"]:
            dependency_candidates = selected_base[dependency["field"]]
            combined_candidates.setdefault(rule["field"], []).append(
                {
                    "field": rule["field"],
                    "value": rule["value"],
                    "rule_id": rule["rule_id"],
                    "provenance": "DETERMINISTIC_DERIVATION",
                    "source_spans": [
                        span
                        for item in dependency_candidates
                        for span in item["source_spans"]
                    ],
                    "depends_on_fields": [dependency["field"]],
                }
            )
    selected_candidates, combined_issues, combined_blocked_fields = (
        _resolve_candidates(text, combined_candidates, allowed_values)
    )
    issues.extend(combined_issues)
    blocked_fields.update(combined_blocked_fields)
    selected: list[dict[str, Any]] = []
    for field, field_candidates in sorted(selected_candidates.items()):
        value = field_candidates[0]["value"]
        selected.append(
            {
                "field": field,
                "value": value,
                "provenance": (
                    field_candidates[0]["provenance"]
                    if len({item["provenance"] for item in field_candidates}) == 1
                    else "DETERMINISTIC_DERIVATION"
                ),
                "rule_ids": sorted(
                    {item["rule_id"] for item in field_candidates}
                ),
                "source_spans": sorted(
                    {
                        (span["start"], span["end"], span["quote"])
                        for item in field_candidates
                        for span in item["source_spans"]
                    }
                ),
                "depends_on_fields": sorted(
                    {
                        dependency
                        for item in field_candidates
                        for dependency in item["depends_on_fields"]
                    }
                ),
            }
        )

    selected.sort(key=lambda item: item["field"])
    facts: list[dict[str, Any]] = []
    fact_ids_by_field: dict[str, str] = {}
    for index, item in enumerate(selected, start=1):
        fact_id = f"SOURCE-FACT-{index:03d}"
        fact_ids_by_field[item["field"]] = fact_id
        facts.append(
            {
                "fact_id": fact_id,
                "field": item["field"],
                "value": item["value"],
                "provenance": item["provenance"],
                "rule_ids": item["rule_ids"],
                "source_spans": [
                    {"start": start, "end": end, "quote": quote}
                    for start, end, quote in item["source_spans"]
                ],
                "depends_on_fact_ids": [],
            }
        )
    for fact, item in zip(facts, selected, strict=True):
        fact["depends_on_fact_ids"] = [
            fact_ids_by_field[field]
            for field in item["depends_on_fields"]
            if field in fact_ids_by_field
        ]

    locked_fields = {fact["field"]: fact["value"] for fact in facts}
    field_resolutions: list[dict[str, Any]] = []
    for stage in HYBRID_STAGE_ORDER:
        for field in sorted(HYBRID_STAGE_REQUIRED_KEYS[stage]):
            path = f"{stage}.{field}"
            if path in blocked_fields:
                state = "BLOCKED"
                delegation = "CLARIFICATION_REQUIRED"
            elif path in locked_fields:
                state = "LOCKED_SOURCE_FACT"
                delegation = "SYSTEM_OWNED_READ_ONLY"
            else:
                state = "NOT_STATED"
                delegation = "MODEL_PROPOSABLE_NON_AUTHORITATIVE"
            field_resolutions.append(
                {"field": path, "state": state, "delegation": delegation}
            )

    result = {
        "schema_version": extraction_version,
        "request_binding": {
            "request_id": request["request_id"],
            "request_sha256": canonical_sha256(request),
            "source_text_sha256": canonical_sha256(text),
        },
        "extractor": {
            "contract_version": contract_version,
            "contract_sha256": source_fact_extractor_contract_sha256(
                contract_version
            ),
        },
        "facts": facts,
        "field_resolutions": field_resolutions,
        "issues": sorted(issues, key=lambda item: (item["field"], item["code"])),
        "blocking_issue_count": sum(item["blocking"] for item in issues),
        "locked_fields": locked_fields,
        "delegable_fields": [
            item["field"]
            for item in field_resolutions
            if item["delegation"] == "MODEL_PROPOSABLE_NON_AUTHORITATIVE"
        ],
        "clarification_required_fields": sorted(blocked_fields),
        "held_out_observation_used": False,
        "formal_decision_created": False,
        "creative_review_required": True,
    }
    if contract_version == SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2:
        result["match_decisions"] = match_decisions
    return result


def field_ownership_view(extraction: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": HYBRID_MERGE_CONTRACT_VERSION,
        "request_binding": deepcopy(extraction["request_binding"]),
        "field_resolutions": deepcopy(extraction["field_resolutions"]),
        "locked_fields": deepcopy(extraction["locked_fields"]),
        "delegable_fields": list(extraction["delegable_fields"]),
        "blocking_issue_count": extraction["blocking_issue_count"],
        "model_may_write_locked_fields": False,
        "formal_decision_created": False,
    }


def locked_fields_for_stage(
    extraction: dict[str, Any], stage: str
) -> dict[str, str]:
    prefix = f"{stage}."
    return {
        path[len(prefix) :]: value
        for path, value in extraction["locked_fields"].items()
        if path.startswith(prefix)
    }


def residual_fields_for_stage(
    extraction: dict[str, Any], stage: str
) -> list[str]:
    locked = set(locked_fields_for_stage(extraction, stage))
    return sorted(HYBRID_STAGE_REQUIRED_KEYS[stage] - locked)


def merge_hybrid_stage_payload(
    stage: str,
    model_payload: Any,
    extraction: dict[str, Any],
) -> tuple[dict[str, Any] | None, list[dict[str, Any]], dict[str, Any]]:
    """合并模型残余字段与只读事实，不自动修补模型输出。"""

    if extraction["blocking_issue_count"]:
        raise SourceFactExtractionError("原句事实存在阻断问题，不能执行混合合并。")
    locked = locked_fields_for_stage(extraction, stage)
    expected_model_fields = set(residual_fields_for_stage(extraction, stage))
    observations: list[dict[str, Any]] = []
    merged: dict[str, Any] | None = None
    if not isinstance(model_payload, dict):
        observations.append(
            {
                "code": "HYBRID_RESIDUAL_NOT_OBJECT",
                "category": "STRUCTURE",
                "path": f"$.stages.{stage}",
                "expected": "object",
                "observed": type(model_payload).__name__,
            }
        )
    else:
        actual = set(model_payload)
        for field in sorted(actual & set(locked)):
            observations.append(
                {
                    "code": "MODEL_WROTE_LOCKED_FIELD",
                    "category": "AUTHORITY",
                    "path": f"$.stages.{stage}.{field}",
                    "expected": "field omitted from model residual payload",
                    "observed": model_payload[field],
                }
            )
        for field in sorted(actual - expected_model_fields - set(locked)):
            observations.append(
                {
                    "code": "HYBRID_RESIDUAL_FIELD_UNAUTHORIZED",
                    "category": "STRUCTURE",
                    "path": f"$.stages.{stage}.{field}",
                    "expected": sorted(expected_model_fields),
                    "observed": model_payload[field],
                }
            )
        for field in sorted(expected_model_fields - actual):
            observations.append(
                {
                    "code": "HYBRID_RESIDUAL_FIELD_MISSING",
                    "category": "STRUCTURE",
                    "path": f"$.stages.{stage}.{field}",
                    "expected": "non-empty JSON string field",
                    "observed": None,
                }
            )
        merged = {
            **locked,
            **{
                field: model_payload[field]
                for field in sorted(expected_model_fields & actual)
            },
        }
    merge_observation = {
        "stage": stage,
        "locked_fields": locked,
        "expected_model_fields": sorted(expected_model_fields),
        "observations": deepcopy(observations),
        "automatic_repair_attempted": False,
        "formal_decision_created": False,
    }
    return merged, observations, merge_observation
