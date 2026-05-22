from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from wabi_sabi.core.redaction import redact_mapping


CLOUD_BUDGET_SCHEMA = "wabi.cloud_budget_gate.v0_1"
CLOUD_BUDGET_STATE_SCHEMA = "wabi.cloud_budget_state.v0_1"
CLOUD_BUDGET_ENABLE_ENV = "WABI_BUILD_ASSIST_CLOUD"
CLOUD_PROVIDER_ENABLE_ENV = "WABI_ALLOW_CLOUD_PROVIDERS"
CLOUD_MAX_CALLS_PER_SESSION_ENV = "WABI_CLOUD_MAX_CALLS_PER_SESSION"
CLOUD_MAX_CALLS_PER_DAY_ENV = "WABI_CLOUD_MAX_CALLS_PER_DAY"
CLOUD_BUDGET_MODE_ENV = "WABI_CLOUD_BUDGET_MODE"
CLOUD_BUDGET_RESET_ENV = "WABI_CLOUD_BUDGET_RESET"
CLOUD_USAGE_DIR_ENV = "WABI_CLOUD_USAGE_DIR"

DEFAULT_MAX_CALLS_PER_SESSION = 3
DEFAULT_MAX_CALLS_PER_DAY = 10
DEFAULT_BUDGET_MODE = "strict"
DEFAULT_BUDGET_RESET = "session"


