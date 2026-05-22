# WABI LLM CLOUD WORK MODE 2026-05-19

Fingerprint: WABI_LLM_CLOUD_WORK_MODE_20260519

Estado: LLM_CLOUD_DEFAULT_PROPOSAL_ONLY_READY.

Wabi puede preparar propuestas con un LLM cloud por defecto cuando el operador
activa la bandera de preferencia cloud. La autoridad de ejecucion sigue siendo
local: el proveedor cloud propone, Wabi valida, gatea y solo aplica localmente
si PathAllowlist, rollback, scans y tests pasan.

## Cierre 2026-05-20 - Safe JSON contract

Se agrego `wabi_sabi/core/llm_work_response.py` como normalizador comun para
respuestas UI/API de trabajo con LLM. La salida estable cumple el contrato:

```json
{
  "status": "OK|REVIEW",
  "intent_name": "...",
  "route": "...",
  "proposal": "...",
  "task_spec": {},
  "graphics_plan": {},
  "cloud_provider_called": false,
  "applied_to_sources": false,
  "rollback_snapshot_required": true,
  "next_safe_action": "Review TaskSpec / Preview Apply Local",
  "warnings": ["Proposal-only; Apply Local blocked until explicit local readiness."],
  "tags": ["LLM_proposal", "proposal_only", "apply_local_requires_confirmation"],
  "metadata": {"incremental": true, "budget_control": "CloudBudgetGate"}
}
```

Superficies actualizadas:

- `POST /api/conversation/turn` devuelve el contrato seguro como campos top-level.
- `POST /api/taskspec/llm-proposal` devuelve `status=OK|REVIEW` y conserva el
  estado crudo del LLM en `llm_status`.
- El contrato incluye `patch_candidate` redacted para `Apply Local Preview`.
- El contrato incluye `graphics_plan` top-level en modo DUAT plan-only.
- El contrato incluye `tags` para clasificacion segura por UI/CLI.
- El contrato incluye `metadata` para prioridad, riesgo, categoria, relevancia
  e incrementalidad.
- Cada respuesta normalizada escribe runtime JSON local y WitnessLog redacted.
- `wabi --once "<tarea>" --json` usa el mismo contrato seguro.

Gates preservados:

- `cloud_provider_called=false` sin doble opt-in.
- `applied_to_sources=false` siempre en la propuesta.
- `rollback_snapshot_required=true`.
- `graphics_live=false`.
- `PublicationGate=BLOCK`.
- No se guardan prompts completos en el artefacto normalizado.

Referencia operativa: `docs/WABI_LLM_RESPONSIBLE_USE_2026-05-20.md`.

## Principios activos

- Todo output del LLM cloud es `proposal_only`.
- `cloud_provider_called=true` solo puede ocurrir con doble opt-in y presupuesto disponible.
- Apply local sigue separado del provider.
- Apply local solo opera sobre rutas allowlisted.
- Rollback snapshot, TestRunner, SensitiveValueScan y BoundaryScan son obligatorios para escritura local.
- GraphicsBridge queda `plan-only`: `graphics_live=false`.
- Push, deploy y publicacion siguen bloqueados.

## Configuracion

Preferencia cloud proposal por defecto:

```powershell
$env:WABI_LLM_PROVIDER_CLOUD_DEFAULT='1'
```

Doble opt-in requerido para llamada live:

```powershell
$env:WABI_BUILD_ASSIST_CLOUD='1'
$env:WABI_ALLOW_CLOUD_PROVIDERS='1'
```

Provider/model opcionales:

```powershell
$env:WABI_LLM_PROVIDER='nvidia'
$env:WABI_LLM_MODEL_ALIAS='nano-30b'
```

Defaults actuales:

- provider: `nvidia`
- model alias: `nano-30b`
- presupuesto sesion: `WABI_CLOUD_MAX_CALLS_PER_SESSION`, default `3`
- presupuesto dia: `WABI_CLOUD_MAX_CALLS_PER_DAY`, default `10`

