from __future__ import annotations

import json
from typing import Any, Iterable


def parse_json_object(text: str) -> tuple[bool, dict[str, Any], str]:
    """Parse a JSON object without hooks or side effects."""
    if not isinstance(text, str):
        return False, {}, "input_must_be_text"
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        return False, {}, f"invalid_json:{exc.msg}"
    if not isinstance(value, dict):
        return False, {}, "json_root_must_be_object"
    return True, value, "ok"


def validate_json_object(text: str, required_keys: Iterable[str] = ()) -> dict[str, Any]:
    """Return a parsed object or raise ValueError with a stable reason."""
    ok, value, reason = parse_json_object(text)
    if not ok:
        raise ValueError(reason)
    missing = [key for key in required_keys if key not in value]
    if missing:
        raise ValueError("missing_required_keys:" + ",".join(sorted(missing)))
    return value
