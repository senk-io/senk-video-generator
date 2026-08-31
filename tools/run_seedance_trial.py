#!/usr/bin/env python3
"""预检或执行一次显式计费的 Seedance / BytePlus ModelArk 远端试验。"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_ROOT = REPO_ROOT / "experiments" / "provider_compatibility"
DEFAULT_CONTRACT = CONTRACT_ROOT / "seedance_fictional_child_crying_closeup_v1.json"
DEFAULT_EVIDENCE_ROOT = REPO_ROOT / "evidence" / "runtime"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from provider_adapters.seedance import (
    SEEDANCE_API_BASE,
    SEEDANCE_API_KEY_ENV,
    AdapterError,
    UrllibSeedanceTransport,
    run_trial,
    sha256_file,
    validate_trial_contract,
    write_json,
    write_manifest,
    utc_now,
)


def load_contract(path: Path) -> dict[str, Any]:
    resolved = path.resolve()
    if not resolved.is_relative_to(CONTRACT_ROOT) or resolved.suffix != ".json":
        raise ValueError("Seedance 试验合同必须位于受控试验目录")
    try:
        value = json.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("无法读取 Seedance 试验合同") from exc
    return validate_trial_contract(value)


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


def probe_media(path: Path) -> dict[str, Any]:
    import imageio.v2 as imageio
    import imageio_ffmpeg

    reader = imageio.get_reader(path)
    try:
        metadata = reader.get_meta_data()
        decoded_frame_count = reader.count_frames()
    finally:
        reader.close()
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    inspected = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", str(path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    ).stderr
    audio_line = next((line for line in inspected.splitlines() if " Audio:" in line), "")
    sample_rate = re.search(r"(\d+) Hz", audio_line)
    channels = "stereo" if "stereo" in audio_line.lower() else "mono" if "mono" in audio_line.lower() else None
    return {
        "decoded_frame_count": decoded_frame_count,
        "fps": float(metadata.get("fps") or 0.0),
        "duration_seconds": float(metadata.get("duration") or 0.0),
        "size": list(metadata.get("size", ())),
        "audio_stream_present": bool(audio_line),
        "audio_sample_rate_hz": int(sample_rate.group(1)) if sample_rate else None,
        "audio_channels": channels,
    }


def validate_media_contract(metadata: dict[str, Any], contract: dict[str, Any]) -> None:
    generation = contract["generation"]
    size = metadata.get("size") or []
    expected_short_edge = {"480p": 480, "720p": 720, "1080p": 1080}[generation["resolution"]]
    if len(size) != 2 or min(size) != expected_short_edge:
        raise AdapterError("OUTPUT_RESOLUTION_MISMATCH", "输出短边不是合同要求的分辨率")
    if abs(float(metadata.get("fps") or 0.0) - 24.0) > 0.1:
        raise AdapterError("OUTPUT_FPS_MISMATCH", "输出帧率不是合同要求的 24 fps")
    if abs(float(metadata.get("duration_seconds") or 0.0) - generation["duration"]) > 0.25:
        raise AdapterError("OUTPUT_DURATION_MISMATCH", "输出时长与合同不一致")
    if generation["generate_audio"] and not metadata.get("audio_stream_present"):
        raise AdapterError("OUTPUT_AUDIO_MISSING", "Seedance 输出缺少原生音频流")


def environment_record(execution_id: str, contract_path: Path) -> dict[str, Any]:
    return {
        "execution_id": execution_id,
        "recorded_at": utc_now(),
        "operating_system": platform.system(),
        "operating_system_version": platform.mac_ver()[0],
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "git_head": git_value("rev-parse", "HEAD"),
        "git_status_porcelain": git_value("status", "--porcelain") or "",
        "adapter_sha256": sha256_file(REPO_ROOT / "provider_adapters" / "seedance.py"),
        "runner_sha256": sha256_file(Path(__file__)),
        "contract_sha256": sha256_file(contract_path),
        "api_origin": SEEDANCE_API_BASE,
        "credential_env": SEEDANCE_API_KEY_ENV,
        "credential_present": True,
        "credential_recorded": False,
        "sensitive_machine_identifiers_recorded": False,
    }


def observe_preflight(contract: dict[str, Any], *, execute: bool) -> dict[str, Any]:
    key_present = bool(os.environ.get(SEEDANCE_API_KEY_ENV, "").strip())
    return {
        "preflight": "ready" if key_present else "blocked",
        "provider_key": "seedance",
        "model_id": "dreamina-seedance-2-0-260128",
        "api_version": "v3",
        "api_origin": SEEDANCE_API_BASE,
        "credential_env": SEEDANCE_API_KEY_ENV,
        "credential_present": key_present,
        "credential_recorded": False,
        "paid_remote_request": True,
        "execute_flag_present": execute,
        "generation": contract["generation"],
        "creates_formal_fact": False,
        "visual_quality_acceptance": "REQUIRES_REVIEW",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", default=str(DEFAULT_CONTRACT))
    parser.add_argument("--execution-id")
    parser.add_argument("--evidence-root", default=str(DEFAULT_EVIDENCE_ROOT))
    parser.add_argument(
        "--execute",
        action="store_true",
        help="显式提交计费远端任务；省略时只执行无费用预检",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    contract_path = Path(args.contract).resolve()
    try:
        contract = load_contract(contract_path)
    except ValueError as exc:
        print(json.dumps({"preflight": "blocked", "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    preflight = observe_preflight(contract, execute=args.execute)
    key_present = bool(preflight["credential_present"])
    if not args.execute:
        print(json.dumps(preflight, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if key_present else 2
    if not key_present:
        print(json.dumps(preflight, ensure_ascii=False, indent=2, sort_keys=True))
        return 2
    if not args.execution_id:
        print("执行计费任务时必须提供 --execution-id", file=sys.stderr)
        return 2

    evidence_dir = Path(args.evidence_root).resolve() / args.execution_id
    transport = UrllibSeedanceTransport(os.environ[SEEDANCE_API_KEY_ENV])

    def checked_probe(path: Path) -> dict[str, Any]:
        metadata = probe_media(path)
        validate_media_contract(metadata, contract)
        return metadata

    exit_code = 0
    try:
        summary = run_trial(
            contract,
            args.execution_id,
            evidence_dir,
            transport,
            media_probe=checked_probe,
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    except (AdapterError, ValueError, OSError) as exc:
        print(f"Seedance 试验失败：{exc}", file=sys.stderr)
        exit_code = 1
    finally:
        if evidence_dir.is_dir():
            write_json(evidence_dir / "environment.json", environment_record(args.execution_id, contract_path))
            write_manifest(evidence_dir)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
