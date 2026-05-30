"""Adapter that lets DUAT Genesis consume the canonical obsai-core OSIT ladder.

obsai-core (``packages/open-dev/obsai-core``) is the single source of truth for the
regime ladder and residue. See its
``docs/OSIT_CANON_REUSE_CONTRACT_2026-05-29.md``.

Genesis used to be residue-aware but epistemic-state-blind. This module classifies
synthetic observations into OSIT epistemic states so a simulation can refuse to run
on a BLOQUEADO input instead of silently proceeding. Calibration is DEMO_ONLY.
"""

from __future__ import annotations

from typing import Any, Iterable

try:  # Canonical regime ladder + epistemic state from obsai-core (single source of truth).
    from obsai_core import estimate_epistemic_state as _obsai_estimate_epistemic_state
    from obsai_core import estimate_regime as _obsai_estimate_regime
except Exception:  # pragma: no cover - dependency-light fallback.
    _obsai_estimate_epistemic_state = None
    _obsai_estimate_regime = None

# Mirrors obsai_core.metrics.estimate_regime (strict '<' boundaries).
_REGIME_BANDS = (
    (0.15, "OPTIMO"),
    (0.30, "FUNCIONAL"),
    (0.45, "PRE_JAMMING"),
    (0.60, "JAMMING_TEMPRANO"),
)
# Hard-boundary policy tags that force BLOQUEADO regardless of residue.
HARD_BOUNDARY_TAGS = {
    "secret",
    "touches_secret",
    "destructive",
    "external_write",
    "private",
    "publication_without_gate",
}
OBSERVATION_GATE_SCHEMA = "duat.genesis.observation_gate.v1"


def _clamp01(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(1.0, number))


def regime_for_residue(residue: Any) -> str:
    """Canonical OSIT regime label for a residue R in [0,1]."""
    if _obsai_estimate_regime is not None:
        return str(_obsai_estimate_regime(residue).value)
    r = _clamp01(residue)
    for threshold, label in _REGIME_BANDS:
        if r < threshold:
            return label
    return "JAMMING"


def epistemic_state_for_residue(residue: Any) -> str:
    """Canonical R -> epistemic-state bridge (OSIT_CANON_REUSE_CONTRACT §2.4).

    R<0.15 CERTEZA | 0.15..0.45 INFERENCIA | 0.45..0.60 INCOGNITA | >=0.60 BLOQUEADO.
    Sourced from obsai_core.estimate_epistemic_state (canonical); local fallback if absent.
    """
    if _obsai_estimate_epistemic_state is not None:
        return str(_obsai_estimate_epistemic_state(residue).value)
    r = _clamp01(residue)
    if r < 0.15:
        return "CERTEZA"
    if r < 0.45:
        return "INFERENCIA"
    if r < 0.60:
        return "INCOGNITA"
    return "BLOQUEADO"


def observation_residue(observation: Any) -> float:
    """Residue proxy for an observation: explicit ``metadata['residue']`` else ``1 - confidence``."""
    metadata = getattr(observation, "metadata", None) or {}
    if isinstance(metadata, dict) and "residue" in metadata:
        return _clamp01(metadata["residue"])
    confidence = getattr(observation, "confidence", 1.0)
    return _clamp01(1.0 - _clamp01(confidence))


def classify_observation(observation: Any) -> str:
    """Epistemic state of an observation, honoring explicit metadata and hard-boundary tags."""
    metadata = getattr(observation, "metadata", None) or {}
    if isinstance(metadata, dict):
        explicit = str(metadata.get("epistemic_state") or "").upper()
        if explicit == "BLOQUEO":
            return "BLOQUEADO"
        if explicit in {"CERTEZA", "INFERENCIA", "INCOGNITA", "BLOQUEADO"}:
            return explicit
        tags = {str(tag).lower() for tag in (metadata.get("policy_tags") or [])}
        if tags & HARD_BOUNDARY_TAGS:
            return "BLOQUEADO"
    return epistemic_state_for_residue(observation_residue(observation))


def gate_observations(observations: Iterable[Any]) -> dict[str, Any]:
    """Gate a batch of observations. Any BLOQUEADO observation blocks the batch."""
    states = [classify_observation(obs) for obs in observations]
    blocking = [index for index, state in enumerate(states) if state == "BLOQUEADO"]
    return {
        "schema": OBSERVATION_GATE_SCHEMA,
        "states": states,
        "blocked": bool(blocking),
        "blocking_indices": blocking,
        "gate": "BLOCK" if blocking else "APPROVE",
        "source": "obsai_core" if _obsai_estimate_regime is not None else "local_fallback",
        "calibration": "DEMO_ONLY",
    }
