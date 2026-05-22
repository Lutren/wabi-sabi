# Wabi Conversational CLI v0.1 - 2026-05-19

## Estado

`wabi` sin argumentos abre una sesion conversacional local-first:

```powershell
.\wabi.cmd
```

Salida esperada:

```text
Wabi-Sabi Conversational CLI
mode: local-first
cloud: proposal_only
graphics: available|unavailable_plan_stub
type /help for commands
wabi>
```

Para salir:

```text
/exit
/quit
```

## Capa comun

La capa nueva vive en:

- `wabi_sabi/core/conversation_engine.py`
- `wabi_sabi/core/graphics_bridge.py`

`ConversationEngine` envuelve la sesion conversacional existente
`ConversationSession`, por lo que CLI y UI/local adapters pueden compartir:

- clasificacion de intencion;
- `ConversationTurn`;
- `WorkIntent`;
- `TaskSpec` proposal-only;
- status/providers heredados;
- redaccion;
- memoria local;
- gates antes de cualquier escritura real.

## Intenciones v0.1

`classify_intent(text)` devuelve:

- `chat_general`
- `status_query`
- `plan_request`
- `code_request`
- `debug_request`
- `file_task_request`
- `graphics_scene_request`
- `graphics_asset_request`
- `build_assist_request`
- `handoff_request`
- `unsafe_or_external_request`

Cada intent incluye:

- `intent_name`
- `confidence`
- `action_gate`
- `needs_cloud`
- `needs_graphics`
- `needs_file_write`
- `proposal_only`
- `reason`

## Comandos internos

```text
/help
/status
/providers
/graphics
/tasks
/plan <texto>
/work <texto>
/create <texto>
/code <texto>
/debug <texto>
/exit
/quit
```

Tambien se acepta lenguaje natural sin slash:

```text
hola wabi
programa un helper seguro para validar json
debuggea el build assist
crea una escena de DUAT city con nodos de agentes
genera assets para agentes
usa nvidia para planear este cambio
```

## Build Assist NVIDIA

La integracion conserva el contrato:

- cloud solo propone;
- no hay auto-apply;
- no se imprimen secretos;
- no se envia workspace completo;
- live requiere doble bandera:
  - `WABI_BUILD_ASSIST_CLOUD=1`
  - `WABI_ALLOW_CLOUD_PROVIDERS=1`

`ConversationEngine` puede reconocer `build_assist_request`, consultar estado y
preparar `TaskSpec`, pero no llama provider desde el turno conversacional. La
llamada live sigue aislada en:

```powershell
.\wabi.cmd build-assist-smoke --provider nvidia --model nano-30b --live --json
```

## Graphics Bridge

`GraphicsBridge` descubre el motor grafico DUAT local si existe:

- `artifacts/duat-city/src/graphics`
- renderers isometricos;
- atlas/sprite resolver;
- light/shadow/particle/render budget.

Estado v0.1:

- `graphics_plan_ready=true`
- `graphics_live=false`
- `external_calls_allowed=false`
- `publication_allowed=false`
- `private_asset_access_allowed=false`

Puede crear:

- scene plan;
- asset plan;
- graphics task spec;
- artefacto JSON local bajo runtime.

No modifica renderer, no copia assets, no publica y no usa red.

## Gates y limites

- `ActionGate BLOCK`: secretos, deploy, push, publicacion, borrado.
- `proposal_only=true`: todo turno de trabajo prepara plan/spec; no aplica.
- `applied_to_sources=false`: salida cloud/grafica no toca fuentes.
- `PublicationGate=BLOCK`: no hay release externo.
- `BrowserBridge live`: no activado.

## Evidencia 2026-05-19

Pruebas focales:

```powershell
python -B -m pytest tests\test_conversational_cli.py tests\test_conversation_engine.py tests\test_graphics_bridge.py -q -p no:cacheprovider
```

Resultado final:

- `14 passed in 3.69s`
- Focal expandido conversacional + redaccion: `25 passed in 15.26s`

Regresion completa:

```powershell
python -B -m pytest -q -p no:cacheprovider
```

Resultado final:

- `336 passed in 495.58s (0:08:15)`

Compilacion Python:

```powershell
python -B -m py_compile wabi_sabi\cli\main.py wabi_sabi\core\conversation_engine.py wabi_sabi\core\graphics_bridge.py wabi_sabi\core\redaction.py
```

Resultado:

- PASS

Smokes manuales:

- `.\wabi.cmd --help`: PASS.
- `.\wabi.cmd --once "hola wabi" --json`: PASS, `route=local_chat`, `intent_name=chat_general`, `cloud_provider_called=false`.
- `.\wabi.cmd build-assist-status --json`: PASS, `cloud_live_ready=false` en sesion sin doble bandera, `default_model_alias=nano-30b`.
- `.\wabi.cmd` con `/help`, `/status`, escena DUAT, helper JSON y `/exit`: PASS.

## Artefactos runtime

La prueba interactiva genero artefactos locales proposal-only:

- `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\graphics_bridge\wabi_graphics_plan_20260519-140223.json`
- `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\conversation_tasks\wabi_conversation_task_20260519-140223.json`

## Estado pendiente

- UI local puede reutilizar `ConversationEngine`, pero aun no se actualizo un
  componente UI para consumir directamente `ConversationTurn`.
- `GraphicsBridge` no tiene API live del renderer; queda plan-only hasta que
  DUAT exponga endpoint/adapter estable.
- Costos/tokens cloud solo se conocen cuando el provider los devuelve.
