"""从 0.1 证据数据库到 0.2 证据数据库的保守迁移。"""

from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Any, Callable

from .catalog import SPEC_BY_IDENTITY
from .kernel import GovernanceKernel, canonical_json, sha256_text


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _connect(path: Path, *, read_only: bool = False) -> sqlite3.Connection:
    if read_only:
        connection = sqlite3.connect(f"file:{path}?mode=ro&immutable=1", uri=True)
    else:
        connection = sqlite3.connect(path, timeout=30, isolation_level=None)
    connection.row_factory = sqlite3.Row
    return connection


def _columns(connection: sqlite3.Connection, table_name: str) -> tuple[str, ...]:
    return tuple(row["name"] for row in connection.execute(f"PRAGMA table_info({table_name})"))


def _rows(
    connection: sqlite3.Connection,
    table_name: str,
    columns: tuple[str, ...] | None = None,
) -> list[dict[str, Any]]:
    selected = ", ".join(columns) if columns else "*"
    rows = connection.execute(
        f"SELECT {selected} FROM {table_name} ORDER BY {ORDER_COLUMNS[table_name]}"
    ).fetchall()
    return [dict(row) for row in rows]


def _drop_append_only_triggers(connection: sqlite3.Connection) -> None:
    trigger_names = [
        row["name"]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'trigger' AND name LIKE '%_reject_%'"
        ).fetchall()
    ]
    for trigger_name in trigger_names:
        connection.execute(f'DROP TRIGGER "{trigger_name}"')


def _install_append_only_triggers(
    connection: sqlite3.Connection, table_names: tuple[str, ...]
) -> None:
    for table_name in table_names:
        connection.execute(
            f"""
            CREATE TRIGGER {table_name}_reject_update
            BEFORE UPDATE ON {table_name}
            BEGIN
                SELECT RAISE(ABORT, 'append_only_violation');
            END
            """
        )
        connection.execute(
            f"""
            CREATE TRIGGER {table_name}_reject_delete
            BEFORE DELETE ON {table_name}
            BEGIN
                SELECT RAISE(ABORT, 'append_only_violation');
            END
            """
        )


def _add_column_if_missing(
    connection: sqlite3.Connection, table_name: str, column_name: str, declaration: str
) -> None:
    if column_name not in _columns(connection, table_name):
        connection.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {declaration}"
        )


def _content_digest(payload_json: str, predecessor_record_id: str | None) -> str:
    return sha256_text(
        canonical_json(
            {
                "payload": json.loads(payload_json),
                "predecessor_record_id": predecessor_record_id,
            }
        )
    )


