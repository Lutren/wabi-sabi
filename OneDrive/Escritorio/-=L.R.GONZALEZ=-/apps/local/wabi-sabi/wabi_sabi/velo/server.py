"""Local HTTP server that exposes the Velo browser driver to Wabi.

Wabi's BrowserBridge already knows how to POST a prompt to a localhost
WebBridge endpoint and read back ``{ok, status, output}``. This server *is*
that endpoint. It binds to localhost only, serves one request at a time
(Playwright's sync API is single-threaded), and forwards each prompt to a
shared :class:`VeloDriver`.

Transport contract
------------------
``POST /``  body  ``{"service": "chatgpt", "prompt": "..."}``
            reply ``{"ok": true, "status": 200, "output": "...", "site": "chatgpt"}``
``GET /health`` reply ``{"ok": true, "service": "wabi-velo", "sites": [...]}``

Only loopback binds are allowed; a non-local host raises at construction.
"""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from wabi_sabi.velo.driver import VeloDriver, VeloDriverError
from wabi_sabi.velo.sites import normalize_site, site_keys

_LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1", ""}
VELO_SERVER_SCHEMA = "wabi.velo_server.v0_1"


class _VeloHandler(BaseHTTPRequestHandler):
    """One-request-at-a-time handler bound to a shared VeloDriver."""

    protocol_version = "HTTP/1.1"

    # -- helpers -----------------------------------------------------------
    def _send(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except Exception:  # pragma: no cover - client hung up
            pass

    def log_message(self, *_args: Any) -> None:  # noqa: D401 - silence stdlib noise
        """Suppress the default stderr access log."""

    # -- routes ------------------------------------------------------------
    def do_GET(self) -> None:  # noqa: N802 - stdlib naming
        if self.path.rstrip("/") in ("", "/health"):
            self._send(
                200,
                {
                    "ok": True,
                    "schema": VELO_SERVER_SCHEMA,
                    "service": "wabi-velo",
                    "status": 200,
                    "sites": site_keys(),
                    "headless": self.server.velo_driver.headless,  # type: ignore[attr-defined]
                },
            )
            return
        self._send(404, {"ok": False, "status": 404, "error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802 - stdlib naming
        try:
            length = int(self.headers.get("Content-Length", "0") or "0")
        except ValueError:
            length = 0
        raw = self.rfile.read(length) if length > 0 else b""
        try:
            request = json.loads(raw.decode("utf-8")) if raw else {}
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send(400, {"ok": False, "status": 400, "error": "invalid_json_body"})
            return
        if not isinstance(request, dict):
            self._send(400, {"ok": False, "status": 400, "error": "request_must_be_object"})
            return

        prompt = str(request.get("prompt", "")).strip()
        if not prompt:
            self._send(400, {"ok": False, "status": 400, "error": "missing_prompt"})
            return
        service = request.get("service") or self.server.velo_default_site  # type: ignore[attr-defined]
        site = normalize_site(str(service))
        if site is None:
            self._send(
                400,
                {"ok": False, "status": 400, "error": f"unknown_site:{service}", "sites": site_keys()},
            )
            return

        server: "VeloServer" = self.server  # type: ignore[assignment]
        with server.velo_lock:
            try:
                result = server.velo_driver.ask(
                    site=site,
                    prompt=prompt,
                    answer_timeout=server.velo_answer_timeout,
                )
            except VeloDriverError as exc:
                self._send(
                    502,
                    {"ok": False, "status": 502, "site": site, "error": str(exc)},
                )
                return

        payload = {
            "ok": result.ok,
            "status": 200 if result.ok else 502,
            "schema": VELO_SERVER_SCHEMA,
            "site": result.site,
            "output": result.output,
            "error": result.error,
            "velo_status": result.status,
            "elapsed_seconds": round(result.elapsed_seconds, 2),
        }
        self._send(200 if result.ok else 502, payload)


class VeloServer(HTTPServer):
    """Single-threaded HTTP server owning one persistent VeloDriver."""

    def __init__(
        self,
        *,
        driver: VeloDriver,
        host: str = "127.0.0.1",
        port: int = 8777,
        default_site: str = "chatgpt",
        answer_timeout: float = 120.0,
    ) -> None:
        if host not in _LOOPBACK_HOSTS:
            raise ValueError(f"velo_server_must_bind_loopback:{host}")
        super().__init__((host or "127.0.0.1", port), _VeloHandler)
        self.velo_driver = driver
        self.velo_lock = threading.Lock()
        self.velo_default_site = default_site
        self.velo_answer_timeout = answer_timeout

    @property
    def url(self) -> str:
        host, port = self.server_address[:2]
        return f"http://{host}:{port}"


def serve_velo(
    *,
    driver: VeloDriver,
    host: str = "127.0.0.1",
    port: int = 8777,
    default_site: str = "chatgpt",
    answer_timeout: float = 120.0,
) -> VeloServer:
    """Build and return a (not yet serving) :class:`VeloServer`.

    The caller is responsible for ``driver.start()`` and ``server.serve_forever()``
    on the *same* thread, because Playwright's sync API is single-threaded.
    """

    return VeloServer(
        driver=driver,
        host=host,
        port=port,
        default_site=default_site,
        answer_timeout=answer_timeout,
    )
