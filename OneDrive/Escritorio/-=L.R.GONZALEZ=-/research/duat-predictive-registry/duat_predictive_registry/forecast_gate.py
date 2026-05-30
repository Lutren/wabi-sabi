"""ForecastGate rules for DUAT predictive registry."""

from __future__ import annotations

from dataclasses import dataclass

try:  # Canonical regime ladder + epistemic state from obsai-core (single source of truth).
    from obsai_core import estimate_epistemic_state as _obsai_estimate_epistemic_state
    from obsai_core import estimate_regime as _obsai_estimate_regime
except Exception:  # pragma: no cover - dependency-light fallback.
    _obsai_estimate_epistemic_state = None
    _obsai_estimate_regime = None


def _regime_for_r(r_pred: float) -> str:
    """Canonical OSIT regime for R_pred (mirrors obsai_core.metrics.estimate_regime)."""
    if _obsai_estimate_regime is not None:
        return str(_obsai_estimate_regime(r_pred).value)
    r = max(0.0, min(1.0, float(r_pred)))
    if r < 0.15:
        return "OPTIMO"
    if r < 0.30:
        return "FUNCIONAL"
    if r < 0.45:
        return "PRE_JAMMING"
    if r < 0.60:
        return "JAMMING_TEMPRANO"
    return "JAMMING"


def _epistemic_state_for_r(r_pred: float) -> str:
    """Canonical R -> epistemic-state (obsai_core.estimate_epistemic_state; local fallback)."""
    if _obsai_estimate_epistemic_state is not None:
        return str(_obsai_estimate_epistemic_state(r_pred).value)
    r = max(0.0, min(1.0, float(r_pred)))
    if r < 0.15:
        return "CERTEZA"
    if r < 0.45:
        return "INFERENCIA"
    if r < 0.60:
        return "INCOGNITA"
    return "BLOQUEADO"


@dataclass(frozen=True)
class ForecastGateInput:
    has_source_card: bool
    has_backtest: bool
    data_leakage_detected: bool = False
    unsupported_causality_claim: bool = False
    forbidden_domain_claim: bool = False
    brier_score: float | None = None
    baseline_brier: float | None = None
    R_pred: float = 1.0


def _forecast_gate_core(item: ForecastGateInput) -> dict[str, str]:
    if not item.has_source_card:
        return {"gate": "REVIEW", "reason": "missing_source_card"}
    if not item.has_backtest:
        return {"gate": "REVIEW", "reason": "missing_backtest"}
    if item.data_leakage_detected:
        return {"gate": "BLOCK", "reason": "data_leakage_detected"}
    if item.unsupported_causality_claim:
        return {"gate": "BLOCK", "reason": "unsupported_causality_claim"}
    if item.forbidden_domain_claim:
        return {"gate": "BLOCK", "reason": "forbidden_domain_claim"}
    if (
        item.brier_score is not None
        and item.baseline_brier is not None
        and item.brier_score > item.baseline_brier
    ):
        return {"gate": "BLOCK_PRODUCTION", "reason": "worse_than_baseline_brier"}
    if item.R_pred >= 0.60:
        return {"gate": "BLOCK", "reason": "r_pred_high"}
    if item.R_pred >= 0.35:
        return {"gate": "REVIEW", "reason": "r_pred_review"}
    return {"gate": "APPROVE", "reason": "forecast_gate_passed"}


def forecast_gate(gate_input: ForecastGateInput | dict[str, object]) -> dict[str, str]:
    if isinstance(gate_input, ForecastGateInput):
        item = gate_input
    else:
        item = ForecastGateInput(**gate_input)

    result = _forecast_gate_core(item)
    # Annotate with the canonical OSIT regime/state (obsai-core). The gate DECISION is
    # unchanged; thresholds are not renumbered here (canon decision is separate).
    result.setdefault("regime", _regime_for_r(item.R_pred))
    result.setdefault("epistemic_state", _epistemic_state_for_r(item.R_pred))
    return result


def obsai_forecast_precheck(r_pred: float) -> dict[str, object]:
    """Strict canonical pre-check (NEW wiring) for before a prediction is emitted/written.

    INCOGNITA/BLOQUEADO -> BLOCK, INFERENCIA at/above the review band -> REVIEW, else APPROVE.
    This is an additional obsai-core guard; it does NOT replace or renumber forecast_gate.
    """
    regime = _regime_for_r(r_pred)
    state = _epistemic_state_for_r(r_pred)
    if state in {"INCOGNITA", "BLOQUEADO"}:
        gate = "BLOCK"
    elif state == "INFERENCIA" and float(r_pred) >= 0.35:
        gate = "REVIEW"
    else:
        gate = "APPROVE"
    return {
        "schema": "duat.predictive.obsai_forecast_precheck.v1",
        "regime": regime,
        "epistemic_state": state,
        "gate": gate,
        "R_pred": round(float(r_pred), 6),
        "calibration": "DEMO_ONLY",
        "publication_gate": "BLOCK",
    }
