# WABI UI Visual QA - Cloud Budget

Fecha: 2026-05-19

Fingerprint: `WABI_CLOUD_BUDGET_UI_VISUAL_QA_20260519`

## Estado

- ActionGate: `APPROVE_LOCAL_VISUAL_UI_QA`
- CloudGate: `PROPOSAL_ONLY_DOUBLE_OPT_IN`
- CloudBudgetGate: `UI_VISIBLE_DRY_RUN_CONFIRMED`
- UIGate: `PASS_LOCAL_8787`
- GraphicsGate: `PLAN_ONLY_READY / graphics_live=false`
- BrowserBridgeGate: `NO_LIVE_CALL`
- PublicationGate: `BLOCK`

## Servidor UI

- URL usada: `http://127.0.0.1:8787/`
- Servidor real: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\02_CLAUDIO\server\wabi_local_server.py`
- UI real: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\apps\local\wabi_ui\index.html`
- PID stale encontrado: `23276`, proceso no encontrado.
- PID nuevo registrado: `30848`.

## Endpoint Validado

- Endpoint: `GET /api/cloud-budget/status`
- Fuente de verdad: `wabi_sabi.core.cloud_budget.CloudBudgetGate.render_status`
- Resultado: `PASS`

Campos confirmados:

- `budget_gate=CLOUD_BUDGET_DRY_RUN`
- `provider=nvidia`
- `model_alias=nano-30b`
- `double_opt_in=false`
- `cloud_live_ready=false`
- `proposal_only=true`
- `cloud_provider_called=false`
- `next_cloud_call_allowed=false`
- `session_calls=0/3`
- `daily_calls=0/10`
- `usage_known=false`
- `cost_known=false`

## Evidencia Visual

El panel `Cloud Budget` aparece visualmente en la UI local. Campos visibles:

- CloudGate
- Provider/model
- Double opt-in
- Next call allowed
- Provider called
- Proposal-only
- Usage/cost known
- Last status
- Session calls
- Daily calls

Artefactos:

- `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_visual_qa\WABI_CLOUD_BUDGET_UI_VISUAL_QA_20260519\cloud_budget_status_redacted.json`
- `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_visual_qa\WABI_CLOUD_BUDGET_UI_VISUAL_QA_20260519\wabi_cloud_budget_ui_20260519.png`
- `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_visual_qa\WABI_CLOUD_BUDGET_UI_VISUAL_QA_20260519\wabi_cloud_budget_ui_tall_20260519.png`
- `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_visual_qa\WABI_CLOUD_BUDGET_UI_VISUAL_QA_20260519\ui_visual_qa_summary_redacted.json`

## Comandos Ejecutados

```powershell
Start-Process python -B 02_CLAUDIO/server/wabi_local_server.py --host 127.0.0.1 --port 8787
Invoke-RestMethod http://127.0.0.1:8787/api/cloud-budget/status
msedge --headless --disable-background-networking --screenshot ... http://127.0.0.1:8787/
python -B -m pytest 02_CLAUDIO\tests\test_wabi_local_server.py -q -p no:cacheprovider
python -B -m pytest tests\test_cloud_budget_ui_status.py tests\test_cloud_budget.py tests\test_build_assist_cloud.py tests\test_conversation_engine.py tests\test_conversational_cli.py -q -p no:cacheprovider
python -B -m pytest -q -p no:cacheprovider
python -B -m py_compile 02_CLAUDIO\server\wabi_local_server.py
python -B -m py_compile wabi_sabi\core\cloud_budget.py wabi_sabi\cli\main.py
.\wabi.cmd build-assist-status --json
.\wabi.cmd --once "hola wabi"
.\wabi.cmd build-assist-plan "crear helper seguro" --dry-run --json
.\wabi.cmd with /status, /providers, /exit
```

## Resultados

- BRAIN_OS server focal: `229 passed in 116.51s (0:01:56)`
- Wabi focal: `39 passed in 23.23s`
- Wabi full regression: `352 passed in 214.62s (0:03:34)`
- `py_compile`: `PASS`
- Manual no-live smokes: `PASS`

## Gates Preservados

- No hubo llamada live cloud.
- No se activaron `WABI_BUILD_ASSIST_CLOUD=1` ni `WABI_ALLOW_CLOUD_PROVIDERS=1`.
- `cloud_provider_called=false`.
- BrowserBridge live no se activo.
- `graphics_live=false`.
- No hubo push, deploy, commit ni publicacion.
- No se imprimieron secretos.
- No se guardaron prompts completos.

## Proxima Accion Verificable

Cablear la UI local de Wabi al `ConversationEngine` mediante un endpoint local seguro, manteniendo:

- `cloud_provider_called=false` por defecto.
- `applied_to_sources=false` por defecto.
- `graphics_live=false`.
- CloudBudgetGate visible.
- Sin boton para aplicar output cloud.

## Continuacion - UI ConversationEngine

- Se agrego `POST /api/conversation/turn`.
- La UI ahora muestra panel `Wabi Conversation`.
- La clasificacion de intents ocurre en `ConversationEngine`, no en JavaScript.
- Cloud Budget sigue visible y conectado a `CloudBudgetGate.render_status()`.
- Smokes UI:
  - `hola wabi` -> `chat_general`.
  - `crea una escena de DUAT city con nodos de agentes` -> `graphics_scene_request`, `graphics_live=false`.
  - `usa nvidia para planear este cambio` -> `build_assist_request`, `cloud_provider_called=false`.
- No hubo live cloud call.
- Evidencia visual nueva:
  `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_conversation_engine_20260519\wabi_ui_conversation_engine.png`
