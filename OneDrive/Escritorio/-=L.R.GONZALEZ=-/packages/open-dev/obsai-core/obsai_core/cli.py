from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .fingerprint import make_fingerprint
from .gate import evaluate_action
from .jsonutil import pretty_json
from .metrics import estimate_regime, estimate_residue_from_signals, phi_eff_power
from .ontology import ObservationEnvelope, ObservationEnvelopeStore, PACReasoner, validate_observation_envelope
from .world import simulate_world


def read_json(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("JSON input must be an object")
    return data


def command_triage(args: argparse.Namespace) -> int:
    residue = estimate_residue_from_signals(args.signals)
    output = {
        "schemaVersion": "obsai.triage.v1",
        "signals": args.signals,
        "R": residue,
        "regime": estimate_regime(residue).value,
        "phi_eff": phi_eff_power(residue),
        "claims": {
            "calibration": "DEMO_ONLY",
        },
    }
    print(pretty_json(output))
    return 0


def command_evaluate_action(args: argparse.Namespace) -> int:
    print(pretty_json(evaluate_action(read_json(args.action_file))))
    return 0


def command_validate_envelope(args: argparse.Namespace) -> int:
    envelope = ObservationEnvelope.from_dict(read_json(args.envelope_file))
    validation = validate_observation_envelope(envelope)
    reasoning = PACReasoner().evaluate(envelope)
    payload: dict[str, Any] = {
        "envelope": envelope.to_dict(),
        "validation": validation,
        "reasoning": reasoning,
    }
    if args.db:
        payload["stored"] = ObservationEnvelopeStore(args.db).insert_envelope(envelope)
    print(pretty_json(payload))
    return 0


def command_fingerprint(args: argparse.Namespace) -> int:
    residue = estimate_residue_from_signals(args.signals)
    output = make_fingerprint(
        session_id=args.session_id,
        residue=residue,
        signals=args.signals,
        decisions=args.decision,
        pending=[{"task": item, "evidence": "operator supplied"} for item in args.pending],
        next_action=args.next_action,
    )
    print(pretty_json(output))
    return 0


def command_simulate_world(args: argparse.Namespace) -> int:
    print(pretty_json(simulate_world(ticks=args.ticks, seed=args.seed)))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="obsai-core operational CLI.")
    sub = parser.add_subparsers(dest="command", required=True)

    triage = sub.add_parser("triage", help="estimate residue/regime from signals")
    triage.add_argument("--signals", nargs="*", default=[])
    triage.set_defaults(func=command_triage)

    action = sub.add_parser("evaluate-action", help="evaluate an action JSON file")
    action.add_argument("action_file")
    action.set_defaults(func=command_evaluate_action)

    envelope = sub.add_parser("validate-envelope", help="validate and optionally store an observation envelope")
    envelope.add_argument("envelope_file")
    envelope.add_argument("--db", default="")
    envelope.set_defaults(func=command_validate_envelope)

    fingerprint = sub.add_parser("fingerprint", help="generate a stable session fingerprint")
    fingerprint.add_argument("--session-id", required=True)
    fingerprint.add_argument("--signals", nargs="*", default=[])
    fingerprint.add_argument("--decision", action="append", default=[])
    fingerprint.add_argument("--pending", action="append", default=[])
    fingerprint.add_argument("--next-action", default="")
    fingerprint.set_defaults(func=command_fingerprint)

    world = sub.add_parser("simulate-world", help="run deterministic world simulation")
    world.add_argument("--ticks", type=int, default=20)
    world.add_argument("--seed", default="obsai")
    world.set_defaults(func=command_simulate_world)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
