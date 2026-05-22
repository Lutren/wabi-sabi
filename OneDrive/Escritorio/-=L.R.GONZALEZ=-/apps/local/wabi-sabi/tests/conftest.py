"""Shared pytest configuration for the Wabi-Sabi test suite.

The operator's real machine now has cloud + Ollama enabled persistently
(``WABI_ALLOW_CLOUD_PROVIDERS=1`` etc. in the Windows user environment), and
some code paths call ``os.environ.setdefault(...)`` at runtime. Both of those
would leak provider-routing toggles into tests that assume a clean,
local-only baseline -- making the suite pass or fail depending on the host.

This autouse fixture deletes those routing/enablement toggles before *every*
test so the suite is hermetic. A test that needs one of them simply sets it
with ``monkeypatch.setenv(...)`` inside the test body; that runs after this
fixture and therefore wins.
"""

from __future__ import annotations

import pytest

# Behaviour toggles that must never leak in from the host environment.
# These only switch routing/enablement -- not API keys -- so scrubbing them
# is safe: tests that want a behaviour opt in explicitly.
_LEAKABLE_WABI_ENV: tuple[str, ...] = (
    "WABI_ALLOW_CLOUD_PROVIDERS",
    "WABI_PROVIDER_ORDER",
    "WABI_ENABLE_OLLAMA",
    "WABI_DISABLE_BASE_MODEL",
    "WABI_BUILD_ASSIST_CLOUD",
    "WABI_BUILD_ASSIST_NVIDIA_MODEL_ALIAS",
    "WABI_ALLOW_CLOUD_MODELS",
    "MEDIOEVO_NO_MODEL_MODE",
    "WABI_ALLOW_BROWSER_BRIDGE",
    "WABI_ALLOW_BROWSER_SEND",
    "WABI_KIMI_WEBBRIDGE_URL",
    "WABI_ALLOW_VELO",
    "WABI_VELO_URL",
    "WABI_VELO_HEADLESS",
)


@pytest.fixture(autouse=True)
def _hermetic_wabi_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Scrub host-leaked Wabi routing toggles before each test."""

    for name in _LEAKABLE_WABI_ENV:
        monkeypatch.delenv(name, raising=False)
