from __future__ import annotations

import json
import statistics
import time
from pathlib import Path
from typing import Any

from .observacionismo_state import DEFAULT_THRESHOLDS_SECONDS


class StageMetricsStore:
    def __init__(self, metrics_path: Path) -> None:
        self.metrics_path = Path(metrics_path)

    def learned_thresholds(self, minimums: dict[str, float] | None = None) -> dict[str, float]:
        minimums = minimums or DEFAULT_THRESHOLDS_SECONDS
        durations: dict[str, list[float]] = {}
        for row in self._read_recent_rows(limit=500):
            state = str(row.get("state") or "")
            duration = float(row.get("duration_seconds") or 0.0)
            if state and duration > 0:
                durations.setdefault(state, []).append(duration)
        thresholds = dict(minimums)
        for state, values in durations.items():
            if len(values) < 3:
                continue
            learned = percentile(values, 0.95) * 2.5
            thresholds[state] = max(float(minimums.get(state, 0.0)), min(1800.0, learned))
        return thresholds

    def record_job(self, job_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
        events_path = Path(job_dir) / "events.jsonl"
        if not events_path.exists():
            return {"ok": False, "error": "events_missing"}
        events = []
        for line in events_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        rows = []
        for current, nxt in zip(events, events[1:]):
            state = str(current.get("state") or "")
            duration = max(0.0, float(nxt.get("ts", 0.0)) - float(current.get("ts", 0.0)))
            if state and duration > 0:
                rows.append(
                    {
                        "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                        "job_id": manifest.get("job_id"),
                        "kind": manifest.get("kind"),
                        "state": state,
                        "duration_seconds": round(duration, 3),
                        "terminal_state": manifest.get("state"),
                        "ok": bool(manifest.get("ok")),
                    }
                )
        if rows:
            self.metrics_path.parent.mkdir(parents=True, exist_ok=True)
            with self.metrics_path.open("a", encoding="utf-8") as handle:
                for row in rows:
                    handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        return {
            "ok": True,
            "path": str(self.metrics_path),
            "rows_recorded": len(rows),
            "learned_thresholds": self.learned_thresholds(),
        }

    def _read_recent_rows(self, limit: int) -> list[dict[str, Any]]:
        if not self.metrics_path.exists():
            return []
        rows = []
        for line in self.metrics_path.read_text(encoding="utf-8", errors="ignore").splitlines()[-limit:]:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return rows


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    index = (len(ordered) - 1) * fraction
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    weight = index - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight
