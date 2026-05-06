from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "tools" / "observacionismo" / "validate_concepts.py"
SCHEMA_PATH = ROOT / "schemas" / "observacionismo_concepts.schema.json"
DATASET_PATH = ROOT / "data" / "observacionismo" / "concepts_seed.jsonl"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_concepts", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def base_record(**overrides):
    record = {
        "concept_id": "test_concept",
        "name": "Test Concept",
        "aliases": ["test"],
        "layer": "evidence",
        "status": "proxy_operacional",
        "claim_type": "evidence",
        "operational_definition": "A local test concept with enough evidence to validate.",
        "DO_deconstruction": {
            "observed_parts": ["source", "evidence"],
            "narrative_boundary": "test only",
            "technical_function": "exercise validator",
            "residue": "none",
        },
        "IOI_recompilation": {
            "validable_object": "json object",
            "runtime_target": "validator",
            "pass_condition": "no validation errors",
        },
        "inputs": ["input"],
        "transforms": ["validate"],
        "outputs": ["report"],
        "invariants": ["source exists"],
        "evidence_required": ["source path"],
        "falsifiers": ["source path missing"],
        "gates": [
            {
                "decision": "REVIEW",
                "condition": "test record",
                "required_evidence": ["source path"],
            }
        ],
        "safety_notes": ["test only"],
        "source_paths": ["schemas/observacionismo_concepts.schema.json"],
        "tests": [],
        "public_claim_allowed": False,
    }
    record.update(overrides)
    return record


def write_dataset(tmp_path: Path, *records: dict) -> Path:
    path = tmp_path / "concepts.jsonl"
    path.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")
    return path


def test_current_seed_dataset_validates():
    validator = load_validator()
    result = validator.validate_dataset(SCHEMA_PATH, DATASET_PATH, root=ROOT)

    assert result.ok, [issue.to_dict() for issue in result.errors]
    assert len(result.records) >= 20
    assert any(row["concept_id"] == "wabi_sabi_control_node" for row in result.records)


def test_public_claim_without_sufficient_evidence_fails(tmp_path):
    validator = load_validator()
    dataset = write_dataset(
        tmp_path,
        base_record(public_claim_allowed=True, status="proxy_operacional"),
    )

    result = validator.validate_dataset(SCHEMA_PATH, dataset, root=ROOT)

    assert not result.ok
    assert any(issue.path == "public_claim_allowed" for issue in result.errors)


def test_hypothesis_cannot_have_approve_gate(tmp_path):
    validator = load_validator()
    dataset = write_dataset(
        tmp_path,
        base_record(
            status="hipotesis",
            gates=[
                {
                    "decision": "APPROVE",
                    "condition": "not allowed for hypothesis",
                    "required_evidence": ["source path"],
                }
            ],
        ),
    )

    result = validator.validate_dataset(SCHEMA_PATH, dataset, root=ROOT)

    assert not result.ok
    assert any("hypothesis" in issue.message for issue in result.errors)


def test_missing_source_path_fails(tmp_path):
    validator = load_validator()
    dataset = write_dataset(
        tmp_path,
        base_record(source_paths=["missing/path/for/concept.md"]),
    )

    result = validator.validate_dataset(SCHEMA_PATH, dataset, root=ROOT)

    assert not result.ok
    assert any("source path not found" in issue.message for issue in result.errors)
