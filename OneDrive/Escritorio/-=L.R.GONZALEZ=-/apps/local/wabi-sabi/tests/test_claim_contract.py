import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.claim_contract import evaluate_claim_contract, evaluate_claim_contract_payload


APP_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args, workspace: Path, runtime: Path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(APP_ROOT)
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "wabi_sabi.cli.main",
            *args,
            "--workspace",
            str(workspace),
            "--runtime",
            str(runtime),
        ],
        cwd=str(APP_ROOT),
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
    )


def write_contract(workspace: Path, payload: dict) -> Path:
    path = workspace / "claim_contract.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def base_contract() -> dict:
    return {
        "schema": "wabi.claim_contract.v1",
        "claim": "The local operator panel reports state without applying source changes.",
        "claim_level": "operational",
        "evidence": ["python -m wabi_sabi.cli.main operator-status --json"],
        "falsifiers": ["Fails if source files are created by operator-status."],
        "risk_flags": [],
    }


def test_claim_contract_approves_operational_claim_with_evidence(tmp_path):
    path = write_contract(tmp_path, base_contract())

    payload = evaluate_claim_contract(workspace=tmp_path, spec_path=path)

    assert payload["schema"] == "wabi.claim_contract_evaluation.v1"
    assert payload["ok"] is True
    assert payload["gate"] == "APPROVE"
    assert payload["evidence_count"] == 1
    assert payload["falsifier_count"] == 1


def test_claim_contract_payload_evaluation_matches_file_path_gate():
    payload = evaluate_claim_contract_payload(base_contract(), contract_path="runtime/generated_claim_contract.json")

    assert payload["schema"] == "wabi.claim_contract_evaluation.v1"
    assert payload["gate"] == "APPROVE"
    assert payload["contract_path"].replace("\\", "/") == "runtime/generated_claim_contract.json"


def test_claim_contract_reviews_strong_claim_without_enough_evidence(tmp_path):
    contract = base_contract()
    contract["claim_level"] = "scientific"
    contract["evidence"] = ["one local note"]
    path = write_contract(tmp_path, contract)

    payload = evaluate_claim_contract(workspace=tmp_path, spec_path=path)

    assert payload["ok"] is True
    assert payload["gate"] == "REVIEW"
    assert "strong_claim_needs_two_or_more_evidence_refs" in payload["reasons"]
    assert "scientific_claim_requires_human_review" in payload["reasons"]


def test_claim_contract_blocks_unsafe_flags(tmp_path):
    contract = base_contract()
    contract["risk_flags"] = ["stealth"]
    path = write_contract(tmp_path, contract)

    payload = evaluate_claim_contract(workspace=tmp_path, spec_path=path)

    assert payload["ok"] is False
    assert payload["gate"] == "BLOCK"
    assert payload["status"] == "blocked"


def test_claim_contract_cli(tmp_path):
    path = write_contract(tmp_path, base_contract())

    proc = run_cli("claim-contract", str(path), "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["gate"] == "APPROVE"
    assert payload["fingerprint"]
