# WABI UI TaskSpec Gate Preview v0.1 - 2026-05-19

Fingerprint: `WABI_UI_TASKSPEC_GATE_PREVIEW_20260519`

## Estado

- UI local: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\apps\local\wabi_ui\index.html`
- Servidor local: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\02_CLAUDIO\server\wabi_local_server.py`
- Backend: `wabi_sabi/core/taskspec_review.py`
- Endpoint nuevo: `GET /api/taskspec/gate-preview`
- Apply: bloqueado, `APPLY_BLOCKED_REVIEW_ONLY_V0_1`
- Gate Preview: `APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1`
- Cloud: no live call, `cloud_provider_called=false`
- Graphics: plan-only, `graphics_live=false`
- PublicationGate: `BLOCK`

## Implementacion

`taskspec_review.py` ahora expone funciones de preview:

- `build_gate_preview(task_spec)`
- `evaluate_apply_readiness(task_spec)`
- `list_required_gates(task_spec)`
- `list_required_tests(task_spec)`
- `list_required_rollback(task_spec)`
- `block_apply_with_preview(task_spec)`

El servidor local agrega `GET /api/taskspec/gate-preview` y devuelve una evaluacion redacted del TaskSpec actual. El endpoint usa la misma normalizacion backend de TaskSpec; la UI solo renderiza el JSON recibido.

## Respuesta Minima

El preview devuelve:

- `apply_status=BLOCKED`
- `reason=APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1`
- `proposal_only=true`
- `applied_to_sources=false`
- `cloud_provider_called=false`
- `graphics_live=false`
- `rollback_required=true`
- required future gates: `ActionGate`, `GhostGate`, `RollbackStore`, `TestRunner`, `PathAllowlist`

Si el TaskSpec necesita cloud o graphics, el preview conserva el limite:

- Cloud sigue `proposal_only`.
- Graphics sigue `plan-only`.
- Ninguna salida se aplica a fuentes.

## UI

El panel `Review TaskSpec` ahora incluye seccion `Gate Preview` con:

- Apply Status
- Reason
- Required Gates
- Required Tests
- Rollback Required
- Affected Paths Preview
- Blockers
- Next Safe Action
- JSON redacted desplegable

El boton `Gate Preview` llama `GET /api/taskspec/gate-preview`. El boton `Apply bloqueado` sigue llamando al endpoint bloqueado y muestra el mismo preview; no ejecuta comandos ni modifica archivos.

## QA

Comandos ejecutados:

- `python -B -m pytest tests\test_taskspec_review.py -q -p no:cacheprovider` -> `9 passed in 0.84s`
- `python -B -m pytest 02_CLAUDIO\tests\test_wabi_taskspec_gate_preview_api.py -q -p no:cacheprovider` -> `6 passed in 7.71s`
- `python -B -m pytest tests\test_taskspec_review.py tests\test_conversation_engine.py tests\test_conversational_cli.py tests\test_graphics_bridge.py tests\test_cloud_budget.py tests\test_cloud_budget_ui_status.py tests\test_build_assist_cloud.py -q -p no:cacheprovider` -> `52 passed in 14.33s`
- `python -B -m pytest 02_CLAUDIO\tests\test_wabi_local_server.py 02_CLAUDIO\tests\test_wabi_conversation_api.py 02_CLAUDIO\tests\test_wabi_taskspec_review_api.py 02_CLAUDIO\tests\test_wabi_taskspec_gate_preview_api.py -q -p no:cacheprovider` -> `248 passed in 270.38s`
- `python -B -m pytest -q -p no:cacheprovider` in Wabi -> `362 passed in 156.89s`
- `python -B -m pytest -q -p no:cacheprovider` in BRAIN_OS -> `758 passed in 153.48s`
- `python -B -m py_compile ...` -> PASS for Wabi modules and BRAIN_OS server

Manual no-live smokes:

- `.\wabi.cmd --once "hola wabi"` -> PASS
- `.\wabi.cmd build-assist-status --json` -> PASS, `CLOUD_BUDGET_DRY_RUN`
- `.\wabi.cmd build-assist-plan "crear helper seguro" --dry-run --json` -> PASS, `cloud_provider_called=false`
- Local API smoke for `POST /api/conversation/turn`, `GET /api/taskspec/gate-preview`, `POST /api/taskspec/apply` -> PASS
- Interactive UI screenshot confirms `Gate Preview`, `Apply Status=BLOCKED`, required gates and `Cloud Budget` dry-run.

## Evidencia

- Endpoint smoke: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_taskspec_gate_preview_20260519\gate_preview_endpoint_smoke.json`
- UI screenshot: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_taskspec_gate_preview_20260519\wabi_ui_taskspec_gate_preview_interactive.png`
- Static UI screenshot: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_taskspec_gate_preview_20260519\wabi_ui_taskspec_gate_preview.png`

## Limites

- No existe apply real en v0.1.
- No se ejecutan tests desde UI.
- No se escriben fuentes desde UI.
- No hay cloud live call.
- No hay BrowserBridge live.
- No hay graphics live.

## Proxima Accion

Definir el contrato futuro de `ActionGate + GhostGate + RollbackStore + TestRunner` para un sandbox local apply, manteniendo UI apply bloqueado hasta que exista snapshot, allowlist, rollback y tests por TaskSpec.
