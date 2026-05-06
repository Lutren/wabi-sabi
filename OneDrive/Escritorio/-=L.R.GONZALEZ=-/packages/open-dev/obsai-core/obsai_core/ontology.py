from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import closing
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .metrics import clamp01


SCHEMA_VERSION = "obsai.observation_envelope.v1"
SCHEMA_VERSION_V2 = "obsai.observation_envelope.v2"
SHACL_SCHEMA_VERSION = "obsai.shacl_validation.v1"
PROV_SCHEMA_VERSION = "obsai.prov_o_graph.v1"
PAC_SCHEMA_VERSION = "obsai.pac_reasoning.v1"
STORE_SCHEMA_VERSION = "obsai.observation_store.v1"

ALLOWED_KINDS = {"process", "artifact", "mixed"}
EPSTEMIC_STATES = {"CERTEZA", "INFERENCIA", "HIPOTESIS", "ESPECULACION", "BLOQUEADO", ""}
CONTROLLED_CLAIM_TYPES = {
    "medical",
    "medical_claim",
    "publication",
    "publication_claim",
    "scientific",
    "scientific_claim",
    "social",
    "social_claim",
    "social_prediction",
}
DOLCE_KIND_MAP = {
    "process": "dolce:perdurant",
    "artifact": "dolce:endurant",
    "mixed": "dolce:mixed",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def observation_id(data: dict[str, Any]) -> str:
    digest = hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()[:24]
    return f"obs_{digest}"


def normalize_evidence(items: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(items or []):
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "id": str(item.get("id") or f"evidence_{index + 1}"),
                "label": str(item.get("label") or item.get("source") or "evidence"),
                "source": str(item.get("source") or item.get("uri") or item.get("label") or ""),
                "verified": bool(item.get("verified")),
                "confidence": clamp01(item.get("confidence", 0.5)),
            }
        )
    return normalized


def normalize_falsifiers(items: list[dict[str, Any]] | list[str] | None) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(items or []):
        if isinstance(item, dict):
            normalized.append(
                {
                    "id": str(item.get("id") or f"falsifier_{index + 1}"),
                    "status": str(item.get("status") or "not_run"),
                    "note": str(item.get("note") or item.get("description") or ""),
                }
            )
        else:
            normalized.append({"id": str(item), "status": "not_run", "note": ""})
    return normalized


