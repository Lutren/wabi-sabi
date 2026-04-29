from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from _common import ROOT, rel


APP_DIR = ROOT / "apps" / "commercial" / "argus-desktop"


def tail(text: str, limit: int = 20) -> list[str]:
    return text.splitlines()[-limit:]


def run(command: list[str], cwd: Path) -> dict[str, object]:
    resolved = list(command)
    executable = shutil.which(resolved[0])
    if executable:
        resolved[0] = executable
    try:
        result = subprocess.run(resolved, cwd=cwd, text=True, capture_output=True)
    except FileNotFoundError as exc:
        return {
            "cwd": rel(cwd),
            "command": command,
            "returncode": 127,
            "error": str(exc),
        }
    return {
        "cwd": rel(cwd),
        "command": command,
        "returncode": result.returncode,
        "stdout_tail": tail(result.stdout),
        "stderr_tail": tail(result.stderr),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Argus reproducible commercial-app checks.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cache_dir = Path(tempfile.gettempdir()) / "argus-npm-cache-20260429"
    commands = [
        ["npm", "ci", "--cache", str(cache_dir), "--prefer-online", "--no-audit", "--no-fund"],
        ["npm", "rebuild"],
        ["npm", "run", "typecheck"],
        ["npm", "run", "build"],
        ["npm", "audit", "--omit=dev", "--audit-level=high"],
    ]
    results: list[dict[str, object]] = []
    for command in commands:
        result = run(command, APP_DIR)
        results.append(result)
        if result.get("returncode") != 0:
            break

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for result in results:
            print(result)
    return 0 if all(result.get("returncode") == 0 for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
