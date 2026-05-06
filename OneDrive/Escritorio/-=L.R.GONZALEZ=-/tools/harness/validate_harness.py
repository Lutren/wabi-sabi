from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / "tools" / "harness"
REQUIRED_SECTIONS = [
    "## Reads",
    "## May Touch",
    "## Required Evidence",
    "## ActionGate Blocks",
]
FORBIDDEN_TEXT = [
    "git add -- .",
    "-AcknowledgePreviewRisk until preflight ready_to_launch=true",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_skill(skill_path: Path) -> list[str]:
    failures: list[str] = []
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        failures.append(f"{skill_path}: missing YAML frontmatter")
    if not re.search(r"^name: [a-z0-9-]+$", text, re.M):
        failures.append(f"{skill_path}: missing valid name")
    if not re.search(r"^description: .+", text, re.M):
        failures.append(f"{skill_path}: missing description")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            failures.append(f"{skill_path}: missing {section}")
    if "ActionGate" not in text or "host_observacionista" not in text:
        failures.append(f"{skill_path}: missing ActionGate/host_observacionista gate")
    if "No usar git add ." not in text:
        failures.append(f"{skill_path}: missing no git add dot rule")
    return failures


def main() -> int:
    failures: list[str] = []
    manifest = load_json(HARNESS / "harness_manifest.json")
    if manifest.get("schema") != "medioevo.harness_manifest.v1":
        failures.append("harness_manifest schema mismatch")
    if not manifest.get("git_policy", {}).get("no_git_add_dot"):
        failures.append("harness manifest does not block git add dot")

    allowlist = load_json(HARNESS / "mcp_allowlist.json")
    if allowlist.get("default_policy") != "deny":
        failures.append("MCP allowlist must default deny")
    if not allowlist.get("actiongate_required_for_exceptions"):
        failures.append("MCP allowlist exceptions must require ActionGate")

    candidates = load_json(HARNESS / "candidate_routes.json")
    routes = {item.get("id"): item for item in candidates.get("routes", [])}
    for route_id in ["n8n", "open-webui", "dagger"]:
        route = routes.get(route_id)
        if not route:
            failures.append(f"missing candidate route {route_id}")
            continue
        if route.get("status") != "candidate_disabled":
            failures.append(f"{route_id} must remain candidate_disabled")
        gate = route.get("launch_gate", {})
        if not gate.get("requires_actiongate"):
            failures.append(f"{route_id} launch gate must require ActionGate")
    open_webui = routes.get("open-webui", {})
    forbidden = open_webui.get("launch_gate", {}).get("forbidden_until_ready", [])
    if "-AcknowledgePreviewRisk" not in forbidden:
        failures.append("Open WebUI route must block -AcknowledgePreviewRisk")

    for skill in manifest.get("skills", []):
        failures.extend(validate_skill(ROOT / skill["path"]))

    for path in HARNESS.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in FORBIDDEN_TEXT:
                if token in text and path.name != "validate_harness.py":
                    failures.append(f"{path}: forbidden unsafe text {token!r}")

    if failures:
        print("HARNESS_VALIDATION_FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("HARNESS_VALIDATION_OK")
    print(f"skills={len(manifest.get('skills', []))}")
    print(f"candidate_routes={len(routes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
