#!/usr/bin/env python3
"""Create one write-once protected-write evidence package for all nine workstreams."""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.governance import (
    GovernanceKernel,
    PROPOSAL_DIGESTS,
    ProtectedWriteRequest,
    RECORD_SPECS,
)


RUN_ID = os.environ.get("GOVERNANCE_EVIDENCE_RUN_ID", "CR-0014-PW-004")
SUPERSEDES_RUN_ID = os.environ.get("GOVERNANCE_EVIDENCE_SUPERSEDES", "CR-0014-PW-003")
SCOPE_REF = "scope:evidence:nine-workstreams"
EVIDENCE_PARENT = ROOT / "evidence" / "runtime"
TARGET = EVIDENCE_PARENT / RUN_ID


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


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def implementation_digest() -> str:
    source_paths = (
        ROOT / "runtime" / "governance" / "catalog.py",
        ROOT / "runtime" / "governance" / "kernel.py",
        ROOT / "tools" / "run_protected_write_evidence.py",
    )
    manifest_lines = [f"{sha256_file(path)}  {path.relative_to(ROOT)}\n" for path in source_paths]
    return sha256_bytes("".join(sorted(manifest_lines)).encode("utf-8"))


def payload_for(spec, marker: str = "accepted") -> dict[str, Any]:
    return {
        "candidate_payload": {"marker": marker, "scope": SCOPE_REF},
        "evidence_mode": "NON_AUTHORITATIVE_CONFORMANCE",
        "institution_freeze_ref": "NOT_CREATED_EVIDENCE_ONLY",
        "knowledge_boundary": f"K:{RUN_ID}",
        "proposal_ref": spec.proposal_version,
        "result": "EVIDENCE_ONLY",
        "temporal_coordinate": {"Q": RUN_ID, "S": "evidence-subject", "RR": "evidence-rr"},
    }


def write_new_json(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))
        stream.write("\n")


def write_new_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(canonical_json(row))
            stream.write("\n")


def request_for(
    spec,
    index: int,
    *,
    attempt_kind: str,
    semantic_key: str,
    payload: dict[str, Any],
    prerequisite_record_ids: tuple[str, ...] = (),
    principal_id: str | None = None,
    predecessor_record_id: str | None = None,
    scope_ref: str = SCOPE_REF,
) -> ProtectedWriteRequest:
    return ProtectedWriteRequest(
        attempt_id=f"{RUN_ID}:{attempt_kind}:{index:02d}",
        execution_id=RUN_ID,
        principal_id=principal_id or f"writer:{spec.workflow_id}",
        workflow_id=spec.workflow_id,
        record_type=spec.record_type,
        semantic_key=semantic_key,
        payload=payload,
        authority_ref=f"grant:{RUN_ID}:{index:02d}",
        scope_ref=scope_ref,
        prerequisite_record_ids=prerequisite_record_ids,
        predecessor_record_id=predecessor_record_id,
        observed_at=utc_now(),
        expected_behavior=attempt_kind.upper(),
    )


