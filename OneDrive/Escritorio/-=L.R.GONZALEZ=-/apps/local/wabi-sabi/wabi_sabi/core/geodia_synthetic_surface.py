from __future__ import annotations

from typing import Any, Callable

from wabi_sabi.core.geodia_math_core import GeodiaCell, compute_eml, compute_psi, update_cell


GEODIA_SYNTHETIC_SURFACE_SCHEMA = "wabi.geodia_synthetic_surface.v1"


def build_geodia_synthetic_surface() -> dict[str, Any]:
    """Expose geodia_math_core through a deterministic local-only contract."""
    cells = _sample_cells()
    before = compute_psi(cells)
    random = _cycle_random([0.17, 0.43, 0.61, 0.29, 0.73, 0.11])
    updated_cells = [update_cell(cell, random) for cell in cells]
    after = compute_psi(updated_cells, ticks=1, prev_fatigue=before.fatigue)
    eml = compute_eml(
        load=after.R,
        saturation=1.0,
        noise=after.epsilon,
        intrinsic_clarity=1.8,
        scale=5.0,
    )
    metrics = {
        "before": before.to_dict(),
        "after": after.to_dict(),
        "eml": eml,
    }
    return {
        "schema": GEODIA_SYNTHETIC_SURFACE_SCHEMA,
        "ok": True,
        "status": "SYNTHETIC_ONLY",
        "action_gate": "APPROVE_LOCAL_SYNTHETIC",
        "claim_gate": "NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC_VALIDATION",
        "source": {
            "module": "wabi_sabi.core.geodia_math_core",
            "input_mode": "deterministic_fixture",
            "external_io": False,
            "runtime_writes": False,
        },
        "surface_contract": {
            "input": "none; deterministic fixture generated in-process",
            "output": "json-serializable PSI, EML and sample cell update payload",
            "owner": "Wabi/Sabi local runtime",
            "validation": [
                "bounded numeric outputs",
                "deterministic sample update",
                "synthetic-only epistemic posture",
            ],
        },
        "cells": {
            "count": len(cells),
            "before": [cell.to_dict() for cell in cells],
            "after": [cell.to_dict() for cell in updated_cells],
        },
        "metrics": metrics,
        "bounded": _metrics_are_bounded(metrics),
        "certainty": [
            "geodia_math_core can produce deterministic bounded metrics from typed local fixtures.",
            "This surface performs no network, browser, file import or external publication action.",
        ],
        "inference": [
            "The contract is suitable as a local smoke surface for agents that need DUAT/GEODIA metrics.",
        ],
        "unknown": [
            "No real-world physical, economic or city-simulation validity is claimed.",
            "Numeric validation against a dedicated dataset remains pending.",
        ],
        "not_claimed": [
            "This is not a scientific proof.",
            "This is not a production DUAT/GEODIA boot report.",
            "This is not imported Replit runtime code.",
        ],
        "next_gate": {
            "allowed": [
                "add synthetic falsifier tests",
                "connect to local dashboard only as RESEARCH_ONLY",
                "compare variant groups before any canon merge",
            ],
            "review_required": [
                "real dataset calibration",
                "public claims",
                "imports from archive quarantine",
            ],
        },
    }


def _sample_cells() -> list[GeodiaCell]:
    return [
        GeodiaCell(
            x=0,
            y=0,
            resources=0.62,
            knowledge=0.44,
            memory=0.38,
            conflict=0.18,
            signal_noise=0.22,
            stability=0.76,
            agent_density=0.48,
        ),
        GeodiaCell(
            x=1,
            y=0,
            resources=0.49,
            knowledge=0.57,
            memory=0.42,
            conflict=0.28,
            signal_noise=0.34,
            stability=0.66,
            agent_density=0.53,
        ),
        GeodiaCell(
            x=0,
            y=1,
            resources=0.71,
            knowledge=0.36,
            memory=0.51,
            conflict=0.12,
            signal_noise=0.19,
            stability=0.81,
            agent_density=0.44,
        ),
    ]


def _cycle_random(values: list[float]) -> Callable[[], float]:
    if not values:
        raise ValueError("values_must_not_be_empty")
    index = 0

    def random() -> float:
        nonlocal index
        value = values[index % len(values)]
        index += 1
        return value

    return random


def _metrics_are_bounded(metrics: dict[str, Any]) -> bool:
    for key in ["before", "after"]:
        metric = metrics[key]
        for name in ["R", "phi_eff", "j_c", "epsilon", "fatigue", "I_obs"]:
            if not 0 <= float(metric[name]) <= 1:
                return False
        for value in metric["sigma"]:
            if not 0 <= float(value) <= 1:
                return False
    return 0 <= float(metrics["eml"]) <= 10
