from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

from wabi_sabi.core.provider_orchestrator import ProviderOrchestrator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="wabi-job-runner")
    parser.add_argument("--job", required=True)
    args = parser.parse_args(argv)
    job_path = Path(args.job)
    job = json.loads(job_path.read_text(encoding="utf-8"))
    _update(job_path, job, status="running")
    try:
        orchestrator = ProviderOrchestrator(workspace=job["workspace"], runtime_root=job["runtime_root"])
        result = orchestrator.ask(
            job["prompt"],
            provider=job.get("provider", "auto"),
            timeout=int(job.get("timeout", 180)),
        ).to_dict()
        job.update(
            {
                "status": "done" if result["ok"] else "failed",
                "updated_at_utc": dt.datetime.now(dt.UTC).isoformat(),
                "output": result.get("output", ""),
                "artifacts": result.get("artifacts", []),
                "error": result.get("error", ""),
                "result": result,
            }
        )
        job_path.write_text(json.dumps(job, indent=2, ensure_ascii=False), encoding="utf-8")
        return 0 if result["ok"] else 2
    except Exception as exc:  # pragma: no cover - defensive background runner
        job.update(
            {
                "status": "failed",
                "updated_at_utc": dt.datetime.now(dt.UTC).isoformat(),
                "error": str(exc),
            }
        )
        job_path.write_text(json.dumps(job, indent=2, ensure_ascii=False), encoding="utf-8")
        return 2


def _update(job_path: Path, job: dict, *, status: str) -> None:
    job["status"] = status
    job["updated_at_utc"] = dt.datetime.now(dt.UTC).isoformat()
    job_path.write_text(json.dumps(job, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
