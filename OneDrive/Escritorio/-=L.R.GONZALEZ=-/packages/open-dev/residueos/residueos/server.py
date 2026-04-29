from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .gate import evaluate_action
from .store import ResidueStore


def json_bytes(data: Any) -> bytes:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")


def make_handler(db_path: str | Path) -> type[BaseHTTPRequestHandler]:
    store = ResidueStore(db_path)

    class ResidueOSHandler(BaseHTTPRequestHandler):
        server_version = "ResidueOS/0.1"

        def log_message(self, format: str, *args: Any) -> None:
            return

        def send_json(self, status: int, body: Any) -> None:
            data = json_bytes(body)
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def read_json(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length") or "0")
            if length > 2_000_000:
                raise ValueError("payload too large")
            raw = self.rfile.read(length) if length else b"{}"
            data = json.loads(raw.decode("utf-8") or "{}")
            if not isinstance(data, dict):
                raise ValueError("payload must be a JSON object")
            return data

        def do_GET(self) -> None:
            path = urlparse(self.path).path
            if path == "/api/health":
                self.send_json(200, {"ok": True, "name": "ResidueOS", "schemaVersion": "residueos.api.v1"})
                return
            if path == "/api/actions":
                self.send_json(200, store.list_actions())
                return
            if path == "/api/dashboard":
                self.send_json(200, store.dashboard_stats())
                return
            if path.startswith("/api/actions/"):
                action_id = path.split("/")[3]
                record = store.get_action(action_id)
                self.send_json(200, record) if record else self.send_json(404, {"error": "not found"})
                return
            if path.startswith("/api/"):
                self.send_json(404, {"error": "unknown endpoint"})
                return
            self.send_json(200, {"name": "ResidueOS", "api": "/api/health"})

        def do_POST(self) -> None:
            path = urlparse(self.path).path
            try:
                if path == "/api/evaluate":
                    action = self.read_json()
                    decision = evaluate_action(action)
                    self.send_json(200, store.insert_action(action, decision))
                    return

                if path.startswith("/api/actions/") and path.endswith("/approve"):
                    action_id = path.split("/")[3]
                    body = self.read_json()
                    record = store.update_human_decision(
                        action_id,
                        "APPROVED",
                        reviewer=str(body.get("reviewer") or "human"),
                        note=str(body.get("note") or ""),
                    )
                    self.send_json(200, record) if record else self.send_json(404, {"error": "not found"})
                    return

                if path.startswith("/api/actions/") and path.endswith("/block"):
                    action_id = path.split("/")[3]
                    body = self.read_json()
                    record = store.update_human_decision(
                        action_id,
                        "BLOCKED",
                        reviewer=str(body.get("reviewer") or "human"),
                        note=str(body.get("note") or ""),
                    )
                    self.send_json(200, record) if record else self.send_json(404, {"error": "not found"})
                    return

                self.send_json(404, {"error": "unknown endpoint"})
            except (json.JSONDecodeError, ValueError) as exc:
                self.send_json(400, {"error": str(exc)})

    return ResidueOSHandler


def run_server(db_path: str | Path, host: str = "127.0.0.1", port: int = 8787) -> None:
    server = ThreadingHTTPServer((host, port), make_handler(db_path))
    print(f"ResidueOS running on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