def _dict_or_empty(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


@dataclass
class ObservationEnvelope:
    observer: str
    subject: str
    claim: str
    kind: str = "artifact"
    claim_type: str = "operational_claim"
    epistemic_state: str = ""
    evidence: list[dict[str, Any]] = field(default_factory=list)
    falsifiers: list[dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.5
    observed_at: str = field(default_factory=utc_now)
    provenance: dict[str, Any] = field(default_factory=dict)
    constraints: dict[str, Any] = field(default_factory=dict)
    psi_state: dict[str, Any] = field(default_factory=dict)
    sigma: dict[str, Any] = field(default_factory=dict)
    gate: dict[str, Any] = field(default_factory=dict)
    witness: dict[str, Any] = field(default_factory=dict)
    family_stewardship: dict[str, Any] = field(default_factory=dict)
    envelope_id: str = ""
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self) -> None:
        self.kind = str(self.kind or "").lower()
        self.claim_type = str(self.claim_type or "operational_claim")
        self.epistemic_state = str(self.epistemic_state or "").upper()
        self.confidence = clamp01(self.confidence)
        self.evidence = normalize_evidence(self.evidence)
        self.falsifiers = normalize_falsifiers(self.falsifiers)
        self.psi_state = _dict_or_empty(self.psi_state)
        self.sigma = _dict_or_empty(self.sigma)
        self.gate = _dict_or_empty(self.gate)
        self.witness = _dict_or_empty(self.witness)
        self.family_stewardship = _dict_or_empty(self.family_stewardship)
        if self.schema_version != SCHEMA_VERSION_V2 and self._has_v2_fields():
            self.schema_version = SCHEMA_VERSION_V2
        if not self.envelope_id:
            self.envelope_id = observation_id(
                {
                    "observer": self.observer,
                    "subject": self.subject,
                    "claim": self.claim,
                    "kind": self.kind,
                    "claim_type": self.claim_type,
                    "epistemic_state": self.epistemic_state,
                    "observed_at": self.observed_at,
                }
            )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ObservationEnvelope":
        claim_payload = data.get("claim") if isinstance(data.get("claim"), dict) else {}
        claim_text = str(claim_payload.get("text") or data.get("claim") or "")
        claim_type = str(
            claim_payload.get("claim_type")
            or claim_payload.get("claimType")
            or data.get("claim_type")
            or data.get("claimType")
            or "operational_claim"
        )
        confidence = clamp01(claim_payload.get("confidence", data.get("confidence", 0.5)))
        return cls(
            observer=str(data.get("observer") or ""),
            subject=str(data.get("subject") or ""),
            claim=claim_text,
            kind=str(data.get("kind") or "artifact"),
            claim_type=claim_type,
            epistemic_state=str(
                claim_payload.get("epistemic_state")
                or claim_payload.get("epistemicState")
                or data.get("epistemic_state")
                or data.get("epistemicState")
                or ""
            ),
            evidence=normalize_evidence(data.get("evidence") if isinstance(data.get("evidence"), list) else []),
            falsifiers=normalize_falsifiers(data.get("falsifiers") if isinstance(data.get("falsifiers"), list) else []),
            confidence=confidence,
            observed_at=str(data.get("observed_at") or data.get("observedAt") or utc_now()),
            provenance=data.get("provenance") if isinstance(data.get("provenance"), dict) else {},
            constraints=data.get("constraints") if isinstance(data.get("constraints"), dict) else {},
            psi_state=_dict_or_empty(data.get("psi_state") or data.get("psiState")),
            sigma=_dict_or_empty(data.get("sigma")),
            gate=_dict_or_empty(data.get("gate")),
            witness=_dict_or_empty(data.get("witness")),
            family_stewardship=_dict_or_empty(data.get("family_stewardship") or data.get("familyStewardship")),
            envelope_id=str(data.get("id") or data.get("envelope_id") or data.get("envelopeId") or ""),
            schema_version=str(data.get("schema_version") or data.get("schemaVersion") or SCHEMA_VERSION),
        )

    def _has_v2_fields(self) -> bool:
        return bool(
            self.epistemic_state
            or self.psi_state
            or self.sigma
            or self.falsifiers
            or self.gate
            or self.witness
            or self.family_stewardship
        )

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "schemaVersion": self.schema_version,
            "id": self.envelope_id,
            "observer": self.observer,
            "subject": self.subject,
            "claim": self.claim,
            "claimType": self.claim_type,
            "kind": self.kind,
            "dolceType": classify_dolce_kind(self.kind),
            "evidence": self.evidence,
            "confidence": self.confidence,
            "observedAt": self.observed_at,
            "provenance": self.provenance,
            "constraints": self.constraints,
        }
        if self.schema_version == SCHEMA_VERSION_V2 or self._has_v2_fields():
            payload["schemaVersion"] = SCHEMA_VERSION_V2
            payload["claimObject"] = {
                "text": self.claim,
                "claimType": self.claim_type,
                "epistemicState": self.epistemic_state or "INFERENCIA",
                "confidence": self.confidence,
            }
            payload["psiState"] = self.psi_state
            payload["sigma"] = self.sigma
            payload["falsifiers"] = self.falsifiers
            payload["gate"] = self.gate
            payload["witness"] = self.witness
            if self.family_stewardship:
                payload["familyStewardship"] = self.family_stewardship
        return payload


def ensure_envelope(envelope: ObservationEnvelope | dict[str, Any]) -> ObservationEnvelope:
    if isinstance(envelope, ObservationEnvelope):
        return envelope
    if isinstance(envelope, dict):
        return ObservationEnvelope.from_dict(envelope)
    raise TypeError("envelope must be an ObservationEnvelope or dict")


def classify_dolce_kind(kind: str) -> str:
    return DOLCE_KIND_MAP.get(str(kind or "").lower(), "dolce:unknown")


def _method(envelope: ObservationEnvelope) -> str:
    return str(
        envelope.provenance.get("method")
        or envelope.provenance.get("protocol")
        or envelope.constraints.get("method")
        or envelope.constraints.get("protocol")
        or ""
    )


def _falsifiers(envelope: ObservationEnvelope) -> list[str]:
    values = envelope.constraints.get("falsifiers") or envelope.provenance.get("falsifiers") or []
    raw = [str(item) for item in values] if isinstance(values, list) else []
    normalized = [str(item.get("id") or item.get("note") or "") for item in envelope.falsifiers]
    return [item for item in [*raw, *normalized] if item]


