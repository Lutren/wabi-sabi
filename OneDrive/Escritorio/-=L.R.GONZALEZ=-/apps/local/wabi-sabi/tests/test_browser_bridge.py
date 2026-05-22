import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.browser_bridge import (
    BROWSER_BRIDGE_ENABLE_ENV,
    BROWSER_SEND_ENABLE_ENV,
    build_browser_bridge_status,
    convert_browser_response_to_proposal,
    observe_browser_url,
    prepare_browser_ai_consultation,
    prepare_browser_council,
    run_devtools_readonly_snapshot,
    run_kimi_smoke,
)
from wabi_sabi.core.browser_bridge_selector_pack import (
    PUBLIC_PROMPT,
    PRIVATE_WORKSPACE_BLOCKED,
    build_selector_pack_status,
    rank_browser_council_services,
    select_browser_bridge_backend,
)
from wabi_sabi.core.cloud_code_proposal import build_dry_run_cloud_code_proposal


APP_ROOT = Path(__file__).resolve().parents[1]
KIMI_SETUP_GUIDE = APP_ROOT / "docs" / "KIMI_WEBBRIDGE_SETUP_GUIDE_REDACTED_20260518.md"
KIMI_DRY_RUN_EXAMPLES = APP_ROOT / "docs" / "KIMI_WEBBRIDGE_DRY_RUN_EXAMPLES_20260518.md"


def run_cli(*args, workspace: Path, runtime: Path, extra_env: dict[str, str] | None = None):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(APP_ROOT)
    env.pop("WABI_ALLOW_BROWSER_SEND", None)
    env.pop("WABI_ALLOW_BROWSER_BRIDGE", None)
    env.pop("WABI_KIMI_WEBBRIDGE_URL", None)
    if extra_env:
        env.update(extra_env)
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


def test_browser_bridge_status_is_local_first_and_no_auto_install():
    status = build_browser_bridge_status(env={}, command_finder=lambda _name: None)
    backends = {item["backend"]: item for item in status["backends"]}

    assert status["schema"] == "wabi.browser_bridge_status.v0_1"
    assert status["install_policy"] == "no_auto_install_no_curl_pipe_no_global_config"
    assert status["primary_backend"] == "chrome-devtools-mcp"
    assert backends["dry-run"]["available"] is True
    assert backends["chrome-devtools-mcp"]["available"] is False
    assert backends["kimi-webbridge"]["enabled"] is False
    assert status["send_enabled"] is False
    assert {"kimi", "chatgpt", "claude", "gemini", "deepseek4"}.issubset(set(status["ai_service_allowlist"]))
    assert status["selector_pack"]["version"] == "v0.2"


def test_selector_pack_exists_and_dry_run_available():
    status = build_selector_pack_status(env={}, command_finder=lambda _name: None)
    decision = select_browser_bridge_backend(service_id="dry-run", payload_class=PUBLIC_PROMPT, env={})

    assert status["schema"] == "wabi.browser_bridge_selector_pack.v0_2"
    assert status["dry_run_available"] is True
    assert decision["selected_backend"] == "dry-run"
    assert decision["mode"] == "DRY_RUN"
    assert decision["publication_gate"] == "BLOCK"


def test_selector_blocks_private_workspace_payload():
    decision = select_browser_bridge_backend(
        service_id="kimi",
        payload_class=PRIVATE_WORKSPACE_BLOCKED,
        env={},
    )

    assert decision["mode"] == "BLOCK"
    assert decision["safe_to_send"] is False
    assert "PRIVATE_WORKSPACE_BLOCKED" in decision["blocked_payload_reason"]


def test_selector_kimi_requires_double_opt_in():
    decision = select_browser_bridge_backend(
        service_id="kimi",
        payload_class=PUBLIC_PROMPT,
        requested_backend="kimi-webbridge",
        env={BROWSER_BRIDGE_ENABLE_ENV: "1", "WABI_KIMI_WEBBRIDGE_URL": "http://127.0.0.1:7777/bridge"},
        send_requested=False,
    )

    assert decision["mode"] == "SEND_REVIEW"
    assert decision["requires_double_opt_in"] is True
    assert decision["safe_to_send"] is False


def test_selector_unknown_service_prepare_only():
    decision = select_browser_bridge_backend(service_id="unknown-service", payload_class=PUBLIC_PROMPT, env={})

    assert decision["mode"] == "PREPARE_ONLY"
    assert decision["selected_backend"] == "dry-run"
    assert decision["safe_to_send"] is False


