import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.conversational import ConversationOptions, ConversationSession
from wabi_sabi.core.functional_status import build_functional_status


APP_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args, workspace: Path, runtime: Path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(APP_ROOT)
    env["MEDIOEVO_NO_MODEL_MODE"] = "1"
    env.pop("WABI_ALLOW_CLOUD_PROVIDERS", None)
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


def test_hablar_status_defaults_to_local_no_cloud(tmp_path):
    proc = run_cli("hablar", "/status", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["route"] == "status"
    assert "cloud: bloqueado por defecto" in payload["output"].lower()
    assert "motor modular: disponible" in payload["output"].lower()


def test_hablar_cloud_flag_is_explicit_opt_in(tmp_path):
    proc = run_cli("hablar", "/status", "--cloud", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["route"] == "status"
    assert "cloud: opt-in activo" in payload["output"].lower()


def test_no_cloud_keeps_local_model_eligible(tmp_path, monkeypatch):
    monkeypatch.delenv("MEDIOEVO_NO_MODEL_MODE", raising=False)
    session = ConversationSession(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        options=ConversationOptions(allow_cloud=False),
    )
    status = {
        "auto_provider": "ollama",
        "codex": {"codex_cli": {"available": False}},
    }

    assert session._should_try_model_for_casual("resume este estado en una frase", status) is True


def test_functional_status_accepts_wabi_app_root_without_duplicate_path():
    payload = build_functional_status(APP_ROOT, APP_ROOT / "runtime")

    assert payload["wabi_root"] == str(APP_ROOT.resolve())
    assert payload["agents_can_program"]["status"] == "READY_LOCAL_SAFE_EXECUTOR"
    assert payload["local_engine"]["engine_manifest_ready"] is True
    assert payload["local_engine"]["module_count"] >= 1
    assert "programming_modules_missing" not in payload["blockers"]
