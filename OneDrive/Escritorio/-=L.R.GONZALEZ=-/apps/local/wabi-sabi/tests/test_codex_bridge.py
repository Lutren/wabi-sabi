from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from wabi_sabi.core.codex_bridge import (
    CodexCliAdapter,
    WabiCodexBridge,
    codex_status,
    extract_response_text,
)


def test_codex_status_prefers_cli_when_available():
    status = codex_status(codex_finder=lambda: "C:/tools/codex.cmd", env={})

    assert status["auto_provider"] == "codex-cli"
    assert status["codex_cli"]["available"] is True
    assert status["openai_responses"]["available"] is False


def test_codex_status_uses_openai_when_cli_missing_and_key_present():
    status = codex_status(codex_finder=lambda: None, env={"OPENAI_API_KEY": "test"})

    assert status["auto_provider"] == "openai-responses"
    assert status["openai_responses"]["model"] == "gpt-5.5"


def test_codex_bridge_dry_run_writes_workpack(tmp_path):
    bridge = WabiCodexBridge(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        codex_finder=lambda: None,
        env={},
    )

    result = bridge.ask("responde una prueba corta", dry_run=True)

    assert result.ok is True
    assert result.action == "codex_bridge_dry_run"
    assert result.artifacts
    payload = json.loads(Path(result.artifacts[0]).read_text(encoding="utf-8"))
    assert payload["schema"] == "wabi_codex_workpack.v1"
    assert "responde una prueba corta" in payload["prompt"]


def test_codex_bridge_blocks_external_prompt(tmp_path):
    bridge = WabiCodexBridge(
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        codex_finder=lambda: "codex.cmd",
        env={},
    )

    result = bridge.ask("publica esto en github")

    assert result.ok is False
    assert result.action == "blocked_by_action_gate"
    assert result.gate == "BLOCK"
    assert "external_publication_or_network_action" in result.evidence


def test_codex_cli_adapter_runs_read_only_and_reads_last_message(tmp_path):
    def fake_runner(command, **kwargs):
        output_file = Path(command[command.index("--output-last-message") + 1])
        output_file.write_text("WABI_CODEX_OK", encoding="utf-8")
        assert "--sandbox" in command
        assert "read-only" in command
        assert "--ask-for-approval" in command
        assert "never" in command
        assert command.index("--ask-for-approval") < command.index("exec")
        assert "--ephemeral" in command
        assert isinstance(kwargs["input"], bytes)
        assert "Origen: Wabi-Sabi local." in kwargs["input"].decode("utf-8")
        return SimpleNamespace(returncode=0, stdout=b"", stderr=b"")

    adapter = CodexCliAdapter(
        codex_command="codex.cmd",
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        runner=fake_runner,
    )

    result = adapter.execute("di ok", timeout=10)

    assert result.ok is True
    assert result.output == "WABI_CODEX_OK"
    assert "codex_exec_sandbox=read-only" in result.evidence
    assert "codex_session=ephemeral" in result.evidence


def test_extract_response_text_supports_output_text_and_content_items():
    assert extract_response_text({"output_text": "hola"}) == "hola"
    payload = {
        "output": [
            {"content": [{"type": "output_text", "text": "uno"}, {"type": "output_text", "text": "dos"}]}
        ]
    }

    assert extract_response_text(payload) == "uno\ndos"
