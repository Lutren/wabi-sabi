from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRIDGE_PATH = ROOT / "tools" / "observacionismo" / "bridge_concepts.py"


def load_bridge():
    spec = importlib.util.spec_from_file_location("bridge_concepts", BRIDGE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_seed_bridge_records_are_comms_compatible():
    bridge = load_bridge()
    validation = bridge.validate_dataset(bridge.DEFAULT_SCHEMA, bridge.DEFAULT_DATASET, root=ROOT)
    records, errors = bridge.build_bridge_records(validation.records, bridge.DEFAULT_DATASET, ROOT)

    assert validation.ok, [issue.to_dict() for issue in validation.errors]
    assert not errors
    assert len(records) >= 20
    assert all(row["observation_envelope"]["source_kind"] == "generated_artifact" for row in records)
    assert all(row["observation_envelope"]["evidence"] for row in records)


def test_hypotheses_do_not_get_approve_gate():
    bridge = load_bridge()
    validation = bridge.validate_dataset(bridge.DEFAULT_SCHEMA, bridge.DEFAULT_DATASET, root=ROOT)
    records, errors = bridge.build_bridge_records(validation.records, bridge.DEFAULT_DATASET, ROOT)

    assert not errors
    review_only = [
        row
        for row in records
        if row["status"] in {"hipotesis", "metafora_canon"}
    ]
    assert review_only
    assert all(row["observation_envelope"]["action_gate"] != "APPROVE" for row in review_only)


def test_l1_bridge_keeps_five_verb_contract():
    bridge = load_bridge()
    validation = bridge.validate_dataset(bridge.DEFAULT_SCHEMA, bridge.DEFAULT_DATASET, root=ROOT)
    records, errors = bridge.build_bridge_records(validation.records, bridge.DEFAULT_DATASET, ROOT)

    assert not errors
    for row in records:
        l1_bridge = row["l1_bridge"]
        assert l1_bridge["verb_sequence"] == ["OBSERVAR", "DOCUMENTAR", "VERIFICAR", "ACTUAR", "HANDOFF"]
        assert bridge.validate_l1_bridge(l1_bridge) == []


def test_public_claim_attempt_blocks_action_gate_payload():
    bridge = load_bridge()
    record = {
        "concept_id": "synthetic_public_claim",
        "status": "proxy_operacional",
        "claim_type": "evidence",
        "source_paths": ["schemas/observacionismo_concepts.schema.json"],
        "tests": [],
        "evidence_required": ["source path"],
        "falsifiers": ["missing source"],
        "public_claim_allowed": True,
    }

    assert bridge.claim_level(record) == "blocked_claim"
    payload = bridge.build_action_gate_payload(record)
    assert payload["decision"] == "BLOCK"
    assert payload["no_external_action"] is True
