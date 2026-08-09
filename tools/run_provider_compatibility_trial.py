#!/usr/bin/env python3
"""运行一个有界的视频提供者兼容性试验并生成公开安全的证据包。"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
import platform
import queue
import re
import signal
import subprocess
import sys
import threading
import time
import traceback
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import psutil


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = REPO_ROOT / "experiments/provider_compatibility/trial_contract.json"
DEFAULT_EVIDENCE_ROOT = REPO_ROOT / "evidence/runtime"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from operator_console.contracts import compile_runner_contract, validate_persisted_job

PRIVATE_PATH_PATTERNS = (
    re.compile(r"/Users/[^/\s]+"),
    re.compile(r"/home/[^/\s]+"),
)


class WorkerTerminationRequested(RuntimeError):
    """父进程请求工作进程保存终止证据并释放资源。"""


class WorkerStageFailure(RuntimeError):
    """阶段失败已经转换为不持有模型张量的公开安全观察。"""

    def __init__(self, observation: dict[str, Any]) -> None:
        super().__init__(str(observation.get("message", "工作阶段失败")))
        self.observation = observation


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def sanitize_text(value: str) -> str:
    sanitized = value.replace(str(REPO_ROOT), "<repo>")
    home = str(Path.home())
    sanitized = sanitized.replace(home, "<home>")
    for pattern in PRIVATE_PATH_PATTERNS:
        sanitized = pattern.sub("<private-user-path>", sanitized)
    return sanitized


def sanitized_exception(exc: BaseException) -> dict[str, Any]:
    frames = []
    for frame in traceback.extract_tb(exc.__traceback__):
        path = Path(frame.filename)
        try:
            filename = str(path.resolve().relative_to(REPO_ROOT))
        except (OSError, ValueError):
            filename = f"{path.parent.name}/{path.name}"
        frames.append({"file": filename, "line": frame.lineno, "function": frame.name})
    return {
        "type": type(exc).__name__,
        "message": sanitize_text(str(exc)),
        "frames": frames,
    }


def observe_resource_budget(
    *,
    available_bytes: int,
    swap_used_bytes: int,
    swap_start_bytes: int,
    abort_min_available_bytes: int,
    max_swap_growth_bytes: int,
    low_available_samples: int,
) -> tuple[int, str | None]:
    if abort_min_available_bytes and available_bytes < abort_min_available_bytes:
        low_available_samples += 1
    else:
        low_available_samples = 0
    if low_available_samples >= 6:
        return low_available_samples, "SYSTEM_AVAILABLE_MEMORY_BELOW_BUDGET"
    if max_swap_growth_bytes and swap_used_bytes - swap_start_bytes > max_swap_growth_bytes:
        return low_available_samples, "SYSTEM_SWAP_GROWTH_EXCEEDED_BUDGET"
    return low_available_samples, None


def configure_mps_memory_limit(mps: Any, fraction: float) -> dict[str, Any]:
    recommended_bytes = int(mps.recommended_max_memory())
    mps.set_per_process_memory_fraction(float(fraction))
    return {
        "fraction": float(fraction),
        "recommended_max_memory_bytes": recommended_bytes,
        "configured_limit_bytes": int(recommended_bytes * float(fraction)),
    }


def activate_pipeline_strategy(pipe: Any, strategy: str, device: str = "mps") -> dict[str, Any]:
    if strategy == "mps_model_offload_bounded":
        pipe.enable_model_cpu_offload(device=device)
        return {
            "strategy": strategy,
            "offload_sequence": getattr(pipe, "model_cpu_offload_seq", None),
            "full_pipeline_transfer": False,
        }
    if strategy == "mps_full_bounded":
        pipe.to(device)
        return {
            "strategy": strategy,
            "offload_sequence": None,
            "full_pipeline_transfer": True,
        }
    raise ValueError(f"不受支持的执行策略：{strategy}")


def activate_prompt_encoding_strategy(pipe: Any, device: str = "mps") -> dict[str, Any]:
    """以叶级顺序卸载运行超大文本编码器，避免整模型同时进入 MPS。"""
    pipe.enable_sequential_cpu_offload(device=device)
    return {
        "strategy": "mps_sequential_cpu_offload",
        "offload_granularity": "leaf_module",
        "full_text_encoder_transfer": False,
    }


def release_pipeline_memory(torch_module: Any) -> dict[str, int]:
    gc.collect()
    torch_module.mps.synchronize()
    torch_module.mps.empty_cache()
    return {
        "current_allocated_bytes": int(torch_module.mps.current_allocated_memory()),
        "driver_allocated_bytes": int(torch_module.mps.driver_allocated_memory()),
    }


def request_worker_stop(evidence_dir: Path, child: subprocess.Popen[str], reason: str) -> None:
    write_json(
        evidence_dir / "stop_request.json",
        {"reason": reason, "requested_at": utc_now()},
    )
    child.terminate()


def load_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_execution_contract(args: argparse.Namespace) -> tuple[dict[str, Any], Path]:
    if not args.job_spec:
        return load_contract(), CONTRACT_PATH
    job_spec_path = Path(args.job_spec).resolve()
    try:
        raw_job = json.loads(job_spec_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"无法读取作业规格：{type(exc).__name__}") from exc
    job, errors = validate_persisted_job(raw_job)
    if errors or job is None:
        codes = ", ".join(error["code"] for error in errors)
        raise SystemExit(f"作业规格验证失败：{codes}")
    if job["provider_key"] != args.provider:
        raise SystemExit("作业规格提供者与命令行提供者不一致")
    return compile_runner_contract(job), job_spec_path


def git_value(*args: str) -> str | None:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.stdout.strip() or None if result.returncode == 0 else None


def processor_identity() -> str:
    result = subprocess.run(
        ["sysctl", "-n", "machdep.cpu.brand_string"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else platform.processor()


def hardware_environment(execution_id: str, contract_path: Path) -> dict[str, Any]:
    import accelerate
    import diffusers
    import huggingface_hub
    import imageio_ffmpeg
    import torch
    import transformers

    total_memory = psutil.virtual_memory().total
    return {
        "execution_id": execution_id,
        "recorded_at": utc_now(),
        "operating_system": platform.system(),
        "operating_system_version": platform.mac_ver()[0],
        "architecture": platform.machine(),
        "processor": processor_identity(),
        "logical_cpu_count": psutil.cpu_count(logical=True),
        "physical_memory_bytes": total_memory,
        "python_version": platform.python_version(),
        "torch_version": torch.__version__,
        "diffusers_version": diffusers.__version__,
        "transformers_version": transformers.__version__,
        "accelerate_version": accelerate.__version__,
        "huggingface_hub_version": huggingface_hub.__version__,
        "mps_built": torch.backends.mps.is_built(),
        "mps_available": torch.backends.mps.is_available(),
        "mps_recommended_max_memory_bytes": (
            torch.mps.recommended_max_memory() if torch.backends.mps.is_available() else None
        ),
        "bundled_ffmpeg_version": imageio_ffmpeg.get_ffmpeg_version(),
        "git_head": git_value("rev-parse", "HEAD"),
        "git_status_porcelain": git_value("status", "--porcelain") or "",
        "harness_sha256": sha256_file(Path(__file__)),
        "contract_sha256": sha256_file(contract_path),
        "contract_source": "operator_job" if contract_path != CONTRACT_PATH else "fixed_trial",
        "sensitive_machine_identifiers_recorded": False,
    }


def process_tree_rss(process: psutil.Process) -> int:
    processes = [process]
    try:
        processes.extend(process.children(recursive=True))
    except (psutil.Error, OSError):
        pass
    total = 0
    for item in processes:
        try:
            total += item.memory_info().rss
        except (psutil.Error, OSError):
            continue
    return total


def log_reader(stream: Any, output_path: Path, message_queue: queue.Queue[str]) -> None:
    with output_path.open("w", encoding="utf-8") as handle:
        for line in iter(stream.readline, ""):
            safe_line = sanitize_text(line)
            handle.write(safe_line)
            handle.flush()
            message_queue.put(safe_line)
    stream.close()


def write_manifest(evidence_dir: Path) -> dict[str, Any]:
    entries = []
    for path in sorted(evidence_dir.rglob("*")):
        if not path.is_file() or path.name == "manifest.json":
            continue
        entries.append(
            {
                "path": str(path.relative_to(evidence_dir)),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    manifest = {
        "created_at": utc_now(),
        "file_count": len(entries),
        "files": entries,
    }
    write_json(evidence_dir / "manifest.json", manifest)
    return manifest


def max_jsonl_metric(path: Path, field: str) -> int | None:
    maximum: int | None = None
    if not path.is_file():
        return None
    try:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                try:
                    value = json.loads(line).get(field)
                except (json.JSONDecodeError, AttributeError):
                    continue
                if isinstance(value, (int, float)):
                    maximum = max(maximum or 0, int(value))
    except (OSError, UnicodeDecodeError):
        return None
    return maximum


def run_parent(args: argparse.Namespace) -> int:
    contract, contract_path = load_execution_contract(args)
    provider = contract["providers"][args.provider]
    evidence_root = Path(args.evidence_root).resolve() if args.evidence_root else DEFAULT_EVIDENCE_ROOT
    evidence_dir = evidence_root / args.execution_id
    if evidence_dir.exists():
        raise SystemExit(f"证据目录已经存在，拒绝覆盖：{evidence_dir}")
    evidence_dir.mkdir(parents=True)

    request = {
        "execution_id": args.execution_id,
        "created_at": utc_now(),
        "contract_id": contract["contract_id"],
        "contract_status": contract.get("contract_status"),
        "job_id": contract.get("job_id"),
        "task_type": contract.get("task_type", "text_to_video"),
        "generation_profile_key": contract.get("generation_profile_key"),
        "execution_strategy": contract.get("execution_strategy", "mps_full_bounded"),
        "resource_budget": contract.get("resource_budget"),
        "provider_key": args.provider,
        "provider": provider,
        "prompt": contract["shared_prompt"],
        "seed": contract["shared_seed"],
        "device": contract["device"],
        "mps_fallback_to_cpu": contract["mps_fallback_to_cpu"],
        "timeout_seconds": contract["timeout_seconds"],
        "formal_fact_creation": "PROHIBITED",
        "cross_provider_contract_creation": "PROHIBITED",
    }
    write_json(evidence_dir / "request.json", request)
    write_json(evidence_dir / "environment.json", hardware_environment(args.execution_id, contract_path))

    child_args = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--worker",
        "--provider",
        args.provider,
        "--execution-id",
        args.execution_id,
        "--evidence-root",
        str(evidence_root),
    ]
    if args.job_spec:
        child_args.extend(["--job-spec", str(Path(args.job_spec).resolve())])
    child_environment = os.environ.copy()
    child_environment["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
    child_environment["HF_HUB_DISABLE_TELEMETRY"] = "1"
    child_environment["TOKENIZERS_PARALLELISM"] = "false"

    started_at = utc_now()
    start = time.perf_counter()
    system_start = psutil.virtual_memory()
    swap_start = psutil.swap_memory()
    child = subprocess.Popen(
        child_args,
        cwd=REPO_ROOT,
        env=child_environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
    )
    child_process = psutil.Process(child.pid)
    messages: queue.Queue[str] = queue.Queue()
    reader = threading.Thread(
        target=log_reader,
        args=(child.stdout, evidence_dir / "runtime.log", messages),
        daemon=True,
    )
    reader.start()

    metrics_path = evidence_dir / "process_metrics.jsonl"
    peak_rss = 0
    peak_system_used = system_start.total - system_start.available
    peak_swap_used = swap_start.used
    timed_out = False
    safety_abort_reason: str | None = None
    low_available_samples = 0
    timeout_seconds = int(contract["timeout_seconds"])
    resource_budget = contract.get("resource_budget") or {}
    abort_min_available = int(resource_budget.get("abort_min_available_memory_bytes") or 0)
    max_swap_growth = int(resource_budget.get("max_swap_growth_bytes") or 0)
    with metrics_path.open("w", encoding="utf-8") as metrics:
        while child.poll() is None:
            elapsed = time.perf_counter() - start
            if elapsed > timeout_seconds:
                timed_out = True
                request_worker_stop(evidence_dir, child, "EXECUTION_TIMEOUT")
                try:
                    child.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    child.kill()
                break
            rss = process_tree_rss(child_process)
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            peak_rss = max(peak_rss, rss)
            peak_system_used = max(peak_system_used, memory.total - memory.available)
            peak_swap_used = max(peak_swap_used, swap.used)
            low_available_samples, safety_abort_reason = observe_resource_budget(
                available_bytes=memory.available,
                swap_used_bytes=swap.used,
                swap_start_bytes=swap_start.used,
                abort_min_available_bytes=abort_min_available,
                max_swap_growth_bytes=max_swap_growth,
                low_available_samples=low_available_samples,
            )
            metrics.write(
                json.dumps(
                    {
                        "elapsed_seconds": round(elapsed, 3),
                        "process_tree_rss_bytes": rss,
                        "system_used_bytes": memory.total - memory.available,
                        "system_available_bytes": memory.available,
                        "swap_used_bytes": swap.used,
                    },
                    sort_keys=True,
                )
                + "\n"
            )
            metrics.flush()
            if safety_abort_reason:
                request_worker_stop(evidence_dir, child, safety_abort_reason)
                try:
                    child.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    child.kill()
                break
            while True:
                try:
                    print(messages.get_nowait(), end="", flush=True)
                except queue.Empty:
                    break
            time.sleep(0.5)

    return_code = child.wait()
    reader.join(timeout=10)
    while True:
        try:
            print(messages.get_nowait(), end="", flush=True)
        except queue.Empty:
            break

    worker_state_path = evidence_dir / "worker_state.json"
    worker_state = (
        json.loads(worker_state_path.read_text(encoding="utf-8"))
        if worker_state_path.exists()
        else {"phase": "WORKER_STATE_UNAVAILABLE"}
    )
    stop_request_path = evidence_dir / "stop_request.json"
    try:
        parent_stop_request = json.loads(stop_request_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        parent_stop_request = None
    elapsed_seconds = time.perf_counter() - start
    output_path = evidence_dir / "output.mp4"
    thumbnail_path = evidence_dir / "thumbnail.png"
    inference_completed = bool(worker_state.get("inference_completed"))
    output_export_completed = output_path.exists() and bool(worker_state.get("output_export_completed"))
    observation = (
        "OBSERVED_OUTPUT_AVAILABLE"
        if return_code == 0 and inference_completed and output_export_completed
        else "OBSERVED_EXECUTION_WITHOUT_OUTPUT"
    )
    summary = {
        "execution_id": args.execution_id,
        "provider_key": args.provider,
        "provider_identity": provider["provider_identity"],
        "model_id": provider["model_id"],
        "started_at": started_at,
        "finished_at": utc_now(),
        "elapsed_seconds": round(elapsed_seconds, 3),
        "worker_exit_code": return_code,
        "timed_out": timed_out,
        "safety_abort_reason": safety_abort_reason,
        "job_id": contract.get("job_id"),
        "contract_status": contract.get("contract_status"),
        "generation_profile_key": contract.get("generation_profile_key"),
        "execution_strategy": contract.get("execution_strategy", "mps_full_bounded"),
        "mps_memory_fraction": resource_budget.get("mps_memory_fraction"),
        "observation": observation,
        "last_phase": worker_state.get("phase"),
        "model_snapshot_resolved": bool(worker_state.get("model_snapshot_resolved")),
        "pipeline_loaded": bool(worker_state.get("pipeline_loaded")),
        "mps_transfer_completed": bool(worker_state.get("mps_transfer_completed")),
        "inference_completed": inference_completed,
        "output_export_completed": output_export_completed,
        "stage_elapsed_seconds": worker_state.get("stage_elapsed_seconds", {}),
        "process_tree_peak_rss_bytes": peak_rss,
        "system_start_used_bytes": system_start.total - system_start.available,
        "system_peak_used_bytes": peak_system_used,
        "system_start_swap_used_bytes": swap_start.used,
        "system_peak_swap_used_bytes": peak_swap_used,
        "mps_peak_current_allocated_bytes": worker_state.get("mps_peak_current_allocated_bytes")
        if worker_state.get("mps_peak_current_allocated_bytes") is not None
        else max_jsonl_metric(evidence_dir / "mps_metrics.jsonl", "mps_current_allocated_bytes"),
        "mps_peak_driver_allocated_bytes": worker_state.get("mps_peak_driver_allocated_bytes")
        if worker_state.get("mps_peak_driver_allocated_bytes") is not None
        else max_jsonl_metric(evidence_dir / "mps_metrics.jsonl", "mps_driver_allocated_bytes"),
        "mps_memory_limit": worker_state.get("mps_memory_limit"),
        "mps_strategy_activation": worker_state.get("mps_strategy_activation"),
        "prompt_stage_activation": worker_state.get("prompt_stage_activation"),
        "mps_post_release": worker_state.get("mps_post_release"),
        "component_residency_strategy": worker_state.get("component_residency_strategy"),
        "prompt_encoding_completed": bool(worker_state.get("prompt_encoding_completed")),
        "text_encoder_post_release": worker_state.get("text_encoder_post_release"),
        "mps_dtype_normalization": worker_state.get("mps_dtype_normalization", []),
        "decode_strategy": worker_state.get("decode_strategy"),
        "denoising_completed": bool(worker_state.get("denoising_completed")),
        "mps_post_denoise_release": worker_state.get("mps_post_denoise_release"),
        "stop_request": worker_state.get("stop_request") or parent_stop_request,
        "model_snapshot_revision": worker_state.get("model_snapshot_revision"),
        "output_sha256": sha256_file(output_path) if output_path.exists() else None,
        "output_bytes": output_path.stat().st_size if output_path.exists() else None,
        "thumbnail_sha256": sha256_file(thumbnail_path) if thumbnail_path.exists() else None,
        "output_metadata": worker_state.get("output_metadata"),
        "error_observation": worker_state.get("error_observation"),
        "formal_fact_created": False,
        "cross_provider_contract_created": False,
        "institution_freeze_created": False,
    }
    write_json(evidence_dir / "summary.json", summary)
    manifest = write_manifest(evidence_dir)
    print(json.dumps({**summary, "manifest_file_count": manifest["file_count"]}, ensure_ascii=False, indent=2))
    return 0 if observation == "OBSERVED_OUTPUT_AVAILABLE" else 1


class MpsSampler:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._sample, daemon=True)
        self.start = time.perf_counter()
        self.peak_current = 0
        self.peak_driver = 0
        self.started = False

    def _sample(self) -> None:
        import torch

        with self.path.open("w", encoding="utf-8") as handle:
            while not self.stop_event.is_set():
                try:
                    current = torch.mps.current_allocated_memory()
                    driver = torch.mps.driver_allocated_memory()
                except RuntimeError:
                    current = 0
                    driver = 0
                self.peak_current = max(self.peak_current, current)
                self.peak_driver = max(self.peak_driver, driver)
                handle.write(
                    json.dumps(
                        {
                            "elapsed_seconds": round(time.perf_counter() - self.start, 3),
                            "mps_current_allocated_bytes": current,
                            "mps_driver_allocated_bytes": driver,
                        },
                        sort_keys=True,
                    )
                    + "\n"
                )
                handle.flush()
                self.stop_event.wait(0.25)

    def __enter__(self) -> "MpsSampler":
        self.start_sampling()
        return self

    def __exit__(self, *_: Any) -> None:
        self.stop_sampling()

    def start_sampling(self) -> None:
        if self.started:
            return
        self.started = True
        self.thread.start()

    def stop_sampling(self) -> None:
        if not self.started:
            return
        self.stop_event.set()
        self.thread.join(timeout=5)
        self.started = False


def prepare_wan_prompt_embeddings(
    snapshot_path: Path,
    prompt: str,
    torch_module: Any,
    tokenizer_class: Any,
    text_encoder_class: Any,
    pipeline_class: Any,
    observation_callback: Any = None,
) -> dict[str, Any]:
    """以叶级顺序卸载形成提示词嵌入，随后在装载 Transformer 前完整释放。"""
    stage_pipe = None
    tokenizer = None
    text_encoder = None
    result: dict[str, Any] = {}
    error_observation: dict[str, Any] | None = None
    try:
        tokenizer = tokenizer_class.from_pretrained(
            snapshot_path,
            subfolder="tokenizer",
            local_files_only=True,
        )
        text_encoder = text_encoder_class.from_pretrained(
            snapshot_path,
            subfolder="text_encoder",
            torch_dtype=torch_module.bfloat16,
            low_cpu_mem_usage=True,
            local_files_only=True,
        )
        stage_pipe = pipeline_class(
            tokenizer=tokenizer,
            text_encoder=text_encoder,
            vae=None,
            scheduler=None,
            transformer=None,
        )
        result["activation"] = activate_prompt_encoding_strategy(stage_pipe, "mps")
        if observation_callback is not None:
            observation_callback("prompt_stage_activation", result["activation"])
        with torch_module.inference_mode():
            prompt_embeds, negative_prompt_embeds = stage_pipe.encode_prompt(
                prompt=prompt,
                negative_prompt="",
                do_classifier_free_guidance=True,
                num_videos_per_prompt=1,
                max_sequence_length=512,
                device=torch_module.device("mps"),
                dtype=torch_module.bfloat16,
            )
        torch_module.mps.synchronize()
        result["prompt_embeds"] = prompt_embeds.detach().to("cpu")
        result["negative_prompt_embeds"] = negative_prompt_embeds.detach().to("cpu")
        prompt_embeds = None
        negative_prompt_embeds = None
    except BaseException as exc:
        error_observation = sanitized_exception(exc)
        exc.__traceback__ = None
    finally:
        if stage_pipe is not None and hasattr(stage_pipe, "remove_all_hooks"):
            stage_pipe.remove_all_hooks()
        elif stage_pipe is not None and hasattr(stage_pipe, "maybe_free_model_hooks"):
            stage_pipe.maybe_free_model_hooks()
        stage_pipe = None
        text_encoder = None
        tokenizer = None
        result["post_release"] = release_pipeline_memory(torch_module)
        if observation_callback is not None:
            observation_callback("text_encoder_post_release", result["post_release"])
    if error_observation is not None:
        raise WorkerStageFailure(error_observation) from None
    return result


def build_wan_denoiser_pipeline(
    snapshot_path: Path,
    torch_module: Any,
    transformer_class: Any,
    vae_class: Any,
    scheduler_class: Any,
    pipeline_class: Any,
) -> Any:
    """在文本编码器释放后，仅装载去噪和解码所需组件。"""
    transformer = transformer_class.from_pretrained(
        snapshot_path,
        subfolder="transformer",
        torch_dtype=torch_module.bfloat16,
        low_cpu_mem_usage=True,
        local_files_only=True,
    )
    vae = vae_class.from_pretrained(
        snapshot_path,
        subfolder="vae",
        torch_dtype=torch_module.float32,
        low_cpu_mem_usage=True,
        local_files_only=True,
    )
    scheduler = scheduler_class.from_pretrained(
        snapshot_path,
        subfolder="scheduler",
        local_files_only=True,
    )
    pipe = pipeline_class(
        tokenizer=None,
        text_encoder=None,
        vae=vae,
        scheduler=scheduler,
        transformer=transformer,
    )
    pipe.enable_attention_slicing()
    return pipe


def normalize_mps_float64_buffers(module: Any, torch_module: Any) -> list[dict[str, Any]]:
    """把模型中 MPS 无法承载的 float64 缓冲区降为 float32。"""
    normalized: list[dict[str, Any]] = []
    for full_name, buffer in list(module.named_buffers()):
        if buffer.dtype != torch_module.float64:
            continue
        parent_name, _, buffer_name = full_name.rpartition(".")
        parent = module.get_submodule(parent_name) if parent_name else module
        converted = buffer.to(dtype=torch_module.float32)
        setattr(parent, buffer_name, converted)
        normalized.append(
            {
                "buffer": full_name,
                "from_dtype": "float64",
                "to_dtype": "float32",
                "shape": list(buffer.shape),
            }
        )
    return normalized


def run_worker(args: argparse.Namespace) -> int:
    import imageio.v2 as imageio
    import numpy as np
    import torch
    from diffusers import AutoencoderKLWan, CogVideoXPipeline, WanPipeline, WanTransformer3DModel
    from diffusers.schedulers import UniPCMultistepScheduler
    from diffusers.utils import export_to_video
    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer, UMT5EncoderModel

    contract, _ = load_execution_contract(args)
    provider = contract["providers"][args.provider]
    evidence_dir = Path(args.evidence_root).resolve() / args.execution_id
    state_path = evidence_dir / "worker_state.json"
    state: dict[str, Any] = {
        "execution_id": args.execution_id,
        "provider_key": args.provider,
        "phase": "WORKER_STARTED",
        "started_at": utc_now(),
        "model_snapshot_resolved": False,
        "pipeline_loaded": False,
        "mps_transfer_completed": False,
        "inference_completed": False,
        "output_export_completed": False,
        "stage_elapsed_seconds": {},
        "generation_profile_key": contract.get("generation_profile_key"),
        "execution_strategy": contract.get("execution_strategy", "mps_full_bounded"),
        "mps_memory_limit": None,
        "mps_strategy_activation": None,
        "mps_post_release": None,
        "component_residency_strategy": None,
        "prompt_encoding_completed": False,
        "text_encoder_post_release": None,
        "mps_dtype_normalization": [],
        "decode_strategy": "PIPELINE_DEFAULT",
        "denoising_completed": False,
        "mps_post_denoise_release": None,
    }
    write_json(state_path, state)
    sampler: MpsSampler | None = None
    pipe: Any = None
    prompt_embeds: Any = None
    negative_prompt_embeds: Any = None

    def handle_parent_stop(_signum: int, _frame: Any) -> None:
        raise WorkerTerminationRequested("父进程请求保存终止证据并释放资源")

    def record_prompt_observation(field: str, value: Any) -> None:
        state[field] = value
        write_json(state_path, state)

    signal.signal(signal.SIGTERM, handle_parent_stop)
    try:
        if not torch.backends.mps.is_available():
            raise RuntimeError("PyTorch MPS backend is unavailable")

        resource_budget = contract.get("resource_budget") or {}
        state["phase"] = "CONFIGURING_MPS_BUDGET"
        if resource_budget.get("mps_memory_fraction") is not None:
            state["mps_memory_limit"] = configure_mps_memory_limit(
                torch.mps,
                float(resource_budget["mps_memory_fraction"]),
            )
        else:
            state["mps_memory_limit"] = {
                "fraction": None,
                "recommended_max_memory_bytes": int(torch.mps.recommended_max_memory()),
                "configured_limit_bytes": None,
            }
        write_json(state_path, state)
        sampler = MpsSampler(evidence_dir / "mps_metrics.jsonl")
        sampler.start_sampling()

        stage_start = time.perf_counter()
        state["phase"] = "RESOLVING_MODEL_SNAPSHOT"
        write_json(state_path, state)
        snapshot_path = Path(snapshot_download(provider["model_id"]))
        state["model_snapshot_resolved"] = True
        state["model_snapshot_revision"] = snapshot_path.name
        state["stage_elapsed_seconds"]["snapshot_resolution"] = round(time.perf_counter() - stage_start, 3)
        execution_strategy = contract.get("execution_strategy", "mps_full_bounded")
        if args.provider == "wan" and execution_strategy == "mps_model_offload_bounded":
            state["component_residency_strategy"] = "PRECOMPUTE_PROMPT_THEN_RELEASE_TEXT_ENCODER"
            state["phase"] = "ENCODING_PROMPT"
            write_json(state_path, state)
            stage_start = time.perf_counter()
            prompt_stage = prepare_wan_prompt_embeddings(
                snapshot_path,
                contract["shared_prompt"],
                torch,
                AutoTokenizer,
                UMT5EncoderModel,
                WanPipeline,
                record_prompt_observation,
            )
            prompt_embeds = prompt_stage["prompt_embeds"]
            negative_prompt_embeds = prompt_stage["negative_prompt_embeds"]
            state["prompt_encoding_completed"] = True
            state["prompt_stage_activation"] = prompt_stage["activation"]
            state["text_encoder_post_release"] = prompt_stage["post_release"]
            state["stage_elapsed_seconds"]["prompt_encoding_and_release"] = round(
                time.perf_counter() - stage_start,
                3,
            )
            prompt_stage = None
            state["phase"] = "LOADING_DENOISER_PIPELINE"
            write_json(state_path, state)
            stage_start = time.perf_counter()
            pipe = build_wan_denoiser_pipeline(
                snapshot_path,
                torch,
                WanTransformer3DModel,
                AutoencoderKLWan,
                UniPCMultistepScheduler,
                WanPipeline,
            )
        else:
            state["component_residency_strategy"] = "FULL_PIPELINE_LOAD"
            state["phase"] = "LOADING_PIPELINE"
            write_json(state_path, state)
            stage_start = time.perf_counter()
            if args.provider == "wan":
                vae = AutoencoderKLWan.from_pretrained(
                    snapshot_path,
                    subfolder="vae",
                    torch_dtype=torch.float32,
                    low_cpu_mem_usage=True,
                    local_files_only=True,
                )
                pipe = WanPipeline.from_pretrained(
                    snapshot_path,
                    vae=vae,
                    torch_dtype=torch.bfloat16,
                    low_cpu_mem_usage=True,
                    local_files_only=True,
                )
                pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config, flow_shift=3.0)
                del vae
            else:
                pipe = CogVideoXPipeline.from_pretrained(
                    snapshot_path,
                    torch_dtype=torch.float16,
                    low_cpu_mem_usage=True,
                    local_files_only=True,
                )
                pipe.vae.enable_slicing()
                pipe.vae.enable_tiling()
                state["mps_dtype_normalization"] = normalize_mps_float64_buffers(
                    pipe.transformer,
                    torch,
                )
            pipe.enable_attention_slicing()
        state["pipeline_loaded"] = True
        state["stage_elapsed_seconds"]["pipeline_load"] = round(time.perf_counter() - stage_start, 3)
        state["phase"] = "ACTIVATING_MPS_STRATEGY"
        write_json(state_path, state)

        stage_start = time.perf_counter()
        state["mps_strategy_activation"] = activate_pipeline_strategy(
            pipe,
            contract.get("execution_strategy", "mps_full_bounded"),
            "mps",
        )
        torch.mps.synchronize()
        state["mps_transfer_completed"] = True
        state["stage_elapsed_seconds"]["mps_strategy_activation"] = round(time.perf_counter() - stage_start, 3)
        state["stage_elapsed_seconds"]["mps_transfer"] = state["stage_elapsed_seconds"]["mps_strategy_activation"]
        state["phase"] = "RUNNING_INFERENCE"
        write_json(state_path, state)

        generator = torch.Generator(device="cpu").manual_seed(contract["shared_seed"])
        stage_start = time.perf_counter()
        inference_prompt: dict[str, Any]
        if prompt_embeds is not None:
            prompt_embeds = prompt_embeds.to(device="mps", dtype=pipe.transformer.dtype)
            negative_prompt_embeds = negative_prompt_embeds.to(device="mps", dtype=pipe.transformer.dtype)
            inference_prompt = {
                "prompt": None,
                "prompt_embeds": prompt_embeds,
                "negative_prompt_embeds": negative_prompt_embeds,
            }
        else:
            inference_prompt = {"prompt": contract["shared_prompt"]}
        output = pipe(
            **inference_prompt,
            height=provider["height"],
            width=provider["width"],
            num_frames=provider["num_frames"],
            num_inference_steps=provider["num_inference_steps"],
            guidance_scale=provider["guidance_scale"],
            generator=generator,
            output_type="latent" if args.provider == "cogvideox" else "np",
        )
        torch.mps.synchronize()
        if args.provider == "cogvideox":
            state["denoising_completed"] = True
            state["decode_strategy"] = "LATENT_TO_CPU_THEN_VAE_CPU_TILED"
            state["phase"] = "RELEASING_DENOISER_BEFORE_CPU_DECODE"
            write_json(state_path, state)
            latent_video = output.frames.detach().to(device="cpu", dtype=torch.float32)
            del output
            if hasattr(pipe, "remove_all_hooks"):
                pipe.remove_all_hooks()
            elif hasattr(pipe, "maybe_free_model_hooks"):
                pipe.maybe_free_model_hooks()
            pipe.text_encoder = None
            pipe.transformer = None
            prompt_embeds = None
            negative_prompt_embeds = None
            state["mps_post_denoise_release"] = release_pipeline_memory(torch)
            state["phase"] = "DECODING_VIDEO_ON_CPU"
            write_json(state_path, state)
            decode_start = time.perf_counter()
            pipe.vae.to(device="cpu", dtype=torch.float32)
            with torch.inference_mode():
                decoded_video = pipe.decode_latents(latent_video)
                frames = pipe.video_processor.postprocess_video(
                    video=decoded_video,
                    output_type="np",
                )[0]
            del latent_video
            del decoded_video
            state["stage_elapsed_seconds"]["cpu_vae_decode"] = round(
                time.perf_counter() - decode_start,
                3,
            )
        else:
            frames = output.frames[0]
            del output
        state["inference_completed"] = True
        state["mps_peak_current_allocated_bytes"] = sampler.peak_current
        state["mps_peak_driver_allocated_bytes"] = sampler.peak_driver
        state["stage_elapsed_seconds"]["inference"] = round(time.perf_counter() - stage_start, 3)
        state["phase"] = "RELEASING_MPS_MEMORY"
        write_json(state_path, state)
        release_start = time.perf_counter()
        if hasattr(pipe, "maybe_free_model_hooks"):
            pipe.maybe_free_model_hooks()
        pipe = None
        prompt_embeds = None
        negative_prompt_embeds = None
        state["mps_post_release"] = release_pipeline_memory(torch)
        if sampler is not None:
            sampler.stop_sampling()
            state["mps_peak_current_allocated_bytes"] = sampler.peak_current
            state["mps_peak_driver_allocated_bytes"] = sampler.peak_driver
        state["stage_elapsed_seconds"]["mps_release"] = round(time.perf_counter() - release_start, 3)
        state["phase"] = "EXPORTING_VIDEO"
        write_json(state_path, state)

        stage_start = time.perf_counter()
        output_path = evidence_dir / "output.mp4"
        export_to_video(frames, output_path, fps=provider["fps"])
        first_frame = np.asarray(frames[0])
        if np.issubdtype(first_frame.dtype, np.floating):
            first_frame = np.clip(first_frame * 255.0, 0, 255).round().astype(np.uint8)
        imageio.imwrite(evidence_dir / "thumbnail.png", first_frame)
        reader = imageio.get_reader(output_path)
        metadata = reader.get_meta_data()
        decoded_frames = reader.count_frames()
        reader.close()
        state["output_metadata"] = {
            "decoded_frame_count": decoded_frames,
            "fps": metadata.get("fps"),
            "size": list(metadata.get("size", ())),
            "duration_seconds": metadata.get("duration"),
        }
        state["output_export_completed"] = True
        state["stage_elapsed_seconds"]["video_export"] = round(time.perf_counter() - stage_start, 3)
        state["phase"] = "WORKER_COMPLETED"
        state["finished_at"] = utc_now()
        write_json(state_path, state)
        return 0
    except BaseException as exc:
        error_observation = (
            exc.observation if isinstance(exc, WorkerStageFailure) else sanitized_exception(exc)
        )
        exc.__traceback__ = None
        try:
            if pipe is not None and hasattr(pipe, "maybe_free_model_hooks"):
                pipe.maybe_free_model_hooks()
            pipe = None
            prompt_embeds = None
            negative_prompt_embeds = None
            state["mps_post_release"] = release_pipeline_memory(torch)
        except BaseException as release_exc:
            state["mps_release_error"] = sanitized_exception(release_exc)
        if sampler is not None:
            sampler.stop_sampling()
            state["mps_peak_current_allocated_bytes"] = sampler.peak_current
            state["mps_peak_driver_allocated_bytes"] = sampler.peak_driver
        stop_request_path = evidence_dir / "stop_request.json"
        stop_request = None
        if stop_request_path.exists():
            try:
                stop_request = json.loads(stop_request_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                stop_request = {"reason": "PARENT_STOP_REQUEST_UNREADABLE"}
        state["phase"] = "WORKER_STOPPED_BY_PARENT" if stop_request else "WORKER_FAILED"
        state["stop_request"] = stop_request
        state["finished_at"] = utc_now()
        state["error_observation"] = error_observation
        write_json(state_path, state)
        print(json.dumps(state["error_observation"], ensure_ascii=False), file=sys.stderr, flush=True)
        return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=("wan", "cogvideox"), required=True)
    parser.add_argument("--execution-id", required=True)
    parser.add_argument("--evidence-root")
    parser.add_argument("--job-spec")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Z0-9][A-Z0-9._-]{2,127}", args.execution_id):
        parser.error("execution-id 只能包含大写字母、数字、点、下划线和连字符")
    return args


def main() -> int:
    args = parse_args()
    return run_worker(args) if args.worker else run_parent(args)


if __name__ == "__main__":
    raise SystemExit(main())
