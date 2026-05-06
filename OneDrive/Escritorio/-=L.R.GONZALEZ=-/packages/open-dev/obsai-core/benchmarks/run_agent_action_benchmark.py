from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from demo_agent_action import build_demo_action
from obsai_core.gate import evaluate_action


def iter_scenarios(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def run_benchmark(path: Path) -> dict[str, Any]:
    rows = iter_scenarios(path)
    results = []
    for row in rows:
        decision = evaluate_action(build_demo_action(str(row["action"])))
        status = decision["status"]
        expected = str(row["expected"])
        results.append(
            {
                "id": row["id"],
                "action": row["action"],
                "expected": expected,
                "actual": status,
                "ok": status == expected,
                "risk_class": row.get("risk_class"),
                "should_prevent_error": bool(row.get("should_prevent_error")),
                "R": decision["scores"]["R"],
                "theta": decision["theta"],
                "reason": decision["reasons"][0] if decision["reasons"] else "",
            }
        )
    total = len(results)
    correct = sum(1 for item in results if item["ok"])
    prevented = sum(1 for item in results if item["should_prevent_error"] and item["actual"] in {"BLOCK", "REVIEW"})
    false_blocks = sum(1 for item in results if item["expected"] == "APPROVE" and item["actual"] == "BLOCK")
    correct_allows = sum(1 for item in results if item["expected"] == "APPROVE" and item["actual"] == "APPROVE")
    return {
        "schemaVersion": "obsai.agent_action_benchmark.v1",
        "scenario_count": total,
        "accuracy": round(correct / total, 4) if total else 0.0,
        "errors_prevented": prevented,
        "false_blocks": false_blocks,
        "correct_allows": correct_allows,
        "human_review_cost": sum(1 for item in results if item["actual"] == "REVIEW"),
        "thresholds": "DEMO_ONLY",
        "results": results,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the starter obsai-core agent action benchmark.")
    parser.add_argument(
        "--scenarios",
        default=str(Path(__file__).with_name("agent_action_scenarios.jsonl")),
        help="JSONL scenario file.",
    )
    args = parser.parse_args(argv)
    print(json.dumps(run_benchmark(Path(args.scenarios)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
