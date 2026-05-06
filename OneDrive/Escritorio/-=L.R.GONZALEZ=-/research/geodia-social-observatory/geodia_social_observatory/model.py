"""DUAT, Conway and Observacionismo reporting for social epoch fixtures."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from .contracts import EPOCH_MODEL_SCHEMA, SCENARIO_REPORT_SCHEMA, claim
from .snapshot import create_snapshot_from_fixture


def _by_indicator(snapshot: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in snapshot.get("observations", []):
        grouped[str(item["indicator"])].append(item)
    for rows in grouped.values():
        rows.sort(key=lambda row: int(row["year"]))
    return dict(grouped)


def _direction(first: float, last: float, polarity: str) -> str:
    delta = last - first
    if abs(delta) < 0.000001:
        return "stable"
    improves = delta > 0 if polarity == "positive" else delta < 0
    return "improving" if improves else "degrading"


def normalize_indicators(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    normalized = []
    for name, rows in _by_indicator(snapshot).items():
        if not rows:
            continue
        first = float(rows[0]["value"])
        last = float(rows[-1]["value"])
        polarity = str(rows[-1].get("polarity", rows[0].get("polarity", "positive")))
        span = max(1, int(rows[-1]["year"]) - int(rows[0]["year"]))
        denominator = max(abs(first), 1.0)
        normalized_delta = (last - first) / denominator
        normalized.append(
            {
                "indicator": name,
                "first_year": int(rows[0]["year"]),
                "last_year": int(rows[-1]["year"]),
                "first_value": first,
                "last_value": last,
                "unit": rows[-1].get("unit", ""),
                "polarity": polarity,
                "normalized_delta": round(normalized_delta, 6),
                "annualized_delta": round(normalized_delta / span, 6),
                "direction": _direction(first, last, polarity),
                "evidence_ref": snapshot["content_sha256"],
            }
        )
    return normalized


def duat_state(normalized: list[dict[str, Any]]) -> dict[str, object]:
    if not normalized:
        return {
            "residue": 1.0,
            "resonance": 0.0,
            "regulator": "BLOCK",
            "notes": ["no indicator evidence"],
        }
    magnitude = mean(abs(float(row["normalized_delta"])) for row in normalized)
    degrading = sum(1 for row in normalized if row["direction"] == "degrading")
    residue = min(1.0, round(magnitude + degrading * 0.08, 6))
    resonance = round(max(0.0, 1.0 - residue), 6)
    if residue >= 0.7:
        regulator = "BLOCK"
    elif residue >= 0.35 or degrading >= max(2, len(normalized)):
        regulator = "REVIEW"
    else:
        regulator = "OBSERVE"
    return {
        "residue": residue,
        "resonance": resonance,
        "regulator": regulator,
        "notes": ["demo thresholds; calibrate with real historical datasets before claims"],
    }


def conway_specialists(normalized: list[dict[str, Any]], duat: dict[str, object], source_role: str) -> list[dict[str, object]]:
    improving = sum(1 for row in normalized if row["direction"] == "improving")
    degrading = sum(1 for row in normalized if row["direction"] == "degrading")
    stable = sum(1 for row in normalized if row["direction"] == "stable")
    residue = float(duat["residue"])
    agents = [
        {
            "agent": "continuity",
            "score": round((stable + improving * 0.5) / max(1, len(normalized)), 6),
            "classification": "INFERENCIA",
            "interpretation": "institutional or social continuity remains plausible",
        },
        {
            "agent": "rupture",
            "score": round(min(1.0, residue + degrading * 0.12), 6),
            "classification": "INFERENCIA",
            "interpretation": "transition pressure is visible in indicator movement",
        },
        {
            "agent": "regulator",
            "score": round(1.0 if duat["regulator"] != "OBSERVE" else 0.35, 6),
            "classification": "INFERENCIA",
            "interpretation": "DUAT regulator requires slower claims when residue is high",
        },
    ]
    if source_role == "media_narrative_signal_only":
        agents.append(
            {
                "agent": "media_narrative",
                "score": 1.0,
                "classification": "INFERENCIA",
                "interpretation": "media signal cannot be upgraded to raw social fact without corroboration",
            }
        )
    return sorted(agents, key=lambda item: (-float(item["score"]), str(item["agent"])))


def epoch_label(agents: list[dict[str, object]], duat: dict[str, object]) -> str:
    top = agents[0]["agent"] if agents else "unknown"
    residue = float(duat["residue"])
    if duat["regulator"] == "REVIEW" and top == "rupture":
        return "transition_review"
    if residue < 0.12:
        return "continuity_low_residue"
    if top == "continuity":
        return "continuity_with_residue"
    return "mixed_transition"


def build_epoch_model(snapshot: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_indicators(snapshot)
    duat = duat_state(normalized)
    agents = conway_specialists(normalized, duat, str(snapshot["source"]["role"]))
    return {
        "schema": EPOCH_MODEL_SCHEMA,
        "input_snapshot_sha256": snapshot["content_sha256"],
        "source_role": snapshot["source"]["role"],
        "geography": snapshot.get("geography", "UNKNOWN"),
        "period": snapshot.get("period", "UNKNOWN"),
        "indicator_count": len(normalized),
        "event_count": len(snapshot.get("events", [])),
        "normalized_indicators": normalized,
        "duat": duat,
        "conway_specialists": agents,
        "epoch_label": epoch_label(agents, duat),
        "claim_boundary": "scenario model only; no guaranteed prediction",
    }


def _aggregate_direction(rows: list[dict[str, Any]], year_a: int, year_b: int) -> str:
    by_year: dict[int, list[float]] = defaultdict(list)
    for row in rows:
        by_year[int(row["year"])].append(float(row["value"]))
    if year_a not in by_year or year_b not in by_year:
        return "unknown"
    a = mean(by_year[year_a])
    b = mean(by_year[year_b])
    if abs(b - a) < 0.000001:
        return "stable"
    return "up" if b > a else "down"


def run_backtest(fixture_path: str | Path, holdout_year: int | None = None) -> dict[str, object]:
    snapshot = create_snapshot_from_fixture(fixture_path)
    observations = list(snapshot.get("observations", []))
    years = sorted({int(row["year"]) for row in observations})
    if len(years) < 3:
        return {"status": "insufficient_history", "holdout_year": holdout_year}
    holdout = holdout_year if holdout_year is not None else years[-1]
    train_rows = [row for row in observations if int(row["year"]) < holdout]
    train_years = sorted({int(row["year"]) for row in train_rows})
    if len(train_years) < 2:
        return {"status": "insufficient_training_history", "holdout_year": holdout}
    training_snapshot = dict(snapshot)
    training_snapshot["observations"] = train_rows
    training_snapshot["content_sha256"] = snapshot["content_sha256"] + f":train_until_{holdout - 1}"
    model = build_epoch_model(training_snapshot)
    expected = _aggregate_direction(train_rows, train_years[-2], train_years[-1])
    actual = _aggregate_direction(observations, train_years[-1], holdout)
    return {
        "status": "evaluated",
        "holdout_year": holdout,
        "training_until_year": train_years[-1],
        "expected_aggregate_direction": expected,
        "actual_holdout_direction": actual,
        "direction_match": expected == actual if "unknown" not in (expected, actual) else None,
        "model_epoch_label": model["epoch_label"],
        "classification": "INFERENCIA",
        "notes": [
            "Backtest is a reproducibility check, not a proof of forecast validity.",
            "Fixture data is synthetic until replaced with licensed source snapshots.",
        ],
    }


def build_scenario_report(snapshot: dict[str, Any], backtest: dict[str, object] | None = None) -> dict[str, Any]:
    model = build_epoch_model(snapshot)
    evidence = [
        {"type": "snapshot_hash", "sha256": snapshot["content_sha256"]},
        {"type": "fixture_hash", "sha256": snapshot["fixture_sha256"]},
    ]
    claims = [
        claim(
            "CERTEZA",
            "The scenario report is tied to a stable source snapshot hash.",
            evidence,
        ),
        claim(
            "INFERENCIA",
            f"The current epoch model label is {model['epoch_label']}.",
            evidence + [{"type": "model_schema", "schema": model["schema"]}],
        ),
    ]
    if snapshot["source"]["role"] == "media_narrative_signal_only":
        claims.append(
            claim(
                "INFERENCIA",
                "This source is limited to media narrative signal and is not raw social fact.",
                evidence,
            )
        )
    uncertainties = [
        {
            "classification": "INCOGNITA",
            "item": "Live dataset licensing and provider-specific attribution remain unverified in offline mode.",
        },
        {
            "classification": "INCOGNITA",
            "item": "DUAT and Conway thresholds are demo parameters until calibrated with historical datasets.",
        },
    ]
    if snapshot["source"]["requires_api_key"]:
        uncertainties.append(
            {
                "classification": "INCOGNITA",
                "item": "Live API key handling must be approved before any FRED run.",
            }
        )
    return {
        "schema": SCENARIO_REPORT_SCHEMA,
        "snapshot": {
            "source_id": snapshot["source"]["source_id"],
            "source_url": snapshot["source"]["source_url"],
            "captured_at_utc": snapshot["captured_at_utc"],
            "content_sha256": snapshot["content_sha256"],
            "classification": snapshot["classification"],
        },
        "epoch_model": model,
        "claims": claims,
        "uncertainties": uncertainties,
        "backtest": backtest,
        "publication_gate": {
            "status": "BLOCK",
            "reason": "local private MVP; no external publication without ActionGate, license review and real backtests",
        },
    }
