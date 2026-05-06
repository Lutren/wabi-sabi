from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CaptionCue:
    start: float
    end: float
    text: str


def split_caption_text(text: str) -> list[str]:
    value = " ".join(str(text or "").split())
    if not value:
        return ["MEDIOEVO"]
    pieces = re.split(r"(?<=[.!?])\s+", value)
    lines: list[str] = []
    for piece in pieces:
        words = piece.split()
        current: list[str] = []
        for word in words:
            current.append(word)
            if len(" ".join(current)) >= 58:
                lines.append(" ".join(current))
                current = []
        if current:
            lines.append(" ".join(current))
    return lines[:12] or [value[:80]]


def cues_from_text(text: str, duration: float) -> list[CaptionCue]:
    lines = split_caption_text(text)
    total = max(float(duration), 1.0)
    step = total / max(len(lines), 1)
    cues = []
    for index, line in enumerate(lines):
        start = round(index * step, 3)
        end = round(min(total, (index + 1) * step), 3)
        if end <= start:
            end = start + 1.0
        cues.append(CaptionCue(start=start, end=end, text=line))
    return cues


def write_srt(cues: list[CaptionCue], path: Path) -> Path:
    lines: list[str] = []
    for index, cue in enumerate(cues, start=1):
        lines.append(str(index))
        lines.append(f"{format_srt_time(cue.start)} --> {format_srt_time(cue.end)}")
        lines.append(cue.text)
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_vtt(cues: list[CaptionCue], path: Path) -> Path:
    lines = ["WEBVTT", ""]
    for cue in cues:
        lines.append(f"{format_vtt_time(cue.start)} --> {format_vtt_time(cue.end)}")
        lines.append(cue.text)
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def format_srt_time(seconds: float) -> str:
    whole = int(seconds)
    millis = int(round((seconds - whole) * 1000))
    hours = whole // 3600
    minutes = (whole % 3600) // 60
    secs = whole % 60
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def format_vtt_time(seconds: float) -> str:
    return format_srt_time(seconds).replace(",", ".")
