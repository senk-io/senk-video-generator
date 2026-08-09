#!/usr/bin/env python3
"""生成 0.1 到 0.2 的非权威迁移证据包。"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.governance import GovernanceKernel, ProtectedWriteRequest, RECORD_SPECS
from runtime.governance.migration import migrate_v01_to_v02


RUN_ID = os.environ.get("GOVERNANCE_MIGRATION_RUN_ID", "CR-0016-MIGRATION-001")
SOURCE_RUN_ID = "CR-0014-PW-004"
SOURCE_PACKAGE = ROOT / "evidence" / "runtime" / SOURCE_RUN_ID
SOURCE_DATABASE = SOURCE_PACKAGE / "governance.db"
TARGET = ROOT / "evidence" / "runtime" / RUN_ID
SCOPE_REF = "scope:evidence:nine-workstreams"
EXECUTION_ID = f"{RUN_ID}:post-migration-write"


class DeterministicClock:
    def __init__(self) -> None:
        self.base = datetime(2026, 8, 9, 9, tzinfo=timezone.utc)
        self.ticks = 0

    def __call__(self) -> str:
        self.ticks += 1
        value = self.base + timedelta(microseconds=self.ticks)
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


def migration_harness_digest() -> str:
    return source_digest(
        (
            ROOT / "runtime" / "governance" / "migration.py",
            ROOT / "migration_tests" / "test_v01_to_v02_migration.py",
            ROOT / "tools" / "run_migration_evidence.py",
        )
    )


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def spec_for(record_type: str):
    return next(spec for spec in RECORD_SPECS if spec.record_type == record_type)


def legacy_grant_id(spec) -> str:
    return f"grant:{SOURCE_RUN_ID}:{RECORD_SPECS.index(spec) + 1:02d}"


def grant_id(spec) -> str:
    if spec.record_type in {
        "Registered Projection Rebuild Requirement",
        "Registered Projection Deletion Record",
    }:
        return f"grant:{RUN_ID}:{RECORD_SPECS.index(spec) + 1:02d}"
    return legacy_grant_id(spec)


def payload_for(
    spec,
    marker: str,
    *,
    candidate_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidate: dict[str, Any] = {"marker": marker, "scope": SCOPE_REF}
    if spec.record_type == "Registered Closure Completeness Record":
        candidate["closure_completeness"] = "INCOMPLETE"
    elif spec.record_type in {
        "Registered Projection Change Audit Record",
        "Projection Publication Envelope",
    }:
        candidate.update(
            {
                "change_reason": "SCHEMA_MIGRATION_AND_SOURCE_CORRECTION",
                "closure_completeness": "INCOMPLETE",
                "new_coordinate_digest": "coordinate:migrated:v2",
                "previous_coordinate_digest": "LEGACY_COORDINATE_UNAVAILABLE",
                "previous_publication_record_id": "PENDING",
                "projection_result": "INDETERMINATE",
                "projection_stable_key": "projection:migration:stable:001",
                "transition_rule_version": "transition-rule:v1",
                "view_mode": "AS_KNOWN_AT_K",
            }
        )
    elif spec.record_type == "Registered Projection Rebuild Requirement":
        candidate.update(
            {
                "closure_record_id": "PENDING",
                "impact_scope": "projection:migration:stable:001",
                "new_coordinate_digest": "coordinate:migrated:v2",
                "previous_coordinate_digest": "LEGACY_COORDINATE_UNAVAILABLE",
                "previous_publication_record_id": "PENDING",
                "recovery_path": "PATH_A_NEW_SUPPORT",
                "trigger_record_id": "PENDING",
            }
        )
    elif spec.record_type == "Registered Projection Deletion Record":
        candidate.update(
            {
                "cache_object_id": "cache:projection:migration:legacy",
                "deletion_reason": "SCHEMA_MIGRATION_REBUILD",
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
        "knowledge_boundary": f"K:{RUN_ID}",
        "proposal_ref": spec.proposal_version,
        "result": "EVIDENCE_ONLY",
        "temporal_coordinate": {
            "Q": RUN_ID,
            "RR": "migration-evidence",
            "S": "migration-subject",
        },
    }


def request_for(
    spec,
    clock: DeterministicClock,
    *,
    attempt: str,
    semantic_key: str,
    payload: dict[str, Any],
    prerequisites: tuple[str, ...] = (),
    predecessor: str | None = None,
) -> ProtectedWriteRequest:
    return ProtectedWriteRequest(
        attempt_id=f"{EXECUTION_ID}:{attempt}",
        execution_id=EXECUTION_ID,
        principal_id=f"writer:{spec.workflow_id}",
        workflow_id=spec.workflow_id,
        record_type=spec.record_type,
        semantic_key=semantic_key,
        payload=payload,
        authority_ref=grant_id(spec),
        scope_ref=SCOPE_REF,
        prerequisite_record_ids=prerequisites,
        predecessor_record_id=predecessor,
        observed_at=clock(),
        expected_behavior="POST_MIGRATION_CONTRACT_ENFORCED",
    )


def require_outcome(result, expected: str, label: str) -> str:
    if result.outcome != expected:
        raise RuntimeError(f"{label}: expected {expected}, observed {result.outcome}")
    return result.record_id or ""


def sqlite_checks(path: Path) -> dict[str, Any]:
    connection = sqlite3.connect(path)
    try:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        foreign_key_failures = len(connection.execute("PRAGMA foreign_key_check").fetchall())
        journal_mode = connection.execute("PRAGMA journal_mode").fetchone()[0]
        user_version = connection.execute("PRAGMA user_version").fetchone()[0]
    finally:
        connection.close()
    return {
        "integrity_check": integrity,
        "foreign_key_failure_count": foreign_key_failures,
        "journal_mode": journal_mode,
        "user_version": user_version,
    }


def run_migration_tests(directory: Path) -> dict[str, Any]:
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
            "migration_tests",
            "-v",
        ],
        cwd=ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    (directory / "migration_test_output.txt").write_text(
        completed.stdout, encoding="utf-8", newline="\n"
    )
    if completed.returncode != 0 or "Ran 1 test" not in completed.stdout:
        raise RuntimeError("migration test execution failed")
    return {
        "tests_run": 1,
        "failures": 0,
        "errors": 0,
        "resource_warnings": 0,
        "result": "PASS",
    }


def exercise_current_runtime(
    database_path: Path,
    implementation_version: str,
    clock: DeterministicClock,
) -> dict[str, Any]:
    kernel = GovernanceKernel(database_path, implementation_version, clock=clock)
    kernel.initialize()
    for spec in RECORD_SPECS:
        if spec.record_type not in {
            "Registered Projection Rebuild Requirement",
            "Registered Projection Deletion Record",
        }:
            continue
        kernel.install_evidence_grant(
            grant_id=grant_id(spec),
            authority_type=spec.authority_type,
            holder_id=f"writer:{spec.workflow_id}",
            workflow_id=spec.workflow_id,
            record_type=spec.record_type,
            scope_ref=SCOPE_REF,
            evidence_ref=f"migration-evidence:{RUN_ID}",
        )

    records = kernel.export_rows("protected_records")
    by_type: dict[str, list[dict[str, Any]]] = {}
    for record in sorted(records, key=lambda row: (row["recorded_at"], row["record_id"])):
        by_type.setdefault(record["record_type"], []).append(record)

    institution = by_type["Registered Institution Registry Entry"][0]
    legacy_source = by_type["Registered Source Record"][-1]
    temporal = by_type["Registered Temporal Mapping Record"][0]
    derived = by_type["Registered Derived Record Envelope"][0]
    legacy_closure = by_type["Registered Dependency Closure Record"][0]
    legacy_completeness = by_type["Registered Closure Completeness Record"][0]
    legacy_audit = by_type["Registered Projection Change Audit Record"][0]
    legacy_publication = by_type["Projection Publication Envelope"][0]

    institution_spec = spec_for("Registered Institution Registry Entry")
    legacy_idempotent = kernel.write(
        request_for(
            institution_spec,
            clock,
            attempt="legacy-idempotent",
            semantic_key=institution["semantic_key"],
            payload=json.loads(institution["payload_json"]),
        )
    )
    require_outcome(legacy_idempotent, "IDEMPOTENT_EXISTING", "legacy idempotency")

    source_spec = spec_for("Registered Source Record")
    source = kernel.write(
        request_for(
            source_spec,
            clock,
            attempt="source-successor",
            semantic_key="semantic:migration:source:v3",
            payload=payload_for(source_spec, "post-migration-source"),
            prerequisites=(institution["record_id"],),
            predecessor=legacy_source["record_id"],
        )
    )
    source_id = require_outcome(source, "ACCEPTED_EVIDENCE_ONLY", "source successor")

    closure_spec = spec_for("Registered Dependency Closure Record")
    closure = kernel.write(
        request_for(
            closure_spec,
            clock,
            attempt="closure-successor",
            semantic_key="semantic:migration:closure:v2",
            payload=payload_for(closure_spec, "post-migration-closure"),
            prerequisites=(source_id, temporal["record_id"], derived["record_id"]),
            predecessor=legacy_closure["record_id"],
        )
    )
    closure_id = require_outcome(closure, "ACCEPTED_EVIDENCE_ONLY", "closure successor")

    completeness_spec = spec_for("Registered Closure Completeness Record")
    completeness = kernel.write(
        request_for(
            completeness_spec,
            clock,
            attempt="completeness-successor",
            semantic_key="semantic:migration:completeness:v2",
            payload=payload_for(completeness_spec, "post-migration-incomplete"),
            prerequisites=(closure_id,),
            predecessor=legacy_completeness["record_id"],
        )
    )
    completeness_id = require_outcome(
        completeness, "ACCEPTED_EVIDENCE_ONLY", "completeness successor"
    )

    rebuild_spec = spec_for("Registered Projection Rebuild Requirement")
    rebuild_payload = payload_for(
        rebuild_spec,
        "post-migration-rebuild",
        candidate_overrides={
            "closure_record_id": closure_id,
            "previous_publication_record_id": legacy_publication["record_id"],
            "trigger_record_id": source_id,
        },
    )
    rebuild = kernel.write(
        request_for(
            rebuild_spec,
            clock,
            attempt="rebuild-requirement",
            semantic_key="semantic:migration:rebuild:v2",
            payload=rebuild_payload,
            prerequisites=(source_id, completeness_id, legacy_publication["record_id"]),
        )
    )
    rebuild_id = require_outcome(rebuild, "ACCEPTED_EVIDENCE_ONLY", "rebuild requirement")

    audit_spec = spec_for("Registered Projection Change Audit Record")
    audit_payload = payload_for(
        audit_spec,
        "post-migration-audit",
        candidate_overrides={
            "previous_publication_record_id": legacy_publication["record_id"]
        },
    )
    audit = kernel.write(
        request_for(
            audit_spec,
            clock,
            attempt="projection-audit-successor",
            semantic_key="transition:migration:legacy-to-v2",
            payload=audit_payload,
            prerequisites=(
                temporal["record_id"],
                derived["record_id"],
                closure_id,
                completeness_id,
            ),
            predecessor=legacy_audit["record_id"],
        )
    )
    audit_id = require_outcome(audit, "ACCEPTED_EVIDENCE_ONLY", "audit successor")

    publication_spec = spec_for("Projection Publication Envelope")
    publication = kernel.write(
        request_for(
            publication_spec,
            clock,
            attempt="projection-publication-successor",
            semantic_key="semantic:migration:publication:v2",
            payload=audit_payload,
            prerequisites=(audit_id,),
            predecessor=legacy_publication["record_id"],
        )
    )
    publication_id = require_outcome(
        publication, "ACCEPTED_EVIDENCE_ONLY", "publication successor"
    )
    if audit.payload_digest != publication.payload_digest:
        raise RuntimeError("post-migration audit/publication payload identity mismatch")

    deletion_spec = spec_for("Registered Projection Deletion Record")
    deletion_payload = payload_for(
        deletion_spec,
        "post-migration-delete-legacy-cache",
        candidate_overrides={
            "rebuild_requirement_record_id": rebuild_id,
            "target_publication_record_id": legacy_publication["record_id"],
        },
    )
    deletion = kernel.write(
        request_for(
            deletion_spec,
            clock,
            attempt="projection-deletion",
            semantic_key="semantic:migration:deletion:legacy",
            payload=deletion_payload,
            prerequisites=(legacy_publication["record_id"], rebuild_id),
        )
    )
    deletion_id = require_outcome(deletion, "ACCEPTED_EVIDENCE_ONLY", "deletion record")

    missing_rebuild = kernel.write(
        request_for(
            deletion_spec,
            clock,
            attempt="projection-deletion-missing-rebuild",
            semantic_key="semantic:migration:deletion:missing-rebuild",
            payload=deletion_payload,
            prerequisites=(legacy_publication["record_id"],),
        )
    )
    require_outcome(
        missing_rebuild,
        "REJECTED_MISSING_PREREQUISITE",
        "post-migration deletion without rebuild",
    )

    if not kernel.verify_event_chain():
        raise RuntimeError("mixed-version event chain verification failed")
    kernel.checkpoint()
    final_records = kernel.export_rows("protected_records")
    final_attempts = kernel.export_rows("write_attempts")
    return {
        "legacy_idempotency_verified": True,
        "post_migration_accepted_record_count": 7,
        "post_migration_negative_attempt_count": 1,
        "total_protected_record_count": len(final_records),
        "total_attempt_count": len(final_attempts),
        "total_conflict_count": len(kernel.export_rows("write_conflicts")),
        "outcome_counts": dict(sorted(Counter(row["outcome"] for row in final_attempts).items())),
        "source_successor_record_id": source_id,
        "closure_successor_record_id": closure_id,
        "completeness_successor_record_id": completeness_id,
        "rebuild_requirement_record_id": rebuild_id,
        "audit_successor_record_id": audit_id,
        "publication_successor_record_id": publication_id,
        "deletion_record_id": deletion_id,
        "legacy_history_preserved": all(
            any(row["record_id"] == legacy["record_id"] for row in final_records)
            for legacy in (
                legacy_source,
                legacy_closure,
                legacy_completeness,
                legacy_audit,
                legacy_publication,
            )
        ),
        "audit_publication_payload_identity": True,
        "mixed_version_event_chain_verified": True,
        "result": "PASS",
    }


def write_json(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")


def run() -> Path:
    if TARGET.exists():
        raise FileExistsError(TARGET)
    started_at = utc_now()
    source_manifest = json.loads((SOURCE_PACKAGE / "manifest.json").read_text(encoding="utf-8"))
    code_digest = implementation_digest()
    harness_digest = migration_harness_digest()
    implementation_version = f"governance-kernel/0.2.0+sha256:{code_digest}"
    source_database_digest_before = sha256_file(SOURCE_DATABASE)
    clock = DeterministicClock()

    with tempfile.TemporaryDirectory(
        prefix=f".{RUN_ID}-", dir=TARGET.parent
    ) as temporary_name:
        temporary = Path(temporary_name)
        test_summary = run_migration_tests(temporary)
        migrated_database = temporary / "migrated.db"
        migration_summary = migrate_v01_to_v02(
            SOURCE_DATABASE,
            migrated_database,
            target_implementation_version=implementation_version,
            migration_execution_id=RUN_ID,
            clock=clock,
        )
        runtime_summary = exercise_current_runtime(
            migrated_database, implementation_version, clock
        )
        database_checks = sqlite_checks(migrated_database)
        if database_checks != {
            "integrity_check": "ok",
            "foreign_key_failure_count": 0,
            "journal_mode": "delete",
            "user_version": 2,
        }:
            raise RuntimeError(f"unexpected migrated database checks: {database_checks}")
        source_database_digest_after = sha256_file(SOURCE_DATABASE)
        if source_database_digest_after != source_database_digest_before:
            raise RuntimeError("source database changed during evidence execution")
        completed_at = utc_now()

        input_manifest = {
            "execution_id": RUN_ID,
            "source_execution_id": SOURCE_RUN_ID,
            "source_package_digest": source_manifest["package_digest"],
            "source_database_digest": source_database_digest_before,
            "source_database_path": str(SOURCE_DATABASE.relative_to(ROOT)),
            "source_implementation_version": migration_summary[
                "source_implementation_version"
            ],
            "target_implementation_version": implementation_version,
            "migration_harness_digest": harness_digest,
            "runtime_mode": "NON_AUTHORITATIVE_CONFORMANCE",
            "formal_fact_creation": "PROHIBITED",
            "institution_freeze_creation": "PROHIBITED",
            "started_at": started_at,
        }
        summary = {
            "execution_id": RUN_ID,
            "started_at": started_at,
            "completed_at": completed_at,
            "source_execution_id": SOURCE_RUN_ID,
            "source_package_digest": source_manifest["package_digest"],
            "source_database_digest_before": source_database_digest_before,
            "source_database_digest_after": source_database_digest_after,
            "target_implementation_version": implementation_version,
            "migration_harness_digest": harness_digest,
            "migration_tests": test_summary,
            "migration": migration_summary,
            "post_migration_runtime": runtime_summary,
            "database_checks": database_checks,
            "formal_fact_created": False,
            "institution_freeze_created": False,
            "migration_evidence_result": "PASS_FOR_REVIEWED_0_1_TO_0_2_PATH",
            "cross_provider_evidence_created": False,
            "cross_project_evidence_created": False,
            "cross_domain_evidence_created": False,
            "result": "PASS_AS_NON_AUTHORITATIVE_MIGRATION_EVIDENCE",
            "next_required_stage": "EXTERNAL_CROSS_CONTEXT_EVIDENCE",
        }
        write_json(temporary / "input_manifest.json", input_manifest)
        write_json(temporary / "migration_test_summary.json", test_summary)
        write_json(temporary / "migration_summary.json", migration_summary)
        write_json(temporary / "post_migration_runtime_summary.json", runtime_summary)
        write_json(temporary / "summary.json", summary)

        files = sorted(path for path in temporary.iterdir() if path.is_file())
        file_digests = {path.name: sha256_file(path) for path in files}
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
    return TARGET


if __name__ == "__main__":
    print(run())
