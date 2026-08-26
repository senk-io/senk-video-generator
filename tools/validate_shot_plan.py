"""读取真实本地模型输出并打印非权威规划观察。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from shot_planning.prompting import build_local_planner_prompt
from shot_planning.stability import observe_stability
from shot_planning.validation import observe_proposal


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="验证一句话镜头规划草案；输出观察，不创建通过、失败或选择裁决。"
    )
    parser.add_argument("--request", required=True, type=Path, help="规划请求 JSON")
    parser.add_argument(
        "--proposal",
        action="append",
        default=[],
        type=Path,
        help="本地模型原始规划 JSON；重复传入时生成稳定性观察",
    )
    parser.add_argument(
        "--print-prompt",
        action="store_true",
        help="打印可交给本地文本模型的提示合同",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    request = _read_json(args.request)
    if args.print_prompt:
        output = build_local_planner_prompt(request)
    elif not args.proposal:
        raise SystemExit("至少传入一个 --proposal，或使用 --print-prompt。")
    elif len(args.proposal) == 1:
        output = observe_proposal(request, _read_json(args.proposal[0]))
    else:
        output = observe_stability(request, [_read_json(path) for path in args.proposal])
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
