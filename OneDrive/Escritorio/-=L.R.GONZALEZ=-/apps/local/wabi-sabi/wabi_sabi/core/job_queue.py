from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class JobStore:
    runtime_root: Path

    @property
    def jobs_dir(self) -> Path:
        path = self.runtime_root / "jobs"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def job_path(self, job_id: str) -> Path:
        return self.jobs_dir / f"{job_id}.json"

    def new_job_id(self) -> str:
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{stamp}-{uuid.uuid4().hex[:8]}"

    def write(self, payload: dict[str, Any]) -> Path:
        path = self.job_path(payload["job_id"])
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return path

    def read(self, job_id: str) -> dict[str, Any]:
        return json.loads(self.job_path(job_id).read_text(encoding="utf-8"))

    def list_recent(self, limit: int = 10) -> list[dict[str, Any]]:
        jobs: list[dict[str, Any]] = []
        for path in sorted(self.jobs_dir.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True)[:limit]:
            try:
                jobs.append(json.loads(path.read_text(encoding="utf-8")))
            except json.JSONDecodeError:
                continue
        return jobs

    def latest_id(self) -> str | None:
        jobs = self.list_recent(limit=1)
        return str(jobs[0]["job_id"]) if jobs else None


def submit_codex_job(
    *,
    prompt: str,
    workspace: Path,
    runtime_root: Path,
    provider: str = "auto",
    timeout: int = 35,
) -> dict[str, Any]:
    return submit_orchestrator_job(
        prompt=prompt,
        workspace=workspace,
        runtime_root=runtime_root,
        provider=provider,
        timeout=timeout,
    )


def submit_orchestrator_job(
    *,
    prompt: str,
    workspace: Path,
    runtime_root: Path,
    provider: str = "auto",
    timeout: int = 35,
) -> dict[str, Any]:
    store = JobStore(runtime_root)
    job_id = store.new_job_id()
    now = dt.datetime.now(dt.UTC).isoformat()
    payload = {
        "schema": "wabi_background_job.v1",
        "job_id": job_id,
        "kind": "orchestrator",
        "status": "queued",
        "created_at_utc": now,
        "updated_at_utc": now,
        "workspace": str(workspace),
        "runtime_root": str(runtime_root),
        "provider": provider,
        "timeout": timeout,
        "prompt": prompt,
        "output": "",
        "artifacts": [],
        "error": "",
    }
    job_path = store.write(payload)
    stdout_path = runtime_root / "jobs" / f"{job_id}.stdout.log"
    stderr_path = runtime_root / "jobs" / f"{job_id}.stderr.log"
    command = [
        sys.executable,
        "-m",
        "wabi_sabi.cli.job_runner",
        "--job",
        str(job_path),
    ]
    env = os.environ.copy()
    package_root = Path(__file__).resolve().parents[1].parent
    env["PYTHONPATH"] = str(package_root) + os.pathsep + env.get("PYTHONPATH", "")
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
        proc = subprocess.Popen(
            command,
            cwd=str(package_root),
            env=env,
            stdout=stdout,
            stderr=stderr,
            stdin=subprocess.DEVNULL,
            creationflags=creationflags,
        )
    payload["status"] = "running"
    payload["updated_at_utc"] = dt.datetime.now(dt.UTC).isoformat()
    payload["pid"] = proc.pid
    payload["job_file"] = str(job_path)
    payload["stdout_log"] = str(stdout_path)
    payload["stderr_log"] = str(stderr_path)
    store.write(payload)
    return payload


def summarize_jobs(jobs: list[dict[str, Any]]) -> str:
    if not jobs:
        return "No hay jobs registrados."
    lines = ["JOBS:"]
    for job in jobs:
        output = str(job.get("output", "")).replace("\n", " ").strip()
        if len(output) > 80:
            output = output[:77] + "..."
        lines.append(
            f"- {job.get('job_id')} [{job.get('status')}] {job.get('kind')} :: {output or job.get('prompt', '')[:80]}"
        )
    return "\n".join(lines)


def format_job_result(job: dict[str, Any]) -> str:
    lines = [
        f"JOB {job.get('job_id')} [{job.get('status')}]",
        f"Tipo: {job.get('kind')}  Proveedor: {job.get('provider')}",
        "",
        "RESPUESTA:",
        str(job.get("output") or "- Sin salida todavia."),
    ]
    if job.get("artifacts"):
        lines.append("")
        lines.append("ARTEFACTOS:")
        lines.extend(f"- {artifact}" for artifact in job["artifacts"])
    if job.get("error"):
        lines.append("")
        lines.append(f"ERROR: {job['error']}")
    return "\n".join(lines)
