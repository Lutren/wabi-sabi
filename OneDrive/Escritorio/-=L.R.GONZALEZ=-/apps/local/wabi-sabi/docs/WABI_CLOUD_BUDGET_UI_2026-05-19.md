# WABI_CLOUD_BUDGET_UI_2026-05-19

## Proposito

Exponer `CloudBudgetGate v0.1` en la UI local de Wabi sin activar llamadas live cloud. La UI queda como cockpit de estado: lee presupuesto, muestra gates y avisa que NVIDIA es `proposal_only`.

## Donde aparece

- UI: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\apps\local\wabi_ui\index.html`
- Panel: `Cloud Budget`
- Endpoint local: `GET /api/cloud-budget/status`
- Server: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\02_CLAUDIO\server\wabi_local_server.py`

## Fuente de verdad

El endpoint usa la misma logica que CLI/build-assist:

```txt
wabi_sabi.core.cloud_budget.CloudBudgetGate.render_status()
```

No duplica calculos en JavaScript. El frontend solo renderiza el JSON redacted devuelto por el servidor local.

## Campos visibles

- `CloudGate`
- `CloudBudgetGate`
- provider/model: `nvidia / nano-30b`
- double opt-in
- session calls used / limit / remaining
- daily calls used / limit / remaining
- next cloud call allowed
- `cloud_provider_called=false`
- `proposal_only=true`
- `usage_known` / `cost_known`
- last status

## Por que la UI no llama cloud

Esta fase solo muestra estado y prepara UX. No agrega boton para llamar NVIDIA, no aplica output cloud y no activa `BrowserBridge` ni `graphics_live`.

Llamadas cloud reales siguen aisladas en build-assist y requieren:

```txt
WABI_BUILD_ASSIST_CLOUD=1
WABI_ALLOW_CLOUD_PROVIDERS=1
CloudBudgetGate != CLOUD_BUDGET_EXCEEDED
```

## Estados visuales

- `CLOUD_BUDGET_DRY_RUN`: neutral/review, sin doble opt-in.
- `CLOUD_BUDGET_READY`: normal, doble opt-in y presupuesto disponible.
- `CLOUD_BUDGET_EXCEEDED`: warning/review, no debe llamar provider.
- `CLOUD_BUDGET_REVIEW`: warning, estado incompleto o no disponible.

## Limites v0.1

- El control primario sigue siendo contador local de llamadas, no coste/tokens.
- Si el provider no devuelve usage/cost, `usage_known=false` y `cost_known=false`.
- Consultar estado puede crear el JSON local de presupuesto con contadores en cero.
- La UI aun no ejecuta build-assist; solo muestra presupuesto.

## Evidencia

- Focal UI: `tests/test_cloud_budget_ui_status.py` -> `5 passed`.
- Focal requerido: `tests/test_cloud_budget.py tests/test_cloud_budget_ui_status.py tests/test_conversation_engine.py tests/test_conversational_cli.py tests/test_build_assist_cloud.py` -> `39 passed`.
- Regresion Wabi completa: `352 passed in 372.11s (0:06:12)`.
- BRAIN_OS server/UI focal: `229 passed in 138.64s (0:02:18)`.
- `py_compile`: PASS para Wabi core/CLI/test UI y `-= BRAIN_OS =-\02_CLAUDIO\server\wabi_local_server.py`.
- Manual no-live: `build-assist-status --json`, `--once "hola wabi"`, `build-assist-plan --dry-run --json`, REPL `/status`, `/providers`, `/exit`.
- Live cloud call: no ejecutada.
- `graphics_live`: false.
- BrowserBridge live: no activado.

## Siguiente paso recomendado

Agregar, sin live cloud todavia, una explicacion contextual en el chat UI cuando el usuario pida build-assist: mostrar `CloudBudgetGate` y pedir doble opt-in operativo antes de cualquier llamada real.