def test_observe_browser_url_dry_run_writes_artifact_without_source_or_network(tmp_path):
    runtime = tmp_path / "runtime"
    payload = observe_browser_url(
        workspace=tmp_path,
        runtime_root=runtime,
        url="https://example.com/docs",
        action="extract",
        env={},
    )

    assert payload["ok"] is True
    assert payload["gate"] == "APPROVE"
    assert payload["browser_backend_called"] is False
    assert payload["online_ai_called"] is False
    assert Path(payload["artifact"]).exists()
    assert not (tmp_path / "docs").exists()
    assert payload["observation"]["cookies_extracted"] is False


def test_observe_browser_url_review_does_not_call_backend(tmp_path):
    payload = observe_browser_url(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        url="https://example.com/login",
        action="type",
        text="hello",
        env={},
    )

    assert payload["ok"] is False
    assert payload["gate"] == "REVIEW"
    assert payload["browser_backend_called"] is False
    assert payload["online_ai_called"] is False


def test_browser_ai_consultation_is_review_by_default_and_redacts(tmp_path):
    synthetic_secret = "sk-" + "test-secret-12345678901234567890"
    payload = prepare_browser_ai_consultation(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        service="kimi",
        prompt=f"usa {synthetic_secret} para consultar",
        env={},
    )
    text = json.dumps(payload)

    assert payload["ok"] is True
    assert payload["gate"] == "REVIEW"
    assert payload["online_ai_called"] is False
    assert "sk-test-secret" not in text
    assert "[REDACTED:" in text
    assert Path(payload["artifact"]).exists()


def test_browser_ai_consultation_env_without_send_stays_review(tmp_path):
    payload = prepare_browser_ai_consultation(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        service="chatgpt",
        prompt="compara dos enfoques publicos",
        env={BROWSER_SEND_ENABLE_ENV: "1"},
    )

    assert payload["gate"] == "REVIEW"
    assert "send_flag_required" in payload["reasons"]
    assert payload["online_ai_called"] is False
    assert payload["request"]["local_revalidation_required"] is True


def test_browser_ai_consultation_send_requires_available_proven_backend(tmp_path):
    payload = prepare_browser_ai_consultation(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        service="kimi",
        prompt="responde con propuesta",
        backend="kimi-webbridge",
        env={BROWSER_SEND_ENABLE_ENV: "1"},
        send_requested=True,
    )

    assert payload["gate"] == "REVIEW_SKIPPED"
    assert payload["online_ai_called"] is False
    assert payload["browser_backend_called"] is False
    assert "browser_backend_not_enabled_or_not_configured" in payload["reasons"]


def test_browser_ai_consultation_send_converts_structured_response_to_validated_proposal(tmp_path):
    proposal = build_dry_run_cloud_code_proposal(intent="crear helper")

    def fake_sender(_request):
        return {"ok": True, "output": json.dumps(proposal)}

    payload = prepare_browser_ai_consultation(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        service="kimi",
        prompt="crea una propuesta de codigo",
        backend="kimi-webbridge",
        env={
            BROWSER_SEND_ENABLE_ENV: "1",
            BROWSER_BRIDGE_ENABLE_ENV: "1",
            "WABI_KIMI_WEBBRIDGE_URL": "http://127.0.0.1:65535/webbridge",
        },
        send_requested=True,
        sender=fake_sender,
    )

    assert payload["gate"] == "APPROVE"
    assert payload["online_ai_called"] is True
    assert payload["browser_backend_called"] is True
    assert payload["proposal_extraction"]["ok"] is True
    assert payload["proposal_extraction"]["validation"]["cloud_authority"] == "proposal_only"


def test_kimi_smoke_not_run_without_flags(tmp_path):
    payload = run_kimi_smoke(runtime_root=tmp_path / "runtime", env={}, send_requested=False)

    assert payload["status"] == "KIMI_SEND_FLAGS_MISSING"
    assert payload["online_ai_called"] is False
    assert payload["workspace_sent"] is False


def test_kimi_setup_guide_exists():
    assert KIMI_SETUP_GUIDE.exists()
    text = KIMI_SETUP_GUIDE.read_text(encoding="utf-8")

    assert "KIMI_SEND_FLAGS_MISSING" in text
    assert "BrowserBridge v0.2" in text
    assert "dry-run" in text
    assert "Return exactly this JSON:" in text
    assert '{"ok":true,"service":"kimi","bridge":"smoke"}' in text
    assert "no ejecuta ese comando" in text


def test_kimi_setup_guide_has_no_secret_values():
    text = KIMI_SETUP_GUIDE.read_text(encoding="utf-8")
    lowered = text.lower()

    assert "sk-" not in lowered
    assert "bearer " not in lowered
    assert "api_key=" not in lowered
    assert "password=" not in lowered
    assert "cookie:" not in lowered
    assert "<local-kimi-webbridge-url-redacted>" in text