def run() -> Path:
    if TARGET.exists():
        raise FileExistsError(f"evidence package already exists: {TARGET}")
    EVIDENCE_PARENT.mkdir(parents=True, exist_ok=True)
    started_at = utc_now()
    code_digest = implementation_digest()
    implementation_version = f"governance-kernel/0.1.0+sha256:{code_digest}"

    with tempfile.TemporaryDirectory(prefix=f".{RUN_ID}-", dir=EVIDENCE_PARENT) as temporary_name:
        temporary = Path(temporary_name)
        database_path = temporary / "governance.db"
        kernel = GovernanceKernel(database_path, implementation_version)
        kernel.initialize()

        for index, spec in enumerate(RECORD_SPECS, start=1):
            kernel.install_evidence_grant(
                grant_id=f"grant:{RUN_ID}:{index:02d}",
                authority_type=spec.authority_type,
                holder_id=f"writer:{spec.workflow_id}",
                workflow_id=spec.workflow_id,
                record_type=spec.record_type,
                scope_ref=SCOPE_REF,
                evidence_ref=f"evidence-contract:{RUN_ID}",
            )

        for index, spec in enumerate(RECORD_SPECS, start=1):
            kernel.write(
                request_for(
                    spec,
                    index,
                    attempt_kind="unauthorized",
                    semantic_key=f"semantic:{index:02d}",
                    payload=payload_for(spec),
                    principal_id="intruder:no-grant",
                )
            )
            if spec.prerequisite_types:
                kernel.write(
                    request_for(
                        spec,
                        index,
                        attempt_kind="missing-prerequisite",
                        semantic_key=f"semantic:{index:02d}",
                        payload=payload_for(spec),
                    )
                )

        first_spec = RECORD_SPECS[0]
        kernel.write(
            request_for(
                first_spec,
                1,
                attempt_kind="scope-mismatch",
                semantic_key="semantic:scope-mismatch",
                payload=payload_for(first_spec),
                scope_ref="scope:evidence:wrong",
            )
        )
        formal_payload = payload_for(first_spec)
        formal_payload["evidence_mode"] = "FORMAL"
        kernel.write(
            request_for(
                first_spec,
                1,
                attempt_kind="formal-mode-rejected",
                semantic_key="semantic:formal-mode",
                payload=formal_payload,
            )
        )
        kernel.write(
            ProtectedWriteRequest(
                attempt_id=f"{RUN_ID}:unknown-type:00",
                execution_id=RUN_ID,
                principal_id="writer:unknown",
                workflow_id="WS-00",
                record_type="Unknown Protected Record",
                semantic_key="semantic:unknown",
                payload=payload_for(first_spec),
                authority_ref="grant:unknown",
                scope_ref=SCOPE_REF,
                observed_at=utc_now(),
                expected_behavior="UNKNOWN_TYPE_REJECTED",
            )
        )

        record_ids: dict[str, str] = {}
        payloads: dict[str, dict[str, Any]] = {}
        accepted_results = {}
        for index, spec in enumerate(RECORD_SPECS, start=1):
            prerequisite_ids = tuple(record_ids[item] for item in spec.prerequisite_types)
            payload = payload_for(spec)
            if spec.content_identity_source_type:
                payload = payloads[spec.content_identity_source_type]
            accepted = kernel.write(
                request_for(
                    spec,
                    index,
                    attempt_kind="accepted",
                    semantic_key=f"semantic:{index:02d}",
                    payload=payload,
                    prerequisite_record_ids=prerequisite_ids,
                )
            )
            if accepted.outcome != "ACCEPTED_EVIDENCE_ONLY" or accepted.record_id is None:
                raise RuntimeError(f"accepted path failed for {spec.workflow_id}: {accepted.outcome}")
            record_ids[spec.record_type] = accepted.record_id
            payloads[spec.record_type] = payload
            accepted_results[spec.record_type] = accepted

            idempotent = kernel.write(
                request_for(
                    spec,
                    index,
                    attempt_kind="idempotent",
                    semantic_key=f"semantic:{index:02d}",
                    payload=payload,
                    prerequisite_record_ids=prerequisite_ids,
                )
            )
            if idempotent.outcome != "IDEMPOTENT_EXISTING":
                raise RuntimeError(f"idempotent path failed for {spec.workflow_id}: {idempotent.outcome}")

            conflict_payload = payload_for(spec, "conflicting")
            conflict = kernel.write(
                request_for(
                    spec,
                    index,
                    attempt_kind="conflict",
                    semantic_key=f"semantic:{index:02d}",
                    payload=conflict_payload,
                    prerequisite_record_ids=prerequisite_ids,
                )
            )
            if conflict.outcome != "CONFLICT_RECORDED":
                raise RuntimeError(f"conflict path failed for {spec.workflow_id}: {conflict.outcome}")

        source_index = next(
            index
            for index, spec in enumerate(RECORD_SPECS, start=1)
            if spec.record_type == "Registered Source Record"
        )
        source_spec = RECORD_SPECS[source_index - 1]
        source_first = accepted_results[source_spec.record_type]
        source_prerequisites = tuple(record_ids[item] for item in source_spec.prerequisite_types)
        correction = kernel.write(
            request_for(
                source_spec,
                source_index,
                attempt_kind="correction",
                semantic_key="semantic:source:correction:v2",
                payload=payload_for(source_spec, "corrected"),
                prerequisite_record_ids=source_prerequisites,
                predecessor_record_id=source_first.record_id,
            )
        )
        if correction.outcome != "ACCEPTED_EVIDENCE_ONLY":
            raise RuntimeError(f"correction path failed: {correction.outcome}")

        publication_index = next(
            index
            for index, spec in enumerate(RECORD_SPECS, start=1)
            if spec.record_type == "Projection Publication Envelope"
        )
        publication_spec = RECORD_SPECS[publication_index - 1]
        publication_mismatch = kernel.write(
            request_for(
                publication_spec,
                publication_index,
                attempt_kind="publication-content-mismatch",
                semantic_key="semantic:publication:mismatch",
                payload=payload_for(publication_spec, "different-from-audit"),
                prerequisite_record_ids=(record_ids["Registered Projection Change Audit Record"],),
            )
        )
        if publication_mismatch.outcome != "REJECTED_CONTENT_IDENTITY_MISMATCH":
            raise RuntimeError(
                f"publication content identity guard failed: {publication_mismatch.outcome}"
            )

        if not kernel.verify_event_chain():
            raise RuntimeError("event hash chain verification failed")

        immutability_checks: list[dict[str, str]] = []
        target_record_id = accepted_results[RECORD_SPECS[0].record_type].record_id
        connection = sqlite3.connect(database_path, isolation_level=None)
        try:
            for operation, statement in (
                (
                    "UPDATE_REJECTED",
                    "UPDATE protected_records SET semantic_key = 'forbidden' WHERE record_id = ?",
                ),
                ("DELETE_REJECTED", "DELETE FROM protected_records WHERE record_id = ?"),
            ):
                try:
                    connection.execute(statement, (target_record_id,))
                except sqlite3.IntegrityError as error:
                    if "append_only_violation" not in str(error):
                        raise
                    immutability_checks.append(
                        {"operation": operation, "observed": str(error), "result": "ENFORCED"}
                    )
                else:
                    raise RuntimeError(f"append-only guard did not reject {operation}")
        finally:
            connection.close()

        kernel.checkpoint()
        attempts = kernel.export_rows("write_attempts")
        records = kernel.export_rows("protected_records")
        conflicts = kernel.export_rows("write_conflicts")
        grants = kernel.export_rows("authority_grants")
        outcome_counts = Counter(row["outcome"] for row in attempts)
        completed_at = utc_now()

        expected_outcomes = {
            "ACCEPTED_EVIDENCE_ONLY": len(RECORD_SPECS) + 1,
            "CONFLICT_RECORDED": len(RECORD_SPECS),
            "IDEMPOTENT_EXISTING": len(RECORD_SPECS),
            "REJECTED_CONTENT_IDENTITY_MISMATCH": 1,
            "REJECTED_INVALID_PAYLOAD": 1,
            "REJECTED_MISSING_PREREQUISITE": sum(bool(spec.prerequisite_types) for spec in RECORD_SPECS),
            "REJECTED_UNAUTHORIZED": len(RECORD_SPECS) + 1,
            "REJECTED_UNKNOWN_TYPE": 1,
        }
        if dict(sorted(outcome_counts.items())) != dict(sorted(expected_outcomes.items())):
            raise RuntimeError(f"unexpected outcome counts: {dict(outcome_counts)}")

        input_manifest = {
            "execution_id": RUN_ID,
            "supersedes_execution_id": SUPERSEDES_RUN_ID,
            "supersession_reason": "final evidence packaging switched from WAL to DELETE journaling to prevent unmanifested read sidecars",
            "implementation_version": implementation_version,
            "institution_proposal_versions": sorted({spec.proposal_version for spec in RECORD_SPECS}),
            "proposal_digests": PROPOSAL_DIGESTS,
            "authority_mode": "EVIDENCE_ONLY_TEST_GRANTS",
            "scope_ref": SCOPE_REF,
            "started_at": started_at,
            "formal_fact_creation": "PROHIBITED",
            "next_evidence_stage": "TEST_REPLAY_CONCURRENCY_PROJECTION_CORRECTNESS",
        }
        summary = {
            "execution_id": RUN_ID,
            "implementation_version": implementation_version,
            "started_at": started_at,
            "completed_at": completed_at,
            "workstreams_covered": sorted({spec.workflow_id for spec in RECORD_SPECS}),
            "protected_record_types_covered": len(RECORD_SPECS),
            "attempt_count": len(attempts),
            "accepted_record_count": len(records),
            "conflict_count": len(conflicts),
            "outcome_counts": dict(sorted(outcome_counts.items())),
            "unauthorized_write_rejected": True,
            "scope_mismatch_rejected": True,
            "formal_mode_rejected": True,
            "unknown_type_rejected": True,
            "missing_prerequisite_rejected": True,
            "same_key_same_payload_idempotent": True,
            "same_key_different_payload_conflict_preserved": True,
            "terminal_record_overwrite_prevented": True,
            "correction_history_preserved": True,
            "projection_publication_content_identical": True,
            "projection_publication_mismatch_rejected": True,
            "append_only_update_delete_guards": True,
            "event_hash_chain_verified": True,
            "formal_fact_created": False,
            "institution_freeze_created": False,
            "supersedes_execution_id": SUPERSEDES_RUN_ID,
            "result": "PASS_AS_NON_AUTHORITATIVE_PROTECTED_WRITE_EVIDENCE",
        }

        write_new_json(temporary / "input_manifest.json", input_manifest)
        write_new_jsonl(temporary / "authority_grants.jsonl", grants)
        write_new_jsonl(temporary / "write_attempts.jsonl", attempts)
        write_new_jsonl(temporary / "protected_records.jsonl", records)
        write_new_jsonl(temporary / "write_conflicts.jsonl", conflicts)
        write_new_json(temporary / "immutability_checks.json", immutability_checks)
        write_new_json(temporary / "summary.json", summary)

        package_files = sorted(path for path in temporary.iterdir() if path.is_file())
        file_digests = {path.name: sha256_file(path) for path in package_files}
        package_digest = sha256_bytes(
            "".join(f"{digest}  {name}\n" for name, digest in sorted(file_digests.items())).encode("utf-8")
        )
        manifest = {
            "algorithm": "SHA-256",
            "canonical_manifest": "digest + two spaces + filename + LF, sorted by filename",
            "files": file_digests,
            "package_digest": package_digest,
        }
        write_new_json(temporary / "manifest.json", manifest)

        os.replace(temporary, TARGET)

    for path in TARGET.iterdir():
        if path.is_file():
            path.chmod(0o444)
    return TARGET


if __name__ == "__main__":
    evidence_path = run()
    print(evidence_path)
