"""Append-only local event store and replay for the motor."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import OBSERVATION_EVENT_SCHEMA
from .snapshot import canonical_sha256


def build_event(
    event_type: str,
    actor_id: str,
    payload: dict[str, Any],
    *,
    actor_type: str = "agent",
    risk_level: str = "low",
    approval_state: str = "none",
    parent_event_id: str | None = None,
    ts: str = "1970-01-01T00:00:00Z",
) -> dict[str, Any]:
    base = {
        "schema": OBSERVATION_EVENT_SCHEMA,
        "ts": ts,
        "actor_type": actor_type,
        "actor_id": actor_id,
        "event_type": event_type,
        "payload": payload,
        "parent_event_id": parent_event_id,
        "risk_level": risk_level,
        "approval_state": approval_state,
    }
    event_hash = canonical_sha256(base)
    base["event_id"] = "evt_" + event_hash[:16]
    base["event_sha256"] = event_hash
    return base


class JsonlEventStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def append(self, event: dict[str, Any]) -> dict[str, Any]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        return event

    def read_events(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        rows = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows

    def replay_state(self) -> dict[str, Any]:
        events = self.read_events()
        route_counts: dict[str, int] = {}
        artifact_ids: list[str] = []
        approvals_required = 0
        for event in events:
            payload = event.get("payload", {})
            if event.get("approval_state") == "required":
                approvals_required += 1
            route = payload.get("route")
            if route:
                route_counts[str(route)] = route_counts.get(str(route), 0) + 1
            artifact_id = payload.get("artifact_id")
            if artifact_id:
                artifact_ids.append(str(artifact_id))
        replay_hash = canonical_sha256(
            {
                "event_ids": [event.get("event_id") for event in events],
                "route_counts": route_counts,
                "artifact_ids": artifact_ids,
                "approvals_required": approvals_required,
            }
        )
        return {
            "event_count": len(events),
            "last_event_id": events[-1]["event_id"] if events else None,
            "route_counts": route_counts,
            "artifact_ids": artifact_ids,
            "approvals_required": approvals_required,
            "replay_sha256": replay_hash,
        }
