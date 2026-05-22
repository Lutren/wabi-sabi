import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.cli import main as cli_main


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


def test_cli_e2e_smoke_logs_and_routes(tmp_path):
    proc = run_cli("e2e-smoke", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["intent"] == "code_generation"
    assert payload["agent"] == "programmer"
    assert payload["artifacts"]
    assert Path(payload["log"]).exists()


def test_cli_agents_command(tmp_path):
    proc = run_cli("agents", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert "programmer" in payload["agents"]
    assert "debugger" in payload["agents"]


def test_cli_apply_programs_python_file(tmp_path):
    proc = run_cli(
        "crea una funcion que lea un archivo y resuma sus lineas",
        "--apply",
        "--target",
        "helpers.py",
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["action"] == "scoped_code_patch_applied"
    assert (tmp_path / "helpers.py").exists()
    assert "summarize_file_lines" in (tmp_path / "helpers.py").read_text(encoding="utf-8")


def test_cli_codex_status_and_dry_run(tmp_path):
    status_proc = run_cli("codex-status", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert status_proc.returncode == 0, status_proc.stderr
    status = json.loads(status_proc.stdout)
    assert "auto_provider" in status
    assert "safe_default" in status

    dry_proc = run_cli(
        "codex",
        "responde una prueba corta",
        "--dry-run",
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
    )

    assert dry_proc.returncode == 0, dry_proc.stderr
    payload = json.loads(dry_proc.stdout)
    assert payload["action"] == "codex_bridge_dry_run"
    assert payload["artifacts"]


def test_cli_provider_status_includes_cloud_adapters_without_secret_values(tmp_path, monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "nvapi-test-secret-1234567890")
    monkeypatch.setenv("WABI_NVIDIA_NIM_MODEL_ALIAS", "ultra")
    proc = run_cli("provider-status", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    text = json.dumps(payload)
    assert "cloud" in payload
    assert "nvidia-nim" in payload["cloud"]
    assert payload["cloud"]["nvidia-nim"]["configured"] is True
    assert payload["cloud"]["nvidia-nim"]["model"] == "nvidia/llama-3.1-nemotron-ultra-253b-v1"
    assert {profile["alias"] for profile in payload["cloud"]["nvidia-nim"]["model_catalog"]} >= {
        "ultra",
        "super",
        "nano-30b",
    }
    assert "nvapi-test-secret" not in text


def test_cli_multimodal_status_is_local_and_secret_safe(tmp_path):
    proc = run_cli("multimodal", "status", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    text = json.dumps(payload)
    assert payload["action"] == "multimodal_status"
    assert payload["mode"] == "LOCAL_OPEN_SOURCE"
    assert payload["cloud"]["raw_media_to_cloud_allowed"] is False
    assert payload["secret_values_printed"] is False
    assert "test-secret" not in text


def test_cli_multimodal_cloud_request_stays_review_and_no_call(tmp_path):
    proc = run_cli("multimodal", "observe", "--cloud", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["action"] == "multimodal_cloud_request"
    assert payload["gate"] == "REVIEW"
    assert payload["cloud_provider_called"] is False
    assert payload["secret_values_printed"] is False


def test_cli_doctor_providers_repair_and_debug_are_sanitized(tmp_path, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic-unit-secret")
    monkeypatch.setenv("GEMINI_API_KEY", "gemini-unit-secret")

    providers = run_cli("providers", "--dry-run", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")
    assert providers.returncode == 0, providers.stderr
    provider_payload = json.loads(providers.stdout)
    provider_text = json.dumps(provider_payload)
    assert provider_payload["secret_values_printed"] is False
    assert {row["provider"] for row in provider_payload["providers"]} >= {
        "anthropic",
        "gemini",
        "local/ollama",
        "qwen",
        "dashscope_qwen",
        "deepseek",
        "openrouter",
    }
    assert all("base_url" in row for row in provider_payload["providers"])
    assert "anthropic-unit-secret" not in provider_text
    assert "gemini-unit-secret" not in provider_text

    doctor = run_cli("doctor", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")
    assert doctor.returncode in {0, 2}, doctor.stderr
    doctor_payload = json.loads(doctor.stdout)
    assert "wabi_root" in doctor_payload
    assert doctor_payload["secret_values_printed"] is False

    repair = run_cli("repair", "--dry-run", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")
    assert repair.returncode == 0, repair.stderr
    repair_payload = json.loads(repair.stdout)
    assert repair_payload["dry_run"] is True
    assert repair_payload["secret_values_printed"] is False

    debug = run_cli("debug", "--dry-run", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")
    assert debug.returncode == 0, debug.stderr
    debug_payload = json.loads(debug.stdout)
    assert debug_payload["dry_run"] is True
    assert debug_payload["secret_values_printed"] is False


def test_cli_chat_uses_conversation_route(tmp_path):
    proc = run_cli("chat", "estas ahi", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["route"] == "local_chat"
    assert "contacto directo" in payload["output"].lower()


def test_cli_once_uses_conversation_route(tmp_path):
    proc = run_cli("--once", "Hola Wabi", "--no-cloud", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["route"] == "local_chat"
    assert "estoy aqui" in payload["output"].lower()


def test_cli_auto_routes_local_and_dry_run(tmp_path):
    local_proc = run_cli(
        "auto",
        "ejecuta diagnostico",
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
    )

    assert local_proc.returncode == 0, local_proc.stderr
    local_payload = json.loads(local_proc.stdout)
    assert local_payload["route"] == "local_agent"
    assert local_payload["payload"]["agent"] == "debugger"

    dry_proc = run_cli(
        "auto",
        "analiza el repo y decide que conviene usar",
        "--dry-run",
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
    )

    assert dry_proc.returncode == 0, dry_proc.stderr
    dry_payload = json.loads(dry_proc.stdout)
    assert dry_payload["route"] == "codex_dry_run"
    assert dry_payload["artifacts"]


def test_execute_auto_prompt_can_queue_codex_background(tmp_path, monkeypatch):
    def fake_submit_orchestrator_job(**kwargs):
        return {
            "job_id": "job-fast",
            "job_file": str(tmp_path / "runtime" / "jobs" / "job-fast.json"),
            "prompt": kwargs["prompt"],
            "status": "running",
        }

    monkeypatch.setattr(cli_main, "submit_orchestrator_job", fake_submit_orchestrator_job)

    payload = cli_main.execute_auto_prompt(
        "analiza el repo y decide que conviene usar",
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        background_codex=True,
    )

    assert payload["ok"] is True
    assert payload["route"] == "codex_background"
    assert "job-fast" in payload["output"]


def test_execute_auto_prompt_returns_blueprint_brief_before_background_codex(tmp_path, monkeypatch):
    def fake_submit_orchestrator_job(**kwargs):
        return {
            "job_id": "job-release",
            "job_file": str(tmp_path / "runtime" / "jobs" / "job-release.json"),
            "prompt": kwargs["prompt"],
            "status": "running",
        }

    monkeypatch.setattr(cli_main, "submit_orchestrator_job", fake_submit_orchestrator_job)

    payload = cli_main.execute_auto_prompt(
        "sacame algo de tech que pueda liberar hoy por redes y que sea solucion a algun problema actual",
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        background_codex=True,
    )

    assert payload["ok"] is True
    assert payload["route"] == "hybrid_codex_background"
    assert "ActionGate Lite" in payload["output"]
    assert "job-release" in payload["output"]


def test_execute_auto_prompt_uses_local_memory_for_followup(tmp_path, monkeypatch):
    def fake_submit_orchestrator_job(**kwargs):
        return {
            "job_id": "job-release",
            "job_file": str(tmp_path / "runtime" / "jobs" / "job-release.json"),
            "prompt": kwargs["prompt"],
            "status": "running",
        }

    monkeypatch.setattr(cli_main, "submit_orchestrator_job", fake_submit_orchestrator_job)
    runtime = tmp_path / "runtime"

    first = cli_main.execute_auto_prompt(
        "sacame algo de tech que pueda liberar hoy por redes y que sea solucion a algun problema actual",
        workspace=tmp_path,
        runtime_root=runtime,
        background_codex=True,
    )
    second = cli_main.execute_auto_prompt(
        "aplicalo",
        workspace=tmp_path,
        runtime_root=runtime,
        background_codex=True,
    )

    assert first["route"] == "hybrid_codex_background"
    assert second["route"] == "local_chat"
    assert "Sigo con lo anterior" in second["output"]
    assert "ActionGate Lite" in second["output"]
