from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from runtime.governance import GovernanceKernel, ProtectedWriteRequest, RECORD_SPECS


class SequenceClock:
    def __init__(self) -> None:
        self.value = 0

    def __call__(self) -> str:
        self.value += 1
        return f"2026-08-09T00:00:{self.value:02d}.000000Z"


class GovernanceKernelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_directory.name) / "governance.db"
        self.kernel = GovernanceKernel(
            self.database_path,
            "governance-kernel/test",
            clock=SequenceClock(),
        )
        self.kernel.initialize()
        self.scope_ref = "scope:test"
        for index, spec in enumerate(RECORD_SPECS, start=1):
            self.kernel.install_evidence_grant(
                grant_id=f"grant:{index:02d}",
                authority_type=spec.authority_type,
                holder_id=f"writer:{spec.workflow_id}",
                workflow_id=spec.workflow_id,
                record_type=spec.record_type,
                scope_ref=self.scope_ref,
                evidence_ref="test-fixture",
            )

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    @staticmethod
    def payload(spec, marker: str = "accepted") -> dict[str, object]:
        candidate_payload: dict[str, object] = {"marker": marker}
        if spec.record_type == "Registered Closure Completeness Record":
            candidate_payload["closure_completeness"] = "COMPLETE"
        elif spec.record_type in {
            "Registered Projection Change Audit Record",
            "Projection Publication Envelope",
        }:
            candidate_payload.update(
                {
                    "change_reason": "INITIAL_PUBLICATION",
                    "closure_completeness": "COMPLETE",
                    "new_coordinate_digest": "coordinate:test:v1",
                    "previous_coordinate_digest": "NOT_APPLICABLE",
                    "previous_publication_record_id": "CANONICAL_BOOTSTRAP_MARKER",
                    "projection_result": "COMMITTED",
                    "projection_stable_key": "projection:test",
                    "transition_rule_version": "transition-rule:v1",
                    "view_mode": "AS_KNOWN_AT_K",
                }
            )
        elif spec.record_type == "Registered Projection Rebuild Requirement":
            candidate_payload.update(
                {
                    "closure_record_id": "closure:test",
                    "impact_scope": "projection:test",
                    "new_coordinate_digest": "coordinate:test:v2",
                    "previous_coordinate_digest": "coordinate:test:v1",
                    "previous_publication_record_id": "publication:test:v1",
                    "recovery_path": "PATH_A_NEW_SUPPORT",
                    "trigger_record_id": "source:test:v2",
                }
            )
        elif spec.record_type == "Registered Projection Deletion Record":
            candidate_payload.update(
                {
                    "cache_object_id": "cache:projection:test",
                    "deletion_reason": "REBUILD_REQUIRED",
                    "rebuild_requirement_record_id": "rebuild:test:v1",
                    "target_publication_record_id": "publication:test:v1",
                }
            )
        return {
            "candidate_payload": candidate_payload,
            "evidence_mode": "NON_AUTHORITATIVE_CONFORMANCE",
            "institution_freeze_ref": "NOT_CREATED_EVIDENCE_ONLY",
            "knowledge_boundary": "K:test",
            "proposal_ref": spec.proposal_version,
            "result": "EVIDENCE_ONLY",
            "temporal_coordinate": {"Q": "test", "S": "subject", "RR": "rr"},
        }

    def request(
        self,
        spec,
        attempt_id: str,
        semantic_key: str,
        payload: dict[str, object],
        prerequisites: tuple[str, ...] = (),
        *,
        principal_id: str | None = None,
        predecessor_record_id: str | None = None,
    ) -> ProtectedWriteRequest:
        spec_index = RECORD_SPECS.index(spec) + 1
        return ProtectedWriteRequest(
            attempt_id=attempt_id,
            execution_id="test-execution",
            principal_id=principal_id or f"writer:{spec.workflow_id}",
            workflow_id=spec.workflow_id,
            record_type=spec.record_type,
            semantic_key=semantic_key,
            payload=payload,
            authority_ref=f"grant:{spec_index:02d}",
            scope_ref=self.scope_ref,
            prerequisite_record_ids=prerequisites,
            predecessor_record_id=predecessor_record_id,
        )

    def build_chain(self) -> dict[str, str]:
        record_ids: dict[str, str] = {}
        payloads: dict[str, dict[str, object]] = {}
        for index, spec in enumerate(RECORD_SPECS, start=1):
            prerequisite_ids = tuple(record_ids[item] for item in spec.prerequisite_types)
            payload = self.payload(spec)
            if spec.content_identity_source_type:
                payload = payloads[spec.content_identity_source_type]
            elif spec.record_type == "Registered Projection Rebuild Requirement":
                candidate = payload["candidate_payload"]
                candidate["closure_record_id"] = record_ids["Registered Dependency Closure Record"]
                candidate["previous_publication_record_id"] = record_ids[
                    "Projection Publication Envelope"
                ]
                candidate["trigger_record_id"] = record_ids["Registered Source Record"]
            elif spec.record_type == "Registered Projection Deletion Record":
                candidate = payload["candidate_payload"]
                candidate["rebuild_requirement_record_id"] = record_ids[
                    "Registered Projection Rebuild Requirement"
                ]
                candidate["target_publication_record_id"] = record_ids[
                    "Projection Publication Envelope"
                ]
            result = self.kernel.write(
                self.request(
                    spec,
                    f"chain:{index:02d}",
                    f"semantic:{index:02d}",
                    payload,
                    prerequisite_ids,
                )
            )
            self.assertEqual("ACCEPTED_EVIDENCE_ONLY", result.outcome)
            self.assertIsNotNone(result.record_id)
            record_ids[spec.record_type] = result.record_id or ""
            payloads[spec.record_type] = payload
        return record_ids

    def test_catalog_covers_all_nine_workflows(self) -> None:
        self.assertEqual({f"WS-{index:02d}" for index in range(1, 10)}, {s.workflow_id for s in RECORD_SPECS})

    def test_unauthorized_write_is_rejected(self) -> None:
        spec = RECORD_SPECS[0]
        result = self.kernel.write(
            self.request(
                spec,
                "unauthorized:01",
                "semantic:unauthorized",
                self.payload(spec),
                principal_id="intruder",
            )
        )
        self.assertEqual("REJECTED_UNAUTHORIZED", result.outcome)
        self.assertEqual("ENFORCED", result.failure_closed_result)

    def test_missing_prerequisite_is_rejected(self) -> None:
        spec = RECORD_SPECS[1]
        result = self.kernel.write(
            self.request(spec, "missing:01", "semantic:missing", self.payload(spec))
        )
        self.assertEqual("REJECTED_MISSING_PREREQUISITE", result.outcome)

    def test_full_chain_and_publication_content_identity(self) -> None:
        record_ids = self.build_chain()
        self.assertIn("Projection Publication Envelope", record_ids)
        rows = self.kernel.export_rows("protected_records")
        audit = next(row for row in rows if row["record_type"] == "Registered Projection Change Audit Record")
        publication = next(row for row in rows if row["record_type"] == "Projection Publication Envelope")
        self.assertEqual(audit["payload_digest"], publication["payload_digest"])

    def test_same_key_same_payload_is_idempotent_and_different_payload_conflicts(self) -> None:
        spec = RECORD_SPECS[0]
        request = self.request(spec, "initial:01", "semantic:stable", self.payload(spec))
        initial = self.kernel.write(request)
        replay = self.kernel.write(
            self.request(spec, "replay:01", "semantic:stable", self.payload(spec))
        )
        conflict = self.kernel.write(
            self.request(spec, "conflict:01", "semantic:stable", self.payload(spec, "different"))
        )
        self.assertEqual("ACCEPTED_EVIDENCE_ONLY", initial.outcome)
        self.assertEqual("IDEMPOTENT_EXISTING", replay.outcome)
        self.assertEqual(initial.record_id, replay.record_id)
        self.assertEqual("CONFLICT_RECORDED", conflict.outcome)
        self.assertEqual(1, len(self.kernel.export_rows("protected_records")))
        self.assertEqual(1, len(self.kernel.export_rows("write_conflicts")))

    def test_correction_adds_successor_without_overwriting_history(self) -> None:
        spec = RECORD_SPECS[0]
        first = self.kernel.write(
            self.request(spec, "history:01", "semantic:v1", self.payload(spec, "v1"))
        )
        second = self.kernel.write(
            self.request(
                spec,
                "history:02",
                "semantic:v2",
                self.payload(spec, "v2"),
                predecessor_record_id=first.record_id,
            )
        )
        self.assertEqual("ACCEPTED_EVIDENCE_ONLY", second.outcome)
        rows = self.kernel.export_rows("protected_records")
        self.assertEqual(2, len(rows))
        successor = next(row for row in rows if row["record_id"] == second.record_id)
        self.assertEqual(first.record_id, successor["predecessor_record_id"])

    def test_database_rejects_update_and_delete(self) -> None:
        spec = RECORD_SPECS[0]
        result = self.kernel.write(
            self.request(spec, "immutable:01", "semantic:immutable", self.payload(spec))
        )
        connection = sqlite3.connect(self.database_path, isolation_level=None)
        try:
            with self.assertRaisesRegex(sqlite3.IntegrityError, "append_only_violation"):
                connection.execute(
                    "UPDATE protected_records SET semantic_key = 'changed' WHERE record_id = ?",
                    (result.record_id,),
                )
            with self.assertRaisesRegex(sqlite3.IntegrityError, "append_only_violation"):
                connection.execute(
                    "DELETE FROM protected_records WHERE record_id = ?", (result.record_id,)
                )
        finally:
            connection.close()

    def test_event_hash_chain_verifies(self) -> None:
        spec = RECORD_SPECS[0]
        self.kernel.write(
            self.request(spec, "chain-check:01", "semantic:chain", self.payload(spec))
        )
        self.assertTrue(self.kernel.verify_event_chain())

    def test_formal_runtime_mode_is_unavailable(self) -> None:
        with self.assertRaisesRegex(ValueError, "formal runtime mode is unavailable"):
            GovernanceKernel(
                self.database_path.parent / "formal.db",
                "governance-kernel/test",
                mode="FORMAL",
            )

    def test_existing_database_cannot_mix_implementation_versions(self) -> None:
        other = GovernanceKernel(
            self.database_path,
            "governance-kernel/different-version",
            clock=SequenceClock(),
        )
        with self.assertRaisesRegex(RuntimeError, "runtime metadata mismatch"):
            other.initialize()

    def test_publication_payload_must_match_registered_audit(self) -> None:
        record_ids = self.build_chain()
        publication_spec = next(
            spec for spec in RECORD_SPECS if spec.record_type == "Projection Publication Envelope"
        )
        audit_id = record_ids["Registered Projection Change Audit Record"]
        result = self.kernel.write(
            self.request(
                publication_spec,
                "publication-mismatch:01",
                "semantic:publication:mismatch",
                self.payload(publication_spec, "different-from-audit"),
                (audit_id,),
            )
        )
        self.assertEqual("REJECTED_CONTENT_IDENTITY_MISMATCH", result.outcome)

    def test_noncomplete_closure_cannot_support_determinate_projection(self) -> None:
        record_ids = self.build_chain()
        completeness_spec = next(
            spec
            for spec in RECORD_SPECS
            if spec.record_type == "Registered Closure Completeness Record"
        )
        incomplete_payload = self.payload(completeness_spec, "incomplete")
        incomplete_payload["candidate_payload"]["closure_completeness"] = "INCOMPLETE"
        incomplete = self.kernel.write(
            self.request(
                completeness_spec,
                "completeness:incomplete",
                "semantic:completeness:incomplete",
                incomplete_payload,
                (record_ids["Registered Dependency Closure Record"],),
                predecessor_record_id=record_ids["Registered Closure Completeness Record"],
            )
        )
        self.assertEqual("ACCEPTED_EVIDENCE_ONLY", incomplete.outcome)

        audit_spec = next(
            spec
            for spec in RECORD_SPECS
            if spec.record_type == "Registered Projection Change Audit Record"
        )
        audit_payload = self.payload(audit_spec, "invalid-determinate")
        candidate = audit_payload["candidate_payload"]
        candidate["closure_completeness"] = "INCOMPLETE"
        candidate["previous_publication_record_id"] = record_ids[
            "Projection Publication Envelope"
        ]
        candidate["previous_coordinate_digest"] = "coordinate:test:v1"
        candidate["new_coordinate_digest"] = "coordinate:test:v2"
        candidate["projection_result"] = "COMMITTED"
        result = self.kernel.write(
            self.request(
                audit_spec,
                "projection:invalid-determinate",
                "semantic:projection:invalid-determinate",
                audit_payload,
                (
                    record_ids["Registered Temporal Mapping Record"],
                    record_ids["Registered Derived Record Envelope"],
                    record_ids["Registered Dependency Closure Record"],
                    incomplete.record_id or "",
                ),
                predecessor_record_id=record_ids["Registered Projection Change Audit Record"],
            )
        )
        self.assertEqual("REJECTED_INVALID_PAYLOAD", result.outcome)

    def test_successor_publication_keeps_business_payload_identity_and_history(self) -> None:
        record_ids = self.build_chain()
        completeness_spec = next(
            spec
            for spec in RECORD_SPECS
            if spec.record_type == "Registered Closure Completeness Record"
        )
        incomplete_payload = self.payload(completeness_spec, "incomplete-successor")
        incomplete_payload["candidate_payload"]["closure_completeness"] = "INCOMPLETE"
        incomplete = self.kernel.write(
            self.request(
                completeness_spec,
                "successor:completeness",
                "semantic:successor:completeness",
                incomplete_payload,
                (record_ids["Registered Dependency Closure Record"],),
                predecessor_record_id=record_ids["Registered Closure Completeness Record"],
            )
        )
        audit_spec = next(
            spec
            for spec in RECORD_SPECS
            if spec.record_type == "Registered Projection Change Audit Record"
        )
        audit_payload = self.payload(audit_spec, "downgrade")
        candidate = audit_payload["candidate_payload"]
        candidate.update(
            {
                "change_reason": "SOURCE_CORRECTION",
                "closure_completeness": "INCOMPLETE",
                "new_coordinate_digest": "coordinate:test:v2",
                "previous_coordinate_digest": "coordinate:test:v1",
                "previous_publication_record_id": record_ids[
                    "Projection Publication Envelope"
                ],
                "projection_result": "INDETERMINATE",
            }
        )
        audit = self.kernel.write(
            self.request(
                audit_spec,
                "successor:audit",
                "semantic:successor:audit",
                audit_payload,
                (
                    record_ids["Registered Temporal Mapping Record"],
                    record_ids["Registered Derived Record Envelope"],
                    record_ids["Registered Dependency Closure Record"],
                    incomplete.record_id or "",
                ),
                predecessor_record_id=record_ids["Registered Projection Change Audit Record"],
            )
        )
        self.assertEqual("ACCEPTED_EVIDENCE_ONLY", audit.outcome)
        publication_spec = next(
            spec for spec in RECORD_SPECS if spec.record_type == "Projection Publication Envelope"
        )
        publication = self.kernel.write(
            self.request(
                publication_spec,
                "successor:publication",
                "semantic:successor:publication",
                audit_payload,
                (audit.record_id or "",),
                predecessor_record_id=record_ids["Projection Publication Envelope"],
            )
        )
        self.assertEqual("ACCEPTED_EVIDENCE_ONLY", publication.outcome)
        self.assertEqual(audit.payload_digest, publication.payload_digest)
        self.assertNotEqual(audit.content_digest, publication.content_digest)
        publications = [
            row
            for row in self.kernel.export_rows("protected_records")
            if row["record_type"] == "Projection Publication Envelope"
        ]
        self.assertEqual(2, len(publications))

    def test_projection_deletion_record_does_not_delete_history(self) -> None:
        record_ids = self.build_chain()
        rows = self.kernel.export_rows("protected_records")
        self.assertTrue(
            any(row["record_id"] == record_ids["Registered Projection Deletion Record"] for row in rows)
        )
        self.assertTrue(
            any(row["record_id"] == record_ids["Projection Publication Envelope"] for row in rows)
        )
        self.assertTrue(
            any(
                row["record_id"] == record_ids["Registered Projection Change Audit Record"]
                for row in rows
            )
        )


if __name__ == "__main__":
    unittest.main()
