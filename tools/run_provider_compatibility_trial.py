#!/usr/bin/env python3
"""运行一个有界的视频提供者兼容性试验并生成公开安全的证据包。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import queue
import re
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
                child.terminate()
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
                child.terminate()
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
        "mps_peak_current_allocated_bytes": worker_state.get("mps_peak_current_allocated_bytes"),
        "mps_peak_driver_allocated_bytes": worker_state.get("mps_peak_driver_allocated_bytes"),
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
        self.thread.start()
        return self

    def __exit__(self, *_: Any) -> None:
        self.stop_event.set()
        self.thread.join(timeout=5)


def run_worker(args: argparse.Namespace) -> int:
    import imageio.v2 as imageio
    import numpy as np
    import torch
    from diffusers import AutoencoderKLWan, CogVideoXPipeline, WanPipeline
    from diffusers.schedulers import UniPCMultistepScheduler
    from diffusers.utils import export_to_video
    from huggingface_hub import snapshot_download

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
    }
    write_json(state_path, state)
    sampler: MpsSampler | None = None
    try:
        if not torch.backends.mps.is_available():
            raise RuntimeError("PyTorch MPS backend is unavailable")

        stage_start = time.perf_counter()
        state["phase"] = "RESOLVING_MODEL_SNAPSHOT"
        write_json(state_path, state)
        snapshot_path = Path(snapshot_download(provider["model_id"]))
        state["model_snapshot_resolved"] = True
        state["model_snapshot_revision"] = snapshot_path.name
        state["stage_elapsed_seconds"]["snapshot_resolution"] = round(time.perf_counter() - stage_start, 3)
        state["phase"] = "LOADING_PIPELINE"
        write_json(state_path, state)

        stage_start = time.perf_counter()
        if args.provider == "wan":
            vae = AutoencoderKLWan.from_pretrained(
                snapshot_path,
                subfolder="vae",
                torch_dtype=torch.float32,
                local_files_only=True,
            )
            pipe = WanPipeline.from_pretrained(
                snapshot_path,
                vae=vae,
                torch_dtype=torch.bfloat16,
                local_files_only=True,
            )
            pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config, flow_shift=3.0)
        else:
            pipe = CogVideoXPipeline.from_pretrained(
                snapshot_path,
                torch_dtype=torch.float16,
                local_files_only=True,
            )
            pipe.vae.enable_slicing()
            pipe.vae.enable_tiling()
        pipe.enable_attention_slicing()
        state["pipeline_loaded"] = True
        state["stage_elapsed_seconds"]["pipeline_load"] = round(time.perf_counter() - stage_start, 3)
        state["phase"] = "TRANSFERRING_TO_MPS"
        write_json(state_path, state)

        stage_start = time.perf_counter()
        pipe.to("mps")
        torch.mps.synchronize()
        state["mps_transfer_completed"] = True
        state["stage_elapsed_seconds"]["mps_transfer"] = round(time.perf_counter() - stage_start, 3)
        state["phase"] = "RUNNING_INFERENCE"
        write_json(state_path, state)

        generator = torch.Generator(device="cpu").manual_seed(contract["shared_seed"])
        stage_start = time.perf_counter()
        sampler = MpsSampler(evidence_dir / "mps_metrics.jsonl")
        with sampler:
            output = pipe(
                prompt=contract["shared_prompt"],
                height=provider["height"],
                width=provider["width"],
                num_frames=provider["num_frames"],
                num_inference_steps=provider["num_inference_steps"],
                guidance_scale=provider["guidance_scale"],
                generator=generator,
                output_type="np",
            )
            torch.mps.synchronize()
        frames = output.frames[0]
        state["inference_completed"] = True
        state["mps_peak_current_allocated_bytes"] = sampler.peak_current
        state["mps_peak_driver_allocated_bytes"] = sampler.peak_driver
        state["stage_elapsed_seconds"]["inference"] = round(time.perf_counter() - stage_start, 3)
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
        if sampler is not None:
            state["mps_peak_current_allocated_bytes"] = sampler.peak_current
            state["mps_peak_driver_allocated_bytes"] = sampler.peak_driver
        state["phase"] = "WORKER_FAILED"
        state["finished_at"] = utc_now()
        state["error_observation"] = sanitized_exception(exc)
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
