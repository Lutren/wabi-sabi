import json
import subprocess
import sys

from wabi_sabi.core.geodia_synthetic_surface import (
    GEODIA_SYNTHETIC_SURFACE_SCHEMA,
    build_geodia_synthetic_surface,
)
from wabi_sabi.core.tool_registry import tool_registry_payload


def test_geodia_synthetic_surface_contract_is_bounded_and_low_claim():
    payload = build_geodia_synthetic_surface()

    assert payload["schema"] == GEODIA_SYNTHETIC_SURFACE_SCHEMA
    assert payload["ok"] is True
    assert payload["status"] == "SYNTHETIC_ONLY"
    assert payload["claim_gate"] == "NO_PUBLIC_STRONG_CLAIM_UNTIL_NUMERIC_VALIDATION"
    assert payload["source"]["external_io"] is False
    assert payload["source"]["runtime_writes"] is False
    assert payload["bounded"] is True

    after = payload["metrics"]["after"]
    for value in [after["R"], after["phi_eff"], after["j_c"], after["epsilon"], after["fatigue"], after["I_obs"], *after["sigma"]]:
        assert 0 <= value <= 1
    assert 0 <= payload["metrics"]["eml"] <= 10


def test_geodia_synthetic_surface_is_deterministic():
    first = build_geodia_synthetic_surface()
    second = build_geodia_synthetic_surface()

    assert first["metrics"] == second["metrics"]
    assert first["cells"]["after"] == second["cells"]["after"]


def test_geodia_synthetic_surface_cli_json(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "wabi_sabi.cli.main",
            "geodia-synthetic",
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
    assert payload["schema"] == GEODIA_SYNTHETIC_SURFACE_SCHEMA
    assert payload["status"] == "SYNTHETIC_ONLY"
    assert payload["bounded"] is True


def test_tool_registry_exposes_geodia_synthetic_surface():
    payload = tool_registry_payload()
    names = {tool["name"] for tool in payload["tools"]}

    assert "geodia_synthetic_surface" in names
