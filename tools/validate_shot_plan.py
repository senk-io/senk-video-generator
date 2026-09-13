"""Read real local-model output and print non-authoritative planning observations."""

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
        description="Validate a one-sentence shot-planning draft; emit observations, not pass/fail/selection decisions."
    )
    parser.add_argument("--request", required=True, type=Path, help="Planning-request JSON")
    parser.add_argument(
        "--proposal",
        action="append",
        default=[],
        type=Path,
        help="Raw local-model planning JSON; pass more than once to emit stability observations",
    )
    parser.add_argument(
        "--print-prompt",
        action="store_true",
        help="Print the prompt contract that can be given to a local text model",
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
