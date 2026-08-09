#!/usr/bin/env python3
"""独立复核 CR-0016 迁移证据包。"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.governance.catalog import SPEC_BY_IDENTITY
from runtime.governance.kernel import GovernanceKernel, canonical_json, sha256_text


DEFAULT_TARGET = ROOT / "evidence" / "runtime" / "CR-0016-MIGRATION-001"
SOURCE_PACKAGE = ROOT / "evidence" / "runtime" / "CR-0014-PW-004"
SOURCE_DATABASE = SOURCE_PACKAGE / "governance.db"
GENESIS_HASH = "0" * 64
LEGACY_TABLES = (
    "runtime_metadata",
    "authority_grants",
    "protected_records",
    "write_attempts",
    "write_conflicts",
)
ORDER_COLUMNS = {
    "runtime_metadata": "metadata_key",
    "authority_grants": "grant_id",
    "protected_records": "record_id",
    "write_attempts": "sequence",
    "write_conflicts": "conflict_id",
}


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


def connect(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(f"file:{path}?mode=ro&immutable=1", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def columns(connection: sqlite3.Connection, table_name: str) -> tuple[str, ...]:
    return tuple(row["name"] for row in connection.execute(f"PRAGMA table_info({table_name})"))


def rows(
    connection: sqlite3.Connection,
    table_name: str,
    selected_columns: tuple[str, ...] | None = None,
) -> list[dict[str, Any]]:
    selected = ", ".join(selected_columns) if selected_columns else "*"
    result = connection.execute(
        f"SELECT {selected} FROM {table_name} ORDER BY {ORDER_COLUMNS[table_name]}"
    ).fetchall()
    return [dict(row) for row in result]


def verify_event_chain(connection: sqlite3.Connection) -> dict[str, int]:
    attempts = connection.execute(
        "SELECT * FROM write_attempts ORDER BY sequence"
    ).fetchall()
    previous = GENESIS_HASH
    broken_links = 0
    broken_digests = 0
    for attempt in attempts:
        if attempt["previous_event_hash"] != previous:
            broken_links += 1
        expected = sha256_text(previous + "\n" + attempt["event_body_json"])
        if attempt["event_hash"] != expected:
            broken_digests += 1
        previous = attempt["event_hash"]
    return {
        "event_count": len(attempts),
        "broken_link_count": broken_links,
        "broken_digest_count": broken_digests,
    }


def verify(target: Path) -> dict[str, Any]:
    manifest = json.loads((target / "manifest.json").read_text(encoding="utf-8"))
    input_manifest = json.loads((target / "input_manifest.json").read_text(encoding="utf-8"))
    actual_files = {path.name for path in target.iterdir() if path.is_file()}
    expected_files = set(manifest["files"]) | {"manifest.json"}
    if actual_files != expected_files:
        raise RuntimeError("migration package file closure mismatch")
    observed_digests = {
        filename: sha256_file(target / filename) for filename in manifest["files"]
    }
    if observed_digests != manifest["files"]:
        raise RuntimeError("migration package file digest mismatch")
    package_digest = sha256_bytes(
        "".join(
            f"{digest}  {name}\n" for name, digest in sorted(observed_digests.items())
        ).encode("utf-8")
    )
    if package_digest != manifest["package_digest"]:
        raise RuntimeError("migration package digest mismatch")

    implementation_digest = source_digest(
        (
            ROOT / "runtime" / "governance" / "catalog.py",
            ROOT / "runtime" / "governance" / "kernel.py",
        )
    )
    harness_digest = source_digest(
        (
            ROOT / "runtime" / "governance" / "migration.py",
            ROOT / "migration_tests" / "test_v01_to_v02_migration.py",
            ROOT / "tools" / "run_migration_evidence.py",
        )
    )
    if not input_manifest["target_implementation_version"].endswith(implementation_digest):
        raise RuntimeError("migration target implementation digest mismatch")
    if input_manifest["migration_harness_digest"] != harness_digest:
        raise RuntimeError("migration harness digest mismatch")

    source_manifest = json.loads((SOURCE_PACKAGE / "manifest.json").read_text(encoding="utf-8"))
    source_database_digest = sha256_file(SOURCE_DATABASE)
    if source_manifest["package_digest"] != input_manifest["source_package_digest"]:
        raise RuntimeError("source package digest mismatch")
    if source_database_digest != input_manifest["source_database_digest"]:
        raise RuntimeError("source database digest mismatch")

    migrated_database = target / "migrated.db"
    with connect(SOURCE_DATABASE) as source_connection, connect(migrated_database) as destination:
        source_columns = {
            table_name: columns(source_connection, table_name)
            for table_name in LEGACY_TABLES
        }
        preserved: dict[str, bool] = {}
        for table_name in LEGACY_TABLES:
            source_rows = rows(source_connection, table_name, source_columns[table_name])
            destination_rows = rows(destination, table_name, source_columns[table_name])
            if table_name == "runtime_metadata":
                source_rows = [
                    row for row in source_rows if row["metadata_key"] != "implementation_version"
                ]
                destination_rows = [
                    row
                    for row in destination_rows
                    if row["metadata_key"]
                    not in {
                        "implementation_version",
                        "migration_contract_version",
                        "migration_execution_id",
                        "migration_source_implementation_version",
                    }
                ]
            elif table_name == "authority_grants":
                source_ids = {row["grant_id"] for row in source_rows}
                destination_rows = [
                    row for row in destination_rows if row["grant_id"] in source_ids
                ]
            elif table_name == "protected_records":
                source_ids = {row["record_id"] for row in source_rows}
                destination_rows = [
                    row for row in destination_rows if row["record_id"] in source_ids
                ]
            elif table_name == "write_attempts":
                source_ids = {row["attempt_id"] for row in source_rows}
                destination_rows = [
                    row for row in destination_rows if row["attempt_id"] in source_ids
                ]
            preserved[table_name] = source_rows == destination_rows
        if not all(preserved.values()):
            raise RuntimeError(f"legacy table preservation mismatch: {preserved}")

        source_events = source_connection.execute(
            "SELECT event_hash FROM write_attempts ORDER BY sequence"
        ).fetchall()
        destination_events = destination.execute(
            "SELECT event_hash FROM write_attempts ORDER BY sequence LIMIT ?",
            (len(source_events),),
        ).fetchall()
        if source_events != destination_events:
            raise RuntimeError("legacy event chain prefix changed")

        required_columns = {
            "protected_records": {"content_digest"},
            "write_attempts": {"content_digest"},
            "write_conflicts": {"existing_content_digest", "competing_content_digest"},
        }
        for table_name, required in required_columns.items():
            if not required.issubset(columns(destination, table_name)):
                raise RuntimeError(f"missing migrated columns: {table_name}")

        protected_records = [
            dict(row)
            for row in destination.execute(
                "SELECT * FROM protected_records ORDER BY recorded_at, record_id"
            ).fetchall()
        ]
        for record in protected_records[:12]:
            expected_content_digest = sha256_text(
                canonical_json(
                    {
                        "payload": json.loads(record["payload_json"]),
                        "predecessor_record_id": record["predecessor_record_id"],
                    }
                )
            )
            if record["content_digest"] != expected_content_digest:
                raise RuntimeError(f"legacy record content digest mismatch: {record['record_id']}")

        assessment_counts = dict(
            Counter(
                row[0]
                for row in destination.execute(
                    "SELECT current_payload_status FROM migration_record_assessments"
                ).fetchall()
            )
        )
        if assessment_counts != {
            "CURRENT_PAYLOAD_CONFORMANT": 9,
            "LEGACY_RETAINED_NOT_CURRENTLY_CONFORMANT": 3,
        }:
            raise RuntimeError("legacy payload assessment mismatch")

        resolution_counts = dict(
            Counter(
                (row["entity_kind"], row["resolution_status"])
                for row in destination.execute(
                    "SELECT entity_kind, resolution_status FROM migration_content_resolutions"
                ).fetchall()
            )
        )
        expected_resolutions = {
            ("PROTECTED_RECORD", "DERIVED_FROM_RETAINED_PAYLOAD_AND_PREDECESSOR"): 12,
            ("WRITE_ATTEMPT", "DERIVED_FROM_CONTENT_IDENTICAL_OUTPUT_RECORD"): 23,
            ("WRITE_ATTEMPT", "UNAVAILABLE_LEGACY_REQUEST_PAYLOAD_NOT_RETAINED"): 36,
            ("WRITE_CONFLICT_EXISTING", "DERIVED_FROM_EXISTING_RECORD"): 11,
            (
                "WRITE_CONFLICT_COMPETING",
                "UNAVAILABLE_LEGACY_COMPETING_PAYLOAD_NOT_RETAINED",
            ): 11,
        }
        if resolution_counts != expected_resolutions:
            raise RuntimeError("legacy content-resolution classification mismatch")

        post_migration_records = [
            record
            for record in protected_records
            if record["execution_id"] == "CR-0016-MIGRATION-001:post-migration-write"
        ]
        if len(post_migration_records) != 7:
            raise RuntimeError("post-migration record count mismatch")
        for record in post_migration_records:
            spec = SPEC_BY_IDENTITY[(record["workflow_id"], record["record_type"])]
            error = GovernanceKernel._validate_payload(json.loads(record["payload_json"]), spec)
            if error:
                raise RuntimeError(f"post-migration payload invalid: {record['record_id']}: {error}")

        by_type: dict[str, list[dict[str, Any]]] = {}
        for record in protected_records:
            by_type.setdefault(record["record_type"], []).append(record)
        legacy_publication, successor_publication = by_type["Projection Publication Envelope"]
        legacy_audit, successor_audit = by_type["Registered Projection Change Audit Record"]
        rebuild = by_type["Registered Projection Rebuild Requirement"][0]
        deletion = by_type["Registered Projection Deletion Record"][0]
        deletion_payload = json.loads(deletion["payload_json"])["candidate_payload"]
        if successor_publication["predecessor_record_id"] != legacy_publication["record_id"]:
            raise RuntimeError("post-migration publication predecessor mismatch")
        if successor_audit["predecessor_record_id"] != legacy_audit["record_id"]:
            raise RuntimeError("post-migration audit predecessor mismatch")
        if successor_publication["payload_digest"] != successor_audit["payload_digest"]:
            raise RuntimeError("post-migration audit/publication identity mismatch")
        if deletion_payload["target_publication_record_id"] != legacy_publication["record_id"]:
            raise RuntimeError("post-migration deletion target mismatch")
        if deletion_payload["rebuild_requirement_record_id"] != rebuild["record_id"]:
            raise RuntimeError("post-migration deletion rebuild mismatch")

        metadata = dict(
            destination.execute(
                "SELECT metadata_key, metadata_value FROM runtime_metadata"
            ).fetchall()
        )
        lineage = dict(destination.execute("SELECT * FROM migration_lineage").fetchone())
        event_chain = verify_event_chain(destination)
        integrity = destination.execute("PRAGMA integrity_check").fetchone()[0]
        foreign_key_failures = len(destination.execute("PRAGMA foreign_key_check").fetchall())
        journal_mode = destination.execute("PRAGMA journal_mode").fetchone()[0]
        user_version = destination.execute("PRAGMA user_version").fetchone()[0]
        trigger_count = destination.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type = 'trigger' AND name LIKE '%_reject_%'"
        ).fetchone()[0]
        counts = {
            "authority_grants": destination.execute(
                "SELECT COUNT(*) FROM authority_grants"
            ).fetchone()[0],
            "protected_records": len(protected_records),
            "write_attempts": destination.execute(
                "SELECT COUNT(*) FROM write_attempts"
            ).fetchone()[0],
            "write_conflicts": destination.execute(
                "SELECT COUNT(*) FROM write_conflicts"
            ).fetchone()[0],
        }

    expected_counts = {
        "authority_grants": 13,
        "protected_records": 19,
        "write_attempts": 68,
        "write_conflicts": 11,
    }
    if counts != expected_counts:
        raise RuntimeError(f"migrated database count mismatch: {counts}")
    if event_chain != {"event_count": 68, "broken_link_count": 0, "broken_digest_count": 0}:
        raise RuntimeError("mixed-version event chain mismatch")
    if integrity != "ok" or foreign_key_failures or journal_mode != "delete" or user_version != 2:
        raise RuntimeError("migrated database integrity or version mismatch")
    if trigger_count != 16:
        raise RuntimeError("migrated append-only trigger count mismatch")
    if lineage["source_database_digest"] != source_database_digest:
        raise RuntimeError("migration lineage source digest mismatch")
    if metadata["implementation_version"] != input_manifest["target_implementation_version"]:
        raise RuntimeError("migrated runtime metadata version mismatch")
    sidecars = sorted(path.name for path in target.iterdir() if path.name.endswith(("-wal", "-shm")))
    if sidecars:
        raise RuntimeError("migration evidence contains SQLite sidecars")

    return {
        "execution_id": input_manifest["execution_id"],
        "implementation_digest": implementation_digest,
        "migration_harness_digest": harness_digest,
        "source_package_digest": source_manifest["package_digest"],
        "source_database_digest": source_database_digest,
        "package_digest": package_digest,
        "manifest_file_count": len(observed_digests),
        "exact_file_closure": True,
        "legacy_tables_preserved": preserved,
        "legacy_event_chain_prefix_preserved": True,
        "legacy_record_content_digests_derived": 12,
        "legacy_unavailable_digests_explicitly_preserved_as_unknown": 47,
        "legacy_payload_assessment_counts": assessment_counts,
        "post_migration_current_payload_record_count": len(post_migration_records),
        "post_migration_relationships_verified": True,
        "database_counts": counts,
        "event_chain": event_chain,
        "integrity_check": integrity,
        "foreign_key_failure_count": foreign_key_failures,
        "journal_mode": journal_mode,
        "user_version": user_version,
        "append_only_trigger_count": trigger_count,
        "sqlite_sidecar_count": len(sidecars),
        "formal_fact_created": False,
        "institution_freeze_created": False,
        "result": "PASS_AS_INDEPENDENT_READ_ONLY_MIGRATION_REVIEW",
    }


if __name__ == "__main__":
    evidence_target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_TARGET
    print(json.dumps(verify(evidence_target), ensure_ascii=False, sort_keys=True, indent=2))
