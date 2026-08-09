#!/usr/bin/env python3
"""从已保存的 CogVideoX 潜变量进行低内存中央处理器解码。"""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import threading
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import psutil

try:
    from tools.run_provider_compatibility_trial import sha256_file, write_json, write_manifest
except ModuleNotFoundError:
    from run_provider_compatibility_trial import sha256_file, write_json, write_manifest


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE_ROOT = REPO_ROOT / "evidence" / "runtime"
EXECUTION_ID_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9._-]{2,127}")
GIB = 1024**3
PREFLIGHT_MIN_AVAILABLE = 16 * GIB
PREFLIGHT_MAX_SWAP = 4 * GIB
ABORT_MIN_AVAILABLE = 5 * GIB
MAX_SWAP_GROWTH = 4 * GIB
NORMAL_MEMORY_PRESSURE_LEVEL = 1


class DecodeAbort(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def read_json(file_path: Path) -> dict[str, Any]:
    value = json.loads(file_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("JSON 根值不是对象")
    return value


def read_macos_memory_pressure_level() -> int | None:
    """读取 macOS 的权威内存压力级别；无法读取时返回空值。"""
    try:
        result = subprocess.run(
            ["sysctl", "-n", "kern.memorystatus_vm_pressure_level"],
            check=True,
            capture_output=True,
            text=True,
            timeout=2,
        )
        return int(result.stdout.strip())
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def preflight_block_reason(available_bytes: int, swap_used_bytes: int, pressure_level: int | None) -> str | None:
    if available_bytes < PREFLIGHT_MIN_AVAILABLE:
        return "启动前可用内存不足 16 GiB"
    if swap_used_bytes > PREFLIGHT_MAX_SWAP and pressure_level != NORMAL_MEMORY_PRESSURE_LEVEL:
        return "启动前换页高于 4 GiB，且系统内存压力并非正常级"
    return None


def validate_decode_source(evidence_root: Path, source_execution_id: str) -> dict[str, Any]:
    if not EXECUTION_ID_PATTERN.fullmatch(source_execution_id):
        raise ValueError("来源执行标识无效")
    evidence_root = evidence_root.resolve()
    source_root = (evidence_root / source_execution_id).resolve()
    if not source_root.is_relative_to(evidence_root):
        raise ValueError("来源目录越界")
    summary = read_json(source_root / "summary.json")
    checkpoint = summary.get("latent_checkpoint")
    if not isinstance(checkpoint, dict) or checkpoint.get("path") != "denoised_latents.safetensors":
        raise ValueError("来源没有可解码潜变量检查点")
    latent_path = source_root / checkpoint["path"]
    if not latent_path.is_file() or sha256_file(latent_path) != checkpoint.get("sha256"):
        raise ValueError("潜变量检查点摘要不匹配")
    return {
        "source_root": source_root,
        "source_summary": summary,
        "latent_path": latent_path,
        "latent_sha256": checkpoint["sha256"],
    }


class ResourceMonitor:
    def __init__(self, metrics_path: Path, swap_start: int) -> None:
        self.metrics_path = metrics_path
        self.swap_start = swap_start
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.abort_reason: str | None = None
        self.peak_rss = 0
        self.peak_swap = swap_start
        self.low_available_samples = 0
        self.started = time.perf_counter()

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self.stop_event.set()
        self.thread.join(timeout=5)

    def _run(self) -> None:
        process = psutil.Process()
        with self.metrics_path.open("w", encoding="utf-8") as handle:
            while not self.stop_event.wait(0.5):
                memory = psutil.virtual_memory()
                swap = psutil.swap_memory()
                rss = process.memory_info().rss
                self.peak_rss = max(self.peak_rss, rss)
                self.peak_swap = max(self.peak_swap, swap.used)
                self.low_available_samples = self.low_available_samples + 1 if memory.available < ABORT_MIN_AVAILABLE else 0
                if self.low_available_samples >= 6:
                    self.abort_reason = "SYSTEM_AVAILABLE_MEMORY_BELOW_BUDGET"
                elif swap.used - self.swap_start > MAX_SWAP_GROWTH:
                    self.abort_reason = "SYSTEM_SWAP_GROWTH_EXCEEDED_BUDGET"
                handle.write(
                    json.dumps(
                        {
                            "elapsed_seconds": round(time.perf_counter() - self.started, 3),
                            "process_rss_bytes": rss,
                            "system_available_bytes": memory.available,
                            "swap_used_bytes": swap.used,
                        },
                        sort_keys=True,
                    )
                    + "\n"
                )
                handle.flush()
                if self.abort_reason:
                    os.kill(os.getpid(), signal.SIGTERM)
                    return


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-execution-id", required=True)
    parser.add_argument("--execution-id", required=True)
    parser.add_argument("--evidence-root", default=str(DEFAULT_EVIDENCE_ROOT))
    args = parser.parse_args()
    for field in ("source_execution_id", "execution_id"):
        if not EXECUTION_ID_PATTERN.fullmatch(getattr(args, field)):
            parser.error(f"{field} 无效")
    return args


def main() -> int:
    args = parse_args()
    evidence_root = Path(args.evidence_root).resolve()
    source = validate_decode_source(evidence_root, args.source_execution_id)
    output_root = (evidence_root / args.execution_id).resolve()
    if not output_root.is_relative_to(evidence_root) or output_root.exists():
        raise SystemExit("输出证据目录无效或已经存在")
    memory_start = psutil.virtual_memory()
    swap_start = psutil.swap_memory()
    memory_pressure_level = read_macos_memory_pressure_level()
    block_reason = preflight_block_reason(memory_start.available, swap_start.used, memory_pressure_level)
    if block_reason:
        raise SystemExit(block_reason)

    output_root.mkdir(parents=True)
    request = {
        "schema_version": "cogvideox-latent-decode.v2",
        "execution_id": args.execution_id,
        "source_execution_id": args.source_execution_id,
        "source_latent_sha256": source["latent_sha256"],
        "device": "cpu",
        "dtype": "float32",
        "tile_sample_size": [180, 120],
        "resource_budget": {
            "preflight_min_available_memory_bytes": PREFLIGHT_MIN_AVAILABLE,
            "preflight_max_swap_used_bytes": PREFLIGHT_MAX_SWAP,
            "preflight_swap_residue_override_requires_memory_pressure_level": NORMAL_MEMORY_PRESSURE_LEVEL,
            "observed_memory_pressure_level": memory_pressure_level,
            "historical_swap_residue_override_applied": swap_start.used > PREFLIGHT_MAX_SWAP,
            "abort_min_available_memory_bytes": ABORT_MIN_AVAILABLE,
            "max_swap_growth_bytes": MAX_SWAP_GROWTH,
        },
        "created_at": utc_now(),
        "formal_fact_creation": "PROHIBITED",
    }
    write_json(output_root / "request.json", request)
    monitor = ResourceMonitor(output_root / "process_metrics.jsonl", swap_start.used)
    started = time.perf_counter()

    def handle_stop(_signum: int, _frame: Any) -> None:
        raise DecodeAbort(monitor.abort_reason or "DECODE_STOP_REQUESTED")

    signal.signal(signal.SIGTERM, handle_stop)
    monitor.start()
    output_path = output_root / "output.mp4"
    observation = "OBSERVED_EXECUTION_WITHOUT_OUTPUT"
    error: dict[str, str] | None = None
    metadata: dict[str, Any] | None = None
    try:
        import imageio.v2 as imageio
        import numpy as np
        import torch
        from diffusers import AutoencoderKLCogVideoX, CogVideoXPipeline
        from diffusers.utils import export_to_video
        from huggingface_hub import snapshot_download
        from safetensors.torch import load_file as load_safetensors

        source_summary = source["source_summary"]
        snapshot_path = Path(snapshot_download(source_summary["model_id"], revision=source_summary["model_snapshot_revision"]))
        vae = AutoencoderKLCogVideoX.from_pretrained(
            snapshot_path,
            subfolder="vae",
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True,
            local_files_only=True,
        )
        vae.enable_slicing()
        vae.enable_tiling(tile_sample_min_height=120, tile_sample_min_width=180)
        pipe = CogVideoXPipeline(tokenizer=None, text_encoder=None, vae=vae, transformer=None, scheduler=None)
        latent_video = load_safetensors(source["latent_path"])["latents"].to(dtype=torch.float32)
        with torch.inference_mode():
            decoded = pipe.decode_latents(latent_video)
            frames = pipe.video_processor.postprocess_video(video=decoded, output_type="np")[0]
        export_to_video(frames, output_path, fps=8)
        first_frame = np.asarray(frames[0])
        if np.issubdtype(first_frame.dtype, np.floating):
            first_frame = np.clip(first_frame * 255.0, 0, 255).round().astype(np.uint8)
        imageio.imwrite(output_root / "thumbnail.png", first_frame)
        reader = imageio.get_reader(output_path)
        metadata = {
            "decoded_frame_count": reader.count_frames(),
            "fps": reader.get_meta_data().get("fps"),
            "size": list(reader.get_meta_data().get("size", ())),
            "duration_seconds": reader.get_meta_data().get("duration"),
        }
        reader.close()
        observation = "OBSERVED_OUTPUT_AVAILABLE"
    except BaseException as exc:
        error = {"type": type(exc).__name__, "message": str(exc)}
    finally:
        monitor.stop()

    summary = {
        "execution_id": args.execution_id,
        "source_execution_id": args.source_execution_id,
        "observation": observation,
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "safety_abort_reason": monitor.abort_reason,
        "process_peak_rss_bytes": monitor.peak_rss,
        "system_start_swap_used_bytes": swap_start.used,
        "system_peak_swap_used_bytes": monitor.peak_swap,
        "output_metadata": metadata,
        "output_sha256": sha256_file(output_path) if output_path.is_file() else None,
        "error_observation": error,
        "formal_fact_created": False,
        "quality_acceptance_created": False,
        "institution_freeze_created": False,
        "finished_at": utc_now(),
    }
    write_json(output_root / "summary.json", summary)
    write_manifest(output_root)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if observation == "OBSERVED_OUTPUT_AVAILABLE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
