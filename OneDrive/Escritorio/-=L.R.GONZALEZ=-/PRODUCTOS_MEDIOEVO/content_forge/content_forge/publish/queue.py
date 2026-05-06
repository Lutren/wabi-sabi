from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


def enqueue_publish_request(runtime_root: Path, manifest: dict[str, Any], platforms: list[str]) -> dict[str, Any]:
    runtime_root.mkdir(parents=True, exist_ok=True)
    queue_path = runtime_root / "publish_queue.jsonl"
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "job_id": manifest.get("job_id"),
        "status": "requiere_aprobacion",
        "approval_required": True,
        "auto_publish": False,
        "platforms": platforms or [],
        "final": manifest.get("artifacts", {}).get("final_mp4"),
        "preview": manifest.get("artifacts", {}).get("preview_mp4"),
        "notes": "Prepared only. Official API upload or assisted browser flow requires human approval.",
    }
    with queue_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    entry["queue_path"] = str(queue_path)
    return entry
