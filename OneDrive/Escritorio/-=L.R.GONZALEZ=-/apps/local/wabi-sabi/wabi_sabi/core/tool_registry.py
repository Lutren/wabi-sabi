from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolSpec:
    name: str
    purpose: str
    gate: str
    reads: list[str]
    writes: list[str]
    validation: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "purpose": self.purpose,
            "gate": self.gate,
            "reads": list(self.reads),
            "writes": list(self.writes),
            "validation": list(self.validation),
        }


def default_tool_registry() -> list[ToolSpec]:
    return [
        ToolSpec(
            name="rg",
            purpose="buscar texto y archivos dentro del workspace",
            gate="APPROVE",
            reads=["workspace"],
            writes=[],
            validation=["no secret printing", "path scoped"],
        ),
        ToolSpec(
            name="git_worktree_summary",
            purpose="resumir estado git sin stage, commit ni contenido de archivos",
            gate="APPROVE",
            reads=["git metadata", "workspace file names"],
            writes=[],
            validation=["read-only", "no file contents", "no git add"],
        ),
        ToolSpec(
            name="operator_panel",
            purpose="agregar status, worktree, herramientas, task spec y witness en modo solo lectura",
            gate="APPROVE",
            reads=["provider metadata", "git metadata", "task spec json", "witness sqlite"],
            writes=["runtime/logs"],
            validation=["no source writes", "no external actions", "runtime log only"],
        ),
        ToolSpec(
            name="claim_contract",
            purpose="evaluar claims con evidencia y falsadores antes de integrarlos o publicarlos",
            gate="APPROVE",
            reads=["claim contract json"],
            writes=["runtime/logs"],
            validation=["spec inside workspace", "blocked risk flags", "research-only for strong claims"],
        ),
        ToolSpec(
            name="project_scan",
            purpose="detectar stack, gestores, comandos de test y fronteras repo sin modificar fuente",
            gate="APPROVE",
            reads=["workspace file names", "package.json scripts", "git metadata"],
            writes=["runtime/logs"],
            validation=["deny dirs skipped", "no secret content", "no source writes"],
        ),
        ToolSpec(
            name="test_plan",
            purpose="convertir project-scan en comandos de verificacion sugeridos sin ejecutarlos",
            gate="APPROVE",
            reads=["project scan metadata"],
            writes=["runtime/logs"],
            validation=["no auto execution", "no auto apply", "allowlisted command posture"],
        ),
        ToolSpec(
            name="run_safe_tests",
            purpose="ejecutar solo comandos allowlisted de test-plan y registrar evidencia",
            gate="APPROVE",
            reads=["project scan metadata", "test files"],
            writes=["runtime/outputs", "runtime/witness", "test cache"],
            validation=["allowlisted commands only", "auto_apply false", "witness event"],
        ),
        ToolSpec(
            name="curator_assistant",
            purpose="generar inventario seco de orden, candidatos de revision y reglas para agentes/humanos",
            gate="APPROVE",
            reads=["git metadata", "workspace file names", "project scan metadata"],
            writes=["runtime/outputs", "runtime/logs", "runtime/witness"],
            validation=["dry-run only", "no delete", "no move", "no git add", "no file contents"],
        ),
        ToolSpec(
            name="curator_fichas",
            purpose="convertir candidatos del curador en fichas revisables sin limpieza fisica",
            gate="APPROVE",
            reads=["curator assistant report", "workspace docs/intake existence"],
            writes=["runtime/outputs", "runtime/logs", "runtime/witness", "docs/intake when present"],
            validation=["fichas only", "delete_approved_count 0", "no move", "no git add", "no file contents"],
        ),
        ToolSpec(
            name="cerebro_line_audit",
            purpose="leer CEREBRO linea por linea cuando sea texto y generar manifiesto, senales, variantes y grafo maestro",
            gate="APPROVE",
            reads=["-=MEDIOEVO=-/-=LIBROS/-=CEREBRO=-"],
            writes=["runtime/cerebro_master_index"],
            validation=["read-only sources", "binary files stay REVIEW", "no source moves", "no merge without review"],
        ),
        ToolSpec(
            name="cerebro_archive_intake",
            purpose="inventariar ZIP/TAR.GZ de CEREBRO y extraer solo texto no secreto a cuarentena runtime",
            gate="APPROVE",
            reads=["selected archive under workspace"],
            writes=["runtime/cerebro_archive_intake"],
            validation=[
                "source archive untouched",
                "no raw archive extraction",
                "path traversal blocked",
                "secret-like paths blocked",
                "git metadata/cache blocked",
            ],
        ),
        ToolSpec(
            name="cerebro_variant_compare",
            purpose="comparar semanticamente grupos de variantes de CEREBRO sin fusionar ni mover fuentes",
            gate="APPROVE",
            reads=["runtime/cerebro_master_index", "readable CEREBRO text files"],
            writes=["runtime/cerebro_master_index"],
            validation=["unit tests", "json artifacts", "no source writes", "no automatic merge"],
        ),
        ToolSpec(
            name="cerebro_duplicate_migration_plan",
            purpose="crear plan dry-run para archivar duplicados exactos de CEREBRO sin mover fuentes",
            gate="APPROVE",
            reads=["runtime/cerebro_master_index/VARIANT_SEMANTIC_COMPARISON.json", "LINE_AUDIT_MANIFEST.jsonl"],
            writes=["runtime/cerebro_master_index"],
            validation=["unit tests", "dry-run only", "source_mutations 0", "migration log required before execution"],
        ),
        ToolSpec(
            name="cerebro_canon_merge_review",
            purpose="preparar excerpts y decision gates para candidatos de merge canonico sin fusionar fuentes",
            gate="APPROVE",
            reads=["runtime/cerebro_master_index/VARIANT_SEMANTIC_COMPARISON.json", "LINE_SIGNAL_INDEX.jsonl", "readable text files"],
            writes=["runtime/cerebro_master_index"],
            validation=["unit tests", "auto_merge_actions 0", "source_mutations 0", "license boundaries marked"],
        ),
        ToolSpec(
            name="geodia_math_core",
            purpose="nucleo sintetico sin dependencias para Phi_eff, epsilon, regimen, PSI y EML derivado del intake DUAT/GEODIA",
            gate="APPROVE",
            reads=["typed numeric inputs", "GeodiaCell fixtures"],
            writes=[],
            validation=["unit tests", "bounded outputs", "SYNTHETIC_ONLY posture"],
        ),
        ToolSpec(
            name="geodia_synthetic_surface",
            purpose="superficie CLI/JSON local para consumir geodia_math_core sin claims fuertes ni E/S externa",
            gate="APPROVE",
            reads=["deterministic synthetic fixtures"],
            writes=["runtime/logs"],
            validation=["unit tests", "CLI smoke test", "NO_PUBLIC_STRONG_CLAIM gate"],
        ),
        ToolSpec(
            name="geodia_synthetic_falsifier",
            purpose="falsador sintetico y claim contract operacional para la superficie GEODIA local",
            gate="APPROVE",
            reads=["geodia_synthetic_surface payload"],
            writes=["runtime/outputs", "runtime/logs"],
            validation=["claim_contract evaluation", "unit tests", "RESEARCH_ONLY posture"],
        ),
        ToolSpec(
            name="browser_gate",
            purpose="evaluar acciones de navegador y separar inspeccion local/read-only de login, publicacion, pagos o secretos",
            gate="APPROVE",
            reads=["target URL/action metadata"],
            writes=["runtime/logs"],
            validation=["local/read-only approve", "auth/publish/payment review", "secret/destructive block"],
        ),
        ToolSpec(
            name="browser_bridge",
            purpose="crear observaciones de navegador local-first y solicitudes revisables a IAs online sin instalar ni llamar servicios por defecto",
            gate="APPROVE",
            reads=["target URL/action metadata", "backend availability metadata", "sanitized AI consultation prompt"],
            writes=["runtime/outputs/browser_bridge", "runtime/logs"],
            validation=[
                "dry-run is deterministic",
                "real backends require explicit local enable flags",
                "online AI send stays REVIEW unless WABI_ALLOW_BROWSER_SEND=1",
                "provider output remains proposal-only",
            ],
        ),
        ToolSpec(
            name="functional_status",
            purpose="unificar evidencia local de CEREBRO, agentes programadores, navegador gateado y DUAT/GEODIA OS",
            gate="APPROVE",
            reads=["runtime/cerebro_master_index", "wabi_sabi/core", "claudio qa/runtime reports"],
            writes=["runtime/outputs"],
            validation=["claim only existing artifacts", "boot success requires current evidence"],
        ),
        ToolSpec(
            name="multimodal_intake",
            purpose="capturar metadatos locales de camara y microfono para WorldModel/Fusion sin guardar media cruda",
            gate="APPROVE",
            reads=["local camera device", "local microphone device", "BRAIN_OS bridge modules when present"],
            writes=["runtime/outputs", "runtime/witness", "runtime/logs"],
            validation=[
                "raw image/audio excluded",
                "cloud providers not called by default",
                "secrets not printed",
                "WitnessLog event",
            ],
        ),
        ToolSpec(
            name="engine_status",
            purpose="mostrar manifiesto del motor modular clean-room para app, juego y programacion",
            gate="APPROVE",
            reads=["wabi_sabi/engine"],
            writes=["runtime/logs"],
            validation=["read-only manifest", "no external install", "no source writes"],
        ),
        ToolSpec(
            name="engine_intake",
            purpose="convertir una fuente publica o declarada en tarjeta clean-room de patrones, limites y evidencia",
            gate="APPROVE",
            reads=["source name or repository URL"],
            writes=["runtime/logs"],
            validation=["clean-room only", "no vendoring", "no source-code copy", "license review note"],
        ),
        ToolSpec(
            name="engine_plan",
            purpose="crear plan modular local-first para que Wabi-Sabi pueda programar app/juego con Observacionismo",
            gate="APPROVE",
            reads=["user goal", "engine source cards", "engine module manifest"],
            writes=["runtime/logs"],
            validation=["ActionGate posture", "private game/TCG/RPG boundary", "providers optional"],
        ),
        ToolSpec(
            name="engine_task_spec",
            purpose="convertir wabi.engine.plan.v1 en wabi.task_spec.v1 revisable antes de escribir archivos",
            gate="APPROVE",
            reads=["engine plan json inside workspace"],
            writes=["runtime/logs"],
            validation=["markdown target only", "sensitive paths blocked", "task-spec-plan compatible"],
        ),
        ToolSpec(
            name="engine_sandbox",
            purpose="generar project_graph y event_sheet local-only para el Observatorio Sandbox",
            gate="APPROVE",
            reads=["wabi_sabi/engine project runtime"],
            writes=["docs/engine/local_only when --write-docs", "runtime/logs"],
            validation=["LOCAL_ONLY", "publish_allowed false", "project validation fingerprint"],
        ),
        ToolSpec(
            name="engine_project_validate",
            purpose="validar wabi.engine.project_spec.v1 con grafo, escenas, reglas y frontera local",
            gate="APPROVE",
            reads=["engine project spec json inside workspace"],
            writes=["runtime/logs"],
            validation=["graph edges resolved", "event rules complete", "private path markers blocked"],
        ),
        ToolSpec(
            name="engine_simulate",
            purpose="ejecutar de forma deterministica el event_sheet del Observatorio Sandbox sin UI ni canales externos",
            gate="APPROVE",
            reads=["engine project spec json inside workspace"],
            writes=["runtime/logs"],
            validation=["project spec validates", "local events only", "no source writes"],
        ),
        ToolSpec(
            name="task_spec_plan",
            purpose="construir PatchPlan multiarchivo desde un JSON explicito",
            gate="APPROVE",
            reads=["task spec json", "declared content files"],
            writes=["runtime/outputs/patch_plans"],
            validation=["spec inside workspace", "targets declared", "no target guessing"],
        ),
        ToolSpec(
            name="patch_plan",
            purpose="crear un plan de parche textual antes de escribir",
            gate="APPROVE",
            reads=["target file"],
            writes=["runtime/outputs/patch_plans"],
            validation=["target inside workspace", "sensitive paths blocked"],
        ),
        ToolSpec(
            name="safe_execute_patch",
            purpose="aplicar un plan aprobado con snapshot de rollback",
            gate="APPROVE",
            reads=["patch plan", "target file"],
            writes=["target file", "runtime/rollback", "runtime/executions"],
            validation=["py_compile for python targets", "allowlisted test commands", "rollback on failure", "witness event"],
        ),
        ToolSpec(
            name="rollback",
            purpose="restaurar exactamente un snapshot generado por Wabi/Sabi",
            gate="APPROVE",
            reads=["runtime/rollback"],
            writes=["previously touched target files"],
            validation=["workspace boundary", "snapshot exists", "witness event"],
        ),
        ToolSpec(
            name="pytest",
            purpose="ejecutar pruebas locales del paquete",
            gate="APPROVE",
            reads=["workspace"],
            writes=["test cache"],
            validation=["bounded command", "local only"],
        ),
    ]


def tool_registry_payload() -> dict[str, Any]:
    tools = [tool.to_dict() for tool in default_tool_registry()]
    return {
        "schema": "wabi.tool_registry.v1",
        "tools": tools,
        "blocked_patterns": [
            "secret exposure",
            "external publication",
            "large destructive delete",
            "production deploy",
            "billing changes",
        ],
    }
