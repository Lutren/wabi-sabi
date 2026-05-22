from __future__ import annotations

from pathlib import Path
from typing import Any

from wabi_sabi.core.project_scan import scan_project


TEST_PLAN_SCHEMA = "wabi.test_plan.v1"


def build_test_plan(*, workspace: str | Path) -> dict[str, Any]:
    scan = scan_project(workspace=workspace)
    commands = []
    seen: set[str] = set()
    for item in scan.get("test_commands", []):
        command = item.get("command", "")
        if not command or command in seen:
            continue
        seen.add(command)
        commands.append(
            {
                "command": command,
                "source": item.get("source", "project_scan"),
                "gate": "APPROVE",
                "execution": "manual_or_safe_executor",
            }
        )
    if not commands:
        commands.append(
            {
                "command": "NO_TEST_BASELINE",
                "source": "project_scan_no_tests_detected",
                "gate": "REVIEW",
                "execution": "document_gap",
            }
        )
    return {
        "schema": TEST_PLAN_SCHEMA,
        "ok": True,
        "action": "test_plan",
        "workspace": scan["workspace"],
        "commands": commands,
        "scan": {
            "package_managers": scan.get("package_managers", []),
            "languages": scan.get("languages", []),
            "repo_boundaries": scan.get("repo_boundaries", {}),
            "content_included": scan.get("limits", {}).get("content_included", False),
        },
        "policy": {
            "auto_execute": False,
            "auto_apply": False,
            "allowed_executor": "SafeExecutor allowlisted commands only",
        },
    }
