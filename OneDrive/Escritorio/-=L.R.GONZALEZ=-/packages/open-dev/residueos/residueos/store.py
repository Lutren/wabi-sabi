from __future__ import annotations

import json
import sqlite3
import uuid
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def loads(data: str | None) -> Any:
    if not data:
        return None
    return json.loads(data)


class ResidueStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.ensure_schema()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def ensure_schema(self) -> None:
        with closing(self.connect()) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS actions (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    action_json TEXT NOT NULL,
                    decision_json TEXT NOT NULL,
                    human_decision_json TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_events (
                    event_id TEXT PRIMARY KEY,
                    action_id TEXT NOT NULL,
                    at TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    FOREIGN KEY(action_id) REFERENCES actions(id)
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_events_action_id ON audit_events(action_id)")
            conn.commit()

    def insert_action(self, action: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
        record_id = str(action.get("id") or uuid.uuid4())
        now = utc_now()
        with closing(self.connect()) as conn:
            conn.execute(
                """
                INSERT INTO actions (id, created_at, updated_at, action_json, decision_json, human_decision_json)
                VALUES (?, ?, ?, ?, ?, NULL)
                """,
                (record_id, now, now, dumps(action), dumps(decision)),
            )
            self._insert_audit(
                conn,
                record_id,
                "evaluated",
                {"decisionStatus": decision["status"], "theta": decision["theta"]},
                at=now,
            )
            conn.commit()
        return self.get_action(record_id) or {}

    def update_human_decision(self, action_id: str, status: str, reviewer: str, note: str = "") -> dict[str, Any] | None:
        normalized = status.strip().upper()
        if normalized not in {"APPROVED", "BLOCKED"}:
            raise ValueError("human decision status must be APPROVED or BLOCKED")

        now = utc_now()
        human_decision = {
            "status": normalized,
            "reviewer": reviewer or "unknown",
            "note": note or "",
            "at": now,
        }
        with closing(self.connect()) as conn:
            existing = conn.execute("SELECT id FROM actions WHERE id = ?", (action_id,)).fetchone()
            if not existing:
                return None
            conn.execute(
                "UPDATE actions SET updated_at = ?, human_decision_json = ? WHERE id = ?",
                (now, dumps(human_decision), action_id),
            )
            self._insert_audit(conn, action_id, "human_decision", human_decision, at=now)
            conn.commit()
        return self.get_action(action_id)

    def get_action(self, action_id: str) -> dict[str, Any] | None:
        with closing(self.connect()) as conn:
            row = conn.execute("SELECT * FROM actions WHERE id = ?", (action_id,)).fetchone()
            if not row:
                return None
            return self._row_to_record(conn, row)

    def list_actions(self, limit: int = 100) -> list[dict[str, Any]]:
        with closing(self.connect()) as conn:
            rows = conn.execute(
                "SELECT * FROM actions ORDER BY created_at DESC LIMIT ?",
                (max(1, min(500, int(limit))),),
            ).fetchall()
            return [self._row_to_record(conn, row) for row in rows]

    def dashboard_stats(self) -> dict[str, Any]:
        records = self.list_actions(limit=500)
        by_status = {"APPROVE": 0, "REVIEW": 0, "BLOCK": 0}
        theta_total = 0.0
        residue_total = 0.0
        for record in records:
            decision = record["decision"]
            status = decision["status"]
            by_status[status] = by_status.get(status, 0) + 1
            theta_total += float(decision.get("theta") or 0)
            residue_total += float(decision.get("residue", {}).get("residueScore") or 0)
        total = len(records)
        return {
            "total": total,
            "byStatus": by_status,
            "avgTheta": theta_total / total if total else 0.0,
            "avgResidue": residue_total / total if total else 0.0,
            "latest": records[:10],
        }

    def _row_to_record(self, conn: sqlite3.Connection, row: sqlite3.Row) -> dict[str, Any]:
        audit_rows = conn.execute(
            "SELECT at, event_type, payload_json FROM audit_events WHERE action_id = ? ORDER BY at ASC",
            (row["id"],),
        ).fetchall()
        return {
            "id": row["id"],
            "createdAt": row["created_at"],
            "updatedAt": row["updated_at"],
            "action": loads(row["action_json"]),
            "decision": loads(row["decision_json"]),
            "humanDecision": loads(row["human_decision_json"]),
            "audit": [
                {
                    "at": item["at"],
                    "type": item["event_type"],
                    "payload": loads(item["payload_json"]),
                }
                for item in audit_rows
            ],
        }

    @staticmethod
    def _insert_audit(
        conn: sqlite3.Connection,
        action_id: str,
        event_type: str,
        payload: dict[str, Any],
        *,
        at: str | None = None,
    ) -> None:
        conn.execute(
            """
            INSERT INTO audit_events (event_id, action_id, at, event_type, payload_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (str(uuid.uuid4()), action_id, at or utc_now(), event_type, dumps(payload)),
        )
