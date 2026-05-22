from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


DESTRUCTIVE_WORDS = {
    "borrar",
    "borra",
    "elimina",
    "eliminar",
    "destruye",
    "destruir",
    "delete",
    "remove",
    "rm -rf",
    "format",
    "formatear",
    "wipe",
    "purge",
    "clear all",
    "limpia todo",
    "reset hard",
}

EXTERNAL_WORDS = {
    "push",
    "deploy",
    "publica",
    "publicar",
    "gumroad",
    "linkedin",
    "twitter",
    "x.com",
    "github release",
    "sube a internet",
}

SECRET_WORDS = {
    "token",
    "secret",
    "secreto",
    "credential",
    "credencial",
    ".env",
    "private key",
    "api key",
}


@dataclass(frozen=True)
class GateDecision:
    gate: str
    reasons: list[str] = field(default_factory=list)

    @property
    def allowed(self) -> bool:
        return self.gate in {"APPROVE", "REVIEW"}


class ActionGate:
    """Small local gate for actions that a deterministic CLI can judge safely."""

    def evaluate_text(self, text: str) -> GateDecision:
        lowered = text.lower()
        reasons: list[str] = []
        if any(word in lowered for word in DESTRUCTIVE_WORDS):
            reasons.append("destructive_or_delete_request")
        if any(word in lowered for word in EXTERNAL_WORDS):
            reasons.append("external_publication_or_network_action")
        if any(word in lowered for word in SECRET_WORDS):
            reasons.append("secret_or_credential_boundary")
        if reasons:
            return GateDecision("BLOCK", reasons)
        if any(word in lowered for word in ["arregla", "modifica", "edita", "repair", "fix tests"]):
            return GateDecision("REVIEW", ["local_write_or_repair_requires_scoped_artifact"])
        return GateDecision("APPROVE", ["safe_local_deterministic_action"])

    def ensure_runtime_path(self, candidate: str | Path, runtime_root: Path) -> Path:
        target = Path(candidate).resolve()
        root = runtime_root.resolve()
        if target == root or root in target.parents:
            return target
        raise ValueError(f"unsafe_path_outside_runtime: {target}")
