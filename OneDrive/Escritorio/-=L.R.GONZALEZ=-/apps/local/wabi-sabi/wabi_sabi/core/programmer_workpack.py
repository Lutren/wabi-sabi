from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

from wabi_sabi.core.tools import write_artifact


PROGRAMMER_WORKPACK_SCHEMA = "wabi.programmer_workpack.v0_1"


def build_programmer_workpack(*, prompt: str, snapshot: dict[str, Any]) -> dict[str, Any]:
    decision = snapshot.get("decision", {}) if isinstance(snapshot.get("decision"), dict) else {}
    host = snapshot.get("host", {}) if isinstance(snapshot.get("host"), dict) else {}
    pending = snapshot.get("pending", {}) if isinstance(snapshot.get("pending"), dict) else {}
    host_blocked = host.get("gate") == "BLOCK"
    workpack = {
        "schema": PROGRAMMER_WORKPACK_SCHEMA,
        "generated_at_utc": _utc_now(),
        "prompt": prompt.strip() or "preparar workpack de programacion",
        "mode": "PLAN_ONLY",
        "workpack_gate": "REVIEW",
        "application_gate": "BLOCK" if host_blocked else "REVIEW",
        "host": {
            "status": host.get("status"),
            "gate": host.get("gate"),
            "timestamp": host.get("timestamp"),
            "reasons": host.get("reasons", []),
        },
        "pending": {
            "active_dedup": pending.get("active_dedup"),
            "by_blocker": pending.get("by_blocker", {}),
        },
        "decision": {
            "recommended_mode": decision.get("recommended_mode"),
            "reasons": decision.get("reasons", []),
        },
        "allowed_now": [
            "read_local_files",
            "draft_patch_plan",
            "run_focused_tests",
            "write_runtime_workpack",
        ],
        "blocked_now": [
            "apply_multi_file_patch",
            "destructive_file_moves",
            "external_publish_or_push",
            "model_alias_or_training",
        ],
        "required_before_apply": [
            "host_gate_not_block",
            "explicit_file_scope",
            "rollback_or_backup_plan",
            "focused_tests_declared",
            "ActionGate_not_BLOCK",
        ],
        "proposed_files": [],
        "patches": [],
        "tests": [],
        "falsifiers": [
            "workpack applies a multi-file patch directly",
            "target files are omitted before apply",
            "rollback plan is missing",
            "host remains BLOCK while apply is attempted",
            "focused tests are not declared",
        ],
    }
    workpack["workpack_hash"] = _hash_payload(workpack)
    return workpack


def write_programmer_workpack(output_dir: Path, workpack: dict[str, Any]) -> Path:
    text = json.dumps(workpack, indent=2, sort_keys=True, ensure_ascii=False)
    return write_artifact(output_dir, "wabi_programmer_workpack", ".json", text)


def _hash_payload(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()


def _utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
