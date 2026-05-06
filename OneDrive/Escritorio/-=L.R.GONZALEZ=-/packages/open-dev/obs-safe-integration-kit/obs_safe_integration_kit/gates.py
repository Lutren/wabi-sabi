"""Safe ActionGate and policy logic.

Default posture: dry-run, local-only, block destructive commands, block secrets,
escalate anything with external side effects to human review.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Any, Dict, List, Optional
import json
import re
import shlex

from .core import EstadoPSI, clamp, stable_hash


class GateStatus(str, Enum):
    ALLOW = "ALLOW"
    DRY_RUN = "DRY_RUN"
    HOLD = "HOLD"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    BLOCK = "BLOCK"


@dataclass
class ActionProposal:
    tool: str
    args: Dict[str, Any] = field(default_factory=dict)
    intent: str = ""
    dry_run: bool = True
    external_effect: bool = False
    writes_files: bool = False
    network: bool = False
    shell: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def canonical(self) -> Dict[str, Any]:
        return {
            "tool": self.tool,
            "args": self.args,
            "intent": self.intent,
            "dry_run": self.dry_run,
            "external_effect": self.external_effect,
            "writes_files": self.writes_files,
            "network": self.network,
            "shell": self.shell,
            "metadata": self.metadata,
        }

    @property
    def args_hash(self) -> str:
        return stable_hash(self.canonical())


@dataclass
class GateDecision:
    status: GateStatus
    reason: str
    epsilon: float = 0.0
    risk_score: float = 0.0
    required_human: bool = False
    safe_command_preview: Optional[str] = None
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


class ActionGate:
    """Pre-execution control layer.

    It never executes actions. The caller must execute only if status is ALLOW
    and its own human/operator policy agrees.
    """

    def __init__(self, max_r: float = 0.45, max_epsilon: float = 0.55, default_dry_run: bool = True):
        self.max_r = max_r
        self.max_epsilon = max_epsilon
        self.default_dry_run = default_dry_run

    def evaluate(self, proposal: ActionProposal, psi: EstadoPSI) -> GateDecision:
        text = json.dumps(proposal.canonical(), ensure_ascii=False, sort_keys=True)
        risk_score, warnings = self._risk_scan(proposal, text)
        epsilon = semantic_epsilon(proposal.intent, f"{proposal.tool} {text}") if proposal.intent else 0.0
        psi.update_epsilon(epsilon)

        if contains_secret(text):
            return GateDecision(
                status=GateStatus.BLOCK,
                reason="Se detectó posible secreto/token/credencial en argumentos. Bloqueado.",
                epsilon=epsilon,
                risk_score=1.0,
                warnings=warnings + ["possible_secret"],
            )

        if any(w in warnings for w in ["destructive_shell", "credential_access", "network_exec", "sql_danger"]):
            return GateDecision(
                status=GateStatus.BLOCK,
                reason="Patrón crítico detectado antes de ejecutar.",
                epsilon=epsilon,
                risk_score=max(risk_score, 0.80),
                warnings=warnings,
            )

        if psi.R >= psi.J_c:
            return GateDecision(
                status=GateStatus.BLOCK,
                reason="PSI en JAMMING: R alcanzó o superó J_c. Compacta antes de actuar.",
                epsilon=epsilon,
                risk_score=risk_score,
                warnings=warnings,
            )

        if psi.R > self.max_r:
            return GateDecision(
                status=GateStatus.HOLD,
                reason="R alto. No ejecutar; hacer P1/compresión o reducir tarea.",
                epsilon=epsilon,
                risk_score=risk_score,
                warnings=warnings,
            )

        if epsilon > self.max_epsilon:
            return GateDecision(
                status=GateStatus.HUMAN_REVIEW,
                reason="Divergencia alta entre intención y acción propuesta.",
                epsilon=epsilon,
                risk_score=risk_score,
                required_human=True,
                warnings=warnings,
            )

        if risk_score >= 0.80:
            return GateDecision(
                status=GateStatus.BLOCK,
                reason="Riesgo crítico por patrón peligroso.",
                epsilon=epsilon,
                risk_score=risk_score,
                warnings=warnings,
            )

        if risk_score >= 0.45 or proposal.external_effect:
            return GateDecision(
                status=GateStatus.HUMAN_REVIEW,
                reason="Acción con efecto externo o riesgo medio/alto. Requiere aprobación humana.",
                epsilon=epsilon,
                risk_score=risk_score,
                required_human=True,
                warnings=warnings,
            )

        if proposal.dry_run or self.default_dry_run:
            return GateDecision(
                status=GateStatus.DRY_RUN,
                reason="Seguro para simulación. Dry-run por defecto; no ejecutar todavía.",
                epsilon=epsilon,
                risk_score=risk_score,
                safe_command_preview=safe_preview(proposal),
                warnings=warnings,
            )

        return GateDecision(
            status=GateStatus.ALLOW,
            reason="Permitido por política local.",
            epsilon=epsilon,
            risk_score=risk_score,
            safe_command_preview=safe_preview(proposal),
            warnings=warnings,
        )

    def _risk_scan(self, proposal: ActionProposal, text: str) -> tuple[float, List[str]]:
        warnings: List[str] = []
        risk = 0.0
        low = text.lower()

        dangerous_patterns = {
            "destructive_shell": [r"\brm\s+-rf\b", r"\bmkfs\b", r"\bdd\s+if=", r">\s*/dev/sd", r"\bshutdown\b", r"\breboot\b"],
            "credential_access": [r"\.ssh(?:/|\b)", r"\.aws(?:/|\b)", r"\.kube(?:/|\b)", r"\.env\b", r"credentials\.json", r"id_rsa", r"shadow\b", r"passwd\b"],
            "network_exec": [r"curl\s+[^|]+\|\s*(bash|sh)", r"wget\s+[^|]+\|\s*(bash|sh)", r"powershell.*iex"],
            "sql_danger": [r"drop\s+table", r"delete\s+from", r"truncate\s+table", r"union\s+select"],
            "browser_risky": [r"upload_file", r"submit", r"payment", r"purchase", r"login", r"evaluate", r"javascript"],
        }
        for name, patterns in dangerous_patterns.items():
            if any(re.search(p, low, flags=re.I) for p in patterns):
                warnings.append(name)
                risk += 0.35

        if proposal.shell:
            risk += 0.20
            warnings.append("shell_action")
        if proposal.writes_files:
            risk += 0.16
            warnings.append("writes_files")
        if proposal.network:
            risk += 0.16
            warnings.append("network")
        if proposal.external_effect:
            risk += 0.25
            warnings.append("external_effect")

        return clamp(risk, 0.0, 1.0), sorted(set(warnings))


def contains_secret(text: str) -> bool:
    patterns = [
        r"github_pat_[A-Za-z0-9_]+",
        r"ghp_[A-Za-z0-9_]{20,}",
        r"sk-[A-Za-z0-9]{20,}",
        r"AKIA[0-9A-Z]{16}",
        r"(?i)api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}",
        r"(?i)password\s*[:=]\s*['\"]?[^'\"\s]{8,}",
        r"(?i)token\s*[:=]\s*['\"]?[A-Za-z0-9_\-.]{16,}",
    ]
    return any(re.search(p, text) for p in patterns)


def semantic_epsilon(intent: str, action: str) -> float:
    """Simple lexical divergence; replace with embeddings later if needed."""
    a = set(tokenize(intent))
    b = set(tokenize(action))
    if not a or not b:
        return 0.75
    return 1.0 - len(a & b) / len(a | b)


def tokenize(text: str) -> List[str]:
    stop = {"para", "como", "este", "esta", "pero", "desde", "sobre", "entre", "cuando", "donde", "the", "and", "for", "with", "this", "that", "from"}
    return [t for t in re.findall(r"[\wáéíóúüñ]{4,}", text.lower()) if t not in stop]


def safe_preview(proposal: ActionProposal) -> str:
    if proposal.shell and "command" in proposal.args:
        try:
            return " ".join(shlex.quote(x) for x in shlex.split(str(proposal.args["command"])))
        except ValueError:
            return "<unparseable shell command>"
    return json.dumps({"tool": proposal.tool, "args": proposal.args}, ensure_ascii=False, sort_keys=True)[:500]
