# WABI LLM RESPONSIBLE USE 2026-05-20

Fingerprint: WABI_LLM_RESPONSIBLE_USE_20260520

Estado: `ACTIVE_LOCAL_GATED / PROPOSAL_ONLY`.

Este documento fija el contrato operativo para que WabiSabi use LLM cloud como
asistente real de programacion, debug, planificacion y DUAT graphics sin ceder
autoridad de ejecucion.

## Contexto

- Operador: Tyr.
- Modo: local privado.
- PublicationGate: `BLOCK`.
- CloudGate: `PROPOSAL_ONLY_DOUBLE_OPT_IN`.
- CloudBudgetGate: activo por sesion/dia.
- GraphicsGate: `PLAN_ONLY_READY`, `graphics_live=false`.
- Apply local: solo con preview, PathAllowlist, rollback, tests y scans.

## Reglas de seguridad

1. El LLM cloud propone; Wabi local valida, gatea y ejecuta solo si el operador
   confirma Apply Local.
2. No hay llamada cloud live sin doble opt-in:
   - `WABI_BUILD_ASSIST_CLOUD=1`
   - `WABI_ALLOW_CLOUD_PROVIDERS=1`
3. `WABI_LLM_PROVIDER_CLOUD_DEFAULT=1` habilita preferencia de propuesta cloud,
   pero sin doble opt-in queda en dry-run/proposal-only con
   `cloud_provider_called=false`.
4. CloudBudgetGate debe permitir la llamada antes de invocar provider.
5. Nunca se exponen prompts completos, valores de entorno, credenciales,
   secretos, tokens o rutas privadas innecesarias.
6. DUAT graphics se genera en `plan_mode`; `graphics_live=false`.
7. Push, deploy, publicacion, BrowserBridge live y graphics live quedan fuera de
   este contrato.

## Contrato JSON seguro

Toda superficie UI/API que devuelve propuesta de trabajo debe exponer:

```json
{
  "status": "OK|REVIEW",
  "intent_name": "...",
  "route": "...",
  "proposal": "...",
  "task_spec": {},
  "patch_candidate": {},
  "graphics_plan": {},
  "cloud_provider_called": false,
  "applied_to_sources": false,
  "rollback_snapshot_required": true,
  "next_safe_action": "Review TaskSpec / Preview Apply Local",
  "warnings": [
    "Proposal-only; Apply Local blocked until explicit local readiness."
  ],
  "tags": [
    "LLM_proposal",
    "proposal_only",
    "apply_local_requires_confirmation",
    "rollback_required",
    "publication_blocked"
  ],
  "metadata": {
    "priority": "P1|P2",
    "risk": "low|medium",
    "category": "code|debug|duat_graphics|planning",
    "relevance": "medium|high",
    "incremental": true,
    "fallback_mode": "local_rules_task_spec|cloud_proposal_validated_locally",
    "budget_control": "CloudBudgetGate"
  }
}
```

El estado interno del provider o del presupuesto puede exponerse como
`llm_status`, pero `status` externo se mantiene estable como `OK|REVIEW`.

## Flujo esperado

```text
Usuario CLI/UI
ConversationEngine
WorkIntent
TaskSpec multiarchivo
LLM proposal proposal-only
Safe JSON response
Review TaskSpec
Gate Preview
Apply Local Preview
Apply Local confirmado
Rollback snapshot
Tests/scans
WitnessLog/runtime JSON
```

## CLI

`wabi --once "<tarea>" --json` usa el mismo normalizador seguro que la UI:

- clasifica con `ConversationEngine`;
- adjunta LLM proposal cuando `WABI_LLM_PROVIDER_CLOUD_DEFAULT=1`;
- respeta doble opt-in y CloudBudgetGate;
- devuelve `patch_candidate`, `graphics_plan`, `warnings` y `tags`;
- no ejecuta Apply Local.

Ejemplo:

```powershell
wabi --once "programa un helper seguro para validar JSON y genera tests asociados" --json
```

## Capacidades proposal-only

- Generacion incremental: el contrato incluye `metadata.incremental=true` y una
  estrategia segura por intent.
- Patch candidate diffs: `patch_candidate.diff_preview` resume cambios sin
  aplicar fuentes.
- DUAT graphics incremental: planes graficos se separan en escena/assets y
  conservan `graphics_live=false`.
- Fallback local: si cloud no esta permitido o falla, se devuelve propuesta
  local por reglas y templates.
- Simulacion de Apply: `metadata.apply_simulation.available=true` refiere a
  `Apply Local Preview`, sin modificar archivos.
- Auditoria de assets: intents graficos marcan `asset_audit_required=true`.
- Metadata operativa: prioridad, riesgo, categoria y relevancia quedan en
  `metadata`.
- Manejo de errores: errores quedan `status=REVIEW`, warnings y WitnessLog; no
  hacen apply.

## Comportamiento por escenario

### Sin doble opt-in

- Entrada: `WABI_LLM_PROVIDER_CLOUD_DEFAULT=1`.
- Ausente: `WABI_BUILD_ASSIST_CLOUD=1` o `WABI_ALLOW_CLOUD_PROVIDERS=1`.
- Resultado: propuesta dry-run local.
- `cloud_provider_called=false`.
- No consume presupuesto cloud completado.

### Con doble opt-in y presupuesto disponible

- Wabi prepara prompt redacted.
- Provider devuelve propuesta estructurada.
- `cloud_provider_called=true`.
- La propuesta se valida y normaliza.
- No se aplica ningun cambio automaticamente.

### DUAT graphics

- `intent_name=graphics_scene_request` o `graphics_asset_request`.
- `route=graphics_plan`.
- `graphics_plan.graphics_live=false`.
- La salida es plan grafico, no ejecucion de renderer live.

## Prompt corto para CLI/UI

```text
Genera una propuesta Wabi proposal-only para esta tarea. Devuelve JSON seguro
con status, intent_name, route, proposal, task_spec, patch_candidate,
graphics_plan si aplica, cloud_provider_called, applied_to_sources=false,
rollback_snapshot_required=true, next_safe_action, warnings y tags. No apliques
cambios. No ejecutes comandos. No llames cloud live sin doble opt-in y
CloudBudgetGate. Si aplica DUAT graphics, usa plan_mode y graphics_live=false.
Tarea: <escribe aqui la tarea>
```

## Evidencia

- `wabi_sabi/core/llm_work_response.py` normaliza el contrato.
- `POST /api/conversation/turn` devuelve el contrato top-level.
- `POST /api/taskspec/llm-proposal` devuelve el contrato top-level.
- Runtime JSON: `~/.medioevo/wabi/runtime/outputs/llm_work_response/`.
- WitnessLog: `~/.medioevo/wabi/runtime/witness/wabi_patch_witness.sqlite`.

## Decision

WabiSabi puede usar LLM cloud como capa productiva de propuesta solo bajo doble
opt-in y CloudBudgetGate. La autoridad de escritura queda en Apply Local
sandboxed y confirmado por el operador.
