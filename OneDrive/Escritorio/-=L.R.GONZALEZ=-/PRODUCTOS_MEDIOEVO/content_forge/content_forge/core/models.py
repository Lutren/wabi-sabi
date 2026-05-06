from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PRESETS: dict[str, dict[str, Any]] = {
    "tiktok": {"width": 1080, "height": 1920, "fps": 30, "label": "TikTok vertical"},
    "shorts": {"width": 1080, "height": 1920, "fps": 30, "label": "YouTube Shorts"},
    "reel": {"width": 1080, "height": 1920, "fps": 30, "label": "Instagram Reel"},
    "youtube": {"width": 1920, "height": 1080, "fps": 30, "label": "YouTube landscape"},
}


def normalize_preset(value: str | None) -> str:
    preset = str(value or "shorts").strip().lower()
    if preset not in PRESETS:
        raise ValueError(f"Unsupported preset '{preset}'. Use one of: {', '.join(sorted(PRESETS))}")
    return preset


def slugify(text: str, fallback: str = "job") -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", text or "").strip("-").lower()
    return (slug or fallback)[:48]


def as_path_list(values: Any) -> list[Path]:
    if not values:
        return []
    if isinstance(values, (str, Path)):
        values = [values]
    return [Path(str(value)).expanduser() for value in values if str(value).strip()]


@dataclass(frozen=True)
class ForgePaths:
    product_root: Path
    runtime_root: Path
    jobs_root: Path
    medioevo_root: Path | None
    claudio_root: Path | None
