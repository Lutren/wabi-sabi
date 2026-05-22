from __future__ import annotations

import hashlib
import json
import tarfile
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from wabi_sabi.core.cerebro_line_audit import TEXT_EXTENSIONS, _line_signals, _slug


ARCHIVE_INTAKE_SCHEMA = "wabi.cerebro_archive_intake.v1"
DEFAULT_ARCHIVE_REL = (
    Path("-=MEDIOEVO=-")
    / "-=LIBROS"
    / "-=CEREBRO=-"
    / "-=PSI=-"
    / "ReplitExport-lutren.tar.gz"
)
DEFAULT_OUTPUT_REL = Path("runtime") / "cerebro_archive_intake"
MAX_TEXT_BYTES = 750_000
SECRET_MARKERS = (
    ".env",
    "secret",
    "token",
    "credential",
    "password",
    "private_key",
    "apikey",
    "api_key",
)
BLOCKED_PARTS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "__pycache__",
    "node_modules",
    "target",
    "dist",
    "build",
}


@dataclass(frozen=True)
class ArchiveMember:
    name: str
    size: int
    is_file: bool


def run_archive_intake(
    workspace: str | Path,
    *,
    archive_path: str | Path | None = None,
    output_root: str | Path | None = None,
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    archive = _resolve_archive(workspace_path, archive_path)
    output_base = Path(output_root).resolve() if output_root else workspace_path / DEFAULT_OUTPUT_REL
    archive_hash = _sha256_file(archive)
    intake_id = f"{archive.stem.replace('.', '_')}_{archive_hash[:12]}"
    output_dir = output_base / intake_id
    text_dir = output_dir / "text"
    output_dir.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)

    manifest: list[dict[str, Any]] = []
    text_records: list[dict[str, Any]] = []
    classification_counts: dict[str, int] = {}
    signal_counts: dict[str, int] = {}

    with _open_archive(archive) as opened:
        for member in opened.members():
            record = _member_record(member)
            if not member.is_file:
                record["classification"] = "DIRECTORY"
                _count(classification_counts, record["classification"])
                manifest.append(record)
                continue
            classification, reasons = _classify_member(member)
            record["classification"] = classification
            record["reasons"] = reasons
            _count(classification_counts, classification)
            if classification == "TEXT_INDEXABLE":
                raw = opened.read(member)
                text = raw.decode("utf-8", errors="replace")
                lines = text.splitlines()
                member_signals: dict[str, int] = {}
                for line in lines:
                    for signal in _line_signals(line):
                        _count(member_signals, signal)
                        _count(signal_counts, signal)
                text_path = text_dir / f"{hashlib.sha256(member.name.encode('utf-8')).hexdigest()[:12]}_{_slug(Path(member.name).name)}.txt"
                text_path.write_text(text, encoding="utf-8")
                record.update(
                    {
                        "line_count": len(lines),
                        "signals": member_signals,
                        "quarantine_text": str(text_path),
                        "sha256_text": hashlib.sha256(raw).hexdigest(),
                    }
                )
                text_records.append(
                    {
                        "member": member.name,
                        "line_count": len(lines),
                        "signals": member_signals,
                        "quarantine_text": str(text_path),
                    }
                )
            manifest.append(record)

    payload: dict[str, Any] = {
        "schema": ARCHIVE_INTAKE_SCHEMA,
        "ok": True,
        "generated_at_utc": _utc_now(),
        "workspace": str(workspace_path),
        "archive": str(archive),
        "archive_sha256": archive_hash,
        "output_dir": str(output_dir),
        "policy": {
            "source_writes": False,
            "raw_archive_extract": False,
            "text_quarantine_extract": True,
            "blocked_parts": sorted(BLOCKED_PARTS),
            "secret_like_paths_blocked": True,
            "max_text_bytes": MAX_TEXT_BYTES,
        },
        "summary": {
            "member_count": len(manifest),
            "file_count": sum(1 for item in manifest if item.get("is_file")),
            "text_indexed_count": len(text_records),
            "classification_counts": dict(sorted(classification_counts.items())),
            "signal_counts": dict(sorted(signal_counts.items(), key=lambda item: (-item[1], item[0]))),
        },
        "manifest": manifest,
        "text_records": text_records,
        "certainty": [
            "Archive source was not moved, deleted or extracted raw into the workspace.",
            "Text-like non-secret members were copied into a quarantine text directory for review.",
            "Git metadata, path traversal, secret-like paths and large/binary files were blocked from text extraction.",
        ],
        "inference": [
            "Indexed text members can feed module review, but import into runtime still requires per-file review and tests.",
        ],
        "unknown": [
            "Binary files and blocked metadata were inventoried but not semantically absorbed.",
            "Quarantined text may still require human/agent review before becoming canon or production code.",
        ],
    }
    payload["artifacts"] = write_archive_intake_outputs(payload, output_dir)
    return payload


