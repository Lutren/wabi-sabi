from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from _common import (
    BINARY_SUFFIXES,
    DENY_SUBSTRINGS,
    PRODUCTS,
    PRIVATE_GAME_SUBSTRINGS,
    ROOT,
    SECRET_NAME_MARKERS,
    add_common_args,
    collect_product_files,
    ensure_under_root,
    is_denied,
    is_private_game,
    is_secret_named,
    iter_files,
    print_json,
    product_by_name,
    rel,
    validate_root_arg,
)


PATTERNS = [
    re.compile(r"(api[_-]?key|secret|token|password|passwd|private[_-]?key)\s*[:=]\s*[\"']?[^\s\"']{8,}", re.I),
    re.compile(r"bearer\s+[a-z0-9._-]+", re.I),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{16,}"),
]
SECRET_NAME_ALLOWLIST = {"scan_secrets.py", "SECRET_SCAN_REPORT.md", "secret_scan_report.schema.json"}


def is_code_placeholder_assignment(path: Path | None, line: str, match: re.Match[str]) -> bool:
    if path is not None and path.suffix.lower() != ".py":
        return False
    fragment = match.group(0)
    separator = ":" if ":" in fragment else "=" if "=" in fragment else ""
    if not separator:
        return False
    value = fragment.split(separator, 1)[1].strip().strip(",")
    value = value.strip("\"'").rstrip(",)]")
    if not value:
        return False
    if "(" in value or "." in value:
        return True
    return value.isidentifier() or value in {"None", "True", "False"}


def scan_text(path, max_bytes: int) -> list[str]:
    if path.suffix.lower() in BINARY_SUFFIXES or path.stat().st_size > max_bytes:
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    hits = []
    for line in text.splitlines():
        for pattern in PATTERNS:
            match = pattern.search(line)
            if match and not is_code_placeholder_assignment(path, line, match):
                hits.append(pattern.pattern)
    return hits


def scan_text_value(text: str) -> list[str]:
    hits = []
    for line in text.splitlines():
        for pattern in PATTERNS:
            match = pattern.search(line)
            if match and not is_code_placeholder_assignment(None, line, match):
                hits.append(pattern.pattern)
    return hits


def finding_for_file(path: Path, max_bytes: int) -> dict[str, object] | None:
    reasons = []
    if path.name not in SECRET_NAME_ALLOWLIST and is_secret_named(path):
        reasons.append("secret-like filename")
    content_hits = scan_text(path, max_bytes)
    if content_hits:
        reasons.append("secret-like content markers")
    if not reasons:
        return None
    return {"path": rel(path), "reasons": sorted(set(reasons))}


def zip_member_is_denied(name: str) -> bool:
    value = "/" + name.replace("\\", "/").lower().lstrip("/")
    return any(marker in value for marker in DENY_SUBSTRINGS)


def zip_member_is_private_game(name: str) -> bool:
    value = "/" + name.replace("\\", "/").lower().lstrip("/")
    return any(marker in value for marker in PRIVATE_GAME_SUBSTRINGS)


def zip_member_is_secret_named(name: str) -> bool:
    value = "/" + name.replace("\\", "/").lower().lstrip("/")
    filename = Path(name).name.lower()
    return any(marker in filename or marker in value for marker in SECRET_NAME_MARKERS)


def zip_member_is_binary(name: str) -> bool:
    return Path(name).suffix.lower() in BINARY_SUFFIXES


def finding_for_zip(path: Path, max_bytes: int, limit_remaining: int) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    try:
        with ZipFile(path) as archive:
            for info in archive.infolist():
                if len(findings) >= limit_remaining:
                    break
                name = info.filename
                if not name or name.endswith("/"):
                    continue
                reasons = []
                if name.startswith("/") or ".." in Path(name).parts:
                    reasons.append("unsafe zip member path")
                if zip_member_is_private_game(name):
                    reasons.append("private game path")
                if zip_member_is_denied(name):
                    reasons.append("denylist path")
                if zip_member_is_secret_named(name):
                    reasons.append("secret-like filename")
                if not zip_member_is_binary(name) and info.file_size <= max_bytes:
                    try:
                        text = archive.read(info).decode("utf-8", errors="ignore")
                    except (KeyError, OSError):
                        text = ""
                    if scan_text_value(text):
                        reasons.append("secret-like content markers")
                if reasons:
                    findings.append(
                        {
                            "path": f"{rel(path)}::{name}",
                            "reasons": sorted(set(reasons)),
                        }
                    )
    except BadZipFile:
        findings.append({"path": rel(path), "reasons": ["invalid zip artifact"]})
    return findings


