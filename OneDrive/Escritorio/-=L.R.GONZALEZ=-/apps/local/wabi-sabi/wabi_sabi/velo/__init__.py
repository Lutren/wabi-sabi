"""Wabi Velo: peripheral-level browser bridge to web AI services.

The Velo lets Wabi type a prompt into a web AI UI (ChatGPT, Gemini, DeepSeek,
Kimi, Claude, Grok, ...), submit it, wait for the answer to finish streaming,
and extract the response text. It is the Option-C fallback: it needs no API
key, only a real browser profile where the operator is already signed in.

Security model (kept identical to the cloud path):
- The Velo only ever sends the explicit prompt text. It never reads workspace
  files, .env, credentials, or private canon.
- Prompts are redacted before they leave the process.
- Any response is advisory/proposal-only. Code still goes through Wabi's
  validate -> ActionGate -> PatchPlan -> SafeExecutor chain.
- The Velo never performs a publish, deploy, push, purchase, or destructive
  delete. It only types into a text box and reads the answer.
"""

from __future__ import annotations

from wabi_sabi.velo.sites import SITES, VeloSite, normalize_site, site_keys

__all__ = ["SITES", "VeloSite", "normalize_site", "site_keys"]