def validate_observation_envelope(envelope: ObservationEnvelope | dict[str, Any]) -> dict[str, Any]:
    item = ensure_envelope(envelope)
    violations: list[dict[str, Any]] = []

    def add(path: str, message: str, severity: str = "Violation") -> None:
        violations.append({"path": path, "severity": severity, "message": message})

    if not item.observer.strip():
        add("observer", "observer is required")
    if not item.subject.strip():
        add("subject", "subject is required")
    if not item.claim.strip():
        add("claim", "claim is required")
    if item.kind not in ALLOWED_KINDS:
        add("kind", "kind must be process, artifact or mixed")
    if item.epistemic_state not in EPSTEMIC_STATES:
        add("epistemic_state", "epistemic_state must be CERTEZA, INFERENCIA, HIPOTESIS, ESPECULACION or BLOQUEADO")
    if item.epistemic_state == "BLOQUEADO":
        add("epistemic_state", "blocked epistemic state cannot be approved")
    if not item.evidence:
        add("evidence", "at least one evidence item is required", "Warning")
    if not 0.0 <= item.confidence <= 1.0:
        add("confidence", "confidence must be between 0 and 1")

    claim_type = item.claim_type.lower()
    scientific = claim_type == "scientific_claim"
    controlled_claim = claim_type in CONTROLLED_CLAIM_TYPES
    verified_evidence = any(evidence.get("verified") for evidence in item.evidence)
    if controlled_claim and not verified_evidence:
        add("evidence", f"{item.claim_type} requires verified evidence")
    if scientific and not _method(item):
        add("provenance.method", "scientific_claim requires method or protocol", "Warning")
    if controlled_claim and not _falsifiers(item):
        add("constraints.falsifiers", f"{item.claim_type} requires falsifiers", "Warning")

    psi = item.psi_state
    if psi:
        regime = str(psi.get("regime") or "").upper()
        phi_eff = psi.get("Phi_eff", psi.get("phi_eff", 1.0))
        residue = psi.get("R", psi.get("residue", 0.0))
        jamming_threshold = psi.get("J_c", psi.get("j_c", 1.0))
        try:
            if float(residue) >= float(jamming_threshold):
                add("psi_state.R", "R must stay below J_c for approval")
            if float(phi_eff) < 0.55:
                add("psi_state.Phi_eff", "Phi_eff below approval band", "Warning")
        except (TypeError, ValueError):
            add("psi_state", "R, J_c and Phi_eff must be numeric", "Warning")
        if regime in {"JAMMING", "BLOCKED"}:
            add("psi_state.regime", "regime blocks approval")

    gate_decision = str(item.gate.get("decision") or "").upper()
    if gate_decision == "BLOCK":
        add("gate.decision", "gate decision BLOCK cannot be approved")

    family = item.family_stewardship
    if family:
        if family.get("storesSecretsPlaintext") is True or family.get("stores_secrets_plaintext") is True:
            add("family_stewardship.stores_secrets_plaintext", "family stewardship cannot store secrets in plaintext")
        if family.get("externalAction") is True or family.get("external_action") is True:
            add("family_stewardship.external_action", "family stewardship external actions require a separate gate")
        if family.get("localOnly") is False or family.get("local_only") is False:
            add("family_stewardship.local_only", "family stewardship envelope must remain local")

    return {
        "schemaVersion": SHACL_SCHEMA_VERSION,
        "profile": "shacl-lite-json",
        "shape": "ObservationEnvelopeShape",
        "target": item.envelope_id,
        "conforms": not any(v["severity"] == "Violation" for v in violations),
        "violations": violations,
    }


def to_prov_o(envelope: ObservationEnvelope | dict[str, Any]) -> dict[str, Any]:
    item = ensure_envelope(envelope)
    envelope_dict = item.to_dict()
    evidence_nodes = [
        {
            "@id": f"{item.envelope_id}:evidence:{evidence['id']}",
            "@type": "prov:Entity",
            "schema:name": evidence["label"],
            "schema:url": evidence["source"],
            "prov:wasAttributedTo": f"{item.envelope_id}:observer",
            "obsai:verified": evidence["verified"],
            "obsai:confidence": evidence["confidence"],
        }
        for evidence in item.evidence
    ]
    return {
        "schemaVersion": PROV_SCHEMA_VERSION,
        "@context": {
            "prov": "http://www.w3.org/ns/prov#",
            "schema": "https://schema.org/",
            "dolce": "http://www.loa-cnr.it/ontologies/DOLCE-Lite.owl#",
            "obsai": "https://medioevo.local/obsai#",
        },
        "@graph": [
            {
                "@id": f"{item.envelope_id}:observer",
                "@type": "prov:Agent",
                "schema:name": item.observer,
            },
            {
                "@id": f"{item.envelope_id}:activity",
                "@type": ["prov:Activity", classify_dolce_kind(item.kind)],
                "prov:startedAtTime": item.observed_at,
                "prov:wasAssociatedWith": f"{item.envelope_id}:observer",
                "prov:used": [node["@id"] for node in evidence_nodes],
            },
            {
                "@id": f"{item.envelope_id}:claim",
                "@type": ["prov:Entity", "schema:Claim"],
                "schema:about": item.subject,
                "schema:text": item.claim,
                "obsai:claimType": item.claim_type,
                "obsai:confidence": item.confidence,
                "prov:wasGeneratedBy": f"{item.envelope_id}:activity",
                "obsai:envelope": envelope_dict,
            },
            *evidence_nodes,
        ],
    }


