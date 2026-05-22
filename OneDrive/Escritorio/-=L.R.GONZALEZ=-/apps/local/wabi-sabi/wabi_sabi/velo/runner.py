"""High-level Velo orchestration used by the Wabi CLI.

This module is the safe entry point. Every prompt is screened by
:class:`ActionGate` and redacted before a browser is ever touched, so the
Velo can never type a secret, a destructive command, or a publish action
into a web AI box.
"""

from __future__ import annotations

import json
import shutil
import time
from pathlib import Path
from typing import Any

from wabi_sabi.core.gate import ActionGate
from wabi_sabi.core.redaction import redact_text
from wabi_sabi.core.tools import write_artifact
from wabi_sabi.velo.driver import VeloAskResult, VeloDriver, playwright_available
from wabi_sabi.velo.server import serve_velo
from wabi_sabi.velo.sites import SITES, normalize_site, site_keys

VELO_SCHEMA = "wabi.velo.v0_1"
VELO_ENABLE_ENV = "WABI_ALLOW_VELO"


def _profile_dir(runtime_root: str | Path) -> Path:
    return Path(runtime_root) / "velo" / "profile"


def _outputs_dir(runtime_root: str | Path) -> Path:
    return Path(runtime_root) / "outputs" / "velo"


def velo_status(runtime_root: str | Path) -> dict[str, Any]:
    """Report Velo capabilities without launching a browser."""

    importable, detail = playwright_available()
    chromium_ready = False
    chromium_detail = "playwright_not_importable"
    if importable:
        chromium_ready, chromium_detail = _chromium_installed()
    profile = _profile_dir(runtime_root)
    return {
        "ok": importable and chromium_ready,
        "schema": VELO_SCHEMA,
        "action": "velo_status",
        "gate": "APPROVE",
        "playwright_importable": importable,
        "playwright_detail": detail,
        "chromium_ready": chromium_ready,
        "chromium_detail": chromium_detail,
        "profile_dir": str(profile),
        "profile_exists": profile.exists(),
        "sites": site_keys(),
        "site_catalog": {key: SITES[key].to_dict() for key in site_keys()},
        "enable_env": VELO_ENABLE_ENV,
        "authority": "browser_response_is_proposal_only",
        "publication_gate": "BLOCK",
        "next_step": (
            "run: wabi velo login <site>  (sign in once), then: wabi velo ask <site> \"...\""
            if importable and chromium_ready
            else "run: python -m playwright install chromium"
        ),
    }


def _chromium_installed() -> tuple[bool, str]:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # pragma: no cover - import guard
        return False, f"playwright_import_failed:{exc}"
    try:
        pw = sync_playwright().start()
    except Exception as exc:  # pragma: no cover - runtime guard
        return False, f"playwright_start_failed:{exc}"
    try:
        path = pw.chromium.executable_path
        ready = bool(path) and Path(path).exists()
        return ready, "chromium_executable_present" if ready else "chromium_not_installed"
    except Exception as exc:  # pragma: no cover - runtime guard
        return False, f"chromium_probe_failed:{exc}"
    finally:
        try:
            pw.stop()
        except Exception:  # pragma: no cover - best-effort
            pass


def screen_prompt(prompt: str) -> dict[str, Any]:
    """Gate + redact a prompt before any browser action.

    Returns a dict with ``ok`` (safe to send), ``gate``, ``reasons`` and the
    ``redacted`` prompt text that is actually safe to type.
    """

    text = (prompt or "").strip()
    decision = ActionGate().evaluate_text(text)
    redacted = redact_text(text)
    return {
        "ok": decision.gate != "BLOCK",
        "gate": decision.gate,
        "reasons": list(decision.reasons),
        "redacted": redacted,
        "was_redacted": redacted != text,
    }


def velo_ask(
    *,
    runtime_root: str | Path,
    service: str | None,
    prompt: str,
    headless: bool | None = None,
    answer_timeout: float = 120.0,
) -> dict[str, Any]:
    """One-shot: open a browser, ask one web AI, return the answer.

    The browser closes when the call finishes. Use :func:`velo_serve` for a
    long-lived bridge that keeps the profile warm.
    """

    site = normalize_site(service) or site_keys()[0]
    screen = screen_prompt(prompt)
    if not screen["ok"]:
        return {
            "ok": False,
            "schema": VELO_SCHEMA,
            "action": "velo_ask_blocked",
            "gate": screen["gate"],
            "site": site,
            "reasons": screen["reasons"],
            "error": "velo_prompt_blocked_by_action_gate",
            "online_ai_called": False,
            "publication_gate": "BLOCK",
        }

    importable, detail = playwright_available()
    if not importable:
        return {
            "ok": False,
            "schema": VELO_SCHEMA,
            "action": "velo_ask_unavailable",
            "gate": "REVIEW",
            "site": site,
            "error": detail,
            "online_ai_called": False,
            "next_step": "pip install playwright && python -m playwright install chromium",
        }

    driver = VeloDriver(profile_dir=_profile_dir(runtime_root), headless=headless)
    try:
        result = driver.ask(site=site, prompt=screen["redacted"], answer_timeout=answer_timeout)
    finally:
        driver.close()

    return _result_payload(
        runtime_root=runtime_root,
        action="velo_ask",
        result=result,
        screen=screen,
    )


