from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .ffmpeg import run_ffmpeg


def analyze_video_frame(video: Path, frame_path: Path, log_path: Path) -> dict[str, Any]:
    frame_path.parent.mkdir(parents=True, exist_ok=True)
    result = run_ffmpeg(
        ["-y", "-i", str(video), "-frames:v", "1", "-vf", "scale=64:64", str(frame_path)],
        log_path=log_path,
        timeout=120,
    )
    if result.returncode != 0 or not frame_path.exists():
        return {"ok": False, "error": "frame_extract_failed", "frame_path": str(frame_path)}
    stats = analyze_ppm(frame_path)
    stats["frame_path"] = str(frame_path)
    stats["ok"] = bool(stats.get("nonblank") and stats.get("contrast_ok"))
    return stats


def analyze_ppm(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    offset, width, height, max_value = parse_ppm_header(data)
    pixels = data[offset:]
    if not pixels:
        return {"nonblank": False, "contrast_ok": False, "width": width, "height": height}
    sample = pixels[:: max(3, len(pixels) // 4096)]
    if len(sample) < 12:
        sample = pixels
    values = list(sample)
    min_value = min(values)
    max_seen = max(values)
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    unique = len(set(values))
    return {
        "nonblank": unique > 8 and max_seen - min_value > 8,
        "contrast_ok": variance > 16.0,
        "width": width,
        "height": height,
        "max_value": max_value,
        "sample_unique_values": unique,
        "sample_min": min_value,
        "sample_max": max_seen,
        "sample_variance": round(variance, 3),
    }


def parse_ppm_header(data: bytes) -> tuple[int, int, int, int]:
    tokens: list[bytes] = []
    token = bytearray()
    index = 0
    while index < len(data) and len(tokens) < 4:
        byte = data[index]
        if byte == ord("#"):
            while index < len(data) and data[index] not in (10, 13):
                index += 1
        elif byte in b" \t\r\n":
            if token:
                tokens.append(bytes(token))
                token.clear()
        else:
            token.append(byte)
        index += 1
    if token and len(tokens) < 4:
        tokens.append(bytes(token))
    if len(tokens) < 4 or tokens[0] != b"P6":
        raise ValueError("unsupported ppm frame")
    while index < len(data) and data[index] in b" \t\r\n":
        index += 1
    return index, int(tokens[1]), int(tokens[2]), int(tokens[3])


def write_visual_qa(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
