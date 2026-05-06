from pathlib import Path

from wabi_sabi.cli.main import execute_prompt


def test_programmer_agent_generates_safe_artifact(tmp_path):
    payload = execute_prompt(
        "crea una funcion que lea un archivo y resuma sus lineas",
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        json_mode=True,
    )

    assert payload["ok"] is True
    assert payload["agent"] == "programmer"
    artifact = Path(payload["artifacts"][0])
    assert artifact.exists()
    assert "summarize_file_lines" in artifact.read_text(encoding="utf-8")


def test_debug_agent_generates_diagnostic(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")

    payload = execute_prompt(
        "ejecuta diagnostico",
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        json_mode=True,
    )

    assert payload["ok"] is True
    assert payload["agent"] == "debugger"
    assert payload["artifacts"]
    assert Path(payload["artifacts"][0]).exists()


def test_action_gate_blocks_external_publish(tmp_path):
    payload = execute_prompt(
        "publica esto en github y usa mi token",
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        json_mode=True,
    )

    assert payload["ok"] is False
    assert payload["gate"] == "BLOCK"
    assert "secret_or_credential_boundary" in payload["gate_reasons"]


def test_file_agent_generates_readme_draft(tmp_path):
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")

    payload = execute_prompt(
        "crea un README para este modulo",
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        json_mode=True,
    )

    assert payload["ok"] is True
    assert payload["agent"] == "file"
    artifact = Path(payload["artifacts"][0])
    assert artifact.exists()
    assert "# Modulo Local" in artifact.read_text(encoding="utf-8")


def test_research_agent_searches_local_docs(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "ARCHITECTURE.md").write_text("Observacionismo local agent router evidence.", encoding="utf-8")

    payload = execute_prompt(
        "investiga observacionismo agent router",
        workspace=tmp_path,
        runtime_root=tmp_path / "runtime",
        json_mode=True,
    )

    assert payload["ok"] is True
    assert payload["agent"] == "researcher"
    artifact = Path(payload["artifacts"][0])
    assert artifact.exists()
    assert "ARCHITECTURE.md" in artifact.read_text(encoding="utf-8")
