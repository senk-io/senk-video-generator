"""本地非权威视频作业请求的固定字段、范围和执行合同编译。"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any


EXECUTION_ID_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9._-]{2,127}")
JOB_SCHEMA_VERSION = "operator-job.v4"
LEGACY_JOB_SCHEMA_VERSIONS = frozenset({"operator-job.v2", "operator-job.v3"})
GIB = 1024**3
JOB_ID_PATTERN = re.compile(r"JOB-[0-9]{8}T[0-9]{6}Z-[A-F0-9]{8}")
PROJECT_ID_PATTERN = re.compile(r"PILOT-[A-Z0-9][A-Z0-9-]{2,95}")
SHOT_ID_PATTERN = re.compile(r"SHOT-[0-9]{3}")
SHA256_PATTERN = re.compile(r"[a-f0-9]{64}")

SECRET_REQUEST_FIELDS = frozenset(
    {
        "access_token",
        "api_key",
        "ark_api_key",
        "authorization",
        "bearer",
        "credential",
        "minimax_api_key",
        "password",
        "secret",
        "token",
    }
)

PROVIDER_PROFILES: dict[str, dict[str, Any]] = {
    "wan": {
        "key": "wan",
        "name": "Wan2.1-T2V-1.3B",
        "provider_identity": "Wan-AI",
        "model_id": "Wan-AI/Wan2.1-T2V-1.3B-Diffusers",
        "execution_backend": "local_diffusers",
        "observed_revision": "0fad780a534b6463e45facd96134c9f345acfa5b",
        "runtime_observation": "OBSERVED_OUTPUT_AVAILABLE",
        "startable": True,
        "risk": "HIGH_MEMORY",
        "risk_message": "当前 36GB 统一内存 Mac 已完成低内存探针，但更高分辨率、帧数和步数仍可能显著增加换页。",
        "dtype": "bfloat16",
        "vae_dtype": "float32",
        "defaults": {
            "width": 416,
            "height": 240,
            "num_frames": 17,
            "num_inference_steps": 4,
            "guidance_scale": 5.0,
            "fps": 8,
        },
        "limits": {
            "width": [256, 416],
            "height": [144, 240],
            "num_frames": [9, 17],
            "num_inference_steps": [1, 16],
            "guidance_scale": [1.0, 8.0],
            "fps": [1, 12],
        },
    },
    "cogvideox": {
        "key": "cogvideox",
        "name": "CogVideoX-2B",
        "provider_identity": "zai-org",
        "model_id": "zai-org/CogVideoX-2b",
        "execution_backend": "local_diffusers",
        "observed_revision": "1137dacfc2c9c012bed6a0793f4ecf2ca8e7ba01",
        "runtime_observation": "DOWNLOAD_ONLY_RUNTIME_UNKNOWN",
        "startable": False,
        "risk": "UNVALIDATED_RUNTIME",
        "risk_message": "模型缓存完整，但尚未建立当前 Mac 上的装载、MPS 转移或推理观察。",
        "dtype": "float16",
        "defaults": {
            "width": 720,
            "height": 480,
            "num_frames": 9,
            "num_inference_steps": 4,
            "guidance_scale": 6.0,
            "fps": 8,
        },
        "limits": {
            "width": [720, 720],
            "height": [480, 480],
            "num_frames": [9, 9],
            "num_inference_steps": [1, 4],
            "guidance_scale": [1.0, 8.0],
            "fps": [1, 12],
        },
    },
    "seedance": {
        "key": "seedance",
        "name": "Seedance 2.0 / BytePlus ModelArk",
        "provider_identity": "BytePlus",
        "model_id": "dreamina-seedance-2-0-260128",
        "execution_backend": "remote_api",
        "api_version": "v3",
        "api_origin": "https://ark.ap-southeast.bytepluses.com/api/v3",
        "credential_env": "ARK_API_KEY",
        "observed_revision": None,
        "runtime_observation": "REMOTE_PRECHECK_ONLY",
        "startable": False,
        "paid_execute_via_console": False,
        "risk": "PAID_REMOTE_REQUEST",
        "risk_message": "默认只做无费用预检；控制台不会提交计费任务，也不会把密钥写入作业或前端状态。显式计费仍须使用 CLI --execute。",
        "trial_contract": "experiments/provider_compatibility/seedance_fictional_child_crying_closeup_v1.json",
        "trial_runner": "tools.run_seedance_trial",
        "default_generation_profile_key": "seedance_remote_trial",
        "default_execution_strategy": "remote_precheck_only",
    },
    "minimax_h3": {
        "key": "minimax_h3",
        "name": "MiniMax H3 / 开放平台 V2",
        "provider_identity": "MiniMax",
        "model_id": "MiniMax-H3",
        "execution_backend": "remote_api",
        "api_version": "v2",
        "api_origin": "https://api.minimax.io",
        "credential_env": "MINIMAX_API_KEY",
        "observed_revision": None,
        "runtime_observation": "REMOTE_PRECHECK_ONLY",
        "startable": False,
        "paid_execute_via_console": False,
        "risk": "PAID_REMOTE_REQUEST",
        "risk_message": "默认只做无费用预检；控制台不会提交计费任务，也不会把密钥写入作业或前端状态。显式计费仍须使用 CLI --execute。",
        "trial_contract": "experiments/provider_compatibility/minimax_h3_fictional_child_crying_closeup_v1.json",
        "trial_runner": "tools.run_minimax_h3_trial",
        "default_generation_profile_key": "minimax_h3_remote_trial",
        "default_execution_strategy": "remote_precheck_only",
    },
}

TASK_TYPES = {
    "text_to_video": {
        "label": "文生视频",
        "available": True,
        "requires_material": False,
        "description": "使用文本提示词直接生成候选视频。",
    },
    "image_to_video": {
        "label": "图生视频",
        "available": False,
        "requires_material": True,
        "description": "需要参考图片；当前执行器尚未接入。",
    },
    "video_to_video": {
        "label": "视频转换",
        "available": False,
        "requires_material": True,
        "description": "需要参考视频；当前执行器尚未接入。",
    },
}

GENERATION_PROFILES: dict[str, dict[str, Any]] = {
    "wan_probe": {
        "key": "wan_probe",
        "provider_key": "wan",
        "name": "内存探针",
        "description": "最小画幅、帧数和步数，用于先验证内存边界。",
        "parameters": {
            "width": 256,
            "height": 144,
            "num_frames": 9,
            "num_inference_steps": 1,
            "guidance_scale": 5.0,
            "fps": 8,
        },
    },
    "wan_quality_probe": {
        "key": "wan_quality_probe",
        "provider_key": "wan",
        "name": "质量探针",
        "description": "保持最低画幅与帧数，仅把推理提高到 4 步以观察可辨识度。",
        "parameters": {
            "width": 256,
            "height": 144,
            "num_frames": 9,
            "num_inference_steps": 4,
            "guidance_scale": 5.0,
            "fps": 8,
        },
    },
    "wan_balance_probe": {
        "key": "wan_balance_probe",
        "provider_key": "wan",
        "name": "平衡探针",
        "description": "保持最低画幅与帧数，把推理提高到 16 步以寻找最低可辨识档位。",
        "parameters": {
            "width": 256,
            "height": 144,
            "num_frames": 9,
            "num_inference_steps": 16,
            "guidance_scale": 5.0,
            "fps": 8,
        },
    },
    "wan_balance_backtest": {
        "key": "wan_balance_backtest",
        "provider_key": "wan",
        "name": "推荐平衡",
        "description": "当前 Mac 已验证的最低可辨识档位：8 步、最低画幅与 9 帧。",
        "parameters": {
            "width": 256,
            "height": 144,
            "num_frames": 9,
            "num_inference_steps": 8,
            "guidance_scale": 5.0,
            "fps": 8,
        },
    },
    "wan_low_memory": {
        "key": "wan_low_memory",
        "provider_key": "wan",
        "name": "低内存生成",
        "description": "保持已观察画幅，将时长缩短到 9 帧。",
        "parameters": {
            "width": 416,
            "height": 240,
            "num_frames": 9,
            "num_inference_steps": 4,
            "guidance_scale": 5.0,
            "fps": 8,
        },
    },
    "wan_observed_compatibility": {
        "key": "wan_observed_compatibility",
        "provider_key": "wan",
        "name": "既有兼容基线",
        "description": "复现已成功的 416×240、17 帧兼容性参数。",
        "parameters": {
            "width": 416,
            "height": 240,
            "num_frames": 17,
            "num_inference_steps": 4,
            "guidance_scale": 5.0,
            "fps": 8,
        },
    },
    "cogvideox_probe": {
        "key": "cogvideox_probe",
        "provider_key": "cogvideox",
        "name": "CogVideoX 探针",
        "description": "保留为未来独立运行验证；当前仍禁止启动。",
        "parameters": {
            "width": 720,
            "height": 480,
            "num_frames": 9,
            "num_inference_steps": 1,
            "guidance_scale": 6.0,
            "fps": 8,
        },
    },
    "seedance_remote_trial": {
        "key": "seedance_remote_trial",
        "provider_key": "seedance",
        "name": "远端试验预检",
        "description": "固定 720p、5 秒、16:9 试验合同；只预检，不提交计费任务。",
        "parameters": {
            "resolution": "720p",
            "duration": 5,
            "ratio": "16:9",
            "generate_audio": True,
            "watermark": False,
        },
    },
    "minimax_h3_remote_trial": {
        "key": "minimax_h3_remote_trial",
        "provider_key": "minimax_h3",
        "name": "远端试验预检",
        "description": "固定 768P、5 秒、16:9 试验合同；只预检，不提交计费任务。",
        "parameters": {
            "resolution": "768P",
            "duration": 5,
            "ratio": "16:9",
        },
    },
}

EXECUTION_STRATEGIES: dict[str, dict[str, Any]] = {
    "mps_model_offload_bounded": {
        "key": "mps_model_offload_bounded",
        "name": "分阶段驻留",
        "recommended": True,
        "execution_backend": "local_diffusers",
        "description": "文本编码器以无梯度叶级顺序进入 MPS；形成嵌入并释放后再装载 Transformer 与 VAE。",
    },
    "mps_full_bounded": {
        "key": "mps_full_bounded",
        "name": "全量驻留基线",
        "recommended": False,
        "execution_backend": "local_diffusers",
        "description": "整条管线进入 MPS；仅用于与既有证据比较，内存风险更高。",
    },
    "remote_precheck_only": {
        "key": "remote_precheck_only",
        "name": "远端预检",
        "recommended": True,
        "execution_backend": "remote_api",
        "description": "只校验固定试验合同与凭据观察，不提交计费任务，不加载本地模型。",
    },
}


def provider_backend(profile: dict[str, Any] | None) -> str:
    if not profile:
        return "unknown"
    return str(profile.get("execution_backend") or "local_diffusers")


def is_remote_api_provider(profile: dict[str, Any] | None) -> bool:
    return provider_backend(profile) == "remote_api"


def secret_request_fields(value: dict[str, Any]) -> list[str]:
    return [str(key) for key in value if str(key).lower() in SECRET_REQUEST_FIELDS]


def public_catalog() -> dict[str, Any]:
    return {
        "providers": [deepcopy(profile) for profile in PROVIDER_PROFILES.values()],
        "task_types": [
            {"key": key, **deepcopy(value)} for key, value in TASK_TYPES.items()
        ],
        "generation_profiles": [deepcopy(value) for value in GENERATION_PROFILES.values()],
        "execution_strategies": [deepcopy(value) for value in EXECUTION_STRATEGIES.values()],
        "defaults": {
            "provider_key": "wan",
            "task_type": "text_to_video",
            "generation_profile_key": "wan_balance_backtest",
            "execution_strategy": "mps_model_offload_bounded",
            "seed": 42,
            "timeout_seconds": 3600,
            "preflight_min_available_memory_bytes": 16 * GIB,
            "preflight_max_swap_used_bytes": 4 * GIB,
            "abort_min_available_memory_bytes": 3 * GIB,
            "max_swap_growth_bytes": 8 * GIB,
            "mps_memory_fraction": 0.75,
        },
    }


def validate_job_request(value: Any) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    errors: list[dict[str, str]] = []
    if not isinstance(value, dict):
        return None, [{"field": "$", "code": "INVALID_BODY", "message": "作业请求必须是对象。"}]

    provider_key = str(value.get("provider_key", ""))
    profile = PROVIDER_PROFILES.get(provider_key)
    if not profile:
        errors.append({"field": "provider_key", "code": "UNKNOWN_PROVIDER", "message": "提供者不受支持。"})
    elif is_remote_api_provider(profile):
        errors.append(
            {
                "field": "provider_key",
                "code": "REMOTE_PROVIDER_NOT_STARTABLE",
                "message": "远端提供者不能登记为本地作业；控制台只提供无费用预检。",
            }
        )

    task_type = str(value.get("task_type", ""))
    task = TASK_TYPES.get(task_type)
    if not task:
        errors.append({"field": "task_type", "code": "UNKNOWN_TASK_TYPE", "message": "作业类型不受支持。"})
    elif not task["available"]:
        errors.append({"field": "task_type", "code": "TASK_TYPE_UNAVAILABLE", "message": task["description"]})

    execution_id = str(value.get("execution_id", "")).strip().upper()
    if not EXECUTION_ID_PATTERN.fullmatch(execution_id):
        errors.append(
            {
                "field": "execution_id",
                "code": "INVALID_EXECUTION_ID",
                "message": "执行标识只能包含大写字母、数字、点、下划线和连字符，长度为 3 至 128。",
            }
        )

    prompt = str(value.get("prompt", "")).strip()
    if not prompt:
        errors.append({"field": "prompt", "code": "PROMPT_REQUIRED", "message": "文生视频必须输入提示词。"})
    elif len(prompt) > 2000:
        errors.append({"field": "prompt", "code": "PROMPT_TOO_LONG", "message": "提示词不能超过 2000 个字符。"})

    project_binding = validate_project_binding(value.get("project_binding"), errors)

    seed = integer_field(value, "seed", 0, 2**32 - 1, errors)
    timeout_seconds = integer_field(value, "timeout_seconds", 300, 7200, errors)
    preflight_memory = integer_field(
        value,
        "preflight_min_available_memory_bytes",
        4 * GIB,
        24 * GIB,
        errors,
    )
    preflight_max_swap = integer_field(
        value,
        "preflight_max_swap_used_bytes",
        0,
        16 * GIB,
        errors,
    )
    abort_memory = integer_field(
        value,
        "abort_min_available_memory_bytes",
        2 * GIB,
        8 * GIB,
        errors,
    )
    max_swap_growth = integer_field(
        value,
        "max_swap_growth_bytes",
        2 * GIB,
        24 * GIB,
        errors,
    )
    mps_memory_fraction = float_field(value, "mps_memory_fraction", 0.5, 0.9, errors)
    if (
        preflight_memory is not None
        and abort_memory is not None
        and abort_memory >= preflight_memory
    ):
        errors.append(
            {
                "field": "abort_min_available_memory_bytes",
                "code": "INVALID_MEMORY_BUDGET_ORDER",
                "message": "运行中停止阈值必须低于启动前可用内存阈值。",
            }
        )

    generation_profile_key = str(value.get("generation_profile_key", ""))
    generation_profile = GENERATION_PROFILES.get(generation_profile_key)
    if not generation_profile:
        errors.append(
            {
                "field": "generation_profile_key",
                "code": "UNKNOWN_GENERATION_PROFILE",
                "message": "生成档位不受支持。",
            }
        )
    elif generation_profile["provider_key"] != provider_key:
        errors.append(
            {
                "field": "generation_profile_key",
                "code": "PROFILE_PROVIDER_MISMATCH",
                "message": "生成档位不适用于当前提供者。",
            }
        )

    execution_strategy = str(value.get("execution_strategy", ""))
    strategy = EXECUTION_STRATEGIES.get(execution_strategy)
    if not strategy:
        errors.append(
            {
                "field": "execution_strategy",
                "code": "UNKNOWN_EXECUTION_STRATEGY",
                "message": "执行策略不受支持。",
            }
        )
    elif profile and strategy.get("execution_backend", "local_diffusers") != provider_backend(profile):
        errors.append(
            {
                "field": "execution_strategy",
                "code": "STRATEGY_BACKEND_MISMATCH",
                "message": "执行策略不适用于当前提供者后端。",
            }
        )

    parameters: dict[str, int | float] = {}
    raw_parameters = value.get("parameters")
    if is_remote_api_provider(profile):
        raw_parameters = None
    if not isinstance(raw_parameters, dict):
        if not is_remote_api_provider(profile):
            errors.append({"field": "parameters", "code": "PARAMETERS_REQUIRED", "message": "必须提供生成参数。"})
    elif profile:
        for field, bounds in profile["limits"].items():
            raw = raw_parameters.get(field)
            numeric_type = float if field == "guidance_scale" else int
            try:
                number = numeric_type(raw)
            except (TypeError, ValueError):
                errors.append({"field": f"parameters.{field}", "code": "INVALID_NUMBER", "message": f"{field} 必须是数字。"})
                continue
            if not bounds[0] <= number <= bounds[1]:
                errors.append(
                    {
                        "field": f"parameters.{field}",
                        "code": "OUT_OF_BOUNDS",
                        "message": f"{field} 必须位于 {bounds[0]} 至 {bounds[1]}。",
                    }
                )
            parameters[field] = number
        if "width" in parameters and int(parameters["width"]) % 16:
            errors.append({"field": "parameters.width", "code": "INVALID_MULTIPLE", "message": "宽度必须是 16 的倍数。"})
        if "height" in parameters and int(parameters["height"]) % 16:
            errors.append({"field": "parameters.height", "code": "INVALID_MULTIPLE", "message": "高度必须是 16 的倍数。"})
        if "num_frames" in parameters and (int(parameters["num_frames"]) - 1) % 4:
            errors.append({"field": "parameters.num_frames", "code": "INVALID_FRAME_COUNT", "message": "帧数必须满足 4n+1。"})
        if generation_profile and generation_profile["provider_key"] == provider_key:
            for field, expected in generation_profile["parameters"].items():
                if parameters.get(field) != expected:
                    errors.append(
                        {
                            "field": f"parameters.{field}",
                            "code": "PROFILE_PARAMETER_MISMATCH",
                            "message": f"{field} 必须与固定生成档位一致。",
                        }
                    )

    risk_acknowledged = value.get("risk_acknowledged") is True
    if profile and not is_remote_api_provider(profile) and profile["startable"] and not risk_acknowledged:
        errors.append(
            {
                "field": "risk_acknowledged",
                "code": "RISK_ACKNOWLEDGEMENT_REQUIRED",
                "message": "必须明确确认当前模型的高内存风险。",
            }
        )
    if profile and not is_remote_api_provider(profile) and not profile["startable"]:
        errors.append(
            {
                "field": "provider_key",
                "code": "PROVIDER_RUNTIME_BLOCKED",
                "message": profile["risk_message"],
            }
        )

    if errors:
        return None, errors

    assert profile is not None
    normalized = {
        "schema_version": JOB_SCHEMA_VERSION,
        "execution_id": execution_id,
        "provider_key": provider_key,
        "provider_identity": profile["provider_identity"],
        "model_id": profile["model_id"],
        "model_revision": profile["observed_revision"],
        "task_type": task_type,
        "generation_profile_key": generation_profile_key,
        "prompt": prompt,
        "seed": seed,
        "parameters": parameters,
        "execution_strategy": execution_strategy,
        "timeout_seconds": timeout_seconds,
        "resource_budget": {
            "preflight_min_available_memory_bytes": preflight_memory,
            "preflight_max_swap_used_bytes": preflight_max_swap,
            "abort_min_available_memory_bytes": abort_memory,
            "max_swap_growth_bytes": max_swap_growth,
            "mps_memory_fraction": mps_memory_fraction,
        },
        "risk_acknowledged": risk_acknowledged,
        "project_binding": project_binding,
        "formal_fact_creation": "PROHIBITED",
        "cross_provider_contract_creation": "PROHIBITED",
        "institution_freeze_creation": "PROHIBITED",
    }
    return normalized, []


def validate_remote_precheck_request(value: Any) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    errors: list[dict[str, str]] = []
    if not isinstance(value, dict):
        return None, [{"field": "$", "code": "INVALID_BODY", "message": "预检请求必须是对象。"}]

    leaked = secret_request_fields(value)
    if leaked:
        errors.append(
            {
                "field": leaked[0],
                "code": "SECRET_FIELD_PROHIBITED",
                "message": "请求不得携带密钥、令牌或授权字段。",
            }
        )

    provider_key = str(value.get("provider_key", ""))
    profile = PROVIDER_PROFILES.get(provider_key)
    if not profile:
        errors.append({"field": "provider_key", "code": "UNKNOWN_PROVIDER", "message": "提供者不受支持。"})
    elif not is_remote_api_provider(profile):
        errors.append(
            {
                "field": "provider_key",
                "code": "NOT_REMOTE_PROVIDER",
                "message": "该预检路径只接受远端接口提供者。",
            }
        )
    elif not profile.get("trial_runner"):
        errors.append(
            {
                "field": "provider_key",
                "code": "REMOTE_PROVIDER_NOT_WIRED",
                "message": "该远端提供者尚未接入控制台预检。",
            }
        )
    elif profile.get("paid_execute_via_console") is not False:
        errors.append(
            {
                "field": "provider_key",
                "code": "CONSOLE_PAID_EXECUTE_NOT_DISABLED",
                "message": "控制台远端提供者必须明确禁止计费执行。",
            }
        )

    if "execute" in value:
        raw_execute = value.get("execute")
        if raw_execute is True:
            errors.append(
                {
                    "field": "execute",
                    "code": "CONSOLE_PAID_EXECUTE_PROHIBITED",
                    "message": "控制台不提交计费远端任务；请使用 CLI --execute。",
                }
            )
        elif raw_execute is not False:
            errors.append(
                {
                    "field": "execute",
                    "code": "UNKNOWN_EXECUTE_FLAG",
                    "message": "execute 只能是 false 或省略；未知值失败关闭。",
                }
            )

    generation_profile_key = str(
        value.get("generation_profile_key")
        or (profile or {}).get("default_generation_profile_key")
        or ""
    )
    generation_profile = GENERATION_PROFILES.get(generation_profile_key)
    if not generation_profile:
        errors.append(
            {
                "field": "generation_profile_key",
                "code": "UNKNOWN_GENERATION_PROFILE",
                "message": "生成档位不受支持。",
            }
        )
    elif profile and generation_profile["provider_key"] != provider_key:
        errors.append(
            {
                "field": "generation_profile_key",
                "code": "PROFILE_PROVIDER_MISMATCH",
                "message": "生成档位不适用于当前提供者。",
            }
        )

    execution_strategy = str(
        value.get("execution_strategy") or (profile or {}).get("default_execution_strategy") or ""
    )
    strategy = EXECUTION_STRATEGIES.get(execution_strategy)
    if not strategy:
        errors.append(
            {
                "field": "execution_strategy",
                "code": "UNKNOWN_EXECUTION_STRATEGY",
                "message": "执行策略不受支持。",
            }
        )
    elif profile and strategy.get("execution_backend", "local_diffusers") != provider_backend(profile):
        errors.append(
            {
                "field": "execution_strategy",
                "code": "STRATEGY_BACKEND_MISMATCH",
                "message": "执行策略不适用于当前提供者后端。",
            }
        )

    task_type = str(value.get("task_type") or "text_to_video")
    task = TASK_TYPES.get(task_type)
    if not task:
        errors.append({"field": "task_type", "code": "UNKNOWN_TASK_TYPE", "message": "作业类型不受支持。"})
    elif not task["available"]:
        errors.append({"field": "task_type", "code": "TASK_TYPE_UNAVAILABLE", "message": task["description"]})

    if errors:
        return None, errors

    assert profile is not None
    assert generation_profile is not None
    return {
        "provider_key": provider_key,
        "provider_identity": profile["provider_identity"],
        "model_id": profile["model_id"],
        "execution_backend": "remote_api",
        "task_type": task_type,
        "generation_profile_key": generation_profile_key,
        "execution_strategy": execution_strategy,
        "execute": False,
        "paid_remote_request": False,
        "credential_env": profile["credential_env"],
        "credential_recorded": False,
        "trial_contract": profile["trial_contract"],
        "generation": deepcopy(generation_profile["parameters"]),
        "formal_fact_creation": "PROHIBITED",
        "selection_decision_creation": "PROHIBITED",
        "timeline_binding_creation": "PROHIBITED",
        "institution_freeze_creation": "PROHIBITED",
    }, []


def validate_project_binding(
    value: Any,
    errors: list[dict[str, str]],
) -> dict[str, str] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        errors.append(
            {
                "field": "project_binding",
                "code": "INVALID_PROJECT_BINDING",
                "message": "样片项目绑定必须是对象。",
            }
        )
        return None
    fields = {
        "project_id": (PROJECT_ID_PATTERN, "样片项目标识无效。"),
        "shot_id": (SHOT_ID_PATTERN, "镜头标识无效。"),
        "project_contract_sha256": (SHA256_PATTERN, "样片合同摘要无效。"),
        "prompt_sha256": (SHA256_PATTERN, "镜头提示词摘要无效。"),
    }
    normalized: dict[str, str] = {}
    for field, (pattern, message) in fields.items():
        raw = str(value.get(field, ""))
        if not pattern.fullmatch(raw):
            errors.append(
                {
                    "field": f"project_binding.{field}",
                    "code": "INVALID_PROJECT_BINDING_FIELD",
                    "message": message,
                }
            )
        normalized[field] = raw
    return normalized


def integer_field(
    value: dict[str, Any],
    field: str,
    minimum: int,
    maximum: int,
    errors: list[dict[str, str]],
) -> int | None:
    raw = value.get(field)
    if isinstance(raw, bool):
        raw = None
    try:
        number = int(raw)
    except (TypeError, ValueError):
        errors.append({"field": field, "code": "INVALID_INTEGER", "message": f"{field} 必须是整数。"})
        return None
    if not minimum <= number <= maximum:
        errors.append(
            {
                "field": field,
                "code": "OUT_OF_BOUNDS",
                "message": f"{field} 必须位于 {minimum} 至 {maximum}。",
            }
        )
    return number


def float_field(
    value: dict[str, Any],
    field: str,
    minimum: float,
    maximum: float,
    errors: list[dict[str, str]],
) -> float | None:
    raw = value.get(field)
    if isinstance(raw, bool):
        raw = None
    try:
        number = float(raw)
    except (TypeError, ValueError):
        errors.append({"field": field, "code": "INVALID_FLOAT", "message": f"{field} 必须是数字。"})
        return None
    if not minimum <= number <= maximum:
        errors.append(
            {
                "field": field,
                "code": "OUT_OF_BOUNDS",
                "message": f"{field} 必须位于 {minimum} 至 {maximum}。",
            }
        )
    return number


def compile_runner_contract(job: dict[str, Any]) -> dict[str, Any]:
    profile = PROVIDER_PROFILES[job["provider_key"]]
    if is_remote_api_provider(profile):
        raise ValueError("远端提供者不能编译为本地运行器合同")
    provider = {
        "provider_identity": profile["provider_identity"],
        "model_id": profile["model_id"],
        "dtype": profile["dtype"],
        **job["parameters"],
    }
    if profile.get("vae_dtype"):
        provider["vae_dtype"] = profile["vae_dtype"]
    return {
        "contract_id": job["job_id"],
        "contract_status": "LOCAL_OPERATOR_JOB_NON_AUTHORITATIVE",
        "job_id": job["job_id"],
        "task_type": job["task_type"],
        "generation_profile_key": job["generation_profile_key"],
        "execution_strategy": job["execution_strategy"],
        "shared_prompt": job["prompt"],
        "shared_seed": job["seed"],
        "device": "mps",
        "mps_fallback_to_cpu": True,
        "timeout_seconds": job["timeout_seconds"],
        "resource_budget": deepcopy(job["resource_budget"]),
        "project_binding": deepcopy(job.get("project_binding")),
        "providers": {job["provider_key"]: provider},
        "non_goals": [
            "visual_quality_acceptance",
            "selection_decision",
            "cross_provider_contract_creation",
            "institution_freeze",
            "production_readiness",
        ],
    }


def validate_persisted_job(value: Any) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    if not isinstance(value, dict):
        return None, [{"field": "$", "code": "INVALID_JOB", "message": "持久化作业必须是对象。"}]
    resource_budget = value.get("resource_budget")
    if not isinstance(resource_budget, dict):
        return None, [{"field": "resource_budget", "code": "INVALID_BUDGET", "message": "资源预算缺失。"}]
    schema_version = value.get("schema_version")
    legacy_v2 = schema_version in LEGACY_JOB_SCHEMA_VERSIONS
    raw = {
        "execution_id": value.get("execution_id"),
        "provider_key": value.get("provider_key"),
        "task_type": value.get("task_type"),
        "prompt": value.get("prompt"),
        "seed": value.get("seed"),
        "generation_profile_key": value.get("generation_profile_key"),
        "execution_strategy": value.get("execution_strategy"),
        "parameters": value.get("parameters"),
        "timeout_seconds": value.get("timeout_seconds"),
        "preflight_min_available_memory_bytes": resource_budget.get("preflight_min_available_memory_bytes"),
        "preflight_max_swap_used_bytes": resource_budget.get("preflight_max_swap_used_bytes", 4 * GIB)
        if legacy_v2
        else resource_budget.get("preflight_max_swap_used_bytes"),
        "abort_min_available_memory_bytes": resource_budget.get("abort_min_available_memory_bytes"),
        "max_swap_growth_bytes": resource_budget.get("max_swap_growth_bytes"),
        "mps_memory_fraction": resource_budget.get("mps_memory_fraction"),
        "risk_acknowledged": value.get("risk_acknowledged"),
        "project_binding": value.get("project_binding"),
    }
    normalized, errors = validate_job_request(raw)
    job_id = str(value.get("job_id", ""))
    if not JOB_ID_PATTERN.fullmatch(job_id):
        errors.append({"field": "job_id", "code": "INVALID_JOB_ID", "message": "作业标识无效。"})
    if schema_version != JOB_SCHEMA_VERSION and schema_version not in LEGACY_JOB_SCHEMA_VERSIONS:
        errors.append({"field": "schema_version", "code": "INVALID_SCHEMA", "message": "作业规格版本不受支持。"})
    if normalized:
        protected = {
            "provider_identity": normalized["provider_identity"],
            "model_id": normalized["model_id"],
            "model_revision": normalized["model_revision"],
            "execution_strategy": normalized["execution_strategy"],
        }
        for field, expected in protected.items():
            if value.get(field) != expected:
                errors.append(
                    {
                        "field": field,
                        "code": "PROTECTED_FIELD_MISMATCH",
                        "message": f"{field} 与固定提供者配置不一致。",
                    }
                )
        if value.get("project_binding") != normalized.get("project_binding"):
            errors.append(
                {
                    "field": "project_binding",
                    "code": "PROTECTED_FIELD_MISMATCH",
                    "message": "样片项目绑定与不可变作业请求不一致。",
                }
            )
    if errors or not normalized:
        return None, errors
    normalized["job_id"] = job_id
    normalized["created_at"] = value.get("created_at")
    return normalized, []
