from __future__ import annotations

import pytest

from wabi_sabi.core.json_safety import parse_json_object, validate_json_object


def test_parse_json_object_accepts_object() -> None:
    ok, value, reason = parse_json_object('{"status":"ok","count":1}')
    assert ok is True
    assert value == {"status": "ok", "count": 1}
    assert reason == "ok"


def test_parse_json_object_rejects_invalid_json() -> None:
    ok, value, reason = parse_json_object("{")
    assert ok is False
    assert value == {}
    assert reason.startswith("invalid_json:")


def test_parse_json_object_rejects_non_object_root() -> None:
    ok, value, reason = parse_json_object("[1, 2, 3]")
    assert ok is False
    assert value == {}
    assert reason == "json_root_must_be_object"


def test_validate_json_object_requires_keys() -> None:
    with pytest.raises(ValueError, match="missing_required_keys:mode"):
        validate_json_object('{"status":"ok"}', required_keys=["mode", "status"])


def test_validate_json_object_returns_object() -> None:
    assert validate_json_object('{"status":"ok"}', required_keys=["status"]) == {"status": "ok"}