class CloudBudgetGate:
    def __init__(
        self,
        *,
        runtime_root: str | Path | None = None,
        session_id: str | None = None,
        env: Mapping[str, str] | None = None,
    ):
        self.env = os.environ if env is None else env
        self.runtime_root = Path(runtime_root).resolve() if runtime_root is not None else _default_runtime_root()
        self.session_id = session_id or self.env.get("WABI_SESSION_ID") or f"session-{os.getpid()}"

    def load_state(self, session_id: str | None = None) -> dict[str, Any]:
        state = self._read_state()
        sid = session_id or self.session_id
        self._ensure_session(state, sid)
        self._write_state(state)
        return self._with_current_session_fields(state, sid)

    def get_limits(self) -> dict[str, Any]:
        return {
            "mode": _budget_mode(self.env),
            "reset": _budget_reset(self.env),
            "max_calls_per_session": _positive_int(
                self.env.get(CLOUD_MAX_CALLS_PER_SESSION_ENV),
                DEFAULT_MAX_CALLS_PER_SESSION,
            ),
            "max_calls_per_day": _positive_int(
                self.env.get(CLOUD_MAX_CALLS_PER_DAY_ENV),
                DEFAULT_MAX_CALLS_PER_DAY,
            ),
            "max_calls_per_session_env": CLOUD_MAX_CALLS_PER_SESSION_ENV,
            "max_calls_per_day_env": CLOUD_MAX_CALLS_PER_DAY_ENV,
            "mode_env": CLOUD_BUDGET_MODE_ENV,
            "reset_env": CLOUD_BUDGET_RESET_ENV,
        }

    def get_usage(self) -> dict[str, Any]:
        state = self.load_state()
        session = state["sessions"][self.session_id]
        limits = self.get_limits()
        session_used = _used_calls(session)
        daily_used = _used_calls(state["daily"])
        return {
            "schema": f"{CLOUD_BUDGET_SCHEMA}.usage",
            "date": state["date"],
            "session_id": self.session_id,
            "state_path": str(self._state_path()),
            "calls_planned": session.get("calls_planned", 0),
            "calls_completed": session.get("calls_completed", 0),
            "calls_failed": session.get("calls_failed", 0),
            "calls_blocked": session.get("calls_blocked", 0),
            "daily_calls_planned": state["daily"].get("calls_planned", 0),
            "daily_calls_completed": state["daily"].get("calls_completed", 0),
            "daily_calls_failed": state["daily"].get("calls_failed", 0),
            "daily_calls_blocked": state["daily"].get("calls_blocked", 0),
            "session_calls_used": session_used,
            "daily_calls_used": daily_used,
            "remaining_session_calls": max(0, limits["max_calls_per_session"] - session_used),
            "remaining_daily_calls": max(0, limits["max_calls_per_day"] - daily_used),
        }

    def can_call(self, provider: str, model_alias: str, intent: str) -> dict[str, Any]:
        limits = self.get_limits()
        usage = self.get_usage()
        double_opt_in = _double_opt_in(self.env)
        if not double_opt_in:
            return self._decision(
                provider,
                model_alias,
                intent,
                status="CLOUD_BUDGET_DRY_RUN",
                allowed=False,
                reason="double_opt_in_missing",
                usage=usage,
                limits=limits,
                double_opt_in=double_opt_in,
            )
        session_exceeded = usage["session_calls_used"] >= limits["max_calls_per_session"]
        day_exceeded = usage["daily_calls_used"] >= limits["max_calls_per_day"]
        if session_exceeded or day_exceeded:
            allowed = limits["mode"] == "warn"
            status = "CLOUD_BUDGET_REVIEW" if allowed else "CLOUD_BUDGET_EXCEEDED"
            reason = "session_limit_exceeded" if session_exceeded else "daily_limit_exceeded"
            return self._decision(
                provider,
                model_alias,
                intent,
                status=status,
                allowed=allowed,
                reason=reason,
                usage=usage,
                limits=limits,
                double_opt_in=double_opt_in,
            )
        return self._decision(
            provider,
            model_alias,
            intent,
            status="CLOUD_BUDGET_READY",
            allowed=True,
            reason="within_budget",
            usage=usage,
            limits=limits,
            double_opt_in=double_opt_in,
        )

    def record_planned_call(self, provider: str, model_alias: str, intent: str) -> dict[str, Any]:
        state = self._read_state()
        session = self._ensure_session(state, self.session_id)
        self._increment(state, session, "calls_planned")
        self._update_last_call(state, session, provider, model_alias, intent, status="planned")
        self._write_state(state)
        return {"status": "CLOUD_BUDGET_RECORD_PASS", "record_type": "planned", "cloud_budget": self.render_status(provider, model_alias, intent)}

    def record_completed_call(self, provider: str, model_alias: str, result: dict[str, Any]) -> dict[str, Any]:
        state = self._read_state()
        session = self._ensure_session(state, self.session_id)
        status = str(result.get("status") or result.get("error_class") or result.get("provider_action") or "completed")
        if _result_failed(result):
            self._increment(state, session, "calls_failed")
        else:
            self._increment(state, session, "calls_completed")
        self._update_last_call(state, session, provider, model_alias, "provider_result", status=status)
        usage = result.get("usage") if isinstance(result.get("usage"), dict) else {}
        cost = result.get("cost_estimate")
        session["usage_known"] = any(value is not None for value in usage.values()) if usage else False
        session["cost_known"] = cost is not None
        state["usage_known"] = bool(session["usage_known"])
        state["cost_known"] = bool(session["cost_known"])
        state["last_status"] = status
        self._write_state(state)
        return {
            "status": "CLOUD_BUDGET_RECORD_PASS",
            "record_type": "completed",
            "cloud_budget": self.render_status(provider, model_alias, "provider_result"),
        }

    def record_blocked_call(self, provider: str, model_alias: str, intent: str, *, status: str = "CLOUD_BUDGET_EXCEEDED") -> dict[str, Any]:
        state = self._read_state()
        session = self._ensure_session(state, self.session_id)
        self._increment(state, session, "calls_blocked")
        self._update_last_call(state, session, provider, model_alias, intent, status=status)
        self._write_state(state)
        return {"status": "CLOUD_BUDGET_RECORD_PASS", "record_type": "blocked", "cloud_budget": self.render_status(provider, model_alias, intent)}

    def render_status(self, provider: str = "nvidia", model_alias: str = "nano-30b", intent: str = "status") -> dict[str, Any]:
        decision = self.can_call(provider, model_alias, intent)
        return {
            "schema": CLOUD_BUDGET_SCHEMA,
            "mode": decision["mode"],
            "reset": decision["reset"],
            "provider": provider,
            "model": model_alias,
            "session_id": self.session_id,
            "session_calls_used": decision["session_calls_used"],
            "session_calls_limit": decision["session_calls_limit"],
            "daily_calls_used": decision["daily_calls_used"],
            "daily_calls_limit": decision["daily_calls_limit"],
            "remaining_session_calls": decision["remaining_session_calls"],
            "remaining_daily_calls": decision["remaining_daily_calls"],
            "cloud_live_ready": decision["double_opt_in"] and decision["next_cloud_call_allowed"],
            "double_opt_in": decision["double_opt_in"],
            "budget_gate": decision["budget_gate"],
            "next_cloud_call_allowed": decision["next_cloud_call_allowed"],
            "usage_known": decision["usage_known"],
            "cost_known": decision["cost_known"],
            "state_path": decision["state_path"],
        }

    def _decision(
        self,
        provider: str,
        model_alias: str,
        intent: str,
        *,
        status: str,
        allowed: bool,
        reason: str,
        usage: dict[str, Any],
        limits: dict[str, Any],
        double_opt_in: bool,
    ) -> dict[str, Any]:
        next_allowed = bool(allowed and double_opt_in)
        return redact_mapping(
            {
                "schema": CLOUD_BUDGET_SCHEMA,
                "provider": provider,
                "model_alias": model_alias,
                "intent_label": _intent_label(intent),
                "intent_hash": _intent_hash(intent),
                "allowed": next_allowed,
                "next_cloud_call_allowed": next_allowed,
                "budget_gate": status,
                "status": status,
                "reason": reason,
                "mode": limits["mode"],
                "reset": limits["reset"],
                "double_opt_in": double_opt_in,
                "session_calls_used": usage["session_calls_used"],
                "session_calls_limit": limits["max_calls_per_session"],
                "daily_calls_used": usage["daily_calls_used"],
                "daily_calls_limit": limits["max_calls_per_day"],
                "remaining_session_calls": usage["remaining_session_calls"],
                "remaining_daily_calls": usage["remaining_daily_calls"],
                "usage_known": False,
                "cost_known": False,
                "state_path": usage["state_path"],
                "cloud_provider_called": False,
            },
            env=self.env,
        )

    def _increment(self, state: dict[str, Any], session: dict[str, Any], key: str) -> None:
        session[key] = int(session.get(key, 0)) + 1
        state["daily"][key] = int(state["daily"].get(key, 0)) + 1

    def _update_last_call(
        self,
        state: dict[str, Any],
        session: dict[str, Any],
        provider: str,
        model_alias: str,
        intent: str,
        *,
        status: str,
    ) -> None:
        now = datetime.now().isoformat(timespec="seconds")
        for target in (state, session):
            target["provider"] = provider
            target["model_alias"] = model_alias
            target["last_call_at"] = now
            target["last_status"] = status
            target["last_intent_label"] = _intent_label(intent)
            target["last_intent_hash"] = _intent_hash(intent)

    def _read_state(self) -> dict[str, Any]:
        path = self._state_path()
        if path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(payload, dict) and payload.get("date") == _today():
                    return self._normalize_state(payload)
            except (json.JSONDecodeError, OSError):
                pass
        return self._new_state()

    def _write_state(self, state: dict[str, Any]) -> None:
        path = self._state_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(redact_mapping(state, env=self.env), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def _state_path(self) -> Path:
        usage_dir = self.env.get(CLOUD_USAGE_DIR_ENV)
        root = Path(usage_dir).expanduser() if usage_dir else self.runtime_root / "cloud_budget"
        return root / f"cloud_budget_{_today_compact()}.json"

    def _new_state(self) -> dict[str, Any]:
        limits = self.get_limits()
        return {
            "schema": CLOUD_BUDGET_STATE_SCHEMA,
            "date": _today(),
            "sessions": {},
            "daily": _counter_state(),
            "provider": "nvidia",
            "model_alias": "nano-30b",
            "calls_planned": 0,
            "calls_completed": 0,
            "calls_blocked": 0,
            "max_calls_per_session": limits["max_calls_per_session"],
            "max_calls_per_day": limits["max_calls_per_day"],
            "last_call_at": None,
            "last_status": None,
            "usage_known": False,
            "cost_known": False,
        }

    def _normalize_state(self, state: dict[str, Any]) -> dict[str, Any]:
        state.setdefault("schema", CLOUD_BUDGET_STATE_SCHEMA)
        state.setdefault("date", _today())
        state.setdefault("sessions", {})
        state.setdefault("daily", _counter_state())
        state.setdefault("usage_known", False)
        state.setdefault("cost_known", False)
        limits = self.get_limits()
        state["max_calls_per_session"] = limits["max_calls_per_session"]
        state["max_calls_per_day"] = limits["max_calls_per_day"]
        return state

    def _ensure_session(self, state: dict[str, Any], session_id: str) -> dict[str, Any]:
        sessions = state.setdefault("sessions", {})
        if session_id not in sessions:
            sessions[session_id] = {
                **_counter_state(),
                "session_id": session_id,
                "provider": "nvidia",
                "model_alias": "nano-30b",
                "last_call_at": None,
                "last_status": None,
                "usage_known": False,
                "cost_known": False,
            }
        return sessions[session_id]

    def _with_current_session_fields(self, state: dict[str, Any], session_id: str) -> dict[str, Any]:
        session = state["sessions"][session_id]
        merged = dict(state)
        merged.update(
            {
                "session_id": session_id,
                "provider": session.get("provider", state.get("provider", "nvidia")),
                "model_alias": session.get("model_alias", state.get("model_alias", "nano-30b")),
                "calls_planned": session.get("calls_planned", 0),
                "calls_completed": session.get("calls_completed", 0),
                "calls_blocked": session.get("calls_blocked", 0),
                "last_call_at": session.get("last_call_at"),
                "last_status": session.get("last_status"),
                "usage_known": bool(session.get("usage_known", state.get("usage_known", False))),
                "cost_known": bool(session.get("cost_known", state.get("cost_known", False))),
            }
        )
        return merged


def _default_runtime_root() -> Path:
    return Path.home() / ".medioevo" / "wabi" / "runtime"


def _today() -> str:
    return datetime.now().date().isoformat()


def _today_compact() -> str:
    return datetime.now().strftime("%Y%m%d")


def _counter_state() -> dict[str, int]:
    return {
        "calls_planned": 0,
        "calls_completed": 0,
        "calls_failed": 0,
        "calls_blocked": 0,
    }


def _used_calls(counter: dict[str, Any]) -> int:
    return max(int(counter.get("calls_planned", 0)), int(counter.get("calls_completed", 0)) + int(counter.get("calls_failed", 0)))


def _double_opt_in(env: Mapping[str, str]) -> bool:
    return env.get(CLOUD_BUDGET_ENABLE_ENV, "0") == "1" and env.get(CLOUD_PROVIDER_ENABLE_ENV, "0") == "1"


def _budget_mode(env: Mapping[str, str]) -> str:
    mode = str(env.get(CLOUD_BUDGET_MODE_ENV) or DEFAULT_BUDGET_MODE).strip().lower()
    return mode if mode in {"strict", "warn"} else DEFAULT_BUDGET_MODE


def _budget_reset(env: Mapping[str, str]) -> str:
    reset = str(env.get(CLOUD_BUDGET_RESET_ENV) or DEFAULT_BUDGET_RESET).strip().lower()
    return reset if reset in {"session", "daily"} else DEFAULT_BUDGET_RESET


def _positive_int(value: str | None, default: int) -> int:
    try:
        parsed = int(str(value or "").strip())
    except ValueError:
        return default
    return parsed if parsed > 0 else default


def _intent_hash(intent: str) -> str:
    return hashlib.sha256(str(intent or "").encode("utf-8", errors="replace")).hexdigest()


def _intent_label(intent: str) -> str:
    clean = " ".join(str(intent or "").strip().split()).lower()
    safe_labels = {
        "status",
        "build_assist_plan",
        "build_assist_smoke",
        "build_assist_request",
        "provider_result",
        "test",
    }
    if clean in safe_labels:
        return clean
    if not clean or len(clean) > 64 or " " in clean:
        return "redacted_user_intent"
    return "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in clean)[:64]


def _result_failed(result: dict[str, Any]) -> bool:
    if result.get("ok") is False:
        return True
    status = str(result.get("status") or "").upper()
    return status.startswith("REVIEW") or status.startswith("BLOCK") or status.endswith("FAILED")