def test_no_private_workspace_in_browser_bridge_docs():
    docs = KIMI_SETUP_GUIDE.read_text(encoding="utf-8") + "\n" + KIMI_DRY_RUN_EXAMPLES.read_text(encoding="utf-8")

    assert "C:\\Users" not in docs
    assert "OneDrive" not in docs
    assert "L-Tyr" not in docs
    assert "-= BRAIN_OS =-" not in docs
    assert "workspace privado" in docs


def test_kimi_smoke_uses_public_payload_only(tmp_path):
    def fake_sender(request):
        assert "workspace" not in json.dumps(request).lower()
        assert request["prompt"] == 'Return exactly this JSON:\n{"ok":true,"service":"kimi","bridge":"smoke"}'
        return {"ok": True, "output": '{"ok":true,"service":"kimi","bridge":"smoke"}'}

    payload = run_kimi_smoke(
        runtime_root=tmp_path / "runtime",
        env={
            BROWSER_SEND_ENABLE_ENV: "1",
            BROWSER_BRIDGE_ENABLE_ENV: "1",
            "WABI_KIMI_WEBBRIDGE_URL": "http://127.0.0.1:7777/bridge",
        },
        send_requested=True,
        sender=fake_sender,
    )

    assert payload["status"] == "KIMI_SMOKE_PASS"
    assert payload["online_ai_called"] is True
    assert payload["workspace_sent"] is False


def test_devtools_snapshot_readonly_or_not_available(tmp_path):
    not_available = run_devtools_readonly_snapshot(
        runtime_root=tmp_path / "runtime",
        env={},
        command_finder=lambda _name: None,
    )
    assert not_available["status"] == "DEVTOOLS_MCP_NOT_AVAILABLE"
    assert not_available["browser_backend_called"] is False

    readonly = run_devtools_readonly_snapshot(
        runtime_root=tmp_path / "runtime",
        env={BROWSER_BRIDGE_ENABLE_ENV: "1"},
        command_finder=lambda name: "npx" if name == "npx" else None,
        fetcher=lambda _url, _timeout: "<html><head><title>Wabi Hub</title></head><body><h1>Wabi</h1><button>Run</button></body></html>",
    )
    assert readonly["status"] == "DEVTOOLS_MCP_READONLY_PASS"
    assert readonly["snapshot"]["title"] == "Wabi Hub"
    assert readonly["online_ai_called"] is False


def test_browser_ai_consultation_blocks_unknown_service(tmp_path):
    payload = prepare_browser_ai_consultation(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        service="https://unknown.example.com/",
        prompt="hola",
        env={},
    )

    assert payload["ok"] is False
    assert payload["gate"] == "BLOCK"
    assert payload["online_ai_called"] is False


def test_browser_council_prepares_allowlisted_services_without_send(tmp_path):
    payload = prepare_browser_council(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        prompt="compara el plan",
        env={},
    )

    assert payload["schema"] == "wabi.browser_council.v0_1"
    assert payload["prepared_count"] >= 16
    assert payload["online_ai_called"] is False
    assert payload["gate"] == "REVIEW"
    assert Path(payload["artifact"]).exists()
    assert len(payload["artifacts"]) == len(set(payload["artifacts"]))
    assert payload["ranking"]["schema"] == "wabi.browser_bridge_council_ranking.v0_2"
    assert payload["classifications"]["PREPARE_ONLY"] >= 15
    assert payload["classifications"]["READY_SEND_REVIEW"] >= 1


def test_cli_kimi_smoke_without_flags_does_not_send(tmp_path):
    runtime = tmp_path / "runtime"
    smoke_proc = run_cli(
        "browser-bridge",
        "smoke",
        "--service",
        "kimi",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )
    assert smoke_proc.returncode == 0, smoke_proc.stderr
    smoke = json.loads(smoke_proc.stdout)

    assert smoke["status"] == "KIMI_SEND_FLAGS_MISSING"
    assert smoke["online_ai_called"] is False
    assert smoke["browser_backend_called"] is False
    assert smoke["live_attempts"] == 0


def test_cli_council_prepare_only_no_live_attempts(tmp_path):
    runtime = tmp_path / "runtime"
    council_proc = run_cli(
        "browser-bridge",
        "council",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )
    assert council_proc.returncode == 0, council_proc.stderr
    council = json.loads(council_proc.stdout)

    assert council["live_attempts"] == 0
    assert council["online_ai_called"] is False
    assert council["classifications"]["PREPARE_ONLY"] >= 15


def test_council_ranks_services_without_sending_by_default():
    ranking = rank_browser_council_services(env={})

    assert ranking["online_ai_called"] is False
    assert ranking["recommended_service"] == "kimi"
    assert ranking["prepare_only_count"] >= 15


def test_code_response_to_proposal_valid_json(tmp_path):
    proposal = build_dry_run_cloud_code_proposal(intent="crear helper")
    payload = convert_browser_response_to_proposal(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        response_text="```json\n" + json.dumps(proposal) + "\n```",
    )

    assert payload["proposal_status"] == "VALIDATED"
    assert payload["auto_apply"] is False
    assert payload["task_spec_candidate"] is True


