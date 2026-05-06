from __future__ import annotations

import argparse
import json

from .core import falsify_run, report_run, run_simulation, to_jsonable


def _print(payload: object) -> None:
    print(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description="DUAT Genesis synthetic simulation sandbox.")
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("run", "report", "falsify"):
        command = sub.add_parser(name)
        command.add_argument("--seed", default="demo")
        command.add_argument("--size", type=int, default=8)
        command.add_argument("--ticks", type=int, default=5)

    args = parser.parse_args()
    run = run_simulation(seed=args.seed, size=args.size, ticks=args.ticks)

    if args.command == "run":
        _print(run)
    elif args.command == "report":
        _print(report_run(run))
    elif args.command == "falsify":
        _print(falsify_run(run))


if __name__ == "__main__":
    main()
