from __future__ import annotations

from pathlib import Path
from typing import Iterable


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".ppm"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}


def existing_paths(values: Iterable[Path], allowed_extensions: set[str]) -> list[Path]:
    paths: list[Path] = []
    for value in values:
        path = Path(value)
        if path.exists() and path.is_file() and path.suffix.lower() in allowed_extensions:
            paths.append(path.resolve())
    return paths


def select_image_assets(medioevo_root: Path | None, requested: list[Path], limit: int = 5) -> list[Path]:
    explicit = existing_paths(requested, IMAGE_EXTENSIONS)
    if explicit:
        return explicit[:limit]
    if medioevo_root is None:
        return []
    roots = [
        medioevo_root / "-=PORTADAS=-",
        medioevo_root / "website" / "radiocinema",
        medioevo_root / "website" / "assets",
        medioevo_root / "website" / "img",
        medioevo_root / "MEDIOEVO_BESTSELLER_OUTPUT",
        medioevo_root / "radiocinema",
        medioevo_root / "output",
    ]
    found: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for item in root.rglob("*"):
            if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS:
                found.append(item.resolve())
                if len(found) >= limit:
                    return found
    return found[:limit]


def select_music_asset(medioevo_root: Path | None, requested: Path | None = None) -> Path | None:
    if requested and requested.exists() and requested.is_file() and requested.suffix.lower() in AUDIO_EXTENSIONS:
        return requested.resolve()
    if medioevo_root is None:
        return None
    roots = [
        medioevo_root / "-=SOUNDTRACK_CONSOLA=-",
        medioevo_root / "website" / "audio",
        medioevo_root / "website" / "radiocinema",
    ]
    for root in roots:
        if not root.exists():
            continue
        for item in root.rglob("*"):
            if item.is_file() and item.suffix.lower() in AUDIO_EXTENSIONS:
                return item.resolve()
    return None


def create_placeholder_image(path: Path, prompt: str = "", index: int = 0, width: int = 720, height: int = 720) -> Path:
    """Create a deterministic PPM placeholder without external libraries."""
    path.parent.mkdir(parents=True, exist_ok=True)
    seed = sum(prompt.encode("utf-8", errors="ignore")) + index * 97
    colors = [
        (21, 42, 62),
        (118, 35, 47),
        (28, 83, 72),
        (104, 78, 32),
        (54, 48, 96),
    ]
    base = colors[seed % len(colors)]
    accent = colors[(seed + 2) % len(colors)]
    with path.open("wb") as handle:
        handle.write(f"P6\n{width} {height}\n255\n".encode("ascii"))
        for y in range(height):
            row = bytearray()
            blend = y / max(height - 1, 1)
            for x in range(width):
                pulse = ((x + y + seed) % 97) / 97.0
                r = int(base[0] * (1 - blend) + accent[0] * blend + pulse * 12) % 256
                g = int(base[1] * (1 - blend) + accent[1] * blend + pulse * 10) % 256
                b = int(base[2] * (1 - blend) + accent[2] * blend + pulse * 8) % 256
                row.extend((r, g, b))
            handle.write(row)
    return path
