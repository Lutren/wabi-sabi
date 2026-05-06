from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from ..media.assets import AUDIO_EXTENSIONS, IMAGE_EXTENSIONS, create_placeholder_image


PUBLIC_ASSET_ROOTS = [
    "-=PORTADAS=-",
    "website/radiocinema",
    "website/assets",
    "website/img",
    "MEDIOEVO_BESTSELLER_OUTPUT",
    "radiocinema",
    "output",
]

EXCLUDED_ASSET_ROOTS = [
    "-=Artistas=-",
    "-=CEREBRO=-",
    ".claudio",
    ".chroma_db",
    "_ui_uploads",
]


def build_asset_catalog(
    medioevo_root: Path | None,
    product_root: Path,
    output_path: Path | None = None,
    max_items: int = 500,
) -> dict[str, Any]:
    product_root = Path(product_root).resolve()
    output = output_path or product_root / "runtime" / "content_forge" / "asset_catalog.json"
    roots = resolve_public_roots(medioevo_root)
    items: list[dict[str, Any]] = []
    for root in roots:
        collect_assets_from_root(root, items, medioevo_root, max_items=max_items)
        if len(items) >= max_items:
            break
    if not items:
        placeholder_root = product_root / "assets" / "public_placeholders"
        for index in range(3):
            create_placeholder_image(placeholder_root / f"medioevo_placeholder_{index + 1}.ppm", "MEDIOEVO public placeholder", index=index)
        collect_assets_from_root(placeholder_root, items, medioevo_root=None, max_items=max_items, generated_placeholder=True)

    catalog = {
        "ok": True,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "policy": {
            "public_roots": [str(path) for path in roots],
            "excluded_roots": [str(Path(medioevo_root) / item) for item in EXCLUDED_ASSET_ROOTS] if medioevo_root else [],
            "notes": "Personal/artist/cerebro folders are excluded by default. Explicit assets may still be passed by a human.",
        },
        "counts": {
            "items": len(items),
            "images": sum(1 for item in items if item["type"] == "image"),
            "audio": sum(1 for item in items if item["type"] == "audio"),
        },
        "warnings": ["using_generated_public_placeholders"] if any(item.get("generated_placeholder") for item in items) else [],
        "items": items,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding="utf-8")
    catalog["path"] = str(output)
    return catalog


def resolve_public_roots(medioevo_root: Path | None) -> list[Path]:
    if medioevo_root is None:
        return []
    root = Path(medioevo_root)
    return [(root / value).resolve() for value in PUBLIC_ASSET_ROOTS]


def collect_assets_from_root(
    root: Path,
    items: list[dict[str, Any]],
    medioevo_root: Path | None,
    max_items: int,
    generated_placeholder: bool = False,
) -> None:
    if not root.exists():
        return
    for file_path in root.rglob("*"):
        if len(items) >= max_items:
            break
        if not file_path.is_file():
            continue
        suffix = file_path.suffix.lower()
        if suffix not in IMAGE_EXTENSIONS and suffix not in AUDIO_EXTENSIONS:
            continue
        try:
            stat = file_path.stat()
        except OSError:
            continue
        item = {
            "path": str(file_path.resolve()),
            "relative_to_medioevo": safe_relative(file_path, medioevo_root),
            "type": "image" if suffix in IMAGE_EXTENSIONS else "audio",
            "extension": suffix,
            "size_bytes": stat.st_size,
            "source_root": str(root),
            "public_safe_root": True,
        }
        if generated_placeholder:
            item["generated_placeholder"] = True
        items.append(item)


def safe_relative(file_path: Path, root: Path | None) -> str:
    if root is None:
        return str(file_path)
    try:
        return str(file_path.resolve().relative_to(Path(root).resolve()))
    except ValueError:
        return str(file_path)
