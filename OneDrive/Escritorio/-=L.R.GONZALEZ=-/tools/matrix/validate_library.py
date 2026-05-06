from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED_MODULE_FIELDS = (
    "module_id",
    "name",
    "version",
    "fingerprint",
    "domain",
    "purpose",
    "minimal_summary",
    "DO_deconstruction",
    "IOI_recompilation",
    "primitives",
    "inputs",
    "outputs",
    "invariants",
    "interfaces",
    "dependencies",
    "compatible_modules",
    "forbidden_combinations",
    "safety_constraints",
    "evidence_sources",
    "examples",
    "tests",
    "decay_policy",
    "update_policy",
    "handoff_template",
)

LIST_FIELDS = (
    "DO_deconstruction",
    "IOI_recompilation",
    "primitives",
    "inputs",
    "outputs",
    "invariants",
    "dependencies",
    "compatible_modules",
    "forbidden_combinations",
    "safety_constraints",
    "evidence_sources",
    "examples",
    "tests",
)

NON_EMPTY_LIST_FIELDS = tuple(field for field in LIST_FIELDS if field != "dependencies")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _fingerprint(payload: Any) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(data).hexdigest()[:16].upper()


def validate(root: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    index_path = root / "library" / "index.json"
    if not index_path.exists():
        return {
            "schema": "matrix.library.validation.v1",
            "status": "FAIL",
            "errors": ["missing library/index.json"],
            "warnings": [],
            "module_count": 0,
        }

    try:
        index = _load_json(index_path)
    except Exception as exc:  # pragma: no cover - exact parser message is not important.
        return {
            "schema": "matrix.library.validation.v1",
            "status": "FAIL",
            "errors": [f"index json parse failed: {exc}"],
            "warnings": [],
            "module_count": 0,
        }

    module_entries = index.get("modules", [])
    if not isinstance(module_entries, list) or not module_entries:
        errors.append("index.modules must be a non-empty list")

    modules: dict[str, dict[str, Any]] = {}
    for entry in module_entries:
        if not isinstance(entry, dict):
            errors.append("index module entry is not an object")
            continue
        module_id = entry.get("module_id")
        rel_path = entry.get("path")
        if not isinstance(module_id, str) or not module_id:
            errors.append("index module entry missing module_id")
            continue
        if not isinstance(rel_path, str) or not rel_path:
            errors.append(f"{module_id}: missing path")
            continue
        module_path = root / rel_path
        if not module_path.exists():
            errors.append(f"{module_id}: module file missing at {rel_path}")
            continue
        try:
            module = _load_json(module_path)
        except Exception as exc:
            errors.append(f"{module_id}: json parse failed: {exc}")
            continue
        modules[module_id] = module

        if module.get("module_id") != module_id:
            errors.append(f"{module_id}: module_id mismatch")
        expected_name = f"{module_id}.json"
        if module_path.name != expected_name:
            warnings.append(f"{module_id}: filename does not match {expected_name}")
        for field in REQUIRED_MODULE_FIELDS:
            if field not in module:
                errors.append(f"{module_id}: missing required field {field}")
        for field in LIST_FIELDS:
            if field in module and not isinstance(module[field], list):
                errors.append(f"{module_id}: {field} must be a list")
        for field in NON_EMPTY_LIST_FIELDS:
            if field in module and not module[field]:
                errors.append(f"{module_id}: {field} must be a non-empty list")
        if "interfaces" in module and not isinstance(module["interfaces"], dict):
            errors.append(f"{module_id}: interfaces must be an object")
        if "handoff_template" in module and not isinstance(module["handoff_template"], dict):
            errors.append(f"{module_id}: handoff_template must be an object")
        if "safety_constraints" in module and not module["safety_constraints"]:
            errors.append(f"{module_id}: safety_constraints must not be empty")
        if "forbidden_combinations" in module and not module["forbidden_combinations"]:
            errors.append(f"{module_id}: forbidden_combinations must not be empty")

    module_ids = set(modules)
    for module_id, module in modules.items():
        for dep in module.get("dependencies", []):
            if dep not in module_ids:
                errors.append(f"{module_id}: missing dependency {dep}")
        for compatible in module.get("compatible_modules", []):
            if compatible not in module_ids:
                errors.append(f"{module_id}: missing compatible module {compatible}")
        overlap = set(module.get("dependencies", [])) & set(module.get("forbidden_combinations", []))
        if overlap:
            errors.append(f"{module_id}: dependency is also forbidden: {sorted(overlap)}")
        if module_id in set(module.get("forbidden_combinations", [])):
            errors.append(f"{module_id}: module forbids itself")
        if module_id in set(module.get("dependencies", [])):
            errors.append(f"{module_id}: module depends on itself")

    policy = index.get("policy", {})
    if not isinstance(policy, dict):
        errors.append("index.policy must be an object")
    else:
        if policy.get("no_bulk_canon") is not True:
            errors.append("index.policy.no_bulk_canon must be true")
        if policy.get("no_external_action_without_gate") is not True:
            errors.append("index.policy.no_external_action_without_gate must be true")

    result = {
        "schema": "matrix.library.validation.v1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "module_count": len(modules),
        "active_count": sum(1 for entry in module_entries if entry.get("status") == "ACTIVE"),
        "review_count": sum(1 for entry in module_entries if entry.get("status") == "REVIEW"),
    }
    result["fingerprint"] = _fingerprint(result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Matrix library index and modules.")
    parser.add_argument("--root", default=".", help="Workspace root.")
    parser.add_argument("--json", action="store_true", help="Print JSON result.")
    args = parser.parse_args(argv)
    result = validate(Path(args.root).resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"status={result['status']} modules={result['module_count']} errors={len(result['errors'])}")
        for error in result["errors"]:
            print(f"ERROR: {error}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
