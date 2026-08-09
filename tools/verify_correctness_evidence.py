#!/usr/bin/env python3
"""独立复核 CR-0015 正确性证据包。"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = ROOT / "evidence" / "runtime" / "CR-0015-CORRECTNESS-001"
GENESIS_HASH = "0" * 64


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


def read_only_connection(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(f"file:{path}?mode=ro&immutable=1", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def verify_event_chain(connection: sqlite3.Connection) -> tuple[int, int, int]:
    rows = connection.execute(
        "SELECT previous_event_hash, event_body_json, event_hash FROM write_attempts ORDER BY sequence"
    ).fetchall()
    previous = GENESIS_HASH
    broken_links = 0
    broken_digests = 0
    for row in rows:
        if row["previous_event_hash"] != previous:
            broken_links += 1
        expected = sha256_bytes((previous + "\n" + row["event_body_json"]).encode("utf-8"))
        if row["event_hash"] != expected:
            broken_digests += 1
        previous = row["event_hash"]
    return len(rows), broken_links, broken_digests


def verify_database(path: Path) -> dict[str, Any]:
    with read_only_connection(path) as connection:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        journal_mode = connection.execute("PRAGMA journal_mode").fetchone()[0]
        attempt_count, broken_links, broken_digests = verify_event_chain(connection)
        trigger_count = connection.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type = 'trigger' AND name LIKE '%_reject_%'"
        ).fetchone()[0]
        non_evidence_records = connection.execute(
            "SELECT COUNT(*) FROM protected_records WHERE evidence_mode != 'NON_AUTHORITATIVE_CONFORMANCE'"
        ).fetchone()[0]
        metadata = dict(
            connection.execute(
                "SELECT metadata_key, metadata_value FROM runtime_metadata"
            ).fetchall()
        )
    if integrity != "ok" or journal_mode != "delete":
        raise RuntimeError(f"database state check failed: {path.name}")
    if broken_links or broken_digests:
        raise RuntimeError(f"event chain check failed: {path.name}")
    if trigger_count != 10 or non_evidence_records:
        raise RuntimeError(f"append-only or evidence-mode check failed: {path.name}")
    if metadata.get("formal_fact_creation") != "PROHIBITED":
        raise RuntimeError(f"formal fact prohibition missing: {path.name}")
    return {
        "integrity_check": integrity,
        "journal_mode": journal_mode,
        "event_count": attempt_count,
        "broken_event_links": broken_links,
        "broken_event_digests": broken_digests,
        "append_only_trigger_count": trigger_count,
        "non_evidence_record_count": non_evidence_records,
        "formal_fact_creation": metadata["formal_fact_creation"],
        "result": "PASS",
    }


def verify_concurrency(target: Path) -> dict[str, Any]:
    expected = {
        "thread-idempotent.db": {"ACCEPTED_EVIDENCE_ONLY": 1, "IDEMPOTENT_EXISTING": 31},
        "thread-conflict.db": {"ACCEPTED_EVIDENCE_ONLY": 1, "CONFLICT_RECORDED": 31},
        "process-idempotent.db": {"ACCEPTED_EVIDENCE_ONLY": 1, "IDEMPOTENT_EXISTING": 15},
        "process-conflict.db": {"ACCEPTED_EVIDENCE_ONLY": 1, "CONFLICT_RECORDED": 15},
    }
    observed: dict[str, Any] = {}
    for filename, expected_outcomes in expected.items():
        with read_only_connection(target / filename) as connection:
            outcomes = dict(
                Counter(
                    row[0]
                    for row in connection.execute(
                        "SELECT outcome FROM write_attempts ORDER BY sequence"
                    ).fetchall()
                )
            )
            records = connection.execute("SELECT COUNT(*) FROM protected_records").fetchone()[0]
            conflicts = connection.execute("SELECT COUNT(*) FROM write_conflicts").fetchone()[0]
        expected_conflicts = expected_outcomes.get("CONFLICT_RECORDED", 0)
        if outcomes != expected_outcomes or records != 1 or conflicts != expected_conflicts:
            raise RuntimeError(f"concurrency evidence mismatch: {filename}")
        observed[filename] = {
            "outcomes": dict(sorted(outcomes.items())),
            "record_count": records,
            "conflict_count": conflicts,
            "result": "PASS",
        }
    return {"cases": observed, "single_terminal_assignment": True, "result": "PASS"}


def verify_projection(target: Path) -> dict[str, Any]:
    with read_only_connection(target / "replay-01.db") as connection:
        records = [dict(row) for row in connection.execute(
            "SELECT * FROM protected_records ORDER BY recorded_at, record_id"
        ).fetchall()]
        attempts = [dict(row) for row in connection.execute(
            "SELECT * FROM write_attempts ORDER BY sequence"
        ).fetchall()]
    by_type: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_type.setdefault(record["record_type"], []).append(record)
    publications = by_type["Projection Publication Envelope"]
    audits = by_type["Registered Projection Change Audit Record"]
    rebuilds = by_type["Registered Projection Rebuild Requirement"]
    deletions = by_type["Registered Projection Deletion Record"]
    if len(publications) != 2 or len(audits) != 2 or len(rebuilds) != 1 or len(deletions) != 1:
        raise RuntimeError("projection lifecycle cardinality mismatch")
    initial_publication, successor_publication = publications
    _, successor_audit = audits
    rebuild = rebuilds[0]
    deletion = deletions[0]
    publication_prerequisites = json.loads(successor_publication["prerequisite_record_ids_json"])
    deletion_payload = json.loads(deletion["payload_json"])["candidate_payload"]
    rebuild_payload = json.loads(rebuild["payload_json"])["candidate_payload"]
    record_ids = {record["record_id"] for record in records}
    if successor_publication["predecessor_record_id"] != initial_publication["record_id"]:
        raise RuntimeError("projection publication predecessor mismatch")
    if publication_prerequisites != [successor_audit["record_id"]]:
        raise RuntimeError("projection publication audit reference mismatch")
    if successor_publication["payload_digest"] != successor_audit["payload_digest"]:
        raise RuntimeError("audit/publication business payload identity mismatch")
    if successor_publication["content_digest"] == successor_audit["content_digest"]:
        raise RuntimeError("audit/publication history content was not distinguished")
    if deletion_payload["target_publication_record_id"] != initial_publication["record_id"]:
        raise RuntimeError("projection deletion target mismatch")
    if deletion_payload["rebuild_requirement_record_id"] != rebuild["record_id"]:
        raise RuntimeError("projection deletion rebuild reference mismatch")
    if rebuild_payload["previous_publication_record_id"] != initial_publication["record_id"]:
        raise RuntimeError("projection rebuild predecessor mismatch")
    if not {
        initial_publication["record_id"],
        successor_publication["record_id"],
        successor_audit["record_id"],
        rebuild["record_id"],
        deletion["record_id"],
    }.issubset(record_ids):
        raise RuntimeError("projection history is incomplete")
    outcomes = Counter(row["outcome"] for row in attempts)
    required_outcomes = {
        "REJECTED_INVALID_PAYLOAD": 1,
        "CONFLICT_RECORDED": 1,
        "REJECTED_CONTENT_IDENTITY_MISMATCH": 1,
        "REJECTED_MISSING_PREREQUISITE": 1,
    }
    if any(outcomes[key] != value for key, value in required_outcomes.items()):
        raise RuntimeError("projection negative-path evidence mismatch")
    return {
        "record_count": len(records),
        "publication_count": len(publications),
        "audit_count": len(audits),
        "rebuild_requirement_count": len(rebuilds),
        "deletion_record_count": len(deletions),
        "audit_publication_payload_identity": True,
        "publication_predecessor_preserved": True,
        "rebuild_and_deletion_references_verified": True,
        "negative_paths_verified": True,
        "history_preserved": True,
        "result": "PASS",
    }


def verify(target: Path) -> dict[str, Any]:
    manifest = json.loads((target / "manifest.json").read_text(encoding="utf-8"))
    input_manifest = json.loads((target / "input_manifest.json").read_text(encoding="utf-8"))
    actual_files = {path.name for path in target.iterdir() if path.is_file()}
    expected_files = set(manifest["files"]) | {"manifest.json"}
    if actual_files != expected_files:
        raise RuntimeError("manifest file closure mismatch")
    observed_digests = {
        filename: sha256_file(target / filename) for filename in manifest["files"]
    }
    if observed_digests != manifest["files"]:
        raise RuntimeError("manifest file digest mismatch")
    package_digest = sha256_bytes(
        "".join(
            f"{digest}  {name}\n" for name, digest in sorted(observed_digests.items())
        ).encode("utf-8")
    )
    if package_digest != manifest["package_digest"]:
        raise RuntimeError("package digest mismatch")
    implementation_digest = source_digest(
        (
            ROOT / "runtime" / "governance" / "catalog.py",
            ROOT / "runtime" / "governance" / "kernel.py",
        )
    )
    harness_digest = source_digest(
        (
            ROOT / "tests" / "test_governance_kernel.py",
            ROOT / "tools" / "run_correctness_evidence.py",
        )
    )
    if not input_manifest["implementation_version"].endswith(implementation_digest):
        raise RuntimeError("implementation digest mismatch")
    if input_manifest["test_harness_digest"] != harness_digest:
        raise RuntimeError("test harness digest mismatch")
    replay_files = sorted(target.glob("replay-*.db"))
    replay_digests = [sha256_file(path) for path in replay_files]
    if len(replay_files) != 5 or len(set(replay_digests)) != 1:
        raise RuntimeError("deterministic replay database mismatch")
    database_results = {
        path.name: verify_database(path) for path in sorted(target.glob("*.db"))
    }
    sidecars = sorted(path.name for path in target.iterdir() if path.name.endswith(("-wal", "-shm")))
    if sidecars:
        raise RuntimeError("SQLite sidecar file detected")
    return {
        "execution_id": input_manifest["execution_id"],
        "implementation_digest": implementation_digest,
        "test_harness_digest": harness_digest,
        "package_digest": package_digest,
        "manifest_file_count": len(observed_digests),
        "exact_file_closure": True,
        "manifest_digests_verified": True,
        "replay_database_count": len(replay_files),
        "unique_replay_database_digest_count": len(set(replay_digests)),
        "database_results": database_results,
        "concurrency": verify_concurrency(target),
        "projection": verify_projection(target),
        "sqlite_sidecar_count": len(sidecars),
        "formal_fact_created": False,
        "institution_freeze_created": False,
        "result": "PASS_AS_INDEPENDENT_READ_ONLY_REVIEW",
    }


if __name__ == "__main__":
    evidence_target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_TARGET
    print(json.dumps(verify(evidence_target), ensure_ascii=False, sort_keys=True, indent=2))
