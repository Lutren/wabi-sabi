"""SQLite evidence store with append-only receipts and hash chain."""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable, Optional
import hashlib
import json
import sqlite3
import time

from .core import ObservationEnvelope, EstadoPSI
from .gates import ActionProposal, GateDecision


class EvidenceStore:
    def __init__(self, path: str | Path = "obs_evidence.sqlite"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self):
        return sqlite3.connect(self.path)

    def _init(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS observations (
                    id TEXT PRIMARY KEY,
                    source TEXT,
                    url TEXT,
                    mode TEXT,
                    hash TEXT,
                    title TEXT,
                    text_preview TEXT,
                    created_at REAL,
                    source_confidence REAL,
                    calibration_epsilon REAL,
                    r_cost REAL,
                    phi_gain REAL,
                    token_estimate INTEGER,
                    json TEXT
                );
                CREATE TABLE IF NOT EXISTS claims (
                    id TEXT PRIMARY KEY,
                    observation_id TEXT,
                    claim TEXT,
                    confidence REAL,
                    evidence_ref TEXT,
                    created_at REAL,
                    json TEXT
                );
                CREATE TABLE IF NOT EXISTS actions (
                    id TEXT PRIMARY KEY,
                    tool TEXT,
                    args_hash TEXT,
                    status TEXT,
                    reason TEXT,
                    risk_score REAL,
                    epsilon REAL,
                    created_at REAL,
                    json TEXT
                );
                CREATE TABLE IF NOT EXISTS psi_sessions (
                    id TEXT PRIMARY KEY,
                    topic TEXT,
                    r REAL,
                    phi_eff REAL,
                    epsilon REAL,
                    regime TEXT,
                    fingerprint TEXT,
                    created_at REAL,
                    json TEXT
                );
                CREATE TABLE IF NOT EXISTS receipts (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT,
                    kind TEXT,
                    object_id TEXT,
                    object_hash TEXT,
                    prev_hash TEXT,
                    chain_hash TEXT,
                    created_at REAL,
                    json TEXT
                );
                """
            )

    def add_observation(self, obs: ObservationEnvelope) -> str:
        obs.finalize()
        oid = obs.observation_id
        payload = obs.to_dict()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO observations
                (id, source, url, mode, hash, title, text_preview, created_at, source_confidence,
                 calibration_epsilon, r_cost, phi_gain, token_estimate, json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    oid,
                    obs.source,
                    obs.url,
                    obs.mode,
                    obs.content_hash,
                    obs.title,
                    obs.text[:500],
                    obs.timestamp,
                    obs.source_confidence,
                    obs.calibration_epsilon,
                    obs.r_cost,
                    obs.phi_gain,
                    obs.token_estimate,
                    json.dumps(payload, ensure_ascii=False, sort_keys=True),
                ),
            )
            self._receipt(conn, "observation", oid, payload)
        return oid

    def add_claim(self, observation_id: str, claim: str, confidence: float, evidence_ref: str = "") -> str:
        payload = {
            "observation_id": observation_id,
            "claim": claim,
            "confidence": confidence,
            "evidence_ref": evidence_ref,
            "created_at": time.time(),
        }
        cid = "claim_" + stable_payload_hash(payload)[:16]
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO claims
                (id, observation_id, claim, confidence, evidence_ref, created_at, json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    cid,
                    observation_id,
                    claim,
                    confidence,
                    evidence_ref,
                    payload["created_at"],
                    json.dumps(payload, ensure_ascii=False, sort_keys=True),
                ),
            )
            self._receipt(conn, "claim", cid, payload)
        return cid

    def log_action(self, proposal: ActionProposal, decision: GateDecision) -> str:
        payload = {
            "proposal": proposal.canonical(),
            "decision": decision.to_dict(),
            "created_at": time.time(),
        }
        aid = "act_" + stable_payload_hash(payload)[:16]
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO actions
                (id, tool, args_hash, status, reason, risk_score, epsilon, created_at, json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    aid,
                    proposal.tool,
                    proposal.args_hash,
                    decision.status.value,
                    decision.reason,
                    decision.risk_score,
                    decision.epsilon,
                    payload["created_at"],
                    json.dumps(payload, ensure_ascii=False, sort_keys=True),
                ),
            )
            self._receipt(conn, "action", aid, payload)
        return aid

    def save_session(self, psi: EstadoPSI) -> str:
        payload = psi.to_dict()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO psi_sessions
                (id, topic, r, phi_eff, epsilon, regime, fingerprint, created_at, json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    psi.session_id,
                    psi.topic,
                    psi.R,
                    psi.Phi_eff,
                    psi.epsilon,
                    psi.regime().value,
                    psi.fingerprint(),
                    time.time(),
                    json.dumps(payload, ensure_ascii=False, sort_keys=True),
                ),
            )
            self._receipt(conn, "psi_session", psi.session_id, payload)
        return psi.session_id

    def latest_status(self) -> Dict[str, Any]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            counts = {}
            for table in ["observations", "claims", "actions", "psi_sessions", "receipts"]:
                counts[table] = conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()["n"]
            last_receipt = conn.execute("SELECT * FROM receipts ORDER BY seq DESC LIMIT 1").fetchone()
            return {
                "db": str(self.path),
                "counts": counts,
                "last_chain_hash": last_receipt["chain_hash"] if last_receipt else None,
            }

    def _receipt(self, conn: sqlite3.Connection, kind: str, object_id: str, payload: Dict[str, Any]) -> None:
        prev_row = conn.execute("SELECT chain_hash FROM receipts ORDER BY seq DESC LIMIT 1").fetchone()
        prev_hash = prev_row[0] if prev_row else "GENESIS"
        object_hash = stable_payload_hash(payload)
        receipt = {
            "kind": kind,
            "object_id": object_id,
            "object_hash": object_hash,
            "prev_hash": prev_hash,
            "created_at": time.time(),
        }
        chain_hash = stable_payload_hash(receipt)
        conn.execute(
            """
            INSERT INTO receipts (kind, object_id, object_hash, prev_hash, chain_hash, created_at, json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                kind,
                object_id,
                object_hash,
                prev_hash,
                chain_hash,
                receipt["created_at"],
                json.dumps(receipt, ensure_ascii=False, sort_keys=True),
            ),
        )


def stable_payload_hash(payload: Dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")).hexdigest()
