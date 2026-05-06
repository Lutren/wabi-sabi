"""Snapshot creation and hashing for GEODIA social sources."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .contracts import SOURCE_SNAPSHOT_SCHEMA
from .sources import validate_source


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_fixture(path: str | Path) -> dict[str, Any]:
    fixture_path = Path(path)
    return json.loads(fixture_path.read_text(encoding="utf-8"))


def create_snapshot_from_fixture(path: str | Path) -> dict[str, Any]:
    fixture_path = Path(path)
    payload = load_fixture(fixture_path)
    source_id = str(payload["source_id"])
    source_url = str(payload["source_url"])
    policy = validate_source(source_id, source_url)
    observations = list(payload.get("observations", []))
    events = list(payload.get("events", []))
    content = {
        "source_id": source_id,
        "source_url": source_url,
        "geography": payload.get("geography", "UNKNOWN"),
        "period": payload.get("period", "UNKNOWN"),
        "observations": observations,
        "events": events,
    }
    content_hash = canonical_sha256(content)
    captured_at = payload.get("captured_at_utc", "1970-01-01T00:00:00Z")
    data_license = payload.get("data_license", "LICENSE_REVIEW_REQUIRED")
    retrieval_mode = payload.get("retrieval_mode", "offline_fixture")
    classification = policy.classification_floor
    return {
        "schema": SOURCE_SNAPSHOT_SCHEMA,
        "source": {
            "source_id": policy.source_id,
            "label": policy.label,
            "source_url": source_url,
            "role": policy.role,
            "classification_floor": policy.classification_floor,
            "license_notice": policy.license_notice,
            "requires_api_key": policy.requires_api_key,
            "special_notice": policy.special_notice,
        },
        "captured_at_utc": captured_at,
        "retrieval_mode": retrieval_mode,
        "data_license": data_license,
        "geography": content["geography"],
        "period": content["period"],
        "content_sha256": content_hash,
        "fixture_sha256": file_sha256(fixture_path),
        "classification": classification,
        "observations": observations,
        "events": events,
        "evidence": {
            "hash_algorithm": "sha256",
            "content_sha256": content_hash,
            "fixture_path": str(fixture_path),
        },
    }
