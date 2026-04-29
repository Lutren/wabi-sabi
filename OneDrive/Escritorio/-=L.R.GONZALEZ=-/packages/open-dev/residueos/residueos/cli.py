from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .gate import evaluate_action
from .server import run_server
from .store import ResidueStore


DEFAULT_DB = Path("runtime") / "residueos.sqlite"


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def read_action(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("action JSON must be an object")
    return data


def command_evaluate(args: argparse.Namespace) -> int:
    action = read_action(Path(args.action_file))
    decision = evaluate_action(action)
    if args.no_store:
        print_json({"action": action, "decision": decision})
        return 0
    store = ResidueStore(args.db)
    record = store.insert_action(action, decision)
    print_json(record)
    return 0


def command_actions(args: argparse.Namespace) -> int:
    store = ResidueStore(args.db)
    print_json(store.list_actions(limit=args.limit))
    return 0


def command_review(args: argparse.Namespace) -> int:
    store = ResidueStore(args.db)
    record = store.update_human_decision(
        args.action_id,
        status=args.status,
        reviewer=args.reviewer,
        note=args.note,
    )
    if record is None:
        print_json({"error": "not found", "id": args.action_id})
        return 1
    print_json(record)
    return 0


def command_dashboard(args: argparse.Namespace) -> int:
    store = ResidueStore(args.db)
    print_json(store.dashboard_stats())
    return 0


def command_serve(args: argparse.Namespace) -> int:
    run_server(db_path=args.db, host=args.host, port=args.port)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ResidueOS local action gate.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate = subparsers.add_parser("evaluate", help="evaluate an action JSON file")
    evaluate.add_argument("action_file")
    evaluate.add_argument("--db", default=str(DEFAULT_DB))
    evaluate.add_argument("--no-store", action="store_true")
    evaluate.set_defaults(func=command_evaluate)

    actions = subparsers.add_parser("actions", help="list stored action records")
    actions.add_argument("--db", default=str(DEFAULT_DB))
    actions.add_argument("--limit", type=int, default=100)
    actions.set_defaults(func=command_actions)

    review = subparsers.add_parser("review", help="attach a human review decision")
    review.add_argument("action_id")
    review.add_argument("--db", default=str(DEFAULT_DB))
    review.add_argument("--status", choices=["APPROVED", "BLOCKED"], required=True)
    review.add_argument("--reviewer", default="human")
    review.add_argument("--note", default="")
    review.set_defaults(func=command_review)

    dashboard = subparsers.add_parser("dashboard", help="print aggregate dashboard stats")
    dashboard.add_argument("--db", default=str(DEFAULT_DB))
    dashboard.set_defaults(func=command_dashboard)

    serve = subparsers.add_parser("serve", help="run the local HTTP API")
    serve.add_argument("--db", default=str(DEFAULT_DB))
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8787)
    serve.set_defaults(func=command_serve)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