def test_code_response_blocks_delete_patch(tmp_path):
    proposal = build_dry_run_cloud_code_proposal(intent="delete")
    proposal["changes"] = [{"operation": "delete", "target": "README.md", "content": ""}]
    payload = convert_browser_response_to_proposal(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        response_text=json.dumps(proposal),
    )

    assert payload["proposal_status"] == "REJECTED_OUT_OF_SCOPE"
    assert payload["auto_apply"] is False


def test_code_response_blocks_out_of_scope_path(tmp_path):
    proposal = build_dry_run_cloud_code_proposal(intent="outside")
    proposal["changes"] = [{"operation": "write_text", "target": "C:/Users/L-Tyr/private.py", "suffix": ".py", "content": "x=1\n"}]
    payload = convert_browser_response_to_proposal(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        response_text=json.dumps(proposal),
    )

    assert payload["proposal_status"] == "REJECTED_OUT_OF_SCOPE"
    assert payload["patch_plan_created"] is False


def test_browser_bridge_cli_status_observe_and_ai_consult(tmp_path):
    runtime = tmp_path / "runtime"
    status_proc = run_cli("browser-bridge", "status", "--json", workspace=tmp_path, runtime=runtime)
    assert status_proc.returncode == 0, status_proc.stderr
    status = json.loads(status_proc.stdout)
    assert status["schema"] == "wabi.browser_bridge_status.v0_1"

    observe_proc = run_cli(
        "browser-bridge",
        "observe",
        "https://example.com/docs",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )
    assert observe_proc.returncode == 0, observe_proc.stderr
    observation = json.loads(observe_proc.stdout)
    assert observation["ok"] is True
    assert observation["browser_backend_called"] is False

    consult_proc = run_cli(
        "browser-bridge",
        "ai-consult",
        "kimi",
        "responde solo con propuesta estructurada",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )
    assert consult_proc.returncode == 0, consult_proc.stderr
    consultation = json.loads(consult_proc.stdout)
    assert consultation["gate"] == "REVIEW"
    assert consultation["online_ai_called"] is False

    send_proc = run_cli(
        "browser-bridge",
        "ai-consult",
        "kimi",
        "responde solo con propuesta estructurada",
        "--send",
        "--browser-backend",
        "kimi-webbridge",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
        extra_env={BROWSER_SEND_ENABLE_ENV: "1"},
    )
    assert send_proc.returncode == 0, send_proc.stderr
    send_payload = json.loads(send_proc.stdout)
    assert send_payload["gate"] == "REVIEW_SKIPPED"
    assert send_payload["online_ai_called"] is False

    council_proc = run_cli(
        "browser-bridge",
        "council",
        "compara este cambio",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )
    assert council_proc.returncode == 0, council_proc.stderr
    council = json.loads(council_proc.stdout)
    assert council["schema"] == "wabi.browser_council.v0_1"
    assert council["online_ai_called"] is False

    select_proc = run_cli(
        "browser-bridge",
        "select",
        "--service",
        "kimi",
        "--payload-class",
        "PUBLIC_PROMPT",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )
    assert select_proc.returncode == 0, select_proc.stderr
    selected = json.loads(select_proc.stdout)
    assert selected["decision"]["selected_service"] == "kimi"
    assert selected["decision"]["safe_to_send"] is False

    smoke_proc = run_cli(
        "browser-bridge",
        "smoke",
        "--service",
        "kimi",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )
    assert smoke_proc.returncode == 0, smoke_proc.stderr
    smoke = json.loads(smoke_proc.stdout)
    assert smoke["status"] == "KIMI_SEND_FLAGS_MISSING"
    assert smoke["online_ai_called"] is False

    snapshot_proc = run_cli(
        "browser-bridge",
        "snapshot",
        "--backend",
        "chrome-devtools-mcp",
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )
    assert snapshot_proc.returncode == 0, snapshot_proc.stderr
    snapshot = json.loads(snapshot_proc.stdout)
    assert snapshot["status"] == "DEVTOOLS_MCP_NOT_AVAILABLE"

    response_file = tmp_path / "response.json"
    response_file.write_text(json.dumps(build_dry_run_cloud_code_proposal(intent="crear helper")), encoding="utf-8")
    proposal_proc = run_cli(
        "browser-bridge",
        "proposal-from-response",
        "--input",
        str(response_file),
        "--json",
        workspace=tmp_path,
        runtime=runtime,
    )
    assert proposal_proc.returncode == 0, proposal_proc.stderr
    proposal_payload = json.loads(proposal_proc.stdout)
    assert proposal_payload["proposal_status"] == "VALIDATED"
    assert proposal_payload["auto_apply"] is False
