from __future__ import annotations

import datetime as dt
import hashlib
import json
from dataclasses import asdict, dataclass, field


@dataclass
class ObservationEnvelope:
    envelope_version: str = "wabi-observation-v1"
    observed_at_utc: str = field(default_factory=lambda: dt.datetime.now(dt.UTC).isoformat())
    prompt: str = ""
    intent: str = "general"
    agent: str = ""
    action_gate: str = "REVIEW"
    certainty: list[str] = field(default_factory=list)
    inference: list[str] = field(default_factory=list)
    unknown: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    fingerprint: str = ""

    def finalize(self) -> "ObservationEnvelope":
        payload = json.dumps(
            {
                "prompt": self.prompt,
                "intent": self.intent,
                "agent": self.agent,
                "action_gate": self.action_gate,
                "artifacts": self.artifacts,
                "evidence": self.evidence,
            },
            sort_keys=True,
            ensure_ascii=True,
        )
        self.fingerprint = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return self

    def to_dict(self) -> dict:
        return asdict(self)
