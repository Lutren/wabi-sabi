from __future__ import annotations

from pathlib import Path

from tools.release import humanize_source_archive


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_humanize_source_archive_moves_flat_files_by_function(tmp_path):
    root = tmp_path / "source_archive" / "downloads" / "2026-05-05"
    write(root / "AAA_observacionismo.txt", "psi")
    write(root / "BBB_claudio_agent.py", "print('agent')")
    write(root / "CCC_duat_pack.zip", "zip bytes")
    write(root / "DDD_1.png", "png bytes")

    result = humanize_source_archive.humanize_archive(root, write=True)

    assert result["moved"] == 4
    assert (root / "01_teoria_observacionismo_psi_osit" / "AAA_observacionismo.txt").exists()
    assert (root / "02_claudio_wabisabi_agentes" / "BBB_claudio_agent.py").exists()
    assert (root / "05_paquetes_zip_fuentes" / "CCC_duat_pack.zip").exists()
    assert (root / "06_imagenes_assets" / "DDD_1.png").exists()
    assert (root / "00_LEER_PRIMERO.md").exists()


def test_humanize_source_archive_is_idempotent(tmp_path):
    root = tmp_path / "archive"
    existing = root / "01_teoria_observacionismo_psi_osit" / "AAA_osit.txt"
    write(existing, "osit")

    result = humanize_source_archive.humanize_archive(root, write=True)

    assert result["moved"] == 0
    assert existing.exists()


def test_humanize_source_archive_absorbs_noncanonical_subfolders(tmp_path):
    root = tmp_path / "archive"
    nested = root / "New folder" / "AAA_psi_notes.txt"
    write(nested, "psi")

    result = humanize_source_archive.humanize_archive(root, write=True)

    assert result["moved"] == 1
    assert not (root / "New folder").exists()
    assert (root / "01_teoria_observacionismo_psi_osit" / "AAA_psi_notes.txt").exists()
