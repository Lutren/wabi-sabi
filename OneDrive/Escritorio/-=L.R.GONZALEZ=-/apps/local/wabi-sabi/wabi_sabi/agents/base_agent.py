from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from wabi_sabi.cli.parser import ParsedCommand
from wabi_sabi.core.config import RuntimeConfig

if TYPE_CHECKING:
    from wabi_sabi.cli.router import AgentSpec


@dataclass(frozen=True)
class AgentInput:
    prompt: str
    parsed: ParsedCommand
    options: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    agent_name: str
    ok: bool
    action: str
    output: str
    artifacts: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    certainty: list[str] = field(default_factory=list)
    inference: list[str] = field(default_factory=list)
    unknown: list[str] = field(default_factory=list)
    error: str = ""


class BaseAgent:
    def __init__(self, spec: "AgentSpec", config: RuntimeConfig) -> None:
        self.spec = spec
        self.config = config

    @property
    def name(self) -> str:
        return self.spec.name

    def run(self, agent_input: AgentInput) -> AgentResult:
        raise NotImplementedError
