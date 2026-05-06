from __future__ import annotations

from textwrap import dedent

from wabi_sabi.agents.base_agent import AgentInput, AgentResult, BaseAgent
from wabi_sabi.core.tools import discover_project, write_artifact


class FileAgent(BaseAgent):
    def run(self, agent_input: AgentInput) -> AgentResult:
        lowered = agent_input.prompt.lower()
        if "readme" in lowered:
            discovery = discover_project(self.config.workspace, max_files=80)
            text = self._readme_draft(discovery)
            artifact = write_artifact(self.config.output_dir, "README_draft", ".md", text)
            return AgentResult(
                agent_name=self.name,
                ok=True,
                action="readme_draft_generated",
                output="Genere un README borrador en runtime/outputs.",
                artifacts=[str(artifact)],
                evidence=[f"artifact_written={artifact}", "source_tree_not_overwritten"],
                certainty=["El agente de archivos genero un artefacto sin sobrescribir README existente."],
                inference=["El borrador usa marcadores y muestra de archivos del workspace."],
                unknown=["El README final puede requerir copy humano si el producto tiene frontera comercial/legal."],
            )
        artifact = write_artifact(
            self.config.output_dir,
            "file_request_note",
            ".md",
            f"# File Agent Note\n\nSolicitud recibida:\n\n```text\n{agent_input.prompt}\n```\n",
        )
        return AgentResult(
            agent_name=self.name,
            ok=True,
            action="file_request_recorded",
            output="Registre la solicitud de archivo como artefacto local.",
            artifacts=[str(artifact)],
            evidence=[f"artifact_written={artifact}"],
            certainty=["La solicitud fue registrada sin cambios destructivos."],
            inference=["Falta una ruta especifica para operar sobre un archivo real."],
            unknown=["No se selecciono archivo destino."],
        )

    def _readme_draft(self, discovery: dict) -> str:
        markers = "\n".join(f"- `{marker}`" for marker in discovery["markers"][:20]) or "- Sin marcadores detectados"
        return dedent(
            f"""
            # Modulo Local

            ## Descripcion

            Borrador generado por Wabi Sabi a partir del workspace local.

            ## Marcadores detectados

            {markers}

            ## Uso

            ```powershell
            python -m pytest
            ```

            ## Estado

            Este README es un borrador en `runtime/outputs`; no reemplaza
            documentacion canonica ni autoriza publicacion.
            """
        ).lstrip()
