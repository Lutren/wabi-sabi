"""DUAT health metrics over a window of local events."""

from __future__ import annotations

from statistics import mean
from typing import Any

from .contracts import DUAT_HEALTH_WINDOW_SCHEMA


def _avg(rows: list[dict[str, Any]], key: str, default: float = 0.0) -> float:
    if not rows:
        return default
    return mean(float(row.get(key, default)) for row in rows)


def duat_health_window(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "schema": DUAT_HEALTH_WINDOW_SCHEMA,
            "status": "empty",
            "epsilon": 1.0,
            "R": 1.0,
            "Phi_eff": 0.0,
            "fitness": 0.0,
            "Phi_Duat": 0.0,
        }
    epsilon = _avg(rows, "verify_fail")
    residue = mean(
        float(row.get("residue", 0.0))
        + 0.25 * float(row.get("queue_pressure", 0.0))
        + 0.25 * float(row.get("auth_drift", 0.0))
        + 0.25 * float(row.get("rework", 0.0))
        + 0.25 * float(row.get("social_conflict", 0.0))
        for row in rows
    )
    utility = _avg(rows, "accepted_utility")
    latency_ms = max(_avg(rows, "latency_ms", 1.0), 1.0)
    gpu_seconds = max(_avg(rows, "gpu_seconds", 0.1), 0.1)
    phi_eff = utility / (latency_ms * gpu_seconds + 1.0)
    cooperation = _avg(rows, "cooperation")
    incidents = _avg(rows, "security_incident")
    authenticity = 1.0 - _avg(rows, "auth_drift")
    coherence = 1.0 - _avg(rows, "contradiction")
    adaptability = _avg(rows, "novelty_kept")
    fitness = 0.45 * phi_eff + 0.20 * cooperation + 0.15 * coherence - 0.10 * epsilon - 0.10 * residue
    phi_duat = ((1.0 - epsilon) * coherence * authenticity * adaptability) / (1.0 + residue + incidents)
    return {
        "schema": DUAT_HEALTH_WINDOW_SCHEMA,
        "status": "evaluated",
        "event_count": len(rows),
        "epsilon": round(float(epsilon), 6),
        "R": round(float(residue), 6),
        "Phi_eff": round(float(phi_eff), 6),
        "fitness": round(float(fitness), 6),
        "Phi_Duat": round(float(phi_duat), 6),
        "claim_boundary": "engineering metric window; not a scientific law",
    }