class OntologyGraph:
    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []

    def add_envelope(self, envelope: ObservationEnvelope | dict[str, Any]) -> dict[str, Any]:
        item = ensure_envelope(envelope)
        validation = validate_observation_envelope(item)
        record = {
            "envelope": item.to_dict(),
            "validation": validation,
            "provO": to_prov_o(item),
            "dolceType": classify_dolce_kind(item.kind),
        }
        self.records.append(record)
        return record

    def validate_all(self) -> dict[str, Any]:
        validations = [record["validation"] for record in self.records]
        return {
            "schemaVersion": SHACL_SCHEMA_VERSION,
            "profile": "shacl-lite-json",
            "conforms": all(item["conforms"] for item in validations),
            "count": len(validations),
            "validations": validations,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "schemaVersion": "obsai.ontology_graph.v1",
            "count": len(self.records),
            "records": self.records,
        }


class PACReasoner:
    def evaluate(self, envelope: ObservationEnvelope | dict[str, Any]) -> dict[str, Any]:
        item = ensure_envelope(envelope)
        validation = validate_observation_envelope(item)
        reasons: list[str] = []
        status = "APPROVE"
        action = "APPROVE"

        hard_violations = [v for v in validation["violations"] if v["severity"] == "Violation"]
        warnings = [v for v in validation["violations"] if v["severity"] == "Warning"]
        if hard_violations:
            status = "BLOCK"
            action = "ABSTAIN"
            reasons.extend(v["message"] for v in hard_violations)
        elif warnings or item.confidence < 0.55:
            status = "REVIEW"
            action = "REVIEW"
            reasons.extend(v["message"] for v in warnings)
            if item.confidence < 0.55:
                reasons.append("confidence below PAC approval band")
        else:
            reasons.append("evidence and envelope shape satisfy PAC minimums")

        return {
            "schemaVersion": PAC_SCHEMA_VERSION,
            "status": status,
            "action": action,
            "reasons": reasons,
            "validation": validation,
            "claims": {
                "reasoning": "PAC_GATE_ONLY",
                "thresholdCalibration": "DEMO_ONLY",
            },
        }


class ObservationEnvelopeStore:
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
                CREATE TABLE IF NOT EXISTS observation_envelopes (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    envelope_json TEXT NOT NULL,
                    validation_json TEXT NOT NULL,
                    prov_json TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def insert_envelope(self, envelope: ObservationEnvelope | dict[str, Any]) -> dict[str, Any]:
        item = ensure_envelope(envelope)
        envelope_dict = item.to_dict()
        validation = validate_observation_envelope(item)
        prov = to_prov_o(item)
        with closing(self.connect()) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO observation_envelopes
                (id, created_at, envelope_json, validation_json, prov_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    item.envelope_id,
                    utc_now(),
                    canonical_json(envelope_dict),
                    canonical_json(validation),
                    canonical_json(prov),
                ),
            )
            conn.commit()
        return self.get_envelope(item.envelope_id) or {}

    def get_envelope(self, envelope_id: str) -> dict[str, Any] | None:
        with closing(self.connect()) as conn:
            row = conn.execute("SELECT * FROM observation_envelopes WHERE id = ?", (envelope_id,)).fetchone()
            if row is None:
                return None
            return self._row(row)

    def list_envelopes(self, limit: int = 100) -> list[dict[str, Any]]:
        with closing(self.connect()) as conn:
            rows = conn.execute(
                "SELECT * FROM observation_envelopes ORDER BY created_at DESC LIMIT ?",
                (max(1, min(500, int(limit))),),
            ).fetchall()
            return [self._row(row) for row in rows]

    @staticmethod
    def _row(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "schemaVersion": STORE_SCHEMA_VERSION,
            "id": row["id"],
            "createdAt": row["created_at"],
            "envelope": json.loads(row["envelope_json"]),
            "validation": json.loads(row["validation_json"]),
            "provO": json.loads(row["prov_json"]),
        }
