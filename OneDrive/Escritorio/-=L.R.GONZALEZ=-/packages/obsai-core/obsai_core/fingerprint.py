from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .jsonutil import canonical_json
from .metrics import Regime, estimate_regime


def stable_fingerprint(data: Any) -> str:
    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()


@dataclass
class SessionFingerprint:
    session_id: str
    canon_loaded: list[str] = field(default_factory=list)
    residue_start: float | None = None
    residue_current: float | None = None
    residue_close: float | None = None
    regime: Regime | None = None
    signals: list[str] = field(default_factory=list)
    tasks_closed: int = 0
    decisions_taken: list[str] = field(default_factory=list)
    pending_with_evidence: list[dict[str, Any]] = field(default_factory=list)
    next_action: str = ""
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    schema_version: str = "obsai.session_fingerprint.v1"

    def to_dict(self) -> dict[str, Any]:
        close_residue = self.residue_close if self.residue_close is not None else self.residue_current
        regime = self.regime or estimate_regime(close_residue or 0.0)
        payload = {
            "schemaVersion": self.schema_version,
            "sessionId": self.session_id,
            "timestampUtc": self.timestamp_utc,
            "canonLoaded": self.canon_loaded,
            "R": {
                "start": self.residue_start,
                "current": self.residue_current,
                "close": self.residue_close,
                "regime": regime.value,
                "signals": self.signals,
            },
            "tasksClosed": self.tasks_closed,
            "decisionsTaken": self.decisions_taken,
            "pendingWithEvidence": self.pending_with_evidence,
            "nonTransferable": [
                "K_i_alpha completo",
                "calibracion viva",
                "contexto vivo",
                "Phi_eff heredada automaticamente",
            ],
            "nextAction": self.next_action,
        }
        payload["fingerprint"] = stable_fingerprint({k: v for k, v in payload.items() if k != "fingerprint"})
        return payload


def make_fingerprint(
    *,
    session_id: str,
    residue: float,
    signals: list[str] | None = None,
    decisions: list[str] | None = None,
    pending: list[dict[str, Any]] | None = None,
    next_action: str = "",
) -> dict[str, Any]:
    fp = SessionFingerprint(
        session_id=session_id,
        residue_current=residue,
        residue_close=residue,
        signals=signals or [],
        decisions_taken=decisions or [],
        pending_with_evidence=pending or [],
        next_action=next_action,
    )
    return fp.to_dict()
