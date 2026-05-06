from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


CATEGORY_ORDER = {
    "01_teoria_observacionismo_psi_osit": "Teoria Observacionismo / PSI / OSIT",
    "02_claudio_wabisabi_agentes": "Claudio / Wabi-Sabi / agentes",
    "03_duat_geodia_sensorium": "DUAT / GEODIA / Sensorium",
    "04_codigo_scripts_labs": "Codigo, scripts y labs",
    "05_paquetes_zip_fuentes": "Paquetes comprimidos y fuentes",
    "06_imagenes_assets": "Imagenes y assets",
    "07_datasets_resultados": "Datasets y resultados",
    "08_documentos_pdf_docx": "Documentos PDF/DOCX",
    "09_ui_html": "Interfaces HTML/UI",
    "10_publicacion_productos": "Publicacion, productos y venta",
    "90_revision_privado_riesgo": "Revision privada o riesgo",
    "99_revision_misc": "Revision miscelanea",
}

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"}
PACKAGE_SUFFIXES = {".zip", ".7z", ".rar", ".tar", ".gz"}
DATA_SUFFIXES = {".csv", ".json", ".jsonl", ".sqlite", ".db"}
DOC_SUFFIXES = {".pdf", ".docx", ".doc", ".pptx", ".xlsx", ".xls"}
CODE_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css"}


@dataclass
class ArchiveMove:
    source: str
    destination: str
    sha256: str
    size_bytes: int
    category: str
    reason: str
    moved: bool


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def norm_name(path: Path) -> str:
    return path.name.encode("ascii", "ignore").decode("ascii").lower()


def category_for(path: Path) -> tuple[str, str]:
    name = norm_name(path)
    suffix = path.suffix.lower()
    if any(token in name for token in ["private", "privado", "rpg", "tcg", "secret", "credential"]):
        return "90_revision_privado_riesgo", "private_or_sensitive_marker"
    if any(token in name for token in ["gumroad", "github", "sponsor", "linkedin", "release", "publicacion", "producto"]):
        return "10_publicacion_productos", "publication_or_product_marker"
    if suffix in IMAGE_SUFFIXES:
        return "06_imagenes_assets", "image_suffix"
    if suffix in PACKAGE_SUFFIXES:
        return "05_paquetes_zip_fuentes", "package_suffix"
    if any(token in name for token in ["duat", "geodia", "sensorium", "living_matrix"]):
        return "03_duat_geodia_sensorium", "duat_geodia_marker"
    if any(token in name for token in ["claudio", "wabi", "nollm", "agent", "agente", "qwen", "router"]):
        return "02_claudio_wabisabi_agentes", "claudio_agent_marker"
    if any(token in name for token in ["observacionismo", "osit", "tuip", "psi", "sigma", "chi"]):
        return "01_teoria_observacionismo_psi_osit", "theory_marker"
    if suffix in DATA_SUFFIXES:
        return "07_datasets_resultados", "data_suffix"
    if suffix == ".html":
        return "09_ui_html", "html_suffix"
    if suffix in CODE_SUFFIXES:
        return "04_codigo_scripts_labs", "code_suffix"
    if suffix in DOC_SUFFIXES:
        return "08_documentos_pdf_docx", "document_suffix"
    if suffix in {".txt", ".md"}:
        return "99_revision_misc", "text_without_strong_marker"
    return "99_revision_misc", "fallback_review"


def iter_archive_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.name == "00_LEER_PRIMERO.md":
            continue
        files.append(path)
    return sorted(files, key=lambda item: str(item).lower())


def safe_destination(root: Path, category: str, filename: str) -> Path:
    folder = root / category
    destination = folder / filename
    if not destination.exists():
        return destination
    stem = destination.stem
    suffix = destination.suffix
    index = 2
    while True:
        candidate = folder / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def humanize_archive(root: Path, write: bool) -> dict[str, object]:
    root = root.resolve()
    moves: list[ArchiveMove] = []
    for source in iter_archive_files(root):
        category, reason = category_for(source)
        destination = root / category / source.name
        moved = False
        source_hash = sha256_file(source)
        if source.resolve() != destination.resolve():
            destination = safe_destination(root, category, source.name)
            if write:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(destination))
                if sha256_file(destination) != source_hash:
                    raise RuntimeError(f"hash_mismatch_after_move: {destination}")
            moved = True
        moves.append(
            ArchiveMove(
                source=str(source),
                destination=str(destination),
                sha256=source_hash,
                size_bytes=destination.stat().st_size if destination.exists() else source.stat().st_size,
                category=category,
                reason=reason,
                moved=moved,
            )
        )

    if write:
        write_index(root, moves)
        prune_empty_noncanonical_dirs(root)
    return {
        "archive_root": str(root),
        "files": len(moves),
        "moved": sum(1 for move in moves if move.moved),
        "categories": category_counts(moves),
        "write": write,
    }


def prune_empty_noncanonical_dirs(root: Path) -> None:
    canonical_dirs = set(CATEGORY_ORDER)
    for path in sorted([item for item in root.rglob("*") if item.is_dir()], key=lambda item: len(item.parts), reverse=True):
        if path == root:
            continue
        rel = path.relative_to(root)
        if len(rel.parts) == 1 and rel.parts[0] in canonical_dirs:
            continue
        try:
            path.rmdir()
        except OSError:
            pass


def category_counts(moves: list[ArchiveMove]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for move in moves:
        counts[move.category] = counts.get(move.category, 0) + 1
    return dict(sorted(counts.items()))


def write_index(root: Path, moves: list[ArchiveMove]) -> None:
    lines = [
        "# Leer Primero - Archivo Frio",
        "",
        "Este directorio ya no debe leerse como una carpeta plana.",
        "",
        "Regla humana:",
        "- Abrir primero este archivo.",
        "- Entrar por la carpeta funcional.",
        "- Usar el hash solo para auditoria.",
        "- No editar fuentes archivadas.",
        "- Volver al manifiesto o ficha cuando haya duda.",
        "",
        "## Carpetas",
        "",
        "| carpeta | funcion | archivos |",
        "|---|---|---:|",
    ]
    counts = category_counts(moves)
    for category, label in CATEGORY_ORDER.items():
        if category in counts:
            lines.append(f"| `{category}` | {label} | {counts[category]} |")
    lines.extend(["", "## Archivos", "", "| archivo | carpeta | sha256 | razon |", "|---|---|---|---|"])
    for move in sorted(moves, key=lambda item: (item.category, Path(item.destination).name.lower())):
        lines.append(
            f"| `{Path(move.destination).name}` | `{move.category}` | `{move.sha256[:16]}` | `{move.reason}` |"
        )
    (root / "00_LEER_PRIMERO.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Organize a source_archive date folder for human navigation.")
    parser.add_argument("--archive-root", required=True, help="Archive date folder to organize.")
    parser.add_argument("--write", action="store_true", help="Apply moves and write 00_LEER_PRIMERO.md.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = parse_args(argv)
    result = humanize_archive(Path(args.archive_root), args.write)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"archive_root: {result['archive_root']}")
        print(f"files: {result['files']}")
        print(f"moved: {result['moved']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
