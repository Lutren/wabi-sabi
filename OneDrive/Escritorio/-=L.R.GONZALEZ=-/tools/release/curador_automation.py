from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DOWNLOADS = Path.home() / "Downloads"
TODAY = datetime.now().date().isoformat()

TEXT_SUFFIXES = {".md", ".txt", ".py", ".json", ".csv", ".html", ".js", ".ts", ".css", ".yml", ".yaml"}
ZIP_SUFFIXES = {".zip", ".docx", ".pptx", ".xlsx"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
PDF_SUFFIXES = {".pdf"}
SECRET_MARKERS = {
    ".env",
    "secret",
    "token",
    "credential",
    "api_key",
    "apikey",
    "private_key",
    "settings.local",
}
PRIVATE_MARKERS = {"metaevo-tcg", "tcg", "game_bridge", "medioevo_rpg"}
CLAIM_MARKERS = {"fisica", "physics", "antigravity", "antigravedad", "diagnostico", "medical"}


@dataclass
class FileRecord:
    path: str
    rel_path: str
    sha256: str
    size_bytes: int
    suffix: str
    kind: str
    line_count: int | None
    psi_state: str
    status: str
    classification: str
    lane: str
    decision: str
    action_gate: str
    summary: str
    target: str
    falsifiers: str
    risk_flags: list[str]
    ficha_path: str
    canonical_path: str | None = None
    deleted: bool = False


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def configure_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def ensure_under(path: Path, parent: Path) -> Path:
    resolved = path.resolve()
    root = parent.resolve()
    if resolved != root and root not in resolved.parents:
        raise ValueError(f"path escapes allowed root: {resolved}")
    return resolved


def slugify(value: str, limit: int = 72) -> str:
    normalized = value.encode("ascii", "ignore").decode("ascii").lower()
    normalized = re.sub(r"[^a-z0-9._-]+", "-", normalized).strip("-._")
    return (normalized or "file")[:limit]


def has_copy_suffix(path: Path) -> bool:
    return bool(re.search(r"\s*\(\d+\)$", path.stem))


def is_low_semantic_name(path: Path) -> bool:
    name = path.name.lower()
    return (
        name.startswith("pasted ")
        or name.startswith("untitled")
        or name.startswith("readme")
        or name.startswith("```")
        or name.startswith("#!")
        or "copy" in name
        or "copia" in name
    )


def line_count(path: Path, max_bytes: int = 5_000_000) -> int | None:
    try:
        if path.stat().st_size > max_bytes:
            return None
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    return len(text.splitlines())


def zip_member_count(path: Path) -> int | None:
    try:
        with zipfile.ZipFile(path) as archive:
            return len([item for item in archive.infolist() if not item.is_dir()])
    except (OSError, zipfile.BadZipFile):
        return None


def pdf_page_hint(path: Path) -> int | None:
    try:
        data = path.read_bytes()[:5_000_000]
    except OSError:
        return None
    count = data.count(b"/Type /Page")
    return count or None


def classify(path: Path) -> tuple[str, str, str, str, str, list[str]]:
    name = path.name.lower()
    suffix = path.suffix.lower()
    full = str(path).lower()
    risk_flags: list[str] = []
    if any(marker in name or marker in full for marker in SECRET_MARKERS):
        risk_flags.append("secret_like")
    if any(marker in full for marker in PRIVATE_MARKERS):
        risk_flags.append("private_ip")
    if any(marker in name for marker in CLAIM_MARKERS):
        risk_flags.append("strong_claim_review")

    if suffix in IMAGE_SUFFIXES:
        return (
            "ASSET_IMAGE",
            "assets-review",
            "FICHA_BATCH_IMAGE_ASSET",
            "REVIEW",
            "Image asset; registered by hash and batch ficha.",
            risk_flags,
        )
    if suffix in {".zip", ".docx", ".pdf"}:
        lane = "research-boundary"
        if "duat" in name:
            lane = "duat-lab"
        elif "psi" in name or "observ" in name or "tuip" in name or "osit" in name:
            lane = "research-boundary"
        elif "claudio" in name:
            lane = "local-agent"
        return (
            "PACKAGE_OR_DOCUMENT_REVIEW",
            lane,
            "FICHA_TECHNICAL_CARD_NO_RAW_IMPORT",
            "REVIEW",
            "Package/document source; lineage and claims must be reviewed before import.",
            risk_flags,
        )
    if "duat" in name:
        return (
            "DUAT_LAB_SOURCE",
            "duat-lab",
            "TECHNICAL_CARD_AND_RESEARCH_BACKLOG",
            "REVIEW",
            "DUAT source; computational lab material, not validated physics or product claim.",
            risk_flags,
        )
    if suffix in {".py", ".js", ".ts"} or "code" in name or "codigo" in name or "código" in name:
        lane = "local-agent" if "claudio" in name or "agent" in name else "research-boundary"
        return (
            "CODE_PROTOTYPE_REVIEW",
            lane,
            "READ_REVIEW_TEST_BEFORE_IMPORT",
            "REVIEW",
            "Code prototype; no execution or import until dependencies and side effects are reviewed.",
            risk_flags,
        )
    if "sensorium" in name:
        return (
            "SENSORIUM_SOURCE",
            "sensorium",
            "RESEARCH_ONLY_WITH_CLAIM_BOUNDARY",
            "REVIEW",
            "Sensorium source; preserve as research input with claim boundary.",
            risk_flags,
        )
    if "psi" in name or "observ" in name or "tuip" in name or "osit" in name or "sigma" in name:
        return (
            "OBSERVACIONISMO_RESEARCH_SYNTHESIS",
            "research-boundary",
            "RESEARCH_ONLY_WITH_CLAIM_BOUNDARY",
            "REVIEW",
            "Observacionismo/TUIP/PSI synthesis; preserve evidence, inference and unknown labels.",
            risk_flags,
        )
    if suffix in {".csv", ".json"}:
        return (
            "LAB_EVIDENCE_DATA",
            "research-boundary",
            "EVIDENCE_ONLY",
            "REVIEW",
            "Small evidence/data artifact; keep linked to source and validation status.",
            risk_flags,
        )
    if suffix in TEXT_SUFFIXES:
        return (
            "TEXT_SOURCE_REVIEW",
            "cleanup",
            "HOLD_WITH_TECHNICAL_CARD_BEFORE_USE",
            "REVIEW",
            "Text source; register before deciding canon, archive or deletion.",
            risk_flags,
        )
    return (
        "UNKNOWN_REVIEW_REQUIRED",
        "cleanup",
        "HOLD_WITH_TECHNICAL_CARD_BEFORE_USE",
        "REVIEW",
        "Unknown source; keep out of public packages until ficha exists.",
        risk_flags,
    )


def target_for_lane(lane: str) -> str:
    return {
        "research-boundary": "docs/intake and research/ after claim review",
        "duat-lab": "docs/intake and future research/duat-lab",
        "local-agent": "Claudio local-agent backlog and COMMS contracts",
        "sensorium": "docs/intake and Sensorium research backlog",
        "assets-review": "docs/intake/curador_fichas/downloads/assets batch",
        "cleanup": "Curador review queue",
    }.get(lane, "Curador review queue")


def scan_downloads(downloads_dir: Path, recursive: bool) -> list[Path]:
    ensure_under(downloads_dir, downloads_dir)
    if not downloads_dir.exists():
        return []
    if recursive:
        iterator = downloads_dir.rglob("*")
    else:
        iterator = downloads_dir.iterdir()
    files = []
    for path in iterator:
        if not path.is_file():
            continue
        parts = {part.lower() for part in path.parts}
        if parts & {".git", "node_modules", "__pycache__", ".venv", "venv"}:
            continue
        files.append(path)
    return sorted(files, key=lambda item: str(item).lower())


def make_file_records(downloads_dir: Path, files: Iterable[Path], fichas_dir: Path) -> list[FileRecord]:
    records: list[FileRecord] = []
    image_batch = "docs/intake/curador_fichas/downloads/DOWNLOADS_IMAGE_ASSETS_BATCH.md"
    for path in files:
        resolved = ensure_under(path, downloads_dir)
        stat = resolved.stat()
        classification, lane, decision, gate, summary, risk_flags = classify(resolved)
        if risk_flags and ("secret_like" in risk_flags or "private_ip" in risk_flags):
            gate = "BLOCK"
            decision = "KEEP_BLOCKED_BOUNDARY"
        rel_path = resolved.relative_to(downloads_dir).as_posix()
        digest = sha256_file(resolved)
        suffix = resolved.suffix.lower()
        kind = "file"
        if suffix in ZIP_SUFFIXES:
            kind = f"zip_like_members_{zip_member_count(resolved) or 'unknown'}"
        elif suffix in PDF_SUFFIXES:
            kind = f"pdf_page_hint_{pdf_page_hint(resolved) or 'unknown'}"
        ficha_path = image_batch
        if suffix not in IMAGE_SUFFIXES:
            ficha_path = f"docs/intake/curador_fichas/downloads/{digest[:16]}_{slugify(resolved.stem)}.md"
        records.append(
            FileRecord(
                path=str(resolved),
                rel_path=rel_path,
                sha256=digest,
                size_bytes=stat.st_size,
                suffix=suffix,
                kind=kind,
                line_count=line_count(resolved) if suffix in TEXT_SUFFIXES else None,
                psi_state="BLOQUEADO" if gate == "BLOCK" else "CERTEZA",
                status="REGISTRADO",
                classification=classification,
                lane=lane,
                decision=decision,
                action_gate=gate,
                summary=summary,
                target=target_for_lane(lane),
                falsifiers="secret/private marker, hash mismatch, unique content loss, strong claim without validation",
                risk_flags=risk_flags,
                ficha_path=ficha_path,
            )
        )
    return records


def canonical_key(record: FileRecord, downloads_dir: Path) -> tuple[int, int, int, int, str]:
    path = Path(record.path)
    rel_parts = path.relative_to(downloads_dir).parts
    is_top = 0 if len(rel_parts) == 1 else 1
    copy_score = 1 if has_copy_suffix(path) else 0
    semantic_score = 1 if is_low_semantic_name(path) else 0
    length_score = len(path.name)
    return (is_top, copy_score, semantic_score, length_score, str(path).lower())


def duplicate_groups(records: list[FileRecord], downloads_dir: Path) -> list[dict[str, object]]:
    grouped: dict[str, list[FileRecord]] = {}
    for record in records:
        grouped.setdefault(record.sha256, []).append(record)
    groups = []
    for digest, members in grouped.items():
        if len(members) < 2:
            continue
        canonical = sorted(members, key=lambda item: canonical_key(item, downloads_dir))[0]
        risk_flags = sorted({flag for member in members for flag in member.risk_flags})
        gate = "BLOCK" if {"secret_like", "private_ip"} & set(risk_flags) else "APPROVE"
        groups.append(
            {
                "sha256": digest,
                "count": len(members),
                "canonical_path": canonical.path,
                "candidate_paths": [member.path for member in members if member.path != canonical.path],
                "bytes_each": canonical.size_bytes,
                "duplicate_bytes_if_one_kept": canonical.size_bytes * (len(members) - 1),
                "action_gate": gate,
                "risk_flags": risk_flags,
            }
        )
        for member in members:
            member.canonical_path = canonical.path
            if member.path == canonical.path:
                member.status = "CANONICO"
                member.decision = "KEEP_CANONICAL_EXACT_DUPLICATE"
            else:
                member.status = "DUPLICADO_EXACTO"
                if gate == "APPROVE" and member.action_gate != "BLOCK":
                    member.action_gate = "APPROVE"
                    member.decision = "DELETE_APPROVED_AFTER_HASH"
                else:
                    member.action_gate = "BLOCK"
                    member.decision = "CANDIDATE_DELETE_BLOCKED"
    return sorted(groups, key=lambda item: str(item["sha256"]))


def write_sqlite(db_path: Path, records: list[FileRecord], groups: list[dict[str, object]], event: dict[str, object]) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS files (
              path TEXT PRIMARY KEY,
              rel_path TEXT,
              sha256 TEXT,
              size_bytes INTEGER,
              suffix TEXT,
              kind TEXT,
              psi_state TEXT,
              status TEXT,
              classification TEXT,
              lane TEXT,
              decision TEXT,
              action_gate TEXT,
              summary TEXT,
              target TEXT,
              falsifiers TEXT,
              risk_flags_json TEXT,
              ficha_path TEXT,
              canonical_path TEXT,
              deleted INTEGER,
              last_seen_utc TEXT
            );
            CREATE TABLE IF NOT EXISTS duplicate_groups (
              sha256 TEXT PRIMARY KEY,
              count INTEGER,
              canonical_path TEXT,
              candidate_paths_json TEXT,
              action_gate TEXT,
              risk_flags_json TEXT,
              duplicate_bytes_if_one_kept INTEGER,
              updated_utc TEXT
            );
            CREATE TABLE IF NOT EXISTS fichas (
              source_path TEXT PRIMARY KEY,
              ficha_path TEXT,
              sha256 TEXT,
              status TEXT,
              kind TEXT,
              updated_utc TEXT
            );
            CREATE TABLE IF NOT EXISTS duplicates (
              sha256 TEXT,
              member_path TEXT,
              canonical_path TEXT,
              role TEXT,
              action_gate TEXT,
              deleted INTEGER,
              decision TEXT,
              updated_utc TEXT,
              PRIMARY KEY (sha256, member_path)
            );
            CREATE TABLE IF NOT EXISTS synapses (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              source_path TEXT,
              target TEXT,
              relation TEXT,
              psi_state TEXT,
              evidence TEXT
            );
            CREATE TABLE IF NOT EXISTS decisions (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              timestamp_utc TEXT,
              source_path TEXT,
              decision TEXT,
              action_gate TEXT,
              reason TEXT,
              canonical_path TEXT,
              evidence TEXT
            );
            CREATE TABLE IF NOT EXISTS witness_events (
              event_hash TEXT PRIMARY KEY,
              previous_hash TEXT,
              timestamp_utc TEXT,
              event_type TEXT,
              actor TEXT,
              summary_json TEXT
            );
            """
        )
        db.execute("DELETE FROM duplicate_groups")
        db.execute("DELETE FROM duplicates")
        db.execute("DELETE FROM fichas")
        db.execute("DELETE FROM synapses")
        for record in records:
            db.execute(
                """
                INSERT OR REPLACE INTO files VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    record.path,
                    record.rel_path,
                    record.sha256,
                    record.size_bytes,
                    record.suffix,
                    record.kind,
                    record.psi_state,
                    record.status,
                    record.classification,
                    record.lane,
                    record.decision,
                    record.action_gate,
                    record.summary,
                    record.target,
                    record.falsifiers,
                    json.dumps(record.risk_flags, ensure_ascii=False),
                    record.ficha_path,
                    record.canonical_path,
                    1 if record.deleted else 0,
                    utc_now(),
                ),
            )
            db.execute(
                "INSERT INTO synapses(source_path,target,relation,psi_state,evidence) VALUES (?,?,?,?,?)",
                (record.path, record.target, "curador_lane", record.psi_state, record.sha256),
            )
            db.execute(
                "INSERT OR REPLACE INTO fichas VALUES (?,?,?,?,?,?)",
                (record.path, record.ficha_path, record.sha256, record.status, record.kind, utc_now()),
            )
        for group in groups:
            db.execute(
                "INSERT INTO duplicate_groups VALUES (?,?,?,?,?,?,?,?)",
                (
                    group["sha256"],
                    group["count"],
                    group["canonical_path"],
                    json.dumps(group["candidate_paths"], ensure_ascii=False),
                    group["action_gate"],
                    json.dumps(group["risk_flags"], ensure_ascii=False),
                    group["duplicate_bytes_if_one_kept"],
                    utc_now(),
                ),
            )
        db.execute(
            """
            INSERT OR REPLACE INTO duplicates
            SELECT
              sha256,
              path,
              canonical_path,
              CASE WHEN path = canonical_path THEN 'canonical' ELSE 'candidate' END,
              action_gate,
              deleted,
              decision,
              ?
            FROM files
            WHERE canonical_path IS NOT NULL
            """,
            (utc_now(),),
        )
        db.execute(
            """
            INSERT OR REPLACE INTO fichas
            SELECT path, ficha_path, sha256, status, kind, ?
            FROM files
            WHERE ficha_path IS NOT NULL AND ficha_path != ''
            """,
            (utc_now(),),
        )
        for record in records:
            db.execute(
                "INSERT INTO decisions(timestamp_utc,source_path,decision,action_gate,reason,canonical_path,evidence) VALUES (?,?,?,?,?,?,?)",
                (utc_now(), record.path, record.decision, record.action_gate, record.summary, record.canonical_path, record.sha256),
            )
        db.execute(
            "INSERT OR REPLACE INTO witness_events VALUES (?,?,?,?,?,?)",
            (
                event["event_hash"],
                event.get("previous_hash"),
                event["timestamp_utc"],
                event["event_type"],
                event["actor"],
                json.dumps(event, ensure_ascii=False),
            ),
        )


