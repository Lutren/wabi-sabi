#!/usr/bin/env python3
import hashlib
import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

HOST = "127.0.0.1"
PORT = 4787
DEFAULT_POLICY = {
    "j_c": 0.65,
    "epsilon_degrade": 0.7,
    "require_approval": ["publish", "spend_credits", "paid_api", "clone_voice", "canon_write", "irreversible"],
    "blocked": ["bypass_captcha", "create_account", "change_password", "scrape_private_data", "purchase_without_approval"],
    "browser_requires_manifest": True,
    "witness_log": "/var/log/claudio/guardian_events.jsonl",
}


def load_policy():
    path = Path(os.environ.get("CLAUDIO_POLICY", "/etc/claudio/policy.yaml"))
    if not path.exists():
        return DEFAULT_POLICY
    try:
        import yaml

        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return {**DEFAULT_POLICY, **data}
    except Exception:
        return DEFAULT_POLICY


POLICY = load_policy()
EVENTS = []


def witness_id(payload):
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def write_event(event):
    EVENTS.append(event)
    if len(EVENTS) > 200:
        del EVENTS[:-200]
    path = Path(POLICY.get("witness_log") or DEFAULT_POLICY["witness_log"])
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        fallback = Path("/tmp/claudio_guardian_events.jsonl")
        with fallback.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def decide(payload):
    action = str(payload.get("action") or payload.get("task") or "unknown")
    tags = set(payload.get("tags") or [])
    r_value = float(payload.get("R", payload.get("r", 0.0)) or 0.0)
    j_c = float(payload.get("J_c", payload.get("j_c", POLICY["j_c"])) or POLICY["j_c"])
    epsilon = float(payload.get("epsilon", 0.0) or 0.0)
    evidence = bool(payload.get("evidence", True))
    browser = bool(payload.get("browser", False) or payload.get("browser_action", False))
    manifest = bool(payload.get("manifest", False) or payload.get("manifest_present", False))

    blocked = set(POLICY.get("blocked", []))
    approval = set(POLICY.get("require_approval", []))
    action_tokens = {action, *tags}

    if not evidence:
        result = ("hold", "missing_evidence", "Gather evidence before acting.")
    elif r_value >= j_c:
        result = ("hold", "jamming", f"R={r_value:.2f} >= J_c={j_c:.2f}.")
    elif action_tokens & blocked:
        result = ("block", "blocked_action", f"Forbidden action: {sorted(action_tokens & blocked)}.")
    elif browser and POLICY.get("browser_requires_manifest", True) and not manifest:
        result = ("block", "browser_manifest", "Browser automation requires manifest.")
    elif action_tokens & approval:
        result = ("ask", "approval_required", f"Approval required: {sorted(action_tokens & approval)}.")
    elif bool(payload.get("paid_api", False)):
        result = ("ask", "paid_api", "External paid API requires approval.")
    elif epsilon >= float(POLICY.get("epsilon_degrade", 0.7)):
        result = ("degrade", "high_uncertainty", f"epsilon={epsilon:.2f}.")
    else:
        result = ("allow", "pass", "Allowed with witness.")

    decision, gate, reason = result
    event = {
        "id": witness_id({"payload": payload, "ts_bucket": int(time.time() // 60)}),
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "action": action,
        "decision": decision,
        "gate": gate,
        "reason": reason,
        "payload": payload,
    }
    write_event(event)
    return event


class Handler(BaseHTTPRequestHandler):
    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            self._json(200, {"ok": True, "service": "claudio-guardian", "port": PORT})
        elif path == "/events":
            self._json(200, {"events": EVENTS[-50:]})
        else:
            self._json(404, {"error": "not_found"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/decide":
            self._json(404, {"error": "not_found"})
            return
        length = int(self.headers.get("Content-Length", "0") or 0)
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        except Exception:
            self._json(400, {"error": "invalid_json"})
            return
        self._json(200, decide(payload))

    def log_message(self, fmt, *args):
        return


if __name__ == "__main__":
    print(f"claudio-guardian listening on http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), Handler).serve_forever()
