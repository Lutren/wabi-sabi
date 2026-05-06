#!/usr/bin/env python3
"""
Model Slimmer evidence lane for Brain OS / ClaudioOS.

This module does not prune or quantize models. It creates the measurement
contract that must be satisfied before a smaller model replaces a baseline.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any
import argparse
import json


SCHEMA = "model_slimmer.evidence/v0.1"
REQUIRED_METRICS = {"accuracy", "latency_ms", "memory_mb", "safety_score"}


def default_acceptance() -> dict[str, Any]:
    return {
        "accuracy_drop_max": 0.02,
        "safety_drop_max": 0.01,
        "latency_must_not_increase": True,
        "memory_must_not_increase": True,
        "energy_must_not_increase": True,
        "regression_suite_required": True,
        "human_approval_for_replacement": True,
    }


def generate_plan(
    *,
    model: str,
    task: str,
    baseline: dict[str, float],
    acceptance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    _require_metrics(baseline, "baseline")
    return {
        "schema": SCHEMA,
        "model": model,
        "task": task,
        "baseline": deepcopy(baseline),
        "variants": [
            {"id": "quantize_q8", "method": "quantization", "target": "q8", "risk": "low"},
            {"id": "quantize_q5", "method": "quantization", "target": "q5", "risk": "medium"},
            {"id": "quantize_q4", "method": "quantization", "target": "q4", "risk": "medium"},
            {"id": "prune_30", "method": "pruning", "sparsity": 0.30, "risk": "medium"},
            {"id": "prune_50", "method": "pruning", "sparsity": 0.50, "risk": "high"},
            {"id": "prune_70", "method": "pruning", "sparsity": 0.70, "risk": "high"},
            {"id": "prune_90", "method": "pruning", "sparsity": 0.90, "risk": "critical"},
        ],
        "acceptance": deepcopy(acceptance or default_acceptance()),
        "gates": [
            "baseline_evidence",
            "task_accuracy",
            "latency",
            "memory",
            "energy",
            "safety",
            "regression",
            "human_approval",
        ],
        "decision": "measure_before_adoption",
    }


def assess_candidate(plan: dict[str, Any], candidate: dict[str, float]) -> dict[str, Any]:
    _require_metrics(candidate, "candidate")
    baseline = plan["baseline"]
    acceptance = plan["acceptance"]

    accuracy_drop = float(baseline["accuracy"]) - float(candidate["accuracy"])
    safety_drop = float(baseline["safety_score"]) - float(candidate["safety_score"])
    latency_delta = float(candidate["latency_ms"]) - float(baseline["latency_ms"])
    memory_delta = float(candidate["memory_mb"]) - float(baseline["memory_mb"])
    energy_delta = float(candidate.get("energy_wh", 0.0)) - float(baseline.get("energy_wh", 0.0))

    failures: list[str] = []
    if accuracy_drop > float(acceptance["accuracy_drop_max"]):
        failures.append("accuracy_drop")
    if safety_drop > float(acceptance["safety_drop_max"]):
        failures.append("safety_drop")
    if acceptance.get("latency_must_not_increase") and latency_delta > 0:
        failures.append("latency_increase")
    if acceptance.get("memory_must_not_increase") and memory_delta > 0:
        failures.append("memory_increase")
    if acceptance.get("energy_must_not_increase") and energy_delta > 0:
        failures.append("energy_increase")

    decision = "allow" if not failures else "block"
    reason = "candidate meets measured thresholds" if not failures else f"failed gates: {', '.join(failures)}"
    if acceptance.get("human_approval_for_replacement") and decision == "allow":
        decision = "ask"
        reason = "candidate meets thresholds; replacement requires approval"

    return {
        "schema": SCHEMA,
        "model": plan["model"],
        "task": plan["task"],
        "decision": decision,
        "reason": reason,
        "deltas": {
            "accuracy_drop": round(accuracy_drop, 6),
            "safety_drop": round(safety_drop, 6),
            "latency_delta_ms": round(latency_delta, 6),
            "memory_delta_mb": round(memory_delta, 6),
            "energy_delta_wh": round(energy_delta, 6),
        },
        "failures": failures,
    }


def _require_metrics(metrics: dict[str, Any], label: str) -> None:
    missing = sorted(REQUIRED_METRICS - set(metrics))
    if missing:
        raise ValueError(f"{label} missing required metrics: {missing}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a model slimmer evidence plan")
    parser.add_argument("--model", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--accuracy", required=True, type=float)
    parser.add_argument("--latency-ms", required=True, type=float)
    parser.add_argument("--memory-mb", required=True, type=float)
    parser.add_argument("--safety-score", required=True, type=float)
    parser.add_argument("--energy-wh", type=float, default=0.0)
    args = parser.parse_args()

    plan = generate_plan(
        model=args.model,
        task=args.task,
        baseline={
            "accuracy": args.accuracy,
            "latency_ms": args.latency_ms,
            "memory_mb": args.memory_mb,
            "safety_score": args.safety_score,
            "energy_wh": args.energy_wh,
        },
    )
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
