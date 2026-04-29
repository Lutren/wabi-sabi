from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass
from typing import Any

from .jsonutil import canonical_json
from .metrics import clamp01


@dataclass
class WorldState:
    tick: int
    coherence: float = 0.62
    residue: float = 0.18
    broadcast: float = 0.40
    self_reference: float = 0.35

    def step(self, rng: random.Random) -> None:
        pressure = rng.uniform(0.0, 0.09)
        repair = rng.uniform(0.0, 0.07)
        coupling = (self.broadcast + self.self_reference) / 2.0
        self.residue = clamp01(self.residue + pressure - repair * (0.5 + coupling))
        self.broadcast = clamp01(self.broadcast + rng.uniform(-0.04, 0.06) - self.residue * 0.015)
        self.self_reference = clamp01(self.self_reference + rng.uniform(-0.03, 0.05) - self.residue * 0.010)
        self.coherence = clamp01(0.45 * self.broadcast + 0.35 * self.self_reference + 0.20 * (1.0 - self.residue))
        self.tick += 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "tick": self.tick,
            "coherence": round(self.coherence, 6),
            "residue": round(self.residue, 6),
            "broadcast": round(self.broadcast, 6),
            "selfReference": round(self.self_reference, 6),
        }


def simulate_world(ticks: int = 20, seed: str = "obsai") -> dict[str, Any]:
    rng = random.Random(seed)
    state = WorldState(tick=0)
    trace = [state.to_dict()]
    for _ in range(max(0, int(ticks))):
        state.step(rng)
        trace.append(state.to_dict())
    payload = {
        "schemaVersion": "obsai.world_simulation.v1",
        "seed": seed,
        "ticks": max(0, int(ticks)),
        "final": trace[-1],
        "trace": trace,
        "claims": {
            "simulation": "DEMO_ONLY",
            "physicalModel": "NO_PRODUCT_CLAIMS",
        },
    }
    payload["fingerprint"] = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
    return payload
