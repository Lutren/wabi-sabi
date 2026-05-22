# Wabi CloudBudgetGate v0.1 - 2026-05-19

## Proposito

`CloudBudgetGate` agrega un control local de llamadas cloud para build-assist.
La nube sigue siendo una capa temporal de propuesta; Wabi local decide, valida,
gatea y aplica solo por rutas separadas con rollback/tests.

No se hizo llamada live cloud en esta fase.

## Por que contador primero

NVIDIA y otros proveedores pueden no devolver `usage`, tokens o coste de forma
confiable en todos los adapters. Por eso v0.1 usa contador de llamadas como
control primario:

- llamadas por sesion;
- llamadas por dia local;
- estado `strict` por defecto;
- `usage/cost` solo informativo si aparece.

## Variables

```text
WABI_CLOUD_MAX_CALLS_PER_SESSION=3
WABI_CLOUD_MAX_CALLS_PER_DAY=10
WABI_CLOUD_BUDGET_MODE=strict
WABI_CLOUD_BUDGET_RESET=session
WABI_CLOUD_USAGE_DIR=<runtime>\cloud_budget
```

Para permitir una llamada cloud real siguen siendo obligatorias ambas banderas:

```text
WABI_BUILD_ASSIST_CLOUD=1
WABI_ALLOW_CLOUD_PROVIDERS=1
```

Sin doble opt-in, el estado es `CLOUD_BUDGET_DRY_RUN` y
`cloud_provider_called=false`.

## Runtime JSON

Ruta por defecto:

```text
C:\Users\<user>\.medioevo\wabi\runtime\cloud_budget\cloud_budget_YYYYMMDD.json
```

Ruta creada en esta corrida:

```text
C:\Users\L-Tyr\.medioevo\wabi\runtime\cloud_budget\cloud_budget_20260519.json
```

El archivo guarda contadores y metadatos redacted. No guarda prompts completos;
si hay intención de usuario, se registra `last_intent_hash` y una etiqueta
segura.

## Status

`/status` muestra:

```text
cloud_budget:
  mode: strict
  provider: nvidia
  model: nano-30b
  session_calls_used: 0
  session_calls_limit: 3
  daily_calls_used: 0
  daily_calls_limit: 10
  remaining_session_calls: 3
  remaining_daily_calls: 10
  cloud_live_ready: False
  double_opt_in: False
  budget_gate: CLOUD_BUDGET_DRY_RUN
  next_cloud_call_allowed: False
```

## Providers

`/providers` conserva la matriz de proveedores y agrega el mismo bloque
`cloud_budget` resumido al final.

## Build Assist

`build-assist-status --json` ahora incluye:

- `cloud_budget.schema=wabi.cloud_budget_gate.v0_1`
- `budget_gate`
- `remaining_session_calls`
- `remaining_daily_calls`
- `double_opt_in`
- `next_cloud_call_allowed`

`build-assist-plan` revisa presupuesto antes de cualquier llamada real. Si el
presupuesto esta excedido:

- `error=CLOUD_BUDGET_EXCEEDED`
- `cloud_provider_called=false`
- `real_apply_allowed=false`

## Estados

- `CLOUD_BUDGET_READY`: doble opt-in y presupuesto disponible.
- `CLOUD_BUDGET_DRY_RUN`: falta doble opt-in; no llama provider.
- `CLOUD_BUDGET_EXCEEDED`: presupuesto excedido en modo strict.
- `CLOUD_BUDGET_REVIEW`: presupuesto excedido en modo warn; no usar como
  aprobacion de seguridad.
- `CLOUD_BUDGET_RECORD_PASS`: registro local de planned/completed/blocked.

## Limites v0.1

- El control de coste es informativo si el provider devuelve uso; no es el gate
  primario.
- La sesion por defecto se deriva del proceso si no existe `WABI_SESSION_ID`.
- No hay UI cableada todavia; el estado ya existe para CLI/engine.
- No cambia aliases `super/ultra`; siguen en revision manual.
- `GraphicsBridge` permanece plan-only (`graphics_live=false`).

## Evidencia

```powershell
python -B -m pytest tests\test_cloud_budget.py tests\test_conversation_engine.py tests\test_conversational_cli.py tests\test_build_assist_cloud.py -q -p no:cacheprovider
python -B -m py_compile wabi_sabi\core\cloud_budget.py wabi_sabi\core\conversation_engine.py wabi_sabi\core\build_assist_cloud.py wabi_sabi\cli\main.py
python -B -m pytest -q -p no:cacheprovider
```

Resultados:

- Focal: `34 passed in 15.93s`.
- `py_compile`: PASS.
- Regresion Wabi: `347 passed in 192.89s (0:03:12)`.
- Secret scan focal del budget JSON: `0` coincidencias.

## Siguiente paso recomendado

Exponer el mismo `cloud_budget` en la UI local de Wabi y agregar un contador de
sesion legible para el operador, sin abrir llamadas live nuevas.