def files_under_path(raw_path: str) -> tuple[list[Path], list[dict[str, object]]]:
    path = Path(raw_path)
    target = path if path.is_absolute() else ROOT / path
    try:
        resolved = ensure_under_root(target)
    except ValueError as exc:
        return [], [{"path": str(target), "reasons": [str(exc)]}]
    if not resolved.exists():
        return [], [{"path": rel(resolved), "reasons": ["missing path"]}]
    if is_private_game(resolved):
        return [], [{"path": rel(resolved), "reasons": ["private game path"]}]
    if is_denied(resolved):
        return [], [{"path": rel(resolved), "reasons": ["denylist path"]}]
    if resolved.is_file():
        return [resolved], []

    files: list[Path] = []
    findings: list[dict[str, object]] = []
    for base, dirs, names in os.walk(resolved):
        base_path = Path(base)
        kept_dirs = []
        for name in dirs:
            child = base_path / name
            if is_private_game(child):
                findings.append({"path": rel(child), "reasons": ["private game path"]})
            elif is_denied(child):
                continue
            elif is_secret_named(child):
                findings.append({"path": rel(child), "reasons": ["secret-like directory name"]})
            else:
                kept_dirs.append(name)
        dirs[:] = kept_dirs
        for name in names:
            child = base_path / name
            if is_private_game(child):
                findings.append({"path": rel(child), "reasons": ["private game path"]})
            elif is_denied(child):
                continue
            else:
                files.append(child)
    return files, findings


def artifact_file(raw_path: str) -> tuple[list[Path], list[dict[str, object]]]:
    path = Path(raw_path)
    target = path if path.is_absolute() else ROOT / path
    try:
        resolved = ensure_under_root(target)
    except ValueError as exc:
        return [], [{"path": str(target), "reasons": [str(exc)]}]
    if not resolved.exists():
        return [], [{"path": rel(resolved), "reasons": ["missing artifact"]}]
    if not resolved.is_file():
        return [], [{"path": rel(resolved), "reasons": ["artifact must be a file"]}]
    return [resolved], []


def selected_targets(args: argparse.Namespace) -> tuple[list[Path], list[dict[str, object]]]:
    files: list[Path] = []
    findings: list[dict[str, object]] = []
    for name in args.product or []:
        product = product_by_name(name)
        allowed, blocked, _excluded = collect_product_files(product)
        files.extend(allowed)
        for path, reason in blocked:
            findings.append({"path": path, "reasons": [f"blocked by product manifest: {reason}"]})
    for raw_path in args.path or []:
        path_files, path_findings = files_under_path(raw_path)
        files.extend(path_files)
        findings.extend(path_findings)
    for raw_path in args.artifact or []:
        artifact_files, artifact_findings = artifact_file(raw_path)
        files.extend(artifact_files)
        findings.extend(artifact_findings)
    unique: dict[str, Path] = {}
    for path in files:
        unique[str(path.resolve())] = path
    return list(unique.values()), findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan for secret-like files and content without printing values.")
    add_common_args(parser)
    parser.add_argument("--product", choices=[p.name for p in PRODUCTS], action="append", help="scan one allowlisted product/artifact")
    parser.add_argument("--path", action="append", help="scan one path under the workspace root")
    parser.add_argument("--artifact", action="append", help="scan one release artifact file under the workspace root, including ZIP members")
    parser.add_argument("--max-bytes", type=int, default=300_000)
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--fail-on-findings", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)

    findings = []
    if args.product or args.path or args.artifact:
        scan_files, findings = selected_targets(args)
    else:
        scan_files = list(iter_files(include_denied=False))

    for path in scan_files:
        if is_private_game(path):
            continue
        if path.suffix.lower() == ".zip":
            findings.extend(finding_for_zip(path, args.max_bytes, args.limit - len(findings)))
        else:
            item = finding_for_file(path, args.max_bytes)
            if item:
                findings.append(item)
        if len(findings) >= args.limit:
            break

    data = {
        "scope": {
            "products": args.product or [],
            "paths": args.path or [],
            "artifacts": args.artifact or [],
            "default_workspace_scan": not (args.product or args.path or args.artifact),
        },
        "findings": findings[: args.limit],
        "count_reported": min(len(findings), args.limit),
        "truncated_at": args.limit,
    }
    if args.json:
        print_json(data)
    else:
        print(f"reported findings: {len(findings)}")
        for item in findings:
            print(f"- {item['path']} :: {', '.join(item['reasons'])}")
    return 1 if args.fail_on_findings and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
