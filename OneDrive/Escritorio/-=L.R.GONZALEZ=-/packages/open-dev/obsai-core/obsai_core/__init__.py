"""Dependency-free Observacionismo/PSI-IA operational core."""

from .claim_gate_contract import CANONICAL_CLAIM_GATES, build_claim_gate_contract
from .epistemic_engine import OSITEpistemicEngine, classify_text
from .fingerprint import SessionFingerprint, stable_fingerprint
from .gate import DEFAULT_GATE_CONFIG, evaluate_action
from .metrics import (
    EpistemicState,
    Regime,
    estimate_epistemic_state,
    estimate_regime,
    estimate_residue_from_signals,
    phi_eff_power,
)
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
from .tasks import TaskEvidence, TaskManager, TaskRecord
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
    "CANONICAL_CLAIM_GATES",
    "EpistemicState",
    "OSITEpistemicEngine",
    "Regime",
    "estimate_epistemic_state",
    "ResidueItem",
    "ResidueTracker",
    "SessionFingerprint",
    "TaskEvidence",
    "TaskManager",
    "TaskRecord",
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
    "build_claim_gate_contract",
    "classify_text",
    "classify_dolce_kind",
    "page_rank",
    "phi_eff_power",
    "simulate_world",
    "stable_fingerprint",
    "to_prov_o",
    "transduce_signal",
    "validate_observation_envelope",
]
