"""Tests for the Velo browser bridge (Option C).

These tests never launch a real browser. The driver is faked so the HTTP
transport, the security screening, and the site registry are all exercised
deterministically.
"""

from __future__ import annotations

import json
import threading
import urllib.request

import pytest

from wabi_sabi.velo.driver import VeloAskResult, playwright_available
from wabi_sabi.velo.runner import screen_prompt, velo_status
from wabi_sabi.velo.server import VeloServer, serve_velo
from wabi_sabi.velo.sites import SITES, normalize_site, site_keys


# -- site registry ---------------------------------------------------------
def test_site_keys_are_canonical_and_ordered():
    keys = site_keys()
    assert keys[0] == "chatgpt"
    assert set(keys) == set(SITES)
    for key in keys:
        assert SITES[key].key == key
        assert SITES[key].url.startswith("https://")
        assert SITES[key].input_selectors
        assert SITES[key].response_selectors


def test_normalize_site_resolves_aliases_and_urls():
    assert normalize_site("gpt") == "chatgpt"
    assert normalize_site("DeepSeek") == "deepseek"
    assert normalize_site("google") == "gemini"
    assert normalize_site("moonshot") == "kimi"
    assert normalize_site("https://claude.ai/new") == "claude"
    assert normalize_site("does-not-exist") is None
    assert normalize_site("") is None
    assert normalize_site(None) is None


# -- security screening ----------------------------------------------------
def test_screen_prompt_allows_public_prompt():
    screen = screen_prompt("Explica que es una funcion recursiva en Python.")
    assert screen["ok"] is True
    assert screen["gate"] in {"APPROVE", "REVIEW"}
    assert screen["redacted"]


def test_screen_prompt_blocks_destructive_request():
    screen = screen_prompt("borra todo y haz git push --force al repositorio remoto")
    assert screen["ok"] is False
    assert screen["gate"] == "BLOCK"
    assert screen["reasons"]


def test_screen_prompt_redacts_api_key_value():
    screen = screen_prompt("usa esta clave nvapi-supersecret-key-1234567890 para conectarte")
    assert "nvapi-supersecret-key-1234567890" not in screen["redacted"]
    assert screen["was_redacted"] is True


# -- status ----------------------------------------------------------------
def test_velo_status_reports_sites_and_enable_env(tmp_path):
    status = velo_status(tmp_path)
    assert status["schema"] == "wabi.velo.v0_1"
    assert status["enable_env"] == "WABI_ALLOW_VELO"
    assert status["sites"] == site_keys()
    assert status["publication_gate"] == "BLOCK"
    assert status["playwright_importable"] is playwright_available()[0]


# -- HTTP server (faked driver) -------------------------------------------
class _FakeDriver:
    """Stands in for VeloDriver: no browser, deterministic answers."""

    headless = True

    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def ask(self, *, site: str, prompt: str, answer_timeout: float = 120.0) -> VeloAskResult:
        self.calls.append((site, prompt))
        if prompt == "FAIL":
            return VeloAskResult(ok=False, site=site, error="velo_empty_response", status="EMPTY_RESPONSE")
        return VeloAskResult(ok=True, site=site, output=f"answer-for:{prompt}", status="VELO_OK")


def _serve_in_thread(server: VeloServer) -> threading.Thread:
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.1}, daemon=True)
    thread.start()
    return thread


def _post(url: str, body: dict) -> tuple[int, dict]:
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:  # pragma: no cover - defensive
        return exc.code, json.loads(exc.read().decode("utf-8"))


def test_velo_server_rejects_non_loopback_host():
    with pytest.raises(ValueError):
        serve_velo(driver=_FakeDriver(), host="0.0.0.0", port=0)


def test_velo_server_health_and_ask_round_trip():
    driver = _FakeDriver()
    server = serve_velo(driver=driver, host="127.0.0.1", port=0, default_site="chatgpt")
    thread = _serve_in_thread(server)
    try:
        base = server.url
        with urllib.request.urlopen(base + "/health", timeout=5) as response:
            health = json.loads(response.read().decode("utf-8"))
        assert health["ok"] is True
        assert health["service"] == "wabi-velo"
        assert "chatgpt" in health["sites"]

        status, payload = _post(base + "/", {"service": "deepseek", "prompt": "hola"})
        assert status == 200
        assert payload["ok"] is True
        assert payload["site"] == "deepseek"
        assert payload["output"] == "answer-for:hola"
        assert driver.calls == [("deepseek", "hola")]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_velo_server_uses_default_site_when_service_missing():
    driver = _FakeDriver()
    server = serve_velo(driver=driver, host="127.0.0.1", port=0, default_site="gemini")
    thread = _serve_in_thread(server)
    try:
        status, payload = _post(server.url + "/", {"prompt": "sin servicio"})
        assert status == 200
        assert payload["site"] == "gemini"
        assert driver.calls[0][0] == "gemini"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_velo_server_rejects_missing_prompt_and_unknown_site():
    driver = _FakeDriver()
    server = serve_velo(driver=driver, host="127.0.0.1", port=0)
    thread = _serve_in_thread(server)
    try:
        status, payload = _post(server.url + "/", {"service": "chatgpt"})
        assert status == 400
        assert payload["error"] == "missing_prompt"

        status, payload = _post(server.url + "/", {"service": "nope", "prompt": "x"})
        assert status == 400
        assert payload["error"].startswith("unknown_site")
        assert driver.calls == []
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_velo_server_propagates_driver_failure_status():
    driver = _FakeDriver()
    server = serve_velo(driver=driver, host="127.0.0.1", port=0)
    thread = _serve_in_thread(server)
    try:
        status, payload = _post(server.url + "/", {"service": "chatgpt", "prompt": "FAIL"})
        assert status == 502
        assert payload["ok"] is False
        assert payload["velo_status"] == "EMPTY_RESPONSE"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_velo_ask_result_to_dict_round_trip():
    result = VeloAskResult(ok=True, site="chatgpt", output="hi", status="VELO_OK", elapsed_seconds=1.234)
    data = result.to_dict()
    assert data["ok"] is True
    assert data["site"] == "chatgpt"
    assert data["elapsed_seconds"] == 1.23
