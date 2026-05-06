from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

from .models import slugify

SAFE_JOB_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,159}$")


def make_job_id(kind: str, prompt: str) -> str:
    stamp = time.strftime("%Y%m%d_%H%M%S")
    suffix = f"{int((time.time() % 1) * 1_000_000):06d}"
    return f"{stamp}_{slugify(kind)}_{slugify(prompt, 'content')}_{suffix}"


class JobStore:
    def __init__(self, jobs_root: Path) -> None:
        self.jobs_root = Path(jobs_root)
        self.jobs_root.mkdir(parents=True, exist_ok=True)

    def create(self, kind: str, request: dict[str, Any]) -> tuple[str, Path, dict[str, Any]]:
        requested_job_id = str(request.get("job_id") or "").strip()
        job_id = normalize_requested_job_id(requested_job_id) if requested_job_id else make_job_id(kind, str(request.get("prompt", "")))
        job_dir = self.job_dir(job_id)
        for folder in ["inputs", "captions", "thumbnails", "logs", "preview", "final", "work"]:
            (job_dir / folder).mkdir(parents=True, exist_ok=True)
        manifest = {
            "ok": False,
            "job_id": job_id,
            "kind": kind,
            "state": "observando",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "request": sanitize_request(request),
            "artifacts": {},
            "warnings": [],
            "approval": {"required": True, "auto_publish": False},
        }
        self.save(job_dir, manifest)
        return job_id, job_dir, manifest

    def save(self, job_dir: Path, manifest: dict[str, Any]) -> None:
        manifest["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        path = Path(job_dir) / "manifest.json"
        path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    def load(self, job_id: str) -> dict[str, Any]:
        path = self.job_dir(job_id) / "manifest.json"
        if not path.exists():
            raise FileNotFoundError(f"job not found: {job_id}")
        return json.loads(path.read_text(encoding="utf-8"))

    def latest(self, limit: int = 20) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for manifest_path in sorted(self.jobs_root.glob("*/manifest.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                rows.append(json.loads(manifest_path.read_text(encoding="utf-8")))
            except Exception:
                continue
            if len(rows) >= limit:
                break
        return rows

    def job_dir(self, job_id: str) -> Path:
        validate_job_id(job_id)
        root = self.jobs_root.resolve()
        target = (root / job_id).resolve()
        if root != target and root not in target.parents:
            raise ValueError(f"job_id escapes jobs root: {job_id}")
        return target


def normalize_requested_job_id(job_id: str) -> str:
    if SAFE_JOB_ID_RE.fullmatch(job_id) and ".." not in Path(job_id).parts:
        return job_id
    slug = slugify(job_id, fallback="job")
    stamp = time.strftime("%Y%m%d_%H%M%S")
    return f"{stamp}_{slug}"


def validate_job_id(job_id: str) -> None:
    value = str(job_id or "").strip()
    if not SAFE_JOB_ID_RE.fullmatch(value) or ".." in Path(value).parts:
        raise ValueError(f"invalid job_id: {job_id}")


def sanitize_request(request: dict[str, Any]) -> dict[str, Any]:
    blocked = {"token", "password", "secret", "api_key", "access_token", "refresh_token"}
    clean: dict[str, Any] = {}
    for key, value in dict(request).items():
        lowered = str(key).lower()
        if any(part in lowered for part in blocked):
            clean[key] = "[redacted]"
        else:
            clean[key] = value
    return clean
