from __future__ import annotations

import argparse
import json
from typing import Sequence

from .core import fingerprint_payload, load_json, noise_report, observe_payload


def print_json(payload: object) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))


def observe_main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Observe a JSON response sample.")
    parser.add_argument("input_json")
    args = parser.parse_args(argv)
    print_json(observe_payload(load_json(args.input_json)))
    return 0


def noise_report_main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare cleanup noise before and after.")
    parser.add_argument("before_json")
    parser.add_argument("after_json")
    args = parser.parse_args(argv)
    print_json(noise_report(load_json(args.before_json), load_json(args.after_json)))
    return 0


def fingerprint_main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a stable sample fingerprint.")
    parser.add_argument("sample_json")
    args = parser.parse_args(argv)
    print_json(fingerprint_payload(load_json(args.sample_json)))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gemma Observacionismo cleanup toolkit.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    observe = subparsers.add_parser("observe")
    observe.add_argument("input_json")

    report = subparsers.add_parser("noise-report")
    report.add_argument("before_json")
    report.add_argument("after_json")

    fingerprint = subparsers.add_parser("fingerprint")
    fingerprint.add_argument("sample_json")

    args = parser.parse_args(argv)
    if args.command == "observe":
        return observe_main([args.input_json])
    if args.command == "noise-report":
        return noise_report_main([args.before_json, args.after_json])
    if args.command == "fingerprint":
        return fingerprint_main([args.sample_json])
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
