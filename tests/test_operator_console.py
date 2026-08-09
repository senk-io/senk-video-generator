from __future__ import annotations

import argparse
import json
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from operator_console.contracts import (
    GIB,
    compile_runner_contract,
    public_catalog,
    validate_job_request,
    validate_persisted_job,
)
from operator_console.server import ControlError, JobManager, WEB_ROOT, create_server
from tools.run_provider_compatibility_trial import (
    activate_pipeline_strategy,
    configure_mps_memory_limit,
    load_execution_contract,
    observe_resource_budget,
    release_pipeline_memory,
)
from tools.verify_provider_compatibility_evidence import verify_operator_memory_contract


class FakeObserver:
    def __init__(self, active: bool = False, available_bytes: int = 16 * GIB) -> None:
        self.active = active
        self.available_bytes = available_bytes

    def model_statuses(self) -> list[dict]:
        return [
            {
                "key": "wan",
                "state": "ready",
                "observed_revision_present": True,
                "incomplete_file_count": 0,
                "cache_bytes": 27 * GIB,
            },
            {
                "key": "cogvideox",
                "state": "ready",
                "observed_revision_present": True,
                "incomplete_file_count": 0,
                "cache_bytes": 13 * GIB,
            },
        ]

    def system_status(self) -> dict:
        return {
            "cpu_percent": 10,
            "logical_cpu_count": 12,
            "memory": {
                "total_bytes": 36 * GIB,
                "used_bytes": 20 * GIB,
                "available_bytes": self.available_bytes,
                "used_percent": 55.6,
                "pressure": "healthy",
            },
            "swap": {"total_bytes": 32 * GIB, "used_bytes": 2 * GIB, "used_percent": 6.25},
            "disk": {"total_bytes": 100 * GIB, "used_bytes": 40 * GIB, "free_bytes": 60 * GIB, "used_percent": 40},
        }

    def active_processes(self) -> list[dict]:
        return [{"pid": 999, "execution_id": "OTHER"}] if self.active else []


class OperatorConsoleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.state_root = self.root / "state"
        self.evidence = self.root / "evidence"
        self.cache = self.root / "cache"
        self.repo.mkdir()
        self.evidence.mkdir()
        runner_dir = self.root / "tools"
        runner_dir.mkdir()
        self.runner = runner_dir / "run_provider_compatibility_trial.py"
        self.runner.write_text(
            """
import argparse
import json
import time
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--provider')
parser.add_argument('--execution-id')
parser.add_argument('--job-spec')
parser.add_argument('--evidence-root')
args = parser.parse_args()
job = json.loads(Path(args.job_spec).read_text())
if job['prompt'] == 'sleep':
    time.sleep(60)
else:
    root = Path(args.evidence_root) / args.execution_id
    root.mkdir(parents=True)
    (root / 'summary.json').write_text(json.dumps({'observation': 'OBSERVED_OUTPUT_AVAILABLE'}))
""".strip()
            + "\n",
            encoding="utf-8",
        )
        self.manager = JobManager(
            repo_root=self.repo,
            state_root=self.state_root,
            evidence_root=self.evidence,
            cache_root=self.cache,
            runner_path=self.runner,
        )
        self.manager.observer = FakeObserver()

    def tearDown(self) -> None:
        for job_id, process in list(self.manager._processes.items()):
            if process.poll() is None:
                process.kill()
                process.wait(timeout=3)
            self.manager._processes.pop(job_id, None)
        self.temporary.cleanup()

    def request(self, execution_id: str = "LOCAL-WAN-TEST-001", prompt: str = "A red paper boat.") -> dict:
        catalog = public_catalog()
        profile = next(item for item in catalog["generation_profiles"] if item["key"] == "wan_probe")
        return {
            "provider_key": "wan",
            "task_type": "text_to_video",
            "generation_profile_key": "wan_probe",
            "execution_strategy": "mps_model_offload_bounded",
            "execution_id": execution_id,
            "prompt": prompt,
            "seed": 42,
            "parameters": profile["parameters"],
            "timeout_seconds": 3600,
            "preflight_min_available_memory_bytes": 10 * GIB,
            "abort_min_available_memory_bytes": 3 * GIB,
            "max_swap_growth_bytes": 8 * GIB,
            "mps_memory_fraction": 0.75,
            "risk_acknowledged": True,
        }

    def test_contract_validation_and_runner_compilation(self) -> None:
        normalized, errors = validate_job_request(self.request())

        self.assertEqual(errors, [])
        self.assertIsNotNone(normalized)
        normalized["job_id"] = "JOB-20260809T000000Z-A1B2C3D4"
        contract = compile_runner_contract(normalized)
        self.assertEqual(contract["shared_prompt"], "A red paper boat.")
        self.assertEqual(contract["providers"]["wan"]["width"], 256)
        self.assertEqual(contract["generation_profile_key"], "wan_probe")
        self.assertEqual(contract["execution_strategy"], "mps_model_offload_bounded")
        self.assertEqual(contract["resource_budget"]["mps_memory_fraction"], 0.75)
        self.assertEqual(contract["resource_budget"]["max_swap_growth_bytes"], 8 * GIB)
        self.assertEqual(contract["contract_status"], "LOCAL_OPERATOR_JOB_NON_AUTHORITATIVE")

    def test_persisted_job_is_loaded_by_runner_without_model_import(self) -> None:
        job = self.manager.create_job(self.request())
        job_spec = self.state_root / "jobs" / job["job_id"] / "request.json"

        contract, source = load_execution_contract(
            argparse.Namespace(job_spec=str(job_spec), provider="wan")
        )

        self.assertEqual(source, job_spec.resolve())
        self.assertEqual(contract["job_id"], job["job_id"])
        self.assertEqual(contract["providers"]["wan"]["num_frames"], 9)

    def test_resource_budget_requires_sustained_low_memory_and_blocks_swap_growth(self) -> None:
        samples = 0
        reason = None
        for _ in range(5):
            samples, reason = observe_resource_budget(
                available_bytes=2 * GIB,
                swap_used_bytes=2 * GIB,
                swap_start_bytes=2 * GIB,
                abort_min_available_bytes=3 * GIB,
                max_swap_growth_bytes=8 * GIB,
                low_available_samples=samples,
            )
            self.assertIsNone(reason)
        samples, reason = observe_resource_budget(
            available_bytes=2 * GIB,
            swap_used_bytes=2 * GIB,
            swap_start_bytes=2 * GIB,
            abort_min_available_bytes=3 * GIB,
            max_swap_growth_bytes=8 * GIB,
            low_available_samples=samples,
        )
        self.assertEqual(reason, "SYSTEM_AVAILABLE_MEMORY_BELOW_BUDGET")

        _, reason = observe_resource_budget(
            available_bytes=12 * GIB,
            swap_used_bytes=11 * GIB,
            swap_start_bytes=2 * GIB,
            abort_min_available_bytes=3 * GIB,
            max_swap_growth_bytes=8 * GIB,
            low_available_samples=0,
        )
        self.assertEqual(reason, "SYSTEM_SWAP_GROWTH_EXCEEDED_BUDGET")

    def test_mps_limit_strategy_activation_and_release_are_explicit(self) -> None:
        class FakeMps:
            fraction = None
            synchronized = False
            cache_emptied = False

            @staticmethod
            def recommended_max_memory() -> int:
                return 30_000

            def set_per_process_memory_fraction(self, fraction: float) -> None:
                self.fraction = fraction

            def synchronize(self) -> None:
                self.synchronized = True

            def empty_cache(self) -> None:
                self.cache_emptied = True

            @staticmethod
            def current_allocated_memory() -> int:
                return 100

            @staticmethod
            def driver_allocated_memory() -> int:
                return 200

        class FakePipe:
            model_cpu_offload_seq = "text_encoder->transformer->vae"

            def __init__(self) -> None:
                self.offload_device = None
                self.full_device = None

            def enable_model_cpu_offload(self, device: str) -> None:
                self.offload_device = device

            def to(self, device: str) -> None:
                self.full_device = device

        mps = FakeMps()
        limit = configure_mps_memory_limit(mps, 0.75)
        staged = FakePipe()
        activation = activate_pipeline_strategy(staged, "mps_model_offload_bounded")
        full = FakePipe()
        full_activation = activate_pipeline_strategy(full, "mps_full_bounded")
        release = release_pipeline_memory(SimpleNamespace(mps=mps))

        self.assertEqual(limit["configured_limit_bytes"], 22_500)
        self.assertEqual(mps.fraction, 0.75)
        self.assertEqual(staged.offload_device, "mps")
        self.assertEqual(activation["offload_sequence"], "text_encoder->transformer->vae")
        self.assertEqual(full.full_device, "mps")
        self.assertTrue(full_activation["full_pipeline_transfer"])
        self.assertTrue(mps.synchronized)
        self.assertTrue(mps.cache_emptied)
        self.assertEqual(release["driver_allocated_bytes"], 200)

    def test_profile_parameters_and_mps_fraction_are_fail_closed(self) -> None:
        request = self.request()
        request["parameters"] = {**request["parameters"], "num_frames": 17}
        request["mps_memory_fraction"] = 1.0

        normalized, errors = validate_job_request(request)
        codes = {error["code"] for error in errors}

        self.assertIsNone(normalized)
        self.assertIn("PROFILE_PARAMETER_MISMATCH", codes)
        self.assertIn("OUT_OF_BOUNDS", codes)

    def test_operator_evidence_requires_matching_memory_contract(self) -> None:
        request = {
            "contract_status": "LOCAL_OPERATOR_JOB_NON_AUTHORITATIVE",
            "generation_profile_key": "wan_probe",
            "execution_strategy": "mps_model_offload_bounded",
            "resource_budget": {"mps_memory_fraction": 0.75},
        }
        summary = {
            "execution_strategy": "mps_model_offload_bounded",
            "mps_memory_limit": {"fraction": 0.75},
            "mps_strategy_activation": {"strategy": "mps_model_offload_bounded"},
            "inference_completed": True,
            "mps_post_release": {
                "current_allocated_bytes": 0,
                "driver_allocated_bytes": 0,
            },
        }

        verify_operator_memory_contract(request, summary)
        summary["mps_post_release"] = None
        with self.assertRaisesRegex(ValueError, "主动释放"):
            verify_operator_memory_contract(request, summary)

    def test_unavailable_provider_missing_prompt_and_invalid_budget_are_blocked(self) -> None:
        cog = self.request()
        cog["provider_key"] = "cogvideox"
        cog["prompt"] = ""
        cog_profile = next(item for item in public_catalog()["generation_profiles"] if item["key"] == "cogvideox_probe")
        cog["generation_profile_key"] = "cogvideox_probe"
        cog["parameters"] = cog_profile["parameters"]
        cog["abort_min_available_memory_bytes"] = cog["preflight_min_available_memory_bytes"]

        normalized, errors = validate_job_request(cog)
        codes = {error["code"] for error in errors}

        self.assertIsNone(normalized)
        self.assertIn("PROVIDER_RUNTIME_BLOCKED", codes)
        self.assertIn("PROMPT_REQUIRED", codes)
        self.assertIn("INVALID_MEMORY_BUDGET_ORDER", codes)

    def test_preflight_checks_memory_active_process_and_execution_identity(self) -> None:
        self.manager.observer = FakeObserver(active=True, available_bytes=8 * GIB)
        (self.evidence / "LOCAL-WAN-TEST-001").mkdir()

        result = self.manager.preflight(self.request())
        blocked = {check["id"] for check in result["checks"] if check["status"] == "blocked"}

        self.assertFalse(result["passed"])
        self.assertIn("NO_ACTIVE_GENERATION", blocked)
        self.assertIn("AVAILABLE_MEMORY", blocked)
        self.assertIn("EXECUTION_ID_UNUSED", blocked)

        mps_check = next(check for check in result["checks"] if check["id"] == "MPS_MEMORY_LIMIT_CONFIGURED")
        self.assertEqual(mps_check["status"], "passed")
        self.assertEqual(mps_check["details"]["mps_memory_fraction"], 0.75)

    def test_job_registration_is_immutable_and_event_chain_is_linked(self) -> None:
        job = self.manager.create_job(self.request())
        job_dir = self.state_root / "jobs" / job["job_id"]
        request_path = job_dir / "request.json"
        persisted = json.loads(request_path.read_text(encoding="utf-8"))
        validated, errors = validate_persisted_job(persisted)

        self.assertEqual(job["state"], "REGISTERED")
        self.assertEqual(errors, [])
        self.assertEqual(validated["execution_id"], "LOCAL-WAN-TEST-001")
        events = [json.loads(line) for line in (job_dir / "events.jsonl").read_text().splitlines()]
        self.assertEqual(events[0]["previous_record_sha256"], None)

        persisted["prompt"] = "tampered"
        request_path.write_text(json.dumps(persisted), encoding="utf-8")
        with self.assertRaises(ControlError) as error:
            self.manager.job_detail(job["job_id"])
        self.assertEqual(error.exception.code, "REQUEST_DIGEST_MISMATCH")

    def test_tampered_event_chain_is_rejected(self) -> None:
        job = self.manager.create_job(self.request())
        events_path = self.state_root / "jobs" / job["job_id"] / "events.jsonl"
        event = json.loads(events_path.read_text(encoding="utf-8"))
        event["payload"]["request_sha256"] = "tampered"
        events_path.write_text(json.dumps(event) + "\n", encoding="utf-8")

        with self.assertRaises(ControlError) as error:
            self.manager.job_detail(job["job_id"])
        self.assertEqual(error.exception.code, "EVENT_CHAIN_INVALID")

    def test_exact_confirmation_is_required_and_fake_job_completes(self) -> None:
        job = self.manager.create_job(self.request())
        with self.assertRaises(ControlError) as error:
            self.manager.start_job(job["job_id"], "WRONG-ID")
        self.assertEqual(error.exception.code, "CONFIRMATION_MISMATCH")

        started = self.manager.start_job(job["job_id"], job["execution_id"])
        self.assertIn(started["state"], {"RUNNING", "COMPLETED"})
        final = self.wait_for_terminal(job["job_id"])
        self.assertEqual(final["state"], "COMPLETED")
        self.assertEqual(final["terminal_reason"], "OBSERVED_OUTPUT_AVAILABLE")

    def test_stop_terminates_only_matching_fake_job(self) -> None:
        job = self.manager.create_job(self.request("LOCAL-WAN-SLEEP-001", "sleep"))
        self.manager.start_job(job["job_id"], job["execution_id"])

        stopped = self.manager.stop_job(job["job_id"])
        self.assertIn(stopped["state"], {"STOP_REQUESTED", "STOPPED"})
        final = self.wait_for_terminal(job["job_id"])
        self.assertEqual(final["state"], "STOPPED")
        self.assertEqual(final["terminal_reason"], "LOCAL_OPERATOR_STOP")

    def test_http_requires_csrf_and_blocks_path_traversal(self) -> None:
        server = create_server("127.0.0.1", 0, self.manager, WEB_ROOT)
        import threading

        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_address[1]}"
        try:
            with urlopen(f"{base}/api/v1/operator", timeout=3) as response:
                overview = json.load(response)
                token = overview["csrf_token"]
                self.assertEqual(overview["mode"], "LOCAL_CONTROLLED_EXECUTION")
            body = json.dumps(self.request()).encode()
            request = Request(
                f"{base}/api/v1/preflight",
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with self.assertRaises(HTTPError) as error:
                urlopen(request, timeout=3)
            self.assertEqual(error.exception.code, 403)
            request.add_header("X-Senknet-CSRF", token)
            with urlopen(request, timeout=3) as response:
                self.assertTrue(json.load(response)["passed"])
            with self.assertRaises(HTTPError) as traversal:
                urlopen(f"{base}/%2e%2e/README.md", timeout=3)
            self.assertEqual(traversal.exception.code, 404)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

    def test_non_loopback_binding_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            create_server("0.0.0.0", 0, self.manager)

    def wait_for_terminal(self, job_id: str) -> dict:
        deadline = time.monotonic() + 6
        while time.monotonic() < deadline:
            job = self.manager.job_detail(job_id)
            if job["state"] in {"COMPLETED", "FAILED", "STOPPED"}:
                return job
            time.sleep(0.05)
        self.fail("作业没有在测试时限内进入终态")


if __name__ == "__main__":
    unittest.main()
