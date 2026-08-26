"""可替换视频能力提供者的协议适配器。"""

from .minimax_h3 import (
    MINIMAX_H3_API_BASE,
    MINIMAX_H3_API_KEY_ENV,
    MINIMAX_H3_MODEL_ID,
    AdapterError,
    MiniMaxH3Transport,
    build_generation_payload,
    run_trial,
    validate_trial_contract,
)

__all__ = [
    "MINIMAX_H3_API_BASE",
    "MINIMAX_H3_API_KEY_ENV",
    "MINIMAX_H3_MODEL_ID",
    "AdapterError",
    "MiniMaxH3Transport",
    "build_generation_payload",
    "run_trial",
    "validate_trial_contract",
]
