"""Playwright-backed browser driver for the Velo.

The driver opens a *persistent* browser profile so operator sign-ins survive
between runs, navigates to a web AI service, types a prompt, submits it, waits
for the answer to stop streaming (text-stabilisation, no fragile "done"
selector), and returns the response text.

It is deliberately resilient: every site selector list is tried in order and,
if all fail, a generic heuristic locates the largest visible editable element
(the chat box is almost always the biggest one low in the viewport).
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from wabi_sabi.velo.sites import SITES, VeloSite, normalize_site

# JS: tag the most likely chat input so Playwright can locate it afterwards.
_TAG_INPUT_JS = """
() => {
  const tagged = document.querySelector("[data-wabi-velo-input='1']");
  if (tagged) tagged.removeAttribute('data-wabi-velo-input');
  const els = Array.from(document.querySelectorAll(
    "textarea, [contenteditable='true'], [role='textbox']"));
  let best = null, bestScore = -1;
  for (const el of els) {
    const r = el.getBoundingClientRect();
    if (r.width < 120 || r.height < 14) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    if (el.disabled || el.getAttribute('aria-disabled') === 'true') continue;
    // Chat inputs sit low in the viewport and are wide.
    const score = r.top + Math.min(r.width, 800) * 0.05;
    if (score > bestScore) { bestScore = score; best = el; }
  }
  if (best) { best.setAttribute('data-wabi-velo-input', '1'); return true; }
  return false;
}
"""

# JS: read the innerText of the last element matching any response selector.
_READ_RESPONSE_JS = """
(selectors) => {
  for (const sel of selectors) {
    let nodes;
    try { nodes = document.querySelectorAll(sel); } catch (e) { continue; }
    if (nodes && nodes.length) {
      const last = nodes[nodes.length - 1];
      const text = (last.innerText || last.textContent || '').trim();
      if (text) return { count: nodes.length, text: text, selector: sel };
    }
  }
  return { count: 0, text: '', selector: '' };
}
"""


@dataclass
class VeloAskResult:
    """Outcome of one Velo prompt/answer round-trip."""

    ok: bool
    site: str
    output: str = ""
    error: str = ""
    elapsed_seconds: float = 0.0
    status: str = ""
    artifacts: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "site": self.site,
            "output": self.output,
            "error": self.error,
            "elapsed_seconds": round(self.elapsed_seconds, 2),
            "status": self.status,
            "artifacts": list(self.artifacts),
        }


class VeloDriverError(RuntimeError):
    """Raised when Playwright is unavailable or a browser action fails hard."""


def playwright_available() -> tuple[bool, str]:
    """Return (importable, detail). Does not launch a browser."""

    try:
        import playwright  # noqa: F401
    except Exception as exc:  # pragma: no cover - import guard
        return False, f"playwright_not_installed:{exc}"
    return True, "playwright_importable"


def _chromium_ok() -> bool:
    """Return True when Playwright can find an installed Chromium binary."""

    importable, _ = playwright_available()
    if not importable:
        return False
    try:
        from playwright.sync_api import sync_playwright

        pw = sync_playwright().start()
        try:
            path = pw.chromium.executable_path
            return bool(path) and Path(path).exists()
        finally:
            pw.stop()
    except Exception:  # pragma: no cover - probe guard
        return False


class VeloDriver:
    """Drives one persistent browser context against web AI services.

    Not thread-safe: Playwright's sync API must be used from a single thread.
    The Velo server therefore owns exactly one driver on one worker thread.
    """

    def __init__(
        self,
        *,
        profile_dir: str | Path,
        headless: bool | None = None,
        slow_mo_ms: int = 0,
    ) -> None:
        self.profile_dir = Path(profile_dir)
        if headless is None:
            headless = os.environ.get("WABI_VELO_HEADLESS", "0") == "1"
        self.headless = bool(headless)
        self.slow_mo_ms = max(0, int(slow_mo_ms))
        self._pw: Any = None
        self._context: Any = None
        self._page: Any = None

    # -- lifecycle ---------------------------------------------------------
    def start(self) -> None:
        """Launch the persistent browser context."""

        if self._context is not None:
            return
        ok, detail = playwright_available()
        if not ok:
            raise VeloDriverError(detail)
        from playwright.sync_api import sync_playwright

        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self._pw = sync_playwright().start()
        try:
            self._context = self._pw.chromium.launch_persistent_context(
                user_data_dir=str(self.profile_dir),
                headless=self.headless,
                slow_mo=self.slow_mo_ms,
                viewport={"width": 1280, "height": 900},
                args=["--disable-blink-features=AutomationControlled"],
            )
        except Exception as exc:  # pragma: no cover - launch guard
            self.close()
            raise VeloDriverError(f"velo_browser_launch_failed:{exc}") from exc
        pages = self._context.pages
        self._page = pages[0] if pages else self._context.new_page()

    def close(self) -> None:
        """Close the browser context and stop Playwright."""

        for closer in (self._context, self._pw):
            if closer is None:
                continue
            try:
                if closer is self._context:
                    closer.close()
                else:
                    closer.stop()
            except Exception:  # pragma: no cover - best-effort teardown
                pass
        self._context = None
        self._pw = None
        self._page = None

    def __enter__(self) -> "VeloDriver":
        self.start()
        return self

    def __exit__(self, *_exc: Any) -> None:
        self.close()

    # -- main action -------------------------------------------------------
    def ask(
        self,
        *,
        site: str,
        prompt: str,
        answer_timeout: float = 120.0,
        stable_seconds: float = 4.0,
        poll_seconds: float = 1.5,
    ) -> VeloAskResult:
        """Type ``prompt`` into ``site`` and return the finished answer."""

        key = normalize_site(site)
        if key is None:
            return VeloAskResult(ok=False, site=str(site), error=f"unknown_site:{site}", status="UNKNOWN_SITE")
        target = SITES[key]
        if self._context is None:
            self.start()

        started = time.monotonic()
        try:
            self._goto(target)
            login_wall = self._login_wall(target)
            before = self._read_response(target)
            self._fill_and_submit(target, prompt)
            output = self._wait_for_answer(
                target,
                baseline=before,
                answer_timeout=answer_timeout,
                stable_seconds=stable_seconds,
                poll_seconds=poll_seconds,
            )
        except VeloDriverError as exc:
            return VeloAskResult(
                ok=False,
                site=key,
                error=str(exc),
                status="DRIVER_ERROR",
                elapsed_seconds=time.monotonic() - started,
            )
        except Exception as exc:  # pragma: no cover - unexpected page error
            return VeloAskResult(
                ok=False,
                site=key,
                error=f"velo_unexpected:{type(exc).__name__}:{exc}",
                status="UNEXPECTED_ERROR",
                elapsed_seconds=time.monotonic() - started,
            )

        elapsed = time.monotonic() - started
        if not output.strip():
            status = "LOGIN_REQUIRED" if login_wall else "EMPTY_RESPONSE"
            return VeloAskResult(
                ok=False,
                site=key,
                error="velo_login_wall" if login_wall else "velo_empty_response",
                status=status,
                elapsed_seconds=elapsed,
            )
        return VeloAskResult(ok=True, site=key, output=output.strip(), status="VELO_OK", elapsed_seconds=elapsed)

    # -- steps -------------------------------------------------------------
    def _goto(self, site: VeloSite) -> None:
        page = self._page
        current = (page.url or "").rstrip("/")
        host = site.url.split("//", 1)[-1].split("/", 1)[0]
        if host not in current:
            page.goto(site.url, wait_until="domcontentloaded", timeout=45_000)
        try:
            page.wait_for_load_state("networkidle", timeout=8_000)
        except Exception:
            pass  # SPA keeps a socket open; that is fine.

    def _login_wall(self, site: VeloSite) -> bool:
        if not site.auth_markers:
            return False
        try:
            body = (self._page.inner_text("body", timeout=4_000) or "").lower()
        except Exception:
            return False
        # Treat as a wall only if a marker shows AND no input was found.
        marker_hit = any(marker.lower() in body for marker in site.auth_markers)
        return marker_hit and not self._tag_input(quiet=True)

    def _tag_input(self, *, quiet: bool = False) -> bool:
        try:
            return bool(self._page.evaluate(_TAG_INPUT_JS))
        except Exception:
            if quiet:
                return False
            return False

    def _locate_input(self, site: VeloSite) -> Any:
        page = self._page
        for selector in site.input_selectors:
            try:
                locator = page.locator(selector).first
                locator.wait_for(state="visible", timeout=6_000)
                return locator
            except Exception:
                continue
        # Generic heuristic fallback.
        deadline = time.monotonic() + 12.0
        while time.monotonic() < deadline:
            if self._tag_input():
                return page.locator("[data-wabi-velo-input='1']").first
            time.sleep(0.5)
        raise VeloDriverError("velo_input_not_found")

    def _fill_and_submit(self, site: VeloSite, prompt: str) -> None:
        page = self._page
        locator = self._locate_input(site)
        locator.click(timeout=8_000)
        # Clear any draft, then insert the prompt (works for textarea and
        # contenteditable alike).
        try:
            page.keyboard.press("Control+A")
            page.keyboard.press("Delete")
        except Exception:
            pass
        page.keyboard.insert_text(prompt)
        time.sleep(0.3)
        if site.submit_selectors:
            for selector in site.submit_selectors:
                try:
                    button = page.locator(selector).first
                    button.wait_for(state="visible", timeout=2_500)
                    button.click(timeout=2_500)
                    return
                except Exception:
                    continue
        page.keyboard.press("Enter")

    def _read_response(self, site: VeloSite) -> dict[str, Any]:
        try:
            return dict(self._page.evaluate(_READ_RESPONSE_JS, list(site.response_selectors)))
        except Exception:
            return {"count": 0, "text": "", "selector": ""}

    def _is_busy(self, site: VeloSite) -> bool:
        for selector in site.busy_selectors:
            try:
                if self._page.locator(selector).first.is_visible(timeout=400):
                    return True
            except Exception:
                continue
        return False

    def _wait_for_answer(
        self,
        site: VeloSite,
        *,
        baseline: dict[str, Any],
        answer_timeout: float,
        stable_seconds: float,
        poll_seconds: float,
    ) -> str:
        deadline = time.monotonic() + answer_timeout
        base_count = int(baseline.get("count", 0) or 0)
        base_text = str(baseline.get("text", "") or "")
        last_text = ""
        last_change = time.monotonic()
        saw_new = False

        while time.monotonic() < deadline:
            time.sleep(poll_seconds)
            snapshot = self._read_response(site)
            count = int(snapshot.get("count", 0) or 0)
            text = str(snapshot.get("text", "") or "")

            # A new assistant turn appeared, or the existing one grew.
            is_new = count > base_count or (text and text != base_text)
            if not saw_new:
                if is_new:
                    saw_new = True
                    last_text = text
                    last_change = time.monotonic()
                continue

            if text != last_text:
                last_text = text
                last_change = time.monotonic()
                continue

            # Text is stable; confirm no streaming indicator before returning.
            stable_for = time.monotonic() - last_change
            if stable_for >= stable_seconds and not self._is_busy(site):
                return last_text

        return last_text
