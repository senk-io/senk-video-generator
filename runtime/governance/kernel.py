"""Append-only protected-write kernel for non-authoritative conformance evidence."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

from .catalog import SPEC_BY_IDENTITY, RecordSpec


EVIDENCE_MODE = "NON_AUTHORITATIVE_CONFORMANCE"
GENESIS_HASH = "0" * 64


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class ProtectedWriteRequest:
    attempt_id: str
    execution_id: str
    principal_id: str
    workflow_id: str
    record_type: str
    semantic_key: str
    payload: dict[str, Any]
    authority_ref: str
    scope_ref: str
    prerequisite_record_ids: tuple[str, ...] = ()
    predecessor_record_id: str | None = None
    observed_at: str | None = None
    expected_behavior: str = "PROTECTED_WRITE_ENFORCED"


@dataclass(frozen=True, slots=True)
class ProtectedWriteResult:
    attempt_id: str
    outcome: str
    reason: str
    record_id: str | None
    payload_digest: str
    content_digest: str
    evidence_digest: str
    failure_closed_result: str


class AttemptIdentityConflict(RuntimeError):
    """Raised when one attempt identity is reused for different input."""


class GovernanceKernel:
    """A SQLite-backed, append-only evidence-mode protected-write boundary."""

    def __init__(
        self,
        database_path: str | Path,
        implementation_version: str,
        *,
        clock: Callable[[], str] = utc_now,
        mode: str = EVIDENCE_MODE,
    ) -> None:
        if mode != EVIDENCE_MODE:
            raise ValueError("formal runtime mode is unavailable before institution freeze")
        self.database_path = Path(database_path)
        self.implementation_version = implementation_version
        self.clock = clock
        self.mode = mode

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=30, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 30000")
        return connection

    def initialize(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection:
            connection.execute("PRAGMA journal_mode = WAL")
            connection.execute("PRAGMA synchronous = FULL")
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS runtime_metadata (
                    metadata_key TEXT PRIMARY KEY,
                    metadata_value TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS authority_grants (
                    grant_id TEXT PRIMARY KEY,
                    grant_version TEXT NOT NULL,
                    authority_type TEXT NOT NULL,
                    holder_id TEXT NOT NULL,
                    workflow_id TEXT NOT NULL,
                    record_type TEXT NOT NULL,
                    scope_ref TEXT NOT NULL,
                    evidence_ref TEXT NOT NULL,
                    evidence_mode TEXT NOT NULL CHECK (evidence_mode = 'NON_AUTHORITATIVE_CONFORMANCE'),
                    recorded_at TEXT NOT NULL,
                    payload_digest TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS protected_records (
                    record_id TEXT PRIMARY KEY,
                    workflow_id TEXT NOT NULL,
                    record_type TEXT NOT NULL,
                    semantic_key TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    payload_digest TEXT NOT NULL,
                    content_digest TEXT NOT NULL,
                    proposal_version TEXT NOT NULL,
                    proposal_digest TEXT NOT NULL,
                    authority_ref TEXT NOT NULL,
                    scope_ref TEXT NOT NULL,
                    prerequisite_record_ids_json TEXT NOT NULL,
                    predecessor_record_id TEXT,
                    execution_id TEXT NOT NULL,
                    observed_at TEXT NOT NULL,
                    recorded_at TEXT NOT NULL,
                    evidence_mode TEXT NOT NULL CHECK (evidence_mode = 'NON_AUTHORITATIVE_CONFORMANCE'),
                    UNIQUE (workflow_id, record_type, semantic_key),
                    FOREIGN KEY (predecessor_record_id) REFERENCES protected_records(record_id)
                );

                CREATE TABLE IF NOT EXISTS write_attempts (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    attempt_id TEXT NOT NULL UNIQUE,
                    request_digest TEXT NOT NULL,
                    execution_id TEXT NOT NULL,
                    implementation_version TEXT NOT NULL,
                    proposal_version TEXT NOT NULL,
                    proposal_digest TEXT NOT NULL,
                    principal_id TEXT NOT NULL,
                    workflow_id TEXT NOT NULL,
                    record_type TEXT NOT NULL,
                    semantic_key TEXT NOT NULL,
                    payload_digest TEXT NOT NULL,
                    content_digest TEXT NOT NULL,
                    authority_ref TEXT NOT NULL,
                    scope_ref TEXT NOT NULL,
                    input_refs_json TEXT NOT NULL,
                    output_ref TEXT,
                    outcome TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    expected_behavior TEXT NOT NULL,
                    observed_behavior TEXT NOT NULL,
                    failure_closed_result TEXT NOT NULL,
                    observed_at TEXT NOT NULL,
                    recorded_at TEXT NOT NULL,
                    previous_event_hash TEXT NOT NULL,
                    event_body_json TEXT NOT NULL,
                    event_hash TEXT NOT NULL UNIQUE,
                    evidence_mode TEXT NOT NULL CHECK (evidence_mode = 'NON_AUTHORITATIVE_CONFORMANCE')
                );

                CREATE TABLE IF NOT EXISTS write_conflicts (
                    conflict_id TEXT PRIMARY KEY,
                    attempt_id TEXT NOT NULL UNIQUE,
                    existing_record_id TEXT NOT NULL,
                    workflow_id TEXT NOT NULL,
                    record_type TEXT NOT NULL,
                    semantic_key TEXT NOT NULL,
                    existing_payload_digest TEXT NOT NULL,
                    competing_payload_digest TEXT NOT NULL,
                    existing_content_digest TEXT NOT NULL,
                    competing_content_digest TEXT NOT NULL,
                    recorded_at TEXT NOT NULL,
                    evidence_mode TEXT NOT NULL CHECK (evidence_mode = 'NON_AUTHORITATIVE_CONFORMANCE'),
                    FOREIGN KEY (attempt_id) REFERENCES write_attempts(attempt_id),
                    FOREIGN KEY (existing_record_id) REFERENCES protected_records(record_id)
                );
                """
            )
            for table_name in (
                "runtime_metadata",
                "authority_grants",
                "protected_records",
                "write_attempts",
                "write_conflicts",
            ):
                connection.executescript(
                    f"""
                    CREATE TRIGGER IF NOT EXISTS {table_name}_reject_update
                    BEFORE UPDATE ON {table_name}
                    BEGIN
                        SELECT RAISE(ABORT, 'append_only_violation');
                    END;
                    CREATE TRIGGER IF NOT EXISTS {table_name}_reject_delete
                    BEFORE DELETE ON {table_name}
                    BEGIN
                        SELECT RAISE(ABORT, 'append_only_violation');
                    END;
                    """
                )
            metadata = {
                "implementation_version": self.implementation_version,
                "runtime_mode": self.mode,
                "formal_fact_creation": "PROHIBITED",
            }
            for key, value in metadata.items():
                connection.execute(
                    "INSERT OR IGNORE INTO runtime_metadata(metadata_key, metadata_value) VALUES (?, ?)",
                    (key, value),
                )
                stored = connection.execute(
                    "SELECT metadata_value FROM runtime_metadata WHERE metadata_key = ?", (key,)
                ).fetchone()
                if stored is None or stored["metadata_value"] != value:
                    raise RuntimeError(f"runtime metadata mismatch for {key}")

    def install_evidence_grant(
        self,
        *,
        grant_id: str,
        authority_type: str,
        holder_id: str,
        workflow_id: str,
        record_type: str,
        scope_ref: str,
        evidence_ref: str,
        grant_version: str = "evidence-only-v1",
    ) -> str:
        grant_payload = {
            "grant_id": grant_id,
            "grant_version": grant_version,
            "authority_type": authority_type,
            "holder_id": holder_id,
            "workflow_id": workflow_id,
            "record_type": record_type,
            "scope_ref": scope_ref,
            "evidence_ref": evidence_ref,
            "evidence_mode": self.mode,
        }
        payload_digest = sha256_text(canonical_json(grant_payload))
        recorded_at = self.clock()
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            existing = connection.execute(
                "SELECT payload_digest FROM authority_grants WHERE grant_id = ?", (grant_id,)
            ).fetchone()
            if existing is not None:
                if existing["payload_digest"] != payload_digest:
                    connection.execute("ROLLBACK")
                    raise ValueError("authority grant identity conflict")
                connection.execute("COMMIT")
                return payload_digest
            connection.execute(
                """
                INSERT INTO authority_grants(
                    grant_id, grant_version, authority_type, holder_id, workflow_id,
                    record_type, scope_ref, evidence_ref, evidence_mode, recorded_at,
                    payload_digest
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    grant_id,
                    grant_version,
                    authority_type,
                    holder_id,
                    workflow_id,
                    record_type,
                    scope_ref,
                    evidence_ref,
                    self.mode,
                    recorded_at,
                    payload_digest,
                ),
            )
            connection.execute("COMMIT")
        return payload_digest

    def write(self, request: ProtectedWriteRequest) -> ProtectedWriteResult:
        observed_at = request.observed_at or self.clock()
        recorded_at = self.clock()
        payload_json = canonical_json(request.payload)
        content_json = canonical_json(
            {
                "payload": request.payload,
                "predecessor_record_id": request.predecessor_record_id,
            }
        )
        payload_digest = sha256_text(payload_json)
        content_digest = sha256_text(content_json)
        request_body = {
            "attempt_id": request.attempt_id,
            "execution_id": request.execution_id,
            "principal_id": request.principal_id,
            "workflow_id": request.workflow_id,
            "record_type": request.record_type,
            "semantic_key": request.semantic_key,
            "payload_digest": payload_digest,
            "content_digest": content_digest,
            "authority_ref": request.authority_ref,
            "scope_ref": request.scope_ref,
            "prerequisite_record_ids": sorted(request.prerequisite_record_ids),
            "predecessor_record_id": request.predecessor_record_id,
            "observed_at": observed_at,
            "expected_behavior": request.expected_behavior,
        }
        request_digest = sha256_text(canonical_json(request_body))

        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            existing_attempt = connection.execute(
                "SELECT * FROM write_attempts WHERE attempt_id = ?", (request.attempt_id,)
            ).fetchone()
            if existing_attempt is not None:
                if existing_attempt["request_digest"] != request_digest:
                    connection.execute("ROLLBACK")
                    raise AttemptIdentityConflict(request.attempt_id)
                connection.execute("COMMIT")
                return self._result_from_attempt(existing_attempt)

            spec = SPEC_BY_IDENTITY.get((request.workflow_id, request.record_type))
            if spec is None:
                return self._finish_attempt(
                    connection,
                    request,
                    request_digest,
                    payload_digest,
                    observed_at,
                    recorded_at,
                    proposal_version="UNREGISTERED_TYPE",
                    proposal_digest=GENESIS_HASH,
                    outcome="REJECTED_UNKNOWN_TYPE",
                    reason="record type is not present in the reviewed protected-write catalog",
                    record_id=None,
                    failure_closed_result="ENFORCED",
                )

            validation_error = self._validate_payload(request.payload, spec)
            if validation_error:
                return self._finish_attempt(
                    connection,
                    request,
                    request_digest,
                    payload_digest,
                    observed_at,
                    recorded_at,
                    spec.proposal_version,
                    spec.proposal_digest,
                    "REJECTED_INVALID_PAYLOAD",
                    validation_error,
                    None,
                    "ENFORCED",
                )

            authority = connection.execute(
                """
                SELECT grant_id FROM authority_grants
                WHERE grant_id = ? AND authority_type = ? AND holder_id = ?
                  AND workflow_id = ? AND record_type = ? AND scope_ref = ?
                  AND evidence_mode = ?
                """,
                (
                    request.authority_ref,
                    spec.authority_type,
                    request.principal_id,
                    request.workflow_id,
                    request.record_type,
                    request.scope_ref,
                    self.mode,
                ),
            ).fetchone()
            if authority is None:
                return self._finish_attempt(
                    connection,
                    request,
                    request_digest,
                    payload_digest,
                    observed_at,
                    recorded_at,
                    spec.proposal_version,
                    spec.proposal_digest,
                    "REJECTED_UNAUTHORIZED",
                    "no exact holder, authority type, record type and scope grant",
                    None,
                    "ENFORCED",
                )

            prerequisites = self._load_prerequisites(connection, request.prerequisite_record_ids)
            missing_types = self._missing_prerequisite_types(spec, prerequisites, request.scope_ref)
            if missing_types:
                return self._finish_attempt(
                    connection,
                    request,
                    request_digest,
                    payload_digest,
                    observed_at,
                    recorded_at,
                    spec.proposal_version,
                    spec.proposal_digest,
                    "REJECTED_MISSING_PREREQUISITE",
                    "missing exact registered prerequisite types: " + ", ".join(missing_types),
                    None,
                    "ENFORCED",
                )

            prerequisite_consistency_error = self._validate_prerequisite_consistency(
                spec, request.payload, prerequisites
            )
            if prerequisite_consistency_error:
                return self._finish_attempt(
                    connection,
                    request,
                    request_digest,
                    payload_digest,
                    observed_at,
                    recorded_at,
                    spec.proposal_version,
                    spec.proposal_digest,
                    "REJECTED_PREREQUISITE_CONTENT_MISMATCH",
                    prerequisite_consistency_error,
                    None,
                    "ENFORCED",
                )

            predecessor_error = self._validate_predecessor(connection, request, spec)
            if predecessor_error:
                return self._finish_attempt(
                    connection,
                    request,
                    request_digest,
                    payload_digest,
                    observed_at,
                    recorded_at,
                    spec.proposal_version,
                    spec.proposal_digest,
                    "REJECTED_INVALID_PREDECESSOR",
                    predecessor_error,
                    None,
                    "ENFORCED",
                )

            existing_record = connection.execute(
                """
                SELECT * FROM protected_records
                WHERE workflow_id = ? AND record_type = ? AND semantic_key = ?
                """,
                (request.workflow_id, request.record_type, request.semantic_key),
            ).fetchone()
            if existing_record is not None:
                if existing_record["content_digest"] == content_digest:
                    return self._finish_attempt(
                        connection,
                        request,
                        request_digest,
                        payload_digest,
                        observed_at,
                        recorded_at,
                        spec.proposal_version,
                        spec.proposal_digest,
                        "IDEMPOTENT_EXISTING",
                        "same semantic key and content-identical payload already registered",
                        existing_record["record_id"],
                        "ENFORCED",
                    )
                conflict_id = f"conflict:{request.attempt_id}"
                result = self._finish_attempt(
                    connection,
                    request,
                    request_digest,
                    payload_digest,
                    observed_at,
                    recorded_at,
                    spec.proposal_version,
                    spec.proposal_digest,
                    "CONFLICT_RECORDED",
                    "same semantic key has a different payload digest; original record preserved",
                    existing_record["record_id"],
                    "ENFORCED",
                    commit=False,
                )
                connection.execute(
                    """
                    INSERT INTO write_conflicts(
                        conflict_id, attempt_id, existing_record_id, workflow_id,
                        record_type, semantic_key, existing_payload_digest,
                        competing_payload_digest, existing_content_digest,
                        competing_content_digest, recorded_at, evidence_mode
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        conflict_id,
                        request.attempt_id,
                        existing_record["record_id"],
                        request.workflow_id,
                        request.record_type,
                        request.semantic_key,
                        existing_record["payload_digest"],
                        payload_digest,
                        existing_record["content_digest"],
                        content_digest,
                        recorded_at,
                        self.mode,
                    ),
                )
                connection.execute("COMMIT")
                return result

            identity_error = self._validate_content_identity(spec, prerequisites, payload_digest)
            if identity_error:
                return self._finish_attempt(
                    connection,
                    request,
                    request_digest,
                    payload_digest,
                    observed_at,
                    recorded_at,
                    spec.proposal_version,
                    spec.proposal_digest,
                    "REJECTED_CONTENT_IDENTITY_MISMATCH",
                    identity_error,
                    None,
                    "ENFORCED",
                )

            record_seed = canonical_json(
                {
                    "workflow_id": request.workflow_id,
                    "record_type": request.record_type,
                    "semantic_key": request.semantic_key,
                    "content_digest": content_digest,
                }
            )
            record_id = f"record:{request.workflow_id}:{sha256_text(record_seed)[:24]}"
            connection.execute(
                """
                INSERT INTO protected_records(
                    record_id, workflow_id, record_type, semantic_key, payload_json,
                    payload_digest, content_digest, proposal_version, proposal_digest, authority_ref,
                    scope_ref, prerequisite_record_ids_json, predecessor_record_id,
                    execution_id, observed_at, recorded_at, evidence_mode
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record_id,
                    request.workflow_id,
                    request.record_type,
                    request.semantic_key,
                    payload_json,
                    payload_digest,
                    content_digest,
                    spec.proposal_version,
                    spec.proposal_digest,
                    request.authority_ref,
                    request.scope_ref,
                    canonical_json(sorted(request.prerequisite_record_ids)),
                    request.predecessor_record_id,
                    request.execution_id,
                    observed_at,
                    recorded_at,
                    self.mode,
                ),
            )
            return self._finish_attempt(
                connection,
                request,
                request_digest,
                payload_digest,
                observed_at,
                recorded_at,
                spec.proposal_version,
                spec.proposal_digest,
                "ACCEPTED_EVIDENCE_ONLY",
                "exact evidence-mode authority, scope, prerequisites and content checks satisfied",
                record_id,
                "ENFORCED",
            )

    @staticmethod
    def _validate_payload(payload: dict[str, Any], spec: RecordSpec) -> str | None:
        required_fields = {
            "candidate_payload",
            "evidence_mode",
            "institution_freeze_ref",
            "knowledge_boundary",
            "proposal_ref",
            "result",
            "temporal_coordinate",
        }
        missing = sorted(required_fields.difference(payload))
        if missing:
            return "missing required payload fields: " + ", ".join(missing)
        if payload["evidence_mode"] != EVIDENCE_MODE:
            return "formal or unknown evidence mode is prohibited"
        if payload["institution_freeze_ref"] != "NOT_CREATED_EVIDENCE_ONLY":
            return "unverified institution freeze reference is prohibited"
        if payload["proposal_ref"] != spec.proposal_version:
            return "payload proposal reference does not match the protected-write catalog"
        candidate_payload = payload["candidate_payload"]
        if not isinstance(candidate_payload, dict):
            return "candidate_payload must be an object"
        missing_candidate_fields = sorted(
            set(spec.required_candidate_fields).difference(candidate_payload)
        )
        if missing_candidate_fields:
            return "missing required candidate payload fields: " + ", ".join(
                missing_candidate_fields
            )
        if spec.record_type in {
            "Registered Projection Change Audit Record",
            "Projection Publication Envelope",
        }:
            projection_result = candidate_payload["projection_result"]
            if projection_result not in {
                "ABORTED",
                "COMMITTED",
                "CONFLICTED",
                "INDETERMINATE",
            }:
                return "projection result is outside the reviewed result algebra"
            if (
                candidate_payload["closure_completeness"] != "COMPLETE"
                and projection_result not in {"CONFLICTED", "INDETERMINATE"}
            ):
                return "non-complete closure cannot support a determinate projection"
            previous_publication = candidate_payload["previous_publication_record_id"]
            previous_coordinate = candidate_payload["previous_coordinate_digest"]
            if previous_publication == "CANONICAL_BOOTSTRAP_MARKER":
                if previous_coordinate != "NOT_APPLICABLE":
                    return "bootstrap transition must use NOT_APPLICABLE previous coordinate"
            elif previous_coordinate == "NOT_APPLICABLE":
                return "successor transition must pin the previous coordinate digest"
        return None

    @staticmethod
    def _load_prerequisites(
        connection: sqlite3.Connection, prerequisite_record_ids: Iterable[str]
    ) -> list[sqlite3.Row]:
        records: list[sqlite3.Row] = []
        for record_id in sorted(set(prerequisite_record_ids)):
            record = connection.execute(
                "SELECT * FROM protected_records WHERE record_id = ?", (record_id,)
            ).fetchone()
            if record is not None:
                records.append(record)
        return records

    @staticmethod
    def _missing_prerequisite_types(
        spec: RecordSpec, prerequisites: list[sqlite3.Row], scope_ref: str
    ) -> list[str]:
        present_types = {
            record["record_type"]
            for record in prerequisites
            if record["scope_ref"] == scope_ref
        }
        return sorted(set(spec.prerequisite_types).difference(present_types))

    @staticmethod
    def _validate_prerequisite_consistency(
        spec: RecordSpec, payload: dict[str, Any], prerequisites: list[sqlite3.Row]
    ) -> str | None:
        candidate_payload = payload["candidate_payload"]
        if spec.record_type == "Registered Projection Change Audit Record":
            completeness_records = [
                record
                for record in prerequisites
                if record["record_type"] == "Registered Closure Completeness Record"
            ]
            if len(completeness_records) != 1:
                return "projection audit requires exactly one closure completeness record"
            completeness_payload = json.loads(completeness_records[0]["payload_json"])
            registered_value = completeness_payload["candidate_payload"].get(
                "closure_completeness"
            )
            claimed_value = candidate_payload["closure_completeness"]
            if registered_value != claimed_value:
                return "projection closure completeness claim differs from its registered prerequisite"
        elif spec.record_type == "Registered Projection Rebuild Requirement":
            by_type = {record["record_type"]: record for record in prerequisites}
            if (
                candidate_payload["trigger_record_id"]
                != by_type["Registered Source Record"]["record_id"]
            ):
                return "rebuild trigger record differs from the registered source prerequisite"
            if (
                candidate_payload["previous_publication_record_id"]
                != by_type["Projection Publication Envelope"]["record_id"]
            ):
                return "rebuild predecessor differs from the publication prerequisite"
            completeness = by_type["Registered Closure Completeness Record"]
            closure_ids = json.loads(completeness["prerequisite_record_ids_json"])
            if candidate_payload["closure_record_id"] not in closure_ids:
                return "rebuild closure differs from the completeness prerequisite lineage"
        elif spec.record_type == "Registered Projection Deletion Record":
            by_type = {record["record_type"]: record for record in prerequisites}
            if (
                candidate_payload["target_publication_record_id"]
                != by_type["Projection Publication Envelope"]["record_id"]
            ):
                return "deletion target differs from the publication prerequisite"
            if (
                candidate_payload["rebuild_requirement_record_id"]
                != by_type["Registered Projection Rebuild Requirement"]["record_id"]
            ):
                return "deletion rebuild reference differs from the registered prerequisite"
        return None

    @staticmethod
    def _validate_predecessor(
        connection: sqlite3.Connection,
        request: ProtectedWriteRequest,
        spec: RecordSpec,
    ) -> str | None:
        if request.predecessor_record_id is None:
            return None
        if not spec.allow_correction:
            return "this record type does not allow correction successors"
        predecessor = connection.execute(
            "SELECT * FROM protected_records WHERE record_id = ?",
            (request.predecessor_record_id,),
        ).fetchone()
        if predecessor is None:
            return "predecessor record does not exist"
        if (
            predecessor["workflow_id"] != request.workflow_id
            or predecessor["record_type"] != request.record_type
            or predecessor["scope_ref"] != request.scope_ref
        ):
            return "predecessor workflow, record type or scope mismatch"
        if predecessor["semantic_key"] == request.semantic_key:
            return "correction must use a new semantic key"
        return None

    @staticmethod
    def _validate_content_identity(
        spec: RecordSpec, prerequisites: list[sqlite3.Row], payload_digest: str
    ) -> str | None:
        if spec.content_identity_source_type is None:
            return None
        source_records = [
            record
            for record in prerequisites
            if record["record_type"] == spec.content_identity_source_type
        ]
        if len(source_records) != 1:
            return "exactly one content-identity source record is required"
        if source_records[0]["payload_digest"] != payload_digest:
            return "publication payload digest differs from the registered audit payload digest"
        return None

    def _finish_attempt(
        self,
        connection: sqlite3.Connection,
        request: ProtectedWriteRequest,
        request_digest: str,
        payload_digest: str,
        observed_at: str,
        recorded_at: str,
        proposal_version: str,
        proposal_digest: str,
        outcome: str,
        reason: str,
        record_id: str | None,
        failure_closed_result: str,
        *,
        commit: bool = True,
    ) -> ProtectedWriteResult:
        content_digest = sha256_text(
            canonical_json(
                {
                    "payload": request.payload,
                    "predecessor_record_id": request.predecessor_record_id,
                }
            )
        )
        previous = connection.execute(
            "SELECT event_hash FROM write_attempts ORDER BY sequence DESC LIMIT 1"
        ).fetchone()
        previous_event_hash = previous["event_hash"] if previous else GENESIS_HASH
        input_refs = sorted(
            set(request.prerequisite_record_ids)
            | ({request.predecessor_record_id} if request.predecessor_record_id else set())
        )
        event_body = {
            "attempt_id": request.attempt_id,
            "execution_id": request.execution_id,
            "implementation_version": self.implementation_version,
            "proposal_version": proposal_version,
            "proposal_digest": proposal_digest,
            "principal_id": request.principal_id,
            "workflow_id": request.workflow_id,
            "record_type": request.record_type,
            "semantic_key": request.semantic_key,
            "payload_digest": payload_digest,
            "content_digest": content_digest,
            "authority_ref": request.authority_ref,
            "scope_ref": request.scope_ref,
            "input_refs": input_refs,
            "output_ref": record_id,
            "outcome": outcome,
            "reason": reason,
            "expected_behavior": request.expected_behavior,
            "observed_behavior": outcome,
            "failure_closed_result": failure_closed_result,
            "observed_at": observed_at,
            "recorded_at": recorded_at,
            "evidence_mode": self.mode,
        }
        event_body_json = canonical_json(event_body)
        event_hash = sha256_text(previous_event_hash + "\n" + event_body_json)
        connection.execute(
            """
            INSERT INTO write_attempts(
                attempt_id, request_digest, execution_id, implementation_version,
                proposal_version, proposal_digest, principal_id, workflow_id,
                record_type, semantic_key, payload_digest, content_digest, authority_ref, scope_ref,
                input_refs_json, output_ref, outcome, reason, expected_behavior,
                observed_behavior, failure_closed_result, observed_at, recorded_at,
                previous_event_hash, event_body_json, event_hash, evidence_mode
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request.attempt_id,
                request_digest,
                request.execution_id,
                self.implementation_version,
                proposal_version,
                proposal_digest,
                request.principal_id,
                request.workflow_id,
                request.record_type,
                request.semantic_key,
                payload_digest,
                content_digest,
                request.authority_ref,
                request.scope_ref,
                canonical_json(input_refs),
                record_id,
                outcome,
                reason,
                request.expected_behavior,
                outcome,
                failure_closed_result,
                observed_at,
                recorded_at,
                previous_event_hash,
                event_body_json,
                event_hash,
                self.mode,
            ),
        )
        if commit:
            connection.execute("COMMIT")
        return ProtectedWriteResult(
            attempt_id=request.attempt_id,
            outcome=outcome,
            reason=reason,
            record_id=record_id,
            payload_digest=payload_digest,
            content_digest=content_digest,
            evidence_digest=event_hash,
            failure_closed_result=failure_closed_result,
        )

    @staticmethod
    def _result_from_attempt(attempt: sqlite3.Row) -> ProtectedWriteResult:
        return ProtectedWriteResult(
            attempt_id=attempt["attempt_id"],
            outcome=attempt["outcome"],
            reason=attempt["reason"],
            record_id=attempt["output_ref"],
            payload_digest=attempt["payload_digest"],
            content_digest=attempt["content_digest"],
            evidence_digest=attempt["event_hash"],
            failure_closed_result=attempt["failure_closed_result"],
        )

    def verify_event_chain(self) -> bool:
        previous_event_hash = GENESIS_HASH
        with closing(self._connect()) as connection:
            attempts = connection.execute(
                "SELECT * FROM write_attempts ORDER BY sequence"
            ).fetchall()
        for attempt in attempts:
            if attempt["previous_event_hash"] != previous_event_hash:
                return False
            expected_hash = sha256_text(previous_event_hash + "\n" + attempt["event_body_json"])
            if attempt["event_hash"] != expected_hash:
                return False
            previous_event_hash = attempt["event_hash"]
        return True

    def export_rows(self, table_name: str) -> list[dict[str, Any]]:
        allowed_tables = {
            "authority_grants",
            "protected_records",
            "runtime_metadata",
            "write_attempts",
            "write_conflicts",
        }
        if table_name not in allowed_tables:
            raise ValueError("table is not exportable")
        order_column = {
            "authority_grants": "grant_id",
            "protected_records": "record_id",
            "runtime_metadata": "metadata_key",
            "write_attempts": "sequence",
            "write_conflicts": "conflict_id",
        }[table_name]
        with closing(self._connect()) as connection:
            rows = connection.execute(
                f"SELECT * FROM {table_name} ORDER BY {order_column}"
            ).fetchall()
        return [dict(row) for row in rows]

    def checkpoint(self) -> None:
        with closing(self._connect()) as connection:
            connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            connection.execute("PRAGMA journal_mode = DELETE")
