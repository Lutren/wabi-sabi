from __future__ import annotations

from wabi_sabi.agents.base_agent import AgentInput, AgentResult, BaseAgent
from wabi_sabi.core.programming import apply_python_patch, code_for_prompt
from wabi_sabi.core.tools import write_artifact


class ProgrammerAgent(BaseAgent):
    def run(self, agent_input: AgentInput) -> AgentResult:
        prompt = agent_input.prompt
        lowered = prompt.lower()
        code, output, inference = code_for_prompt(prompt)

        if agent_input.options.get("apply"):
            target = agent_input.options.get("target")
            if not target:
                return AgentResult(
                    agent_name=self.name,
                    ok=False,
                    action="scoped_code_patch_missing_target",
                    output="Para programar sobre el arbol real se requiere --target con una ruta Python dentro del workspace.",
                    evidence=["apply_requested_without_target"],
                    certainty=["Wabi Sabi no aplico cambios al codigo fuente."],
                    inference=["El modo apply necesita alcance explicito para preservar el gate."],
                    unknown=["Ruta destino no indicada."],
                    error="missing_target",
                )
            try:
                patch = apply_python_patch(
                    workspace=self.config.workspace,
                    runtime_root=self.config.runtime_root,
                    target=target,
                    code=code,
                )
            except Exception as exc:
                return AgentResult(
                    agent_name=self.name,
                    ok=False,
                    action="scoped_code_patch_rejected",
                    output="ActionGate local rechazo o no pudo aplicar el parche acotado.",
                    evidence=[f"error={exc}"],
                    certainty=["No se aplico ningun cambio confirmado al destino solicitado."],
                    inference=["La ruta, extension o contenido no paso las restricciones locales."],
                    unknown=["Reintentar solo con una ruta .py dentro del workspace."],
                    error=str(exc),
                )
            artifacts = [str(patch.diff)]
            for artifact in (patch.plan, patch.rollback, patch.execution):
                if artifact:
                    artifacts.append(str(artifact))
            return AgentResult(
                agent_name=self.name,
                ok=True,
                action="scoped_code_patch_applied" if patch.changed else "scoped_code_patch_noop",
                output=f"{output} El cambio quedo aplicado de forma acotada en {patch.target}.",
                artifacts=artifacts,
                evidence=[
                    f"target={patch.target}",
                    f"before_sha256={patch.before_hash}",
                    f"after_sha256={patch.after_hash}",
                    f"diff_written={patch.diff}",
                    f"plan_written={patch.plan}",
                    f"rollback_snapshot={patch.rollback}",
                    f"execution_record={patch.execution}",
                    f"changed={patch.changed}",
                    patch.verification,
                ],
                certainty=[
                    "La escritura quedo limitada al target indicado.",
                    "Se genero diff y verificacion py_compile.",
                ],
                inference=inference,
                unknown=["No se ejecuto suite de pruebas completa; solo verificacion focal de sintaxis Python y rollback disponible."],
            )

        if "archivo" in lowered and ("linea" in lowered or "lineas" in lowered or "línea" in lowered):
            artifact = write_artifact(self.config.output_dir, "programmer_file_summary", ".py", code)
            return AgentResult(
                agent_name=self.name,
                ok=True,
                action="safe_code_artifact_generated",
                output=output + " El codigo quedo como artefacto seguro, no se modifico codigo fuente del proyecto.",
                artifacts=[str(artifact)],
                evidence=[f"artifact_written={artifact}", "source_tree_not_modified_by_agent"],
                certainty=[
                    "La solicitud fue interpretada como generacion de codigo.",
                    "La escritura se limito a runtime/outputs.",
                ],
                inference=inference,
                unknown=["No se indico una ruta concreta para integrar el codigo en un modulo existente."],
            )
        artifact = write_artifact(self.config.output_dir, "programmer_draft", ".py", code)
        return AgentResult(
            agent_name=self.name,
            ok=True,
            action="safe_code_draft_generated",
            output="Genere un borrador de codigo local en runtime/outputs.",
            artifacts=[str(artifact)],
            evidence=[f"artifact_written={artifact}"],
            certainty=["La tarea fue enrutada al agente programador."],
            inference=inference,
            unknown=["No se detecto archivo destino especifico."],
        )
