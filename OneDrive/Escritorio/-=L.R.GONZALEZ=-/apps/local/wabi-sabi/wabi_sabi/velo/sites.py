"""Web AI service definitions for the Velo browser bridge.

Each :class:`VeloSite` describes how to drive one web AI UI: where the input
box is, how to submit, and where the answer renders. Selectors are ordered
fallback lists because these UIs change often; the driver also has a generic
heuristic fallback so a single broken selector does not kill the run.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class VeloSite:
    """How to drive one web AI service."""

    key: str
    label: str
    url: str
    # Ordered CSS selectors for the prompt input (textarea / contenteditable).
    input_selectors: tuple[str, ...]
    # Ordered CSS selectors for the assistant response containers.
    response_selectors: tuple[str, ...]
    # Selectors that, when present, mean a generation is still streaming.
    busy_selectors: tuple[str, ...] = ()
    # Optional explicit submit button; empty means "press Enter".
    submit_selectors: tuple[str, ...] = ()
    # Substrings that, if visible, indicate a login / paywall wall.
    auth_markers: tuple[str, ...] = ()
    needs_login: bool = True
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# Ordered by how reliably the free web tier works without friction.
SITES: dict[str, VeloSite] = {
    "chatgpt": VeloSite(
        key="chatgpt",
        label="ChatGPT",
        url="https://chatgpt.com/",
        input_selectors=(
            "#prompt-textarea",
            "div[contenteditable='true']",
            "textarea[data-testid='prompt-textarea']",
            "textarea",
        ),
        response_selectors=(
            "div[data-message-author-role='assistant'] .markdown",
            "div[data-message-author-role='assistant']",
            ".markdown.prose",
        ),
        busy_selectors=(
            "button[data-testid='stop-button']",
            "button[aria-label='Stop streaming']",
            "button[aria-label*='Stop']",
        ),
        submit_selectors=(
            "button[data-testid='send-button']",
            "button[aria-label='Send prompt']",
        ),
        auth_markers=("Log in", "Sign up", "Welcome back"),
        needs_login=False,
        notes="Free web tier usable; sign-in lifts rate limits.",
    ),
    "deepseek": VeloSite(
        key="deepseek",
        label="DeepSeek",
        url="https://chat.deepseek.com/",
        input_selectors=(
            "#chat-input",
            "textarea#chat-input",
            "textarea[placeholder]",
            "textarea",
        ),
        response_selectors=(
            ".ds-markdown",
            "div[class*='_4f9bf79']",
            "div[class*='markdown']",
        ),
        busy_selectors=(
            "div[class*='_8b1f7c7']",
            "div[class*='stop']",
        ),
        auth_markers=("Log in", "Sign in", "Phone number", "Email address"),
        needs_login=True,
        notes="Requires a DeepSeek sign-in; profile keeps the session.",
    ),
    "gemini": VeloSite(
        key="gemini",
        label="Gemini",
        url="https://gemini.google.com/app",
        input_selectors=(
            "div.ql-editor[contenteditable='true']",
            "rich-textarea div[contenteditable='true']",
            "div[contenteditable='true']",
            "textarea",
        ),
        response_selectors=(
            "message-content .markdown",
            ".model-response-text",
            "message-content",
            ".markdown",
        ),
        busy_selectors=(
            "button[aria-label*='Stop']",
            ".stop-icon",
        ),
        submit_selectors=(
            "button.send-button",
            "button[aria-label*='Send']",
        ),
        auth_markers=("Sign in", "Iniciar sesión"),
        needs_login=True,
        notes="Requires a Google sign-in; generous free tier in browser.",
    ),
    "kimi": VeloSite(
        key="kimi",
        label="Kimi",
        url="https://www.kimi.com/",
        input_selectors=(
            "[data-testid='msh-chatinput-editor']",
            ".chat-input-editor",
            "div[contenteditable='true']",
            "textarea",
        ),
        response_selectors=(
            ".segment-content",
            ".markdown-container",
            "div[class*='markdown']",
        ),
        busy_selectors=(
            ".stop-btn",
            "button[class*='stop']",
        ),
        auth_markers=("Log in", "Sign in", "登录"),
        needs_login=True,
        notes="Moonshot Kimi; free tier after sign-in.",
    ),
    "claude": VeloSite(
        key="claude",
        label="Claude",
        url="https://claude.ai/new",
        input_selectors=(
            "div.ProseMirror[contenteditable='true']",
            "div[contenteditable='true']",
            "textarea",
        ),
        response_selectors=(
            "div.font-claude-message",
            "div[data-testid='message-content']",
            ".prose",
        ),
        busy_selectors=(
            "button[aria-label='Stop response']",
            "button[aria-label*='Stop']",
        ),
        auth_markers=("Sign in", "Continue with"),
        needs_login=True,
        notes="Anthropic Claude web; free tier after sign-in.",
    ),
    "grok": VeloSite(
        key="grok",
        label="Grok",
        url="https://grok.com/",
        input_selectors=(
            "textarea[aria-label*='Ask']",
            "textarea",
            "div[contenteditable='true']",
        ),
        response_selectors=(
            ".message-bubble",
            "div[class*='markdown']",
            ".prose",
        ),
        busy_selectors=(
            "button[aria-label*='Stop']",
        ),
        auth_markers=("Sign in", "Sign up"),
        needs_login=True,
        notes="xAI Grok; free tier after sign-in.",
    ),
}

# Aliases so the operator can type the obvious thing.
_ALIASES: dict[str, str] = {
    "gpt": "chatgpt",
    "chat-gpt": "chatgpt",
    "openai": "chatgpt",
    "ds": "deepseek",
    "deep-seek": "deepseek",
    "deepseek-chat": "deepseek",
    "google": "gemini",
    "gemini-web": "gemini",
    "bard": "gemini",
    "moonshot": "kimi",
    "anthropic": "claude",
    "claude-web": "claude",
    "xai": "grok",
}

# Default order the Velo tries when no service is named: most-likely-to-work
# free web tiers first.
DEFAULT_ORDER: tuple[str, ...] = ("chatgpt", "gemini", "deepseek", "kimi", "claude", "grok")


def site_keys() -> list[str]:
    """Return the canonical site keys in default-preference order."""

    return list(DEFAULT_ORDER)


def normalize_site(name: str | None) -> str | None:
    """Resolve an operator-typed service name to a canonical site key."""

    if not name:
        return None
    raw = str(name).strip().lower().replace("_", "-")
    if raw in SITES:
        return raw
    if raw in _ALIASES:
        return _ALIASES[raw]
    # Tolerate a pasted URL.
    for key, site in SITES.items():
        host = site.url.split("//", 1)[-1].split("/", 1)[0]
        if raw and (raw in host or host in raw):
            return key
    return None
