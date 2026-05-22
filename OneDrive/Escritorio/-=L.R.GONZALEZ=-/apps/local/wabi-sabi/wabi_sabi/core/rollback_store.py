from __future__ import annotations

import json
import py_compile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from wabi_sabi.core.bridge import WitnessLog
from wabi_sabi.core.observation import ObservationEnvelope
from wabi_sabi.core.patch_planner import PatchPlan, resolve_workspace_text_target, sha256_text


@dataclass(frozen=True)
class RollbackSnapshot:
    rollback_id: str
    path: Path
    entries: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": "wabi.rollback_snapshot.v1",
            "rollback_id": self.rollback_id,
            "path": str(self.path),
            "entries": self.entries,
        }


class RollbackStore:
    def __init__(self, *, workspace: Path, runtime_root: Path) -> None:
        self.workspace = workspace.resolve()
        self.runtime_root = runtime_root.resolve()
        self.rollback_dir = self.runtime_root / "rollback"
        self.rollback_dir.mkdir(parents=True, exist_ok=True)

    def capture(self, plan: PatchPlan) -> RollbackSnapshot:
        entries: list[dict[str, Any]] = []
        for operation in plan.operations:
            target = resolve_workspace_text_target(self.workspace, operation.relative_path)
            old_text = target.read_text(encoding="utf-8") if target.exists() else ""
            entries.append(
                {
                    "relative_path": operation.relative_path,
                    "existed": target.exists(),
                    "before_hash": sha256_text(old_text),
                    "before_text": old_text,
                }
            )
        path = self.rollback_dir / f"{plan.plan_id}.json"
        snapshot = RollbackSnapshot(rollback_id=plan.plan_id, path=path, entries=entries)
        path.write_text(json.dumps(snapshot.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        return snapshot

    def restore(self, rollback_ref: str | Path) -> dict[str, Any]:
        path = self._resolve_snapshot_path(rollback_ref)
        data = json.loads(path.read_text(encoding="utf-8"))
        restored: list[str] = []
        removed: list[str] = []
        for entry in data.get("entries", []):
            target = resolve_workspace_text_target(self.workspace, entry["relative_path"])
            if entry.get("existed"):
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(entry.get("before_text", ""), encoding="utf-8")
                if target.suffix.lower() == ".py":
                    py_compile.compile(str(target), doraise=True)
                restored.append(entry["relative_path"])
            elif target.exists():
                target.unlink()
                removed.append(entry["relative_path"])
        result = {
            "ok": True,
            "rollback_id": data.get("rollback_id", path.stem),
            "snapshot": str(path),
            "restored": restored,
            "removed": removed,
        }
        result.update(self._append_witness(result))
        return result

    def _resolve_snapshot_path(self, rollback_ref: str | Path) -> Path:
        raw = Path(rollback_ref)
        candidate = raw.resolve() if raw.is_absolute() else (self.rollback_dir / raw).resolve()
        if candidate.suffix.lower() != ".json":
            candidate = candidate.with_suffix(".json")
        root = self.rollback_dir.resolve()
        if candidate != root and root in candidate.parents and candidate.exists():
            return candidate
        raise FileNotFoundError(f"rollback_snapshot_not_found:{rollback_ref}")

    def _append_witness(self, result: dict[str, Any]) -> dict[str, Any]:
        observation = ObservationEnvelope(
            prompt=f"rollback {result['rollback_id']}",
            intent="rollback",
            agent="rollback_store",
            action_gate="APPROVE",
            certainty=["Rollback snapshot was restored inside the workspace boundary."],
            inference=[],
            unknown=[],
            artifacts=[result["snapshot"]],
            evidence=[
                f"rollback_id={result['rollback_id']}",
                f"restored={','.join(result['restored']) or 'none'}",
                f"removed={','.join(result['removed']) or 'none'}",
            ],
        ).finalize()
        witness = WitnessLog(self.runtime_root / "witness" / "wabi_patch_witness.sqlite")
        event_id = witness.append(
            "wabi_patch_rollback",
            {
                "rollback_id": result["rollback_id"],
                "restored": result["restored"],
                "removed": result["removed"],
                "observation_fingerprint": observation.fingerprint,
            },
        )
        witness_ok, witness_reason = witness.verify_chain()
        return {
            "witness_event_id": event_id,
            "witness_verified": witness_ok,
            "witness_verify_reason": witness_reason,
            "witness_db": str(witness.db_path),
            "observation": observation.to_dict(),
        }
