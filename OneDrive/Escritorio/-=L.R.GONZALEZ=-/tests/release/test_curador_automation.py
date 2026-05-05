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


def test_second_unchanged_run_is_noop_and_does_not_append_witness(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    downloads = tmp_path / "Downloads"
    downloads.mkdir(parents=True)
    workspace.mkdir()
    (workspace / "DELETED_OR_ARCHIVED.md").write_text("# DELETED_OR_ARCHIVED\n", encoding="utf-8")
    (downloads / "unique.txt").write_text("unique", encoding="utf-8")

    first = curador.run_curador(
        workspace_root=workspace,
        downloads_dir=downloads,
        recursive=True,
        write_index=True,
        write_fichas_flag=True,
        apply_exact_download_duplicates=True,
    )
    witness = Path(first["witness_log"])
    first_lines = witness.read_text(encoding="utf-8").splitlines()

    second = curador.run_curador(
        workspace_root=workspace,
        downloads_dir=downloads,
        recursive=True,
        write_index=True,
        write_fichas_flag=True,
        apply_exact_download_duplicates=True,
    )
    second_lines = witness.read_text(encoding="utf-8").splitlines()

    assert second["noop"] is True
    assert second["downloads_files_seen"] == 1
    assert second_lines == first_lines


def test_write_next_actions_uses_curador_and_pending_snapshot(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    downloads = tmp_path / "Downloads"
    downloads.mkdir(parents=True)
    workspace.mkdir()
    (workspace / "DELETED_OR_ARCHIVED.md").write_text("# DELETED_OR_ARCHIVED\n", encoding="utf-8")
    (downloads / "unique.txt").write_text("unique", encoding="utf-8")
    pending_dir = workspace / "qa_artifacts" / "pending"
    pending_dir.mkdir(parents=True)
    (pending_dir / "pending_review_latest.json").write_text(
        json.dumps(
            {
                "generated_at": "2026-05-05T00:00:00+00:00",
                "active_markdown": {
                    "dedup_open": 10,
                    "by_blocker": {"local_candidate": 4, "external_or_gated": 2},
                    "by_lane": {"cleanup_migration": 3},
                },
                "claudio_master": {"dedup_open": 2, "by_blocker": {"host_or_heavy": 1}},
            }
        ),
        encoding="utf-8",
    )

    curador.run_curador(
        workspace_root=workspace,
        downloads_dir=downloads,
        recursive=True,
        write_index=True,
        write_fichas_flag=True,
        apply_exact_download_duplicates=True,
    )
    payload = curador.write_next_actions_report(workspace, downloads)

    report = Path(payload["report_path"])
    data = Path(payload["json_path"])
    assert report.exists()
    assert data.exists()
    assert "Mantener CuradorSETO-Downloads-Intake activo" in report.read_text(encoding="utf-8")
    parsed = json.loads(data.read_text(encoding="utf-8"))
    assert parsed["status"]["current_downloads_files"] == 1
    assert parsed["pending"]["active_by_blocker"]["local_candidate"] == 4
    assert parsed["next_actions"][0]["priority"] == "P0"


def test_absorb_archives_unique_sources_and_writes_atlas(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    downloads = tmp_path / "Downloads"
    nested = downloads / "New folder"
    nested.mkdir(parents=True)
    workspace.mkdir()
    (workspace / "DELETED_OR_ARCHIVED.md").write_text("# DELETED_OR_ARCHIVED\n", encoding="utf-8")

    (downloads / "TUIP_SIGMA_R2_1_PRAGMATIC_CANON.md").write_text("# Sigma\nActionGate\nWitnessLog\n", encoding="utf-8")
    (nested / "claudio_local_code_agent.py").write_text("class RepoObserver:\n    pass\n", encoding="utf-8")
    (downloads / "desktop.ini").write_text("[.ShellClassInfo]\n", encoding="utf-8")

    result = curador.run_absorb(
        workspace_root=workspace,
        downloads_dir=downloads,
        recursive=True,
        write_index=True,
        write_fichas_flag=True,
        write_atlas=True,
        archive_absorbed=True,
        apply_safe_deletes=True,
    )

    assert result["downloads_files_seen"] == 3
    assert result["extractions"] == 2
    assert result["archived_sources"] == 2
    assert result["deleted_bytes"] > 0
    assert result["status_counts"]["ARCHIVO_FRIO"] == 2
    assert result["status_counts"]["BASURA_REGENERABLE_BORRADA"] == 1
    assert "REGISTRADO" not in result["status_counts"]
    assert not (downloads / "TUIP_SIGMA_R2_1_PRAGMATIC_CANON.md").exists()
    assert not (nested / "claudio_local_code_agent.py").exists()
    assert not (downloads / "desktop.ini").exists()
    assert not nested.exists()
    assert (workspace / "docs" / "intake" / "ATLAS_MAIN.md").exists()
    assert (workspace / "docs" / "canon" / "atlas" / "psi-observacionismo.md").exists()
    assert (workspace / "docs" / "canon" / "atlas" / "claudio-wabisabi.md").exists()

    with sqlite3.connect(result["db_path"]) as db:
        assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert db.execute("SELECT COUNT(*) FROM canon_nodes").fetchone()[0] >= 8
        assert db.execute("SELECT COUNT(*) FROM extractions").fetchone()[0] == 2
        assert db.execute("SELECT COUNT(*) FROM retirements").fetchone()[0] == 2
        assert db.execute("SELECT COUNT(*) FROM atlas_synapses").fetchone()[0] == 2


def test_absorb_keeps_secret_like_sources_blocked_in_inbox(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    downloads = tmp_path / "Downloads"
    downloads.mkdir(parents=True)
    workspace.mkdir()
    (workspace / "DELETED_OR_ARCHIVED.md").write_text("# DELETED_OR_ARCHIVED\n", encoding="utf-8")

    blocked = downloads / "token_notes.txt"
    blocked.write_text("do not move this source automatically", encoding="utf-8")

    result = curador.run_absorb(
        workspace_root=workspace,
        downloads_dir=downloads,
        recursive=True,
        write_index=True,
        write_fichas_flag=True,
        write_atlas=True,
        archive_absorbed=True,
        apply_safe_deletes=True,
    )

    assert blocked.exists()
    assert result["blocked_records"] == 1
    assert result["status_counts"] == {"BLOQUEADO": 1}
    with sqlite3.connect(result["db_path"]) as db:
        status = db.execute("SELECT status FROM files WHERE path = ?", (str(blocked),)).fetchone()[0]
        assert status == "BLOQUEADO"
        node = db.execute("SELECT canon_node_id FROM extractions").fetchone()[0]
        assert node == "privado-bloqueado"