def render_ficha(record: FileRecord) -> str:
    return "\n".join(
        [
            f"# Ficha Curador SETO - {Path(record.path).name}",
            "",
            "| campo | valor |",
            "|---|---|",
            f"| Ruta original | `{record.path}` |",
            f"| SHA256 | `{record.sha256}` |",
            f"| Bytes | `{record.size_bytes}` |",
            f"| Tipo | `{record.kind}` |",
            f"| Estado PSI | `{record.psi_state}` |",
            f"| Status | `{record.status}` |",
            f"| Clasificacion | `{record.classification}` |",
            f"| Lane | `{record.lane}` |",
            f"| Decision | `{record.decision}` |",
            f"| ActionGate | `{record.action_gate}` |",
            f"| Canonico | `{record.canonical_path or record.path}` |",
            "",
            "## Resumen",
            "",
            record.summary,
            "",
            "## Sinapsis",
            "",
            f"- Destino: `{record.target}`.",
            f"- Evidencia: SHA256 `{record.sha256}`.",
            "- Uso permitido: local, curado, sin publicacion externa directa.",
            "",
            "## Falsadores",
            "",
            f"- {record.falsifiers}.",
            "- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.",
            "",
        ]
    )


def render_image_batch(records: list[FileRecord]) -> str:
    image_records = [record for record in records if record.suffix in IMAGE_SUFFIXES]
    lines = [
        "# Ficha Curador SETO - Downloads Image Assets Batch",
        "",
        "Ficha de lote para imagenes repetitivas o assets visuales en Downloads.",
        "",
        "| metric | value |",
        "|---|---:|",
        f"| files | {len(image_records)} |",
        f"| total_bytes | {sum(record.size_bytes for record in image_records)} |",
        "",
        "| status | count |",
        "|---|---:|",
    ]
    counts: dict[str, int] = {}
    for record in image_records:
        counts[record.status] = counts.get(record.status, 0) + 1
    for key in sorted(counts):
        lines.append(f"| `{key}` | {counts[key]} |")
    lines.extend(["", "## Items", "", "| path | sha256 | bytes | status |", "|---|---|---:|---|"])
    for record in image_records:
        lines.append(f"| `{record.path}` | `{record.sha256}` | {record.size_bytes} | `{record.status}` |")
    lines.append("")
    return "\n".join(lines)


