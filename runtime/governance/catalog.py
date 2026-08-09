"""Exact protected-write surface used by the evidence-only runtime slice."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RecordSpec:
    workflow_id: str
    record_type: str
    authority_type: str
    proposal_version: str
    proposal_digest: str
    prerequisite_types: tuple[str, ...] = ()
    content_identity_source_type: str | None = None
    allow_correction: bool = True


PROPOSAL_DIGESTS: dict[str, str] = {
    "WS-01": "1fbeca02ccf0a712180c8d1ce15f0b4953960e6c29c170e63447613c15f17e55",
    "WS-02": "07d1b2b3d3ca6b647cba0262ad65a7b14270c4f7bc314f447e1f8afde27c9913",
    "WS-03": "7320738cb76be12a2ddb795335c6d527fcc8967ee5731513b2df17c03f5db05a",
    "WS-04": "d04daaecf57407e68c973a5ff80094b42f0addefc376ea74a2f239836d2c933c",
    "WS-05": "3ed4c70164e5a0423ba348561db25e552790a0c4ad23682213348987f1e8b01a",
    "WS-06": "ee49d2cbc375557b88f3fabe407c2be3de4b3a13576096394a3b8eaea55fc7a1",
    "WS-07": "d92c359f8ccd3aab7f8502d3abdf548e21d1a727a476f90262f29ce22eb12091",
    "WS-08": "462f0fc8c4c4fde61646087e4c51b8e531d3956c9b2f6d2990a552ef5c33c1c2",
    "WS-09": "36ef7591ee327e6d5af7aa57dd057d11f9eb22e5f2f2b70c08ab6cade53a3da4",
}


WORKFLOW_ORDER: tuple[str, ...] = tuple(f"WS-{index:02d}" for index in range(1, 10))


def _spec(
    workflow_id: str,
    record_type: str,
    authority_type: str,
    proposal_version: str,
    prerequisite_types: tuple[str, ...] = (),
    content_identity_source_type: str | None = None,
) -> RecordSpec:
    return RecordSpec(
        workflow_id=workflow_id,
        record_type=record_type,
        authority_type=authority_type,
        proposal_version=proposal_version,
        proposal_digest=PROPOSAL_DIGESTS[workflow_id],
        prerequisite_types=prerequisite_types,
        content_identity_source_type=content_identity_source_type,
    )


RECORD_SPECS: tuple[RecordSpec, ...] = (
    _spec(
        "WS-01",
        "Registered Institution Registry Entry",
        "InstitutionRegistryEntryRegistrationAuthorityType",
        "CR-0004-CONSTITUTION-CANDIDATE-R1",
    ),
    _spec(
        "WS-02",
        "Registered Source Record",
        "SourceRecordRegistrationAuthorityType",
        "CR-0005-R11-COMPOSITE",
        ("Registered Institution Registry Entry",),
    ),
    _spec(
        "WS-03",
        "Registered Temporal Mapping Record",
        "TemporalMappingRegistrationAuthorityType",
        "CR-0006-R10-COMPOSITE",
        ("Registered Institution Registry Entry",),
    ),
    _spec(
        "WS-04",
        "Registered Atomic Qualification Resolution",
        "QualificationResolutionRegistrationAuthorityType",
        "CR-0007-R5-COMPOSITE",
        ("Registered Source Record", "Registered Temporal Mapping Record"),
    ),
    _spec(
        "WS-05",
        "Registered Authority Applicability Consumer Resolution",
        "ConsumerResolutionFinalRegistrationAuthorityType",
        "CR-0008-R4-COMPOSITE",
        ("Registered Source Record", "Registered Temporal Mapping Record"),
    ),
    _spec(
        "WS-06",
        "Registered Proof Applicability Record",
        "ProofApplicabilityAtomicRegistrationAuthorityType",
        "CR-0009-R2-COMPOSITE",
        (
            "Registered Atomic Qualification Resolution",
            "Registered Authority Applicability Consumer Resolution",
        ),
    ),
    _spec(
        "WS-07",
        "Registered Derived Record Envelope",
        "DerivedRecordEnvelopeRegistrationAuthorityType",
        "CR-0010-R4-COMPOSITE",
        (
            "Registered Institution Registry Entry",
            "Registered Source Record",
            "Registered Temporal Mapping Record",
            "Registered Proof Applicability Record",
        ),
    ),
    _spec(
        "WS-08",
        "Registered Dependency Closure Record",
        "DependencyClosureRegistrationAuthorityType",
        "CR-0011-R2-COMPOSITE",
        (
            "Registered Source Record",
            "Registered Temporal Mapping Record",
            "Registered Derived Record Envelope",
        ),
    ),
    _spec(
        "WS-08",
        "Registered Closure Completeness Record",
        "ClosureCompletenessRegistrationAuthorityType",
        "CR-0011-R2-COMPOSITE",
        ("Registered Dependency Closure Record",),
    ),
    _spec(
        "WS-09",
        "Registered Projection Change Audit Record",
        "ProjectionChangeAuditRegistrationAuthorityType",
        "CR-0012-R2-COMPOSITE",
        (
            "Registered Temporal Mapping Record",
            "Registered Derived Record Envelope",
            "Registered Dependency Closure Record",
            "Registered Closure Completeness Record",
        ),
    ),
    _spec(
        "WS-09",
        "Projection Publication Envelope",
        "ProjectionPublicationEnvelopeRegistrationAuthorityType",
        "CR-0012-R2-COMPOSITE",
        ("Registered Projection Change Audit Record",),
        content_identity_source_type="Registered Projection Change Audit Record",
    ),
)


SPEC_BY_IDENTITY: dict[tuple[str, str], RecordSpec] = {
    (spec.workflow_id, spec.record_type): spec for spec in RECORD_SPECS
}
