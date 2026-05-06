"""Observacionismo Research Kernel: anti-informacion + informacion oscura."""
from .core import Source, EstadoPSI, Finding
from .eor import EORCalculator
from .epistemic_guard import Claim, ClaimStatus, EpistemicGuard
from .equivalence import EquivalenceCheck, EquivalenceTester, EquivalenceVerdict
from .eml import EMLDomainError, EXPERIMENTAL_OPERATOR_STATUS, eml, gap_eml, operator_contract, residue_eml
from .hypothesis import Hypothesis, HypothesisScorer
from .operator_profile import OperatorProfile, OperatorProfiler
from .orchestrator import ObservacionismoResearchKernel
from .topology import CijEdge, OperatorTopology

__all__ = [
    "Source",
    "EstadoPSI",
    "Finding",
    "ObservacionismoResearchKernel",
    "EORCalculator",
    "Claim",
    "ClaimStatus",
    "EpistemicGuard",
    "EquivalenceCheck",
    "EquivalenceTester",
    "EquivalenceVerdict",
    "eml",
    "residue_eml",
    "gap_eml",
    "operator_contract",
    "EMLDomainError",
    "EXPERIMENTAL_OPERATOR_STATUS",
    "Hypothesis",
    "HypothesisScorer",
    "OperatorProfile",
    "OperatorProfiler",
    "CijEdge",
    "OperatorTopology",
]
__version__ = "0.1.0"
