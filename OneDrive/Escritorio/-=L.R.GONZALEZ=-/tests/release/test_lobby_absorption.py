from __future__ import annotations

import json
from pathlib import Path

from tools.release import lobby_absorption


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def test_lobby_absorption_archives_sources_and_keeps_readme(tmp_path, monkeypatch):
    lobby = tmp_path / "Lobby de Alejandria"
    lobby.mkdir()
    write(lobby / "README_LOBBY_DE_ALEJANDRIA.md", "# Lobby\n")
    write(
        lobby / "Actua como AGENTE MATRIX BIBLIOTECA.txt",
        "MISION: disenar Matrix/Biblioteca.\nActionGate\nWitnessLog\n",
    )
    write(
        lobby / "Actua como AGENTE MEDIOEVO RPG TOOL.txt",
        "MISION: fixture RPG privada.\nRESTRICCIONES: no publicar material privado.\n",
    )

    fake_root = tmp_path / "workspace"
    monkeypatch.setattr(lobby_absorption, "ROOT", fake_root)

    exit_code = lobby_absorption.main(
        [
            "--root",
            str(lobby),
            "--name",
            "fixture_lobby_absorption",
            "--archive-absorbed",
            "--json",
        ]
    )

    assert exit_code == 0
    assert (lobby / "README_LOBBY_DE_ALEJANDRIA.md").exists()
    assert not (lobby / "Actua como AGENTE MATRIX BIBLIOTECA.txt").exists()
    assert not (lobby / "Actua como AGENTE MEDIOEVO RPG TOOL.txt").exists()

    manifest = fake_root / "docs" / "intake" / "fixture_lobby_absorption_MANIFEST.json"
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["summary"]["files"] == 3
    assert payload["summary"]["archived"] == 2
    assert payload["summary"]["kept_in_lobby"] == 1
    lanes = {record["filename"]: record["lane"] for record in payload["records"]}
    assert lanes["Actua como AGENTE MATRIX BIBLIOTECA.txt"] == "Matrix/Biblioteca"
    assert lanes["Actua como AGENTE MEDIOEVO RPG TOOL.txt"] == "Privado RPG/TCG"


def test_lobby_absorption_reads_all_lines(tmp_path, monkeypatch):
    lobby = tmp_path / "Lobby"
    lobby.mkdir()
    write(lobby / "README_LOBBY_DE_ALEJANDRIA.md", "# Lobby\n")
    write(lobby / "Kernel inicial del reto 1 OSIT-QG v.txt", "\n".join(f"line {i} OSIT" for i in range(25)))
    fake_root = tmp_path / "workspace"
    monkeypatch.setattr(lobby_absorption, "ROOT", fake_root)

    lobby_absorption.main(["--root", str(lobby), "--name", "line_read_check", "--json"])

    manifest = fake_root / "docs" / "intake" / "line_read_check_MANIFEST.json"
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["summary"]["total_lines_read"] == 26
    record = next(item for item in payload["records"] if item["filename"].startswith("Kernel"))
    assert record["line_count"] == 25
    assert record["lane"] == "Wabi-Sabi/OSIT"
