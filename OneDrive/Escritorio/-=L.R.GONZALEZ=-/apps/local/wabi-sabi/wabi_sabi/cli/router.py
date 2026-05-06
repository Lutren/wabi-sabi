from __future__ import annotations

import importlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Type

from wabi_sabi.agents.base_agent import BaseAgent
from wabi_sabi.cli.parser import ParsedCommand
from wabi_sabi.core.config import RuntimeConfig


@dataclass(frozen=True)
class AgentSpec:
    name: str
    description: str
    entrypoint: str
    capabilities: list[str]
    limits: list[str]
    safe_mode: bool


class AgentRegistry:
    def __init__(self, registry_path: Path) -> None:
        self.registry_path = registry_path
        self.raw = json.loads(registry_path.read_text(encoding="utf-8"))
        self.routes: dict[str, str] = self.raw.get("intent_routes", {})
        self.agents: dict[str, AgentSpec] = {}
        for name, payload in self.raw.get("agents", {}).items():
            self.agents[name] = AgentSpec(
                name=name,
                description=payload.get("description", ""),
                entrypoint=payload["entrypoint"],
                capabilities=list(payload.get("capabilities", [])),
                limits=list(payload.get("limits", [])),
                safe_mode=bool(payload.get("safe_mode", True)),
            )

    def select_agent_name(self, parsed: ParsedCommand, explicit: str | None = None) -> str:
        if explicit:
            if explicit not in self.agents:
                raise KeyError(f"unknown_agent: {explicit}")
            return explicit
        return self.routes.get(parsed.intent, self.routes.get("general", "debugger"))

    def build_agent(self, name: str, config: RuntimeConfig) -> BaseAgent:
        spec = self.agents[name]
        module_name, class_name = spec.entrypoint.split(":", 1)
        module = importlib.import_module(module_name)
        cls: Type[BaseAgent] = getattr(module, class_name)
        return cls(spec=spec, config=config)

    def as_dict(self) -> dict:
        return self.raw
