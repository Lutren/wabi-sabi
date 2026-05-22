import json
import subprocess
import sys

from wabi_sabi.core.geodia_synthetic_falsifier import (
    GEODIA_SYNTHETIC_FALSIFIER_SCHEMA,
    build_geodia_synthetic_falsifier,
    write_geodia_synthetic_falsifier,
)
from wabi_sabi.core.tool_registry import tool_registry_payload


def test_geodia_synthetic_falsifier_passes_operational_claim_contract(tmp_path):
    payload = build_geodia_synthetic_falsifier()
    enriched = write_geodia_synthetic_falsifier(payload, workspace=tmp_path, output_dir=tmp_path / "runtime" / "outputs")

    assert enriched["schema"] == GEODIA_SYNTHETIC_FALSIFIER_SCHEMA
    assert enriched["ok"] is True
    assert enriched["result"] == "PASS"
    assert enriched["claim_gate"] == "OPERATIONAL_ONLY_NO_PUBLIC_STRONG_CLAIM"
    assert all(item["passed"] for item in enriched["falsifiers"])
    assert enriched["claim_evaluation"]["gate"] == "APPROVE"
    assert enriched["claim_evaluation"]["claim_level"] == "operational"
    for artifact in enriched["artifacts"]:
        assert artifact


def test_geodia_synthetic_falsifier_cli_json(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "wabi_sabi.cli.main",
            "geodia-falsifier",
            "--workspace",
            str(tmp_path),
            "--runtime",
            str(tmp_path / "runtime"),
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(result.stdout)
    assert payload["schema"] == GEODIA_SYNTHETIC_FALSIFIER_SCHEMA
    assert payload["result"] == "PASS"
    assert payload["claim_evaluation"]["gate"] == "APPROVE"
    assert len(payload["artifacts"]) == 2


def test_tool_registry_exposes_geodia_synthetic_falsifier():
    payload = tool_registry_payload()
    names = {tool["name"] for tool in payload["tools"]}

    assert "geodia_synthetic_falsifier" in names
