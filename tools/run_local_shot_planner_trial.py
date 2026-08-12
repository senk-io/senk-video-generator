#!/usr/bin/env python3
"""预检或执行固定三次的 Qwen3 本地镜头规划试验。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = (
    REPO_ROOT
    / "experiments"
    / "shot_planning"
    / "qwen3_0_6b_tokenized_context_trial_v7.json"
)
DEFAULT_EVIDENCE_ROOT = REPO_ROOT / "evidence" / "runtime"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shot_planning.local_trial import (
    MODEL_ID,
    MODEL_REVISION,
    environment_record,
    run_trial,
    validate_request_binding,
    validate_trial_contract,
    write_json,
    write_manifest,
)
from shot_planning.contracts import validate_request


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def relative_repo_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError as exc:
        raise ValueError("试验文件必须位于仓库内。") from exc


def local_preflight(contract: dict[str, Any]) -> dict[str, Any]:
    import torch
    from huggingface_hub import model_info

    info = model_info(MODEL_ID, revision=MODEL_REVISION, files_metadata=True)
    weight = next(
        (item for item in info.siblings or [] if item.rfilename == "model.safetensors"),
        None,
    )
    observed_weight_bytes = getattr(weight, "size", None)
    return {
        "model_id": info.id,
        "requested_revision": MODEL_REVISION,
        "observed_revision": info.sha,
        "model_gated": info.gated,
        "model_private": info.private,
        "expected_weight_bytes": contract["model"]["expected_weight_bytes"],
        "observed_weight_bytes": observed_weight_bytes,
        "weight_within_budget": (
            isinstance(observed_weight_bytes, int)
            and observed_weight_bytes
            <= contract["resource_budget"]["maximum_model_weight_bytes"]
        ),
        "mps_available": bool(torch.backends.mps.is_available()),
        "run_count": contract["execution"]["run_count"],
        "retry_count": contract["resource_budget"]["retry_count"],
        "paid_request": False,
        "formal_fact_creation": False,
    }


def build_generator(contract: dict[str, Any]):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        revision=MODEL_REVISION,
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=MODEL_REVISION,
        dtype=torch.float16,
        low_cpu_mem_usage=True,
    ).to("mps")
    model.eval()

    def generate(prompt: dict[str, Any], _run_index: int) -> str:
        torch.manual_seed(contract["execution"]["seed"])
        messages = [
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]},
        ]
        assistant_prefill = prompt.get("assistant_prefill")
        if assistant_prefill:
            messages.append({"role": "assistant", "content": assistant_prefill})
            rendered = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                continue_final_message=True,
                enable_thinking=contract["execution"]["enable_thinking"],
            )
        else:
            rendered = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=contract["execution"]["enable_thinking"],
            )
        inputs = tokenizer([rendered], return_tensors="pt").to("mps")
        with torch.inference_mode():
            generated = model.generate(
                **inputs,
                max_new_tokens=contract["execution"]["max_new_tokens"],
                do_sample=contract["execution"]["do_sample"],
                pad_token_id=tokenizer.eos_token_id,
            )
        output_ids = generated[0][inputs.input_ids.shape[1] :].to("cpu")
        return (assistant_prefill or "") + tokenizer.decode(output_ids, skip_special_tokens=True)

    return generate


def build_lazy_generator(contract: dict[str, Any]):
    generator_holder: dict[str, Any] = {}

    def generate(prompt: dict[str, Any], run_index: int) -> str:
        if "load_error" in generator_holder:
            raise RuntimeError("模型加载已经失败；固定后续运行不再次尝试加载。")
        if "generator" not in generator_holder:
            try:
                generator_holder["generator"] = build_generator(contract)
            except Exception as exc:
                generator_holder["load_error"] = exc
                raise
        return generator_holder["generator"](prompt, run_index)

    return generate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--execution-id")
    parser.add_argument("--evidence-root", type=Path, default=DEFAULT_EVIDENCE_ROOT)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="下载缺失权重并在 MPS 上执行固定三次；省略时只预检",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    contract_path = args.contract.resolve()
    contract = validate_trial_contract(load_json(contract_path))
    request_path = REPO_ROOT / contract["request_binding"]["request_file"]
    request = validate_request(load_json(request_path))
    validate_request_binding(contract, request, relative_repo_path(request_path))
    preflight = local_preflight(contract)
    ready = (
        preflight["observed_revision"] == MODEL_REVISION
        and preflight["observed_weight_bytes"] == contract["model"]["expected_weight_bytes"]
        and preflight["weight_within_budget"]
        and preflight["mps_available"]
    )
    preflight["preflight"] = "ready" if ready else "blocked"
    preflight["execute_flag_present"] = args.execute
    if not args.execute or not ready:
        print(json.dumps(preflight, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if ready else 2
    if not args.execution_id:
        print("执行本地模型时必须提供 --execution-id", file=sys.stderr)
        return 2

    evidence_dir = args.evidence_root.resolve() / args.execution_id
    generator = build_lazy_generator(contract)
    summary = run_trial(contract, request, args.execution_id, evidence_dir, generator)
    write_json(
        evidence_dir / "environment.json",
        environment_record(
            execution_id=args.execution_id,
            repo_root=REPO_ROOT,
            contract_path=contract_path,
            request_path=request_path,
            runner_path=Path(__file__),
        ),
    )
    write_manifest(evidence_dir)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