def write_fichas(workspace_root: Path, records: list[FileRecord]) -> None:
    ficha_root = workspace_root / "docs" / "intake" / "curador_fichas" / "downloads"
    ficha_root.mkdir(parents=True, exist_ok=True)
    image_records = [record for record in records if record.suffix in IMAGE_SUFFIXES]
    if image_records:
        (workspace_root / image_records[0].ficha_path).write_text(render_image_batch(records), encoding="utf-8")
    for record in records:
        if record.suffix in IMAGE_SUFFIXES:
            continue
        path = workspace_root / record.ficha_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_ficha(record), encoding="utf-8")


def render_master_index(records: list[FileRecord], groups: list[dict[str, object]], deleted: list[dict[str, object]], db_path: Path) -> str:
    status_counts: dict[str, int] = {}
    lane_counts: dict[str, int] = {}
    for record in records:
        status_counts[record.status] = status_counts.get(record.status, 0) + 1
        lane_counts[record.lane] = lane_counts.get(record.lane, 0) + 1
    lines = [
        "# Curador SETO Master Index",
        "",
        f"Generated UTC: `{utc_now()}`",
        "",
        "Fuente canonica operativa para Downloads. SQLite es la base consultable; las fichas Markdown son la capa humana.",
        "",
        "| campo | valor |",
        "|---|---:|",
        f"| archivos registrados | {len(records)} |",
        f"| grupos duplicados exactos detectados | {len(groups)} |",
        f"| duplicados exactos borrados en este pase | {len(deleted)} |",
        f"| sqlite | `{db_path}` |",
        "",
        "## Status",
        "",
        "| status | count |",
        "|---|---:|",
    ]
    for key in sorted(status_counts):
        lines.append(f"| `{key}` | {status_counts[key]} |")
    lines.extend(["", "## Lanes", "", "| lane | count |", "|---|---:|"])
    for key in sorted(lane_counts):
        lines.append(f"| `{key}` | {lane_counts[key]} |")
    lines.extend(["", "## Duplicados exactos", "", "| sha256 | count | canonico | candidatos | gate |", "|---|---:|---|---|---|"])
    for group in groups:
        candidates = "<br>".join(f"`{path}`" for path in group["candidate_paths"])
        lines.append(f"| `{str(group['sha256'])[:16]}...` | {group['count']} | `{group['canonical_path']}` | {candidates} | `{group['action_gate']}` |")
    lines.extend(["", "## Archivos", "", "| status | lane | decision | ficha | path |", "|---|---|---|---|---|"])
    for record in sorted(records, key=lambda item: item.rel_path.lower()):
        lines.append(f"| `{record.status}` | `{record.lane}` | `{record.decision}` | `{record.ficha_path}` | `{record.path}` |")
    lines.append("")
    return "\n".join(lines)


