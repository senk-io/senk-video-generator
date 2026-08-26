"""重复规划结果的确定性结构稳定性观察。"""

from __future__ import annotations

from collections import Counter
from typing import Any, Callable

from .contracts import canonical_sha256, validate_request
from .validation import observe_proposal


def _normalized_scene_assignments(items: list[dict[str, Any]]) -> list[int | None]:
    values: list[int | None] = []
    for item in items:
        scene_id = item.get("scene_id")
        if isinstance(scene_id, str) and scene_id.startswith("SCENE-"):
            try:
                values.append(int(scene_id.rsplit("-", 1)[1]))
                continue
            except ValueError:
                pass
        values.append(None)
    return values


def structural_fingerprint(proposal: dict[str, Any], target_duration: float) -> dict[str, Any]:
    scenes = proposal.get("scenes") if isinstance(proposal.get("scenes"), list) else []
    beats = proposal.get("narrative_beats") if isinstance(proposal.get("narrative_beats"), list) else []
    shots = proposal.get("shots") if isinstance(proposal.get("shots"), list) else []
    duration_profile = []
    for shot in shots:
        duration = shot.get("target_duration_seconds") if isinstance(shot, dict) else None
        duration_profile.append(
            round(float(duration) / target_duration, 4)
            if isinstance(duration, (int, float)) and not isinstance(duration, bool)
            else None
        )
    return {
        "scene_count": len(scenes),
        "beat_count": len(beats),
        "shot_count": len(shots),
        "beat_purpose_sequence": [item.get("purpose") if isinstance(item, dict) else None for item in beats],
        "beat_scene_assignments": _normalized_scene_assignments(
            [item for item in beats if isinstance(item, dict)]
        ),
        "shot_purpose_sequence": [
            item.get("primary_purpose") if isinstance(item, dict) else None for item in shots
        ],
        "shot_action_class_sequence": [
            (item.get("action") or {}).get("class")
            if isinstance(item, dict) and isinstance(item.get("action"), dict)
            else None
            for item in shots
        ],
        "shot_framing_sequence": [item.get("framing") if isinstance(item, dict) else None for item in shots],
        "shot_camera_movement_sequence": [
            (item.get("camera") or {}).get("movement")
            if isinstance(item, dict) and isinstance(item.get("camera"), dict)
            else None
            for item in shots
        ],
        "shot_scene_assignments": _normalized_scene_assignments(
            [item for item in shots if isinstance(item, dict)]
        ),
        "duration_profile": duration_profile,
    }


def _field_observation(fingerprints: list[dict[str, Any]], field: str) -> dict[str, Any]:
    serialized = [canonical_sha256(item[field]) for item in fingerprints]
    counts = Counter(serialized)
    largest_group = max(counts.values(), default=0)
    examples: dict[str, Any] = {}
    for digest, fingerprint in zip(serialized, fingerprints, strict=True):
        examples.setdefault(digest, fingerprint[field])
    return {
        "distinct_value_count": len(counts),
        "largest_group_ratio": round(largest_group / len(fingerprints), 4) if fingerprints else None,
        "value_groups": [
            {"value_sha256": digest, "run_count": count, "value": examples[digest]}
            for digest, count in sorted(counts.items())
        ],
    }


def _comparison_context(proposal: dict[str, Any]) -> dict[str, Any]:
    planner = proposal.get("planner") if isinstance(proposal.get("planner"), dict) else {}
    return {
        "model_id": planner.get("model_id"),
        "model_version": planner.get("model_version"),
        "prompt_contract_version": planner.get("prompt_contract_version"),
        "sampling": planner.get("sampling"),
    }


