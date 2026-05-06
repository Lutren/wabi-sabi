from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = PACKAGE_ROOT.parent
DEFAULT_RUNTIME = APP_ROOT / "runtime"
DEFAULT_REGISTRY = PACKAGE_ROOT / "config" / "agents.json"


@dataclass(frozen=True)
class RuntimeConfig:
    workspace: Path
    runtime_root: Path
    registry_path: Path
    safe_mode: bool = True

    @property
    def output_dir(self) -> Path:
        return self.runtime_root / "outputs"

    @property
    def log_dir(self) -> Path:
        return self.runtime_root / "logs"

    @property
    def memory_dir(self) -> Path:
        return self.runtime_root / "memory"

    def ensure_dirs(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)


def build_config(
    workspace: str | Path | None = None,
    runtime_root: str | Path | None = None,
    registry_path: str | Path | None = None,
    safe_mode: bool = True,
) -> RuntimeConfig:
    ws = Path(workspace or os.environ.get("WABI_WORKSPACE") or Path.cwd()).resolve()
    runtime = Path(runtime_root or os.environ.get("WABI_RUNTIME") or DEFAULT_RUNTIME).resolve()
    registry = Path(registry_path or os.environ.get("WABI_AGENT_REGISTRY") or DEFAULT_REGISTRY).resolve()
    config = RuntimeConfig(workspace=ws, runtime_root=runtime, registry_path=registry, safe_mode=safe_mode)
    config.ensure_dirs()
    return config
