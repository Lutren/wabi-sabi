# WABI UI ConversationEngine - 2026-05-19

Fingerprint: WABI_UI_CONVERSATION_ENGINE_20260519

## Estado

- ActionGate: APPROVE_LOCAL
- CloudGate: PROPOSAL_ONLY_DOUBLE_OPT_IN
- CloudBudgetGate: UI_VISIBLE_DRY_RUN_EXPECTED
- UIGate: LOCAL_UI_CONVERSATION_READY
- ConversationGate: API_CONNECTED_TO_CONVERSATION_ENGINE
- GraphicsGate: PLAN_ONLY_READY / graphics_live=false
- PublicationGate: BLOCK

## Implementacion

La UI local de Wabi en:

`C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\apps\local\wabi_ui\index.html`

ahora contiene un panel `Wabi Conversation` que envia turnos a:

`POST /api/conversation/turn`

El endpoint vive en:

`C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\02_CLAUDIO\server\wabi_local_server.py`

y llama a:

`wabi_sabi.core.conversation_engine.ConversationEngine.handle_turn`

desde la ruta canonica:

`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi`

## Contrato del endpoint

Entrada:

```json
{
  "message": "texto del usuario",
  "mode": "ui",
  "session_id": "..."
}
```

Salida redacted:

```json
{
  "status": "OK",
  "route": "local_chat|work_plan|code_plan|debug_plan|graphics_plan|build_assist_plan",
  "intent": {
    "intent_name": "...",
    "confidence": 0.0,
    "needs_cloud": false,
    "needs_graphics": false,
    "needs_file_write": false,
    "proposal_only": true,
    "action_gate": "APPROVE|REVIEW|BLOCK"
  },
  "response": "...",
  "task_spec": {},
  "cloud_budget": {},
  "graphics": {},
  "applied_to_sources": false,
  "cloud_provider_called": false,
  "secrets_printed": false,
  "proposal_only": true
}
```

## Seguridad

- No hubo llamada live cloud en esta fase.
- La UI no tiene boton para llamar NVIDIA.
- La UI no tiene boton para aplicar output cloud.
- El endpoint instancia `ConversationEngineOptions` con:
  - `allow_cloud=false`
  - `persist_turns=false`
  - `include_prompt_in_turn=false`
  - `write_artifacts=false`
- `GraphicsBridge` permanece `graphics_live=false`.
- `BrowserBridge live` no fue activado.
- `PublicationGate` permanece `BLOCK`.

## Mensajes probados

- `hola wabi` -> `chat_general`, `cloud_provider_called=false`.
- `programa un helper seguro para validar json` -> `code_request`, `applied_to_sources=false`.
- `crea una escena de DUAT city con nodos de agentes` -> `graphics_scene_request`, `graphics_live=false`.
- `usa nvidia para planear este cambio` -> `build_assist_request`, `CLOUD_BUDGET_DRY_RUN`, `cloud_provider_called=false`.

## Evidencia

- UI URL: `http://127.0.0.1:8787/`
- Servidor reiniciado localmente: viejo PID `30848`, nuevo PID `10552`.
- Screenshot:
  `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_conversation_engine_20260519\wabi_ui_conversation_engine.png`
- Endpoint `/api/cloud-budget/status`:
  - `budget_gate=CLOUD_BUDGET_DRY_RUN`
  - `provider=nvidia`
  - `model_alias=nano-30b`
  - `double_opt_in=false`
  - `cloud_live_ready=false`
  - `proposal_only=true`
  - `cloud_provider_called=false`

## QA

```powershell
python -B -m pytest 02_CLAUDIO\tests\test_wabi_local_server.py -q -p no:cacheprovider
python -B -m pytest 02_CLAUDIO\tests\test_wabi_conversation_api.py -q -p no:cacheprovider
python -B -m pytest tests\test_conversation_engine.py tests\test_conversational_cli.py tests\test_graphics_bridge.py tests\test_cloud_budget.py tests\test_cloud_budget_ui_status.py tests\test_build_assist_cloud.py -q -p no:cacheprovider
python -B -m pytest -q -p no:cacheprovider
python -B -m py_compile 02_CLAUDIO\server\wabi_local_server.py
python -B -m py_compile wabi_sabi\core\conversation_engine.py wabi_sabi\core\graphics_bridge.py wabi_sabi\core\cloud_budget.py wabi_sabi\cli\main.py
```

Resultados:

- `02_CLAUDIO\tests\test_wabi_local_server.py`: `229 passed in 173.21s`.
- `02_CLAUDIO\tests\test_wabi_conversation_api.py`: `6 passed in 10.66s`.
- Wabi focal: `43 passed in 69.12s`.
- Wabi full: `353 passed in 218.37s`.
- BRAIN_OS full: `745 passed in 196.72s`.
- `py_compile`: PASS.

## Proxima accion segura

Agregar un flujo UI `Review TaskSpec` que permita ver un plan local generado por ConversationEngine y enviarlo a un gate futuro de apply local, sin cloud live y sin aplicar por defecto.
