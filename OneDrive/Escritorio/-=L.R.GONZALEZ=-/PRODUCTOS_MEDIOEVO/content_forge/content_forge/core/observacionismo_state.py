from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class JobState(str, Enum):
    OBSERVANDO = "observando"
    PLANIFICANDO = "planificando"
    RENDERIZANDO = "renderizando"
    QA = "qa"
    ESPERANDO = "esperando"
    ATASCADO = "atascado"
    REQUIERE_APROBACION = "requiere_aprobacion"
    LISTO = "listo"
    FALLIDO = "fallido"


DEFAULT_THRESHOLDS_SECONDS = {
    JobState.OBSERVANDO.value: 20.0,
    JobState.PLANIFICANDO.value: 20.0,
    JobState.RENDERIZANDO.value: 240.0,
    JobState.QA.value: 60.0,
    JobState.ESPERANDO.value: 300.0,
}


@dataclass
class StageEvent:
    state: str
    message: str
    ts: float = field(default_factory=time.time)
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ts": self.ts,
            "state": self.state,
            "message": self.message,
            "data": self.data,
        }


class ObservacionismoMonitor:
    def __init__(self, job_dir: Path, thresholds: dict[str, float] | None = None) -> None:
        self.job_dir = Path(job_dir)
        self.events_path = self.job_dir / "events.jsonl"
        self.thresholds = dict(DEFAULT_THRESHOLDS_SECONDS)
        if thresholds:
            self.thresholds.update({str(k): float(v) for k, v in thresholds.items()})
        self.state = JobState.OBSERVANDO.value
        self.stage_started = time.time()
        self.last_progress = self.stage_started
        self.job_dir.mkdir(parents=True, exist_ok=True)

    def transition(self, state: JobState | str, message: str, **data: Any) -> StageEvent:
        value = state.value if isinstance(state, JobState) else str(state)
        self.state = value
        self.stage_started = time.time()
        self.last_progress = self.stage_started
        return self.record(message, state=value, **data)

    def progress(self, message: str, **data: Any) -> StageEvent:
        self.last_progress = time.time()
        return self.record(message, **data)

    def record(self, message: str, state: str | None = None, **data: Any) -> StageEvent:
        event = StageEvent(state=state or self.state, message=message, data=data)
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
        return event

    def detect_stall(self, now: float | None = None) -> dict[str, Any]:
        current = now if now is not None else time.time()
        threshold = float(self.thresholds.get(self.state, 120.0))
        stage_age = current - self.stage_started
        idle_age = current - self.last_progress
        stalled = stage_age > threshold or idle_age > max(30.0, threshold / 2)
        return {
            "stalled": stalled,
            "state": self.state,
            "stage_age_seconds": round(stage_age, 3),
            "idle_age_seconds": round(idle_age, 3),
            "threshold_seconds": threshold,
        }

    def mark_stalled_if_needed(self) -> dict[str, Any]:
        status = self.detect_stall()
        if status["stalled"] and self.state != JobState.ATASCADO.value:
            self.transition(JobState.ATASCADO, "stage exceeded observacionista threshold", status=status)
        return status