def previous_witness_hash(log_path: Path) -> str | None:
    if not log_path.exists():
        return None
    try:
        lines = [line for line in log_path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]
    except OSError:
        return None
    if not lines:
        return None
    try:
        return json.loads(lines[-1]).get("event_hash")
    except json.JSONDecodeError:
        return None


def event_hash(event: dict[str, object]) -> str:
    payload = {key: value for key, value in event.items() if key != "event_hash"}
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def append_witness(log_path: Path, event: dict[str, object]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")


def delete_exact_duplicates(downloads_dir: Path, groups: list[dict[str, object]], records: list[FileRecord], apply_delete: bool) -> list[dict[str, object]]:
    by_path = {record.path: record for record in records}
    deleted: list[dict[str, object]] = []
    for group in groups:
        group_gate = str(group.get("action_gate") or "REVIEW")
        canonical = ensure_under(Path(str(group["canonical_path"])), downloads_dir)
        canonical_hash = sha256_file(canonical)
        for raw_path in group["candidate_paths"]:
            candidate = ensure_under(Path(str(raw_path)), downloads_dir)
            if not candidate.exists() or not candidate.is_file():
                continue
            record = by_path[str(candidate)]
            if record.action_gate == "BLOCK":
                continue
            if record.ficha_path == "":
                continue
            candidate_hash = sha256_file(candidate)
            if candidate_hash != canonical_hash or candidate_hash != group["sha256"]:
                continue
            entry = {
                "path": str(candidate),
                "sha256": candidate_hash,
                "bytes": candidate.stat().st_size,
                "canonical_path": str(canonical),
                "reason": "exact duplicate in Downloads with generated ficha and canonical copy",
                "deleted": False,
            }
            if group_gate != "APPROVE" or record.action_gate != "APPROVE":
                entry["blocked_reason"] = "destructive_delete_requires_action_gate_APPROVE"
                deleted.append(entry)
                continue
            if apply_delete:
                candidate.unlink()
                record.deleted = True
                record.status = "BORRADO_DUPLICADO"
                record.decision = "DELETE_APPROVED_AFTER_HASH_EXECUTED"
                entry["deleted"] = True
            deleted.append(entry)
    return deleted


def write_deleted_log(workspace_root: Path, deleted: list[dict[str, object]], result_path: Path) -> None:
    if not deleted:
        return
    deleted_count = sum(1 for item in deleted if item["deleted"])
    deleted_bytes = sum(int(item["bytes"]) for item in deleted if item["deleted"])
    log_path = workspace_root / "DELETED_OR_ARCHIVED.md"
    section = [
        "",
        f"## Curador SETO Downloads Exact Duplicate Cleanup {TODAY}",
        "",
        "Deleted only exact duplicate files under Downloads. Unique material was preserved.",
        "",
        "| date | count | bytes | scope | evidence |",
        "|---|---:|---:|---|---|",
        f"| {TODAY} | {deleted_count} files | {deleted_bytes} | exact SHA256 duplicates in `Downloads`; canonical copy retained | `{result_path.relative_to(workspace_root)}` |",
        "",
        "| deleted path | sha256 | bytes | canonical path |",
        "|---|---|---:|---|",
    ]
    for item in deleted:
        if item["deleted"]:
            section.append(f"| `{item['path']}` | `{item['sha256']}` | {item['bytes']} | `{item['canonical_path']}` |")
    section.append("")
    existing = log_path.read_text(encoding="utf-8") if log_path.exists() else "# DELETED_OR_ARCHIVED\n"
    log_path.write_text(existing.rstrip() + "\n" + "\n".join(section), encoding="utf-8")


def write_runtime_export(runtime_dir: Path, records: list[FileRecord], groups: list[dict[str, object]], deleted: list[dict[str, object]]) -> None:
    runtime_dir.mkdir(parents=True, exist_ok=True)
    export = {
        "generated_at_utc": utc_now(),
        "downloads_records": [asdict(record) for record in records],
        "duplicate_groups": groups,
        "deleted": deleted,
    }
    (runtime_dir / "source_intake_export.json").write_text(json.dumps(export, indent=2, ensure_ascii=False), encoding="utf-8")


def current_snapshot(records: list[FileRecord]) -> list[tuple[str, str, int]]:
    return sorted((record.path, record.sha256, record.size_bytes) for record in records)


def stored_current_snapshot(db_path: Path) -> list[tuple[str, str, int]] | None:
    if not db_path.exists():
        return None
    try:
        with sqlite3.connect(db_path) as db:
            rows = db.execute(
                "SELECT path, sha256, size_bytes FROM files WHERE deleted = 0 ORDER BY path"
            ).fetchall()
    except sqlite3.Error:
        return None
    return [(str(path), str(sha256), int(size_bytes)) for path, sha256, size_bytes in rows]


def curador_outputs_exist(workspace_root: Path, db_path: Path, write_index: bool, write_fichas_flag: bool) -> bool:
    required = [
        db_path,
        workspace_root / "runtime" / "curador_seto" / "source_intake_export.json",
        workspace_root / "qa_artifacts" / "witness_log" / "curador_seto_witnesslog.jsonl",
    ]
    if write_index:
        required.append(workspace_root / "docs" / "intake" / "CURADOR_MASTER_INDEX.md")
    if write_fichas_flag:
        required.append(workspace_root / "docs" / "intake" / "curador_fichas" / "downloads")
    return all(path.exists() for path in required)


def no_change_result(
    *,
    workspace_root: Path,
    downloads_dir: Path,
    db_path: Path,
    witness_path: Path,
    records: list[FileRecord],
) -> dict[str, object]:
    result: dict[str, object] = {
        "generated_at_utc": utc_now(),
        "workspace_root": str(workspace_root),
        "downloads_dir": str(downloads_dir),
        "db_path": str(db_path),
        "master_index": str(workspace_root / "docs" / "intake" / "CURADOR_MASTER_INDEX.md"),
        "witness_log": str(witness_path),
        "witness_event_hash": previous_witness_hash(witness_path),
        "downloads_files_seen": len(records),
        "duplicate_groups_detected": 0,
        "deleted_exact_duplicates": 0,
        "deleted_bytes": 0,
        "new_folder_files_registered": sum(1 for record in records if record.rel_path.lower().startswith("new folder/")),
        "blocked_records": sum(1 for record in records if record.action_gate == "BLOCK"),
        "status_counts": {},
        "duplicate_groups": [],
        "deleted": [],
        "noop": True,
    }
    for record in records:
        result["status_counts"][record.status] = result["status_counts"].get(record.status, 0) + 1
    return result


def sqlite_table_counts(db_path: Path) -> dict[str, int]:
    tables = ["files", "fichas", "duplicates", "duplicate_groups", "synapses", "decisions", "witness_events"]
    if not db_path.exists():
        return {table: 0 for table in tables}
    counts: dict[str, int] = {}
    with sqlite3.connect(db_path) as db:
        for table in tables:
            try:
                counts[table] = int(db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
            except sqlite3.Error:
                counts[table] = 0
    return counts


def curador_status_snapshot(workspace_root: Path, downloads_dir: Path) -> dict[str, object]:
    workspace_root = workspace_root.resolve()
    downloads_dir = downloads_dir.resolve()
    runtime_dir = workspace_root / "runtime" / "curador_seto"
    db_path = runtime_dir / "curador_index.sqlite"
    witness_path = workspace_root / "qa_artifacts" / "witness_log" / "curador_seto_witnesslog.jsonl"
    files = scan_downloads(downloads_dir, recursive=True)
    records = make_file_records(downloads_dir, files, workspace_root / "docs" / "intake" / "curador_fichas" / "downloads")
    groups = duplicate_groups(records, downloads_dir)
    counts = sqlite_table_counts(db_path)
    status_counts: dict[str, int] = {}
    lane_counts: dict[str, int] = {}
    if db_path.exists():
        with sqlite3.connect(db_path) as db:
            try:
                status_counts = dict(db.execute("SELECT status, COUNT(*) FROM files GROUP BY status").fetchall())
                lane_counts = dict(db.execute("SELECT lane, COUNT(*) FROM files GROUP BY lane").fetchall())
            except sqlite3.Error:
                status_counts = {}
                lane_counts = {}
    return {
        "generated_at_utc": utc_now(),
        "workspace_root": str(workspace_root),
        "downloads_dir": str(downloads_dir),
        "db_path": str(db_path),
        "master_index": str(workspace_root / "docs" / "intake" / "CURADOR_MASTER_INDEX.md"),
        "witness_log": str(witness_path),
        "witness_event_hash": previous_witness_hash(witness_path),
        "current_downloads_files": len(records),
        "current_downloads_duplicate_groups": len(groups),
        "sqlite_table_counts": counts,
        "sqlite_status_counts": status_counts,
        "sqlite_lane_counts": lane_counts,
    }


def load_pending_snapshot(workspace_root: Path) -> dict[str, object]:
    path = workspace_root / "qa_artifacts" / "pending" / "pending_review_latest.json"
    if not path.exists():
        return {"available": False, "path": str(path)}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"available": False, "path": str(path), "error": str(exc)}
    active = data.get("active_markdown", {}) if isinstance(data, dict) else {}
    claudio = data.get("claudio_master", {}) if isinstance(data, dict) else {}
    return {
        "available": True,
        "path": str(path),
        "generated_at": data.get("generated_at") if isinstance(data, dict) else None,
        "active_dedup_open": active.get("dedup_open") if isinstance(active, dict) else None,
        "active_by_blocker": active.get("by_blocker", {}) if isinstance(active, dict) else {},
        "active_by_lane": active.get("by_lane", {}) if isinstance(active, dict) else {},
        "claudio_dedup_open": claudio.get("dedup_open") if isinstance(claudio, dict) else None,
        "claudio_by_blocker": claudio.get("by_blocker", {}) if isinstance(claudio, dict) else {},
    }


def build_next_actions(status: dict[str, object], pending: dict[str, object]) -> list[dict[str, str]]:
    active_by_blocker = pending.get("active_by_blocker", {}) if isinstance(pending, dict) else {}
    local_candidates = 0
    if isinstance(active_by_blocker, dict):
        local_candidates = int(active_by_blocker.get("local_candidate", 0) or 0)
    current_dupes = int(status.get("current_downloads_duplicate_groups") or 0)
    actions = [
        {
            "priority": "P0",
            "lane": "curador_seto",
            "action_gate": "APPROVE_LOCAL",
            "title": "Mantener CuradorSETO-Downloads-Intake activo",
            "reason": f"Downloads tiene {status.get('current_downloads_files')} archivos vivos y {current_dupes} grupos duplicados exactos activos.",
            "next_step": "Usar el SQLite y CURADOR_MASTER_INDEX como verdad operativa de Downloads.",
        },
        {
            "priority": "P1",
            "lane": "pending_review",
            "action_gate": "APPROVE_LOCAL" if local_candidates else "REVIEW",
            "title": "Trabajar candidatos locales primero" if local_candidates else "No forzar pendientes gated como locales",
            "reason": f"pending_review reporta {local_candidates} candidatos locales; externos, legal, host-heavy y private_boundary siguen separados.",
            "next_step": "Elegir cierres locales con prueba directa y actualizar trackers, sin publicar ni mover fuentes."
            if local_candidates
            else "Convertir pendientes gated en subtareas locales solo cuando haya evidencia y frontera clara.",
        },
        {
            "priority": "P1",
            "lane": "global_curador",
            "action_gate": "REVIEW",
            "title": "Reemplazar escaneo global largo por auditoria incremental por root",
            "reason": "El refresco global completo puede exceder el tiempo operativo; Downloads ya se resolvio con indice incremental.",
            "next_step": "Agregar modo por root/resumible antes de repetir E:, Desktop y workspace completo.",
        },
        {
            "priority": "P1",
            "lane": "cleanup_migration",
            "action_gate": "REVIEW",
            "title": "Consolidar duplicados grandes solo con hash, ficha y canon",
            "reason": "El dry-run global previo encontro paquetes grandes y duplicados exactos, pero algunos son productos, builds, assets o fronteras privadas.",
            "next_step": "Procesar por lote: Asistente/FlujoCRM releases, vendors/cache, luego E: offload; borrar solo si ActionGate aprueba.",
        },
        {
            "priority": "P2",
            "lane": "claudio_wabisabi",
            "action_gate": "REVIEW",
            "title": "Conectar Curador SETO con Claudio/Wabi-Sabi como memoria operativa",
            "reason": "El Curador ya emite fichas, decisiones, sinapsis y WitnessLog; falta consumo directo por Hormiguero/Claudio.",
            "next_step": "Exponer lectura local del SQLite y del reporte de next-actions sin ejecutar mutaciones externas.",
        },
    ]
    if current_dupes:
        actions.insert(
            1,
            {
                "priority": "P0",
                "lane": "downloads",
                "action_gate": "APPROVE_LOCAL",
                "title": "Resolver duplicados exactos nuevos de Downloads",
                "reason": f"Se detectaron {current_dupes} grupos duplicados exactos activos.",
                "next_step": "Ejecutar curador_automation.py run con apply exact duplicates.",
            },
        )
    return actions


def render_next_actions_report(status: dict[str, object], pending: dict[str, object], actions: list[dict[str, str]]) -> str:
    table_counts = status.get("sqlite_table_counts", {})
    status_counts = status.get("sqlite_status_counts", {})
    by_blocker = pending.get("active_by_blocker", {}) if isinstance(pending, dict) else {}
    pending_source = "qa_artifacts/pending/pending_review_latest.json" if pending.get("available") else "missing"
    lines = [
        "# Curador SETO Next Actions",
        "",
        f"Pending source: `{pending_source}`",
        "",
        "Estado operativo para decidir el siguiente loop sin reescanear todo el sistema.",
        "",
        "## Downloads",
        "",
        "| metric | value |",
        "|---|---:|",
        f"| archivos vivos actuales | {status.get('current_downloads_files')} |",
        f"| duplicados exactos activos | {status.get('current_downloads_duplicate_groups')} |",
        f"| witness_event_hash | `{status.get('witness_event_hash')}` |",
        "",
        "## SQLite",
        "",
        "| table | rows |",
        "|---|---:|",
    ]
    if isinstance(table_counts, dict):
        for table in sorted(table_counts):
            lines.append(f"| `{table}` | {table_counts[table]} |")
    lines.extend(["", "## Status historico", "", "| status | rows |", "|---|---:|"])
    if isinstance(status_counts, dict):
        for key in sorted(status_counts):
            lines.append(f"| `{key}` | {status_counts[key]} |")
    lines.extend(["", "## Pendientes", "", "| blocker | dedup_count |", "|---|---:|"])
    if isinstance(by_blocker, dict):
        for key in sorted(by_blocker):
            lines.append(f"| `{key}` | {by_blocker[key]} |")
    lines.extend(["", "## Cola recomendada", "", "| priority | lane | gate | title | next step |", "|---|---|---|---|---|"])
    for item in actions:
        lines.append(
            f"| `{item['priority']}` | `{item['lane']}` | `{item['action_gate']}` | {item['title']} | {item['next_step']} |"
        )
    lines.extend(
        [
            "",
            "## Bloqueos",
            "",
            "- No publicar, hacer push, deploy, Gumroad, LinkedIn o Sponsors desde esta cola.",
            "- No borrar o mover material unico, privado, RPG/TCG, sesiones, secretos o claims fuertes.",
            "- No repetir el escaneo global completo si puede sustituirse por modo incremental por root.",
            "",
        ]
    )
    return "\n".join(lines)


def stable_next_actions_payload(value: object) -> object:
    if isinstance(value, dict):
        copy = {
            key: stable_next_actions_payload(item)
            for key, item in value.items()
            if key not in {"generated_at", "generated_at_utc"}
        }
        if "status" in copy and isinstance(copy["status"], dict):
            copy["status"] = {key: item for key, item in copy["status"].items() if key != "generated_at_utc"}
        return copy
    if isinstance(value, list):
        return [stable_next_actions_payload(item) for item in value]
    return value


def write_json_if_semantic_changed(path: Path, payload: dict[str, object]) -> None:
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if path.exists():
        try:
            old = json.loads(path.read_text(encoding="utf-8"))
            if stable_next_actions_payload(old) == stable_next_actions_payload(payload):
                return
        except (OSError, json.JSONDecodeError):
            pass
    path.write_text(text, encoding="utf-8")


def write_text_if_changed(path: Path, text: str) -> None:
    if path.exists():
        try:
            if path.read_text(encoding="utf-8") == text:
                return
        except OSError:
            pass
    path.write_text(text, encoding="utf-8")


def write_next_actions_report(workspace_root: Path, downloads_dir: Path) -> dict[str, object]:
    status = curador_status_snapshot(workspace_root, downloads_dir)
    pending = load_pending_snapshot(workspace_root)
    actions = build_next_actions(status, pending)
    report_path = workspace_root / "docs" / "pending" / f"CURADOR_SETO_NEXT_ACTIONS_{TODAY}.md"
    json_path = workspace_root / "qa_artifacts" / "pending" / f"curador_seto_next_actions_{TODAY}.json"
    payload = {
        "schema": "medioevo.curador_seto_next_actions.v1",
        "generated_at_utc": utc_now(),
        "status": status,
        "pending": pending,
        "next_actions": actions,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    write_text_if_changed(report_path, render_next_actions_report(status, pending, actions))
    write_json_if_semantic_changed(json_path, payload)
    payload["report_path"] = str(report_path)
    payload["json_path"] = str(json_path)
    return payload


def run_curador(
    *,
    workspace_root: Path,
    downloads_dir: Path,
    recursive: bool,
    write_index: bool,
    write_fichas_flag: bool,
    apply_exact_download_duplicates: bool,
) -> dict[str, object]:
    workspace_root = workspace_root.resolve()
    downloads_dir = downloads_dir.resolve()
    runtime_dir = workspace_root / "runtime" / "curador_seto"
    db_path = runtime_dir / "curador_index.sqlite"
    result_path = workspace_root / "qa_artifacts" / "release_validation" / f"curador-automation-downloads-result-{TODAY}.json"
    witness_path = workspace_root / "qa_artifacts" / "witness_log" / "curador_seto_witnesslog.jsonl"
    files = scan_downloads(downloads_dir, recursive=recursive)
    records = make_file_records(downloads_dir, files, workspace_root / "docs" / "intake" / "curador_fichas" / "downloads")
    groups = duplicate_groups(records, downloads_dir)
    if (
        not groups
        and stored_current_snapshot(db_path) == current_snapshot(records)
        and curador_outputs_exist(workspace_root, db_path, write_index, write_fichas_flag)
    ):
        return no_change_result(
            workspace_root=workspace_root,
            downloads_dir=downloads_dir,
            db_path=db_path,
            witness_path=witness_path,
            records=records,
        )
    if write_fichas_flag:
        write_fichas(workspace_root, records)
    deleted = delete_exact_duplicates(downloads_dir, groups, records, apply_delete=apply_exact_download_duplicates)
    previous = previous_witness_hash(witness_path)
    event: dict[str, object] = {
        "timestamp_utc": utc_now(),
        "event_type": "curador_downloads_automation_run",
        "actor": "tools/release/curador_automation.py",
        "previous_hash": previous,
        "action_gate": "REVIEW",
        "summary": {
            "downloads_files_seen": len(records),
            "duplicate_groups_detected": len(groups),
            "deleted_exact_duplicates": sum(1 for item in deleted if item["deleted"]),
            "apply_delete": apply_exact_download_duplicates,
        },
    }
    event["event_hash"] = event_hash(event)
    write_sqlite(db_path, records, groups, event)
    if write_index:
        index_path = workspace_root / "docs" / "intake" / "CURADOR_MASTER_INDEX.md"
        index_path.write_text(render_master_index(records, groups, deleted, db_path), encoding="utf-8")
    write_runtime_export(runtime_dir, records, groups, deleted)
    result = {
        "generated_at_utc": utc_now(),
        "workspace_root": str(workspace_root),
        "downloads_dir": str(downloads_dir),
        "db_path": str(db_path),
        "master_index": str(workspace_root / "docs" / "intake" / "CURADOR_MASTER_INDEX.md"),
        "witness_log": str(witness_path),
        "witness_event_hash": event["event_hash"],
        "downloads_files_seen": len(records),
        "duplicate_groups_detected": len(groups),
        "deleted_exact_duplicates": sum(1 for item in deleted if item["deleted"]),
        "deleted_bytes": sum(int(item["bytes"]) for item in deleted if item["deleted"]),
        "new_folder_files_registered": sum(1 for record in records if record.rel_path.lower().startswith("new folder/")),
        "blocked_records": sum(1 for record in records if record.action_gate == "BLOCK"),
        "status_counts": {},
        "duplicate_groups": groups,
        "deleted": deleted,
    }
    for record in records:
        result["status_counts"][record.status] = result["status_counts"].get(record.status, 0) + 1
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    write_deleted_log(workspace_root, deleted, result_path)
    append_witness(witness_path, event)
    return result


def install_task(workspace_root: Path) -> dict[str, object]:
    task_name = "CuradorSETO-Downloads-Intake"
    python_exe = sys.executable
    wrapper = Path.home() / "curador_seto_downloads.cmd"
    wrapper.write_text(
        "\n".join(
            [
                "@echo off",
                f'cd /d "{workspace_root}"',
                f'"{python_exe}" tools\\release\\curador_automation.py run --root downloads --recursive --write-index --write-fichas --apply-exact-download-duplicates',
                "",
            ]
        ),
        encoding="utf-8",
    )
    command = str(wrapper)
    args = [
        "schtasks",
        "/Create",
        "/TN",
        task_name,
        "/TR",
        command,
        "/SC",
        "MINUTE",
        "/MO",
        "30",
        "/F",
    ]
    result = subprocess.run(args, text=True, capture_output=True)
    return {
        "task_name": task_name,
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "command": command,
        "wrapper": str(wrapper),
    }


def main() -> int:
    configure_stdout()
    parser = argparse.ArgumentParser(description="Curador SETO automation for Downloads.")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--root", choices=["downloads"], default="downloads")
    run.add_argument("--workspace-root", default=str(ROOT))
    run.add_argument("--downloads-dir", default=str(DEFAULT_DOWNLOADS))
    run.add_argument("--recursive", action="store_true")
    run.add_argument("--write-index", action="store_true")
    run.add_argument("--write-fichas", action="store_true")
    run.add_argument("--apply-exact-download-duplicates", action="store_true")
    install = sub.add_parser("install-task")
    install.add_argument("--workspace-root", default=str(ROOT))
    status = sub.add_parser("status")
    status.add_argument("--workspace-root", default=str(ROOT))
    status.add_argument("--downloads-dir", default=str(DEFAULT_DOWNLOADS))
    status.add_argument("--write-next-actions", action="store_true")
    args = parser.parse_args()

    if args.command == "install-task":
        data = install_task(Path(args.workspace_root).resolve())
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0 if data["returncode"] == 0 else 1

    if args.command == "status":
        if args.write_next_actions:
            data = write_next_actions_report(Path(args.workspace_root).resolve(), Path(args.downloads_dir).resolve())
        else:
            data = {
                "status": curador_status_snapshot(Path(args.workspace_root).resolve(), Path(args.downloads_dir).resolve()),
                "pending": load_pending_snapshot(Path(args.workspace_root).resolve()),
            }
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    data = run_curador(
        workspace_root=Path(args.workspace_root).resolve(),
        downloads_dir=Path(args.downloads_dir).resolve(),
        recursive=args.recursive,
        write_index=args.write_index,
        write_fichas_flag=args.write_fichas,
        apply_exact_download_duplicates=args.apply_exact_download_duplicates,
    )
    print(json.dumps({key: data[key] for key in [
        "downloads_files_seen",
        "duplicate_groups_detected",
        "deleted_exact_duplicates",
        "deleted_bytes",
        "new_folder_files_registered",
        "blocked_records",
        "witness_event_hash",
    ]}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