def migrate_v01_to_v02(
    source_path: str | Path,
    destination_path: str | Path,
    *,
    target_implementation_version: str,
    migration_execution_id: str,
    clock: Callable[[], str],
) -> dict[str, Any]:
    """复制旧证据数据库，保留历史后增加 0.2 可验证边界。"""

    source = Path(source_path)
    destination = Path(destination_path)
    if destination.exists():
        raise FileExistsError(destination)
    if not source.is_file():
        raise FileNotFoundError(source)

    source_digest_before = sha256_file(source)
    with closing(_connect(source, read_only=True)) as source_connection:
        legacy_columns = {
            table_name: _columns(source_connection, table_name)
            for table_name in LEGACY_TABLES
        }
        if "content_digest" in legacy_columns["protected_records"]:
            raise ValueError("source database is not a 0.1 schema")
        source_snapshots = {
            table_name: _rows(source_connection, table_name, legacy_columns[table_name])
            for table_name in LEGACY_TABLES
        }
        source_metadata = {
            row["metadata_key"]: row["metadata_value"]
            for row in source_snapshots["runtime_metadata"]
        }
        source_integrity = source_connection.execute("PRAGMA integrity_check").fetchone()[0]
    if source_integrity != "ok":
        raise RuntimeError("source database integrity check failed")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    migrated_at = clock()

    with closing(_connect(destination)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("BEGIN IMMEDIATE")
        _drop_append_only_triggers(connection)
        _add_column_if_missing(connection, "protected_records", "content_digest", "TEXT")
        _add_column_if_missing(connection, "write_attempts", "content_digest", "TEXT")
        _add_column_if_missing(connection, "write_conflicts", "existing_content_digest", "TEXT")
        _add_column_if_missing(connection, "write_conflicts", "competing_content_digest", "TEXT")
        connection.execute(
            """
            CREATE TABLE migration_lineage (
                migration_execution_id TEXT PRIMARY KEY,
                migration_contract_version TEXT NOT NULL,
                source_database_digest TEXT NOT NULL,
                source_implementation_version TEXT NOT NULL,
                target_implementation_version TEXT NOT NULL,
                source_record_count INTEGER NOT NULL,
                source_attempt_count INTEGER NOT NULL,
                source_conflict_count INTEGER NOT NULL,
                migrated_at TEXT NOT NULL,
                evidence_mode TEXT NOT NULL CHECK (evidence_mode = 'NON_AUTHORITATIVE_CONFORMANCE')
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE migration_content_resolutions (
                resolution_id TEXT PRIMARY KEY,
                entity_kind TEXT NOT NULL,
                entity_id TEXT NOT NULL,
                resolution_status TEXT NOT NULL,
                content_digest TEXT,
                reason TEXT NOT NULL,
                recorded_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE migration_record_assessments (
                record_id TEXT PRIMARY KEY,
                workflow_id TEXT NOT NULL,
                record_type TEXT NOT NULL,
                current_payload_status TEXT NOT NULL,
                reason TEXT NOT NULL,
                assessed_at TEXT NOT NULL,
                FOREIGN KEY (record_id) REFERENCES protected_records(record_id)
            )
            """
        )

        record_rows = connection.execute(
            "SELECT * FROM protected_records ORDER BY record_id"
        ).fetchall()
        record_content_digests: dict[str, str] = {}
        record_payload_digests: dict[str, str] = {}
        current_payload_counts: dict[str, int] = {}
        for record in record_rows:
            content_digest = _content_digest(
                record["payload_json"], record["predecessor_record_id"]
            )
            record_content_digests[record["record_id"]] = content_digest
            record_payload_digests[record["record_id"]] = record["payload_digest"]
            connection.execute(
                "UPDATE protected_records SET content_digest = ? WHERE record_id = ?",
                (content_digest, record["record_id"]),
            )
            connection.execute(
                """
                INSERT INTO migration_content_resolutions(
                    resolution_id, entity_kind, entity_id, resolution_status,
                    content_digest, reason, recorded_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"record:{record['record_id']}",
                    "PROTECTED_RECORD",
                    record["record_id"],
                    "DERIVED_FROM_RETAINED_PAYLOAD_AND_PREDECESSOR",
                    content_digest,
                    "legacy record retained canonical payload and predecessor identity",
                    migrated_at,
                ),
            )
            spec = SPEC_BY_IDENTITY.get((record["workflow_id"], record["record_type"]))
            if spec is None:
                status = "UNKNOWN_CURRENT_TYPE"
                reason = "record type is absent from the current catalog"
            else:
                validation_error = GovernanceKernel._validate_payload(
                    json.loads(record["payload_json"]), spec
                )
                status = (
                    "CURRENT_PAYLOAD_CONFORMANT"
                    if validation_error is None
                    else "LEGACY_RETAINED_NOT_CURRENTLY_CONFORMANT"
                )
                reason = validation_error or "current payload contract satisfied"
            current_payload_counts[status] = current_payload_counts.get(status, 0) + 1
            connection.execute(
                """
                INSERT INTO migration_record_assessments(
                    record_id, workflow_id, record_type, current_payload_status,
                    reason, assessed_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    record["record_id"],
                    record["workflow_id"],
                    record["record_type"],
                    status,
                    reason,
                    migrated_at,
                ),
            )

        attempt_resolution_counts: dict[str, int] = {}
        attempts = connection.execute(
            "SELECT sequence, attempt_id, output_ref, payload_digest FROM write_attempts ORDER BY sequence"
        ).fetchall()
        for attempt in attempts:
            output_ref = attempt["output_ref"]
            if (
                output_ref in record_content_digests
                and record_payload_digests[output_ref] == attempt["payload_digest"]
            ):
                status = "DERIVED_FROM_CONTENT_IDENTICAL_OUTPUT_RECORD"
                content_digest = record_content_digests[output_ref]
                reason = "attempt payload digest matches the retained output record"
            else:
                status = "UNAVAILABLE_LEGACY_REQUEST_PAYLOAD_NOT_RETAINED"
                content_digest = None
                reason = "legacy attempt retained only payload digest and cannot be reverse-derived"
            attempt_resolution_counts[status] = attempt_resolution_counts.get(status, 0) + 1
            connection.execute(
                "UPDATE write_attempts SET content_digest = ? WHERE sequence = ?",
                (content_digest, attempt["sequence"]),
            )
            connection.execute(
                """
                INSERT INTO migration_content_resolutions(
                    resolution_id, entity_kind, entity_id, resolution_status,
                    content_digest, reason, recorded_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    f"attempt:{attempt['attempt_id']}",
                    "WRITE_ATTEMPT",
                    attempt["attempt_id"],
                    status,
                    content_digest,
                    reason,
                    migrated_at,
                ),
            )

        conflict_resolution_counts: dict[str, int] = {}
        conflicts = connection.execute(
            "SELECT * FROM write_conflicts ORDER BY conflict_id"
        ).fetchall()
        for conflict in conflicts:
            existing_digest = record_content_digests[conflict["existing_record_id"]]
            connection.execute(
                """
                UPDATE write_conflicts
                SET existing_content_digest = ?, competing_content_digest = NULL
                WHERE conflict_id = ?
                """,
                (existing_digest, conflict["conflict_id"]),
            )
            for side, status, content_digest, reason in (
                (
                    "existing",
                    "DERIVED_FROM_EXISTING_RECORD",
                    existing_digest,
                    "existing record retained canonical payload and predecessor identity",
                ),
                (
                    "competing",
                    "UNAVAILABLE_LEGACY_COMPETING_PAYLOAD_NOT_RETAINED",
                    None,
                    "legacy conflict retained only the competing payload digest",
                ),
            ):
                conflict_resolution_counts[status] = conflict_resolution_counts.get(status, 0) + 1
                connection.execute(
                    """
                    INSERT INTO migration_content_resolutions(
                        resolution_id, entity_kind, entity_id, resolution_status,
                        content_digest, reason, recorded_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        f"conflict:{conflict['conflict_id']}:{side}",
                        f"WRITE_CONFLICT_{side.upper()}",
                        conflict["conflict_id"],
                        status,
                        content_digest,
                        reason,
                        migrated_at,
                    ),
                )

        connection.execute(
            "UPDATE runtime_metadata SET metadata_value = ? WHERE metadata_key = 'implementation_version'",
            (target_implementation_version,),
        )
        for key, value in (
            ("migration_contract_version", "governance-schema-migration/0.1-to-0.2"),
            ("migration_execution_id", migration_execution_id),
            ("migration_source_implementation_version", source_metadata["implementation_version"]),
        ):
            connection.execute(
                "INSERT INTO runtime_metadata(metadata_key, metadata_value) VALUES (?, ?)",
                (key, value),
            )
        connection.execute(
            """
            INSERT INTO migration_lineage(
                migration_execution_id, migration_contract_version,
                source_database_digest, source_implementation_version,
                target_implementation_version, source_record_count,
                source_attempt_count, source_conflict_count, migrated_at, evidence_mode
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                migration_execution_id,
                "governance-schema-migration/0.1-to-0.2",
                source_digest_before,
                source_metadata["implementation_version"],
                target_implementation_version,
                len(source_snapshots["protected_records"]),
                len(source_snapshots["write_attempts"]),
                len(source_snapshots["write_conflicts"]),
                migrated_at,
                "NON_AUTHORITATIVE_CONFORMANCE",
            ),
        )
        _install_append_only_triggers(
            connection,
            LEGACY_TABLES
            + (
                "migration_lineage",
                "migration_content_resolutions",
                "migration_record_assessments",
            ),
        )
        connection.execute("PRAGMA user_version = 2")

        preserved = {}
        for table_name in LEGACY_TABLES:
            destination_rows = _rows(
                connection, table_name, legacy_columns[table_name]
            )
            if table_name == "runtime_metadata":
                source_comparable = [
                    row
                    for row in source_snapshots[table_name]
                    if row["metadata_key"] != "implementation_version"
                ]
                destination_comparable = [
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
                preserved[table_name] = source_comparable == destination_comparable
            else:
                preserved[table_name] = source_snapshots[table_name] == destination_rows
        if not all(preserved.values()):
            raise RuntimeError(f"legacy history preservation failed: {preserved}")
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        foreign_key_failures = connection.execute("PRAGMA foreign_key_check").fetchall()
        trigger_count = connection.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type = 'trigger' AND name LIKE '%_reject_%'"
        ).fetchone()[0]
        connection.execute("COMMIT")
        connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        connection.execute("PRAGMA journal_mode = DELETE")

    source_digest_after = sha256_file(source)
    if source_digest_after != source_digest_before:
        raise RuntimeError("source evidence database was modified")
    if integrity != "ok" or foreign_key_failures:
        raise RuntimeError("migrated database integrity check failed")

    return {
        "migration_execution_id": migration_execution_id,
        "migration_contract_version": "governance-schema-migration/0.1-to-0.2",
        "source_database_digest_before": source_digest_before,
        "source_database_digest_after": source_digest_after,
        "source_database_unchanged": True,
        "source_implementation_version": source_metadata["implementation_version"],
        "target_implementation_version": target_implementation_version,
        "source_counts": {
            "protected_records": len(source_snapshots["protected_records"]),
            "write_attempts": len(source_snapshots["write_attempts"]),
            "write_conflicts": len(source_snapshots["write_conflicts"]),
        },
        "legacy_tables_preserved": preserved,
        "record_payload_assessment_counts": dict(sorted(current_payload_counts.items())),
        "attempt_content_resolution_counts": dict(sorted(attempt_resolution_counts.items())),
        "conflict_content_resolution_counts": dict(sorted(conflict_resolution_counts.items())),
        "integrity_check": integrity,
        "foreign_key_failure_count": len(foreign_key_failures),
        "append_only_trigger_count": trigger_count,
        "journal_mode": "delete",
        "result": "PASS_WITH_EXPLICIT_LEGACY_UNAVAILABLE_DIGESTS",
    }
