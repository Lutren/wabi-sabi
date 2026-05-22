import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.cerebro_index import build_cerebro_navigation, write_cerebro_navigation_docs


APP_ROOT = Path(__file__).resolve().parents[1]


def make_workspace(root: Path) -> None:
    cerebro = root / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-"
    master = root / "MEDIOEVO_OBSERVACIONISMO_MASTER"
    productos = root / "PRODUCTOS_MEDIOEVO"
    cerebro.mkdir(parents=True)
    master.mkdir()
    productos.mkdir()
    (cerebro / "00_LEER_PRIMERO_HUMANO.md").write_text("# Leer primero\n", encoding="utf-8")
    (master / "00_README_MASTER.md").write_text("# Master\n", encoding="utf-8")
    (master / "SOURCE_MANIFEST.json").write_text(
        json.dumps(
            {
                "schema": "medioevo.source_manifest.v1",
                "source_count": 3,
                "by_category": {"CANON_CURADO": 2, "CODIGO_CONFIG_MODULO": 1},
                "records": [],
            }
        ),
        encoding="utf-8",
    )
    (productos / "00_LEER_PRIMERO.md").write_text("# Productos\n", encoding="utf-8")


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
        timeout=45,
    )


def test_build_cerebro_navigation_is_dry_run(tmp_path):
    make_workspace(tmp_path)

    payload = build_cerebro_navigation(tmp_path)

    assert payload["schema"] == "wabi.cerebro_navigation.v1"
    assert payload["ok"] is True
    assert payload["source_summary"]["source_count"] == 3
    assert payload["artifact_status"]["missing_docs"]
    assert not (tmp_path / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-" / "00_BIBLIOTECA_HUMANA").exists()


def test_write_cerebro_navigation_docs_creates_human_library_and_bridges(tmp_path):
    make_workspace(tmp_path)
    payload = build_cerebro_navigation(tmp_path)

    artifacts = write_cerebro_navigation_docs(payload)
    biblioteca = tmp_path / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-" / "00_BIBLIOTECA_HUMANA"

    assert len(artifacts) >= 10
    assert (biblioteca / "README.md").exists()
    assert (biblioteca / "RUTA_5_MINUTOS.md").exists()
    assert (biblioteca / "CEREBRO_NAVIGATION_MANIFEST.json").exists()
    assert "Biblioteca humana principal" in (
        tmp_path / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-" / "00_LEER_PRIMERO_HUMANO.md"
    ).read_text(encoding="utf-8")
    assert "mapa canonico" in (tmp_path / "PRODUCTOS_MEDIOEVO" / "PRODUCT_MAP.md").read_text(encoding="utf-8")
    assert (tmp_path / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-" / "_MANIFIESTOS" / "AGENTE_ULTIMO_PROCESAMIENTO_CEREBRO.json").exists()


def test_cerebro_index_cli_json_and_write_docs(tmp_path):
    make_workspace(tmp_path)

    dry = run_cli("cerebro-index", "--json", workspace=tmp_path, runtime=tmp_path / "runtime")
    assert dry.returncode == 0, dry.stderr
    dry_payload = json.loads(dry.stdout)
    assert dry_payload["action"] == "cerebro_index_dry_run"
    assert dry_payload["artifacts"] == []

    write = run_cli(
        "cerebro-index",
        "--write-docs",
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
    )
    assert write.returncode == 0, write.stderr
    payload = json.loads(write.stdout)
    assert payload["action"] == "cerebro_index_docs_written"
    assert payload["artifacts"]
    assert (tmp_path / "-=MEDIOEVO=-" / "-=LIBROS" / "-=CEREBRO=-" / "00_BIBLIOTECA_HUMANA" / "README.md").exists()
