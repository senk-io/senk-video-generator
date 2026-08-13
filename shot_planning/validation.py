"""只记录镜头规划草案的结构观察，不创建接受裁决。"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import asdict, dataclass
from typing import Any

from .contracts import (
    PLANNER_GENERALIZED_OBSERVABILITY_PROMPT_CONTRACT_VERSION,
    PLANNER_HYBRID_SOURCE_FACT_PROMPT_CONTRACT_VERSION,
    PLANNER_PROMPT_CONTRACT_VERSION,
    PLANNER_SCALAR_CHOICE_PROMPT_CONTRACT_VERSION,
    PLANNER_SEMANTIC_GLOSS_PROMPT_CONTRACT_VERSION,
    PROPOSAL_SCHEMA_VERSION,
    PROPOSAL_SCHEMA_VERSION_V2,
    REQUEST_SCHEMA_VERSION_V2,
    SUBJECT_ID_PATTERN,
    SUPPORTED_PLANNER_PROMPT_CONTRACT_VERSIONS,
    canonical_sha256,
    validate_request,
)


SCENE_ID_PATTERN = re.compile(r"SCENE-[0-9]{3}")
BEAT_ID_PATTERN = re.compile(r"BEAT-[0-9]{3}")
SHOT_ID_PATTERN = re.compile(r"SHOT-[0-9]{3}")

PURPOSES = frozenset(
    {
        "ESTABLISH_CONTEXT",
        "DEVELOP_ACTION",
        "EMPHASIZE_EMOTION",
        "REVEAL_INFORMATION",
        "TRANSITION",
        "CLOSE_SEQUENCE",
    }
)
ACTION_CLASSES = frozenset({"STATIC", "MOVE", "PERFORM", "EXPRESS", "INTERACT", "TRANSITION"})
FRAMINGS = frozenset(
    {
        "EXTREME_WIDE",
        "WIDE",
        "MEDIUM_WIDE",
        "MEDIUM",
        "MEDIUM_CLOSE_UP",
        "CLOSE_UP",
        "EXTREME_CLOSE_UP",
        "OVER_THE_SHOULDER",
        "POINT_OF_VIEW",
    }
)
CAMERA_MOVEMENTS = frozenset(
    {"STATIC", "PAN", "TILT", "DOLLY", "TRUCK", "PEDESTAL", "ZOOM", "ARC", "HANDHELD"}
)
CAMERA_DIRECTIONS = frozenset(
    {"NONE", "LEFT", "RIGHT", "UP", "DOWN", "IN", "OUT", "CLOCKWISE", "COUNTERCLOCKWISE"}
)
CAMERA_SPEEDS = frozenset({"NONE", "SLOW", "MODERATE", "FAST"})
CAMERA_DIRECTIONS_BY_MOVEMENT = {
    "PAN": frozenset({"LEFT", "RIGHT"}),
    "TILT": frozenset({"UP", "DOWN"}),
    "DOLLY": frozenset({"IN", "OUT"}),
    "TRUCK": frozenset({"LEFT", "RIGHT"}),
    "PEDESTAL": frozenset({"UP", "DOWN"}),
    "ZOOM": frozenset({"IN", "OUT"}),
    "ARC": frozenset({"LEFT", "RIGHT", "CLOCKWISE", "COUNTERCLOCKWISE"}),
    "HANDHELD": CAMERA_DIRECTIONS,
}
FORBIDDEN_DECISION_KEYS = frozenset(
    {
        "accepted",
        "approved",
        "fail",
        "pass",
        "quality_acceptance",
        "selected",
        "verified",
    }
)


@dataclass(frozen=True, slots=True)
class PlanningObservation:
    code: str
    category: str
    path: str
    expected: Any
    observed: Any


def _observe(
    observations: list[PlanningObservation],
    code: str,
    category: str,
    path: str,
    expected: Any,
    observed: Any,
) -> None:
    observations.append(PlanningObservation(code, category, path, expected, observed))


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _positive_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def _content_positions(text: str) -> set[int]:
    return {
        index
        for index, character in enumerate(text)
        if not character.isspace() and not unicodedata.category(character).startswith("P")
    }


def _forbidden_decision_paths(value: Any, path: str = "$") -> list[str]:
    matches: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            nested_path = f"{path}.{key}"
            if str(key).lower() in FORBIDDEN_DECISION_KEYS:
                matches.append(nested_path)
            matches.extend(_forbidden_decision_paths(nested, nested_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            matches.extend(_forbidden_decision_paths(nested, f"{path}[{index}]"))
    return matches


def observe_proposal(request_value: Any, proposal: Any) -> dict[str, Any]:
    """比较请求与模型草案，返回结构观察和差异，不返回通过或失败。"""

    request = validate_request(request_value)
    observations: list[PlanningObservation] = []

    if not isinstance(proposal, dict):
        _observe(observations, "PROPOSAL_NOT_OBJECT", "STRUCTURE", "$", "object", type(proposal).__name__)
        return _report(request, {}, observations)

    expected_header = {
        "schema_version": (
            PROPOSAL_SCHEMA_VERSION_V2
            if request["schema_version"] == REQUEST_SCHEMA_VERSION_V2
            else PROPOSAL_SCHEMA_VERSION
        ),
        "request_id": request["request_id"],
        "source_text_sha256": canonical_sha256(request["source_text"]),
        "status": "DRAFT_NON_AUTHORITATIVE",
    }
    for field, expected in expected_header.items():
        if proposal.get(field) != expected:
            _observe(
                observations,
                f"{field.upper()}_MISMATCH",
                "BINDING",
                f"$.{field}",
                expected,
                proposal.get(field),
            )

    proposal_id = proposal.get("proposal_id")
    if not _nonempty_text(proposal_id):
        _observe(observations, "PROPOSAL_ID_REQUIRED", "IDENTITY", "$.proposal_id", "non-empty string", proposal_id)

    planner = proposal.get("planner")
    if not isinstance(planner, dict):
        _observe(observations, "PLANNER_METADATA_REQUIRED", "EVIDENCE", "$.planner", "object", planner)
    else:
        for field in ("model_id", "model_version", "run_id"):
            if not _nonempty_text(planner.get(field)):
                _observe(
                    observations,
                    "PLANNER_METADATA_INCOMPLETE",
                    "EVIDENCE",
                    f"$.planner.{field}",
                    "non-empty string",
                    planner.get(field),
                )
        expected_prompt_versions = (
            {
                PLANNER_GENERALIZED_OBSERVABILITY_PROMPT_CONTRACT_VERSION,
                PLANNER_SCALAR_CHOICE_PROMPT_CONTRACT_VERSION,
                PLANNER_SEMANTIC_GLOSS_PROMPT_CONTRACT_VERSION,
                PLANNER_HYBRID_SOURCE_FACT_PROMPT_CONTRACT_VERSION,
            }
            if request["schema_version"] == REQUEST_SCHEMA_VERSION_V2
            else SUPPORTED_PLANNER_PROMPT_CONTRACT_VERSIONS
            - {
                PLANNER_GENERALIZED_OBSERVABILITY_PROMPT_CONTRACT_VERSION,
                PLANNER_SCALAR_CHOICE_PROMPT_CONTRACT_VERSION,
                PLANNER_SEMANTIC_GLOSS_PROMPT_CONTRACT_VERSION,
                PLANNER_HYBRID_SOURCE_FACT_PROMPT_CONTRACT_VERSION,
            }
        )
        if planner.get("prompt_contract_version") not in expected_prompt_versions:
            _observe(
                observations,
                "PROMPT_CONTRACT_VERSION_MISMATCH",
                "EVIDENCE",
                "$.planner.prompt_contract_version",
                sorted(expected_prompt_versions),
                planner.get("prompt_contract_version"),
            )
        sampling = planner.get("sampling")
        if not isinstance(sampling, dict):
            _observe(observations, "SAMPLING_METADATA_REQUIRED", "EVIDENCE", "$.planner.sampling", "object", sampling)
        else:
            if not isinstance(sampling.get("temperature"), (int, float)) or isinstance(
                sampling.get("temperature"), bool
            ):
                _observe(
                    observations,
                    "SAMPLING_TEMPERATURE_REQUIRED",
                    "EVIDENCE",
                    "$.planner.sampling.temperature",
                    "number",
                    sampling.get("temperature"),
                )
            seed = sampling.get("seed")
            if seed is not None and (not isinstance(seed, int) or isinstance(seed, bool)):
                _observe(
                    observations,
                    "SAMPLING_SEED_INVALID",
                    "EVIDENCE",
                    "$.planner.sampling.seed",
                    "integer or null",
                    seed,
                )

    forbidden_paths = _forbidden_decision_paths(proposal)
    for path in forbidden_paths:
        _observe(
            observations,
            "FORMAL_DECISION_FIELD_FORBIDDEN",
            "AUTHORITY",
            path,
            "decision field absent",
            "present",
        )

    scenes, scene_ids = _observe_scenes(proposal.get("scenes"), observations)
    beats, beat_ids, covered_positions = _observe_beats(
        proposal.get("narrative_beats"),
        request["source_text"],
        scene_ids,
        observations,
    )
    shots, referenced_beats = _observe_shots(
        proposal.get("shots"),
        scene_ids,
        beat_ids,
        beats,
        observations,
        request_schema_version=request["schema_version"],
    )

    expected_scene_count = request.get("expected_scene_count")
    if expected_scene_count is not None and len(scenes) != expected_scene_count:
        _observe(
            observations,
            "SCENE_COUNT_MISMATCH",
            "STRUCTURE",
            "$.scenes",
            expected_scene_count,
            len(scenes),
        )
    bounds = request["shot_count_bounds"]
    if not bounds["minimum"] <= len(shots) <= bounds["maximum"]:
        _observe(
            observations,
            "SHOT_COUNT_OUT_OF_BOUNDS",
            "STRUCTURE",
            "$.shots",
            bounds,
            len(shots),
        )

    missing_content = sorted(_content_positions(request["source_text"]) - covered_positions)
    if missing_content:
        _observe(
            observations,
            "SOURCE_CONTENT_NOT_COVERED",
            "COVERAGE",
            "$.narrative_beats",
            "all non-punctuation source characters covered",
            {"missing_indexes": missing_content},
        )
    unreferenced_beats = sorted(beat_ids - referenced_beats)
    if unreferenced_beats:
        _observe(
            observations,
            "BEAT_NOT_MAPPED_TO_SHOT",
            "COVERAGE",
            "$.shots[*].beat_ids",
            "every beat referenced",
            unreferenced_beats,
        )

    duration_sum = sum(
        float(shot.get("target_duration_seconds", 0))
        for shot in shots
        if _positive_number(shot.get("target_duration_seconds"))
    )
    if abs(duration_sum - float(request["target_duration_seconds"])) > float(
        request["duration_tolerance_seconds"]
    ):
        _observe(
            observations,
            "SHOT_DURATION_SUM_MISMATCH",
            "DURATION",
            "$.shots[*].target_duration_seconds",
            {
                "target": request["target_duration_seconds"],
                "tolerance": request["duration_tolerance_seconds"],
            },
            duration_sum,
        )

    observed_subject_ids = {
        subject_id
        for shot in shots
        for subject_id in shot.get("subject_ids", [])
        if isinstance(subject_id, str)
    }
    missing_subjects = sorted(set(request["required_subject_ids"]) - observed_subject_ids)
    if missing_subjects:
        _observe(
            observations,
            "REQUIRED_SUBJECT_NOT_COVERED",
            "COVERAGE",
            "$.shots[*].subject_ids",
            request["required_subject_ids"],
            sorted(observed_subject_ids),
        )

    referenced_scene_ids = {
        item.get("scene_id") for item in [*beats, *shots] if isinstance(item.get("scene_id"), str)
    }
    unused_scenes = sorted(scene_ids - referenced_scene_ids)
    if unused_scenes:
        _observe(
            observations,
            "SCENE_NOT_REFERENCED",
            "COVERAGE",
            "$.scenes",
            "every scene referenced",
            unused_scenes,
        )

    _observe_semantic_constraints(request, scenes, beats, shots, observations)

    return _report(request, proposal, observations)


def _observe_semantic_constraints(
    request: dict[str, Any],
    scenes: list[dict[str, Any]],
    beats: list[dict[str, Any]],
    shots: list[dict[str, Any]],
    observations: list[PlanningObservation],
) -> None:
    constraints = request.get("semantic_constraints")
    if not isinstance(constraints, dict):
        return
    allowed_framings = set(constraints["allowed_framings"])
    allowed_action_classes = set(constraints["allowed_action_classes"])
    allowed_purposes = set(constraints["allowed_primary_purposes"])
    forbidden = {item.casefold() for item in constraints["forbidden_placeholder_values"]}
    minimum_characters = constraints["minimum_free_text_characters"]

    environment_text = " ".join(
        str(scene.get("environment", "")) for scene in scenes if isinstance(scene, dict)
    )
    for term in constraints["required_environment_terms"]:
        if term not in environment_text:
            _observe(
                observations,
                "REQUIRED_ENVIRONMENT_TERM_MISSING",
                "SEMANTIC",
                "$.scenes[*].environment",
                term,
                environment_text,
            )

    scene_term_constraints = {
        "required_location_terms": (
            "location",
            " ".join(
                str(scene.get("location", ""))
                for scene in scenes
                if isinstance(scene, dict)
            ),
        ),
        "required_time_terms": (
            "time",
            " ".join(
                str(scene.get("time", ""))
                for scene in scenes
                if isinstance(scene, dict)
            ),
        ),
    }
    for constraint_field, (scene_field, observed_text) in scene_term_constraints.items():
        for term in constraints.get(constraint_field, []):
            if term not in observed_text:
                _observe(
                    observations,
                    "REQUIRED_SCENE_TERM_MISSING",
                    "SEMANTIC",
                    f"$.scenes[*].{scene_field}",
                    term,
                    observed_text,
                )

    beat_action_text = " ".join(
        str(beat.get("action", "")) for beat in beats if isinstance(beat, dict)
    )
    shot_action_text = " ".join(
        str((shot.get("action") or {}).get("description", ""))
        for shot in shots
        if isinstance(shot, dict) and isinstance(shot.get("action"), dict)
    )
    for term in constraints["required_action_terms"]:
        if term not in beat_action_text:
            _observe(
                observations,
                "REQUIRED_BEAT_ACTION_TERM_MISSING",
                "SEMANTIC",
                "$.narrative_beats[*].action",
                term,
                beat_action_text,
            )
        if term not in shot_action_text:
            _observe(
                observations,
                "REQUIRED_SHOT_ACTION_TERM_MISSING",
                "SEMANTIC",
                "$.shots[*].action.description",
                term,
                shot_action_text,
            )

    for index, shot in enumerate(shots):
        path = f"$.shots[{index}]"
        if shot.get("framing") not in allowed_framings:
            _observe(
                observations,
                "EXPLICIT_FRAMING_MISMATCH",
                "SEMANTIC",
                f"{path}.framing",
                sorted(allowed_framings),
                shot.get("framing"),
            )
        action = shot.get("action") if isinstance(shot.get("action"), dict) else {}
        if action.get("class") not in allowed_action_classes:
            _observe(
                observations,
                "EXPLICIT_ACTION_CLASS_MISMATCH",
                "SEMANTIC",
                f"{path}.action.class",
                sorted(allowed_action_classes),
                action.get("class"),
            )
        if shot.get("primary_purpose") not in allowed_purposes:
            _observe(
                observations,
                "EXPLICIT_PURPOSE_MISMATCH",
                "SEMANTIC",
                f"{path}.primary_purpose",
                sorted(allowed_purposes),
                shot.get("primary_purpose"),
            )
        camera = shot.get("camera") if isinstance(shot.get("camera"), dict) else {}
        camera_semantic_constraints = {
            "allowed_camera_movements": ("movement", "EXPLICIT_CAMERA_MOVEMENT_MISMATCH"),
            "allowed_camera_directions": ("direction", "EXPLICIT_CAMERA_DIRECTION_MISMATCH"),
            "allowed_camera_speeds": ("speed", "EXPLICIT_CAMERA_SPEED_MISMATCH"),
        }
        for constraint_field, (camera_field, code) in camera_semantic_constraints.items():
            allowed_values = constraints.get(constraint_field)
            if isinstance(allowed_values, list) and camera.get(camera_field) not in set(
                allowed_values
            ):
                _observe(
                    observations,
                    code,
                    "CAMERA",
                    f"{path}.camera.{camera_field}",
                    sorted(allowed_values),
                    camera.get(camera_field),
                )
        performance_field = (
            "performance"
            if request["schema_version"] == REQUEST_SCHEMA_VERSION_V2
            else "emotion"
        )
        free_text_fields = {
            "composition": shot.get("composition"),
            performance_field: shot.get(performance_field),
            "lighting": shot.get("lighting"),
            "continuity_in": shot.get("continuity_in"),
            "continuity_out": shot.get("continuity_out"),
        }
        checks = shot.get("observable_checks")
        if isinstance(checks, list):
            free_text_fields.update(
                {f"observable_checks[{check_index}]": check for check_index, check in enumerate(checks)}
            )
        for field, value in free_text_fields.items():
            normalized = value.strip().casefold() if isinstance(value, str) else ""
            if normalized in forbidden or len(normalized) < minimum_characters:
                _observe(
                    observations,
                    "PLACEHOLDER_OR_UNOBSERVABLE_TEXT",
                    "OBSERVABILITY",
                    f"{path}.{field}",
                    {
                        "minimum_characters": minimum_characters,
                        "forbidden_values": sorted(forbidden),
                    },
                    value,
                )

        semantic_text_fields = {
            "required_composition_terms": ("composition", shot.get("composition")),
            "required_emotion_terms": (performance_field, shot.get(performance_field)),
            "required_performance_terms": (
                performance_field,
                shot.get(performance_field),
            ),
            "required_lighting_terms": ("lighting", shot.get("lighting")),
            "required_continuity_in_terms": ("continuity_in", shot.get("continuity_in")),
            "required_continuity_out_terms": (
                "continuity_out",
                shot.get("continuity_out"),
            ),
            "required_observable_terms": (
                "observable_checks",
                " ".join(str(check) for check in checks)
                if isinstance(checks, list)
                else "",
            ),
        }
        for constraint_field, (proposal_field, observed_text) in semantic_text_fields.items():
            for term in constraints.get(constraint_field, []):
                if term not in str(observed_text):
                    _observe(
                        observations,
                        "REQUIRED_OBSERVABLE_TERM_MISSING",
                        "OBSERVABILITY",
                        f"{path}.{proposal_field}",
                        term,
                        observed_text,
                    )
        full_proposal_text = " ".join(
            str(value)
            for value in (
                " ".join(
                    " ".join(
                        str(scene.get(field, ""))
                        for field in ("location", "time", "environment")
                    )
                    for scene in scenes
                    if isinstance(scene, dict)
                ),
                " ".join(
                    str(beat.get("action", ""))
                    for beat in beats
                    if isinstance(beat, dict)
                ),
                shot.get("script_segment"),
                (shot.get("action") or {}).get("description")
                if isinstance(shot.get("action"), dict)
                else "",
                shot.get("composition"),
                shot.get(performance_field),
                shot.get("lighting"),
                shot.get("continuity_in"),
                shot.get("continuity_out"),
                " ".join(str(check) for check in checks)
                if isinstance(checks, list)
                else "",
            )
        )
        for term in constraints.get("forbidden_output_terms", []):
            if term in full_proposal_text:
                _observe(
                    observations,
                    "FORBIDDEN_OUTPUT_TERM_PRESENT",
                    "OBSERVABILITY",
                    path,
                    {"term_absent": term},
                    full_proposal_text,
                )
        minimum_check_count = constraints.get("minimum_observable_check_count")
        if isinstance(minimum_check_count, int) and (
            not isinstance(checks, list) or len(checks) < minimum_check_count
        ):
            _observe(
                observations,
                "OBSERVABLE_CHECK_COUNT_BELOW_MINIMUM",
                "OBSERVABILITY",
                f"{path}.observable_checks",
                {"minimum_count": minimum_check_count},
                len(checks) if isinstance(checks, list) else None,
            )


def _observe_scenes(value: Any, observations: list[PlanningObservation]) -> tuple[list[dict[str, Any]], set[str]]:
    if not isinstance(value, list) or not value:
        _observe(observations, "SCENES_REQUIRED", "STRUCTURE", "$.scenes", "non-empty array", value)
        return [], set()
    scene_ids: set[str] = set()
    scenes: list[dict[str, Any]] = []
    for index, scene in enumerate(value):
        path = f"$.scenes[{index}]"
        if not isinstance(scene, dict):
            _observe(observations, "SCENE_NOT_OBJECT", "STRUCTURE", path, "object", scene)
            continue
        scenes.append(scene)
        expected_id = f"SCENE-{index + 1:03d}"
        scene_id = scene.get("scene_id")
        if scene_id != expected_id or not isinstance(scene_id, str) or not SCENE_ID_PATTERN.fullmatch(scene_id):
            _observe(observations, "SCENE_ID_INVALID", "IDENTITY", f"{path}.scene_id", expected_id, scene_id)
        elif scene_id in scene_ids:
            _observe(observations, "SCENE_ID_DUPLICATE", "IDENTITY", f"{path}.scene_id", "unique", scene_id)
        else:
            scene_ids.add(scene_id)
        if scene.get("ordinal") != index + 1:
            _observe(observations, "SCENE_ORDINAL_INVALID", "ORDER", f"{path}.ordinal", index + 1, scene.get("ordinal"))
        for field in ("location", "time", "environment"):
            if not _nonempty_text(scene.get(field)):
                _observe(observations, "SCENE_FIELD_REQUIRED", "STRUCTURE", f"{path}.{field}", "non-empty string", scene.get(field))
        anchors = scene.get("continuity_anchors")
        if not isinstance(anchors, list) or not all(_nonempty_text(item) for item in anchors):
            _observe(
                observations,
                "SCENE_CONTINUITY_ANCHORS_INVALID",
                "CONTINUITY",
                f"{path}.continuity_anchors",
                "array of non-empty strings",
                anchors,
            )
    return scenes, scene_ids


def _observe_beats(
    value: Any,
    source_text: str,
    scene_ids: set[str],
    observations: list[PlanningObservation],
) -> tuple[list[dict[str, Any]], set[str], set[int]]:
    if not isinstance(value, list) or not value:
        _observe(observations, "BEATS_REQUIRED", "STRUCTURE", "$.narrative_beats", "non-empty array", value)
        return [], set(), set()
    beats: list[dict[str, Any]] = []
    beat_ids: set[str] = set()
    covered_positions: set[int] = set()
    previous_scene_ordinal = 0
    for index, beat in enumerate(value):
        path = f"$.narrative_beats[{index}]"
        if not isinstance(beat, dict):
            _observe(observations, "BEAT_NOT_OBJECT", "STRUCTURE", path, "object", beat)
            continue
        beats.append(beat)
        expected_id = f"BEAT-{index + 1:03d}"
        beat_id = beat.get("beat_id")
        if beat_id != expected_id or not isinstance(beat_id, str) or not BEAT_ID_PATTERN.fullmatch(beat_id):
            _observe(observations, "BEAT_ID_INVALID", "IDENTITY", f"{path}.beat_id", expected_id, beat_id)
        elif beat_id in beat_ids:
            _observe(observations, "BEAT_ID_DUPLICATE", "IDENTITY", f"{path}.beat_id", "unique", beat_id)
        else:
            beat_ids.add(beat_id)
        if beat.get("ordinal") != index + 1:
            _observe(observations, "BEAT_ORDINAL_INVALID", "ORDER", f"{path}.ordinal", index + 1, beat.get("ordinal"))
        scene_id = beat.get("scene_id")
        if scene_id not in scene_ids:
            _observe(observations, "BEAT_SCENE_UNKNOWN", "REFERENCE", f"{path}.scene_id", sorted(scene_ids), scene_id)
        elif isinstance(scene_id, str):
            scene_ordinal = int(scene_id.rsplit("-", 1)[1])
            if scene_ordinal < previous_scene_ordinal:
                _observe(
                    observations,
                    "BEAT_SCENE_ORDER_REVERSED",
                    "ORDER",
                    f"{path}.scene_id",
                    f"scene ordinal >= {previous_scene_ordinal}",
                    scene_ordinal,
                )
            previous_scene_ordinal = max(previous_scene_ordinal, scene_ordinal)
        purpose = beat.get("purpose")
        if purpose not in PURPOSES:
            _observe(observations, "BEAT_PURPOSE_INVALID", "SEMANTIC_SHAPE", f"{path}.purpose", sorted(PURPOSES), purpose)
        if not _nonempty_text(beat.get("action")):
            _observe(observations, "BEAT_ACTION_REQUIRED", "STRUCTURE", f"{path}.action", "non-empty string", beat.get("action"))
        _observe_subject_ids(beat.get("subject_ids"), f"{path}.subject_ids", observations)

        span = beat.get("source_span")
        if not isinstance(span, dict):
            _observe(observations, "BEAT_SOURCE_SPAN_REQUIRED", "COVERAGE", f"{path}.source_span", "object", span)
            continue
        start = span.get("start")
        end = span.get("end")
        quote = span.get("quote")
        if (
            not isinstance(start, int)
            or isinstance(start, bool)
            or not isinstance(end, int)
            or isinstance(end, bool)
            or start < 0
            or end <= start
            or end > len(source_text)
        ):
            _observe(
                observations,
                "BEAT_SOURCE_SPAN_INVALID",
                "COVERAGE",
                f"{path}.source_span",
                {"start": ">= 0", "end": f"<= {len(source_text)} and > start"},
                span,
            )
            continue
        actual_quote = source_text[start:end]
        if quote != actual_quote:
            _observe(observations, "BEAT_SOURCE_QUOTE_MISMATCH", "BINDING", f"{path}.source_span.quote", actual_quote, quote)
        covered_positions.update(range(start, end))
    return beats, beat_ids, covered_positions


def _observe_shots(
    value: Any,
    scene_ids: set[str],
    beat_ids: set[str],
    beats: list[dict[str, Any]],
    observations: list[PlanningObservation],
    *,
    request_schema_version: str,
) -> tuple[list[dict[str, Any]], set[str]]:
    if not isinstance(value, list) or not value:
        _observe(observations, "SHOTS_REQUIRED", "STRUCTURE", "$.shots", "non-empty array", value)
        return [], set()
    beat_scene_by_id = {
        beat.get("beat_id"): beat.get("scene_id")
        for beat in beats
        if isinstance(beat.get("beat_id"), str)
    }
    shots: list[dict[str, Any]] = []
    shot_ids: set[str] = set()
    referenced_beats: set[str] = set()
    previous_scene_ordinal = 0
    for index, shot in enumerate(value):
        path = f"$.shots[{index}]"
        if not isinstance(shot, dict):
            _observe(observations, "SHOT_NOT_OBJECT", "STRUCTURE", path, "object", shot)
            continue
        shots.append(shot)
        expected_id = f"SHOT-{index + 1:03d}"
        shot_id = shot.get("shot_id")
        if shot_id != expected_id or not isinstance(shot_id, str) or not SHOT_ID_PATTERN.fullmatch(shot_id):
            _observe(observations, "SHOT_ID_INVALID", "IDENTITY", f"{path}.shot_id", expected_id, shot_id)
        elif shot_id in shot_ids:
            _observe(observations, "SHOT_ID_DUPLICATE", "IDENTITY", f"{path}.shot_id", "unique", shot_id)
        else:
            shot_ids.add(shot_id)
        if shot.get("ordinal") != index + 1:
            _observe(observations, "SHOT_ORDINAL_INVALID", "ORDER", f"{path}.ordinal", index + 1, shot.get("ordinal"))
        scene_id = shot.get("scene_id")
        if scene_id not in scene_ids:
            _observe(observations, "SHOT_SCENE_UNKNOWN", "REFERENCE", f"{path}.scene_id", sorted(scene_ids), scene_id)
        elif isinstance(scene_id, str):
            scene_ordinal = int(scene_id.rsplit("-", 1)[1])
            if scene_ordinal < previous_scene_ordinal:
                _observe(
                    observations,
                    "SHOT_SCENE_ORDER_REVERSED",
                    "ORDER",
                    f"{path}.scene_id",
                    f"scene ordinal >= {previous_scene_ordinal}",
                    scene_ordinal,
                )
            previous_scene_ordinal = max(previous_scene_ordinal, scene_ordinal)

        referenced = shot.get("beat_ids")
        if (
            not isinstance(referenced, list)
            or not referenced
            or any(not isinstance(item, str) for item in referenced)
            or len(referenced) != len(set(referenced))
        ):
            _observe(observations, "SHOT_BEAT_IDS_INVALID", "REFERENCE", f"{path}.beat_ids", "non-empty unique array", referenced)
        else:
            for beat_id in referenced:
                if beat_id not in beat_ids:
                    _observe(observations, "SHOT_BEAT_UNKNOWN", "REFERENCE", f"{path}.beat_ids", sorted(beat_ids), beat_id)
                else:
                    referenced_beats.add(beat_id)
                    if beat_scene_by_id.get(beat_id) != scene_id:
                        _observe(
                            observations,
                            "SHOT_BEAT_SCENE_MISMATCH",
                            "REFERENCE",
                            f"{path}.beat_ids",
                            scene_id,
                            {beat_id: beat_scene_by_id.get(beat_id)},
                        )

        if shot.get("primary_purpose") not in PURPOSES:
            _observe(
                observations,
                "SHOT_PRIMARY_PURPOSE_INVALID",
                "SEMANTIC_SHAPE",
                f"{path}.primary_purpose",
                sorted(PURPOSES),
                shot.get("primary_purpose"),
            )
        if not _positive_number(shot.get("target_duration_seconds")):
            _observe(
                observations,
                "SHOT_DURATION_INVALID",
                "DURATION",
                f"{path}.target_duration_seconds",
                "positive number",
                shot.get("target_duration_seconds"),
            )
        if shot.get("framing") not in FRAMINGS:
            _observe(observations, "SHOT_FRAMING_INVALID", "CAMERA", f"{path}.framing", sorted(FRAMINGS), shot.get("framing"))
        _observe_subject_ids(shot.get("subject_ids"), f"{path}.subject_ids", observations)

        action = shot.get("action")
        if not isinstance(action, dict):
            _observe(observations, "SHOT_ACTION_REQUIRED", "SEMANTIC_SHAPE", f"{path}.action", "one action object", action)
        else:
            if action.get("class") not in ACTION_CLASSES:
                _observe(
                    observations,
                    "SHOT_ACTION_CLASS_INVALID",
                    "SEMANTIC_SHAPE",
                    f"{path}.action.class",
                    sorted(ACTION_CLASSES),
                    action.get("class"),
                )
            if not _nonempty_text(action.get("description")):
                _observe(
                    observations,
                    "SHOT_ACTION_DESCRIPTION_REQUIRED",
                    "SEMANTIC_SHAPE",
                    f"{path}.action.description",
                    "non-empty string",
                    action.get("description"),
                )

        camera = shot.get("camera")
        if not isinstance(camera, dict):
            _observe(observations, "SHOT_CAMERA_REQUIRED", "CAMERA", f"{path}.camera", "object", camera)
        else:
            if camera.get("movement") not in CAMERA_MOVEMENTS:
                _observe(observations, "SHOT_CAMERA_MOVEMENT_INVALID", "CAMERA", f"{path}.camera.movement", sorted(CAMERA_MOVEMENTS), camera.get("movement"))
            if camera.get("direction") not in CAMERA_DIRECTIONS:
                _observe(observations, "SHOT_CAMERA_DIRECTION_INVALID", "CAMERA", f"{path}.camera.direction", sorted(CAMERA_DIRECTIONS), camera.get("direction"))
            if camera.get("speed") not in CAMERA_SPEEDS:
                _observe(observations, "SHOT_CAMERA_SPEED_INVALID", "CAMERA", f"{path}.camera.speed", sorted(CAMERA_SPEEDS), camera.get("speed"))
            if camera.get("movement") == "STATIC" and (
                camera.get("direction") != "NONE" or camera.get("speed") != "NONE"
            ):
                _observe(
                    observations,
                    "STATIC_CAMERA_HAS_MOTION",
                    "CAMERA",
                    f"{path}.camera",
                    {"direction": "NONE", "speed": "NONE"},
                    camera,
                )
            movement = camera.get("movement")
            allowed_directions = CAMERA_DIRECTIONS_BY_MOVEMENT.get(movement)
            if allowed_directions is not None and camera.get("direction") not in allowed_directions:
                _observe(
                    observations,
                    "CAMERA_DIRECTION_INCOMPATIBLE_WITH_MOVEMENT",
                    "CAMERA",
                    f"{path}.camera.direction",
                    sorted(allowed_directions),
                    camera.get("direction"),
                )
            if movement != "STATIC" and movement in CAMERA_MOVEMENTS and camera.get("speed") == "NONE":
                _observe(
                    observations,
                    "MOVING_CAMERA_SPEED_NONE",
                    "CAMERA",
                    f"{path}.camera.speed",
                    ["SLOW", "MODERATE", "FAST"],
                    camera.get("speed"),
                )

        performance_field = (
            "performance"
            if request_schema_version == REQUEST_SCHEMA_VERSION_V2
            else "emotion"
        )
        for field in (
            "script_segment",
            "composition",
            performance_field,
            "lighting",
            "continuity_in",
            "continuity_out",
        ):
            if not _nonempty_text(shot.get(field)):
                _observe(observations, "SHOT_FIELD_REQUIRED", "STRUCTURE", f"{path}.{field}", "non-empty string", shot.get(field))
        checks = shot.get("observable_checks")
        if not isinstance(checks, list) or not checks or not all(_nonempty_text(item) for item in checks):
            _observe(
                observations,
                "SHOT_OBSERVABLE_CHECKS_INVALID",
                "OBSERVABILITY",
                f"{path}.observable_checks",
                "non-empty array of non-empty strings",
                checks,
            )
    return shots, referenced_beats


def _observe_subject_ids(value: Any, path: str, observations: list[PlanningObservation]) -> None:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) for item in value)
        or len(value) != len(set(value))
        or any(not SUBJECT_ID_PATTERN.fullmatch(item) for item in value)
    ):
        _observe(
            observations,
            "SUBJECT_IDS_INVALID",
            "IDENTITY",
            path,
            "non-empty unique SUBJECT-000 array",
            value,
        )


def _report(
    request: dict[str, Any],
    proposal: dict[str, Any],
    observations: list[PlanningObservation],
) -> dict[str, Any]:
    return {
        "schema_version": "shot-planning-observation.v1",
        "request_id": request["request_id"],
        "proposal_id": proposal.get("proposal_id"),
        "proposal_sha256": canonical_sha256(proposal),
        "observation_count": len(observations),
        "blocking_observation_count": len(observations),
        "observations": [asdict(item) for item in observations],
        "formal_decision_created": False,
        "creative_review_required": True,
    }
