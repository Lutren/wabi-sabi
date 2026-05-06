from __future__ import annotations

from textwrap import dedent

from wabi_sabi.agents.base_agent import AgentInput, AgentResult, BaseAgent
from wabi_sabi.core.tools import write_artifact


class ProgrammerAgent(BaseAgent):
    def run(self, agent_input: AgentInput) -> AgentResult:
        prompt = agent_input.prompt.lower()
        if "archivo" in prompt and ("linea" in prompt or "lineas" in prompt or "línea" in prompt):
            code = self._file_summary_function()
            artifact = write_artifact(self.config.output_dir, "programmer_file_summary", ".py", code)
            output = (
                "Genere una funcion Python local para leer un archivo y resumir sus lineas. "
                "El codigo quedo como artefacto seguro, no se modifico codigo fuente del proyecto."
            )
            return AgentResult(
                agent_name=self.name,
                ok=True,
                action="safe_code_artifact_generated",
                output=output,
                artifacts=[str(artifact)],
                evidence=[f"artifact_written={artifact}", "source_tree_not_modified_by_agent"],
                certainty=[
                    "La solicitud fue interpretada como generacion de codigo.",
                    "La escritura se limito a runtime/outputs.",
                ],
                inference=["El usuario probablemente queria un helper reutilizable para archivos de texto."],
                unknown=["No se indico una ruta concreta para integrar el codigo en un modulo existente."],
            )
        code = self._generic_module_template(agent_input.prompt)
        artifact = write_artifact(self.config.output_dir, "programmer_draft", ".py", code)
        return AgentResult(
            agent_name=self.name,
            ok=True,
            action="safe_code_draft_generated",
            output="Genere un borrador de codigo local en runtime/outputs.",
            artifacts=[str(artifact)],
            evidence=[f"artifact_written={artifact}"],
            certainty=["La tarea fue enrutada al agente programador."],
            inference=["El pedido necesita revision humana o integracion dirigida para tocar codigo existente."],
            unknown=["No se detecto archivo destino especifico."],
        )

    def _file_summary_function(self) -> str:
        return dedent(
            '''
            from __future__ import annotations

            from pathlib import Path


            def summarize_file_lines(path: str | Path, preview_lines: int = 5) -> dict:
                """Read a text file and return a compact line summary."""
                file_path = Path(path)
                text = file_path.read_text(encoding="utf-8", errors="replace")
                lines = text.splitlines()
                return {
                    "path": str(file_path),
                    "line_count": len(lines),
                    "empty_lines": sum(1 for line in lines if not line.strip()),
                    "first_lines": lines[:preview_lines],
                    "last_lines": lines[-preview_lines:] if preview_lines else [],
                }
            '''
        ).lstrip()

    def _generic_module_template(self, prompt: str) -> str:
        escaped = prompt.replace('"""', '\\"\\"\\"')
        return dedent(
            f'''
            """Generated Wabi Sabi code draft.

            Original request:
            {escaped}
            """


            def run() -> str:
                return "TODO: complete this local implementation after selecting a target file."


            if __name__ == "__main__":
                print(run())
            '''
        ).lstrip()
