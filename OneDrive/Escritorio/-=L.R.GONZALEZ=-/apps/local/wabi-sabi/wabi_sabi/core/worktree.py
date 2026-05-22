from __future__ import annotations

from pathlib import Path
from typing import Any

from wabi_sabi.core.subprocess_utils import run_hidden


def git_worktree_summary(workspace: str | Path, *, max_files: int = 120) -> dict[str, Any]:
    root = Path(workspace).resolve()
    if _find_git_marker(root) is None:
        return {
            "ok": False,
            "schema": "wabi.git_worktree_summary.v1",
            "workspace": str(root),
            "error": "not_a_git_worktree",
            "details": "no_git_marker_in_parent_chain",
        }
    git_root = _git(["rev-parse", "--show-toplevel"], root)
    if git_root["returncode"] != 0:
        return {
            "ok": False,
            "schema": "wabi.git_worktree_summary.v1",
            "workspace": str(root),
            "error": "not_a_git_worktree",
            "details": git_root["stderr"] or git_root["stdout"],
        }
    repo_root = Path(git_root["stdout"].strip()).resolve()
    branch = _git(["branch", "--show-current"], repo_root)
    commit = _git(["rev-parse", "--short", "HEAD"], repo_root)
    status = _git(["status", "--short"], repo_root)
    diff_stat = _git(["diff", "--stat"], repo_root)
    diff_names = _git(["diff", "--name-only"], repo_root)
    untracked = _git(["ls-files", "--others", "--exclude-standard"], repo_root)

    status_lines = _lines(status["stdout"])
    modified_names = _lines(diff_names["stdout"])[:max_files]
    untracked_names = _lines(untracked["stdout"])[:max_files]
    return {
        "ok": True,
        "schema": "wabi.git_worktree_summary.v1",
        "workspace": str(root),
        "repo_root": str(repo_root),
        "branch": branch["stdout"].strip() or "unknown",
        "base_commit": commit["stdout"].strip() if commit["returncode"] == 0 else "unknown",
        "dirty": bool(status_lines),
        "status_count": len(status_lines),
        "status_sample": status_lines[:max_files],
        "modified_tracked": modified_names,
        "untracked": untracked_names,
        "diff_stat": diff_stat["stdout"].strip(),
        "limits": {"max_files": max_files, "content_included": False},
    }


def _find_git_marker(root: Path) -> Path | None:
    home = Path.home().resolve()
    for candidate in [root, *root.parents]:
        if candidate == home and root != home:
            break
        marker = candidate / ".git"
        if marker.exists():
            return marker
    return None


def _git(args: list[str], cwd: Path) -> dict[str, Any]:
    proc = run_hidden(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=30,
    )
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr[-4000:],
    }


def _lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.strip()]