def write_archive_intake_outputs(payload: dict[str, Any], output_dir: str | Path) -> list[str]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    manifest_path = output_path / "ARCHIVE_MEMBER_MANIFEST.jsonl"
    text_path = output_path / "ARCHIVE_TEXT_INDEX.jsonl"
    report_path = output_path / "ARCHIVE_INTAKE_REPORT.md"
    payload_path = output_path / "ARCHIVE_INTAKE_PAYLOAD.json"
    manifest_path.write_text(
        "\n".join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in payload.get("manifest", [])) + "\n",
        encoding="utf-8",
    )
    text_path.write_text(
        "\n".join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in payload.get("text_records", [])) + "\n",
        encoding="utf-8",
    )
    report_path.write_text(_archive_report_markdown(payload), encoding="utf-8")
    compact = dict(payload)
    compact["manifest_sample"] = compact.pop("manifest", [])[:80]
    compact["text_records_sample"] = compact.pop("text_records", [])[:80]
    payload_path.write_text(json.dumps(compact, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    return [str(manifest_path), str(text_path), str(report_path), str(payload_path)]


def compact_archive_intake_payload(payload: dict[str, Any]) -> dict[str, Any]:
    compact = dict(payload)
    compact["manifest_sample"] = compact.pop("manifest", [])[:30]
    compact["text_records_sample"] = compact.pop("text_records", [])[:30]
    return compact


def _resolve_archive(workspace: Path, archive_path: str | Path | None) -> Path:
    raw = Path(archive_path) if archive_path else DEFAULT_ARCHIVE_REL
    candidates = [raw] if raw.is_absolute() else [workspace / raw, raw]
    for candidate in candidates:
        path = candidate.resolve()
        if path.exists() and path.is_file():
            return path
    raise FileNotFoundError(str(archive_path or DEFAULT_ARCHIVE_REL))


class _OpenedArchive:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._zip: zipfile.ZipFile | None = None
        self._tar: tarfile.TarFile | None = None

    def __enter__(self) -> "_OpenedArchive":
        if self.path.suffix.lower() == ".zip":
            self._zip = zipfile.ZipFile(self.path)
        else:
            self._tar = tarfile.open(self.path, "r:*")
        return self

    def __exit__(self, *args: object) -> None:
        if self._zip:
            self._zip.close()
        if self._tar:
            self._tar.close()

    def members(self) -> Iterable[ArchiveMember]:
        if self._zip:
            for info in self._zip.infolist():
                yield ArchiveMember(name=info.filename, size=info.file_size, is_file=not info.is_dir())
            return
        if self._tar:
            for member in self._tar.getmembers():
                yield ArchiveMember(name=member.name, size=member.size, is_file=member.isfile())

    def read(self, member: ArchiveMember) -> bytes:
        if self._zip:
            return self._zip.read(member.name)
        if self._tar:
            assert self._tar is not None
            extracted = self._tar.extractfile(member.name)
            if extracted is None:
                return b""
            with extracted:
                return extracted.read()
        return b""


def _open_archive(path: Path) -> _OpenedArchive:
    return _OpenedArchive(path)


def _classify_member(member: ArchiveMember) -> tuple[str, list[str]]:
    reasons: list[str] = []
    normalized = member.name.replace("\\", "/")
    posix = PurePosixPath(normalized)
    lower = normalized.lower()
    parts = [part.lower() for part in posix.parts]
    if posix.is_absolute() or any(part == ".." for part in parts):
        return "PATH_TRAVERSAL_BLOCK", ["unsafe_member_path"]
    if any(part in BLOCKED_PARTS for part in parts):
        return "BLOCKED_METADATA_OR_CACHE", ["blocked_part"]
    if any(marker in lower for marker in SECRET_MARKERS):
        return "SECRET_LIKE_BLOCK", ["secret_like_path"]
    if member.size > MAX_TEXT_BYTES:
        return "SKIP_REVIEW", ["too_large_for_text_quarantine"]
    suffix = Path(posix.name).suffix.lower()
    if suffix in TEXT_EXTENSIONS or not suffix:
        return "TEXT_INDEXABLE", []
    return "BINARY_REVIEW", ["non_text_extension"]


def _member_record(member: ArchiveMember) -> dict[str, Any]:
    return {
        "name": member.name,
        "size_bytes": member.size,
        "is_file": member.is_file,
        "classification": "",
        "reasons": [],
        "line_count": 0,
        "signals": {},
        "quarantine_text": "",
        "sha256_text": "",
    }


def _archive_report_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    counts = summary.get("classification_counts", {})
    signal_counts = summary.get("signal_counts", {})
    lines = [
        "# Archive Intake Report",
        "",
        "CERTEZA:",
        "- Source archive was not moved, deleted or raw-extracted into the workspace.",
        "- Text-like safe members were copied to quarantine text files under this report directory.",
        "- Secret-like paths, `.git`, caches, path traversal, oversized and binary members were blocked from text extraction.",
        "",
        "INFERENCIA:",
        "- This is enough for review and routing; it is not an import into production runtime.",
        "",
        "INCOGNITA:",
        "- Blocked/binary members still need specialized review if a claim depends on them.",
        "",
        "## Archive",
        "",
        f"- Path: `{payload.get('archive')}`",
        f"- SHA256: `{payload.get('archive_sha256')}`",
        f"- Output: `{payload.get('output_dir')}`",
        "",
        "## Counts",
        "",
        f"- Members: `{summary.get('member_count', 0)}`",
        f"- Files: `{summary.get('file_count', 0)}`",
        f"- Text indexed: `{summary.get('text_indexed_count', 0)}`",
    ]
    for name, count in counts.items():
        lines.append(f"- `{name}`: {count}")
    lines.extend(["", "## Top Signals", ""])
    for name, count in list(signal_counts.items())[:20]:
        lines.append(f"- `{name}`: {count}")
    if not signal_counts:
        lines.append("- none")
    lines.extend(["", "## Next Action", ""])
    lines.append("- Review quarantined text records and select only owned, tested modules for any runtime import.")
    return "\n".join(lines) + "\n"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _count(counter: dict[str, int], key: str) -> None:
    counter[key] = counter.get(key, 0) + 1


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
