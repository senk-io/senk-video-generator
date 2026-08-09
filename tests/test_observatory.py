from __future__ import annotations

import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from observatory.server import (
    ObservatoryConfig,
    ObservatoryState,
    WEB_ROOT,
    classify_memory_pressure,
    create_server,
    derive_lifecycle,
)


class ObservatoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.evidence = self.repo / "evidence" / "runtime"
        self.cache = self.root / "cache"
        self.execution_id = "CR-TEST-001"
        self.execution = self.evidence / self.execution_id
        self.execution.mkdir(parents=True)
        (self.repo / "LICENSE").write_text("Apache-2.0\n", encoding="utf-8")
        self._write_json(
            self.execution / "request.json",
            {
                "execution_id": self.execution_id,
                "created_at": "2026-08-09T00:00:00+00:00",
                "contract_id": "TEST-CONTRACT",
                "provider_key": "wan",
                "provider": {
                    "provider_identity": "Wan-AI",
                    "model_id": "Wan-AI/Wan2.1-T2V-1.3B-Diffusers",
                    "width": 416,
                    "height": 240,
                    "num_frames": 17,
                },
                "prompt": "A red paper boat.",
                "seed": 42,
                "device": "mps",
                "timeout_seconds": 60,
            },
        )
        self._write_json(self.execution / "environment.json", {"python_version": "3.12.11"})
        self._write_json(
            self.execution / "worker_state.json",
            {
                "execution_id": self.execution_id,
                "phase": "WORKER_COMPLETED",
                "model_snapshot_resolved": True,
                "pipeline_loaded": True,
                "mps_transfer_completed": True,
                "inference_completed": True,
                "output_export_completed": True,
                "model_snapshot_revision": "revision-1",
            },
        )
        self._write_json(
            self.execution / "summary.json",
            {
                "execution_id": self.execution_id,
                "observation": "OBSERVED_OUTPUT_AVAILABLE",
                "model_snapshot_resolved": True,
                "pipeline_loaded": True,
                "mps_transfer_completed": True,
                "inference_completed": True,
                "output_export_completed": True,
                "formal_fact_created": False,
                "cross_provider_contract_created": False,
                "institution_freeze_created": False,
                "system_start_swap_used_bytes": 0,
                "system_peak_swap_used_bytes": 0,
            },
        )
        (self.execution / "process_metrics.jsonl").write_text(
            json.dumps(
                {
                    "elapsed_seconds": 1,
                    "process_tree_rss_bytes": 100,
                    "system_used_bytes": 200,
                    "system_available_bytes": 300,
                    "swap_used_bytes": 0,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        (self.execution / "runtime.log").write_text(
            f"repo={self.repo}\nhome={Path.home()}\nready\n",
            encoding="utf-8",
        )
        (self.execution / "output.mp4").write_bytes(b"0123456789")
        manifest_files = [
            "request.json",
            "environment.json",
            "worker_state.json",
            "summary.json",
            "process_metrics.jsonl",
            "runtime.log",
            "output.mp4",
        ]
        self._write_json(
            self.execution / "manifest.json",
            {
                "file_count": len(manifest_files),
                "files": [{"path": name, "bytes": 1, "sha256": "a" * 64} for name in manifest_files],
            },
        )
        self.config = ObservatoryConfig(
            repo_root=self.repo,
            evidence_root=self.evidence,
            cache_root=self.cache,
            web_root=WEB_ROOT,
        )
        self.state = ObservatoryState(self.config)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @staticmethod
    def _write_json(path: Path, value: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")

    def test_dashboard_projects_complete_observation_without_authority_upgrade(self) -> None:
        payload = self.state.dashboard()
        selected = payload["selected_execution"]

        self.assertEqual(payload["mode"], "LOCAL_READ_ONLY")
        self.assertEqual(selected["lifecycle"]["state"], "completed_observation")
        self.assertEqual(selected["lifecycle"]["progress_percent"], 100)
        self.assertTrue(all(item["status"] == "completed" for item in selected["lifecycle"]["stages"]))
        self.assertFalse(selected["evidence"]["formal_fact_created"])
        self.assertFalse(selected["evidence"]["institution_freeze_created"])
        self.assertFalse(payload["governance_boundary"]["can_start_generation"])
        self.assertNotIn(str(self.repo), selected["log_tail"])
        self.assertNotIn(str(Path.home()), selected["log_tail"])

    def test_memory_health_marks_high_swap_as_recovering(self) -> None:
        self.assertEqual(
            classify_memory_pressure(36 * 1024**3, 20 * 1024**3, 9 * 1024**3),
            ("recovering", "SWAP_RESIDUE_HIGH"),
        )
        self.assertEqual(
            classify_memory_pressure(36 * 1024**3, 20 * 1024**3, 2 * 1024**3),
            ("healthy", "RESOURCE_READY"),
        )
        self.assertEqual(
            classify_memory_pressure(36 * 1024**3, 2 * 1024**3, 0),
            ("critical", "AVAILABLE_MEMORY_CRITICAL"),
        )

    def test_lifecycle_marks_unclosed_execution_as_waiting(self) -> None:
        (self.execution / "summary.json").unlink()
        (self.execution / "manifest.json").unlink()
        worker = json.loads((self.execution / "worker_state.json").read_text(encoding="utf-8"))
        worker["phase"] = "RUNNING_INFERENCE"
        worker["inference_completed"] = False
        worker["output_export_completed"] = False

        lifecycle = derive_lifecycle(self.execution, worker, {}, active=False)

        self.assertEqual(lifecycle["state"], "interrupted_or_waiting")
        self.assertLess(lifecycle["progress_percent"], 100)
        inference = next(item for item in lifecycle["stages"] if item["id"] == "inference")
        self.assertEqual(inference["status"], "pending")

    def test_lifecycle_distinguishes_active_and_failed_observations(self) -> None:
        worker = json.loads((self.execution / "worker_state.json").read_text(encoding="utf-8"))
        worker["phase"] = "RUNNING_INFERENCE"
        worker["inference_completed"] = False
        worker["output_export_completed"] = False
        active = derive_lifecycle(self.execution, worker, {}, active=True)

        self.assertEqual(active["state"], "active")
        self.assertEqual(active["active_stage"], "inference")
        self.assertEqual(
            next(item for item in active["stages"] if item["id"] == "inference")["status"],
            "active",
        )

        worker["phase"] = "WORKER_FAILED"
        failed = derive_lifecycle(
            self.execution,
            worker,
            {"observation": "OBSERVED_EXECUTION_WITHOUT_OUTPUT"},
            active=False,
        )

        self.assertEqual(failed["state"], "failed_observation")
        self.assertEqual(
            next(item for item in failed["stages"] if item["id"] == "inference")["status"],
            "failed",
        )

    def test_model_cache_distinguishes_ready_and_incomplete(self) -> None:
        wan_revision = "0fad780a534b6463e45facd96134c9f345acfa5b"
        cog_revision = "1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01"
        wan = self.cache / "models--Wan-AI--Wan2.1-T2V-1.3B-Diffusers"
        cog = self.cache / "models--zai-org--CogVideoX-2b"
        (wan / "snapshots" / wan_revision).mkdir(parents=True)
        (wan / "blobs").mkdir()
        (wan / "blobs" / "weight").write_bytes(b"1234")
        (wan / "snapshots" / wan_revision / "model").write_bytes(b"x")
        (cog / "snapshots" / cog_revision).mkdir(parents=True)
        (cog / "blobs").mkdir()
        (cog / "blobs" / "weight.incomplete").write_bytes(b"12")

        models = {item["key"]: item for item in self.state.model_statuses()}

        self.assertEqual(models["wan"]["state"], "ready")
        self.assertEqual(models["wan"]["cache_bytes"], 4)
        self.assertEqual(models["cogvideox"]["state"], "downloading")
        self.assertEqual(models["cogvideox"]["incomplete_file_count"], 1)

    def test_http_api_static_security_and_media_range(self) -> None:
        server = create_server("127.0.0.1", 0, self.state)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_address[1]}"
        try:
            with urlopen(f"{base}/api/v1/dashboard", timeout=3) as response:
                payload = json.load(response)
                self.assertEqual(payload["schema_version"], "observatory.v1")
                self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])
            with urlopen(f"{base}/", timeout=3) as response:
                self.assertIn(b"SENKNET", response.read())
            request = Request(
                f"{base}/media/{self.execution_id}/output.mp4",
                headers={"Range": "bytes=2-5"},
            )
            with urlopen(request, timeout=3) as response:
                self.assertEqual(response.status, 206)
                self.assertEqual(response.read(), b"2345")
            with self.assertRaises(HTTPError) as error:
                urlopen(f"{base}/%2e%2e/LICENSE", timeout=3)
            self.assertEqual(error.exception.code, 404)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

    def test_non_loopback_binding_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            create_server("0.0.0.0", 0, self.state)


if __name__ == "__main__":
    unittest.main()
