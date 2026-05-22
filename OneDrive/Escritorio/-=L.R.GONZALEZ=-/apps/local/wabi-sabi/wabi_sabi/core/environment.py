from __future__ import annotations

import datetime as dt
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from wabi_sabi.core.tools import write_artifact


ENVIRONMENT_SCHEMA = "wabi.environment_snapshot.v0_2"
COMMS_SCHEMA = "wabi.comms_state.v0_2"


class CommsBridge:
    def __init__(self, portfolio_root: str | Path | None) -> None:
        self.portfolio_root = Path(portfolio_root).resolve() if portfolio_root else None

    @property
    def agents_state_dir(self) -> Path | None:
        if self.portfolio_root is None:
            return None
        return self.portfolio_root / "COMMS" / "agents_state"

    @property
    def validator_path(self) -> Path | None:
        if self.portfolio_root is None:
            return None
        return self.portfolio_root / "COMMS" / "tools" / "validate_seto_comms.py"

    def read_agents(self) -> list[dict[str, Any]]:
        agents_dir = self.agents_state_dir
        if agents_dir is None or not agents_dir.exists():
            return []

        records: list[dict[str, Any]] = []
        for path in sorted(agents_dir.glob("*.json")):
            records.append(_read_agent_state(path))
        return records

    def summary(self) -> dict[str, Any]:
        records = self.read_agents()
        valid_records = [record for record in records if not record.get("error")]
        by_gate = Counter(str(record.get("action_gate") or "UNKNOWN") for record in valid_records)
        by_status = Counter(str(record.get("status") or "UNKNOWN") for record in valid_records)
        by_department = Counter(str(record.get("department") or "UNKNOWN") for record in valid_records)
        return {
            "schema": COMMS_SCHEMA,
            "exists": bool(self.portfolio_root and (self.portfolio_root / "COMMS").exists()),
            "root": str(self.portfolio_root / "COMMS") if self.portfolio_root else "",
            "agents_state_dir": str(self.agents_state_dir) if self.agents_state_dir else "",
            "agent_count": len(valid_records),
            "invalid_count": len(records) - len(valid_records),
            "by_gate": dict(sorted(by_gate.items())),
            "by_status": dict(sorted(by_status.items())),
            "by_department": dict(sorted(by_department.items())),
            "agents": valid_records,
            "invalid_agents": [record for record in records if record.get("error")],
        }

    def validate(self, timeout: int = 20) -> dict[str, Any]:
        validator = self.validator_path
        if self.portfolio_root is None:
            return {"available": False, "ok": False, "reason": "portfolio_root_not_found"}
        if validator is None or not validator.exists():
            return {
                "available": False,
                "ok": False,
                "reason": "validator_not_found",
                "path": str(validator) if validator else "",
            }

        try:
            proc = subprocess.run(
                [sys.executable, str(validator), "--json"],
                cwd=str(self.portfolio_root),
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            return {
                "available": True,
                "ok": False,
                "reason": "validator_timeout",
                "path": str(validator),
                "timeout": timeout,
                "stdout": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
                "stderr": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
            }

        parsed: dict[str, Any] = {}
        parse_error = ""
        if proc.stdout.strip():
            try:
                raw = json.loads(proc.stdout)
                parsed = raw if isinstance(raw, dict) else {"payload": raw}
            except json.JSONDecodeError as exc:
                parse_error = str(exc)

        status = str(parsed.get("status") or parsed.get("gate") or "").upper()
        errors = parsed.get("errors") if isinstance(parsed.get("errors"), list) else []
        ok_flag = parsed.get("ok")
        ok = proc.returncode == 0 and parse_error == "" and not errors
        if isinstance(ok_flag, bool):
            ok = ok and ok_flag
        if status:
            ok = ok and status not in {"FAIL", "BLOCK", "ERROR"}

        return {
            "available": True,
            "ok": ok,
            "path": str(validator),
            "returncode": proc.returncode,
            "status": status or ("PASS" if ok else "UNKNOWN"),
            "errors": errors,
            "warnings": parsed.get("warnings", []),
            "counts": parsed.get("counts", {}),
            "schema_hashes": parsed.get("schema_hashes", {}),
            "witness_tail": parsed.get("witness_tail", []),
            "parse_error": parse_error,
            "stdout_tail": proc.stdout[-2000:],
            "stderr_tail": proc.stderr[-2000:],
        }


def build_environment_snapshot(
    *,
    workspace: str | Path,
    runtime_root: str | Path,
    provider_status: dict[str, Any] | None = None,
    run_comms_validator: bool = True,
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    runtime_path = Path(runtime_root).resolve()
    portfolio_root = find_portfolio_root(workspace_path, runtime_path)
    bridge = CommsBridge(portfolio_root)
    comms = bridge.summary()
    validator = bridge.validate() if run_comms_validator else {"available": False, "ok": False, "reason": "not_run"}
    comms["validator"] = _trim_validator(validator)

    pending = _read_pending_review(portfolio_root)
    host = _read_host_report(portfolio_root)
    programming_lane = _programming_lane(host=host, provider_status=provider_status or {})
    decision = _decision(
        pending=pending,
        host=host,
        comms=comms,
        validator=validator,
        provider_status=provider_status or {},
    )

    return {
        "schema": ENVIRONMENT_SCHEMA,
        "generated_at_utc": _utc_now(),
        "workspace": str(workspace_path),
        "runtime_root": str(runtime_path),
        "portfolio_root": str(portfolio_root) if portfolio_root else "",
        "pending": pending,
        "host": host,
        "comms": comms,
        "providers": provider_status or {},
        "programming_lane": programming_lane,
        "decision": decision,
    }


def write_environment_snapshot(output_dir: Path, snapshot: dict[str, Any]) -> Path:
    text = json.dumps(snapshot, indent=2, ensure_ascii=False, sort_keys=True)
    return write_artifact(output_dir, "wabi_environment_snapshot", ".json", text)


def write_comms_state(output_dir: Path, payload: dict[str, Any]) -> Path:
    text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)
    return write_artifact(output_dir, "wabi_comms_state", ".json", text)


def find_portfolio_root(*bases: str | Path) -> Path | None:
    candidates: list[Path] = []
    for raw_base in bases:
        base = Path(raw_base).resolve()
        candidates.extend([base, *base.parents])

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (candidate / "docs" / "ops").exists() and (candidate / "COMMS").exists():
            return candidate
        if candidate.name == "-=L.R.GONZALEZ=-":
            return candidate
    return None


def _read_agent_state(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive path for corrupted local state.
        return {"path": str(path), "file": path.name, "error": f"{type(exc).__name__}: {exc}"}

    department = data.get("department_slug")
    if not department and isinstance(data.get("department"), dict):
        department = data["department"].get("id") or data["department"].get("name")

    record = {
        "agent_id": data.get("agent_id") or path.stem,
        "status": data.get("status", "UNKNOWN"),
        "department": department or "UNKNOWN",
        "action_gate": data.get("action_gate") or data.get("gate") or "UNKNOWN",
        "handoff_required": bool(data.get("handoff_required", False)),
        "owns": _as_list(data.get("owns")),
        "may_touch": _as_list(data.get("may_touch")),
        "must_not_touch_without_handoff": _as_list(data.get("must_not_touch_without_handoff")),
        "allowed_actions": _as_list(data.get("allowed_actions")),
        "blocked_actions": _as_list(data.get("blocked_actions")),
        "last_observation_fingerprint": data.get("last_observation_fingerprint", ""),
        "current_outbox": data.get("current_outbox"),
        "path": str(path),
        "sha256": _sha256(path),
    }
    envelope = data.get("comms_envelope")
    if isinstance(envelope, dict):
        record["comms_envelope"] = {
            "gate": envelope.get("gate"),
            "observation": envelope.get("observation"),
            "handoff_required": envelope.get("handoff_required"),
            "origin": envelope.get("origin"),
            "destination": envelope.get("destination"),
        }
    return record


def _read_pending_review(portfolio_root: Path | None) -> dict[str, Any]:
    if portfolio_root is None:
        return {"loaded": False, "reason": "portfolio_root_not_found"}
    path = portfolio_root / "qa_artifacts" / "pending" / "pending_review_latest.json"
    payload = _read_json(path)
    if payload is None:
        return {"loaded": False, "path": str(path), "reason": "pending_review_latest_not_found"}

    active = payload.get("active_markdown", {}) if isinstance(payload.get("active_markdown"), dict) else {}
    return {
        "loaded": True,
        "path": str(path),
        "generated_at": payload.get("generated_at"),
        "date": payload.get("date"),
        "active_dedup": active.get("dedup_open", payload.get("active_dedup")),
        "active_raw": active.get("raw_open", payload.get("active_raw")),
        "claudio_open": payload.get("claudio_open", 0),
        "by_lane": active.get("by_lane", {}),
        "by_blocker": active.get("by_blocker", {}),
        "top_items": active.get("top_items", [])[:8],
    }


def _read_host_report(portfolio_root: Path | None) -> dict[str, Any]:
    if portfolio_root is None:
        return {"loaded": False, "reason": "portfolio_root_not_found"}

    candidates = [
        portfolio_root
        / "-=MEDIOEVO=-"
        / "-=LIBROS"
        / "claudio"
        / "runtime"
        / "host_observacionista"
        / "latest_report.json",
        portfolio_root / "claudio" / "runtime" / "host_observacionista" / "latest_report.json",
    ]
    path = next((candidate for candidate in candidates if candidate.exists()), candidates[0])
    payload = _read_json(path)
    if payload is None:
        return {"loaded": False, "path": str(path), "reason": "host_report_not_found"}

    gate = payload.get("gate", {}) if isinstance(payload.get("gate"), dict) else {}
    metrics = payload.get("metrics", {}) if isinstance(payload.get("metrics"), dict) else {}
    return {
        "loaded": True,
        "path": str(path),
        "timestamp": payload.get("timestamp"),
        "root": payload.get("root"),
        "status": gate.get("status"),
        "gate": gate.get("gate"),
        "action": gate.get("action"),
        "lambda_sat": gate.get("lambda_sat"),
        "reasons": gate.get("reasons", []),
        "metrics": {
            "cpu_pct": metrics.get("cpu_pct"),
            "memory_pct": metrics.get("memory_pct"),
            "disk_pct": metrics.get("disk_pct"),
            "process_count": metrics.get("process_count"),
            "top_cpu_pct": metrics.get("top_cpu_pct"),
        },
        "top_cpu": payload.get("top_cpu", [])[:5],
    }


def _programming_lane(*, host: dict[str, Any], provider_status: dict[str, Any]) -> dict[str, Any]:
    policy = provider_status.get("blueprint_policy", {}) if isinstance(provider_status, dict) else {}
    reasons = policy.get("reasons", []) if isinstance(policy, dict) else []
    host_blocked = host.get("gate") == "BLOCK"
    heavy_blocked = "host_or_heavy_models_blocked" in reasons
    return {
        "apply_mode": "scoped_local_only" if not host_blocked else "read_review_and_scoped_dry_run",
        "external_actions": "blocked",
        "heavy_models": "blocked" if host_blocked or heavy_blocked else "optional_gated",
        "destructive_file_moves": "blocked",
        "safe_programming_actions": [
            "local_read",
            "focused_tests",
            "small_scoped_patches",
            "runtime_artifacts",
            "dry_run_workpacks",
        ],
    }


def _decision(
    *,
    pending: dict[str, Any],
    host: dict[str, Any],
    comms: dict[str, Any],
    validator: dict[str, Any],
    provider_status: dict[str, Any],
) -> dict[str, Any]:
    reasons: set[str] = set()
    blocked_actions = {"external_publish", "destructive_file_moves", "model_alias_or_training"}
    allowed_actions = {"local_read", "local_tests", "local_docs", "local_runtime_artifacts", "comms_validation"}

    if pending.get("active_dedup"):
        reasons.add("pending_review_has_open_items")
    if host.get("gate") == "BLOCK":
        reasons.add("host_gate_block")
        blocked_actions.add("heavy_model_routes")
    elif host.get("loaded"):
        reasons.add("host_report_loaded")
    else:
        reasons.add("host_report_missing")

    by_gate = comms.get("by_gate", {})
    if by_gate.get("BLOCK"):
        reasons.add("comms_has_blocked_agents")
    if by_gate.get("REVIEW"):
        reasons.add("comms_has_review_agents")

    if validator.get("available"):
        reasons.add("comms_validator_pass" if validator.get("ok") else "comms_validator_not_clean")
    else:
        reasons.add("comms_validator_unavailable")

    policy = provider_status.get("blueprint_policy", {}) if isinstance(provider_status, dict) else {}
    for reason in policy.get("reasons", []) if isinstance(policy, dict) else []:
        reasons.add(f"provider_policy:{reason}")

    if "host_gate_block" in reasons:
        recommended_mode = "A0_LOCAL_REVIEW_ONLY"
    elif "comms_validator_not_clean" in reasons or "comms_has_blocked_agents" in reasons:
        recommended_mode = "LOCAL_EVIDENCE_REVIEW"
    else:
        recommended_mode = "LOCAL_CONTROL_PLANE_READY"

    return {
        "recommended_mode": recommended_mode,
        "reasons": sorted(reasons),
        "allowed_actions": sorted(allowed_actions),
        "blocked_actions": sorted(blocked_actions),
    }


def _trim_validator(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "available": payload.get("available", False),
        "ok": payload.get("ok", False),
        "path": payload.get("path", ""),
        "returncode": payload.get("returncode"),
        "status": payload.get("status"),
        "errors": payload.get("errors", []),
        "warnings": payload.get("warnings", []),
        "counts": payload.get("counts", {}),
        "schema_hashes": payload.get("schema_hashes", {}),
        "reason": payload.get("reason", ""),
        "parse_error": payload.get("parse_error", ""),
    }


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else {"payload": payload}


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
