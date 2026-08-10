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

import numpy as np

from operator_console.contracts import (
    GIB,
    compile_runner_contract,
    public_catalog,
    validate_job_request,
    validate_persisted_job,
)
from operator_console.server import ControlError, JobManager, WEB_ROOT, create_server
from tools.run_provider_compatibility_trial import (
    WorkerStageFailure,
    activate_pipeline_strategy,
    build_cogvideox_denoiser_pipeline,
    build_wan_denoiser_pipeline,
    configure_mps_memory_limit,
    load_execution_contract,
    max_jsonl_metric,
    normalize_mps_float64_buffers,
    observe_resource_budget,
    prepare_cogvideox_prompt_embeddings,
    prepare_wan_prompt_embeddings,
    request_worker_stop,
    release_pipeline_memory,
    validate_bounded_trial_variant,
)
from tools.decode_cogvideox_latent import preflight_block_reason, validate_decode_source
from tools.verify_provider_compatibility_evidence import verify_operator_memory_contract, verify_staged_prompt_release
from tools.stabilize_cogvideox_candidate import (
    stabilize_frames,
    subject_observation,
    threshold_comparisons,
    validate_contract as validate_stability_contract,
)


class FakeObserver:
    def __init__(
        self,
        active: bool = False,
        available_bytes: int = 16 * GIB,
        swap_used_bytes: int = 2 * GIB,
    ) -> None:
        self.active = active
        self.available_bytes = available_bytes
        self.swap_used_bytes = swap_used_bytes

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
            "swap": {
                "total_bytes": 32 * GIB,
                "used_bytes": self.swap_used_bytes,
                "used_percent": round(self.swap_used_bytes / (32 * GIB) * 100, 2),
            },
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
            "preflight_min_available_memory_bytes": 16 * GIB,
            "preflight_max_swap_used_bytes": 4 * GIB,
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
        self.assertEqual(contract["resource_budget"]["preflight_max_swap_used_bytes"], 4 * GIB)
        self.assertEqual(contract["resource_budget"]["max_swap_growth_bytes"], 8 * GIB)
        self.assertEqual(contract["contract_status"], "LOCAL_OPERATOR_JOB_NON_AUTHORITATIVE")
        quality_profile = next(
            item for item in public_catalog()["generation_profiles"] if item["key"] == "wan_quality_probe"
        )
        self.assertEqual(quality_profile["parameters"]["width"], 256)
        self.assertEqual(quality_profile["parameters"]["num_inference_steps"], 4)
        balance_profile = next(
            item for item in public_catalog()["generation_profiles"] if item["key"] == "wan_balance_probe"
        )
        self.assertEqual(balance_profile["parameters"]["width"], 256)
        self.assertEqual(balance_profile["parameters"]["num_inference_steps"], 16)
        backtest_profile = next(
            item for item in public_catalog()["generation_profiles"] if item["key"] == "wan_balance_backtest"
        )
        self.assertEqual(backtest_profile["parameters"]["width"], 256)
        self.assertEqual(backtest_profile["parameters"]["num_inference_steps"], 8)
        self.assertEqual(backtest_profile["name"], "推荐平衡")
        self.assertEqual(public_catalog()["defaults"]["generation_profile_key"], "wan_balance_backtest")

    def test_persisted_job_is_loaded_by_runner_without_model_import(self) -> None:
        job = self.manager.create_job(self.request())
        job_spec = self.state_root / "jobs" / job["job_id"] / "request.json"

        contract, source = load_execution_contract(
            argparse.Namespace(job_spec=str(job_spec), provider="wan")
        )

        self.assertEqual(source, job_spec.resolve())
        self.assertEqual(contract["job_id"], job["job_id"])
        self.assertEqual(contract["providers"]["wan"]["num_frames"], 9)

    def test_bounded_cogvideox_quality_and_five_second_contracts_are_fail_closed(self) -> None:
        contract_path = Path("experiments/provider_compatibility/cogvideox_quality_8_steps.json").resolve()
        contract, source = load_execution_contract(
            argparse.Namespace(job_spec=None, trial_contract=str(contract_path), provider="cogvideox")
        )

        self.assertEqual(source, contract_path)
        self.assertEqual(contract["providers"]["cogvideox"]["num_inference_steps"], 8)
        mutated = json.loads(json.dumps(contract))
        mutated["providers"]["cogvideox"]["width"] = 704
        with self.assertRaisesRegex(ValueError, "不得改变提供者基线字段"):
            validate_bounded_trial_variant(mutated, "cogvideox")

        five_second_path = Path(
            "experiments/provider_compatibility/cogvideox_five_second_16_steps.json"
        ).resolve()
        five_second, source = load_execution_contract(
            argparse.Namespace(job_spec=None, trial_contract=str(five_second_path), provider="cogvideox")
        )
        self.assertEqual(source, five_second_path)
        self.assertEqual(five_second["providers"]["cogvideox"]["num_frames"], 41)
        self.assertEqual(five_second["providers"]["cogvideox"]["num_inference_steps"], 16)
        self.assertEqual(five_second["temporal_derivation"]["derived_frame_count"], 40)
        self.assertEqual(five_second["temporal_derivation"]["duration_seconds"], 5.0)

        mutated_five_second = json.loads(json.dumps(five_second))
        mutated_five_second["providers"]["cogvideox"]["num_frames"] = 45
        with self.assertRaisesRegex(ValueError, "只允许 41 帧和 16 步"):
            validate_bounded_trial_variant(mutated_five_second, "cogvideox")

        mutated_derivation = json.loads(json.dumps(five_second))
        mutated_derivation["temporal_derivation"]["derived_frame_count"] = 39
        with self.assertRaisesRegex(ValueError, "派生合同必须固定"):
            validate_bounded_trial_variant(mutated_derivation, "cogvideox")

        thirty_two_path = Path(
            "experiments/provider_compatibility/cogvideox_quality_32_steps.json"
        ).resolve()
        thirty_two, source = load_execution_contract(
            argparse.Namespace(job_spec=None, trial_contract=str(thirty_two_path), provider="cogvideox")
        )
        self.assertEqual(source, thirty_two_path)
        self.assertEqual(thirty_two["providers"]["cogvideox"]["num_frames"], 9)
        self.assertEqual(thirty_two["providers"]["cogvideox"]["num_inference_steps"], 32)

        mutated_thirty_two = json.loads(json.dumps(thirty_two))
        mutated_thirty_two["non_goals"].remove("five_second_generation")
        with self.assertRaisesRegex(ValueError, "三十二步探针缺少"):
            validate_bounded_trial_variant(mutated_thirty_two, "cogvideox")

        origami_path = Path(
            "experiments/provider_compatibility/cogvideox_quality_32_steps_origami_prompt.json"
        ).resolve()
        origami, source = load_execution_contract(
            argparse.Namespace(job_spec=None, trial_contract=str(origami_path), provider="cogvideox")
        )
        self.assertEqual(source, origami_path)
        self.assertEqual(origami["providers"]["cogvideox"]["num_inference_steps"], 32)
        self.assertIn("triangular creases", origami["shared_prompt"])

        mutated_origami = json.loads(json.dumps(origami))
        mutated_origami["shared_prompt"] = mutated_origami["shared_prompt"].replace(
            "triangular creases", "paper folds"
        )
        with self.assertRaisesRegex(ValueError, "必须固定为已登记的单提示词变量"):
            validate_bounded_trial_variant(mutated_origami, "cogvideox")

        shot_two_path = Path(
            "experiments/provider_compatibility/cogvideox_quality_32_steps_shot_002.json"
        ).resolve()
        shot_two, source = load_execution_contract(
            argparse.Namespace(job_spec=None, trial_contract=str(shot_two_path), provider="cogvideox")
        )
        self.assertEqual(source, shot_two_path)
        self.assertEqual(shot_two["prompt_variant"]["shot_id"], "SHOT-002")
        self.assertEqual(shot_two["providers"]["cogvideox"]["num_frames"], 9)
        mutated_shot_two = json.loads(json.dumps(shot_two))
        mutated_shot_two["shared_prompt"] = mutated_shot_two["shared_prompt"].replace(
            "left to right", "right to left"
        )
        with self.assertRaisesRegex(ValueError, "已登记的单提示词变量"):
            validate_bounded_trial_variant(mutated_shot_two, "cogvideox")

        origami_five_second_path = Path(
            "experiments/provider_compatibility/cogvideox_five_second_32_steps_origami.json"
        ).resolve()
        origami_five_second, source = load_execution_contract(
            argparse.Namespace(
                job_spec=None,
                trial_contract=str(origami_five_second_path),
                provider="cogvideox",
            )
        )
        self.assertEqual(source, origami_five_second_path)
        self.assertEqual(origami_five_second["providers"]["cogvideox"]["num_frames"], 41)
        self.assertEqual(origami_five_second["providers"]["cogvideox"]["num_inference_steps"], 32)
        self.assertEqual(origami_five_second["temporal_derivation"]["derived_frame_count"], 40)
        self.assertEqual(
            origami_five_second["resource_budget_basis"]["decision"],
            "KEEP_EXISTING_HARD_LIMITS",
        )

        mutated_origami_five_second = json.loads(json.dumps(origami_five_second))
        mutated_origami_five_second["providers"]["cogvideox"]["num_frames"] = 45
        with self.assertRaisesRegex(ValueError, "折纸五秒探针只允许 41 帧和 32 步"):
            validate_bounded_trial_variant(mutated_origami_five_second, "cogvideox")

        mutated_origami_budget = json.loads(json.dumps(origami_five_second))
        mutated_origami_budget["resource_budget_basis"]["decision"] = "RELAX_LIMITS"
        with self.assertRaisesRegex(ValueError, "资源预算依据无效"):
            validate_bounded_trial_variant(mutated_origami_budget, "cogvideox")

        shot_two_five_second_path = Path(
            "experiments/provider_compatibility/cogvideox_five_second_32_steps_shot_002.json"
        ).resolve()
        shot_two_five_second, source = load_execution_contract(
            argparse.Namespace(
                job_spec=None,
                trial_contract=str(shot_two_five_second_path),
                provider="cogvideox",
            )
        )
        self.assertEqual(source, shot_two_five_second_path)
        self.assertEqual(
            shot_two_five_second["providers"]["cogvideox"]["num_frames"],
            41,
        )
        self.assertEqual(
            shot_two_five_second["temporal_derivation"]["derived_frame_count"],
            40,
        )
        self.assertEqual(
            shot_two_five_second["resource_budget_basis"]["decision"],
            "KEEP_EXISTING_HARD_LIMITS",
        )
        mutated_shot_two_five_second = json.loads(json.dumps(shot_two_five_second))
        mutated_shot_two_five_second["resource_budget"]["mps_memory_fraction"] = 0.75
        with self.assertRaisesRegex(ValueError, "不得改变固定字段"):
            validate_bounded_trial_variant(mutated_shot_two_five_second, "cogvideox")

        mutated_shot_two_five_second_budget = json.loads(json.dumps(shot_two_five_second))
        mutated_shot_two_five_second_budget["resource_budget_basis"]["decision"] = "RELAX_LIMITS"
        with self.assertRaisesRegex(ValueError, "第二镜头五秒探针资源预算依据无效"):
            validate_bounded_trial_variant(mutated_shot_two_five_second_budget, "cogvideox")

    def test_cogvideox_temporal_stability_contract_and_linear_trajectory_are_fail_closed(self) -> None:
        contract_path = Path(
            "experiments/postprocessing/cogvideox_temporal_stability_v1.json"
        )
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        validate_stability_contract(contract)
        mutated = json.loads(json.dumps(contract))
        mutated["temporal_filter"]["weights"] = [1, 2, 1]
        with self.assertRaisesRegex(ValueError, "混合权重"):
            validate_stability_contract(mutated)

        origami_contract_path = Path(
            "experiments/postprocessing/cogvideox_origami_temporal_stability_v1.json"
        )
        origami_contract = json.loads(origami_contract_path.read_text(encoding="utf-8"))
        validate_stability_contract(origami_contract)
        self.assertEqual(
            origami_contract["source"]["execution_id"],
            "LM-COGVIDEOX-5S-32STEP-ORIGAMI-20260809T194654Z",
        )
        mutated_origami_contract = json.loads(json.dumps(origami_contract))
        mutated_origami_contract["source"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "来源合同无效"):
            validate_stability_contract(mutated_origami_contract)

        frames = np.full((4, 32, 48, 3), 240, dtype=np.uint8)
        for index, x in enumerate((4, 18, 8, 22)):
            frames[index, 12:22, x : x + 12] = (230, 20, 20)
        measurement = {
            "red_minimum": 150,
            "red_to_green_ratio_numerator": 3,
            "red_to_green_ratio_denominator": 2,
            "red_to_blue_ratio_numerator": 3,
            "red_to_blue_ratio_denominator": 2,
            "minimum_subject_area_pixels": 100,
        }
        source = subject_observation(frames, measurement)
        stabilized, shifts = stabilize_frames(
            frames,
            source,
            {
                "maximum_translation_pixels": 32,
            },
            {"weights": [1, 4, 1]},
        )
        observed = subject_observation(stabilized, measurement)
        comparisons = threshold_comparisons(
            observed,
            {
                "all_frames_retain_subject": True,
                "maximum_adjacent_centroid_jump_pixels": 7.0,
                "mean_adjacent_centroid_jump_pixels": 7.0,
                "maximum_adjacent_subject_area_change_percent": 1.0,
            },
        )
        self.assertEqual(len(shifts), 4)
        self.assertTrue(observed["all_frames_retain_subject"])
        self.assertTrue(all(item["within_threshold"] for item in comparisons.values()))

    def test_legacy_v2_job_remains_readable_with_new_swap_gate(self) -> None:
        job = self.manager.create_job(self.request())
        job_spec = self.state_root / "jobs" / job["job_id"] / "request.json"
        persisted = json.loads(job_spec.read_text(encoding="utf-8"))
        persisted["schema_version"] = "operator-job.v2"
        persisted["resource_budget"].pop("preflight_max_swap_used_bytes")

        normalized, errors = validate_persisted_job(persisted)

        self.assertEqual(errors, [])
        self.assertEqual(normalized["resource_budget"]["preflight_max_swap_used_bytes"], 4 * GIB)

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

    def test_decode_preflight_accepts_only_normal_pressure_swap_residue(self) -> None:
        self.assertIsNone(preflight_block_reason(20 * GIB, 5 * GIB, 1))
        self.assertEqual(
            preflight_block_reason(20 * GIB, 5 * GIB, 2),
            "启动前换页高于 4 GiB，且系统内存压力并非正常级",
        )
        self.assertEqual(
            preflight_block_reason(20 * GIB, 5 * GIB, None),
            "启动前换页高于 4 GiB，且系统内存压力并非正常级",
        )
        self.assertEqual(preflight_block_reason(15 * GIB, 2 * GIB, 1), "启动前可用内存不足 16 GiB")

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

    def test_cogvideox_float64_position_buffer_is_normalized_for_mps(self) -> None:
        import torch

        class PositionModule(torch.nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.register_buffer("pos_embedding", torch.ones((1, 4, 8), dtype=torch.float64))

        module = torch.nn.Module()
        module.patch_embed = PositionModule()

        observations = normalize_mps_float64_buffers(module, torch)

        self.assertEqual(module.patch_embed.pos_embedding.dtype, torch.float32)
        self.assertEqual(observations[0]["buffer"], "patch_embed.pos_embedding")
        self.assertEqual(observations[0]["shape"], [1, 4, 8])

    def test_cogvideox_decode_retry_requires_matching_latent_digest(self) -> None:
        source_root = self.evidence / "COG-LATENT-SOURCE-001"
        source_root.mkdir()
        latent_path = source_root / "denoised_latents.safetensors"
        latent_path.write_bytes(b"bounded-latent-test")
        digest = __import__("hashlib").sha256(latent_path.read_bytes()).hexdigest()
        (source_root / "summary.json").write_text(
            json.dumps(
                {
                    "latent_checkpoint": {
                        "path": latent_path.name,
                        "sha256": digest,
                    }
                }
            ),
            encoding="utf-8",
        )

        source = validate_decode_source(self.evidence, source_root.name)
        self.assertEqual(source["latent_sha256"], digest)

        latent_path.write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError, "摘要不匹配"):
            validate_decode_source(self.evidence, source_root.name)

    def test_wan_text_encoder_is_released_before_denoiser_load(self) -> None:
        events: list[str] = []

        class FakeTensor:
            def detach(self):
                return self

            def to(self, *_args, **_kwargs):
                return self

        class FakeMps:
            @staticmethod
            def synchronize() -> None:
                events.append("mps_synchronize")

            @staticmethod
            def empty_cache() -> None:
                events.append("mps_empty_cache")

            @staticmethod
            def current_allocated_memory() -> int:
                return 0

            @staticmethod
            def driver_allocated_memory() -> int:
                return 0

        class FakeInferenceMode:
            def __enter__(self):
                events.append("inference_mode_enter")

            def __exit__(self, *_args):
                events.append("inference_mode_exit")

        fake_torch = SimpleNamespace(
            bfloat16="bfloat16",
            float32="float32",
            device=lambda value: value,
            inference_mode=FakeInferenceMode,
            mps=FakeMps(),
        )

        def component(name: str):
            class Component:
                @classmethod
                def from_pretrained(cls, *_args, **_kwargs):
                    events.append(name)
                    return cls()

            return Component

        class FakePipeline:
            model_cpu_offload_seq = "text_encoder->transformer->vae"

            def __init__(self, **kwargs) -> None:
                self.kwargs = kwargs
                events.append("pipeline")

            def enable_sequential_cpu_offload(self, device: str) -> None:
                events.append(f"sequential_offload:{device}")

            def encode_prompt(self, **_kwargs):
                events.append("encode_prompt")
                return FakeTensor(), FakeTensor()

            def remove_all_hooks(self) -> None:
                events.append("release_text_encoder")

            def enable_attention_slicing(self) -> None:
                events.append("attention_slicing")

        prompt = prepare_wan_prompt_embeddings(
            Path("/snapshot"),
            "A paper boat.",
            fake_torch,
            component("tokenizer"),
            component("text_encoder"),
            FakePipeline,
        )
        pipe = build_wan_denoiser_pipeline(
            Path("/snapshot"),
            fake_torch,
            component("transformer"),
            component("vae"),
            component("scheduler"),
            FakePipeline,
        )

        self.assertIsInstance(prompt["prompt_embeds"], FakeTensor)
        self.assertEqual(prompt["activation"]["strategy"], "mps_sequential_cpu_offload")
        self.assertIn("sequential_offload:mps", events)
        self.assertLess(events.index("inference_mode_enter"), events.index("encode_prompt"))
        self.assertLess(events.index("encode_prompt"), events.index("inference_mode_exit"))
        self.assertLess(events.index("release_text_encoder"), events.index("transformer"))
        self.assertIsNone(pipe.kwargs["text_encoder"])
        self.assertIsNone(pipe.kwargs["tokenizer"])

        observations: dict[str, dict] = {}

        class FailingPipeline(FakePipeline):
            def encode_prompt(self, **_kwargs):
                raise RuntimeError("受控文本编码失败")

        with self.assertRaises(WorkerStageFailure) as failure:
            prepare_wan_prompt_embeddings(
                Path("/snapshot"),
                "A paper boat.",
                fake_torch,
                component("tokenizer_failed"),
                component("text_encoder_failed"),
                FailingPipeline,
                lambda field, value: observations.__setitem__(field, value),
            )

        self.assertEqual(failure.exception.observation["type"], "RuntimeError")
        self.assertEqual(
            observations["prompt_stage_activation"]["strategy"],
            "mps_sequential_cpu_offload",
        )
        self.assertEqual(observations["text_encoder_post_release"]["driver_allocated_bytes"], 0)

    def test_cogvideox_text_encoder_is_released_before_denoiser_load(self) -> None:
        events: list[str] = []
        encode_options: dict = {}

        class FakeTensor:
            def detach(self):
                return self

            def to(self, *_args, **_kwargs):
                return self

        class FakeMps:
            synchronize = staticmethod(lambda: events.append("mps_synchronize"))
            empty_cache = staticmethod(lambda: events.append("mps_empty_cache"))
            current_allocated_memory = staticmethod(lambda: 0)
            driver_allocated_memory = staticmethod(lambda: 0)

        class FakeInferenceMode:
            def __enter__(self):
                events.append("inference_mode_enter")

            def __exit__(self, *_args):
                events.append("inference_mode_exit")

        fake_torch = SimpleNamespace(
            float16="float16",
            float32="float32",
            device=lambda value: value,
            inference_mode=FakeInferenceMode,
            mps=FakeMps(),
        )

        def component(name: str):
            class Component:
                @classmethod
                def from_pretrained(cls, *_args, **_kwargs):
                    events.append(name)
                    return cls()

            return Component

        class FakeVae:
            def enable_slicing(self) -> None:
                events.append("vae_slicing")

            def enable_tiling(self) -> None:
                events.append("vae_tiling")

        class FakeVaeComponent:
            @classmethod
            def from_pretrained(cls, *_args, **_kwargs):
                events.append("vae")
                return FakeVae()

        class FakePipeline:
            def __init__(self, **kwargs) -> None:
                self.kwargs = kwargs
                self.vae = kwargs.get("vae")
                events.append("pipeline")

            def enable_sequential_cpu_offload(self, device: str) -> None:
                events.append(f"sequential_offload:{device}")

            def encode_prompt(self, **kwargs):
                encode_options.update(kwargs)
                events.append("encode_prompt")
                return FakeTensor(), FakeTensor()

            def remove_all_hooks(self) -> None:
                events.append("release_text_encoder")

            def enable_attention_slicing(self) -> None:
                events.append("attention_slicing")

        prompt = prepare_cogvideox_prompt_embeddings(
            Path("/snapshot"),
            "A paper boat.",
            fake_torch,
            component("tokenizer"),
            component("text_encoder"),
            FakePipeline,
        )
        pipe = build_cogvideox_denoiser_pipeline(
            Path("/snapshot"),
            fake_torch,
            component("transformer"),
            FakeVaeComponent,
            component("scheduler"),
            FakePipeline,
        )

        self.assertIsInstance(prompt["prompt_embeds"], FakeTensor)
        self.assertEqual(encode_options["max_sequence_length"], 226)
        self.assertEqual(encode_options["dtype"], "float16")
        self.assertLess(events.index("release_text_encoder"), events.index("transformer"))
        self.assertIsNone(pipe.kwargs["text_encoder"])
        self.assertIn("vae_tiling", events)

    def test_parent_stop_and_metric_fallback_preserve_abort_evidence(self) -> None:
        class FakeChild:
            terminated = False

            def terminate(self) -> None:
                self.terminated = True

        evidence_dir = self.root / "stop-evidence"
        evidence_dir.mkdir()
        child = FakeChild()
        request_worker_stop(evidence_dir, child, "SYSTEM_SWAP_GROWTH_EXCEEDED_BUDGET")
        metrics = evidence_dir / "mps_metrics.jsonl"
        metrics.write_text(
            '\n'.join(
                [
                    json.dumps({"mps_driver_allocated_bytes": 100}),
                    json.dumps({"mps_driver_allocated_bytes": 400}),
                    json.dumps({"mps_driver_allocated_bytes": 250}),
                ]
            )
            + '\n',
            encoding="utf-8",
        )

        stop_request = json.loads((evidence_dir / "stop_request.json").read_text(encoding="utf-8"))
        self.assertTrue(child.terminated)
        self.assertEqual(stop_request["reason"], "SYSTEM_SWAP_GROWTH_EXCEEDED_BUDGET")
        self.assertEqual(max_jsonl_metric(metrics, "mps_driver_allocated_bytes"), 400)

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
            "provider_key": "wan",
            "generation_profile_key": "wan_probe",
            "execution_strategy": "mps_model_offload_bounded",
            "resource_budget": {
                "mps_memory_fraction": 0.75,
                "preflight_max_swap_used_bytes": 4 * GIB,
            },
        }
        summary = {
            "execution_strategy": "mps_model_offload_bounded",
            "mps_memory_limit": {"fraction": 0.75},
            "mps_strategy_activation": {"strategy": "mps_model_offload_bounded"},
            "prompt_stage_activation": {"strategy": "mps_sequential_cpu_offload"},
            "component_residency_strategy": "PRECOMPUTE_PROMPT_THEN_RELEASE_TEXT_ENCODER",
            "prompt_encoding_completed": True,
            "text_encoder_post_release": {
                "current_allocated_bytes": 0,
                "driver_allocated_bytes": 0,
            },
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

        verify_staged_prompt_release(summary | {"mps_post_release": {"current_allocated_bytes": 0}})
        with self.assertRaisesRegex(ValueError, "文本编码器释放观察"):
            verify_staged_prompt_release(summary | {"text_encoder_post_release": None})

        early_failure = {
            "execution_strategy": "mps_model_offload_bounded",
            "mps_memory_limit": {"fraction": 0.75},
            "mps_strategy_activation": None,
            "mps_transfer_completed": False,
            "component_residency_strategy": "PRECOMPUTE_PROMPT_THEN_RELEASE_TEXT_ENCODER",
            "prompt_encoding_completed": False,
            "pipeline_loaded": False,
            "inference_completed": False,
        }
        verify_operator_memory_contract(request, early_failure)

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

    def test_preflight_blocks_high_existing_swap_during_recovery(self) -> None:
        self.manager.observer = FakeObserver(swap_used_bytes=9 * GIB)

        result = self.manager.preflight(self.request("LOCAL-WAN-SWAP-RECOVERY-001"))
        swap_check = next(check for check in result["checks"] if check["id"] == "SWAP_RECOVERY_READY")

        self.assertFalse(result["passed"])
        self.assertEqual(swap_check["status"], "blocked")
        self.assertIn("最多允许", swap_check["message"])

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
