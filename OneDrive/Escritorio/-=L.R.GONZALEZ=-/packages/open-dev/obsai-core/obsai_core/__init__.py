"""Dependency-free Observacionismo/PSI-IA operational core."""

from .fingerprint import SessionFingerprint, stable_fingerprint
from .gate import DEFAULT_GATE_CONFIG, evaluate_action
from .metrics import Regime, estimate_regime, estimate_residue_from_signals, phi_eff_power
from .residue import ResidueItem, ResidueTracker
from .world import simulate_world

__all__ = [
    "DEFAULT_GATE_CONFIG",
    "Regime",
    "ResidueItem",
    "ResidueTracker",
    "SessionFingerprint",
    "estimate_regime",
    "estimate_residue_from_signals",
    "evaluate_action",
    "phi_eff_power",
    "simulate_world",
    "stable_fingerprint",
]
