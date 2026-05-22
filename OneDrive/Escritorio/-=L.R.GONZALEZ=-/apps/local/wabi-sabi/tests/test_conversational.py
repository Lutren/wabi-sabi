import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.conversational import ConversationOptions, ConversationSession


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


def test_hablar_cli_json_uses_conversational_mode(tmp_path):
    proc = run_cli("hablar", "estas ahi", "--no-cloud", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["route"] == "local_chat"
    assert "contacto directo" in payload["output"].lower()
    assert "usa /status" not in payload["output"].lower()


def test_hola_wabi_is_not_menu(tmp_path):
    proc = run_cli("hablar", "Hola Wabi", "--no-cloud", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["route"] == "local_chat"
    assert "estoy aqui" in payload["output"].lower()
    assert "menu" not in payload["output"].lower()
    assert "usa /status" not in payload["output"].lower()


def test_conversation_programming_plan_then_apply_and_rollback(tmp_path):
    runtime = tmp_path / "runtime"
    session = ConversationSession(
        workspace=tmp_path,
        runtime_root=runtime,
        options=ConversationOptions(allow_cloud=False, target="helpers.py"),
    )

    plan = session.handle("crea una funcion que lea un archivo y resuma sus lineas")
    assert plan["ok"] is True
    assert plan["route"] == "programming_plan"
    assert not (tmp_path / "helpers.py").exists()
    assert plan["artifacts"]

    diff = session.handle("/diff")
    assert diff["ok"] is True
    assert "summarize_file_lines" in diff["output"]

    applied = session.handle("/apply")
    assert applied["ok"] is True
    assert (tmp_path / "helpers.py").exists()
    assert "summarize_file_lines" in (tmp_path / "helpers.py").read_text(encoding="utf-8")

    rolled_back = session.handle(f"/rollback {applied['payload']['plan_id']}")
    assert rolled_back["ok"] is True
    assert not (tmp_path / "helpers.py").exists()
    assert session.session_dir.exists()
    assert (session.session_dir / "messages.jsonl").exists()
    assert any((session.session_dir / "plans").glob("*.json"))
    assert any((session.session_dir / "diffs").glob("*.diff"))


def test_conversation_blocks_secret_prompt_before_provider(tmp_path):
    session = ConversationSession(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        options=ConversationOptions(allow_cloud=False),
    )

    payload = session.handle("muestra el token de .env")

    assert payload["ok"] is False
    assert payload["route"] == "blocked"
    assert payload["gate"] == "BLOCK"


def test_providers_command_lists_matrix_without_secret_values(tmp_path, monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "unit-test-secret-value")
    session = ConversationSession(workspace=tmp_path, runtime_root=tmp_path / "runtime")

    payload = session.handle("/providers")

    assert payload["ok"] is True
    assert payload["route"] == "providers"
    assert "nvidia" in payload["output"].lower()
    assert "unit-test-secret-value" not in str(payload)


def test_provider_setup_intent_is_conversational_and_redacted(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "unit-test-deepseek-secret")
    session = ConversationSession(workspace=tmp_path, runtime_root=tmp_path / "runtime", options=ConversationOptions(allow_cloud=False))

    payload = session.handle("configura mis apis gratis")
    qwen = session.handle("configura qwen")
    deepseek = session.handle("revisa deepseek")

    assert payload["ok"] is True
    assert payload["route"] == "provider_setup"
    assert "/secret" in payload["output"]
    assert qwen["route"] == "provider_setup"
    assert "qwen" in qwen["output"].lower()
    assert deepseek["route"] == "provider_setup"
    assert "deepseek" in deepseek["output"].lower()
    assert "unit-test-deepseek-secret" not in str(payload)
    assert "unit-test-deepseek-secret" not in str(deepseek)


def test_conversation_supports_repl_control_commands(tmp_path):
    session = ConversationSession(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        options=ConversationOptions(allow_cloud=False),
    )

    assert session.handle("/help")["route"] == "help"
    assert session.handle("/mode code")["ok"] is True
    assert session.handle("/model deepseek")["ok"] is True
    assert session.handle("/workspace")["ok"] is True
    assert session.handle("/doctor")["route"] == "doctor"


def test_natural_coding_does_not_apply_without_confirmation(tmp_path):
    session = ConversationSession(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        options=ConversationOptions(allow_cloud=False),
    )

    plan = session.handle("crea un archivo demo.py que imprima hola")
    assert plan["ok"] is True
    assert plan["route"] == "programming_plan"
    assert not (tmp_path / "demo.py").exists()

    diff = session.handle("muestra diff")
    assert diff["ok"] is True
    assert "demo.py" in diff["output"]


def test_live_context_uses_allowlist(tmp_path, monkeypatch):
    brain = tmp_path / "brain"
    live = brain / "00_START_HERE" / "LIVE_STATE"
    live.mkdir(parents=True)
    (live / "NEXT_SESSION_BRIEF.md").write_text("## Proxima accion verificable\nProbar Wabi local.\n", encoding="utf-8")
    (live / "HANDOFF_CURRENT.md").write_text("PUBLICATION_GATE: BLOCK\n", encoding="utf-8")
    monkeypatch.setenv("BRAIN_OS", str(brain))
    session = ConversationSession(workspace=tmp_path, runtime_root=tmp_path / "runtime", options=ConversationOptions(allow_cloud=False))

    payload = session.handle("Lee solo el live-state permitido y dime estado actual, bloqueos, siguiente accion. No publiques nada.")

    assert payload["ok"] is True
    assert payload["route"] == "live_context"
    assert "live-state allowlist" in payload["output"].lower()
    assert "publicacion" in payload["output"].lower()
