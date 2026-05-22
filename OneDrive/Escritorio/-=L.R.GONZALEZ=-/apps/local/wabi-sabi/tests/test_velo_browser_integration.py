"""End-to-end Velo test against a local mock chat page.

This launches a *real* Chromium via the real :class:`VeloDriver` and drives a
local HTML page that behaves like a streaming chat UI (textarea -> Enter ->
a response div fills in over time). It proves the full mechanic: navigate,
locate input, type, submit, wait for the answer to stabilise, extract text.

No external network, no AI service, no credentials. Skipped automatically if
Chromium is not installed.
"""

from __future__ import annotations

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from wabi_sabi.velo.driver import VeloDriver, _chromium_ok
from wabi_sabi.velo.sites import SITES, VeloSite

# A minimal page: #prompt-textarea + Enter spawns a streaming assistant div.
_MOCK_CHAT_HTML = """<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><title>Mock Chat</title></head>
<body>
<div id="chat"></div>
<textarea id="prompt-textarea" rows="3" cols="80"></textarea>
<script>
  const ta = document.getElementById('prompt-textarea');
  ta.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      const q = ta.value;
      ta.value = '';
      const wrap = document.createElement('div');
      wrap.setAttribute('data-message-author-role', 'assistant');
      const md = document.createElement('div');
      md.className = 'markdown';
      wrap.appendChild(md);
      document.getElementById('chat').appendChild(wrap);
      const full = 'ECHO: ' + q + ' [fin]';
      let i = 0;
      const timer = setInterval(function () {
        i += 6;
        md.innerText = full.slice(0, i);
        if (i >= full.length) { clearInterval(timer); }
      }, 150);
    }
  });
</script>
</body></html>
"""


class _MockChatHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 - stdlib naming
        body = _MOCK_CHAT_HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):  # noqa: D401 - silence
        pass


@pytest.fixture()
def mock_chat_server():
    server = HTTPServer(("127.0.0.1", 0), _MockChatHandler)
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.1}, daemon=True)
    thread.start()
    host, port = server.server_address[:2]
    try:
        yield f"http://{host}:{port}/"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


@pytest.mark.skipif(not _chromium_ok(), reason="Chromium not installed for Playwright")
def test_velo_driver_drives_real_browser_against_mock_chat(mock_chat_server, tmp_path):
    mock_site = VeloSite(
        key="mock",
        label="Mock Chat",
        url=mock_chat_server,
        input_selectors=("#prompt-textarea", "textarea"),
        response_selectors=("div[data-message-author-role='assistant'] .markdown",),
        busy_selectors=(),
        needs_login=False,
    )
    SITES["mock"] = mock_site
    try:
        driver = VeloDriver(profile_dir=tmp_path / "profile", headless=True)
        try:
            result = driver.ask(
                site="mock",
                prompt="prueba velo 123",
                answer_timeout=40.0,
                stable_seconds=2.0,
                poll_seconds=0.8,
            )
        finally:
            driver.close()
    finally:
        SITES.pop("mock", None)

    assert result.ok is True, f"velo failed: {result.error} / {result.status}"
    assert "ECHO: prueba velo 123" in result.output
    assert result.output.endswith("[fin]")
    assert result.status == "VELO_OK"
    assert result.elapsed_seconds > 0
