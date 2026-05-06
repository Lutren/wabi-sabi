from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass, field
from statistics import mean, pvariance
from typing import Any


SCHEMA_RUN = "duat.genesis.simulation_run.v1"
SCHEMA_REPORT = "duat.genesis.report.v1"
SCHEMA_FALSIFIER = "duat.genesis.falsifier_result.v1"


@dataclass(frozen=True)
class Observation:
    observer_id: str
    target_index: int
    signal: float
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def bounded(self, size: int) -> "Observation":
        target = max(0, min(size - 1, int(self.target_index)))
        return Observation(
            observer_id=self.observer_id,
            target_index=target,
            signal=max(-1.0, min(1.0, float(self.signal))),
            confidence=max(0.0, min(1.0, float(self.confidence))),
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class Observer:
    observer_id: str
    sensitivity: float = 0.5


@dataclass(frozen=True)
class GenesisRule:
    rule_id: str
    description: str
    pressure: float = 0.1
    diffusion: float = 0.12


@dataclass(frozen=True)
class GenesisState:
    tick: int
    values: tuple[float, ...]
    residue: float
    phi_eff: float


@dataclass(frozen=True)
class FalsifierResult:
    schemaVersion: str
    name: str
    passed: bool
    reason: str
    evidence: dict[str, Any]


@dataclass(frozen=True)
class SimulationRun:
    schemaVersion: str
    seed: str
    size: int
    ticks: int
    rules: tuple[GenesisRule, ...]
    observations: tuple[Observation, ...]
    states: tuple[GenesisState, ...]
    fingerprint: str
    claims: dict[str, str]


def _stable_unit(seed: str, index: int) -> float:
    digest = hashlib.sha256(f"{seed}:{index}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF


def _fingerprint(payload: Any) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _initial_state(seed: str, size: int) -> GenesisState:
    values = tuple(round((_stable_unit(seed, i) * 2.0) - 1.0, 6) for i in range(size))
    return GenesisState(tick=0, values=values, residue=0.0, phi_eff=1.0)


def _step(
    state: GenesisState,
    rule: GenesisRule,
    observations: tuple[Observation, ...],
    rng: random.Random,
) -> GenesisState:
    size = len(state.values)
    next_values: list[float] = []
    obs_by_index: dict[int, float] = {}
    for obs in observations:
        bounded = obs.bounded(size)
        obs_by_index[bounded.target_index] = obs_by_index.get(bounded.target_index, 0.0) + (
            bounded.signal * bounded.confidence
        )

    for i, value in enumerate(state.values):
        left = state.values[(i - 1) % size]
        right = state.values[(i + 1) % size]
        neighborhood = (left + value + right) / 3.0
        observation_pressure = obs_by_index.get(i, 0.0) * 0.18
        jitter = (rng.random() - 0.5) * 0.015
        updated = (
            value * (1.0 - rule.diffusion)
            + neighborhood * rule.diffusion
            + rule.pressure * math.tanh(neighborhood)
            + observation_pressure
            + jitter
        )
        next_values.append(round(max(-1.0, min(1.0, updated)), 6))

    drift = sum(abs(a - b) for a, b in zip(state.values, next_values)) / max(1, size)
    residue = round(max(0.0, min(1.0, (state.residue * 0.72) + drift)), 6)
    phi_eff = round(max(0.0, min(1.0, 1.0 - residue)), 6)
    return GenesisState(tick=state.tick + 1, values=tuple(next_values), residue=residue, phi_eff=phi_eff)


def run_simulation(
    *,
    seed: str = "demo",
    size: int = 8,
    ticks: int = 5,
    rules: tuple[GenesisRule, ...] | None = None,
    observations: tuple[Observation, ...] | None = None,
) -> SimulationRun:
    if size < 2:
        raise ValueError("size must be >= 2")
    if ticks < 0:
        raise ValueError("ticks must be >= 0")

    active_rules = rules or (
        GenesisRule(
            rule_id="synthetic_diffusion",
            description="Bounded neighbor diffusion with observation pressure.",
        ),
    )
    active_observations = observations or (
        Observation(observer_id="demo_observer", target_index=size // 2, signal=0.35, confidence=0.8),
    )
    rng = random.Random(_fingerprint({"seed": seed, "size": size, "ticks": ticks})[:16])
    states = [_initial_state(seed, size)]
    for tick in range(ticks):
        rule = active_rules[tick % len(active_rules)]
        states.append(_step(states[-1], rule, active_observations, rng))

    payload = {
        "seed": seed,
        "size": size,
        "ticks": ticks,
        "rules": [asdict(rule) for rule in active_rules],
        "observations": [asdict(obs) for obs in active_observations],
        "states": [asdict(state) for state in states],
    }
    return SimulationRun(
        schemaVersion=SCHEMA_RUN,
        seed=seed,
        size=size,
        ticks=ticks,
        rules=tuple(active_rules),
        observations=tuple(active_observations),
        states=tuple(states),
        fingerprint=_fingerprint(payload),
        claims={
            "calibration": "DEMO_ONLY",
            "data": "SYNTHETIC_ONLY",
            "private_engineering": "EXCLUDED",
            "prediction": "NOT_CLAIMED",
        },
    )


def report_run(run: SimulationRun) -> dict[str, Any]:
    final = run.states[-1]
    values = list(final.values)
    return {
        "schemaVersion": SCHEMA_REPORT,
        "runFingerprint": run.fingerprint,
        "ticks": run.ticks,
        "size": run.size,
        "final": {
            "mean": round(mean(values), 6),
            "variance": round(pvariance(values), 6),
            "residue": final.residue,
            "phi_eff": final.phi_eff,
        },
        "claims": dict(run.claims),
    }


def falsify_run(run: SimulationRun) -> tuple[FalsifierResult, ...]:
    values = [value for state in run.states for value in state.values]
    bounded = all(-1.0 <= value <= 1.0 for value in values)
    ticks_match = len(run.states) == run.ticks + 1
    no_private_claim = run.claims.get("private_engineering") == "EXCLUDED"
    return (
        FalsifierResult(
            schemaVersion=SCHEMA_FALSIFIER,
            name="bounded_state",
            passed=bounded,
            reason="all state values must stay inside [-1, 1]",
            evidence={"min": min(values), "max": max(values)},
        ),
        FalsifierResult(
            schemaVersion=SCHEMA_FALSIFIER,
            name="tick_count",
            passed=ticks_match,
            reason="simulation stores initial state plus one state per tick",
            evidence={"states": len(run.states), "ticks": run.ticks},
        ),
        FalsifierResult(
            schemaVersion=SCHEMA_FALSIFIER,
            name="private_boundary",
            passed=no_private_claim,
            reason="public Genesis package must exclude private Geodia/RPG engineering",
            evidence={"private_engineering": run.claims.get("private_engineering")},
        ),
    )


def to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    if isinstance(value, tuple):
        return [to_jsonable(item) for item in value]
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    return value
