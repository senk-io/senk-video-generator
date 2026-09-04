"""进模型前确定性守卫：复用 v12 提取器，不足则追加规则，不降观察阈值。"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Final

from .diagnosis_report import build_diagnosis_report, validate_diagnosis_report
from .source_facts import (
    SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
    extract_source_facts,
)
from .contracts import validate_request


PRE_MODEL_GUARD_CONTRACT_VERSION: Final[str] = "shot-planning-pre-model-guard.v1"
ADVERSARIAL_SET_SCHEMA_VERSION: Final[str] = (
    "shot-planning-adversarial-pre-model-set.v1"
)
BLOCK_CATEGORIES: Final[dict[str, str]] = {
    "NEGATION_WITHOUT_REPLACEMENT": "否定无正向替代",
    "SUBJECT_CAMERA_CROSSOVER": "主客机位穿越",
    "STATIC_CAMERA_COMPOUND_CONFLICT": "固定相机复合冲突",
    "ABBREVIATION_OVERRIDE": "缩写覆盖",
    "LOCKED_FIELD_POLLUTION": "锁定字段污染",
    "CROSS_STAGE_CONTRADICTION": "跨阶段自相矛盾",
}
CONTROLLED_REPLACEMENT_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"而是|反而|反倒|改用|改为|换成|转为"
)
SUBJECT_NEAR_CAMERA_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"(?:身后|附近|旁边|前方|后面|前头)的?(?:相机|镜头|摄像机|摄影机|机位)"
)
CAMERA_LATERAL_MOTION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"(?:相机|镜头|摄像机|摄影机|机位)(?:不要|并未|没有|并非)?"
    r"(?:从左向右|从右向左)(?:移动|行驶|穿过|走|跑)"
)
STATIC_CAMERA_TOKEN_PATTERN: Final[re.Pattern[str]] = re.compile(r"固定相机|保持静止")
CAMERA_MOTION_CONFLICT_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"摇摄|推进|拉近|拉远|手持运动|从左向右移动|从右向左移动|向右摇|向左摇"
)
ABBREVIATION_OVERRIDE_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"(?:CU|ECU|MCU|MS|WS|LS|ELS).{0,16}(?:覆盖|顶替|改成|改为|简称)"
    r"|(?:覆盖|顶替|简称|缩写).{0,16}(?:CU|ECU|MCU|MS|WS|LS|ELS|特写|中景|全景|锁定)"
    r"|用缩写"
)
LOCKED_FIELD_POLLUTION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"(?:已锁定|系统锁定|锁定的|锁定字段|把锁定|覆盖已锁定|模型改写)"
    r"|锁定.{0,16}(?:改成|改为|改写|覆盖|换成)"
)
FRAMING_TERMS: Final[tuple[tuple[str, str], ...]] = (
    ("特写", "CLOSE_UP"),
    ("中景", "MEDIUM"),
    ("全景", "WIDE"),
)
ACTION_TERMS: Final[tuple[tuple[str, str], ...]] = (
    ("微笑", "SMILING"),
    ("哭泣", "CRYING"),
)
TIME_TERMS: Final[tuple[tuple[str, str], ...]] = (
    ("白天", "DAY"),
    ("夜晚", "NIGHT"),
    ("夜间", "NIGHT"),
)
LOCATION_TERMS: Final[tuple[tuple[str, str], ...]] = (
    ("室内", "INDOOR_LOCATION"),
    ("室外", "OUTDOOR_LOCATION"),
)


class PreModelGuardError(ValueError):
    """进模型前守卫阻断，禁止构建第十二版提示或启动模型。"""

    def __init__(self, report: dict[str, Any]) -> None:
        reasons = report.get("cannot_approve_reasons") or ["进模型前守卫阻断"]
        super().__init__("；".join(reasons))
        self.report = report


def _block(
    category: str,
    code: str,
    *,
    field: str | None = None,
    summary: str,
    evidence: str,
) -> dict[str, Any]:
    return {
        "category": category,
        "category_zh": BLOCK_CATEGORIES[category],
        "code": code,
        "field": field,
        "blocking": True,
        "summary": summary,
        "evidence": evidence,
    }


def _map_extractor_issues(extraction: dict[str, Any]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    for issue in extraction.get("issues") or []:
        code = issue.get("code")
        field = issue.get("field")
        if code == "SOURCE_FACT_NEGATION_UNREPRESENTABLE":
            category = "NEGATION_WITHOUT_REPLACEMENT"
        elif code in {"SOURCE_FACT_POLARITY_UNRESOLVED", "SOURCE_FACT_POLARITY_CONFLICT"}:
            category = "NEGATION_WITHOUT_REPLACEMENT"
        elif code in {"SOURCE_FACT_CONFLICT", "SOURCE_FACT_AMBIGUOUS"} and isinstance(
            field, str
        ) and field.startswith("shot_core.camera_"):
            category = "STATIC_CAMERA_COMPOUND_CONFLICT"
        else:
            category = "CROSS_STAGE_CONTRADICTION"
        blocks.append(
            _block(
                category,
                str(code),
                field=field if isinstance(field, str) else None,
                summary=f"v12 提取器阻断 {code}",
                evidence=json.dumps(issue, ensure_ascii=False, sort_keys=True),
            )
        )
    return blocks


def _has_controlled_replacement(text: str) -> bool:
    return CONTROLLED_REPLACEMENT_PATTERN.search(text) is not None


def _paired_terms_conflict(
    text: str,
    terms: tuple[tuple[str, str], ...],
) -> list[tuple[str, str]]:
    hits = [label for label, _value in terms if label in text]
    unique = []
    for label in hits:
        if label not in unique:
            unique.append(label)
    if len(unique) < 2 or _has_controlled_replacement(text):
        return []
    return [(unique[0], unique[1])]


def _additional_rule_blocks(text: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    if SUBJECT_NEAR_CAMERA_PATTERN.search(text) and (
        "从左向右" in text or "从右向左" in text
    ):
        blocks.append(
            _block(
                "SUBJECT_CAMERA_CROSSOVER",
                "PRE_MODEL_SUBJECT_CAMERA_CROSSOVER",
                field="performance.orientation_state",
                summary="主体附近机位承担横向运动",
                evidence=text,
            )
        )
    if CAMERA_LATERAL_MOTION_PATTERN.search(text):
        blocks.append(
            _block(
                "SUBJECT_CAMERA_CROSSOVER",
                "PRE_MODEL_CAMERA_LATERAL_AS_SUBJECT_MOTION",
                field="shot_core.camera_movement",
                summary="相机术语直接承接主体横向运动",
                evidence=text,
            )
        )
    if STATIC_CAMERA_TOKEN_PATTERN.search(text) and CAMERA_MOTION_CONFLICT_PATTERN.search(
        text
    ):
        blocks.append(
            _block(
                "STATIC_CAMERA_COMPOUND_CONFLICT",
                "PRE_MODEL_STATIC_CAMERA_COMPOUND_CONFLICT",
                field="shot_core.camera_movement",
                summary="固定相机或保持静止与相机运动复合并存",
                evidence=text,
            )
        )
    if ABBREVIATION_OVERRIDE_PATTERN.search(text):
        blocks.append(
            _block(
                "ABBREVIATION_OVERRIDE",
                "PRE_MODEL_ABBREVIATION_OVERRIDE",
                summary="缩写或简称用于覆盖显式镜头事实",
                evidence=text,
            )
        )
    if LOCKED_FIELD_POLLUTION_PATTERN.search(text):
        blocks.append(
            _block(
                "LOCKED_FIELD_POLLUTION",
                "PRE_MODEL_LOCKED_FIELD_POLLUTION",
                summary="原句要求改写或污染锁定字段",
                evidence=text,
            )
        )
    for left, right in _paired_terms_conflict(text, FRAMING_TERMS):
        blocks.append(
            _block(
                "CROSS_STAGE_CONTRADICTION",
                "PRE_MODEL_FRAMING_CROSS_STAGE_CONTRADICTION",
                field="shot_core.framing",
                summary=f"景别跨阶段并存：{left} / {right}",
                evidence=text,
            )
        )
    for left, right in _paired_terms_conflict(text, ACTION_TERMS):
        blocks.append(
            _block(
                "CROSS_STAGE_CONTRADICTION",
                "PRE_MODEL_ACTION_CROSS_STAGE_CONTRADICTION",
                field="performance.visible_action_state",
                summary=f"表演与连续性动作互斥：{left} / {right}",
                evidence=text,
            )
        )
    for left, right in _paired_terms_conflict(text, TIME_TERMS):
        blocks.append(
            _block(
                "CROSS_STAGE_CONTRADICTION",
                "PRE_MODEL_TIME_CROSS_STAGE_CONTRADICTION",
                field="scene_context.time",
                summary=f"时间跨阶段并存：{left} / {right}",
                evidence=text,
            )
        )
    if "室内" in text and "室外" in text and "室内设计" not in text:
        if not _has_controlled_replacement(text):
            blocks.append(
                _block(
                    "CROSS_STAGE_CONTRADICTION",
                    "PRE_MODEL_LOCATION_CROSS_STAGE_CONTRADICTION",
                    field="scene_context.location",
                    summary="地点跨阶段并存：室内 / 室外",
                    evidence=text,
                )
            )
    return blocks


def _dedupe_blocks(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, str | None]] = set()
    unique: list[dict[str, Any]] = []
    for item in blocks:
        key = (item["category"], item["code"], item.get("field"))
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def evaluate_pre_model_guard(request_value: Any) -> dict[str, Any]:
    """对一句话请求做进模型前拦截，并产出诊断报告骨架。"""

    request = validate_request(request_value)
    extraction = extract_source_facts(
        request,
        contract_version=SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
    )
    blocks = _dedupe_blocks(
        [
            *_map_extractor_issues(extraction),
            *_additional_rule_blocks(request["source_text"]),
        ]
    )
    report = build_diagnosis_report(
        extraction=extraction,
        blocks=blocks,
        source_text=request["source_text"],
        request_id=request["request_id"],
        extra_cannot_approve_reasons=[
            "进模型前守卫使用 shot-planning-pre-model-guard.v1，不加载模型权重"
        ],
    )
    report["guard"] = {
        "contract_version": PRE_MODEL_GUARD_CONTRACT_VERSION,
        "extractor_contract_version": SOURCE_FACT_EXTRACTOR_CONTRACT_VERSION_V2,
        "automatic_repair": False,
        "observation_threshold_lowered": False,
    }
    report["extraction"] = {
        "schema_version": extraction["schema_version"],
        "blocking_issue_count": extraction["blocking_issue_count"],
        "formal_decision_created": extraction["formal_decision_created"],
    }
    return validate_diagnosis_report(report)


def assert_model_invocation_allowed(report: dict[str, Any]) -> dict[str, Any]:
    checked = validate_diagnosis_report(report)
    if not checked["model_invocation_allowed"]:
        raise PreModelGuardError(checked)
    return checked


def load_adversarial_set(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != ADVERSARIAL_SET_SCHEMA_VERSION:
        raise ValueError("对抗集合同版本不受支持。")
    items = payload.get("items")
    if not isinstance(items, list) or len(items) < 20:
        raise ValueError("对抗集必须至少包含 20 条。")
    categories = {item.get("expected_block_category") for item in items}
    missing = set(BLOCK_CATEGORIES) - categories
    if missing:
        raise ValueError("对抗集缺少冻结类别：" + "、".join(sorted(missing)))
    return payload


def evaluate_adversarial_set(
    set_path: str | Path,
    *,
    experiment_root: str | Path,
) -> dict[str, Any]:
    """对固定对抗集做无模型拦截观察，不产生正式过线裁决。"""

    payload = load_adversarial_set(set_path)
    root = Path(experiment_root)
    results: list[dict[str, Any]] = []
    for item in payload["items"]:
        request = json.loads(
            (root / item["request_template"]).read_text(encoding="utf-8")
        )
        request["source_text"] = item["source_text"]
        report = evaluate_pre_model_guard(request)
        categories = {block["category"] for block in report["blocks"]}
        intercepted = report["model_invocation_allowed"] is False
        expected_present = item["expected_block_category"] in categories
        results.append(
            {
                "id": item["id"],
                "source_text": item["source_text"],
                "expected_block_category": item["expected_block_category"],
                "intercepted": intercepted,
                "expected_category_present": expected_present,
                "observed_categories": sorted(categories),
                "model_invoked": report["model_invoked"],
                "report": report,
            }
        )
    missed = [
        item["id"]
        for item in results
        if not item["intercepted"] or not item["expected_category_present"]
    ]
    return {
        "schema_version": ADVERSARIAL_SET_SCHEMA_VERSION,
        "status": "DRAFT_NON_AUTHORITATIVE",
        "item_count": len(results),
        "intercepted_count": sum(item["intercepted"] for item in results),
        "expected_category_hit_count": sum(
            item["expected_category_present"] for item in results
        ),
        "missed_ids": missed,
        "model_weight_loaded": False,
        "formal_decision_created": False,
        "formal_shot_spec_created": False,
        "formal_quality_acceptance_created": False,
        "counts_toward_planning_gate": False,
        "results": results,
    }
