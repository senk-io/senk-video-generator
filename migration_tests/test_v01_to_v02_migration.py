from __future__ import annotations

import hashlib
import sqlite3
import tempfile
import unittest
from pathlib import Path

from runtime.governance import GovernanceKernel
from runtime.governance.migration import migrate_v01_to_v02


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence" / "runtime" / "CR-0014-PW-004" / "governance.db"
TARGET_VERSION = "governance-kernel/0.2.0+sha256:migration-test"


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MigrationTests(unittest.TestCase):
    def test_v01_history_is_preserved_and_current_runtime_can_open(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_name:
            destination = Path(temporary_name) / "migrated.db"
            source_digest = file_digest(SOURCE)
            summary = migrate_v01_to_v02(
                SOURCE,
                destination,
                target_implementation_version=TARGET_VERSION,
                migration_execution_id="migration-test",
                clock=lambda: "2026-08-09T09:00:00.000000Z",
            )
            self.assertEqual(source_digest, file_digest(SOURCE))
            self.assertTrue(summary["source_database_unchanged"])
            self.assertTrue(all(summary["legacy_tables_preserved"].values()))
            self.assertEqual(
                {
                    "CURRENT_PAYLOAD_CONFORMANT": 9,
                    "LEGACY_RETAINED_NOT_CURRENTLY_CONFORMANT": 3,
                },
                summary["record_payload_assessment_counts"],
            )
            self.assertEqual("ok", summary["integrity_check"])
            self.assertEqual(0, summary["foreign_key_failure_count"])
            self.assertEqual(16, summary["append_only_trigger_count"])

            kernel = GovernanceKernel(destination, TARGET_VERSION)
            kernel.initialize()
            self.assertTrue(kernel.verify_event_chain())

            connection = sqlite3.connect(destination, isolation_level=None)
            try:
                metadata = dict(
                    connection.execute(
                        "SELECT metadata_key, metadata_value FROM runtime_metadata"
                    ).fetchall()
                )
                self.assertEqual(TARGET_VERSION, metadata["implementation_version"])
                self.assertEqual(
                    "governance-schema-migration/0.1-to-0.2",
                    metadata["migration_contract_version"],
                )
                with self.assertRaisesRegex(sqlite3.IntegrityError, "append_only_violation"):
                    connection.execute(
                        "UPDATE migration_lineage SET migration_contract_version = 'changed'"
                    )
            finally:
                connection.close()


if __name__ == "__main__":
    unittest.main()
