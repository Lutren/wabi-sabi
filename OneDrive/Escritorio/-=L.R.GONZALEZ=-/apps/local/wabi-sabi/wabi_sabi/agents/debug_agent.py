from __future__ import annotations

import json

from wabi_sabi.agents.base_agent import AgentInput, AgentResult, BaseAgent
from wabi_sabi.core.tools import discover_project, safe_command_snapshot, write_artifact


class DebugAgent(BaseAgent):
    def run(self, agent_input: AgentInput) -> AgentResult:
        discovery = discover_project(self.config.workspace)
        snapshot = safe_command_snapshot()
        test_commands = self._detect_test_commands(discovery["markers"])
        report = {
            "workspace": str(self.config.workspace),
            "snapshot": snapshot,
            "markers": discovery["markers"],
            "file_sample_count": discovery["file_sample_count"],
            "suggested_test_commands": test_commands,
            "failure_classification": self._classify(agent_input.prompt),
        }
        artifact = write_artifact(
            self.config.output_dir,
            "debug_diagnostic",
            ".json",
            json.dumps(report, indent=2, ensure_ascii=False),
        )
        return AgentResult(
            agent_name=self.name,
            ok=True,
            action="local_diagnostic_snapshot",
            output=(
                f"Diagnostico local generado. Marcadores detectados: "
                f"{', '.join(discovery['markers'][:8]) or 'sin marcadores principales'}."
            ),
            artifacts=[str(artifact)],
            evidence=[f"artifact_written={artifact}", f"workspace={self.config.workspace}"],
            certainty=[
                "El CLI arranco y pudo inspeccionar el workspace local.",
                "El diagnostico no ejecuto acciones externas ni destructivas.",
            ],
            inference=["Los comandos sugeridos se infieren por marcadores de stack."],
            unknown=["No se ejecutaron suites largas desde el agente para evitar recorridos amplios no solicitados."],
        )

    def _detect_test_commands(self, markers: list[str]) -> list[str]:
        commands: list[str] = []
        marker_names = {marker.replace("\\", "/").split("/")[-1] for marker in markers}
        if "pyproject.toml" in marker_names or "setup.py" in marker_names:
            commands.append("python -m pytest")
        if "package.json" in marker_names:
            commands.append("npm test")
        if "Cargo.toml" in marker_names:
            commands.append("cargo test")
        if "Makefile" in marker_names:
            commands.append("make test")
        return commands or ["no_test_command_detected"]

    def _classify(self, prompt: str) -> str:
        lowered = prompt.lower()
        if "import" in lowered:
            return "import_roto"
        if "depend" in lowered or "modulo" in lowered or "module" in lowered:
            return "dependencia_o_modulo_faltante"
        if "test" in lowered:
            return "test_o_configuracion_incompleta"
        if "permiso" in lowered or "permission" in lowered:
            return "error_de_permisos"
        return "diagnostico_general"
