import json
import os
import subprocess
import sys
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args, workspace: Path, runtime: Path, input_text: str | None = None, env_overrides: dict[str, str] | None = None):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(APP_ROOT)
    env["MEDIOEVO_NO_MODEL_MODE"] = "1"
    if env_overrides:
        env.update(env_overrides)
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
        input=input_text,
        cwd=str(APP_ROOT),
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
    )


def test_wabi_without_args_enters_conversational_mode_and_exit(tmp_path):
    proc = run_cli(workspace=tmp_path, runtime=tmp_path / "runtime", input_text="/exit\n")

    assert proc.returncode == 0, proc.stderr
    assert "Wabi-Sabi Conversational CLI" in proc.stdout
    assert "wabi>" in proc.stdout
    assert "cloud: proposal_only" in proc.stdout


def test_interactive_help_lists_new_commands(tmp_path):
    proc = run_cli(workspace=tmp_path, runtime=tmp_path / "runtime", input_text="/help\n/exit\n")

    assert proc.returncode == 0, proc.stderr
    assert "/graphics" in proc.stdout
    assert "/tasks" in proc.stdout
    assert "/code <texto>" in proc.stdout


def test_cli_once_still_works_and_is_redacted(tmp_path, monkeypatch):
    proc = run_cli(
        "--once",
        "hola wabi",
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
        env_overrides={"NVIDIA_API_KEY": "nvapi-test-secret-1234567890"},
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    text = json.dumps(payload)
    assert payload["schema"] == "wabi.conversation_turn.v0_1"
    assert payload["route"] == "local_chat"
    assert payload["intent_name"] == "chat_general"
    assert payload["status"] == "OK"
    assert payload["proposal_only"] is True
    assert payload["applied_to_sources"] is False
    assert payload["rollback_snapshot_required"] is True
    assert "proposal_only" in payload["tags"]
    assert payload["cloud_provider_called"] is False
    assert "nvapi-test-secret" not in text


def test_cli_once_code_request_returns_safe_proposal_contract(tmp_path):
    proc = run_cli(
        "--once",
        "programa un helper seguro para validar JSON y genera tests asociados",
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
        env_overrides={"WABI_LLM_PROVIDER_CLOUD_DEFAULT": "1"},
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["status"] == "OK"
    assert payload["intent_name"] == "code_request"
    assert payload["route"] == "code_plan"
    assert payload["proposal"]
    assert isinstance(payload["task_spec"], dict)
    assert isinstance(payload["patch_candidate"], dict)
    assert isinstance(payload["graphics_plan"], dict)
    assert payload["cloud_provider_called"] is False
    assert payload["applied_to_sources"] is False
    assert payload["rollback_snapshot_required"] is True
    assert payload["next_safe_action"]
    assert "LLM_proposal" in payload["tags"]
    assert "proposal_only" in payload["tags"]
    assert "vibe_coding" in payload["tags"]
    assert payload["metadata"]["category"] == "code"
    assert payload["metadata"]["interface_mode"] == "vibe_coding"
    assert payload["metadata"]["incremental"] is True


def test_existing_build_assist_status_command_still_works(tmp_path):
    proc = run_cli("build-assist-status", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["schema"] == "wabi.build_assist_cloud.v0_1"
    assert payload["authority"]["cloud_authority"] == "proposal_only"


def test_interactive_graphics_and_code_requests_do_not_apply(tmp_path):
    proc = run_cli(
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
        input_text=(
            "/status\n"
            "crea una escena de DUAT city con agentes y handoff\n"
            "programa un helper seguro para validar json\n"
            "/exit\n"
        ),
    )

    assert proc.returncode == 0, proc.stderr
    assert "GraphicsBridge preparado en modo plan-only" in proc.stdout
    assert "Tarea de programacion preparada" in proc.stdout
    assert "cloud_budget:" in proc.stdout
    assert "proposal_only=YES" in proc.stdout
    assert not list(tmp_path.glob("*.py"))


def test_interactive_providers_include_cloud_budget(tmp_path):
    proc = run_cli(
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
        input_text="/providers\n/exit\n",
    )

    assert proc.returncode == 0, proc.stderr
    assert "cloud_budget:" in proc.stdout
    assert "budget_gate:" in proc.stdout


def test_cli_local_apply_preview_uses_latest_taskspec_without_writing(tmp_path):
    workspace = tmp_path / "workspace"
    runtime = tmp_path / "runtime"
    (workspace / "wabi_sabi" / "core").mkdir(parents=True)
    (workspace / "tests").mkdir(parents=True)
    (workspace / "wabi_sabi" / "__init__.py").write_text("", encoding="utf-8")
    (workspace / "wabi_sabi" / "core" / "__init__.py").write_text("", encoding="utf-8")

    once = run_cli(
        "--once",
        "programa un helper seguro para validar json",
        "--json",
        workspace=workspace,
        runtime=runtime,
    )
    assert once.returncode == 0, once.stderr

    preview = run_cli("apply-local-preview", "--latest", "--json", workspace=workspace, runtime=runtime)
    payload = json.loads(preview.stdout)

    assert preview.returncode == 0, preview.stderr
    assert payload["status"] == "LOCAL_APPLY_PATCH_READY"
    assert payload["applied_to_sources"] is False
    assert payload["cloud_provider_called"] is False
    assert (workspace / "wabi_sabi" / "core" / "json_safety.py").exists() is False