def observe_stability(request_value: Any, proposals: list[Any]) -> dict[str, Any]:
    """比较至少两次原始模型输出，只报告一致率，不作稳定或接受裁决。"""

    request = validate_request(request_value)
    proposal_reports = [observe_proposal(request, proposal) for proposal in proposals]
    structurally_comparable = [
        proposal
        for proposal, report in zip(proposals, proposal_reports, strict=True)
        if isinstance(proposal, dict) and report["blocking_observation_count"] == 0
    ]
    identity_unique: list[dict[str, Any]] = []
    seen_proposal_ids: set[str] = set()
    seen_run_ids: set[str] = set()
    duplicate_proposal_ids: set[str] = set()
    duplicate_run_ids: set[str] = set()
    for proposal in structurally_comparable:
        proposal_id = proposal["proposal_id"]
        run_id = proposal["planner"]["run_id"]
        if proposal_id in seen_proposal_ids:
            duplicate_proposal_ids.add(proposal_id)
            continue
        if run_id in seen_run_ids:
            duplicate_run_ids.add(run_id)
            continue
        seen_proposal_ids.add(proposal_id)
        seen_run_ids.add(run_id)
        identity_unique.append(proposal)

    contexts: dict[str, dict[str, Any]] = {}
    for proposal in identity_unique:
        context = _comparison_context(proposal)
        contexts.setdefault(canonical_sha256(context), context)
    comparable = identity_unique if len(contexts) <= 1 else []
    comparison_performed = len(comparable) >= 2
    fingerprints = (
        [
            structural_fingerprint(proposal, float(request["target_duration_seconds"]))
            for proposal in comparable
        ]
        if comparison_performed
        else []
    )
    signature_groups: dict[str, list[str | None]] = {}
    comparison_proposals = comparable if comparison_performed else []
    for proposal, fingerprint in zip(comparison_proposals, fingerprints, strict=True):
        signature_groups.setdefault(canonical_sha256(fingerprint), []).append(proposal.get("proposal_id"))
    largest_exact_group = max((len(group) for group in signature_groups.values()), default=0)
    fields = list(fingerprints[0]) if fingerprints else []
    run_observations: list[dict[str, Any]] = []
    if len(proposals) < 2:
        run_observations.append(
            {
                "code": "REPEATED_RUNS_REQUIRED",
                "expected": "at least 2 runs",
                "observed": len(proposals),
            }
        )
    if len(proposals) < 3:
        run_observations.append(
            {
                "code": "RECOMMENDED_RUN_COUNT_NOT_REACHED",
                "expected": "at least 3 runs for a useful first observation",
                "observed": len(proposals),
            }
        )
    if len(structurally_comparable) != len(proposals):
        run_observations.append(
            {
                "code": "RUNS_EXCLUDED_FROM_COMPARISON",
                "expected": len(proposals),
                "observed": len(structurally_comparable),
            }
        )
    if duplicate_proposal_ids:
        run_observations.append(
            {
                "code": "DUPLICATE_PROPOSAL_IDENTITIES_EXCLUDED",
                "expected": "unique proposal_id per run",
                "observed": sorted(duplicate_proposal_ids),
            }
        )
    if duplicate_run_ids:
        run_observations.append(
            {
                "code": "DUPLICATE_RUN_IDENTITIES_EXCLUDED",
                "expected": "unique planner.run_id per run",
                "observed": sorted(duplicate_run_ids),
            }
        )
    if len(contexts) > 1:
        run_observations.append(
            {
                "code": "COMPARISON_CONTEXTS_DIFFER",
                "expected": "one model, version, prompt contract and sampling context",
                "observed": len(contexts),
            }
        )
    if not comparison_performed:
        run_observations.append(
            {
                "code": "INSUFFICIENT_UNIQUE_COMPARABLE_RUNS",
                "expected": "at least 2 unique runs in one comparison context",
                "observed": len(comparable),
            }
        )
    return {
        "schema_version": "shot-planning-stability-observation.v1",
        "request_id": request["request_id"],
        "run_count": len(proposals),
        "comparable_run_count": len(comparable),
        "comparison_context_count": len(contexts),
        "comparison_contexts": [
            {"context_sha256": digest, "context": context}
            for digest, context in sorted(contexts.items())
        ],
        "comparison_performed": comparison_performed,
        "proposal_observations": proposal_reports,
        "run_observations": run_observations,
        "exact_structure_group_count": len(signature_groups),
        "largest_exact_structure_group_ratio": (
            round(largest_exact_group / len(comparable), 4) if comparison_performed else None
        ),
        "exact_structure_groups": [
            {"signature_sha256": digest, "proposal_ids": proposal_ids}
            for digest, proposal_ids in sorted(signature_groups.items())
        ],
        "field_consistency": {
            field: _field_observation(fingerprints, field) for field in fields
        },
        "formal_decision_created": False,
        "creative_review_required": True,
    }


def collect_local_proposals(
    request_value: Any,
    planner: Callable[[dict[str, Any], int], dict[str, Any]],
    run_count: int,
) -> list[dict[str, Any]]:
    """调用注入的本地规划器；不隐藏重试，也不自行增加运行次数。"""

    request = validate_request(request_value)
    if not isinstance(run_count, int) or isinstance(run_count, bool) or run_count < 1:
        raise ValueError("run_count 必须是正整数。")
    return [planner(request, run_index) for run_index in range(1, run_count + 1)]
