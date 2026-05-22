# WABI UI Review TaskSpec v0.1 - 2026-05-19

Fingerprint: WABI_UI_TASKSPEC_REVIEW_20260519

## Estado

- ActionGate: APPROVE_LOCAL
- CloudGate: PROPOSAL_ONLY_DOUBLE_OPT_IN
- CloudBudgetGate: CLOUD_BUDGET_DRY_RUN
- UIGate: LOCAL_UI_TASKSPEC_REVIEW_READY
- ConversationGate: API_CONNECTED_TO_CONVERSATION_ENGINE
- TaskSpecGate: REVIEW_ONLY_APPLY_BLOCKED
- GraphicsGate: PLAN_ONLY_READY / graphics_live=false
- PublicationGate: BLOCK

## Implementacion

La UI local de Wabi ahora muestra un panel `Review TaskSpec` despues de turnos que generan trabajo:

- `code_request`
- `debug_request`
- `graphics_scene_request`
- `graphics_asset_request`
- `build_assist_request`
- `plan_request`
- `file_task_request`
- `handoff_request`

La UI solo renderiza el TaskSpec normalizado por backend. No clasifica ni reconstruye TaskSpec en JavaScript.

## Backend

Archivo nuevo:

`wabi_sabi/core/taskspec_review.py`

Contrato:

- `normalize_taskspec_for_review(task_spec) -> dict`
- `redact_taskspec(task_spec) -> dict`
- `save_taskspec_draft(task_spec) -> dict`
- `block_apply_attempt(task_spec) -> dict`

Endpoints locales:

- `GET /api/taskspec/latest`
- `POST /api/taskspec/save-draft`
- `POST /api/taskspec/apply`

`POST /api/taskspec/apply` siempre bloquea en v0.1:

```json
{
  "status": "BLOCKED",
  "reason": "APPLY_BLOCKED_REVIEW_ONLY_V0_1",
  "applied_to_sources": false
}
```

## UI

Archivo modificado:

`C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\apps\local\wabi_ui\index.html`

Campos visibles:

- task_id / fingerprint
- intent_name
- route
- action_gate
- proposal_only
- needs_cloud / needs_graphics / needs_file_write
- applied_to_sources
- cloud_provider_called
- graphics_live
- summary
- plan_steps
- risks
- assumptions
- suggested_tests
- affected_paths
- next_action
- gate_status

Acciones:

- `Review`: expande/contrae detalles.
- `Copy TaskSpec`: copia version redacted.
- `Save Draft`: guarda draft redacted local.
- `Apply bloqueado`: llama endpoint bloqueado y no modifica fuentes.
- `Run Tests plan-only`: visible pero deshabilitado en v0.1.

## Runtime

Draft guardado durante QA:

`C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\taskspec_review\wabi_taskspec_review_20260519-195929.json`

El draft no contiene:

- prompt completo;
- valores de secretos;
- source completo;
- env values.

## QA Manual

Servidor:

- URL: `http://127.0.0.1:8787/`
- PID viejo: `10552`
- PID nuevo: `9520`

Mensajes probados:

- `programa un helper seguro para validar json`
  - `intent=code_request`
  - `route=code_plan`
  - `proposal_only=true`
  - `applied_to_sources=false`
  - `cloud_provider_called=false`
- `crea una escena de DUAT city con nodos de agentes`
  - `intent=graphics_scene_request`
  - `graphics_live=false`
- `usa nvidia para planear este cambio`
  - `intent=build_assist_request`
  - `budget_gate=CLOUD_BUDGET_DRY_RUN`
  - `cloud_provider_called=false`
- `POST /api/taskspec/apply`
  - `APPLY_BLOCKED_REVIEW_ONLY_V0_1`
  - `applied_to_sources=false`

Evidencia visual:

`C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_taskspec_review_20260519\wabi_ui_taskspec_review.png`

## Tests

```powershell
python -B -m pytest 02_CLAUDIO\tests\test_wabi_local_server.py 02_CLAUDIO\tests\test_wabi_conversation_api.py 02_CLAUDIO\tests\test_wabi_taskspec_review_api.py -q -p no:cacheprovider
python -B -m pytest tests\test_taskspec_review.py tests\test_conversation_engine.py tests\test_conversational_cli.py tests\test_graphics_bridge.py tests\test_cloud_budget.py tests\test_cloud_budget_ui_status.py tests\test_build_assist_cloud.py -q -p no:cacheprovider
python -B -m pytest -q -p no:cacheprovider
python -B -m py_compile 02_CLAUDIO\server\wabi_local_server.py
python -B -m py_compile wabi_sabi\core\conversation_engine.py wabi_sabi\core\taskspec_review.py wabi_sabi\core\graphics_bridge.py wabi_sabi\core\cloud_budget.py wabi_sabi\core\worktree.py wabi_sabi\cli\main.py
```

Resultados:

- BRAIN_OS focal combinado: `242 passed in 83.67s`.
- Wabi focal: `47 passed in 9.22s`.
- Wabi regression: `357 passed in 355.74s`.
- BRAIN_OS regression: `752 passed in 573.25s`.
- `py_compile`: PASS.
- Worktree timeout fix focal: `4 passed in 4.69s`.

## Nota de Estabilidad

Durante la regresion se detecto un timeout en `provider-status --json` cuando el workspace de prueba estaba bajo `AppData` y `git_worktree_summary()` heredaba el repo host `C:\Users\L-Tyr`. Se corrigio de forma acotada en `wabi_sabi/core/worktree.py` para no subir hasta el home cuando el workspace temporal no tiene marcador `.git`.

## Proxima Accion

Crear `TaskSpec Gate Preview`: vista de preflight que explique que faltaria para permitir apply local futuro, sin ejecutar comandos ni escribir fuentes.
