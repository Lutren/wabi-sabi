from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from obsai_core.gate import evaluate_action


def _slug(value: str) -> str:
    cleaned = []
    for char in value.lower():
        if char.isalnum():
            cleaned.append(char)
        elif cleaned and cleaned[-1] != "-":
            cleaned.append("-")
    return "".join(cleaned).strip("-")[:64] or "action"


def build_demo_action(description: str) -> dict[str, Any]:
    text = description.lower()
    if any(token in text for token in ("delete", "remove", "rm ", "rmdir", "wipe", "drop")):
        return {
            "actor": "demo-agent",
            "action_type": "delete",
            "input": description,
            "output": "Requested destructive filesystem action.",
            "risk": 0.96,
            "reversibility": 0.04,
            "requires_receptor": True,
            "receptor_id": "",
            "sources": [],
            "tool_calls": [],
            "policy_tags": ["requires_authorized_receptor", "requires_human_approval"],
            "self_check": {
                "summary": "No backup proof, receptor authorization, or rollback plan was provided.",
                "confidence": 0.35,
                "assumptions": ["the target may contain user work"],
                "uncertainties": ["backup state unknown", "owner authorization missing"],
                "falsifiers": ["verified backup exists", "authorized receptor is attached", "rollback plan is present"],
            },
        }
    if any(token in text for token in ("summarize", "summary", "readme", "read ")):
        return {
            "actor": "demo-agent",
            "action_type": "read_only_summary",
            "input": description,
            "output": (
                "Summarize a public README without changing files, without sending network requests, "
                "and with the local file path recorded as the only source of evidence."
            ),
            "risk": 0.20,
            "reversibility": 0.85,
            "sources": [{"label": "README.md", "confidence": 0.92, "verified": True}],
            "tool_calls": [{"name": "read_file", "status": "ok"}],
            "self_check": {
                "summary": "Read-only action with a verified local source.",
                "confidence": 0.88,
                "assumptions": [],
                "uncertainties": [],
                "falsifiers": ["README path missing", "source content unavailable"],
            },
        }
    return {
        "actor": "demo-agent",
        "action_type": "general_agent_action",
        "input": description,
        "output": "Unclassified agent action.",
        "risk": 0.45,
        "reversibility": 0.50,
        "sources": [],
        "tool_calls": [],
        "self_check": {
            "summary": "Action requires more context before execution.",
            "confidence": 0.45,
            "assumptions": ["intent is underspecified"],
            "uncertainties": ["risk classification unknown"],
            "falsifiers": ["operator supplies action type, evidence, and receptor"],
        },
    }


def summarize_decision(description: str, decision: dict[str, Any], witness_path: Path) -> dict[str, Any]:
    residue = decision["residue"]
    evidence = []
    for key in ("missing_evidence", "policy_violations", "unresolved", "assumptions"):
        evidence.extend(str(item) for item in residue.get(key, []))
    return {
        "schemaVersion": "obsai.demo_agent_action.v1",
        "action": description,
        "decision": decision["status"],
        "reason": decision["reasons"][0] if decision["reasons"] else "no_reason_recorded",
        "evidence": evidence,
        "scores": {
            "R": decision["scores"]["R"],
            "theta": decision["theta"],
            "thresholds": decision["claims"]["thresholdCalibration"],
        },
        "witness_log": witness_path.as_posix(),
    }


def run_demo(description: str, witness_dir: Path) -> dict[str, Any]:
    action = build_demo_action(description)
    decision = evaluate_action(action)
    witness_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    witness_path = witness_dir / f"{stamp}-{_slug(description)}.json"
    summary = summarize_decision(description, decision, witness_path)
    witness_payload = {
        "schemaVersion": "obsai.witness_log.v1",
        "created_at": stamp,
        "input_action": description,
        "action": action,
        "decision": decision,
        "summary": summary,
        "note": "Demo only. The requested action is evaluated but never executed.",
    }
    witness_path.write_text(json.dumps(witness_payload, indent=2) + "\n", encoding="utf-8")
    return summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the obsai-core action-gate demo.")
    parser.add_argument("--action", required=True, help="Natural-language action to evaluate.")
    parser.add_argument("--witness-dir", default="witness", help="Directory for witness logs.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(json.dumps(run_demo(args.action, Path(args.witness_dir)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
