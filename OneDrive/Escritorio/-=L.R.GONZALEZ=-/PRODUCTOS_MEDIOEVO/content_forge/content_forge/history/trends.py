from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


HISTORY_FILENAMES = [
    "video_schedule.json",
    "youtube_uploads.json",
    "youtube_metadata.json",
    "instagram_log.json",
    "content_calendar.json",
    "campaign_history.json",
]


def load_historical_context(medioevo_root: Path | None, claudio_root: Path | None) -> dict[str, Any]:
    roots = [root for root in [claudio_root, medioevo_root] if root is not None and root.exists()]
    files: list[Path] = []
    for root in roots:
        for name in HISTORY_FILENAMES:
            candidate = root / name
            if candidate.exists():
                files.append(candidate)
    rows: list[Any] = []
    loaded: list[str] = []
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
            rows.append(data)
            loaded.append(str(path))
        except Exception:
            continue
    platforms = Counter()
    statuses = Counter()
    for data in rows:
        for item in flatten_items(data):
            if isinstance(item, dict):
                platform = str(item.get("platform") or item.get("channel") or item.get("site") or "").strip().lower()
                status = str(item.get("status") or item.get("state") or "").strip().lower()
                if platform:
                    platforms[platform] += 1
                if status:
                    statuses[status] += 1
    return {
        "source": "historico_propio",
        "files_loaded": loaded,
        "signals": {
            "platform_counts": dict(platforms.most_common(8)),
            "status_counts": dict(statuses.most_common(8)),
            "documents": len(rows),
        },
        "external_trends": "manual_or_phase_2",
    }


def flatten_items(data: Any) -> list[Any]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        rows: list[Any] = []
        for key in ["items", "videos", "uploads", "posts", "schedule", "campaigns"]:
            value = data.get(key)
            if isinstance(value, list):
                rows.extend(value)
        if not rows:
            rows.extend(data.values())
        return rows
    return []
