"""CLI for GEODIA Social Observatory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .behavior import analyze_behavior_signature
from .duat_sim import run_duat_conway_simulation
from .duat_v2_intake import build_duat_v2_intake
from .events import JsonlEventStore, build_event
from .health import duat_health_window
from .model import build_scenario_report, run_backtest
from .router import decide_route, features_from_mapping
from .snapshot import create_snapshot_from_fixture
from .sources import source_catalog, validate_source
from .source_registry import build_local_source_intake


def _write_or_print(data: dict[str, Any] | list[dict[str, Any]], out: str | None, pretty: bool) -> None:
    text = json.dumps(data, indent=2 if pretty else None, ensure_ascii=False, sort_keys=pretty)
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def _require_offline(args: argparse.Namespace) -> None:
    if not args.offline:
        raise SystemExit("online fetch is not implemented in v1; rerun with --offline and a fixture")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="GEODIA Social Observatory local MVP.")
    sub = parser.add_subparsers(dest="command", required=True)

    catalog = sub.add_parser("catalog", help="print the source allowlist")
    catalog.add_argument("--pretty", action="store_true")
    catalog.add_argument("--out")

    validate = sub.add_parser("validate-source", help="validate a source id and URL against the allowlist")
    validate.add_argument("--source-id", required=True)
    validate.add_argument("--source-url", required=True)
    validate.add_argument("--pretty", action="store_true")
    validate.add_argument("--out")

    snapshot = sub.add_parser("snapshot", help="create a source snapshot from an offline fixture")
    snapshot.add_argument("--offline", action="store_true")
    snapshot.add_argument("--fixture", required=True)
    snapshot.add_argument("--pretty", action="store_true")
    snapshot.add_argument("--out")

    run = sub.add_parser("run", help="create a scenario report from an offline fixture")
    run.add_argument("--offline", action="store_true")
    run.add_argument("--fixture", required=True)
    run.add_argument("--holdout-year", type=int)
    run.add_argument("--pretty", action="store_true")
    run.add_argument("--out")

    backtest = sub.add_parser("backtest", help="run the reproducible offline holdout check")
    backtest.add_argument("--offline", action="store_true")
    backtest.add_argument("--fixture", required=True)
    backtest.add_argument("--holdout-year", type=int)
    backtest.add_argument("--pretty", action="store_true")
    backtest.add_argument("--out")

    intake = sub.add_parser("intake", help="classify the selected Downloads sources without copying them")
    intake.add_argument("--pretty", action="store_true")
    intake.add_argument("--out")

    duat_v2_intake = sub.add_parser("duat-v2-intake", help="distill the latest DUAT v2 Downloads files")
    duat_v2_intake.add_argument("--pretty", action="store_true")
    duat_v2_intake.add_argument("--out")

    signature = sub.add_parser("signature", help="extract an 8-dimension behavioral signature from text")
    signature.add_argument("--text")
    signature.add_argument("--file")
    signature.add_argument("--subject-id", default="local_text")
    signature.add_argument("--pretty", action="store_true")
    signature.add_argument("--out")

    route = sub.add_parser("route", help="decide cache/small/strong/sim/human from a feature JSON object")
    route.add_argument("--features-json")
    route.add_argument("--features-file")
    route.add_argument("--pretty", action="store_true")
    route.add_argument("--out")

    health = sub.add_parser("health", help="compute DUAT health metrics from a JSON list of event metric rows")
    health.add_argument("--window-json")
    health.add_argument("--window-file")
    health.add_argument("--pretty", action="store_true")
    health.add_argument("--out")

    sim = sub.add_parser("simulate-duat", help="run a deterministic DUAT/Conway lab simulation")
    sim.add_argument("--seed", type=int, default=42)
    sim.add_argument("--size", type=int, default=24)
    sim.add_argument("--steps", type=int, default=20)
    sim.add_argument("--chi", type=float, default=0.567)
    sim.add_argument("--sigma", type=float, default=0.12)
    sim.add_argument("--pretty", action="store_true")
    sim.add_argument("--out")

    append_event = sub.add_parser("event-append", help="append one event to a local JSONL event store")
    append_event.add_argument("--store", required=True)
    append_event.add_argument("--event-type", required=True)
    append_event.add_argument("--actor-id", required=True)
    append_event.add_argument("--payload-json", required=True)
    append_event.add_argument("--actor-type", default="agent")
    append_event.add_argument("--risk-level", default="low")
    append_event.add_argument("--approval-state", default="none")
    append_event.add_argument("--ts", default="1970-01-01T00:00:00Z")
    append_event.add_argument("--pretty", action="store_true")
    append_event.add_argument("--out")

    replay = sub.add_parser("event-replay", help="replay a local JSONL event store")
    replay.add_argument("--store", required=True)
    replay.add_argument("--pretty", action="store_true")
    replay.add_argument("--out")

    args = parser.parse_args(argv)

    if args.command == "catalog":
        _write_or_print(source_catalog(), args.out, args.pretty)
        return 0
    if args.command == "validate-source":
        policy = validate_source(args.source_id, args.source_url)
        _write_or_print(
            {
                "ok": True,
                "source_id": policy.source_id,
                "role": policy.role,
                "classification_floor": policy.classification_floor,
                "requires_api_key": policy.requires_api_key,
            },
            args.out,
            args.pretty,
        )
        return 0
    if args.command == "snapshot":
        _require_offline(args)
        _write_or_print(create_snapshot_from_fixture(args.fixture), args.out, args.pretty)
        return 0
    if args.command == "backtest":
        _require_offline(args)
        _write_or_print(run_backtest(args.fixture, args.holdout_year), args.out, args.pretty)
        return 0
    if args.command == "run":
        _require_offline(args)
        snap = create_snapshot_from_fixture(args.fixture)
        bt = run_backtest(args.fixture, args.holdout_year)
        _write_or_print(build_scenario_report(snap, bt), args.out, args.pretty)
        return 0
    if args.command == "intake":
        _write_or_print(build_local_source_intake(), args.out, args.pretty)
        return 0
    if args.command == "duat-v2-intake":
        _write_or_print(build_duat_v2_intake(), args.out, args.pretty)
        return 0
    if args.command == "signature":
        if bool(args.text) == bool(args.file):
            raise SystemExit("provide exactly one of --text or --file")
        text = args.text if args.text is not None else Path(args.file).read_text(encoding="utf-8")
        _write_or_print(analyze_behavior_signature(text, subject_id=args.subject_id), args.out, args.pretty)
        return 0
    if args.command == "route":
        if bool(args.features_json) == bool(args.features_file):
            raise SystemExit("provide exactly one of --features-json or --features-file")
        raw = args.features_json if args.features_json else Path(args.features_file).read_text(encoding="utf-8")
        _write_or_print(decide_route(features_from_mapping(json.loads(raw))), args.out, args.pretty)
        return 0
    if args.command == "health":
        if bool(args.window_json) == bool(args.window_file):
            raise SystemExit("provide exactly one of --window-json or --window-file")
        raw = args.window_json if args.window_json else Path(args.window_file).read_text(encoding="utf-8")
        _write_or_print(duat_health_window(json.loads(raw)), args.out, args.pretty)
        return 0
    if args.command == "simulate-duat":
        _write_or_print(
            run_duat_conway_simulation(
                seed=args.seed,
                size=args.size,
                steps=args.steps,
                chi=args.chi,
                sigma=args.sigma,
            ),
            args.out,
            args.pretty,
        )
        return 0
    if args.command == "event-append":
        payload = json.loads(args.payload_json)
        event = build_event(
            args.event_type,
            args.actor_id,
            payload,
            actor_type=args.actor_type,
            risk_level=args.risk_level,
            approval_state=args.approval_state,
            ts=args.ts,
        )
        JsonlEventStore(args.store).append(event)
        _write_or_print(event, args.out, args.pretty)
        return 0
    if args.command == "event-replay":
        _write_or_print(JsonlEventStore(args.store).replay_state(), args.out, args.pretty)
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
