from __future__ import annotations

import importlib.util
import json
import os
import sys
import threading
import urllib.request
from pathlib import Path

from wabi_sabi.core.cloud_budget import CloudBudgetGate


REPO_ROOT = Path(__file__).resolve().parents[4]
BRAIN_OS_ROOT = REPO_ROOT.parent / "-= BRAIN_OS =-"
SERVER_PATH = BRAIN_OS_ROOT / "02_CLAUDIO" / "server" / "wabi_local_server.py"
UI_INDEX = BRAIN_OS_ROOT / "apps" / "local" / "wabi_ui" / "index.html"


def load_server_module():
    assert SERVER_PATH.exists(), f"missing Wabi UI server: {SERVER_PATH}"
    spec = importlib.util.spec_from_file_location("wabi_cloud_budget_ui_server_test", SERVER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def isolate_budget_env(monkeypatch, tmp_path: Path, **extra: str) -> dict[str, str]:
    for key in (
        "WABI_BUILD_ASSIST_CLOUD",
        "WABI_ALLOW_CLOUD_PROVIDERS",
        "WABI_CLOUD_MAX_CALLS_PER_SESSION",
        "WABI_CLOUD_MAX_CALLS_PER_DAY",
        "WABI_CLOUD_USAGE_DIR",
        "WABI_SESSION_ID",
        "NVIDIA_API_KEY",
    ):
        monkeypatch.delenv(key, raising=False)
    env = {
        "WABI_CLOUD_USAGE_DIR": str(tmp_path / "runtime" / "cloud_budget"),
        "WABI_SESSION_ID": "ui-budget-test",
    }
    env.update(extra)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    return env


def test_cloud_budget_endpoint_returns_redacted_status(monkeypatch, tmp_path):
    isolate_budget_env(monkeypatch, tmp_path, NVIDIA_API_KEY="nvapi-test-secret-1234567890")
    server = load_server_module()
    payload = server.cloud_budget_status_payload()
    encoded = json.dumps(payload, ensure_ascii=False)

    assert payload["ok"] is True
    assert payload["cloud_budget"]["budget_gate"] == "CLOUD_BUDGET_DRY_RUN"
    assert payload["cloud_budget"]["double_opt_in"] is False
    assert payload["cloud_budget"]["proposal_only"] is True
    assert payload["cloud_budget"]["cloud_provider_called"] is False
    assert "nvapi-test-secret" not in encoded
    assert "api_key" not in encoded.lower()


def test_cloud_budget_endpoint_http_response(monkeypatch, tmp_path):
    isolate_budget_env(monkeypatch, tmp_path)
    server_module = load_server_module()
    httpd = server_module.make_server("127.0.0.1", 0)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = httpd.server_address
        with urllib.request.urlopen(f"http://{host}:{port}/api/cloud-budget/status", timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
    finally:
        httpd.shutdown()
        thread.join(timeout=5)
        httpd.server_close()

    assert payload["cloud_budget"]["provider"] == "nvidia"
    assert payload["cloud_budget"]["model_alias"] == "nano-30b"
    assert payload["cloud_budget"]["cloud_provider_called"] is False


def test_cloud_budget_exceeded_status(monkeypatch, tmp_path):
    env = isolate_budget_env(
        monkeypatch,
        tmp_path,
        WABI_BUILD_ASSIST_CLOUD="1",
        WABI_ALLOW_CLOUD_PROVIDERS="1",
        WABI_CLOUD_MAX_CALLS_PER_SESSION="1",
    )
    CloudBudgetGate(runtime_root=tmp_path / "runtime", session_id="ui-budget-test", env={**os.environ, **env}).record_planned_call(
        "nvidia",
        "nano-30b",
        "ui_budget_test",
    )
    server = load_server_module()

    payload = server.cloud_budget_status_payload()

    assert payload["cloud_budget"]["budget_gate"] == "CLOUD_BUDGET_EXCEEDED"
    assert payload["cloud_budget"]["next_cloud_call_allowed"] is False
    assert payload["cloud_budget"]["cloud_provider_called"] is False


def test_wabi_ui_renders_cloud_budget_panel():
    text = UI_INDEX.read_text(encoding="utf-8")

    assert "Cloud Budget" in text
    assert "cloudBudgetPanel" in text
    assert "/api/cloud-budget/status" in text
    assert "cloudBudgetProviderModel" in text
    assert "cloudBudgetProposalOnly" in text
    assert "cloudBudgetProviderCalled" in text
    assert "NVIDIA cloud is proposal-only; outputs are not applied automatically." in text
    assert "Call NVIDIA now" not in text
    assert "Apply cloud output" not in text


def test_operational_workbench_embeds_cloud_budget(monkeypatch, tmp_path):
    isolate_budget_env(monkeypatch, tmp_path)
    server = load_server_module()

    payload = server.operational_workbench_payload()

    assert payload["cloud_budget"]["budget_gate"] == "CLOUD_BUDGET_DRY_RUN"
    assert payload["gates"]["CloudBudgetGate"] == "CLOUD_BUDGET_DRY_RUN"
    assert payload["cloud_budget"]["cloud_provider_called"] is False
