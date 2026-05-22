from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any


class LocalMemory:
    def __init__(self, runtime_root: Path) -> None:
        self.runtime_root = runtime_root
        self.log_dir = runtime_root / "logs"
        self.memory_dir = runtime_root / "memory"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

    @property
    def event_log(self) -> Path:
        return self.log_dir / "wabi_events.jsonl"

    @property
    def session_log(self) -> Path:
        return self.memory_dir / "session_memory.jsonl"

    def append_event(self, event: dict[str, Any]) -> Path:
        payload = dict(event)
        payload.setdefault("logged_at_utc", dt.datetime.now(dt.UTC).isoformat())
        line = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        with self.event_log.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
        return self.event_log

    def append_memory(self, item: dict[str, Any]) -> Path:
        payload = dict(item)
        payload.setdefault("stored_at_utc", dt.datetime.now(dt.UTC).isoformat())
        with self.session_log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
        return self.session_log

    def tail_memory(self, limit: int = 12) -> list[dict[str, Any]]:
        if not self.session_log.exists():
            return []
        lines = self.session_log.read_text(encoding="utf-8", errors="replace").splitlines()
        items: list[dict[str, Any]] = []
        for line in lines[-limit:]:
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return items

    def conversation_summary(self, limit: int = 6) -> str:
        items = [
            item
            for item in self.tail_memory(limit=limit)
            if item.get("channel") in {"wabi_auto_router", "wabi_auto_conversation"}
        ]
        if not items:
            return ""
        parts: list[str] = []
        for item in items[-limit:]:
            prompt = _excerpt(str(item.get("prompt") or ""), 90)
            route = str(item.get("route") or item.get("agent") or "local")
            output = _excerpt(str(item.get("output") or ""), 140)
            if prompt:
                parts.append(f"{route}: {prompt}" + (f" -> {output}" if output else ""))
        return " | ".join(parts)

    def tail_events(self, limit: int = 20) -> list[dict[str, Any]]:
        if not self.event_log.exists():
            return []
        lines = self.event_log.read_text(encoding="utf-8", errors="replace").splitlines()
        events: list[dict[str, Any]] = []
        for line in lines[-limit:]:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return events


def _excerpt(text: str, limit: int) -> str:
    clean = " ".join(str(text or "").split())
    if len(clean) <= limit:
        return clean
    return clean[: max(0, limit - 3)] + "..."
