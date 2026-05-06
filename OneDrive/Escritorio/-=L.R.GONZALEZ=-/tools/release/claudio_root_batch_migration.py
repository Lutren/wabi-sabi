from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

try:
    from .claudio_root_human_audit import build_audit
except ImportError:  # pragma: no cover - direct script execution
    from claudio_root_human_audit import build_audit


ROOT = Path(__file__).resolve().parents[2]

SAFE_MOVE_CATEGORIES = {
    "launcher_script": "tools/launchers",
    "root_document": "docs/root_notes_review",
    "root_media_or_ui": "assets/root_media_review",
    "root_python_script": "tools/root_scripts_review",
}


@dataclass
class MoveEntry:
    name: str
    category: str
    source: str
    destination: str
    sha256: str | None
    size_bytes: int
    git_state: str
    action: str
    applied: bool
    reason: str
    rollback: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def ensure_under(root: Path, target: Path) -> Path:
    root_resolved = root.resolve()
    target_resolved = target.resolve()
    try:
        target_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"target escapes root: {target}") from exc
    return target_resolved


def git_state(path: Path, root: Path) -> str:
    rel_path = str(path.relative_to(root)).replace("\\", "/")
    result = subprocess.run(
        ["git", "status", "--short", "--", rel_path],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    if result.returncode != 0:
        return "unknown"
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if not lines:
        return "tracked_clean_or_ignored"
    marker = lines[0][:2]
    if marker == "??":
        return "untracked"
    if any(flag in marker for flag in ("M", "A", "D", "R")):
        return "tracked_dirty"
    return "tracked_other"


def collision_safe_destination(source: Path, destination_dir: Path) -> Path:
    target = destination_dir / source.name
    if not target.exists():
        return target
    source_hash = sha256_file(source)
    if target.is_file() and sha256_file(target) == source_hash:
        return target
    return destination_dir / f"{source.stem or source.name}__DUP_{source_hash[:8]}{source.suffix}"


def write_readme(destination_dir: Path, category: str) -> None:
    readme = destination_dir / "00_LEER_PRIMERO.md"
    if readme.exists():
        return
    labels = {
        "launcher_script": "Launchers raiz",
        "root_document": "Documentos raiz",
        "root_media_or_ui": "Assets y UI raiz",
        "root_python_script": "Scripts Python raiz",
    }
    label = labels.get(category, "Archivo raiz")
    readme.write_text(
        "\n".join(
            [
                f"# {label} De Claudio",
                "",
                "Esta carpeta contiene archivos retirados del root visible de Claudio",
                "para que humanos y agentes puedan orientarse sin ruido.",
                "",
                "Reglas:",
                "",
                "- No borrar desde aqui sin ficha, hash y decision de gate.",
                "- Consolidar hacia canon o runtime solo despues de lectura.",
                "- Si algo debe volver a la raiz, usar el manifest de rollback.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def build_entries(
    target_root: Path,
    category: str,
    limit: int | None,
    include_tracked_clean: bool,
) -> list[MoveEntry]:
    if category not in SAFE_MOVE_CATEGORIES:
        raise ValueError(f"unsupported or unsafe category: {category}")
    root = target_root.resolve()
    payload = build_audit(root)
    destination_dir = ensure_under(root, root / SAFE_MOVE_CATEGORIES[category])
    entries: list[MoveEntry] = []
    move_seen = 0
    for record in payload["records"]:  # type: ignore[index]
        if record["category"] != category:
            continue
        source = ensure_under(root, root / record["name"])
        if not source.exists() or source.is_dir():
            continue
        state = git_state(source, root)
        sha = sha256_file(source)
        size = source.stat().st_size
        if state != "untracked" and not include_tracked_clean:
            entries.append(
                MoveEntry(
                    name=record["name"],
                    category=category,
                    source=str(source),
                    destination=str(destination_dir / source.name),
                    sha256=sha,
                    size_bytes=size,
                    git_state=state,
                    action="SKIP",
                    applied=False,
                    reason="tracked_or_unknown_state_requires_explicit_include",
                    rollback="n/a",
                )
            )
            continue
        target = collision_safe_destination(source, destination_dir)
        entries.append(
            MoveEntry(
                name=record["name"],
                category=category,
                source=str(source),
                destination=str(target),
                sha256=sha,
                size_bytes=size,
                git_state=state,
                action="MOVE",
                applied=False,
                reason=record["reason"],
                rollback=f"Move-Item -LiteralPath {json.dumps(str(target))} -Destination {json.dumps(str(source))}",
            )
        )
        move_seen += 1
        if limit is not None and move_seen >= limit:
            break
    return entries


def apply_entries(entries: list[MoveEntry], category: str) -> None:
    for entry in entries:
        if entry.action != "MOVE":
            continue
        source = Path(entry.source)
        destination = Path(entry.destination)
        if not source.exists() and destination.exists():
            entry.action = "ALREADY_MOVED"
            entry.reason = "source_missing_destination_present"
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        write_readme(destination.parent, category)
        source.rename(destination)
        entry.applied = True


def render_markdown(payload: dict[str, object]) -> str:
    summary = payload["summary"]  # type: ignore[assignment]
    lines = [
        f"# Claudio Root Batch Migration - {payload['category']}",
        "",
        f"Generated UTC: `{payload['generated_at_utc']}`",
        f"Target root: `{payload['target_root']}`",
        f"Apply: `{payload['apply']}`",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():  # type: ignore[union-attr]
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Entries",
            "",
            "| action | applied | git_state | name | destination | sha256 |",
            "|---|---:|---|---|---|---|",
        ]
    )
    for entry in payload["entries"]:  # type: ignore[assignment]
        lines.append(
            f"| `{entry['action']}` | `{entry['applied']}` | `{entry['git_state']}` | "
            f"`{entry['name']}` | `{entry['destination']}` | `{entry['sha256'] or 'n/a'}` |"
        )
    lines.extend(
        [
            "",
            "## Rollback",
            "",
            "Use the JSON manifest for exact source/destination pairs. Roll back only if",
            "the destination hash still matches the recorded SHA256.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(payload: dict[str, object], output_dir: Path, label: str) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{label}.json"
    md_path = output_dir / f"{label}.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create/apply safe Claudio root batch move manifests.")
    parser.add_argument("--target-root", required=True)
    parser.add_argument("--category", choices=sorted(SAFE_MOVE_CATEGORIES), required=True)
    parser.add_argument("--output-dir", default=str(ROOT / "docs" / "intake"))
    parser.add_argument("--label", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--include-tracked-clean", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = parse_args(argv)
    target_root = Path(args.target_root).resolve()
    entries = build_entries(target_root, args.category, args.limit, args.include_tracked_clean)
    if args.apply:
        apply_entries(entries, args.category)
    payload = {
        "schema": "medioevo.claudio_root_batch_migration.v1",
        "generated_at_utc": utc_now(),
        "target_root": str(target_root),
        "category": args.category,
        "destination_hint": SAFE_MOVE_CATEGORIES[args.category],
        "apply": bool(args.apply),
        "summary": {
            "entries": len(entries),
            "move_count": sum(1 for entry in entries if entry.action == "MOVE"),
            "applied_count": sum(1 for entry in entries if entry.applied),
            "skipped_count": sum(1 for entry in entries if entry.action == "SKIP"),
        },
        "entries": [asdict(entry) for entry in entries],
    }
    label = args.label or f"claudio_root_batch_{args.category}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    paths = write_outputs(payload, Path(args.output_dir).resolve(), label)
    result = {"summary": payload["summary"], "paths": paths}
    print(json.dumps(result if args.json else payload["summary"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
