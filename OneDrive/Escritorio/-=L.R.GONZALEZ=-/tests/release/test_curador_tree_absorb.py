from pathlib import Path

from tools.release import curador_tree_absorb as curador


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_choose_canonical_prefers_non_archive(tmp_path: Path) -> None:
    canonical = tmp_path / "canon" / "core.md"
    archived = tmp_path / "archive" / "core.md"
    write(canonical, "same")
    write(archived, "same")

    assert curador.choose_canonical([archived, canonical]) == canonical


def test_duplicate_archive_copy_is_safe_delete_candidate(tmp_path: Path) -> None:
    root = tmp_path / "PSI"
    write(root / "core.md", "# Core\n")
    write(root / "archive" / "core.md", "# Core\n")

    records = curador.build_records([("psi", root)])
    archive_record = next(record for record in records if "archive" in record.rel_path)

    assert archive_record.decision == "DELETE_EXACT_DUPLICATE_AFTER_HASH"
    assert archive_record.safe_delete_candidate is True
    assert archive_record.action_gate == "APPROVE"


def test_secret_like_duplicate_is_blocked_not_deleted(tmp_path: Path) -> None:
    root = tmp_path / "researchs"
    write(root / "token_notes.txt", "same")
    write(root / "archive" / "token_notes.txt", "same")

    records = curador.build_records([("researchs", root)])

    assert all(record.action_gate == "BLOCK" for record in records)
    assert not any(record.safe_delete_candidate for record in records)


def test_download_executable_is_blocked_before_absorption(tmp_path: Path) -> None:
    root = tmp_path / "Downloads"
    write(root / "tool.exe", "not really binary")

    records = curador.build_records([("downloads", root)])

    assert records[0].status == "BLOQUEADO_AMENAZA_DOWNLOAD"
    assert records[0].decision == "BLOCK_DOWNLOAD_EXECUTION_BEFORE_THREAT_ANALYSIS"
    assert records[0].action_gate == "BLOCK"
    assert records[0].safe_delete_candidate is False


def test_hash_limit_defers_large_file_without_delete_candidate(tmp_path: Path) -> None:
    root = tmp_path / "home"
    path = root / "large.bin"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"x" * 128)

    records = curador.build_records([("home", root)], hash_limit_bytes=16)

    assert records[0].sha256.startswith("UNHASHED_OVER_LIMIT:")
    assert "LARGE_FILE_HASH_DEFERRED" in records[0].risk_flags
    assert records[0].safe_delete_candidate is False
