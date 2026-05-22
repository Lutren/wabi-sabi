import json
import io
import os
import subprocess
import sys
import tarfile
from pathlib import Path

from wabi_sabi.core.cerebro_archive_intake import run_archive_intake


APP_ROOT = Path(__file__).resolve().parents[1]


def make_archive(workspace: Path) -> Path:
    source_dir = workspace / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-" / "-=PSI=-"
    source_dir.mkdir(parents=True)
    archive = source_dir / "sample.tar.gz"
    with tarfile.open(archive, "w:gz") as tf:
        _add_bytes(tf, "Duat-Geodia/app.py", b"def gate():\n    return 'ActionGate OSIT'\n")
        _add_bytes(tf, "Duat-Geodia/notes.md", b"R Phi_eff DUAT GEODIA\n")
        _add_bytes(tf, "Duat-Geodia/.git/config", b"[remote]\n")
        _add_bytes(tf, "Duat-Geodia/.env", b"SECRET=value\n")
        _add_bytes(tf, "../evil.txt", b"R should not extract\n")
    return archive


def _add_bytes(tf: tarfile.TarFile, name: str, data: bytes) -> None:
    info = tarfile.TarInfo(name)
    info.size = len(data)
    tf.addfile(info, fileobj=io.BytesIO(data))


def run_cli(*args, workspace: Path, runtime: Path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(APP_ROOT)
    return subprocess.run(
        [sys.executable, "-m", "wabi_sabi.cli.main", *args, "--workspace", str(workspace), "--runtime", str(runtime)],
        cwd=str(APP_ROOT),
        env=env,
        text=True,
        capture_output=True,
        timeout=45,
    )


def test_archive_intake_blocks_repo_metadata_secret_and_traversal(tmp_path):
    archive = make_archive(tmp_path)

    payload = run_archive_intake(tmp_path, archive_path=archive, output_root=tmp_path / "runtime" / "archive")

    assert payload["schema"] == "wabi.cerebro_archive_intake.v1"
    assert payload["ok"] is True
    assert payload["summary"]["text_indexed_count"] == 2
    counts = payload["summary"]["classification_counts"]
    assert counts["TEXT_INDEXABLE"] == 2
    assert counts["BLOCKED_METADATA_OR_CACHE"] == 1
    assert counts["SECRET_LIKE_BLOCK"] == 1
    assert counts["PATH_TRAVERSAL_BLOCK"] == 1
    assert all(Path(item["quarantine_text"]).exists() for item in payload["text_records"])
    assert (Path(payload["output_dir"]) / "ARCHIVE_INTAKE_REPORT.md").exists()


def test_archive_intake_cli_json(tmp_path):
    archive = make_archive(tmp_path)

    proc = run_cli("archive-intake", str(archive), "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["schema"] == "wabi.cerebro_archive_intake.v1"
    assert payload["summary"]["text_indexed_count"] == 2
    assert "manifest" not in payload
    assert payload["manifest_sample"]
