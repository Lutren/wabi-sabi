from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


BROWSER_GATE_SCHEMA = "wabi.browser_gate.v1"

REVIEW_TERMS = {
    "login",
    "auth",
    "signin",
    "sign-in",
    "signup",
    "sign-up",
    "checkout",
    "purchase",
    "buy",
    "billing",
    "payment",
    "publish",
    "deploy",
    "delete",
    "remove",
    "submit",
    "post",
    "upload",
    "token",
    "secret",
    "password",
    "api_key",
    "apikey",
}


def build_browser_gate_policy(workspace: str | Path | None = None) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve() if workspace else None
    return {
        "schema": BROWSER_GATE_SCHEMA,
        "generated_at_utc": _utc_now(),
        "workspace": str(workspace_path) if workspace_path else "",
        "decision_context": {
            "no_operational_assumptions": True,
            "mode": "COMPLETO_GATEADO",
            "rule": "Browser access is allowed for local and read-only inspection; state-changing, authenticated, paid, publishing, or secret-bearing actions are REVIEW/BLOCK.",
        },
        "allow": [
            {
                "scope": "file://",
                "gate": "APPROVE_LOGGED",
                "reason": "local static artifact inspection",
            },
            {
                "scope": "localhost / 127.0.0.1 / ::1",
                "gate": "APPROVE_LOGGED",
                "reason": "local app smoke testing",
            },
            {
                "scope": "http/https read-only public pages",
                "gate": "APPROVE_LOGGED_READ_ONLY",
                "reason": "documentation or public page inspection without login or form submit",
            },
        ],
        "review": [
            "authenticated sessions",
            "forms that submit data",
            "uploads",
            "posting to social/media/store surfaces",
            "checkout, billing, payment, subscription, or purchase flows",
            "settings that persist account or host state",
        ],
        "block": [
            "secret extraction or printing",
            "credential entry by the agent without explicit credential handoff",
            "public deploy, release, push, or publication without a dedicated gate",
            "destructive account, billing, or data operations",
        ],
        "evidence_required": [
            "target URL",
            "intended browser action",
            "whether authentication or persistence is involved",
            "screenshot/log/result artifact for completed local checks",
        ],
    }


def evaluate_browser_request(url: str, action: str = "read") -> dict[str, Any]:
    parsed = urlparse(url)
    lowered = f"{url} {action}".lower()
    matched_terms = sorted(term for term in REVIEW_TERMS if term in lowered)
    host = (parsed.hostname or "").lower()
    scheme = (parsed.scheme or "").lower()
    is_local_host = host in {"localhost", "127.0.0.1", "::1"} or host.endswith(".local")
    is_file = scheme == "file"
    is_read_action = action.lower() in {"read", "open", "inspect", "screenshot", "snapshot", "navigate", "view", "extract"}

    if matched_terms:
        gate = "REVIEW"
        if any(term in matched_terms for term in {"delete", "remove", "billing", "payment", "token", "secret", "password"}):
            gate = "BLOCK"
        reasons = [f"review_term:{term}" for term in matched_terms]
    elif is_file or is_local_host:
        gate = "APPROVE"
        reasons = ["local_browser_target"]
    elif scheme in {"http", "https"} and is_read_action:
        gate = "APPROVE"
        reasons = ["public_read_only_browser_target"]
    else:
        gate = "REVIEW"
        reasons = ["browser_action_not_proven_read_only"]

    return {
        "schema": "wabi.browser_gate.evaluation.v1",
        "generated_at_utc": _utc_now(),
        "url": url,
        "action": action,
        "gate": gate,
        "reasons": reasons,
        "parsed": {
            "scheme": scheme,
            "host": host,
            "is_local": is_file or is_local_host,
            "is_read_action": is_read_action,
        },
        "evidence_required": [] if gate == "APPROVE" else ["explicit reviewed target and action"],
    }


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
