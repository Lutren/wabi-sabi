from __future__ import annotations

import argparse

from _common import ROOT, add_common_args, print_json, run_command, validate_root_arg


COMMANDS = [
    {
        "name": "secret-scan",
        "cwd": ".",
        "command": ["python", "tools/release/scan_secrets.py"],
        "private": False,
    },
    {
        "name": "release-free-dev-dry-run",
        "cwd": ".",
        "command": ["python", "tools/release/package_free_dev.py"],
        "private": False,
    },
    {
        "name": "release-paid-apps-dry-run",
        "cwd": ".",
        "command": ["python", "tools/release/package_paid_apps.py"],
        "private": False,
    },
    {
        "name": "product-manifest",
        "cwd": ".",
        "command": ["python", "tools/release/product_manifest.py"],
        "private": False,
    },
    {
        "name": "argus-clean-generated-before-build",
        "cwd": ".",
        "command": ["python", "tools/release/clean_generated_artifacts.py", "--execute", "--json"],
        "private": False,
    },
    {
        "name": "argus-release-check",
        "cwd": ".",
        "command": ["python", "tools/release/argus_release_check.py", "--json"],
        "private": False,
    },
    {
        "name": "asistente-public-safe-check",
        "cwd": "apps/commercial/asistente-negocio",
        "command": ["npm", "run", "check"],
        "private": False,
    },
    {
        "name": "asistente-audit-high",
        "cwd": "apps/commercial/asistente-negocio",
        "command": ["npm", "audit", "--omit=dev", "--audit-level=high"],
        "private": False,
    },
    {
        "name": "flujocrm-check",
        "cwd": "apps/commercial/flujocrm",
        "command": ["npm", "run", "check"],
        "private": False,
    },
    {
        "name": "private-metaevo-build",
        "cwd": "-=MEDIOEVO=-/-=LIBROS/metaevo-tcg",
        "command": ["npm", "run", "build"],
        "private": True,
    },
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run or execute known build commands.")
    add_common_args(parser)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--include-private", action="store_true", help="include private game checks")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)

    results = []
    for item in COMMANDS:
        if item.get("private") and not args.include_private:
            results.append({"name": item["name"], "skipped": "private_check_requires_include_private"})
            continue
        cwd = ROOT / item["cwd"]
        if not cwd.exists():
            results.append({"name": item["name"], "missing": item["cwd"]})
            continue
        result = run_command(item["command"], cwd, execute=args.execute)
        result["name"] = item["name"]
        results.append(result)
    if args.json:
        print_json(results)
    else:
        for row in results:
            print(row)
    return 0 if not args.execute or all(row.get("returncode", 0) == 0 for row in results if row.get("executed")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