def _result_payload(
    *,
    runtime_root: str | Path,
    action: str,
    result: VeloAskResult,
    screen: dict[str, Any],
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "ok": result.ok,
        "schema": VELO_SCHEMA,
        "action": action,
        "gate": "APPROVE" if result.ok else "REVIEW",
        "site": result.site,
        "output": redact_text(result.output),
        "velo_status": result.status,
        "error": result.error,
        "elapsed_seconds": round(result.elapsed_seconds, 2),
        "was_redacted": screen.get("was_redacted", False),
        "online_ai_called": result.ok,
        "browser_backend_called": True,
        "authority": "browser_response_is_proposal_only",
        "local_revalidation_required": True,
        "publication_gate": "BLOCK",
    }
    record = {
        "schema": VELO_SCHEMA,
        "action": action,
        "site": result.site,
        "ok": result.ok,
        "velo_status": result.status,
        "elapsed_seconds": round(result.elapsed_seconds, 2),
        "output": redact_text(result.output),
        "error": result.error,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    try:
        artifact = write_artifact(
            _outputs_dir(runtime_root),
            f"velo_{result.site}",
            ".json",
            json.dumps(record, indent=2, ensure_ascii=False) + "\n",
        )
        payload["artifact"] = str(artifact)
    except Exception:  # pragma: no cover - artifact best-effort
        payload["artifact"] = ""
    return payload


def velo_login(
    *,
    runtime_root: str | Path,
    service: str | None,
    wait_seconds: float = 240.0,
) -> dict[str, Any]:
    """Open a visible browser on a site so the operator can sign in once.

    The persistent profile keeps the session for later ``velo ask`` calls.
    Blocks until the operator closes the window or ``wait_seconds`` elapse.
    """

    site = normalize_site(service)
    if site is None:
        return {
            "ok": False,
            "schema": VELO_SCHEMA,
            "action": "velo_login",
            "gate": "REVIEW",
            "error": f"unknown_site:{service}",
            "sites": site_keys(),
        }
    importable, detail = playwright_available()
    if not importable:
        return {
            "ok": False,
            "schema": VELO_SCHEMA,
            "action": "velo_login",
            "gate": "REVIEW",
            "error": detail,
            "next_step": "pip install playwright && python -m playwright install chromium",
        }

    driver = VeloDriver(profile_dir=_profile_dir(runtime_root), headless=False)
    try:
        driver.start()
        driver._goto(SITES[site])  # noqa: SLF001 - intentional internal reuse
        deadline = time.monotonic() + wait_seconds
        while time.monotonic() < deadline:
            if not driver._context or not driver._context.pages:  # noqa: SLF001
                break
            time.sleep(1.0)
    finally:
        driver.close()
    return {
        "ok": True,
        "schema": VELO_SCHEMA,
        "action": "velo_login",
        "gate": "APPROVE",
        "site": site,
        "profile_dir": str(_profile_dir(runtime_root)),
        "note": "session stored in the persistent profile; rerun is not needed unless it expires",
    }


def velo_serve(
    *,
    runtime_root: str | Path,
    host: str = "127.0.0.1",
    port: int = 8777,
    default_site: str = "chatgpt",
    headless: bool | None = None,
    answer_timeout: float = 120.0,
) -> dict[str, Any]:
    """Run the Velo HTTP bridge until interrupted (blocking).

    Returns a summary dict after the server stops. Wabi's BrowserBridge can
    point ``WABI_KIMI_WEBBRIDGE_URL`` (or ``WABI_VELO_URL``) at this server.
    """

    importable, detail = playwright_available()
    if not importable:
        return {
            "ok": False,
            "schema": VELO_SCHEMA,
            "action": "velo_serve",
            "gate": "REVIEW",
            "error": detail,
            "next_step": "pip install playwright && python -m playwright install chromium",
        }

    driver = VeloDriver(profile_dir=_profile_dir(runtime_root), headless=headless)
    server = serve_velo(
        driver=driver,
        host=host,
        port=port,
        default_site=normalize_site(default_site) or "chatgpt",
        answer_timeout=answer_timeout,
    )
    started = time.monotonic()
    interrupted = False
    try:
        driver.start()
        print(f"[velo] bridge ready on {server.url}  (default site: {server.velo_default_site})")
        print(f"[velo] direct use:        wabi velo ask <site> \"...\"")
        print(f"[velo] wire into bridge:  set WABI_KIMI_WEBBRIDGE_URL={server.url}")
        print(f"[velo]                    set WABI_ALLOW_BROWSER_BRIDGE=1")
        print("[velo] press Ctrl+C to stop.")
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:  # pragma: no cover - interactive stop
        interrupted = True
    finally:
        try:
            server.server_close()
        except Exception:  # pragma: no cover - best-effort
            pass
        driver.close()
    return {
        "ok": True,
        "schema": VELO_SCHEMA,
        "action": "velo_serve",
        "gate": "APPROVE",
        "url": server.url,
        "uptime_seconds": round(time.monotonic() - started, 1),
        "interrupted": interrupted,
    }


def velo_reset_profile(runtime_root: str | Path) -> dict[str, Any]:
    """Delete the stored browser profile (sign-ins, cookies, cache)."""

    profile = _profile_dir(runtime_root)
    existed = profile.exists()
    if existed:
        shutil.rmtree(profile, ignore_errors=True)
    return {
        "ok": True,
        "schema": VELO_SCHEMA,
        "action": "velo_reset_profile",
        "gate": "APPROVE",
        "profile_dir": str(profile),
        "removed": existed,
    }
