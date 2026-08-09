#!/usr/bin/env python3
"""生成测试、确定性回放、并发与投影正确性非权威证据包。"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.governance import GovernanceKernel, ProtectedWriteRequest, RECORD_SPECS


RUN_ID = os.environ.get("GOVERNANCE_CORRECTNESS_RUN_ID", "CR-0015-CORRECTNESS-001")
EXECUTION_ID = f"{RUN_ID}:deterministic-input"
SCOPE_REF = "scope:evidence:correctness"
EVIDENCE_PARENT = ROOT / "evidence" / "runtime"
TARGET = EVIDENCE_PARENT / RUN_ID
REPLAY_COUNT = 5
THREAD_WORKERS = 32
PROCESS_WORKERS = 16
TABLES = (
    "runtime_metadata",
    "authority_grants",
    "protected_records",
    "write_attempts",
    "write_conflicts",
)


class DeterministicClock:
    def __init__(self) -> None:
        self._base = datetime(2026, 8, 9, tzinfo=timezone.utc)
        self._ticks = 0

    def __call__(self) -> str:
        self._ticks += 1
        value = self._base + timedelta(microseconds=self._ticks)
        return value.isoformat(timespec="microseconds").replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_digest(paths: tuple[Path, ...]) -> str:
    lines = [f"{sha256_file(path)}  {path.relative_to(ROOT)}\n" for path in paths]
    return sha256_bytes("".join(sorted(lines)).encode("utf-8"))


def implementation_digest() -> str:
    return source_digest(
        (
            ROOT / "runtime" / "governance" / "catalog.py",
            ROOT / "runtime" / "governance" / "kernel.py",
        )
    )


def harness_digest() -> str:
    return source_digest(
        (
            ROOT / "tests" / "test_governance_kernel.py",
            ROOT / "tools" / "run_correctness_evidence.py",
        )
    )


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def spec_for(record_type: str):
    return next(spec for spec in RECORD_SPECS if spec.record_type == record_type)


def spec_index(spec) -> int:
    return RECORD_SPECS.index(spec) + 1


def grant_id(spec) -> str:
    return f"grant:{RUN_ID}:{spec_index(spec):02d}"


def payload_for(
    spec,
    marker: str,
    *,
    candidate_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidate: dict[str, Any] = {"marker": marker, "scope": SCOPE_REF}
    if spec.record_type == "Registered Closure Completeness Record":
        candidate["closure_completeness"] = "COMPLETE"
    elif spec.record_type in {
        "Registered Projection Change Audit Record",
        "Projection Publication Envelope",
    }:
        candidate.update(
            {
                "change_reason": "INITIAL_PUBLICATION",
                "closure_completeness": "COMPLETE",
                "new_coordinate_digest": "coordinate:projection:v1",
                "previous_coordinate_digest": "NOT_APPLICABLE",
                "previous_publication_record_id": "CANONICAL_BOOTSTRAP_MARKER",
                "projection_result": "COMMITTED",
                "projection_stable_key": "projection:stable:001",
                "transition_rule_version": "transition-rule:v1",
                "view_mode": "AS_KNOWN_AT_K",
            }
        )
    elif spec.record_type == "Registered Projection Rebuild Requirement":
        candidate.update(
            {
                "closure_record_id": "PENDING",
                "impact_scope": "projection:stable:001",
                "new_coordinate_digest": "coordinate:projection:v2",
                "previous_coordinate_digest": "coordinate:projection:v1",
                "previous_publication_record_id": "PENDING",
                "recovery_path": "PATH_A_NEW_SUPPORT",
                "trigger_record_id": "PENDING",
            }
        )
    elif spec.record_type == "Registered Projection Deletion Record":
        candidate.update(
            {
                "cache_object_id": "cache:projection:stable:001:v1",
                "deletion_reason": "REBUILD_REQUIRED",
                "rebuild_requirement_record_id": "PENDING",
                "target_publication_record_id": "PENDING",
            }
        )
    if candidate_overrides:
        candidate.update(candidate_overrides)
    return {
        "candidate_payload": candidate,
        "evidence_mode": "NON_AUTHORITATIVE_CONFORMANCE",
        "institution_freeze_ref": "NOT_CREATED_EVIDENCE_ONLY",
        "knowledge_boundary": "K:correctness:fixed",
        "proposal_ref": spec.proposal_version,
        "result": "EVIDENCE_ONLY",
        "temporal_coordinate": {
            "Q": "2026-Q3",
            "RR": "correctness-evidence",
            "S": "fixed-subject",
        },
    }


def request_for(
    spec,
    *,
    attempt_id: str,
    semantic_key: str,
    payload: dict[str, Any],
    prerequisites: tuple[str, ...] = (),
    predecessor: str | None = None,
    execution_id: str = EXECUTION_ID,
    observed_at: str | None = None,
) -> ProtectedWriteRequest:
    return ProtectedWriteRequest(
        attempt_id=attempt_id,
        execution_id=execution_id,
        principal_id=f"writer:{spec.workflow_id}",
        workflow_id=spec.workflow_id,
        record_type=spec.record_type,
        semantic_key=semantic_key,
        payload=payload,
        authority_ref=grant_id(spec),
        scope_ref=SCOPE_REF,
        prerequisite_record_ids=prerequisites,
        predecessor_record_id=predecessor,
        observed_at=observed_at,
        expected_behavior="CORRECTNESS_CONTRACT_ENFORCED",
    )


def install_grants(kernel: GovernanceKernel) -> None:
    for spec in RECORD_SPECS:
        kernel.install_evidence_grant(
            grant_id=grant_id(spec),
            authority_type=spec.authority_type,
            holder_id=f"writer:{spec.workflow_id}",
            workflow_id=spec.workflow_id,
            record_type=spec.record_type,
            scope_ref=SCOPE_REF,
            evidence_ref=f"evidence-contract:{RUN_ID}",
        )


def require_outcome(result, expected: str, label: str) -> str:
    if result.outcome != expected:
        raise RuntimeError(f"{label}: expected {expected}, observed {result.outcome}")
    return result.record_id or ""


def build_initial_projection(kernel: GovernanceKernel) -> tuple[dict[str, str], dict[str, Any]]:
    record_ids: dict[str, str] = {}
    payloads: dict[str, dict[str, Any]] = {}
    for position, spec in enumerate(RECORD_SPECS, start=1):
        if spec.record_type in {
            "Registered Projection Rebuild Requirement",
            "Registered Projection Deletion Record",
        }:
            continue
        prerequisites = tuple(record_ids[item] for item in spec.prerequisite_types)
        payload = payload_for(spec, f"initial:{position:02d}")
        if spec.content_identity_source_type:
            payload = payloads[spec.content_identity_source_type]
        result = kernel.write(
            request_for(
                spec,
                attempt_id=f"{EXECUTION_ID}:initial:{position:02d}",
                semantic_key=f"semantic:initial:{position:02d}",
                payload=payload,
                prerequisites=prerequisites,
            )
        )
        record_ids[spec.record_type] = require_outcome(
            result, "ACCEPTED_EVIDENCE_ONLY", f"initial {spec.record_type}"
        )
        payloads[spec.record_type] = payload
    return record_ids, payloads


def run_projection_lifecycle(kernel: GovernanceKernel) -> dict[str, Any]:
    initial, _ = build_initial_projection(kernel)

    source_spec = spec_for("Registered Source Record")
    corrected_source = kernel.write(
        request_for(
            source_spec,
            attempt_id=f"{EXECUTION_ID}:correction:source",
            semantic_key="semantic:source:v2",
            payload=payload_for(source_spec, "corrected-source"),
            prerequisites=(initial["Registered Institution Registry Entry"],),
            predecessor=initial["Registered Source Record"],
        )
    )
    corrected_source_id = require_outcome(
        corrected_source, "ACCEPTED_EVIDENCE_ONLY", "source correction"
    )

    closure_spec = spec_for("Registered Dependency Closure Record")
    corrected_closure = kernel.write(
        request_for(
            closure_spec,
            attempt_id=f"{EXECUTION_ID}:correction:closure",
            semantic_key="semantic:closure:v2",
            payload=payload_for(closure_spec, "corrected-closure"),
            prerequisites=(
                corrected_source_id,
                initial["Registered Temporal Mapping Record"],
                initial["Registered Derived Record Envelope"],
            ),
            predecessor=initial["Registered Dependency Closure Record"],
        )
    )
    corrected_closure_id = require_outcome(
        corrected_closure, "ACCEPTED_EVIDENCE_ONLY", "closure correction"
    )

    completeness_spec = spec_for("Registered Closure Completeness Record")
    incomplete_payload = payload_for(
        completeness_spec,
        "incomplete-after-correction",
        candidate_overrides={"closure_completeness": "INCOMPLETE"},
    )
    incomplete = kernel.write(
        request_for(
            completeness_spec,
            attempt_id=f"{EXECUTION_ID}:correction:completeness",
            semantic_key="semantic:completeness:v2",
            payload=incomplete_payload,
            prerequisites=(corrected_closure_id,),
            predecessor=initial["Registered Closure Completeness Record"],
        )
    )
    incomplete_id = require_outcome(
        incomplete, "ACCEPTED_EVIDENCE_ONLY", "incomplete closure registration"
    )

    rebuild_spec = spec_for("Registered Projection Rebuild Requirement")
    rebuild_payload = payload_for(
        rebuild_spec,
        "rebuild-required",
        candidate_overrides={
            "closure_record_id": corrected_closure_id,
            "previous_publication_record_id": initial["Projection Publication Envelope"],
            "trigger_record_id": corrected_source_id,
        },
    )
    rebuild = kernel.write(
        request_for(
            rebuild_spec,
            attempt_id=f"{EXECUTION_ID}:projection:rebuild",
            semantic_key="semantic:projection:rebuild:v2",
            payload=rebuild_payload,
            prerequisites=(
                corrected_source_id,
                incomplete_id,
                initial["Projection Publication Envelope"],
            ),
        )
    )
    rebuild_id = require_outcome(rebuild, "ACCEPTED_EVIDENCE_ONLY", "rebuild requirement")

    audit_spec = spec_for("Registered Projection Change Audit Record")
    audit_prerequisites = (
        initial["Registered Temporal Mapping Record"],
        initial["Registered Derived Record Envelope"],
        corrected_closure_id,
        incomplete_id,
    )
    transition_fields = {
        "change_reason": "SOURCE_CORRECTION",
        "closure_completeness": "INCOMPLETE",
        "new_coordinate_digest": "coordinate:projection:v2",
        "previous_coordinate_digest": "coordinate:projection:v1",
        "previous_publication_record_id": initial["Projection Publication Envelope"],
    }
    invalid_payload = payload_for(
        audit_spec,
        "invalid-determinate",
        candidate_overrides={**transition_fields, "projection_result": "COMMITTED"},
    )
    invalid_audit = kernel.write(
        request_for(
            audit_spec,
            attempt_id=f"{EXECUTION_ID}:projection:invalid-determinate",
            semantic_key="transition:projection:stable:001:v1-to-v2",
            payload=invalid_payload,
            prerequisites=audit_prerequisites,
            predecessor=initial["Registered Projection Change Audit Record"],
        )
    )
    require_outcome(invalid_audit, "REJECTED_INVALID_PAYLOAD", "invalid determinate projection")

    audit_payload = payload_for(
        audit_spec,
        "valid-indeterminate",
        candidate_overrides={**transition_fields, "projection_result": "INDETERMINATE"},
    )
    successor_audit = kernel.write(
        request_for(
            audit_spec,
            attempt_id=f"{EXECUTION_ID}:projection:audit:v2",
            semantic_key="transition:projection:stable:001:v1-to-v2",
            payload=audit_payload,
            prerequisites=audit_prerequisites,
            predecessor=initial["Registered Projection Change Audit Record"],
        )
    )
    successor_audit_id = require_outcome(
        successor_audit, "ACCEPTED_EVIDENCE_ONLY", "successor audit"
    )

    conflict_payload = payload_for(
        audit_spec,
        "competing-indeterminate",
        candidate_overrides={**transition_fields, "projection_result": "INDETERMINATE"},
    )
    competing_audit = kernel.write(
        request_for(
            audit_spec,
            attempt_id=f"{EXECUTION_ID}:projection:audit:competing",
            semantic_key="transition:projection:stable:001:v1-to-v2",
            payload=conflict_payload,
            prerequisites=audit_prerequisites,
            predecessor=initial["Registered Projection Change Audit Record"],
        )
    )
    require_outcome(competing_audit, "CONFLICT_RECORDED", "competing transition")

    publication_spec = spec_for("Projection Publication Envelope")
    successor_publication = kernel.write(
        request_for(
            publication_spec,
            attempt_id=f"{EXECUTION_ID}:projection:publication:v2",
            semantic_key="semantic:projection:publication:v2",
            payload=audit_payload,
            prerequisites=(successor_audit_id,),
            predecessor=initial["Projection Publication Envelope"],
        )
    )
    successor_publication_id = require_outcome(
        successor_publication, "ACCEPTED_EVIDENCE_ONLY", "successor publication"
    )
    if successor_audit.payload_digest != successor_publication.payload_digest:
        raise RuntimeError("audit and publication business payload identity was not preserved")
    if successor_audit.content_digest == successor_publication.content_digest:
        raise RuntimeError("publication history metadata was not separated from business payload")

    mismatch_payload = payload_for(
        publication_spec,
        "publication-mismatch",
        candidate_overrides={**transition_fields, "projection_result": "CONFLICTED"},
    )
    mismatch = kernel.write(
        request_for(
            publication_spec,
            attempt_id=f"{EXECUTION_ID}:projection:publication:mismatch",
            semantic_key="semantic:projection:publication:mismatch",
            payload=mismatch_payload,
            prerequisites=(successor_audit_id,),
            predecessor=initial["Projection Publication Envelope"],
        )
    )
    require_outcome(
        mismatch, "REJECTED_CONTENT_IDENTITY_MISMATCH", "publication identity mismatch"
    )

    records_before_deletion = kernel.export_rows("protected_records")
    deletion_spec = spec_for("Registered Projection Deletion Record")
    deletion_payload = payload_for(
        deletion_spec,
        "delete-obsolete-cache",
        candidate_overrides={
            "rebuild_requirement_record_id": rebuild_id,
            "target_publication_record_id": initial["Projection Publication Envelope"],
        },
    )
    deletion = kernel.write(
        request_for(
            deletion_spec,
            attempt_id=f"{EXECUTION_ID}:projection:deletion",
            semantic_key="semantic:projection:deletion:v1",
            payload=deletion_payload,
            prerequisites=(initial["Projection Publication Envelope"], rebuild_id),
        )
    )
    deletion_id = require_outcome(
        deletion, "ACCEPTED_EVIDENCE_ONLY", "projection deletion record"
    )
    records_after_deletion = kernel.export_rows("protected_records")
    before_ids = {row["record_id"] for row in records_before_deletion}
    after_ids = {row["record_id"] for row in records_after_deletion}
    if not before_ids.issubset(after_ids) or len(after_ids) != len(before_ids) + 1:
        raise RuntimeError("deletion registration removed protected history")

    missing_rebuild = kernel.write(
        request_for(
            deletion_spec,
            attempt_id=f"{EXECUTION_ID}:projection:deletion:missing-rebuild",
            semantic_key="semantic:projection:deletion:missing-rebuild",
            payload=deletion_payload,
            prerequisites=(initial["Projection Publication Envelope"],),
        )
    )
    require_outcome(
        missing_rebuild, "REJECTED_MISSING_PREREQUISITE", "deletion without rebuild"
    )

    if not kernel.verify_event_chain():
        raise RuntimeError("projection lifecycle event chain verification failed")
    records = kernel.export_rows("protected_records")
    attempts = kernel.export_rows("write_attempts")
    type_counts = Counter(row["record_type"] for row in records)
    outcome_counts = Counter(row["outcome"] for row in attempts)
    return {
        "attempt_count": len(attempts),
        "protected_record_count": len(records),
        "conflict_count": len(kernel.export_rows("write_conflicts")),
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "record_type_counts": dict(sorted(type_counts.items())),
        "initial_publication_record_id": initial["Projection Publication Envelope"],
        "successor_publication_record_id": successor_publication_id,
        "rebuild_requirement_record_id": rebuild_id,
        "deletion_record_id": deletion_id,
        "audit_publication_payload_digest_equal": True,
        "audit_publication_content_digest_distinct": True,
        "noncomplete_determinate_projection_rejected": True,
        "same_transition_competitor_conflict_preserved": True,
        "publication_mismatch_rejected": True,
        "deletion_requires_rebuild": True,
        "protected_history_preserved_after_deletion": True,
        "event_hash_chain_verified": True,
        "result": "PASS",
    }


def export_signature(kernel: GovernanceKernel) -> tuple[str, dict[str, list[dict[str, Any]]]]:
    exported = {table: kernel.export_rows(table) for table in TABLES}
    return sha256_bytes(canonical_json(exported).encode("utf-8")), exported


def sqlite_checks(database_path: Path) -> dict[str, str]:
    connection = sqlite3.connect(database_path)
    try:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        journal_mode = connection.execute("PRAGMA journal_mode").fetchone()[0]
    finally:
        connection.close()
    return {"integrity_check": integrity, "journal_mode": journal_mode}


def run_replays(directory: Path, implementation_version: str) -> tuple[dict[str, Any], dict[str, Any]]:
    signatures: list[str] = []
    projection_summaries: list[dict[str, Any]] = []
    database_checks: dict[str, dict[str, str]] = {}
    reference_export: dict[str, Any] | None = None
    for index in range(1, REPLAY_COUNT + 1):
        database_path = directory / f"replay-{index:02d}.db"
        kernel = GovernanceKernel(database_path, implementation_version, clock=DeterministicClock())
        kernel.initialize()
        install_grants(kernel)
        projection_summaries.append(run_projection_lifecycle(kernel))
        signature, exported = export_signature(kernel)
        signatures.append(signature)
        if reference_export is None:
            reference_export = exported
        elif exported != reference_export:
            raise RuntimeError(f"replay {index:02d} differs from replay 01")
        kernel.checkpoint()
        database_checks[database_path.name] = sqlite_checks(database_path)
    if len(set(signatures)) != 1:
        raise RuntimeError("deterministic replay signatures differ")
    summary = {
        "execution_id": EXECUTION_ID,
        "replay_count": REPLAY_COUNT,
        "unique_signature_count": len(set(signatures)),
        "replay_signatures": signatures,
        "all_exported_rows_identical": True,
        "event_hash_chains_verified": True,
        "database_checks": database_checks,
        "result": "PASS",
    }
    return summary, projection_summaries[0]


def concurrency_request(
    spec,
    *,
    attempt_id: str,
    semantic_key: str,
    marker: str,
    execution_id: str,
) -> ProtectedWriteRequest:
    return request_for(
        spec,
        attempt_id=attempt_id,
        semantic_key=semantic_key,
        payload=payload_for(spec, marker),
        execution_id=execution_id,
        observed_at="2026-08-09T00:00:00.000000Z",
    )


def process_write(args: tuple[str, str, ProtectedWriteRequest]) -> tuple[str, str | None]:
    database_path, implementation_version, request = args
    kernel = GovernanceKernel(database_path, implementation_version)
    result = kernel.write(request)
    return result.outcome, result.record_id


def check_concurrency_case(
    database_path: Path,
    implementation_version: str,
    *,
    mode: str,
    distinct_payloads: bool,
    worker_count: int,
) -> dict[str, Any]:
    kernel = GovernanceKernel(database_path, implementation_version)
    kernel.initialize()
    install_grants(kernel)
    spec = RECORD_SPECS[0]
    execution_id = f"{RUN_ID}:concurrency:{mode}:{'conflict' if distinct_payloads else 'idempotent'}"
    requests = [
        concurrency_request(
            spec,
            attempt_id=f"{execution_id}:{index:02d}",
            semantic_key=f"semantic:{execution_id}",
            marker=f"candidate:{index:02d}" if distinct_payloads else "same-candidate",
            execution_id=execution_id,
        )
        for index in range(worker_count)
    ]
    if mode == "thread":
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            results = list(executor.map(kernel.write, requests))
        outcomes = [result.outcome for result in results]
        record_ids = [result.record_id for result in results]
    elif mode == "process":
        arguments = [(str(database_path), implementation_version, request) for request in requests]
        with ProcessPoolExecutor(max_workers=min(worker_count, os.cpu_count() or 1)) as executor:
            process_results = list(executor.map(process_write, arguments))
        outcomes = [outcome for outcome, _ in process_results]
        record_ids = [record_id for _, record_id in process_results]
    else:
        raise ValueError(mode)

    counts = Counter(outcomes)
    expected = (
        {"ACCEPTED_EVIDENCE_ONLY": 1, "CONFLICT_RECORDED": worker_count - 1}
        if distinct_payloads
        else {"ACCEPTED_EVIDENCE_ONLY": 1, "IDEMPOTENT_EXISTING": worker_count - 1}
    )
    if dict(counts) != expected:
        raise RuntimeError(f"unexpected {mode} concurrency outcomes: {dict(counts)}")
    if len(kernel.export_rows("protected_records")) != 1:
        raise RuntimeError(f"{mode} concurrency created more than one terminal record")
    expected_conflicts = worker_count - 1 if distinct_payloads else 0
    if len(kernel.export_rows("write_conflicts")) != expected_conflicts:
        raise RuntimeError(f"{mode} concurrency conflict count mismatch")
    if len({record_id for record_id in record_ids if record_id}) != 1:
        raise RuntimeError(f"{mode} concurrency did not converge on one record")
    if not kernel.verify_event_chain():
        raise RuntimeError(f"{mode} concurrency event chain verification failed")
    kernel.checkpoint()
    checks = sqlite_checks(database_path)
    return {
        "mode": mode,
        "scenario": "DISTINCT_PAYLOAD_CONFLICT" if distinct_payloads else "SAME_PAYLOAD_IDEMPOTENT",
        "worker_count": worker_count,
        "outcome_counts": dict(sorted(counts.items())),
        "protected_record_count": 1,
        "conflict_count": expected_conflicts,
        "single_terminal_assignment": True,
        "event_hash_chain_verified": True,
        "database_checks": checks,
        "result": "PASS",
    }


def run_concurrency(directory: Path, implementation_version: str) -> dict[str, Any]:
    cases = []
    for name, mode, distinct, workers in (
        ("thread-idempotent.db", "thread", False, THREAD_WORKERS),
        ("thread-conflict.db", "thread", True, THREAD_WORKERS),
        ("process-idempotent.db", "process", False, PROCESS_WORKERS),
        ("process-conflict.db", "process", True, PROCESS_WORKERS),
    ):
        cases.append(
            check_concurrency_case(
                directory / name,
                implementation_version,
                mode=mode,
                distinct_payloads=distinct,
                worker_count=workers,
            )
        )
    return {
        "case_count": len(cases),
        "thread_worker_count_per_case": THREAD_WORKERS,
        "process_worker_count_per_case": PROCESS_WORKERS,
        "cases": cases,
        "single_terminal_assignment_all_cases": True,
        "same_payload_idempotency_verified": True,
        "distinct_payload_conflict_preservation_verified": True,
        "result": "PASS",
    }


def run_unit_tests(directory: Path) -> dict[str, Any]:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            "-W",
            "error::ResourceWarning",
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-v",
        ],
        cwd=ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output_path = directory / "unit_test_output.txt"
    output_path.write_text(completed.stdout, encoding="utf-8", newline="\n")
    if completed.returncode != 0 or "Ran 14 tests" not in completed.stdout:
        raise RuntimeError("unit test execution failed or test count changed")
    return {
        "command": "python3 -W error::ResourceWarning -m unittest discover -s tests -v",
        "tests_run": 14,
        "failures": 0,
        "errors": 0,
        "resource_warnings": 0,
        "result": "PASS",
    }


def write_json(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")


def verify_package(target: Path) -> dict[str, Any]:
    manifest = json.loads((target / "manifest.json").read_text(encoding="utf-8"))
    expected_files = set(manifest["files"]) | {"manifest.json"}
    actual_files = {path.name for path in target.iterdir() if path.is_file()}
    if actual_files != expected_files:
        raise RuntimeError("evidence file set differs from manifest closure")
    for filename, expected_digest in manifest["files"].items():
        if sha256_file(target / filename) != expected_digest:
            raise RuntimeError(f"manifest digest mismatch: {filename}")
    sidecars = sorted(path.name for path in target.iterdir() if path.name.endswith(("-wal", "-shm")))
    if sidecars:
        raise RuntimeError(f"unmanifested SQLite sidecars: {sidecars}")
    database_checks = {
        path.name: sqlite_checks(path) for path in sorted(target.glob("*.db"))
    }
    if any(
        checks != {"integrity_check": "ok", "journal_mode": "delete"}
        for checks in database_checks.values()
    ):
        raise RuntimeError("final SQLite integrity or journal-mode check failed")
    return {
        "exact_file_closure": True,
        "manifest_digests_verified": True,
        "sqlite_sidecars_absent": True,
        "database_checks": database_checks,
        "result": "PASS",
    }


def run() -> Path:
    if TARGET.exists():
        raise FileExistsError(f"evidence package already exists: {TARGET}")
    EVIDENCE_PARENT.mkdir(parents=True, exist_ok=True)
    started_at = utc_now()
    code_digest = implementation_digest()
    test_harness_digest = harness_digest()
    implementation_version = f"governance-kernel/0.2.0+sha256:{code_digest}"

    with tempfile.TemporaryDirectory(prefix=f".{RUN_ID}-", dir=EVIDENCE_PARENT) as temporary_name:
        temporary = Path(temporary_name)
        unit_test_summary = run_unit_tests(temporary)
        replay_summary, projection_summary = run_replays(temporary, implementation_version)
        concurrency_summary = run_concurrency(temporary, implementation_version)
        completed_at = utc_now()

        input_manifest = {
            "execution_id": RUN_ID,
            "deterministic_execution_id": EXECUTION_ID,
            "implementation_version": implementation_version,
            "test_harness_digest": test_harness_digest,
            "runtime_mode": "NON_AUTHORITATIVE_CONFORMANCE",
            "authority_mode": "EVIDENCE_ONLY_TEST_GRANTS",
            "scope_ref": SCOPE_REF,
            "started_at": started_at,
            "formal_fact_creation": "PROHIBITED",
            "institution_freeze_creation": "PROHIBITED",
            "replay_count": REPLAY_COUNT,
            "thread_worker_count_per_case": THREAD_WORKERS,
            "process_worker_count_per_case": PROCESS_WORKERS,
        }
        summary = {
            "execution_id": RUN_ID,
            "implementation_version": implementation_version,
            "test_harness_digest": test_harness_digest,
            "started_at": started_at,
            "completed_at": completed_at,
            "unit_tests": unit_test_summary,
            "deterministic_replay": replay_summary,
            "concurrency": concurrency_summary,
            "projection_correctness": projection_summary,
            "formal_fact_created": False,
            "institution_freeze_created": False,
            "cross_provider_evidence_created": False,
            "cross_project_evidence_created": False,
            "cross_domain_evidence_created": False,
            "migration_evidence_created": False,
            "result": "PASS_AS_NON_AUTHORITATIVE_CORRECTNESS_EVIDENCE",
            "next_required_stage": "CROSS_CONTEXT_AND_MIGRATION_EVIDENCE",
        }
        write_json(temporary / "input_manifest.json", input_manifest)
        write_json(temporary / "unit_test_summary.json", unit_test_summary)
        write_json(temporary / "replay_summary.json", replay_summary)
        write_json(temporary / "concurrency_summary.json", concurrency_summary)
        write_json(temporary / "projection_summary.json", projection_summary)
        write_json(temporary / "summary.json", summary)

        package_files = sorted(path for path in temporary.iterdir() if path.is_file())
        file_digests = {path.name: sha256_file(path) for path in package_files}
        package_digest = sha256_bytes(
            "".join(
                f"{digest}  {name}\n" for name, digest in sorted(file_digests.items())
            ).encode("utf-8")
        )
        write_json(
            temporary / "manifest.json",
            {
                "algorithm": "SHA-256",
                "canonical_manifest": "digest + two spaces + filename + LF, sorted by filename",
                "files": file_digests,
                "package_digest": package_digest,
            },
        )
        os.replace(temporary, TARGET)

    for path in TARGET.iterdir():
        if path.is_file():
            path.chmod(0o444)
    verification = verify_package(TARGET)
    if verification["result"] != "PASS":
        raise RuntimeError("final evidence verification failed")
    return TARGET


if __name__ == "__main__":
    print(run())
