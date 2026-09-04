"""镜头规划诊断报告骨架：只产出机器可读观察，不裁决通过或失败。"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Final


DIAGNOSIS_REPORT_SCHEMA_VERSION: Final[str] = "shot-planning-diagnosis-report.v1"
REQUIRED_DIAGNOSIS_REPORT_FIELDS: Final[tuple[str, ...]] = (
    "coverage",
    "residual",
    "blocks",
    "cannot_approve_reasons",
)
GUESS_PLACEHOLDER_TOKENS: Final[tuple[str, ...]] = ("待猜", "自由发挥")


class DiagnosisReportError(ValueError):
    """诊断报告缺少法定字段或结构不完整，必须失败关闭。"""


def _require_mapping(name: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise DiagnosisReportError(f"诊断报告字段 {name} 必须是对象。")
    return value


def _require_list(name: str, value: Any) -> list[Any]:
    if not isinstance(value, list):
        raise DiagnosisReportError(f"诊断报告字段 {name} 必须是数组。")
    return value


def validate_diagnosis_report(value: Any) -> dict[str, Any]:
    """缺覆盖、残余、阻断或不能批准原因时失败关闭，不补字段。"""

    report = _require_mapping("$", value)
    missing = [
        field for field in REQUIRED_DIAGNOSIS_REPORT_FIELDS if field not in report
    ]
    if missing:
        raise DiagnosisReportError(
            "诊断报告缺字段，失败关闭：" + "、".join(missing)
        )
    coverage = _require_mapping("coverage", report["coverage"])
    for field in (
        "locked_fields",
        "locked_field_count",
        "stated_fields",
        "unstated_fields",
        "field_resolutions",
    ):
        if field not in coverage:
            raise DiagnosisReportError(f"诊断报告覆盖缺字段，失败关闭：{field}")
    residual = _require_mapping("residual", report["residual"])
    for field in (
        "delegable_fields",
        "clarification_required_fields",
        "contains_guess_placeholder",
        "empty_or_freeform",
    ):
        if field not in residual:
            raise DiagnosisReportError(f"诊断报告残余缺字段，失败关闭：{field}")
    blocks = _require_list("blocks", report["blocks"])
    for index, item in enumerate(blocks):
        block = _require_mapping(f"blocks[{index}]", item)
        for field in ("category", "code", "blocking"):
            if field not in block:
                raise DiagnosisReportError(
                    f"诊断报告阻断项缺字段，失败关闭：blocks[{index}].{field}"
                )
        if block["blocking"] is not True:
            raise DiagnosisReportError("诊断报告阻断项必须标记 blocking=true。")
    reasons = _require_list("cannot_approve_reasons", report["cannot_approve_reasons"])
    if not reasons or any(
        not isinstance(item, str) or not item.strip() for item in reasons
    ):
        raise DiagnosisReportError("不能批准原因必须是非空字符串数组，缺一项失败关闭。")
    return report


def build_diagnosis_report(
    *,
    extraction: dict[str, Any],
    blocks: list[dict[str, Any]],
    source_text: str,
    request_id: str,
    extra_cannot_approve_reasons: list[str] | None = None,
) -> dict[str, Any]:
    """从原句事实与进模型前阻断构造诊断骨架，不产生正式裁决。"""

    field_resolutions = list(extraction.get("field_resolutions") or [])
    locked_fields = dict(extraction.get("locked_fields") or {})
    delegable = list(extraction.get("delegable_fields") or [])
    clarification = list(extraction.get("clarification_required_fields") or [])
    stated = [
        item["field"]
        for item in field_resolutions
        if item.get("state") == "LOCKED_SOURCE_FACT"
    ]
    unstated = [
        item["field"]
        for item in field_resolutions
        if item.get("state") == "NOT_STATED"
    ]
    guess_hits = [token for token in GUESS_PLACEHOLDER_TOKENS if token in source_text]
    empty_or_freeform = bool(guess_hits) or any(
        not field.strip() for field in delegable if isinstance(field, str)
    )
    normalized_blocks = [deepcopy(item) for item in blocks]
    standing_reasons = [
        "产物仍标 DRAFT_NON_AUTHORITATIVE",
        "禁止自称正式 ShotSpec",
        "禁止自称质量通过",
        "本报告不是正式 Diagnosis 事实，也不产生 PASS 或 FAIL 裁决",
    ]
    if empty_or_freeform or guess_hits:
        standing_reasons.append("残余字段不得留「待猜」；留空或自由发挥即失败")
    for item in normalized_blocks:
        standing_reasons.append(
            f"进模型前阻断 {item['category']}：{item.get('summary') or item['code']}"
        )
    if extra_cannot_approve_reasons:
        standing_reasons.extend(extra_cannot_approve_reasons)
    deduped_reasons: list[str] = []
    for reason in standing_reasons:
        if reason not in deduped_reasons:
            deduped_reasons.append(reason)
    report = {
        "schema_version": DIAGNOSIS_REPORT_SCHEMA_VERSION,
        "status": "DRAFT_NON_AUTHORITATIVE",
        "request_id": request_id,
        "formal_decision_created": False,
        "formal_shot_spec_created": False,
        "formal_quality_acceptance_created": False,
        "model_invoked": False,
        "model_invocation_allowed": not normalized_blocks,
        "coverage": {
            "locked_fields": locked_fields,
            "locked_field_count": len(locked_fields),
            "stated_fields": stated,
            "unstated_fields": unstated,
            "field_resolutions": deepcopy(field_resolutions),
        },
        "residual": {
            "delegable_fields": delegable,
            "clarification_required_fields": clarification,
            "contains_guess_placeholder": bool(guess_hits),
            "empty_or_freeform": empty_or_freeform,
            "guess_placeholder_tokens": guess_hits,
        },
        "blocks": normalized_blocks,
        "cannot_approve_reasons": deduped_reasons,
        "creative_review_required": True,
    }
    return validate_diagnosis_report(report)
