from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.nvidia_route_diagnostic import (
    ALIAS_CANDIDATES,
    PROVIDER_OR_MODEL_NOT_FOUND,
    build_nvidia_route_diagnostic,
)
from wabi_sabi.core.provider_status_contract import PRIMARY_MODEL, build_provider_status_contract


def run_cli(*args, workspace: Path, runtime: Path):
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
        cwd=workspace,
        text=True,
        capture_output=True,
        check=False,
    )


def test_nvidia_route_diagnostic_no_cloud_call_by_default(tmp_path):
    payload = build_nvidia_route_diagnostic(
        runtime_root=tmp_path / "runtime",
        env={"NVIDIA_API_KEY": "route-diagnostic-secret-value-1234567890"},
    )

    assert payload["provider"] == "nvidia"
    assert payload["cloud_provider_called"] is False
    assert payload["recommended_next_smoke"] == "DO_NOT_CALL"
    assert payload["route_diagnostic_status"] == "REVIEW"
    assert payload["model_list_api_status"] == "REVIEW_MODEL_LIST_API"


def test_nvidia_route_diagnostic_redacts_credentials(tmp_path):
    redaction_marker = "route-redaction-marker-value-1234567890"

    payload = build_nvidia_route_diagnostic(
        runtime_root=tmp_path / "runtime",
        env={"WABI_ALLOW_CLOUD_PROVIDERS": "1", "NVIDIA_NIM_API_KEY": redaction_marker},
    )
    text = json.dumps(payload, ensure_ascii=False)

    assert payload["credential_present_redacted"] is True
    assert payload["secret_values_printed"] is False
    assert redaction_marker not in text


def test_nvidia_route_diagnostic_includes_alias_candidates(tmp_path):
    payload = build_nvidia_route_diagnostic(runtime_root=tmp_path / "runtime", env={})
    aliases = [item["alias"] for item in payload["alias_candidates"]]

    assert aliases == list(ALIAS_CANDIDATES)
    assert PRIMARY_MODEL in aliases
    assert "nvidia/nemotron-super-120b-a12b" in aliases


def test_provider_diagnose_cli_json(tmp_path, monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "cli-diagnose-secret-value-1234567890")

    proc = run_cli("provider", "diagnose", "--provider", "nvidia", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")
    payload = json.loads(proc.stdout)

    assert proc.returncode == 0
    assert payload["action"] == "provider_diagnose"
    assert payload["provider"] == "nvidia"
    assert payload["cloud_provider_called"] is False
    assert payload["route_diagnostic"]["endpoint_mode"] == "openai_compatible"
    assert payload["route_diagnostic"]["recommended_next_smoke"] == "DO_NOT_CALL"
    assert Path(payload["diagnostic_artifact"]).exists()


def test_provider_diagnose_does_not_print_secret_values(tmp_path, monkeypatch):
    redaction_marker = "cli-diagnose-print-marker-value-1234567890"
    monkeypatch.setenv("NVIDIA_API_KEY", redaction_marker)

    proc = run_cli("provider", "diagnose", "--provider", "nvidia", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0
    assert redaction_marker not in proc.stdout
    assert redaction_marker not in proc.stderr
    assert json.loads(proc.stdout)["secret_values_printed"] is False


def test_provider_status_preserves_smoke_fail_redacted(tmp_path):
    runtime = tmp_path / "runtime"
    latest = runtime / "outputs" / "wabi_provider_status_latest.json"
    latest.parent.mkdir(parents=True)
    latest.write_text(
        json.dumps(
            {
                "live_smoke_status": "SMOKE_FAIL_REDACTED",
                "last_smoke_timestamp": "2026-05-18T03:37:35Z",
                "cloud_allowed_mode": "EPHEMERAL_SINGLE_SMOKE_RECORDED",
            }
        ),
        encoding="utf-8",
    )

    payload = build_provider_status_contract(runtime_root=runtime, env={})

    assert payload["live_smoke_status"] == "SMOKE_FAIL_REDACTED"
    assert payload["cloud_allowed_mode"] == "EPHEMERAL_SINGLE_SMOKE_RECORDED"
    assert payload["provider_state"] == "CLOUD_DISABLED_BY_FLAG"


def test_route_diagnostic_classifies_provider_not_found_redacted(tmp_path):
    payload = build_nvidia_route_diagnostic(
        runtime_root=tmp_path / "runtime",
        env={"NVIDIA_API_KEY": "route-error-secret-value-1234567890"},
        latest_status={
            "live_smoke_status": "SMOKE_FAIL_REDACTED",
            "classification_reason": "single NVIDIA smoke returned provider 404; identifiers redacted",
        },
    )

    assert payload["last_error_class"] == PROVIDER_OR_MODEL_NOT_FOUND
    assert payload["route_diagnostic_status"] == "REVIEW"
    assert payload["recommended_next_action"] == "NVIDIA_DASHBOARD_ROUTE_REVIEW_REDACTED"


def test_provider_panel_v05_data_schema():
    path = Path(__file__).resolve().parents[1] / "qa_artifacts" / "provider_panel_v0_5" / "provider_panel_data_v0_5.json"
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["schema"] == "wabi.provider_panel_data.v0_5"
    assert payload["provider_status"]["live_smoke_status"] == "SMOKE_FAIL_REDACTED"
    assert payload["route_diagnostic"]["last_error_class"] == PROVIDER_OR_MODEL_NOT_FOUND
    assert payload["gates"]["PublicationGate"] == "BLOCK"


def test_provider_panel_v05_no_external_urls():
    root = Path(__file__).resolve().parents[1] / "qa_artifacts" / "provider_panel_v0_5"
    html = (root / "index.html").read_text(encoding="utf-8")

    assert "https://" not in html
    assert "http://" not in html
    assert "cdn" not in html.lower()


def test_provider_panel_v05_no_secret_values():
    root = Path(__file__).resolve().parents[1] / "qa_artifacts" / "provider_panel_v0_5"
    combined = (root / "index.html").read_text(encoding="utf-8") + "\n" + (root / "provider_panel_data_v0_5.json").read_text(encoding="utf-8")

    assert not re.search(r"(?i)nvapi-[A-Za-z0-9_-]{16,}", combined)
    assert not re.search(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]{16,}", combined)
    assert "secret-value" not in combined


def test_main_ui_integration_or_review_marker():
    wabi_root = Path(__file__).resolve().parents[1]
    desktop = wabi_root.parents[3]
    main_ui = desktop / "-= BRAIN_OS =-" / "apps" / "local" / "wabi_ui" / "index.html"
    review_marker = wabi_root / "qa_artifacts" / "provider_panel_v0_5" / "MAIN_UI_NOT_FOUND_REVIEW.md"

    if main_ui.exists():
        text = main_ui.read_text(encoding="utf-8")
        assert "providerDiagnosticPanel" in text
        assert "/api/provider/diagnostic" in text
    else:
        assert review_marker.exists()
