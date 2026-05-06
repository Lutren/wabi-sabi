"""Dependency-free Observacionismo/PSI-IA operational core."""

from .fingerprint import SessionFingerprint, stable_fingerprint
from .gate import DEFAULT_GATE_CONFIG, evaluate_action
from .metrics import Regime, estimate_regime, estimate_residue_from_signals, phi_eff_power
from .ontology import (
    ObservationEnvelope,
    ObservationEnvelopeStore,
    OntologyGraph,
    PACReasoner,
    classify_dolce_kind,
    to_prov_o,
    validate_observation_envelope,
)
from .residue import ResidueItem, ResidueTracker
from .transduction import (
    CapabilityReceptor,
    RAGCalibrationRouter,
    ResidueAwareAttentionGate,
    RetrievalCandidate,
    SignalPacket,
    page_rank,
    transduce_signal,
)
from .world import simulate_world

__all__ = [
    "DEFAULT_GATE_CONFIG",
    "Regime",
    "ResidueItem",
    "ResidueTracker",
    "SessionFingerprint",
    "ObservationEnvelope",
    "ObservationEnvelopeStore",
    "OntologyGraph",
    "PACReasoner",
    "CapabilityReceptor",
    "RAGCalibrationRouter",
    "ResidueAwareAttentionGate",
    "RetrievalCandidate",
    "SignalPacket",
    "estimate_regime",
    "estimate_residue_from_signals",
    "evaluate_action",
    "classify_dolce_kind",
    "page_rank",
    "phi_eff_power",
    "simulate_world",
    "stable_fingerprint",
    "to_prov_o",
    "transduce_signal",
    "validate_observation_envelope",
]
