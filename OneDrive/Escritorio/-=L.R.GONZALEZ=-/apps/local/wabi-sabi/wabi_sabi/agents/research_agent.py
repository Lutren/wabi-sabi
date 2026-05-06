from __future__ import annotations

from pathlib import Path

from wabi_sabi.agents.base_agent import AgentInput, AgentResult, BaseAgent
from wabi_sabi.core.tools import SKIP_DIRS, read_text_sample, write_artifact


class ResearchAgent(BaseAgent):
    def run(self, agent_input: AgentInput) -> AgentResult:
        terms = [word for word in agent_input.prompt.lower().split() if len(word) >= 5][:8]
        hits: list[str] = []
        for path in self._candidate_docs():
            text = read_text_sample(path, max_chars=6000).lower()
            if any(term in text for term in terms):
                rel = path.relative_to(self.config.workspace)
                hits.append(str(rel))
            if len(hits) >= 20:
                break
        report = "Local research hits:\n" + "\n".join(f"- {hit}" for hit in hits)
        if not hits:
            report = "Local research hits:\n- No hubo coincidencias claras en docs/README muestreados."
        artifact = write_artifact(self.config.output_dir, "research_local_hits", ".md", report + "\n")
        return AgentResult(
            agent_name=self.name,
            ok=True,
            action="local_document_search",
            output=f"Busqueda local terminada con {len(hits)} coincidencias.",
            artifacts=[str(artifact)],
            evidence=[f"artifact_written={artifact}", f"hits={len(hits)}"],
            certainty=["La investigacion fue local y no uso red externa."],
            inference=["Los hits se basan en terminos simples extraidos del pedido."],
            unknown=["No se hizo lectura exhaustiva de archivos privados, binarios o vendors."],
        )

    def _candidate_docs(self):
        for path in self.config.workspace.rglob("*"):
            if not path.is_file():
                continue
            parts = set(path.parts)
            if parts.intersection(SKIP_DIRS):
                continue
            if path.suffix.lower() in {".md", ".txt"} or path.name.lower() in {"readme", "agents.md"}:
                yield Path(path)
