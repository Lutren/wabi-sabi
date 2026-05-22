from __future__ import annotations

import os
import re
from collections.abc import Mapping, Sequence
from typing import Any


SENSITIVE_KEY_RE = re.compile(
    r"(api[_-]?key|access[_-]?key|secret|token|password|passwd|credential|private[_-]?key|authorization)",
    re.IGNORECASE,
)

NON_SECRET_STATUS_KEYS = {
    "active_credential_env",
    "credential_present",
    "credential_present_redacted",
    "credentials_sent",
    "input_tokens",
    "output_tokens",
    "secrets_printed",
    "secret_values_printed",
    "secret_scan",
    "secret_scan_status",
}

SECRET_VALUE_PATTERNS = [
    re.compile(r"\b(Bearer\s+)[A-Za-z0-9._~+/=-]{16,}", re.IGNORECASE),
    re.compile(r"\b(sk-[A-Za-z0-9_-]{16,})\b"),
    re.compile(r"\b(nvapi-[A-Za-z0-9_-]{16,})\b", re.IGNORECASE),
    re.compile(r"\b(LTAI[A-Za-z0-9]{12,})\b"),
    re.compile(r"\b(AKIA[0-9A-Z]{12,})\b"),
    re.compile(r"(?i)\b(AccessKey\s+Secret\s*\n)\s*([A-Za-z0-9+/=_-]{20,})"),
    re.compile(r"(?i)\b(Password\s*[:=]\s*)([^\s]+)"),
]

PROVIDER_INTERNAL_PATTERNS = [
    (re.compile(r"\b(Function\s+)'([^']{8,})'", re.IGNORECASE), "provider_function_id"),
    (re.compile(r"\b(account\s+)'([^']{8,})'", re.IGNORECASE), "provider_account_id"),
]


def is_sensitive_key(key: str) -> bool:
    if str(key).lower() in NON_SECRET_STATUS_KEYS:
        return False
    return bool(SENSITIVE_KEY_RE.search(str(key)))


def redact_text(text: str, *, env: Mapping[str, str] | None = None) -> str:
    redacted = str(text)
    values = env or os.environ
    for key, value in values.items():
        if not value or len(value) < 8 or not is_sensitive_key(key):
            continue
        redacted = redacted.replace(value, _marker(key, value))
    for pattern in SECRET_VALUE_PATTERNS:
        redacted = pattern.sub(lambda match: _regex_replacement(match), redacted)
    for pattern, label in PROVIDER_INTERNAL_PATTERNS:
        redacted = pattern.sub(lambda match: f"{match.group(1)}'[REDACTED:{label}:len={len(match.group(2))}]'", redacted)
    return redacted


def redact_mapping(value: Any, *, env: Mapping[str, str] | None = None) -> Any:
    if isinstance(value, Mapping):
        output: dict[str, Any] = {}
        for key, item in value.items():
            if is_sensitive_key(str(key)):
                output[str(key)] = _marker(str(key), str(item))
            else:
                output[str(key)] = redact_mapping(item, env=env)
        return output
    if isinstance(value, str):
        return redact_text(value, env=env)
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        return [redact_mapping(item, env=env) for item in value]
    return value


def _marker(key: str, value: str) -> str:
    return f"[REDACTED:{key}:len={len(str(value))}]"


def _regex_replacement(match: re.Match[str]) -> str:
    if match.lastindex and match.lastindex >= 1 and match.group(1).lower().startswith("bearer"):
        return f"{match.group(1)}[REDACTED:bearer_token:len={len(match.group(0)) - len(match.group(1))}]"
    if match.lastindex and match.lastindex >= 2:
        return f"{match.group(1)}[REDACTED:secret_like_value:len={len(match.group(2))}]"
    return f"[REDACTED:secret_like_value:len={len(match.group(0))}]"
