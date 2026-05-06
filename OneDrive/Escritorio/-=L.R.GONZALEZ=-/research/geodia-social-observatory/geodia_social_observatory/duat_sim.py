"""Deterministic DUAT + Conway-style simulation for lab fixtures."""

from __future__ import annotations

import random
from typing import Any

from .contracts import DUAT_CONWAY_SIMULATION_SCHEMA
from .snapshot import canonical_sha256


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _idx(row: int, col: int, size: int) -> int:
    return row * size + col


def _phase(value: float, low: float, high: float) -> str:
    if value < low:
        return "ordered"
    if value <= high:
        return "griffiths"
    return "disordered"


def run_duat_conway_simulation(
    *,
    seed: int = 42,
    size: int = 24,
    steps: int = 20,
    chi: float = 0.567,
    sigma: float = 0.12,
) -> dict[str, Any]:
    rng = random.Random(seed)
    low = chi * 0.65
    high = chi * 1.55
    cells = [_clamp(rng.gauss(chi, sigma * 2.0), 0.05, 0.95) for _ in range(size * size)]
    next_cells = list(cells)
    for _step in range(steps):
        for row in range(size):
            for col in range(size):
                current = cells[_idx(row, col, size)]
                griffiths_neighbors = 0
                disordered_neighbors = 0
                ordered_neighbors = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        neighbor = cells[_idx((row + dr) % size, (col + dc) % size, size)]
                        phase = _phase(neighbor, low, high)
                        if phase == "griffiths":
                            griffiths_neighbors += 1
                        elif phase == "ordered":
                            ordered_neighbors += 1
                        else:
                            disordered_neighbors += 1
                coupling = griffiths_neighbors / 8.0
                noise = rng.gauss(0.0, 0.008)
                if coupling > 0.1:
                    target = chi + rng.gauss(0.0, sigma * 0.3)
                    new_value = current + 0.15 * (target - current) * coupling + noise
                elif ordered_neighbors > disordered_neighbors:
                    new_value = current - 0.05 * (current - 0.1) + noise
                elif disordered_neighbors > ordered_neighbors:
                    new_value = current + 0.05 * (0.9 - current) + noise
                else:
                    new_value = current + noise
                next_cells[_idx(row, col, size)] = _clamp(new_value, 0.05, 0.95)
        cells, next_cells = next_cells, cells

    counts = {"ordered": 0, "griffiths": 0, "disordered": 0}
    for value in cells:
        counts[_phase(value, low, high)] += 1
    total = float(size * size)
    percentages = {key: round(value / total, 6) for key, value in counts.items()}
    rounded_cells = [round(value, 4) for value in cells]
    state_hash = canonical_sha256(
        {
            "seed": seed,
            "size": size,
            "steps": steps,
            "chi": chi,
            "sigma": sigma,
            "cells": rounded_cells,
        }
    )
    return {
        "schema": DUAT_CONWAY_SIMULATION_SCHEMA,
        "seed": seed,
        "size": size,
        "steps": steps,
        "chi": chi,
        "sigma": sigma,
        "phase_thresholds": {"griffiths_low": round(low, 6), "griffiths_high": round(high, 6)},
        "phase_percentages": percentages,
        "dominant_phase": max(percentages.items(), key=lambda item: item[1])[0],
        "state_sha256": state_hash,
        "claim_boundary": "deterministic lab simulation; not a social prediction",
    }
