from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

from wabi_sabi.core.bridge import WitnessLog
from wabi_sabi.core.tools import write_artifact


DECISION_RECORD_SCHEMA = "wabi.decision_record.v0_2"
TASK_MANAGER_SCHEMA = "obsai.task_manager.v1"


class DecisionLogAdapter:
    """Append-only decision ledger plus TaskManager-compatible current state."""

    def __init__(self, *, runtime_root: str | Path) -> None:
        self.runtime_root = Path(runtime_root).resolve()
        self.decision_dir = self.runtime_root / "decision_log"
        self.decision_dir.mkdir(parents=True, exist_ok=True)
        self.ledger_path = self.decision_dir / "wabi_decisions.jsonl"
        self.task_manager_path = self.decision_dir / "wabi_task_manager.json"
        self.witness = WitnessLog(self.decision_dir / "wabi_decision_witness.sqlite")

    def record(
        self,
        *,
        prompt: str,
        snapshot: dict[str, Any],
        evidence_refs: list[str] | None = None,
    ) -> dict[str, Any]:
        snapshot_hash = _hash_payload(snapshot)
        decision = snapshot.get("decision", {}) if isinstance(snapshot.get("decision"), dict) else {}
        host = snapshot.get("host", {}) if isinstance(snapshot.get("host"), dict) else {}
        pending = snapshot.get("pending", {}) if isinstance(snapshot.get("pending"), dict) else {}
        comms = snapshot.get("comms", {}) if isinstance(snapshot.get("comms"), dict) else {}
        record_base = {
            "schema": DECISION_RECORD_SCHEMA,
            "generated_at_utc": _utc_now(),
            "prompt": prompt.strip() or "estado local",
            "environment_snapshot_hash": snapshot_hash,
            "recommended_mode": decision.get("recommended_mode", "UNKNOWN"),
            "host_gate": host.get("gate", "UNKNOWN"),
            "host_status": host.get("status", "UNKNOWN"),
            "pending_active_dedup": pending.get("active_dedup"),
            "comms_agent_count": comms.get("agent_count"),
            "comms_validator_ok": comms.get("validator", {}).get("ok") if isinstance(comms.get("validator"), dict) else None,
            "reasons": decision.get("reasons", []),
            "allowed_actions": decision.get("allowed_actions", []),
            "blocked_actions": decision.get("blocked_actions", []),
            "evidence_refs": list(evidence_refs or []),
            "next_actions": _next_actions(decision),
            "status": _task_status(decision),
            "priority": _task_priority(decision),
        }
        record_hash = _hash_payload(record_base)
        task = _task_record(record_base, record_hash)
        record = {
            **record_base,
            "record_hash": record_hash,
            "task_record": task,
            "task_manager_path": str(self.task_manager_path),
            "ledger_path": str(self.ledger_path),
            "witness_db": str(self.witness.db_path),
        }
        event_id = self.witness.append(
            "wabi_decision_record",
            {
                "record_hash": record_hash,
                "environment_snapshot_hash": snapshot_hash,
                "task_id": task["id"],
                "status": record_base["status"],
                "recommended_mode": record_base["recommended_mode"],
                "host_gate": record_base["host_gate"],
                "blocked_actions": record_base["blocked_actions"],
            },
        )
        witness_ok, witness_reason = self.witness.verify_chain()
        record["witness_event_id"] = event_id
        record["witness_verified"] = witness_ok
        record["witness_verify_reason"] = witness_reason
        self._append_record(record)
        self._upsert_task(task)
        return record

    def tail(self, limit: int = 10) -> list[dict[str, Any]]:
        if not self.ledger_path.exists():
            return []
        lines = [line for line in self.ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        records: list[dict[str, Any]] = []
        for line in lines[-limit:]:
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                payload = {"schema": DECISION_RECORD_SCHEMA, "error": "invalid_jsonl_line", "raw": line[:500]}
            records.append(payload)
        return records

    def task_manager(self) -> dict[str, Any]:
        return _load_task_manager(self.task_manager_path)

    def _append_record(self, record: dict[str, Any]) -> None:
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with self.ledger_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")

    def _upsert_task(self, task: dict[str, Any]) -> None:
        manager = _load_task_manager(self.task_manager_path)
        tasks = [item for item in manager.get("tasks", []) if item.get("id") != task["id"]]
        tasks.append(task)
        manager["tasks"] = sorted(tasks, key=lambda item: (item.get("status", ""), item.get("priority", ""), item.get("createdAt", "")))
        self.task_manager_path.write_text(json.dumps(manager, indent=2, sort_keys=True, ensure_ascii=False), encoding="utf-8")


def write_decision_record(output_dir: Path, record: dict[str, Any]) -> Path:
    text = json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False)
    return write_artifact(output_dir, "wabi_decision_record", ".json", text)


def _task_record(record: dict[str, Any], record_hash: str) -> dict[str, Any]:
    now = record["generated_at_utc"]
    task_id = f"wabi-decision-{record_hash[:16]}"
    return {
        "id": task_id,
        "title": f"Decision: {record['prompt'][:120]}",
        "priority": record["priority"],
        "status": record["status"],
        "evidence": [
            {
                "label": "environment_snapshot_hash",
                "source": record["environment_snapshot_hash"],
                "verified": True,
                "note": "Snapshot hash captured before decision recording.",
            },
            {
                "label": "decision_record_hash",
                "source": record_hash,
                "verified": True,
                "note": "Decision record hash captured before WitnessLog append.",
            },
        ],
        "createdAt": now,
        "updatedAt": now,
        "closedAt": None,
        "note": "; ".join(record.get("reasons", [])[:6]),
        "metadata": {
            "schema": DECISION_RECORD_SCHEMA,
            "recommended_mode": record["recommended_mode"],
            "host_gate": record["host_gate"],
            "host_status": record["host_status"],
            "blocked_actions": record["blocked_actions"],
            "allowed_actions": record["allowed_actions"],
            "next_actions": record["next_actions"],
        },
    }


def _load_task_manager(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schemaVersion": TASK_MANAGER_SCHEMA, "tasks": []}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"schemaVersion": TASK_MANAGER_SCHEMA, "tasks": []}
    if not isinstance(payload, dict):
        return {"schemaVersion": TASK_MANAGER_SCHEMA, "tasks": []}
    payload.setdefault("schemaVersion", TASK_MANAGER_SCHEMA)
    payload.setdefault("tasks", [])
    if not isinstance(payload["tasks"], list):
        payload["tasks"] = []
    return payload


def _next_actions(decision: dict[str, Any]) -> list[str]:
    mode = str(decision.get("recommended_mode") or "")
    blocked = set(decision.get("blocked_actions", []))
    if mode == "A0_LOCAL_REVIEW_ONLY":
        return [
            "keep_external_actions_blocked",
            "record_local_evidence_only",
            "wait_for_host_gate_before_append_comms_or_broad_programming",
        ]
    actions = ["record_decision_evidence"]
    if "external_publish" in blocked:
        actions.append("keep_publication_blocked")
    actions.append("prepare_scoped_workpack")
    return actions


def _task_status(decision: dict[str, Any]) -> str:
    mode = str(decision.get("recommended_mode") or "")
    if mode == "A0_LOCAL_REVIEW_ONLY":
        return "BLOCKED"
    return "OPEN"


def _task_priority(decision: dict[str, Any]) -> str:
    mode = str(decision.get("recommended_mode") or "")
    if mode == "A0_LOCAL_REVIEW_ONLY":
        return "P1"
    return "P2"


def _hash_payload(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()


def _utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
