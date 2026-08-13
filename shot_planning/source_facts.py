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


SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION: Final[str] = (
    "shot-source-fact-extractor-contract.v1"
)
SOURCE_FACT_EXTRACTION_VERSION: Final[str] = "shot-source-fact-extraction.v1"
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
NEGATION_MARKERS: Final[tuple[str, ...]] = (
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

LEXICAL_RULES: Final[tuple[dict[str, Any], ...]] = (
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


def source_fact_extractor_contract() -> dict[str, Any]:
    return {
        "schema_version": SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION,
        "supported_request_schema_versions": [REQUEST_SCHEMA_VERSION_V2],
        "supported_language": "zh-Hans",
        "source_offset_unit": "UNICODE_CODE_POINT",
        "source_span_interval": "ZERO_BASED_HALF_OPEN",
        "request_passthrough_rules": [deepcopy(REQUEST_PASSTHROUGH_RULE)],
        "lexical_rules": deepcopy(list(LEXICAL_RULES)),
        "derivation_rules": deepcopy(list(DERIVATION_RULES)),
        "matching_policy": {
            "regex_engine": "python.re",
            "unicode_normalization": "NONE",
            "case_sensitive": True,
            "overlapping_matches": False,
            "clause_boundary_pattern": CLAUSE_BOUNDARY_PATTERN,
            "negation_scope": "CLAUSE_START_THROUGH_MATCH_END_CONSERVATIVE",
            "negation_markers": list(NEGATION_MARKERS),
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


def source_fact_extractor_contract_sha256() -> str:
    return _sha256(source_fact_extractor_contract())


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


def _negated(text: str, start: int, end: int) -> bool:
    boundaries = list(re.finditer(CLAUSE_BOUNDARY_PATTERN, text[:start]))
    clause_start = boundaries[-1].end() if boundaries else 0
    evidence_scope = text[clause_start:end]
    return any(marker in evidence_scope for marker in NEGATION_MARKERS)


def _rule_matches(text: str, rule: dict[str, Any]) -> list[dict[str, Any]]:
    pattern = (
        re.escape(rule["phrase"])
        if rule["kind"] == "EXACT"
        else rule["pattern"]
    )
    return [
        _span(text, match.start(), match.end())
        for match in re.finditer(pattern, text)
        if not _inside_balanced_quotes(text, match.start())
        and not _negated(text, match.start(), match.end())
    ]


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


def extract_source_facts(request_value: Any) -> dict[str, Any]:
    """提取原句事实；返回值不读取评测套件或保留观察。"""

    request = validate_request(request_value)
    if request["schema_version"] != REQUEST_SCHEMA_VERSION_V2:
        raise SourceFactExtractionError("原句事实提取器只支持第二版规划请求。")
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
    for rule in LEXICAL_RULES:
        matches = _rule_matches(text, rule)
        if matches:
            add_candidate(
                field=rule["field"],
                value=rule["value"],
                rule_id=rule["rule_id"],
                provenance=rule["provenance"],
                source_spans=matches,
            )

    allowed_values = _allowed_values_by_path(request)
    selected_base, issues, blocked_fields = _resolve_candidates(
        text, candidates, allowed_values
    )
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
        "schema_version": SOURCE_FACT_EXTRACTION_VERSION,
        "request_binding": {
            "request_id": request["request_id"],
            "request_sha256": canonical_sha256(request),
            "source_text_sha256": canonical_sha256(text),
        },
        "extractor": {
            "contract_version": SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION,
            "contract_sha256": source_fact_extractor_contract_sha256(),
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
