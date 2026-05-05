from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "release"))

import curador_automation as curador  # noqa: E402


def test_recursive_downloads_registers_new_folder_and_deletes_safe_duplicate(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    downloads = tmp_path / "Downloads"
    nested = downloads / "New folder"
    nested.mkdir(parents=True)
    workspace.mkdir()
    (workspace / "DELETED_OR_ARCHIVED.md").write_text("# DELETED_OR_ARCHIVED\n", encoding="utf-8")

    (downloads / "canon.txt").write_text("same", encoding="utf-8")
    (nested / "canon (1).txt").write_text("same", encoding="utf-8")
    (nested / "unique.txt").write_text("unique", encoding="utf-8")

    result = curador.run_curador(
        workspace_root=workspace,
        downloads_dir=downloads,
        recursive=True,
        write_index=True,
        write_fichas_flag=True,
        apply_exact_download_duplicates=True,
    )

    assert result["downloads_files_seen"] == 3
    assert result["new_folder_files_registered"] == 2
    assert result["duplicate_groups_detected"] == 1
    assert result["deleted_exact_duplicates"] == 1
    assert (downloads / "canon.txt").exists()
    assert not (nested / "canon (1).txt").exists()
    assert (nested / "unique.txt").exists()
    assert result["deleted"][0]["deleted"] is True
    assert (workspace / "docs" / "intake" / "CURADOR_MASTER_INDEX.md").exists()
    with sqlite3.connect(result["db_path"]) as db:
        assert db.execute("SELECT COUNT(*) FROM duplicate_groups").fetchone()[0] == 1
        assert db.execute("SELECT COUNT(*) FROM duplicates").fetchone()[0] == 2
        assert db.execute("SELECT COUNT(*) FROM fichas").fetchone()[0] == 3


def test_secret_like_duplicate_is_blocked(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    downloads = tmp_path / "Downloads"
    downloads.mkdir(parents=True)
    workspace.mkdir()
    (workspace / "DELETED_OR_ARCHIVED.md").write_text("# DELETED_OR_ARCHIVED\n", encoding="utf-8")

    (downloads / "secret.txt").write_text("same", encoding="utf-8")
    (downloads / "secret (1).txt").write_text("same", encoding="utf-8")

    result = curador.run_curador(
        workspace_root=workspace,
        downloads_dir=downloads,
        recursive=True,
        write_index=True,
        write_fichas_flag=True,
        apply_exact_download_duplicates=True,
    )

    assert result["duplicate_groups_detected"] == 1
    assert result["deleted_exact_duplicates"] == 0
    assert (downloads / "secret.txt").exists()
    assert (downloads / "secret (1).txt").exists()


def test_sqlite_index_and_export_are_valid(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    downloads = tmp_path / "Downloads"
    downloads.mkdir(parents=True)
    workspace.mkdir()
    (workspace / "DELETED_OR_ARCHIVED.md").write_text("# DELETED_OR_ARCHIVED\n", encoding="utf-8")
    (downloads / "duat_observacionismo.py").write_text("print('x')\n", encoding="utf-8")

    result = curador.run_curador(
        workspace_root=workspace,
        downloads_dir=downloads,
        recursive=True,
        write_index=True,
        write_fichas_flag=True,
        apply_exact_download_duplicates=False,
    )

    db_path = Path(result["db_path"])
    with sqlite3.connect(db_path) as db:
        assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert db.execute("SELECT COUNT(*) FROM files").fetchone()[0] == 1
        assert db.execute("SELECT COUNT(*) FROM fichas").fetchone()[0] == 1
        lane = db.execute("SELECT lane FROM files").fetchone()[0]
        assert lane == "duat-lab"
    export = json.loads((workspace / "runtime" / "curador_seto" / "source_intake_export.json").read_text(encoding="utf-8"))
    assert len(export["downloads_records"]) == 1


def test_witness_event_matches_seto_validator_hash_contract(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    downloads = tmp_path / "Downloads"
    downloads.mkdir(parents=True)
    workspace.mkdir()
    (workspace / "DELETED_OR_ARCHIVED.md").write_text("# DELETED_OR_ARCHIVED\n", encoding="utf-8")
    (downloads / "duat_observacionismo.py").write_text("print('x')\n", encoding="utf-8")

    curador.run_curador(
        workspace_root=workspace,
        downloads_dir=downloads,
        recursive=True,
        write_index=True,
        write_fichas_flag=True,
        apply_exact_download_duplicates=False,
    )

    witness = workspace / "qa_artifacts" / "witness_log" / "curador_seto_witnesslog.jsonl"
    event = json.loads(witness.read_text(encoding="utf-8").splitlines()[-1])
    expected = event.pop("event_hash")
    raw = json.dumps(event, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

    assert event["action_gate"] == "REVIEW"
    assert curador.hashlib.sha256(raw).hexdigest() == expected
