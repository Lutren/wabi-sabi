from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from _common import ROOT, print_json


TODAY = "2026-05-05"
DEFAULT_MANIFEST = ROOT / "qa_artifacts" / "release_validation" / f"global-curador-file-manifest-{TODAY}.csv"
DEFAULT_JSON = ROOT / "qa_artifacts" / "release_validation" / f"seto-exact-duplicate-candidates-{TODAY}.json"
DEFAULT_REPORT = ROOT / "docs" / "intake" / f"SETO_EXACT_DUPLICATE_CANDIDATES_{TODAY}.md"

LOW_RISK_EXTENSIONS = {
    ".bat",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".txt",
    ".yaml",
    ".yml",
}
BLOCK_MARKERS = {
    "/.git/",
    "/node_modules/",
    "/.venv",
    "/venv/",
    "/env/",
    "/.skills/",
    "/_archive",
    "/_archivar",
    "/tools/vendor/",
    "/tools/pentest_repos/",
    "/github-modules/",
    "/release/",
    "/releases/",
    "/qa_artifacts/",
    "/publish_staging/",
    "/.claw/",
    "/.claude/",
    "/.wrangler/",
    "/metaevo-tcg/",
    "/tcg/",
    "/runtime/game_bridge/",
    "/game-private/",
    "/04_audiovisual_y_tcg/",
    "/appdata/",
    "/downloads/",
    "/desktop/",
    "/e:/",
}
SECRET_MARKERS = {
    ".env",
    "secret",
    "token",
    "credential",
    "api_key",
    "apikey",
    "private_key",
    "gumroad_api",
    "stripe",
    "discord_token",
    "youtube_token",
    "settings.local.json",
}
CANON_HINTS = (
    "/docs/",
    "/canon/",
    "/packages/",
    "/apps/",
    "/website/",
    "/tools/",
    "/-=psi=-/",
)
SOURCE_HINTS = (
    "/downloads/",
    "/desktop/",
    "/escritorio/",
)
BOILERPLATE_NAMES = {
    ".gitignore",
    "__init__.py",
    "code_of_conduct.md",
    "contributing.md",
    "copying",
    "funding.yml",
    "license",
    "license.md",
    "license.txt",
    "readme.md",
    "security.md",
    "third_party_notices.md",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def norm(value: str) -> str:
    return value.replace("\\", "/").lower()


def row_path(row: dict[str, str]) -> str:
    return row.get("path", "")


def row_rel(row: dict[str, str]) -> str:
    return row.get("rel_to_workspace") or row_path(row)


def path_has_marker(row: dict[str, str], markers: set[str]) -> bool:
    value = "/" + norm(row_path(row)).lstrip("/")
    name = norm(row.get("name", ""))
    return any(marker in value or marker in name for marker in markers)


def parse_size(row: dict[str, str]) -> int:
    try:
        return int(row.get("size_bytes", "0") or 0)
    except ValueError:
        return 0


def is_low_risk_row(row: dict[str, str], max_bytes: int) -> bool:
    if row.get("root") != "workspace_lrgonzalez":
        return False
    if row.get("hash_status") != "hashed":
        return False
    if row.get("action_gate") == "BLOCK":
        return False
    if parse_size(row) <= 0 or parse_size(row) > max_bytes:
        return False
    if path_has_marker(row, BLOCK_MARKERS | SECRET_MARKERS):
        return False
    if row.get("extension", "").lower() not in LOW_RISK_EXTENSIONS:
        return False
    name = row.get("name", "").lower()
    if name in BOILERPLATE_NAMES:
        return False
    if "license" in name or name.startswith(".claude") or name.startswith(".claw"):
        return False
    return True


def canonical_score(row: dict[str, str]) -> tuple[int, str]:
    value = "/" + norm(row_path(row)).lstrip("/")
    score = 0
    if row.get("registered") == "yes":
        score += 100
    if row.get("root") == "workspace_lrgonzalez":
        score += 40
    if any(hint in value for hint in CANON_HINTS):
        score += 25
    if any(hint in value for hint in SOURCE_HINTS):
        score -= 10
    if "new folder" in value:
        score -= 20
    return (-score, value)


def compact_row(row: dict[str, str]) -> dict[str, object]:
    return {
        "path": row_path(row),
        "rel_to_workspace": row_rel(row),
        "root": row.get("root", ""),
        "name": row.get("name", ""),
        "extension": row.get("extension", ""),
        "size_bytes": parse_size(row),
        "registered": row.get("registered", ""),
        "psi_state": row.get("psi_state", ""),
        "action_gate": row.get("action_gate", ""),
        "decision": row.get("decision", ""),
    }


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def build_candidates(rows: list[dict[str, str]], *, limit: int, max_bytes: int) -> dict[str, object]:
    by_hash: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        sha = row.get("sha256", "")
        if sha:
            by_hash[sha].append(row)

    duplicate_groups = {sha: group for sha, group in by_hash.items() if len(group) > 1}
    eligible: list[dict[str, object]] = []
    blocked_or_hard_review = 0

    for sha, group in duplicate_groups.items():
        if not all(is_low_risk_row(row, max_bytes) for row in group):
            blocked_or_hard_review += 1
            continue
        sorted_group = sorted(group, key=canonical_score)
        canonical = sorted_group[0]
        duplicates = sorted_group[1:]
        eligible.append(
            {
                "sha256": sha,
                "size_bytes": parse_size(canonical),
                "extension": canonical.get("extension", ""),
                "group_count": len(sorted_group),
                "action_gate": "REVIEW",
                "decision": "CANDIDATE_DELETE_AFTER_CANONICAL_CONFIRMATION",
                "psi_state": "INFERENCIA",
                "proposed_canonical": compact_row(canonical),
                "candidate_duplicates": [compact_row(row) for row in duplicates],
                "required_before_delete": [
                    "confirm canonical path is the source of truth",
                    "create or update ficha for the group",
                    "record full SHA256 and reason in DELETE_CANDIDATES.md",
                    "run secret scan on touched docs/scripts",
                    "obtain ActionGate APPROVE for the specific paths",
                ],
            }
        )

    eligible.sort(key=lambda item: (int(item["size_bytes"]), str(item["sha256"])))
    selected = eligible[:limit]
    return {
        "schema": "medioevo.seto_exact_duplicate_candidates.v1",
        "generated_at_utc": utc_now(),
        "manifest_csv": str(DEFAULT_MANIFEST),
        "status": "DRY_RUN_NO_DELETE_NO_MOVE",
        "policy": {
            "action_gate": "REVIEW",
            "claim_level": "INFERENCIA_FOR_CANONICAL_CHOICE",
            "no_delete": True,
            "max_bytes_per_file": max_bytes,
            "allowed_extensions": sorted(LOW_RISK_EXTENSIONS),
        },
        "summary": {
            "manifest_rows": len(rows),
            "exact_duplicate_groups": len(duplicate_groups),
            "eligible_low_risk_groups": len(eligible),
            "selected_groups": len(selected),
            "blocked_or_hard_review_groups": blocked_or_hard_review,
        },
        "candidates": selected,
        "rules": [
            "This report never approves deletion.",
            "Every proposed duplicate remains REVIEW until canonical source and ficha are confirmed.",
            "Private, release, env, archive, vendor, secret-like and binary/asset paths are excluded.",
        ],
    }


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_report(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    summary = data["summary"]  # type: ignore[index]
    lines = [
        "# SETO Exact Duplicate Candidates 2026-05-05",
        "",
        "Status: dry-run selector. No files were moved, deleted, extracted or published.",
        "",
        "## Evidence",
        "",
        f"- Manifest: `{data['manifest_csv']}`",
        f"- JSON: `{DEFAULT_JSON}`",
        "- ActionGate: `REVIEW`.",
        "- Claim level: `INFERENCIA` for canonical choice.",
        "",
        "## Summary",
        "",
        "| metric | value |",
        "|---|---:|",
    ]
    for key, value in summary.items():  # type: ignore[union-attr]
        lines.append(f"| {key} | `{value}` |")
    lines.extend(
        [
            "",
            "## Selected Candidates",
            "",
            "| sha256 | size | canonical candidate | duplicate candidates |",
            "|---|---:|---|---|",
        ]
    )
    for item in data["candidates"]:  # type: ignore[index]
        canonical = item["proposed_canonical"]["rel_to_workspace"]  # type: ignore[index]
        duplicates = "<br>".join(
            f"`{row['rel_to_workspace']}`" for row in item["candidate_duplicates"]  # type: ignore[index]
        )
        lines.append(
            f"| `{str(item['sha256'])[:16]}` | `{item['size_bytes']}` | "
            f"`{canonical}` | {duplicates} |"
        )
    lines.extend(
        [
            "",
            "## Rules",
            "",
            "- This report is not a deletion approval.",
            "- Each group still needs ficha, canonical confirmation, SHA256 evidence and ActionGate `APPROVE` before cleanup.",
            "- Releases, env folders, private RPG/TCG, assets, archives, vendor, Git history and secret-like paths are excluded.",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Select low-risk exact duplicate review candidates from SETO CSV manifest.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--report-out", default=str(DEFAULT_REPORT))
    parser.add_argument("--limit", type=int, default=80)
    parser.add_argument("--max-bytes", type=int, default=1024 * 1024)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    manifest = Path(args.manifest)
    rows = load_rows(manifest)
    data = build_candidates(rows, limit=args.limit, max_bytes=args.max_bytes)
    data["manifest_csv"] = str(manifest)

    json_path = Path(args.json_out)
    report_path = Path(args.report_out)
    write_json(json_path, data)
    write_report(report_path, data)

    if args.json:
        print_json(data)
    else:
        summary = data["summary"]  # type: ignore[index]
        print(f"status={data['status']}")
        print(f"eligible={summary['eligible_low_risk_groups']} selected={summary['selected_groups']}")
        print(f"json={json_path}")
        print(f"report={report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
