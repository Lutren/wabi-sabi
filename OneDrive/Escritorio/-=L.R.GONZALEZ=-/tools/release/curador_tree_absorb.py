from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
TODAY = datetime.now().date().isoformat()

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".py",
    ".json",
    ".csv",
    ".html",
    ".htm",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".css",
    ".yml",
    ".yaml",
    ".toml",
    ".obs",
    ".sample",
}
CODE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".obs", ".ps1", ".bat", ".sh"}
DOC_SUFFIXES = {".md", ".txt", ".docx", ".pdf"}
ARCHIVE_SUFFIXES = {".zip", ".rar", ".7z"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
GENERATED_SUFFIXES = {".pyc", ".tmp", ".temp", ".part", ".crdownload"}
GENERATED_NAMES = {"desktop.ini", "thumbs.db", ".ds_store"}
DOWNLOAD_BLOCK_SUFFIXES = {
    ".apk",
    ".bat",
    ".cmd",
    ".com",
    ".dll",
    ".exe",
    ".jar",
    ".lnk",
    ".msi",
    ".ps1",
    ".scr",
    ".sys",
    ".vbs",
}
DOWNLOAD_REVIEW_SUFFIXES = {".7z", ".docm", ".dmg", ".img", ".iso", ".pptm", ".rar", ".xlsm", ".zip"}
DEFAULT_EXCLUDED_DIRS = {
    ".aider",
    ".agents",
    ".android",
    ".android-sdk",
    ".aws",
    ".azure",
    ".cache",
    ".cargo",
    ".claude",
    ".claw",
    ".codex",
    ".config",
    ".copilot",
    ".credentials_local",
    ".cursor",
    ".docker",
    ".gemini",
    ".git",
    ".gradle",
    ".jdk",
    ".medioevo_gumroad_chrome_check",
    ".medioevo_gumroad_session_check",
    ".medioevo_gumroad_session_probe",
    ".medioevo_gumroad_session_probe_fix",
    ".mempalace",
    ".nodejs",
    ".ollama",
    ".openclaw",
    ".openclaw-claudio-safe",
    ".playwright_outlook_profile",
    ".pytest_cache",
    ".qwen",
    ".rustup",
    ".sbx-denybin",
    ".sentinel",
    ".ssh",
    ".venv",
    ".venv_api",
    ".wrangler",
    "__pycache__",
    "appdata",
    "application data",
    "cookies",
    "local settings",
    "nethood",
    "node_modules",
    "printhood",
    "recent",
    "sendto",
    "start menu",
    "templates",
}

ARCHIVE_MARKERS = {
    "archive",
    "_archivar",
    "_archive",
    "duplicados",
    "duplicate",
    "duplicates",
    "raiz_2026-04-26",
    "__pycache__",
}
SECRET_MARKERS = {"secret", "token", "credential", "apikey", "api_key", ".env", "private_key", "discord"}
PRIVATE_MARKERS = {"rpg", "tcg", "game_bridge", "metaevo", "private", "privado"}
CLAIM_MARKERS = {
    "antigrav",
    "antigravedad",
    "qg",
    "quantum",
    "fisica",
    "física",
    "diagnostico",
    "diagnóstico",
    "medical",
    "medico",
    "médico",
    "prediccion",
    "predicción",
}


@dataclass
class TreeRecord:
    source_label: str
    path: str
    rel_path: str
    sha256: str
    size_bytes: int
    suffix: str
    kind: str
    psi_state: str
    status: str
    classification: str
    lane: str
    decision: str
    action_gate: str
    risk_flags: list[str]
    target: str
    summary: str
    falsifiers: str
    canonical_path: str | None = None
    duplicate_count: int = 1
    safe_delete_candidate: bool = False
    deleted: bool = False


def configure_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def fingerprint_file(path: Path, hash_limit_bytes: int | None = None) -> str:
    size = path.stat().st_size
    if hash_limit_bytes is not None and size > hash_limit_bytes:
        marker = hashlib.sha256(str(path).encode("utf-8", errors="ignore")).hexdigest().upper()[:16]
        return f"UNHASHED_OVER_LIMIT:{size}:{path.stat().st_mtime_ns}:{marker}"
    return sha256_file(path)


def slugify(value: str, limit: int = 80) -> str:
    text = value.encode("ascii", "ignore").decode("ascii").lower()
    text = re.sub(r"[^a-z0-9._-]+", "-", text).strip("-._")
    return (text or "file")[:limit]


def path_parts_lower(path: Path) -> list[str]:
    return [part.lower() for part in path.parts]


def contains_marker(path: Path, markers: set[str]) -> bool:
    lowered = str(path).lower()
    return any(marker in lowered for marker in markers)


def is_archive_like(path: Path) -> bool:
    return any(part in ARCHIVE_MARKERS for part in path_parts_lower(path))


def is_generated_trash(path: Path) -> bool:
    return path.name.lower() in GENERATED_NAMES or path.suffix.lower() in GENERATED_SUFFIXES or "__pycache__" in path_parts_lower(path)


def has_copy_suffix(path: Path) -> bool:
    return bool(re.search(r"\s*\(\d+\)$", path.stem))


def is_low_semantic(path: Path) -> bool:
    name = path.name.lower()
    return (
        name.startswith("copy")
        or name.startswith("copia")
        or name.startswith("untitled")
        or name.startswith("pasted")
        or " - copy" in name
        or " copia" in name
        or has_copy_suffix(path)
    )


def kind_for(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in CODE_SUFFIXES:
        return "code_or_prototype"
    if suffix in {".md", ".txt"}:
        return "text_document"
    if suffix in {".docx", ".pdf"}:
        return "research_output"
    if suffix in ARCHIVE_SUFFIXES:
        return "archive_package"
    if suffix in IMAGE_SUFFIXES:
        return "asset"
    if suffix in {".json", ".csv", ".toml", ".yml", ".yaml"}:
        return "structured_data"
    if suffix == ".lnk":
        return "shortcut"
    if not suffix:
        return "extensionless"
    return "other"


def lane_for(path: Path) -> str:
    text = str(path).lower()
    if contains_marker(path, SECRET_MARKERS) or contains_marker(path, PRIVATE_MARKERS):
        return "privado-bloqueado"
    if "geodia" in text or "duat" in text:
        return "duat-geodia"
    if "psi" in text or "observacion" in text or "osit" in text or "tuip" in text:
        return "psi-observacionismo"
    if "claudio" in text or "wabi" in text or "agent" in text or "agente" in text:
        return "claudio-wabisabi"
    if any(word in text for word in ("deploy", "cloudflare", "github", "gumroad", "linkedin", "public")):
        return "publicacion"
    if path.suffix.lower() in IMAGE_SUFFIXES:
        return "assets"
    if is_generated_trash(path):
        return "cleanup"
    return "curaduria"


def is_download_source(source_label: str, path: Path) -> bool:
    parts = path_parts_lower(path)
    return source_label.lower() in {"download", "downloads", "descargas"} or "downloads" in parts or "descargas" in parts


def risk_flags_for(path: Path, source_label: str = "") -> list[str]:
    flags: list[str] = []
    if contains_marker(path, SECRET_MARKERS):
        flags.append("SECRET_OR_CREDENTIAL_MARKER")
    if contains_marker(path, PRIVATE_MARKERS):
        flags.append("PRIVATE_OR_GAME_MARKER")
    if contains_marker(path, CLAIM_MARKERS):
        flags.append("STRONG_CLAIM_REVIEW")
    if path.suffix.lower() in ARCHIVE_SUFFIXES:
        flags.append("ARCHIVE_PACKAGE")
    if path.suffix.lower() in {".docx", ".pdf"}:
        flags.append("GENERATED_RESEARCH_OUTPUT")
    if is_generated_trash(path):
        flags.append("REGENERABLE_TRASH")
    if is_download_source(source_label, path):
        flags.append("DOWNLOAD_INBOX")
        suffix = path.suffix.lower()
        if suffix in DOWNLOAD_BLOCK_SUFFIXES:
            flags.append("DOWNLOAD_EXECUTION_BLOCK")
        elif suffix in DOWNLOAD_REVIEW_SUFFIXES:
            flags.append("DOWNLOAD_THREAT_REVIEW")
        elif suffix in {".pdf", ".docx", ".txt", ".md"}:
            flags.append("DOWNLOAD_DOCUMENT_REVIEW")
    return flags


def psi_state_for(path: Path, flags: list[str]) -> str:
    if "SECRET_OR_CREDENTIAL_MARKER" in flags or "PRIVATE_OR_GAME_MARKER" in flags:
        return "BLOQUEADO"
    if "STRONG_CLAIM_REVIEW" in flags:
        return "BLOQUEADO"
    if path.name.startswith("00_") or "canon" in path_parts_lower(path) or path.name.lower().startswith("readme"):
        return "CERTEZA"
    return "INFERENCIA"


def target_for(lane: str, path: Path) -> str:
    if lane == "psi-observacionismo":
        return "Atlas/PSI-Observacionismo: canon, claims, falsadores y contratos operativos"
    if lane == "duat-geodia":
        return "Atlas/DUAT-GEODIA: interno privado/read-only/sintetico segun frontera"
    if lane == "claudio-wabisabi":
        return "Atlas/Claudio-Wabi-Sabi: runtime local, agentes, COMMS y policies"
    if lane == "publicacion":
        return "Atlas/Publicacion: gated, public-safe, sin accion externa"
    if lane == "assets":
        return "Atlas/Assets: ficha y licencia antes de uso"
    if lane == "privado-bloqueado":
        return "Atlas/Privado-Bloqueado: no publicar ni mover a open-dev"
    return "Atlas/Curaduria: revisar, absorber y retirar si procede"


def summarize_text(path: Path, max_bytes: int = 80_000) -> str:
    try:
        size = path.stat().st_size
    except OSError:
        return ""
    if path.suffix.lower() not in TEXT_SUFFIXES or size > max_bytes:
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    headings = [line.lstrip("# ").strip() for line in lines if line.startswith("#")][:3]
    if headings:
        return "; ".join(headings).strip()[:260]
    return " ".join(lines[:3]).strip()[:260]


def choose_canonical(paths: list[Path]) -> Path:
    def score(path: Path) -> tuple[int, int, int, int, int, str]:
        parts = path_parts_lower(path)
        archive_penalty = 1 if is_archive_like(path) else 0
        generated_penalty = 1 if is_generated_trash(path) else 0
        copy_penalty = 1 if is_low_semantic(path) else 0
        canon_bonus = 0 if any(part in {"canon", "libro"} for part in parts) or path.name[:3].isdigit() else 1
        depth = len(path.parts)
        return (generated_penalty, archive_penalty, copy_penalty, canon_bonus, depth, str(path).lower())

    return sorted(paths, key=score)[0]


def collect_files(root: Path, excluded_dirs: set[str] | None = None) -> list[Path]:
    files: list[Path] = []
    excluded_dirs = excluded_dirs or DEFAULT_EXCLUDED_DIRS
    for base, dirs, names in os.walk(root):
        base_path = Path(base)
        kept_dirs = []
        for dirname in dirs:
            child = base_path / dirname
            if dirname.lower() in excluded_dirs:
                continue
            if child.is_symlink():
                continue
            kept_dirs.append(dirname)
        dirs[:] = kept_dirs
        for name in names:
            path = base_path / name
            if path.is_file() and not path.is_symlink():
                files.append(path)
    return sorted(files, key=lambda p: str(p).lower())


def build_records(
    roots: list[tuple[str, Path]],
    hash_limit_bytes: int | None = None,
    excluded_dirs: set[str] | None = None,
) -> list[TreeRecord]:
    by_hash: dict[str, list[Path]] = {}
    file_meta: dict[Path, tuple[str, str, str]] = {}
    for label, root in roots:
        for path in collect_files(root, excluded_dirs=excluded_dirs):
            try:
                sha = fingerprint_file(path, hash_limit_bytes=hash_limit_bytes)
            except OSError:
                continue
            by_hash.setdefault(sha, []).append(path)
            file_meta[path] = (label, str(path.relative_to(root)), sha)

    canonical_by_hash = {sha: choose_canonical(paths) for sha, paths in by_hash.items()}
    records: list[TreeRecord] = []
    for path, (label, rel_path, sha) in file_meta.items():
        try:
            size_bytes = path.stat().st_size
        except OSError:
            continue
        flags = risk_flags_for(path, label)
        if sha.startswith("UNHASHED_OVER_LIMIT:"):
            flags.append("LARGE_FILE_HASH_DEFERRED")
        lane = lane_for(path)
        psi_state = psi_state_for(path, flags)
        canonical = canonical_by_hash[sha]
        duplicate_count = len(by_hash[sha])
        kind = kind_for(path)
        action_gate = "APPROVE"
        decision = "ABSORB_TO_ATLAS"
        status = "FICHADO"
        classification = "UNIQUE_SOURCE"
        safe_delete = False
        if duplicate_count > 1:
            classification = "DUPLICATE_EXACT"
            if path == canonical:
                decision = "KEEP_CANONICAL"
                status = "CANONICAL_DUPLICATE_KEEP"
            elif (
                not sha.startswith("UNHASHED_OVER_LIMIT:")
                and (is_archive_like(path) or is_low_semantic(path) or is_generated_trash(path))
            ) and not (
                "SECRET_OR_CREDENTIAL_MARKER" in flags or "PRIVATE_OR_GAME_MARKER" in flags
            ):
                decision = "DELETE_EXACT_DUPLICATE_AFTER_HASH"
                status = "DELETE_CANDIDATE"
                safe_delete = True
                action_gate = "APPROVE"
            else:
                decision = "REVIEW_DUPLICATE"
                status = "REVIEW"
                action_gate = "REVIEW"
        if is_generated_trash(path):
            classification = "REGENERABLE_TRASH"
            decision = "DELETE_REGENERABLE_AFTER_LOG"
            status = "DELETE_CANDIDATE"
            safe_delete = True
            action_gate = "APPROVE"
        if "SECRET_OR_CREDENTIAL_MARKER" in flags or "PRIVATE_OR_GAME_MARKER" in flags:
            decision = "BLOCK_KEEP_PRIVATE"
            status = "BLOQUEADO"
            action_gate = "BLOCK"
            safe_delete = False
        elif "DOWNLOAD_EXECUTION_BLOCK" in flags:
            decision = "BLOCK_DOWNLOAD_EXECUTION_BEFORE_THREAT_ANALYSIS"
            status = "BLOQUEADO_AMENAZA_DOWNLOAD"
            action_gate = "BLOCK"
            safe_delete = False
        elif "DOWNLOAD_THREAT_REVIEW" in flags:
            decision = "REVIEW_DOWNLOAD_BEFORE_EXTRACT_OR_EXECUTE"
            status = "REVIEW_AMENAZA_DOWNLOAD"
            action_gate = "REVIEW"
            safe_delete = False
        elif "STRONG_CLAIM_REVIEW" in flags and decision == "ABSORB_TO_ATLAS":
            decision = "ABSORB_AS_RESEARCH_BOUNDARY"
            status = "BLOQUEADO_PUBLICACION"
            action_gate = "REVIEW"
        summary = summarize_text(path) or f"{kind}; {path.name}; {size_bytes} bytes"
        falsifiers = "hash_mismatch; missing_canonical_copy; unverified_claim; secret_or_private_marker"
        if lane == "psi-observacionismo" and "STRONG_CLAIM_REVIEW" in flags:
            falsifiers = "no_recupera_limites; fuente_no_verificada; claim_publico_fuerte; sin_experimento"
        records.append(
            TreeRecord(
                source_label=label,
                path=str(path),
                rel_path=rel_path,
                sha256=sha,
                size_bytes=size_bytes,
                suffix=path.suffix.lower(),
                kind=kind,
                psi_state=psi_state,
                status=status,
                classification=classification,
                lane=lane,
                decision=decision,
                action_gate=action_gate,
                risk_flags=flags,
                target=target_for(lane, path),
                summary=summary,
                falsifiers=falsifiers,
                canonical_path=str(canonical) if duplicate_count > 1 else None,
                duplicate_count=duplicate_count,
                safe_delete_candidate=safe_delete,
            )
        )
    return records


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_report(path: Path, records: list[TreeRecord], deleted: list[TreeRecord], roots: list[tuple[str, Path]]) -> None:
    counts = count_by(records, "status")
    lanes = count_by(records, "lane")
    decisions = count_by(records, "decision")
    lines = [
        "# Curador SETO Tree Absorption",
        "",
        f"Generated UTC: `{utc_now()}`",
        "",
        "Estado: `FICHADO / ABSORBIDO_A_ATLAS / LIMPIEZA_SEGURA_PARCIAL`",
        "",
        "## Rutas",
        "",
    ]
    for label, root in roots:
        lines.append(f"- `{label}`: `{root}`")
    lines.extend(
        [
            "",
            "## Resumen",
            "",
            f"- Archivos registrados: `{len(records)}`",
            f"- Duplicados exactos detectados: `{sum(1 for r in records if r.duplicate_count > 1)}` archivos en grupos duplicados",
            f"- Eliminados seguros en este pase: `{len(deleted)}`",
            "",
            "## Estados",
            "",
            "| estado | archivos |",
            "|---|---:|",
        ]
    )
    for key, value in sorted(counts.items()):
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Carriles", "", "| carril | archivos |", "|---|---:|"])
    for key, value in sorted(lanes.items()):
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Decisiones", "", "| decision | archivos |", "|---|---:|"])
    for key, value in sorted(decisions.items()):
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "## Veredicto",
            "",
            "- La absorcion de este pase crea fichas por archivo y manifest estructurado.",
            "- `Downloads` se trata como zona de amenaza: nada descargado se ejecuta, extrae o publica antes de clasificar riesgo.",
            "- Lo unico que puede retirarse automaticamente es duplicado exacto o basura regenerable con hash y gate.",
            "- Los documentos unicos, privados, de claims fuertes o con frontera de publicacion quedan `REVIEW` o `BLOQUEADO`; no se borran.",
            "",
            "## Archivos eliminados",
            "",
        ]
    )
    if deleted:
        lines.extend(["| sha256 | ruta retirada | copia canonica | motivo |", "|---|---|---|---|"])
        for record in deleted:
            lines.append(
                f"| `{record.sha256[:16]}` | `{record.path}` | `{record.canonical_path or ''}` | `{record.decision}` |"
            )
    else:
        lines.append("Ninguno.")
    lines.extend(
        [
            "",
            "## Siguiente limpieza permitida",
            "",
            "1. Revisar `REVIEW_DUPLICATE` que no estaban en carpeta archive/copia.",
            "2. Convertir fuentes unicas grandes en fichas de concepto antes de archivo frio.",
            "3. No publicar ni abrir OSIT-QG/OSIT-AG/GEODIA sin falsadores y claims boundary.",
            "4. Si una carpeta queda solo como archivo frio ya absorbido, moverla completa en una fase separada con rollback.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_fichas(path: Path, records: list[TreeRecord], max_records: int = 0) -> None:
    lines = [
        "# Fichas Curador SETO",
        "",
        f"Generated UTC: `{utc_now()}`",
        "",
        "Cada bloque es una ficha tecnica minima por archivo: hash, estado, decision, destino y falsadores.",
        "",
    ]
    sorted_records = sorted(records, key=lambda r: (r.source_label, r.rel_path.lower()))
    selected_records = sorted_records[:max_records] if max_records and max_records > 0 else sorted_records
    if max_records and len(sorted_records) > max_records:
        lines.extend(
            [
                f"Nota: esta vista Markdown esta limitada a `{max_records}` fichas para mantener legibilidad.",
                f"El manifest JSON contiene el registro tecnico completo de `{len(sorted_records)}` archivos.",
                "",
            ]
        )
    for index, record in enumerate(selected_records, start=1):
        lines.extend(
            [
                f"## {index}. {record.source_label} / {record.rel_path}",
                "",
                f"- Ruta: `{record.path}`",
                f"- SHA256: `{record.sha256}`",
                f"- Tamaño: `{record.size_bytes}` bytes",
                f"- Tipo: `{record.kind}`",
                f"- Estado PSI: `{record.psi_state}`",
                f"- Estado archivo: `{record.status}`",
                f"- Clasificacion: `{record.classification}`",
                f"- Decision: `{record.decision}`",
                f"- ActionGate: `{record.action_gate}`",
                f"- Carril/Destino: `{record.lane}` -> {record.target}",
                f"- Copia canonica: `{record.canonical_path or 'n/a'}`",
                f"- Riesgos: `{', '.join(record.risk_flags) if record.risk_flags else 'none'}`",
                f"- Resumen: {record.summary.strip()}",
                f"- Falsadores: `{record.falsifiers}`",
                "",
            ]
        )
    if len(selected_records) < len(sorted_records):
        omitted = sorted_records[len(selected_records) :]
        lines.extend(
            [
                "## Fichas no expandidas en Markdown",
                "",
                f"- Total omitido: `{len(omitted)}`",
                "- Registro completo: manifest JSON de este mismo run.",
                "",
                "### Estados omitidos",
                "",
                "| estado | archivos |",
                "|---|---:|",
            ]
        )
        for key, value in sorted(count_by(omitted, "status").items()):
            lines.append(f"| `{key}` | {value} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_deletions(path: Path, deleted: list[TreeRecord]) -> None:
    lines = [
        "# Curador SETO Deletions",
        "",
        f"Generated UTC: `{utc_now()}`",
        "",
        "Solo se registran retiros seguros de duplicados exactos o basura regenerable.",
        "",
    ]
    if not deleted:
        lines.append("No se elimino ningun archivo.")
    else:
        lines.extend(["| sha256 | ruta retirada | copia canonica | decision |", "|---|---|---|---|"])
        for record in deleted:
            lines.append(f"| `{record.sha256}` | `{record.path}` | `{record.canonical_path or ''}` | `{record.decision}` |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def count_by(records: Iterable[TreeRecord], attr: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        key = str(getattr(record, attr))
        counts[key] = counts.get(key, 0) + 1
    return counts


def apply_safe_deletes(records: list[TreeRecord], trash_dir: Path) -> list[TreeRecord]:
    trash_dir.mkdir(parents=True, exist_ok=True)
    deleted: list[TreeRecord] = []
    for record in records:
        if not record.safe_delete_candidate or record.action_gate != "APPROVE":
            continue
        path = Path(record.path)
        if not path.exists() or not path.is_file():
            continue
        # Use a local quarantine instead of permanent unlink. This removes noise
        # from the source tree while preserving rollback evidence.
        target_name = f"{record.sha256[:16]}_{slugify(path.name)}"
        target = trash_dir / target_name
        if target.exists():
            target = trash_dir / f"{record.sha256[:16]}_{int(datetime.now().timestamp())}_{slugify(path.name)}"
        shutil.move(str(path), str(target))
        record.deleted = True
        record.status = "RETIRADO_A_QUARANTINE"
        deleted.append(record)
    return deleted


def parse_roots(raw_roots: list[str]) -> list[tuple[str, Path]]:
    roots: list[tuple[str, Path]] = []
    for raw in raw_roots:
        if "=" in raw:
            label, raw_path = raw.split("=", 1)
        else:
            path_obj = Path(raw)
            label = slugify(path_obj.name, 40)
            raw_path = raw
        path = Path(raw_path).expanduser().resolve()
        if not path.exists() or not path.is_dir():
            raise SystemExit(f"root not found or not directory: {path}")
        roots.append((label, path))
    return roots


def main() -> int:
    configure_stdout()
    parser = argparse.ArgumentParser(description="Curador SETO tree absorption for arbitrary local source trees.")
    parser.add_argument("--root", action="append", required=True, help="label=absolute_path or absolute_path")
    parser.add_argument("--name", default=f"tree_absorption_{TODAY}", help="run name for output files")
    parser.add_argument("--apply-safe-deletes", action="store_true", help="move safe duplicate/trash candidates to local quarantine")
    parser.add_argument(
        "--hash-limit-mb",
        type=int,
        default=0,
        help="defer full SHA256 for files larger than this size in MB; 0 means hash all files",
    )
    parser.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="extra directory name to skip during recursive scans",
    )
    parser.add_argument(
        "--max-markdown-fichas",
        type=int,
        default=0,
        help="limit expanded Markdown fichas; manifest JSON still contains all records",
    )
    parser.add_argument("--json", action="store_true", help="print JSON summary")
    args = parser.parse_args()

    roots = parse_roots(args.root)
    hash_limit_bytes = args.hash_limit_mb * 1024 * 1024 if args.hash_limit_mb else None
    excluded_dirs = set(DEFAULT_EXCLUDED_DIRS)
    excluded_dirs.update(name.lower() for name in args.exclude_dir)
    records = build_records(roots, hash_limit_bytes=hash_limit_bytes, excluded_dirs=excluded_dirs)
    out_base = ROOT / "docs" / "intake"
    safe_name = slugify(args.name, 90)
    quarantine = ROOT / "runtime" / "curador_seto" / "tree_quarantine" / safe_name
    deleted = apply_safe_deletes(records, quarantine) if args.apply_safe_deletes else []

    manifest_path = out_base / f"{safe_name}_MANIFEST.json"
    report_path = out_base / f"{safe_name}_REPORT.md"
    fichas_path = out_base / f"{safe_name}_FICHAS.md"
    deletions_path = out_base / f"{safe_name}_DELETIONS.md"

    payload = {
        "generated_at_utc": utc_now(),
        "roots": [{"label": label, "path": str(path)} for label, path in roots],
        "apply_safe_deletes": bool(args.apply_safe_deletes),
        "hash_limit_mb": args.hash_limit_mb,
        "excluded_dirs": sorted(excluded_dirs),
        "quarantine": str(quarantine),
        "counts": {
            "files": len(records),
            "deleted_or_quarantined": len(deleted),
            "by_status": count_by(records, "status"),
            "by_lane": count_by(records, "lane"),
            "by_decision": count_by(records, "decision"),
        },
        "records": [asdict(record) for record in records],
    }
    write_json(manifest_path, payload)
    write_report(report_path, records, deleted, roots)
    write_fichas(fichas_path, records, max_records=args.max_markdown_fichas)
    write_deletions(deletions_path, deleted)

    summary = {
        "manifest": str(manifest_path),
        "report": str(report_path),
        "fichas": str(fichas_path),
        "deletions": str(deletions_path),
        "quarantine": str(quarantine),
        "files": len(records),
        "deleted_or_quarantined": len(deleted),
        "status_counts": count_by(records, "status"),
        "decision_counts": count_by(records, "decision"),
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"files={len(records)} deleted_or_quarantined={len(deleted)}")
        print(f"report={report_path}")
        print(f"fichas={fichas_path}")
        print(f"manifest={manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