## Flujo CLI/UI

```text
Usuario
ConversationEngine
TaskSpec local
LLM Proposal proposal-only
Review TaskSpec
Gate Preview
Apply Local Preview
Apply Local allowlisted
Rollback snapshot
Tests/scans
WitnessLog/runtime JSON
```

Sin doble opt-in:

- `WABI_LLM_PROVIDER_CLOUD_DEFAULT=1`
- `WABI_BUILD_ASSIST_CLOUD` ausente o distinto de `1`
- `WABI_ALLOW_CLOUD_PROVIDERS` ausente o distinto de `1`
- resultado esperado: `CLOUD_BUDGET_DRY_RUN`
- `cloud_provider_called=false`

Con doble opt-in y presupuesto:

- Wabi prepara prompt redacted.
- Llama al adapter configurado.
- Valida contrato `wabi.cloud_code_proposal.v0_1`.
- Escribe propuesta y TaskSpec en runtime local.
- No aplica cambios.

## Endpoint nuevo

```text
POST /api/taskspec/llm-proposal
```

Entrada minima:

```json
{
  "message": "programa un helper seguro para validar json",
  "intent_name": "code_request",
  "session_id": "ui-session"
}
```

Salida esperada sin doble opt-in:

```json
{
  "status": "OK",
  "llm_status": "CLOUD_BUDGET_DRY_RUN",
  "intent_name": "code_request",
  "route": "llm_proposal",
  "proposal": "LLM proposal is proposal-only/dry-run (CLOUD_BUDGET_DRY_RUN); no provider call was made.",
  "task_spec": {},
  "graphics_plan": {"graphics_live": false, "graphics_plan_ready": false},
  "proposal_only": true,
  "cloud_provider_called": false,
  "applied_to_sources": false,
  "rollback_snapshot_required": true,
  "next_safe_action": "Review TaskSpec / Preview Apply Local",
  "warnings": ["Proposal-only; Apply Local blocked until explicit local readiness."]
}
```

## UI

La UI local muestra:

- Cloud Budget con `LLM default`.
- Wabi Conversation.
- Review TaskSpec.
- Gate Preview.
- LLM Proposal.
- Apply Local Preview.
- Apply Local.

El boton `LLM Proposal` solo pide una propuesta; no aplica archivos.

## Seguridad

- No se guarda el prompt completo dentro del artefacto LLM proposal; se usa un hash redacted.
- No se imprime ningun valor de API key.
- El provider recibe solo un contrato de propuesta y resumen sanitizado.
- La salida cloud se revalida localmente.
- Si el contrato es invalido, queda en REVIEW.
- Si el presupuesto se excede, no se llama provider.

## Evidencia local

- Safe JSON focal Wabi: `55 passed in 47.32s`.
- Safe JSON focal BRAIN_OS: `251 passed in 115.44s`.
- Safe JSON `py_compile`: PASS.
- Safe JSON smoke no-live: `cloud_provider_called=false`, `applied_to_sources=false`,
  `rollback_snapshot_required=true`, `graphics_live=false`, `witness_verified=true`.
- Wabi regression final: `385 passed in 394.59s`.
- BRAIN_OS regression final: `772 passed in 280.24s`.
- Secret scan focal final: PASS, `0` findings.
- Wabi focal: `52 passed in 36.22s`.
- BRAIN_OS focal: `248 passed in 78.22s`.
- Wabi regression: `382 passed in 274.24s`.
- BRAIN_OS regression: `769 passed in 274.79s`.
- `py_compile`: PASS.
- Smoke UI local:
  `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_visual_qa\WABI_LLM_CLOUD_WORK_MODE_20260519\`

## Decision

Wabi queda listo para usar LLM cloud como capa de propuesta por defecto cuando
el operador active `WABI_LLM_PROVIDER_CLOUD_DEFAULT=1`. La llamada live real
continua protegida por doble opt-in, CloudBudgetGate y provider configuration.
