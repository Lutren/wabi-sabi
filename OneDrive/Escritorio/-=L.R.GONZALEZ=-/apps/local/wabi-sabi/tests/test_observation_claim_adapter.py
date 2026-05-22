import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.observation_claim_adapter import (
    run_claim_fixture_review,
    run_claim_observation_adapter,
)


APP_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args, workspace: Path, runtime: Path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(APP_ROOT)
    env["MEDIOEVO_NO_MODEL_MODE"] = "1"
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


def fixture_payload() -> dict:
    return {
        "schema_version": "medioevo.claim_classifier.fixtures.v0.1",
        "publication_gate": "BLOCK",
        "cases": [
            {
                "id": "CC-T-001",
                "claim": "2 + 2 = 4",
                "expected_label": "CERTEZA",
                "expected_gate": "APPROVE_DOCS",
                "r_range": [0.0, 0.35],
                "phi_moi_range": [0.55, 1.0],
            },
            {
                "id": "CC-T-002",
                "claim": "New physics proves extra dimension.",
                "expected_label": "BLOQUEO",
                "expected_gate": "BLOCK_AS_FACT",
                "r_range": [0.70, 1.0],
                "phi_moi_range": [0.0, 0.35],
            },
        ],
    }


def test_claim_observation_adapter_is_proposal_only_and_persists(tmp_path):
    payload = run_claim_observation_adapter(
        "2 + 2 = 4",
        workspace=tmp_path / "workspace",
        runtime_root=tmp_path / "runtime",
    )

    assert payload["schema"] == "wabi.claim_observation_adapter.v0_1"
    assert payload["proposal_only"] is True
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False
    assert payload["publication_gate"] == "BLOCK"
    assert payload["obsai_envelope"]["schemaVersion"] == "obsai.observation_envelope.v2.1"
    assert payload["wabi_observation"]["envelope_version"] == "wabi-observation-v1"
    assert payload["proposal"]["apply_allowed"] is False
    assert payload["persistence"]["witness_verified"] is True
    assert Path(payload["persistence"]["artifact"]).exists()
    assert not list((tmp_path / "workspace").glob("*"))


def test_claim_fixture_review_uses_synthetic_fixtures_without_applying(tmp_path):
    fixture = tmp_path / "fixtures.json"
    fixture.write_text(json.dumps(fixture_payload()), encoding="utf-8")

    payload = run_claim_fixture_review(
        fixture,
        workspace=tmp_path / "workspace",
        runtime_root=tmp_path / "runtime",
    )

    assert payload["schema"] == "wabi.claim_observation_fixture_review.v0_1"
    assert payload["ok"] is True
    assert payload["case_count"] == 2
    assert payload["status"] == "PASS"
    assert payload["next_safe_action"].startswith("Fixture review passed")
    assert payload["proposal_only"] is True
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False
    assert payload["persistence"]["witness_verified"] is True
    assert not list((tmp_path / "workspace").glob("*"))


def test_claim_observation_cli_outputs_json_contract(tmp_path):
    proc = run_cli(
        "claim-observation",
        "2 + 2 = 4",
        "--json",
        workspace=tmp_path / "workspace",
        runtime=tmp_path / "runtime",
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["schema"] == "wabi.claim_observation_adapter.v0_1"
    assert payload["mode"] == "proposal_only"
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False
