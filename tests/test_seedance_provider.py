from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from provider_adapters.seedance import (
    AdapterError,
    UrllibSeedanceTransport,
    build_generation_payload,
    run_trial,
    validate_trial_contract,
    write_json,
    write_manifest,
)
from tools.run_seedance_trial import load_contract
from tools.verify_seedance_evidence import verify


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    ROOT
    / "experiments"
    / "provider_compatibility"
    / "seedance_fictional_child_crying_closeup_v1.json"
)


class FakeTransport:
    def __init__(
        self,
        *,
        mismatched_task: bool = False,
        failed: bool = False,
        unknown_status: bool = False,
    ) -> None:
        self.payload: dict | None = None
        self.query_count = 0
        self.mismatched_task = mismatched_task
        self.failed = failed
        self.unknown_status = unknown_status
        self.cancel_count = 0

    def create(self, payload: dict) -> dict:
        self.payload = payload
        return {"id": "cgt-20260901-test001"}

    def query(self, task_id: str) -> dict:
        self.query_count += 1
        if self.unknown_status:
            status = "queued" if self.query_count == 1 else "almost_done"
        elif self.failed:
            status = "queued" if self.query_count == 1 else "failed"
        else:
            status = "queued" if self.query_count == 1 else "succeeded"
        observed_id = "cgt-OTHER-TASK" if self.mismatched_task else task_id
        task = {
            "id": observed_id,
            "model": "dreamina-seedance-2-0-260128",
            "status": status,
            "created_at": 1785125529,
            "updated_at": 1785125946,
            "resolution": "720p",
            "duration": 5,
            "ratio": "16:9",
            "generate_audio": True,
            "framespersecond": 24,
            "usage": {"completion_tokens": 110000, "total_tokens": 110000},
        }
        if status == "succeeded":
            task["content"] = {
                "video_url": "https://ark-content.bytepluses.com/output.mp4?X-Amz-Signature=secret"
            }
        if status == "failed":
            task["error"] = {"code": "OutputVideoSensitiveContentDetected", "message": "blocked"}
        return task

    def download(self, url: str, destination: Path, max_bytes: int) -> dict:
        self.asserted_url = url
        content = b"fake-mp4"
        destination.write_bytes(content)
        import hashlib

        return {
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
            "content_type": "video/mp4",
        }

    def cancel(self, task_id: str) -> dict:
        self.cancel_count += 1
        return {"id": task_id, "status": "cancelled"}


def fake_probe(_path: Path) -> dict:
    return {
        "decoded_frame_count": 120,
        "fps": 24.0,
        "duration_seconds": 5.0,
        "size": [1280, 720],
        "audio_stream_present": True,
        "audio_sample_rate_hz": 48000,
        "audio_channels": "mono",
    }


class SeedanceProviderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = load_contract(CONTRACT_PATH)

    def test_contract_and_payload_are_fixed_to_modelark_v3(self) -> None:
        normalized = validate_trial_contract(self.contract)
        payload = build_generation_payload(normalized)

        self.assertEqual(payload["model"], "dreamina-seedance-2-0-260128")
        self.assertEqual(payload["resolution"], "720p")
        self.assertEqual(payload["duration"], 5)
        self.assertEqual(payload["ratio"], "16:9")
        self.assertIs(payload["generate_audio"], True)
        self.assertIs(payload["watermark"], False)
        self.assertEqual(payload["content"][0]["type"], "text")
        self.assertIn("Native audio", payload["content"][0]["text"])
        self.assertNotIn("seed", payload)

    def test_contract_rejects_unbounded_or_local_execution(self) -> None:
        mutated = json.loads(json.dumps(self.contract))
        mutated["provider"]["execution_backend"] = "local_mps"
        with self.assertRaisesRegex(ValueError, "remote_api"):
            validate_trial_contract(mutated)

        mutated = json.loads(json.dumps(self.contract))
        mutated["non_goals"].remove("formal_selection_decision")
        with self.assertRaisesRegex(ValueError, "非目标"):
            validate_trial_contract(mutated)

        mutated = json.loads(json.dumps(self.contract))
        mutated["generation"]["ratio"] = "adaptive"
        with self.assertRaisesRegex(ValueError, "画幅比"):
            validate_trial_contract(mutated)

    def test_transport_rejects_non_modelark_origin(self) -> None:
        with self.assertRaisesRegex(ValueError, "接口来源"):
            UrllibSeedanceTransport("demo-key", api_base="https://example.com/api/v3")
        with self.assertRaisesRegex(ValueError, "不能为空"):
            UrllibSeedanceTransport("   ")

    def test_success_records_output_without_signed_url_or_credential(self) -> None:
        transport = FakeTransport()
        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "SD-TEST-001"
            summary = run_trial(
                self.contract,
                "SD-TEST-001",
                evidence_dir,
                transport,
                sleep=lambda _seconds: None,
                media_probe=fake_probe,
            )

            self.assertEqual(summary["observation"], "OBSERVED_OUTPUT_AVAILABLE")
            self.assertEqual(summary["visual_quality_acceptance"], "REQUIRES_REVIEW")
            self.assertTrue((evidence_dir / "output.mp4").is_file())
            final_task = json.loads((evidence_dir / "provider_final_task.json").read_text())
            self.assertTrue(final_task["output_url_present"])
            public_text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in evidence_dir.rglob("*")
                if path.is_file() and path.suffix in {".json", ".jsonl"}
            )
            self.assertNotIn("X-Amz-Signature=secret", public_text)
            self.assertNotIn("Bearer", public_text)
            self.assertNotIn("ARK_API_KEY=", public_text)
            self.assertFalse(summary["formal_selection_decision_created"])

            write_json(
                evidence_dir / "environment.json",
                {
                    "execution_id": "SD-TEST-001",
                    "credential_env": "ARK_API_KEY",
                    "credential_present": True,
                    "credential_recorded": False,
                },
            )
            write_manifest(evidence_dir)
            verified = verify(evidence_dir)
            self.assertEqual(
                verified["verification_result"],
                "VERIFIED_SEEDANCE_OBSERVATION_PACKAGE",
            )
            self.assertEqual(verified["sensitive_path_and_credential_scan"], "CLEAR")

    def test_task_mismatch_fails_and_preserves_failure_evidence(self) -> None:
        transport = FakeTransport(mismatched_task=True)
        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "SD-TEST-002"
            with self.assertRaisesRegex(AdapterError, "任务标识"):
                run_trial(
                    self.contract,
                    "SD-TEST-002",
                    evidence_dir,
                    transport,
                    sleep=lambda _seconds: None,
                    media_probe=fake_probe,
                )

            summary = json.loads((evidence_dir / "summary.json").read_text())
            self.assertEqual(summary["observation"], "OBSERVED_REMOTE_EXECUTION_FAILURE")
            self.assertFalse(summary["output_export_completed"])
            self.assertTrue((evidence_dir / "manifest.json").is_file())
            cancellation = json.loads((evidence_dir / "cancellation_attempt.json").read_text())
            self.assertEqual(cancellation["status"], "cancelled")
            self.assertEqual(transport.cancel_count, 1)

    def test_remote_failure_does_not_retry_after_terminal_status(self) -> None:
        transport = FakeTransport(failed=True)
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(AdapterError, "没有成功完成"):
                run_trial(
                    self.contract,
                    "SD-TEST-003",
                    Path(temporary) / "SD-TEST-003",
                    transport,
                    sleep=lambda _seconds: None,
                    media_probe=fake_probe,
                )
        self.assertEqual(transport.query_count, 2)
        self.assertEqual(transport.cancel_count, 0)

    def test_unknown_status_fails_closed_and_does_not_retry(self) -> None:
        transport = FakeTransport(unknown_status=True)
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(AdapterError, "未知任务状态"):
                run_trial(
                    self.contract,
                    "SD-TEST-005",
                    Path(temporary) / "SD-TEST-005",
                    transport,
                    sleep=lambda _seconds: None,
                    media_probe=fake_probe,
                )
        self.assertEqual(transport.query_count, 2)
        self.assertIsNotNone(transport.payload)
        self.assertEqual(transport.cancel_count, 1)

    def test_downloaded_output_with_audio_gap_is_preserved_as_gap(self) -> None:
        transport = FakeTransport()
        invalid_probe = fake_probe(Path("unused")) | {"audio_stream_present": False}
        with tempfile.TemporaryDirectory() as temporary:
            evidence_dir = Path(temporary) / "SD-TEST-004"
            with self.assertRaisesRegex(AdapterError, "音频流"):
                run_trial(
                    self.contract,
                    "SD-TEST-004",
                    evidence_dir,
                    transport,
                    sleep=lambda _seconds: None,
                    media_probe=lambda _path: invalid_probe,
                )
            summary = json.loads((evidence_dir / "summary.json").read_text())
            self.assertEqual(summary["observation"], "OBSERVED_OUTPUT_WITH_TECHNICAL_GAP")
            self.assertTrue(summary["output_export_completed"])
            self.assertTrue((evidence_dir / "output.mp4").is_file())


if __name__ == "__main__":
    unittest.main()
