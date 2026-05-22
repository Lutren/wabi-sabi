# Report Wabi Sabi Local Agents

Fecha de cierre: 2026-05-05

Estado: FUNCIONAL / PROGRAMACION_LOCAL_ACOTADA

Closure fingerprint operativo:
`cd2307aeed9e4c2463f4247bb292c16c4d1b4dbe2a21efabc434eba9ae39e06d`

## Resumen ejecutivo

Wabi Sabi queda como CLI local-first aislado en `apps/local/wabi-sabi`, con
router de intencion, registro de agentes, ActionGate, memoria JSONL, wrappers
Windows, entrypoint instalable `wabi`, documentacion y pruebas minimas. La
actualizacion del 2026-05-06 agrega programacion local acotada con
`--apply --target <archivo.py>`.

El sistema funciona sin nube y sin claves. No hace push, deploy, publicacion,
borrado destructivo ni lectura de secretos. Las acciones automaticas escriben
artefactos en `runtime/outputs` y registran evidencia append-only en
`runtime/logs/wabi_events.jsonl`. El modo `--apply` puede escribir un archivo
Python dentro del workspace con diff, backup, hashes y `py_compile`; no toca
rutas externas ni sensibles.

## Mapa del sistema

- CLI: `wabi_sabi/cli/main.py`
- Parser: `wabi_sabi/cli/parser.py`
- Router: `wabi_sabi/cli/router.py`
- Registro: `wabi_sabi/config/agents.json`
- Gate: `wabi_sabi/core/gate.py`
- Memoria/logs: `wabi_sabi/core/memory.py`
- ObservationEnvelope: `wabi_sabi/core/observation.py`
- Programacion acotada: `wabi_sabi/core/programming.py`
- Agentes: `wabi_sabi/agents/`
- Tests: `tests/`
- Docs: `docs/`
- Wrapper CMD: `wabi.cmd`
- Wrapper PowerShell: `wabi.ps1`
- Runtime local: `runtime/`

## Agentes registrados

| agente | funcion | gate |
|---|---|---|
| `programmer` | genera codigo local como artefacto seguro; con `--apply --target` aplica parches Python acotados | safe_mode true |
| `debugger` | genera diagnosticos, detecta marcadores y comandos de test | safe_mode true |
| `researcher` | busca evidencia en docs locales | safe_mode true |
| `file` | resume/registra tareas de archivo y genera README borrador | safe_mode true |

## Archivos creados

- `.gitignore`
- `pyproject.toml`
- `README.md`
- `wabi.cmd`
- `wabi.ps1`
- `wabi_sabi/__init__.py`
- `wabi_sabi/config/agents.json`
- `wabi_sabi/core/config.py`
- `wabi_sabi/core/gate.py`
- `wabi_sabi/core/memory.py`
- `wabi_sabi/core/observation.py`
- `wabi_sabi/core/tools.py`
- `wabi_sabi/cli/main.py`
- `wabi_sabi/cli/parser.py`
- `wabi_sabi/cli/router.py`
- `wabi_sabi/agents/base_agent.py`
- `wabi_sabi/agents/programmer_agent.py`
- `wabi_sabi/agents/debug_agent.py`
- `wabi_sabi/agents/research_agent.py`
- `wabi_sabi/agents/file_agent.py`
- `tests/test_cli.py`
- `tests/test_router.py`
- `tests/test_agents.py`
- `tests/test_memory.py`
- `docs/USAGE.md`
- `docs/ARCHITECTURE.md`
- `REPORT_WABI_SABI_LOCAL_AGENTS.md`

## Artefactos runtime generados

- `runtime/logs/wabi_events.jsonl`
- `runtime/memory/session_memory.jsonl`
- `runtime/outputs/programmer_file_summary_20260505-150413.py`
- `runtime/outputs/programmer_file_summary_20260505-151047.py`
- `runtime/outputs/debug_diagnostic_20260505-150426.json`
- `runtime/outputs/debug_diagnostic_20260505-150842.json`
- `runtime/outputs/debug_diagnostic_20260505-150853.json`
- `runtime/outputs/README_draft_20260505-150835.md`

## Comandos ejecutados

Contexto inicial:

```powershell
python tools\release\pending_review.py --write --quiet
python tools\pending_review.py --write --quiet
```

Resultados:

- Raiz: `active_dedup=444`, `claudio_open=69`.
- Claudio: `active_dedup=444`, `claudio_open=69`.

Validacion de Wabi:

```powershell
python -m compileall -q wabi_sabi
python -m pytest -q
.\wabi.cmd e2e-smoke --json
.\wabi.cmd "ejecuta diagnostico" --json
.\wabi.cmd agents --json
python -m pip install -e . --no-deps
python -m pip install -e . --no-deps --no-build-isolation
wabi "crea un README para este modulo" --json
wabi "arregla los tests" --json
wabi "revisa este proyecto y dime que falla" --json
wabi logs
python -m pytest -q
python -m compileall -q wabi_sabi
wabi e2e-smoke --json
```

## Resultados de pruebas

- `python -m compileall -q wabi_sabi` -> OK.
- Primera suite: `8 passed`.
- Suite final despues de agregar cobertura directa para `file` y `researcher`:
  `10 passed in 3.51s`.
- E2E final instalado: `wabi e2e-smoke --json` -> `ok=true`,
  `intent=code_generation`, `agent=programmer`, `gate=APPROVE`,
  artefacto `programmer_file_summary_20260505-151047.py`, log
  `runtime/logs/wabi_events.jsonl`.
- `wabi "ejecuta diagnostico" --json` -> `agent=debugger`, artefacto JSON de
  diagnostico.
- `wabi "crea un README para este modulo" --json` -> `agent=file`, artefacto
  `README_draft_20260505-150835.md`.
- `wabi "arregla los tests" --json` -> `agent=debugger`, `gate=REVIEW`,
  diagnostico local sin edicion destructiva.
- `wabi logs` -> lista eventos JSONL append-only con prompts, agente, gate,
  artefactos y fingerprints.

## Fallos encontrados y corregidos

| fallo | clasificacion | accion |
|---|---|---|
| No habia CLI Wabi Sabi con router/registro de agentes verificable | CLI inexistente / agente no conectado | creado carril `apps/local/wabi-sabi` |
| El CLI existente de Desktop era conversacional con Ollama pero sin contrato Wabi E2E | contrato mal definido | creado parser, router, registry y tests |
| `python -m pip install -e . --no-deps` quedo en timeout | dependencia/build isolation con posible red | documentado y validado `--no-build-isolation` |
| Faltaba cobertura directa para `file` y `researcher` | test incompleto | agregados tests focales; suite final `10 passed` |

## Fallos pendientes reales

- El CLI no es todavia un reemplazo completo de Codex para ediciones profundas
  multiarchivo. En modo seguro genera artefactos y diagnosticos; no parchea
  codigo fuente arbitrario sin un alcance mas especifico.
- Ollama/modelos locales no son dependencia obligatoria en este carril. La
  version funcional actual es determinista/local; se puede agregar proveedor
  local opcional despues sin romper el fallback.
- `arregla los tests` queda en `REVIEW` y genera diagnostico. Es correcto para
  el gate actual porque reparar tests implica escrituras sobre codigo fuente.

## Como ejecutar el CLI

Sin instalar:

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
.\wabi.cmd "crea una funcion que lea un archivo y resuma sus lineas"
.\wabi.cmd "ejecuta diagnostico"
```

Instalado:

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
python -m pip install -e . --no-deps --no-build-isolation
wabi "crea un README para este modulo"
```

Modo interactivo:

```powershell
.\wabi.cmd
```

## Como pedirle tareas

```powershell
wabi "crea una funcion que lea un archivo y resuma sus lineas"
wabi "revisa este proyecto y dime que falla"
wabi "arregla los tests"
wabi "crea un README para este modulo"
wabi "ejecuta diagnostico"
```

## Como agregar nuevos agentes

1. Crear `wabi_sabi/agents/nuevo_agent.py`.
2. Heredar de `BaseAgent`.
3. Devolver `AgentResult` con evidencia, artefactos y CERTEZA/INFERENCIA/INCOGNITA.
4. Agregar entrypoint en `wabi_sabi/config/agents.json`.
5. Agregar ruta en `intent_routes` si necesita intencion propia.
6. Crear test focal en `tests/`.

## Actualizacion 2026-05-06 - programacion local acotada

Se agrego `--apply --target <archivo.py>`:

- solo dentro de `--workspace`;
- bloquea rutas sensibles, runtime, vendors, builds, releases, TCG/game bridge
  y paths externos;
- crea backup cuando el archivo tenia contenido previo;
- crea diff en `runtime/outputs`;
- registra hashes `before/after`;
- verifica con `py_compile`;
- deja evento JSONL y ObservationEnvelope.

Comando de verificacion:

```powershell
python -m pytest -q
python -m compileall -q wabi_sabi
.\wabi.cmd "crea una funcion que lea un archivo y resuma sus lineas" --apply --target runtime_test_helpers.py --json
```

Para no ensuciar el paquete, los targets de prueba deben apuntar a workspaces
temporales o retirarse despues de registrar evidencia.

## Actualizacion 2026-05-06 - puente Codex directo

Se agrego `wabi codex` para poder usar Codex a traves de Wabi-Sabi:

- `codex-status` detecta proveedor disponible.
- proveedor `auto` usa `codex.cmd` si existe.
- `codex-cli` ejecuta `codex --ask-for-approval never exec --sandbox read-only --ephemeral`.
- si no hay CLI y existe `OPENAI_API_KEY`, puede usar OpenAI Responses API.
- `--dry-run` genera workpack local sin llamar modelos.
- `ActionGate` bloquea publicacion, secretos o borrado antes de invocar proveedor.

Evidencia actual:

```powershell
python -m compileall -q wabi_sabi tests
python -m pytest -q
.\wabi.cmd e2e-smoke --json
.\wabi.cmd codex-status --json
.\wabi.cmd codex "responde solo WABI_CODEX_DRY_RUN_OK" --dry-run --json
.\wabi.cmd codex "responde exactamente WABI_CODEX_EPHEMERAL_OK" --json
$inputText = "hola wabi`n/exit`n"; $inputText | .\wabi.cmd
.\wabi.cmd codex "publica esto en github" --json
```

Resultados:

- `python -m compileall -q wabi_sabi tests` -> OK.
- `python -m pytest -q` -> `26 passed in 3.22s`.
- `e2e-smoke` -> `ok=true`, `agent=programmer`, `gate=APPROVE`.
- `codex-status` -> `codex_cli.available=true`,
  `path=C:\Users\L-Tyr\AppData\Roaming\npm\codex.cmd`,
  `auto_provider=codex-cli`; `OPENAI_API_KEY` no esta configurada.
- `codex --dry-run` -> workpack escrito en `runtime/outputs`.
- llamada real `wabi codex` -> salida exacta `WABI_CODEX_EPHEMERAL_OK`,
  `returncode=0`, sandbox `read-only`, sesion `ephemeral`.
- modo interactivo `.\wabi.cmd` acepto prompt por stdin y salio con `/exit`.
- prompt externo `publica esto en github` -> `BLOCK` por
  `external_publication_or_network_action`.

Fallo corregido durante la prueba:

- La primera integracion puso `--ask-for-approval` despues de `exec`; Codex CLI
  lo rechazo como argumento inesperado. Se corrigio el orden para pasarlo como
  opcion global antes de `exec`.

## Actualizacion 2026-05-06 - ventana persistente y modo auto

Se agrego una superficie de operador para uso continuo:

- `wabi-window.cmd` abre una ventana PowerShell visible.
- `wabi-window.ps1 -Here` permite ejecutar la misma ventana en la consola
  actual, util para pruebas.
- `wabi auto` deja un prompt persistente `Wabi-Auto>`.
- `wabi auto "<pedido>"` ejecuta una sola consulta en modo auto.
- `auto_router.py` decide entre `local_agent`, `codex`, `codex_dry_run`,
  `status` o `blocked`.
- Directivas soportadas: `/status`, `/local`, `/codex`, `/dry`, `/exit`.

Regla operativa:

```text
prompt -> parser -> ActionGate -> auto_router
       -> agente local | Codex CLI read-only | OpenAI Responses | dry-run | BLOCK
```

Evidencia actual:

```powershell
python -m compileall -q wabi_sabi tests
python -m pytest -q
.\wabi.cmd auto "ejecuta diagnostico" --json
.\wabi.cmd auto "analiza el repo y decide que conviene usar" --dry-run --json
$inputText = "/status`n/exit`n"; $inputText | powershell -NoProfile -ExecutionPolicy Bypass -File .\wabi-window.ps1 -Here
$inputText = "/exit`n"; $inputText | .\wabi-window.cmd -Here
.\wabi.cmd auto "responde exactamente WABI_AUTO_CODEX_ROUTED_OK" --json
```

Resultados:

- `python -m pytest -q` -> `33 passed in 2.03s`.
- `auto "ejecuta diagnostico"` -> `route=local_agent`, `agent=debugger`,
  artefacto `debug_diagnostic_20260506-082955.json`.
- `auto "...decide..." --dry-run` -> `route=codex_dry_run`, workpack en
  `runtime/outputs`.
- `wabi-window.ps1 -Here` -> prompt `Wabi-Auto>` responde `/status` y sale con
  `/exit`.
- `wabi-window.cmd -Here` -> arranca `Wabi-Auto>` y sale con `/exit`.
- `auto "responde exactamente WABI_AUTO_CODEX_ROUTED_OK"` -> `route=codex`,
  salida exacta `WABI_AUTO_CODEX_ROUTED_OK`, sandbox `read-only`, sesion
  `ephemeral`, `returncode=0`.

Fallo observado y corregido:

- Una prueba con texto que contenia `CODEX` fue mal clasificada como
  `code_generation` porque el parser por reglas veia el substring `code`.
  Se agrego `codex` como pista explicita de ruta Codex en `auto_router.py`.

## Actualizacion 2026-05-06 - respuesta instantanea y Codex en background

Problema observado:

- En la ventana `wabi auto`, una ruta `codex` bloqueaba el prompt mientras
  `codex exec` arrancaba y esperaba modelo/red. Eso podia dejar al operador sin
  respuesta visible por minutos.
- Diagnostico de procesos: una cadena reciente `powershell -> python -> node ->
  codex` confirmo que la ventana estaba esperando un subprocess de Codex.
- `ollama list` mostro modelos locales disponibles (`qwen2.5:0.5b` y
  `qwen2.5-coder:3b`), pero no habia modelo cargado en `ollama ps`.

Cambio aplicado:

- `wabi auto` interactivo ya no ejecuta Codex en foreground.
- Si el router decide `codex`, crea un job en `runtime/jobs` y devuelve
  control inmediatamente.
- Nuevo `JobStore` en `core/job_queue.py`.
- Nuevo runner `wabi_sabi.cli.job_runner` para ejecutar Codex en background y
  escribir resultado en JSON.
- Nuevos comandos interactivos: `/jobs` y `/result [job_id]`.
- `wabi auto "<pedido>" --background-codex` habilita la misma conducta en modo
  one-shot.

Evidencia actual:

```powershell
python -m compileall -q wabi_sabi tests
python -m pytest -q
.\wabi.cmd auto "responde como Codex exactamente WABI_BACKGROUND_OK" --background-codex --json
$inputText = "responde como Codex exactamente WABI_WINDOW_BACKGROUND_OK`n/jobs`n/exit`n"; $inputText | .\wabi-window.cmd -Here
```

Resultados:

- `python -m pytest -q` -> `36 passed in 5.27s`.
- `--background-codex` devolvio `route=codex_background` en `1804 ms` con job
  `20260506-084323-8b830bc7`; el job termino `done` con salida
  `WABI_BACKGROUND_OK`.
- `wabi-window.cmd -Here` devolvio control en `1654 ms`, mostro
  `route=codex_background`, `/jobs` listo, y el job
  `20260506-084355-1be93cf9` termino `done` con salida
  `WABI_WINDOW_BACKGROUND_OK`.

Lectura operativa:

- La ventana ya no debe quedarse muda esperando Codex.
- Codex profundo sigue disponible, pero desacoplado del prompt.
- La mejora de velocidad real no debe depender de Ollama por defecto; los
  planos locales lo tratan como backend opcional bajo gate.

## Actualizacion 2026-05-06 - orquestador sin Ollama por defecto

Planos revisados:

- `docs/ops/WABI_SABI_QWEN_BLUEPRINT_WORKPACK_2026-05-06.md`.
- `docs/ops/QWEN_BLUEPRINT_LOCAL_INDEX_2026-05-06.md`.
- `docs/ops/WABI_OSIT_BRIDGE_FROM_ESTADO_2026-05-06.md`.
- `docs/ops/OSIT_RESOURCE_OPTIMIZER_RUNTIME_SPEC_2026-05-06.md`.
- `COMMS/agents_state/wabi-sabi-sentido-comun.json`.
- `COMMS/agents_state/claudio-local-autonomy.json`.

Lectura de ingenieria:

- Ollama es backend opcional, no arquitectura.
- `qwen2.5:0.5b` y `qwen2.5-coder:3b` son candidatos bajo gate, no fallback
  automatico mientras host este `JAMMING/BLOCK`.
- El carril seguro actual es OSIT policy-only: `ActionGate`, `WitnessLog`,
  workpacks, evidencia y jobs desacoplados.
- La ruta profunda debe degradar rapido de Codex a `dry-run/workpack` cuando
  Codex tarde, falle o no tenga creditos.

Cambio aplicado:

- `ProviderOrchestrator` usa por defecto `codex,dry-run`.
- `ollama` queda apagado salvo `WABI_ENABLE_OLLAMA=1` o seleccion manual.
- `wabi auto /status` muestra `Ollama: OPCIONAL/APAGADO`.
- El adaptador Codex CLI envia stdin como UTF-8 bytes para evitar el error
  `input is not valid UTF-8`.
- El timeout de Codex CLI mata el arbol de procesos en Windows antes de
  degradar al siguiente proveedor.

Evidencia actual:

```powershell
python -m pytest -q
.\wabi.cmd auto /status --json
.\wabi.cmd auto "/codex ... WABI_UTF8_PLANOS_OK" --background-codex --codex-timeout 1 --json
$inputText = "/status`n/exit`n"; $inputText | .\wabi-window.cmd -Here
ollama ps
```

Resultados:

- `python -m pytest -q` -> `42 passed in 3.88s`.
- `/status` -> `Orden: codex, dry-run`, `Codex CLI: OK`, `Ollama:
  OPCIONAL/APAGADO`.
- Job UTF-8 con acentos y timeout bajo -> `done`, `provider=dry-run`,
  intentos `codex:False:codex_cli_timeout, dry-run:True:codex_bridge_dry_run`.
- `wabi-window.cmd -Here` abre `Wabi-Auto>`, responde `/status` y no precarga
  Ollama.
- `ollama ps` -> sin modelos activos despues de detener el arranque manual de
  prueba.

## Actualizacion 2026-05-06 - carga automatica de planos

Cambio aplicado:

- Nuevo `core/blueprint_policy.py`.
- El orquestador busca automaticamente los planos desde el workspace/runtime
  hasta la raiz `-=L.R.GONZALEZ=-`.
- Calcula SHA256 de cada fuente cargada y extrae senales: `ollama_optional`,
  `ollama_alias_blocked`, `host_block`, `policy_only`,
  `deterministic_no_llm` y `workpack_fallback`.
- `ProviderOrchestrator.status()` ahora incluye `blueprint_policy`.
- `/status` muestra `Planos: OK`, cantidad de fuentes y politica activa.
- Si `WABI_PROVIDER_ORDER` contiene `ollama`, se filtra salvo que exista
  `WABI_ENABLE_OLLAMA=1`.

Fuentes detectadas automaticamente en validacion real:

- `docs/ops/WABI_SABI_QWEN_BLUEPRINT_WORKPACK_2026-05-06.md`.
- `docs/ops/QWEN_BLUEPRINT_LOCAL_INDEX_2026-05-06.md`.
- `docs/ops/WABI_OSIT_BRIDGE_FROM_ESTADO_2026-05-06.md`.
- `docs/ops/OSIT_RESOURCE_OPTIMIZER_RUNTIME_SPEC_2026-05-06.md`.
- `runtime/prompt_master/prompt_master_execution_controller_2026-05-06.json`.
- `COMMS/agents_state/wabi-sabi-sentido-comun.json`.
- `COMMS/agents_state/claudio-local-autonomy.json`.

Evidencia actual:

```powershell
python -m pytest -q
.\wabi.cmd auto /status --json
$env:WABI_PROVIDER_ORDER = 'codex,ollama,dry-run'
.\wabi.cmd auto "/codex prueba politica automatica con demas" --background-codex --codex-timeout 1 --json
```

Resultados:

- `python -m pytest -q` -> `45 passed in 4.68s`.
- `/status` -> `Planos: OK`, `Planos fuentes: 7`, `Orden: codex, dry-run`.
- Job con `WABI_PROVIDER_ORDER=codex,ollama,dry-run` -> resultado `done`,
  `provider=dry-run`, `order=codex,dry-run`, `ollama_enabled=false`,
  `policy_loaded=true`, intentos `codex` y `dry-run` solamente.

## Actualizacion 2026-05-06 - plano de control de entorno y COMMS

Cambio aplicado:

- Nuevo `core/environment.py`.
- Nuevo comando `wabi env-status`.
- Nuevo comando `wabi comms-state`.
- `EnvironmentSnapshot` consolida `pending_review`, host observacionista,
  COMMS, validator y estado de proveedores.
- `CommsBridge` lee `COMMS/agents_state/*.json`, resume gates, handoffs,
  departamentos, rutas permitidas y rutas bloqueadas.
- La version actual es read-only para COMMS: no publica, no hace append a
  outbox/inbox y no cruza ActionGate.
- Bajo host `JAMMING/BLOCK`, `decision.recommended_mode` queda en
  `A0_LOCAL_REVIEW_ONLY`.

Evidencia actual:

```powershell
python -m py_compile wabi_sabi\core\environment.py wabi_sabi\cli\main.py tests\test_environment.py
python -m pytest tests\test_environment.py -q
python -m pytest tests -q
.\wabi.cmd env-status --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd comms-state --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

Resultados:

- Tests focales: `2 passed`.
- Suite completa Wabi-Sabi: `53 passed in 3.25s`.
- `env-status` escribe
  `runtime/outputs/wabi_environment_snapshot_20260506-104933.json`.
- `comms-state` escribe
  `runtime/outputs/wabi_comms_state_20260506-104839.json`.
- Estado real leido: `pending.active_dedup=15`, `host=JAMMING/BLOCK`,
  `COMMS agent_count=12`, `COMMS validator=PASS`.
- Verificacion host no-write posterior: `2026-05-06T16:49:19Z`,
  `JAMMING/BLOCK`, `lambda_sat=0.975`, dominante `r_cpu`.
- Verificacion host no-write final: `2026-05-06T18:37:26Z`,
  `CONTAMINADO/REVIEW`, `lambda_sat=0.938`, dominante `r_cpu`.
- Los eventos quedan en `runtime/logs/wabi_events.jsonl`.

Lectura operativa:

- Wabi-Sabi ya puede responder desde verdad local de entorno y comunicacion
  antes de programar.
- La siguiente pieza tecnica sigue siendo `DecisionLogAdapter`; append COMMS y
  programacion multiarchivo quedan detras de gate, rollback y tests.

## Actualizacion 2026-05-06 - DecisionLogAdapter

Cambio aplicado:

- Nuevo `core/decision_log.py`.
- Nuevo comando `wabi decide`.
- Nuevo comando `wabi decision-log`.
- `decide` consume `EnvironmentSnapshot`, calcula hash del snapshot, crea
  `wabi.decision_record.v0_2`, escribe artefacto JSON, agrega ledger JSONL
  append-only, actualiza `wabi_task_manager.json` compatible con
  `obsai.task_manager.v1` y registra WitnessLog SQLite hash-chain.
- `decision-log` lista registros y TaskManager sin tocar COMMS ni publicar.

Evidencia actual:

```powershell
python -m py_compile wabi_sabi\core\decision_log.py wabi_sabi\cli\main.py tests\test_decision_log.py
python -m pytest tests\test_decision_log.py -q
python -m pytest tests -q
.\wabi.cmd decide "continuar pendientes locales sin cruzar gates" --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd decision-log --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

Resultados:

- Tests focales DecisionLog: `2 passed`.
- Suite completa Wabi-Sabi: `55 passed in 2.95s`.
- Artefacto DecisionRecord:
  `runtime/outputs/wabi_decision_record_20260506-122649.json`.
- Snapshot asociado:
  `runtime/outputs/wabi_environment_snapshot_20260506-122649.json`.
- Ledger append-only:
  `runtime/decision_log/wabi_decisions.jsonl`.
- TaskManager compatible:
  `runtime/decision_log/wabi_task_manager.json`.
- WitnessLog:
  `runtime/decision_log/wabi_decision_witness.sqlite`,
  `witness_verified=true`.
- Record hash:
  `F41DFD0587BC3ECF0F496F2E07E908062401EA7344A5E88FDCA67DF041934FA6`.

Estado real leido por la decision:

- `pending.active_dedup=3`.
- `host=JAMMING/BLOCK`.
- `COMMS agent_count=12`.
- `COMMS validator=PASS`.
- `recommended_mode=A0_LOCAL_REVIEW_ONLY`.

Lectura operativa:

- El pendiente `DecisionLogAdapter` queda implementado en carril local
  read-only.
- Append COMMS opt-in sigue pendiente y bloqueado hasta gate/rollback claro.
- Programacion multiarchivo sigue como workpack `REVIEW`, no escritura directa.

## Actualizacion 2026-05-06 - COMMS append plan

Cambio aplicado:

- Nuevo `core/comms_append.py`.
- Nuevo comando `wabi comms-append-plan`.
- Genera mensaje COMMS compatible con `seto-observation-v1` desde el ultimo
  `DecisionRecord`.
- Valida estructura minima del mensaje localmente.
- No escribe COMMS por defecto.
- Si se usa `--apply`, solo escribe cuando `append_allowed=true`.
- Bajo host `JAMMING/BLOCK`, el plan queda bloqueado y no crea outbox.

Evidencia actual:

```powershell
python -m py_compile wabi_sabi\core\comms_append.py wabi_sabi\core\decision_log.py wabi_sabi\cli\main.py tests\test_decision_log.py
python -m pytest tests\test_decision_log.py -q
python -m pytest tests -q
.\wabi.cmd comms-append-plan --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
python COMMS\tools\validate_seto_comms.py --json
Test-Path C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\COMMS\outbox\wabi-sabi-sentido-comun.jsonl
```

Resultados:

- Tests focales DecisionLog/COMMS plan: `3 passed`.
- Suite completa Wabi-Sabi: `56 passed in 3.29s`.
- Artefacto:
  `runtime/outputs/wabi_comms_append_plan_20260506-123143.json`.
- `append_allowed=false`, `append_performed=false`,
  `action_gate=BLOCK`.
- COMMS validator sigue `PASS`.
- `COMMS/outbox/wabi-sabi-sentido-comun.jsonl` no existe; no se hizo append
  real.

Lectura operativa:

- El pendiente de append COMMS queda preparado como workpack/test.
- El append real sigue bloqueado por host/ActionGate.

## Actualizacion 2026-05-06 - programmer workpack multiarchivo

Cambio aplicado:

- Nuevo `core/programmer_workpack.py`.
- Nuevo comando `wabi programmer-workpack`.
- Genera `wabi.programmer_workpack.v0_1`.
- El modo es `PLAN_ONLY`: no genera parches multiarchivo reales y no llama
  `apply_patch`.
- Bajo host `BLOCK`, `application_gate=BLOCK`, `patches=[]` y quedan
  bloqueados `apply_multi_file_patch`, movimientos destructivos, publicacion y
  mutacion de modelos.

Evidencia actual:

```powershell
python -m py_compile wabi_sabi\core\programmer_workpack.py wabi_sabi\core\comms_append.py wabi_sabi\core\decision_log.py wabi_sabi\cli\main.py tests\test_decision_log.py
python -m pytest tests\test_decision_log.py -q
python -m pytest tests -q
.\wabi.cmd programmer-workpack "preparar programacion multiarchivo como REVIEW sin aplicar" --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

Resultados:

- Tests focales DecisionLog/COMMS plan/Programmer workpack: `4 passed`.
- Suite completa Wabi-Sabi: `57 passed in 3.78s`.
- Artefacto:
  `runtime/outputs/wabi_programmer_workpack_20260506-123540.json`.
- `mode=PLAN_ONLY`, `workpack_gate=REVIEW`, `application_gate=BLOCK`,
  `patches=[]`.
- Workpack hash:
  `6C2D3EDE1D59D003A2AB307A181D5EEB7505DBA3AE5B39AF8D25B7BD21D6FC63`.

Lectura operativa:

- El pendiente de programacion multiarchivo queda convertido en workpack
  verificable, sin aplicar cambios.
- No queda carril local seguro adicional que ejecutar mientras el host siga en
  `REVIEW` por presion de recursos; lo restante es legal/humano o gate externo.

## Actualizacion 2026-05-07 - BASE_MODEL primario y EML research-only

Cambio aplicado:

- `ProviderOrchestrator` usa `ollama,codex,dry-run` cuando el modelo base local
  esta disponible.
- `OllamaBridge` resuelve modelo por `BASE_MODEL`, `WABI_BASE_MODEL`,
  `WABI_OLLAMA_BASE_MODEL` o `qwen2.5-coder:3b`.
- `MODEL_ENDPOINT` se acepta como endpoint local si `MODEL_PROVIDER` es
  `ollama`, `local` o `installed_base_model`.
- Modelos `:cloud`/`-cloud` se filtran por defecto.
- `WABI_DISABLE_BASE_MODEL=1` vuelve al carril sin modelo local.
- `WABI_OLLAMA_PREWARM` queda apagado por defecto; no se deja modelo cargado al
  iniciar.
- EML queda integrado solo como helper `RESEARCH_ONLY`, con `safe_eml`,
  `window_load_eml`, `jamming_margin_eml` y comando `wabi eml`.

Evidencia:

```powershell
python -m wabi_sabi.cli.main auto /status --json
$env:WABI_OLLAMA_KEEP_ALIVE='0'; $env:WABI_OLLAMA_NUM_CTX='256'; @'
from pathlib import Path
from wabi_sabi.core.ollama_bridge import OllamaBridge
bridge = OllamaBridge(runtime_root=Path('runtime'))
print(bridge.generate('Responde solamente: OK', timeout=150, num_predict=4).to_dict())
'@ | python -
ollama ps
python -m wabi_sabi.cli.main eml 0 0 --json
python -m pytest -q
```

Resultados:

- `/status` -> `auto_provider=ollama`, `base_model=qwen2.5-coder:3b`,
  `cloud_models_filtered=4`.
- Smoke real -> `provider=ollama`, `model=qwen2.5-coder:3b`, `output=OK`,
  `fallback_used=false`.
- `ollama ps` posterior -> sin modelos activos.
- `wabi eml 0 0 --json` -> `domain_ok=true`, `value=1.0`,
  `epistemic_status=RESEARCH_ONLY`.
- Suite completa Wabi-Sabi: `64 passed`.

Limite:

- El escaner sigiloso encontrado en PSI queda `BLOCK`; no se integra scanning
  stealth ni evasion de deteccion.

## Actualizacion 2026-05-07 - PatchPlan, SafeExecutor y RollbackStore

Cambio aplicado:

- La escritura local dejo de ser un write directo del agente programador: ahora
  pasa por `PatchPlan -> SafeExecutor -> RollbackStore`.
- Nuevo `core/patch_planner.py`: plan JSON, hash, diff y validacion de target.
- Nuevo `core/safe_executor.py`: aplica planes aprobados, verifica con
  `py_compile` y revierte si falla.
- Nuevo `core/rollback_store.py`: snapshot exacto por `plan_id` y restauracion
  dentro del workspace.
- Nuevo `core/tool_registry.py`: inventario de herramientas locales permitidas
  y patrones bloqueados.

Comandos nuevos:

```powershell
python -m wabi_sabi.cli.main patch-plan "crea una funcion que lea un archivo y resuma sus lineas" --target helpers.py --json
python -m wabi_sabi.cli.main patch-apply "crea una funcion que lea un archivo y resuma sus lineas" --target helpers.py --json
python -m wabi_sabi.cli.main rollback <plan_id> --json
python -m wabi_sabi.cli.main tools --json
```

Evidencia:

- `python -m pytest tests/test_safe_executor.py tests/test_patch_cli.py tests/test_agents.py tests/test_cli.py -q` -> 23 passed.
- `python -m pytest tests/test_safe_executor.py tests/test_patch_cli.py -q` -> 12 passed.
- `python -m pytest tests/test_safe_executor.py tests/test_patch_cli.py tests/test_bridge.py -q` -> 18 passed.
- `python -m pytest tests/test_worktree.py tests/test_patch_cli.py -q` -> 6 passed.
- `python -m pytest tests/test_worktree.py tests/test_auto_router.py -q` -> 13 passed.
- `python -m pytest -q` -> 85 passed in 26.32s.
- `python -m wabi_sabi.cli.main tools --json` -> registry con `rg`,
  `patch_plan`, `safe_execute_patch`, `rollback`, `pytest`.
- `python -m json.tool docs\wabi_task_spec.example.json` -> JSON valido.
- `python -m wabi_sabi.cli.main task-spec-plan docs\wabi_task_spec.example.json --json` -> PatchPlan `APPROVE`, sin aplicar fuente.
- `python -m wabi_sabi.cli.main worktree-status --json` -> branch, commit,
  dirty status, diff stat y nombres de archivo sin contenido.
- `python -m wabi_sabi.cli.main auto /status --json` -> incluye linea
  `Worktree: dirty ... status=N`.
- `python -m pytest tests/test_task_spec_planner.py tests/test_safe_executor.py tests/test_patch_cli.py -q` -> 18 passed.
- `python -m pytest tests/test_task_spec_planner.py -q` -> 6 passed.

Limite:

- El contrato interno ya cubre multiarchivo, comandos de test allowlisted y
  witness local para apply/rollback. `task-spec-plan` / `task-spec-apply`
  exponen multiarchivo desde JSON explicito. Falta dashboard/operator UX.

## Actualizacion 2026-05-07 - Operator status CLI

Cambio aplicado:

- Nuevo `core/operator_panel.py`.
- Nuevo comando `wabi operator-status`.
- Agrega proveedor/modelo base, worktree read-only, registry de herramientas,
  task spec in-memory y witness hash-chain.
- No aplica specs, no escribe codigo fuente y no ejecuta acciones externas.

Evidencia:

- `python -m py_compile wabi_sabi\core\operator_panel.py wabi_sabi\cli\main.py wabi_sabi\core\tool_registry.py tests\test_operator_panel.py` -> PASS.
- `python -m pytest tests/test_operator_panel.py tests/test_patch_cli.py -q` -> 6 passed.
- `python -m pytest tests/test_operator_panel.py tests/test_worktree.py tests/test_patch_cli.py -q` -> 9 passed.
- `python -m wabi_sabi.cli.main operator-status --json` -> `gate=APPROVE`, `auto_provider=ollama`, `base_model=qwen2.5-coder:3b`, task spec `APPROVE`, witness valido.
- `python -m pytest -q` -> 87 passed in 25.44s.

Limite:

- Sigue siendo CLI local. Una UI grafica/browser puede construirse encima, pero
  no es necesaria para operar el carril seguro actual.

## Actualizacion 2026-05-07 - Claim contract DUAT/GEODIA

Cambio aplicado:

- Nuevo `core/claim_contract.py`.
- Nuevo comando `wabi claim-contract`.
- Nuevo ejemplo `docs/wabi_claim_contract.example.json`.
- Evalua `claim`, `claim_level`, `evidence`, `falsifiers` y `risk_flags`.
- Bloquea flags de secretos, privado, stealth/ofensivo, publicacion externa,
  pesos de modelo o destruccion.
- Mantiene claims cientificos/publicos fuertes en `REVIEW`.

Lectura operativa:

- Este es un contrato pequeno extraido del backlog Replit DUAT/GEODIA:
  falsifier/evidence gate antes de integrar tecnologia o claims.
- No se importo el export Replit completo.

## Actualizacion 2026-05-07 - Project scan no destructivo

Cambio aplicado:

- Nuevo `core/project_scan.py`.
- Nuevo comando `wabi project-scan`.
- Detecta gestores, lenguajes, comandos de test/build, Git root, repos
  anidados, configs y entrypoints.
- Omite `.git`, vendors, runtime, builds y rutas privadas.
- No incluye contenido de archivos ni escribe fuente.

Lectura operativa:

- Cierra el backlog del intake: scanner de proyecto local para operar como
  agente de codigo sin pedir al usuario el stack/test runner.

## Actualizacion 2026-05-07 - Test plan read-only

Cambio aplicado:

- Nuevo `core/test_plan.py`.
- Nuevo comando `wabi test-plan`.
- Convierte `project-scan` en comandos de verificacion sugeridos.
- No ejecuta tests ni aplica cambios.
- Si no hay baseline, devuelve `NO_TEST_BASELINE` en `REVIEW`.

Evidencia:

- `python -m py_compile wabi_sabi\core\test_plan.py wabi_sabi\core\project_scan.py wabi_sabi\cli\main.py wabi_sabi\core\tool_registry.py tests\test_test_plan.py` -> PASS.
- `python -m pytest tests/test_test_plan.py tests/test_project_scan.py tests/test_claim_contract.py -q` -> 9 passed.
- `python -m wabi_sabi.cli.main test-plan --json` -> `wabi.test_plan.v1`, `auto_execute=false`, `auto_apply=false`.
- `python -m pytest -q` -> 96 passed in 32.31s.

## Actualizacion 2026-05-07 - Run safe tests

Cambio aplicado:

- Nuevo `core/safe_test_runner.py`.
- Nuevo comando `wabi run-safe-tests`.
- `SafeExecutor` expone `run_allowlisted_test_command` para reutilizar una sola
  politica de comandos permitidos.
- Ejecuta solo comandos de `test-plan` con gate `APPROVE`.
- Registra `wabi.safe_test_run.v1`, `ObservationEnvelope` y witness hash-chain.
- Mantiene `auto_apply=false` y no aplica parches.

Evidencia:

- `python -m py_compile wabi_sabi\core\safe_test_runner.py wabi_sabi\core\safe_executor.py wabi_sabi\cli\main.py wabi_sabi\core\tool_registry.py tests\test_safe_test_runner.py` -> PASS.
- `python -m pytest tests/test_safe_test_runner.py tests/test_test_plan.py tests/test_safe_executor.py -q` -> 14 passed.
- `python -m wabi_sabi.cli.main run-safe-tests --json` -> `wabi.safe_test_run.v1`, `python -m pytest -q`, `99 passed in 46.46s`, witness event `1`.

Evidencia:

- `python -m py_compile wabi_sabi\core\claim_contract.py wabi_sabi\cli\main.py wabi_sabi\core\tool_registry.py tests\test_claim_contract.py` -> PASS.
- `python -m json.tool docs\wabi_claim_contract.example.json` -> PASS.
- `python -m pytest tests/test_claim_contract.py tests/test_operator_panel.py tests/test_patch_cli.py -q` -> 10 passed.
- `python -m wabi_sabi.cli.main claim-contract docs\wabi_claim_contract.example.json --json` -> `gate=APPROVE`.
- `python -m py_compile wabi_sabi\core\project_scan.py wabi_sabi\cli\main.py wabi_sabi\core\tool_registry.py tests\test_project_scan.py` -> PASS.
- `python -m pytest tests/test_project_scan.py tests/test_claim_contract.py tests/test_operator_panel.py -q` -> 8 passed.
- `python -m wabi_sabi.cli.main project-scan --json` -> `wabi.project_scan.v1`, `content_included=false`.
- `python -m pytest -q` -> 93 passed in 28.59s.

## Actualizacion 2026-05-07 - Curador Orden Assistant

Cambio aplicado:

- Nuevo `core/curator_assistant.py`.
- Nuevo comando `wabi curator-assistant` con alias `curador-assistant`,
  `orden-assistant` y `curador-orden`.
- Nuevo contrato general
  `docs/developer/CURADOR_ORDEN_ASSISTANT_2026-05-07.md`.
- Nuevo registro `curator_assistant` en `tool_registry`.
- Produce JSON y Markdown en `runtime/outputs`.
- Registra `ObservationEnvelope` y witness hash-chain.
- Clasifica por metadatos: `CONCURRENT_TRACKED_CHANGE`,
  `UNTRACKED_REVIEW`, `ROOT_LOOSE_REVIEW`, `CACHE_OR_BUILD_REVIEW`,
  `HANDOFF_EVIDENCE`, `RUNTIME_EVIDENCE` y `BOUNDARY_BLOCKED`.

Lectura operativa:

- Es el asistente del curador para mantener orden y ensenar higiene de
  workspace a humanos/agentes.
- Es `dry_run_only`: no borra, no mueve, no stagea, no hace commit, no
  revierte, no publica y no lee contenido de archivos.
- Con agentes concurrentes, los cambios tracked quedan en `REVIEW/KEEP` y los
  no trackeados en `UNKNOWN_REVIEW_REQUIRED`.

Evidencia:

- `python -m py_compile wabi_sabi\core\curator_assistant.py wabi_sabi\cli\main.py wabi_sabi\core\tool_registry.py tests\test_curator_assistant.py` -> PASS.
- `python -m pytest tests/test_curator_assistant.py tests/test_project_scan.py tests/test_worktree.py -q` -> 8 passed in 8.26s.
- `python -m wabi_sabi.cli.main curator-assistant --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-` -> `wabi.curator_assistant_report.v1`, `status_count=164`, `candidate_count=120`, `cleanup_performed=false`, `delete_approved_count=0`, witness event `2`.
- `python -m pytest -q` -> 102 passed in 54.43s.
- `python -m wabi_sabi.cli.main run-safe-tests --json` -> `102 passed in 66.63s`, artefacto `runtime\outputs\safe_test_run_20260506-215935.json`, witness event `3`.

## Actualizacion 2026-05-07 - Curador Fichas

Cambio aplicado:

- Nuevo `core/curator_fichas.py`.
- Nuevo comando `wabi curator-fichas` con alias `curador-fichas`,
  `fichas-curador` y `orden-fichas`.
- Nuevo registro `curator_fichas` en `tool_registry`.
- Toma el ultimo `curator_assistant_report_*.json` o un reporte explicito.
- Convierte candidatos `REVIEW`/`UNKNOWN_REVIEW_REQUIRED` en fichas con
  owner, riesgos, evidencia, blocked actions y proxima accion.
- Omite candidatos `BLOCK`.
- Escribe JSON/Markdown en `runtime/outputs` y copia durable en `docs/intake`
  cuando existe.

Lectura operativa:

- Este pase no limpia fisicamente. Reduce incertidumbre antes de cualquier
  archive/delete candidate.
- Invariante: `cleanup_performed=false` y `delete_approved_count=0`.
- Con otro agente activo, cada ficha queda con owner-agente asignado por carril
  y la limpieza fisica sigue bloqueada hasta handoff/evidencia.
- `owner` no cierra curacion. La ficha queda procesada solo si
  `curation.last_record.actor_type=agent`; si el ultimo registro es humano,
  el estado correcto es `NEEDS_AGENT_PROCESSING` y debe correr otro pase de
  agente.

Evidencia:

- `python -m py_compile wabi_sabi\core\curator_fichas.py wabi_sabi\core\curator_assistant.py wabi_sabi\cli\main.py wabi_sabi\core\tool_registry.py tests\test_curator_fichas.py` -> PASS.
- `python -m pytest tests/test_curator_fichas.py tests/test_curator_assistant.py tests/test_project_scan.py tests/test_worktree.py -q` -> 11 passed in 7.73s.
- `python -m wabi_sabi.cli.main curator-fichas --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-` -> `wabi.curator_fichas.v1`, `ficha_count=12`, `delete_approved_count=0`, `cleanup_performed=false`, workspace doc `docs\intake\CURADOR_ORDEN_FICHAS_2026-05-07.md`, witness event `4`.
- `python -m pytest -q` -> 105 passed in 42.32s.
- `python -m wabi_sabi.cli.main run-safe-tests --json` -> `105 passed in 40.92s`, artefacto `runtime\outputs\safe_test_run_20260506-224832.json`, witness event `5`.
- `python -m wabi_sabi.cli.main curator-fichas --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-` posterior -> 12 fichas con hash SHA256/tamano y `content_printed=false`, witness event `7`.
- `python -m pytest -q` final -> 105 passed in 91.02s.
- `python -m wabi_sabi.cli.main run-safe-tests --json` final -> `105 passed in 104.74s`, artefacto `runtime\outputs\safe_test_run_20260506-225628.json`, witness event `8`.

## Actualizacion 2026-05-07 - Operator status lee safe-test latest

Cambio aplicado:

- `core/operator_panel.py` agrega `latest_safe_tests` desde el ultimo
  `runtime/outputs/safe_test_run_*.json`.
- `operator-status` no reejecuta pruebas; solo resume `status`, conteos
  pass/fail, artifact y witness del ultimo runner seguro.
- La salida humana de `operator-status` muestra la linea `Safe tests`.
- El gate incluye `latest_safe_tests_readable` para llevar a `REVIEW` un
  artefacto corrupto o ilegible.

Lectura operativa:

- El operador puede ver si la evidencia de tests mas reciente existe y si esta
  witness-verified sin gastar otra corrida.
- La proxima corrida de `run-safe-tests` reemplaza naturalmente el artifact
  latest sin tocar fuente ni limpiar fisicamente.

Evidencia:

- `python -m py_compile wabi_sabi\core\operator_panel.py wabi_sabi\cli\main.py tests\test_operator_panel.py` -> PASS.
- `python -m pytest tests/test_operator_panel.py tests/test_safe_test_runner.py tests/test_curator_fichas.py -q` -> 8 passed in 10.84s.
- `python -m wabi_sabi.cli.main operator-status` -> `Safe tests: passed passed=1 failed=0 witness=8` antes de la corrida final.
- `python -m pytest -q` -> 105 passed in 49.06s.
- `python -m wabi_sabi.cli.main run-safe-tests --json` -> `105 passed in 52.11s`, artefacto `runtime\outputs\safe_test_run_20260506-231029.json`, witness event `9`.
- `python -m wabi_sabi.cli.main operator-status --json` -> `latest_safe_tests.status=passed`, `latest_safe_tests.artifact=safe_test_run_20260506-231029.json`, `latest_safe_tests.witness_event_id=9`, `checks.latest_safe_tests_readable=true`.

## Actualizacion 2026-05-07 - Curador agent-last processing rule

Cambio aplicado:

- `core/curator_fichas.py` agrega `curation` por ficha.
- Cada ficha registra `curation.required_last_actor_type=agent`,
  `curation.last_record.actor_type` y `curation.status`.
- `owner` queda como asignacion operativa; no cierra curacion por si mismo.
- Si `curation.last_record.actor_type=human`, el estado es
  `NEEDS_AGENT_PROCESSING`.
- Si `curation.last_record.actor_type=agent`, el estado es `AGENT_PROCESSED`.
- El resumen agrega `agent_processed_count` y `needs_agent_processing_count`.

Lectura operativa:

- La curacion de datos pasa por agente. Si un humano asigna owner o edita una
  ficha, esa intervencion no cuenta como cierre; debe correr otro pase de
  agente para que el ultimo registro vuelva a ser `agent`.
- La copia durable en `docs/intake/CURADOR_ORDEN_FICHAS_2026-05-07.md`
  muestra `Curacion` y `Ultimo registro` por ficha.

Evidencia:

- `python -m py_compile wabi_sabi\core\curator_fichas.py tests\test_curator_fichas.py` -> PASS.
- `python -m pytest tests/test_curator_fichas.py -q` -> 4 passed in 2.50s.
- `python -m wabi_sabi.cli.main curator-fichas --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-` -> `agent_processed_count=12`, `needs_agent_processing_count=0`, witness event `10`.
- `Select-String docs\intake\CURADOR_ORDEN_FICHAS_2026-05-07.md` -> `Agent processed: 12`, `Needs agent processing: 0`, `Ultimo registro: agent:curador_orden_assistant`.
- `python -m pytest tests/test_curator_fichas.py tests/test_curator_assistant.py tests/test_operator_panel.py -q` -> 9 passed in 7.60s.
- `python -m pytest -q` -> 106 passed in 79.03s.
- `python -m wabi_sabi.cli.main run-safe-tests --json` -> 106 passed in 101.42s, artefacto `runtime\outputs\safe_test_run_20260506-232926.json`, witness event `11`.
- `python -m wabi_sabi.cli.main operator-status --json` -> ultimo safe-test `status=passed`, `witness_event_id=11`.

## Actualizacion 2026-05-07 - Curador owner agente por carril

Cambio aplicado:

- `core/curator_fichas.py` agrega `owner_assignment` por ficha.
- Cada ficha recibe `owner` con prefijo `agent:` segun carril: Wabi/Sabi local,
  `docs/developer`, `docs/intake`, runtime/cache o gobierno del workspace.
- `owner_assignment.assigned_by_actor_type=agent` y
  `owner_assignment.status=AGENT_ASSIGNED` son requisitos antes de usar una
  ficha para cualquier archivo/movimiento posterior.
- El resumen agrega `owner_assigned_count` y `unassigned_count`.

Lectura operativa:

- Ya no queda pendiente humano para asignar owner a las 12 fichas iniciales.
- Si un humano reasigna o edita una ficha, debe correr otro pase de agente para
  que tanto `owner_assignment` como `curation` vuelvan a cerrar con registro de
  agente.
- La limpieza fisica sigue en `REVIEW`: no hubo delete, move, stage, commit,
  push ni publicacion.

Evidencia:

- `python -m py_compile wabi_sabi\core\curator_fichas.py tests\test_curator_fichas.py` -> PASS.
- `python -m pytest tests/test_curator_fichas.py -q` -> 5 passed in 3.47s.
- `python -m wabi_sabi.cli.main curator-fichas --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-` -> `owner_assigned_count=12`, `unassigned_count=0`, `agent_processed_count=12`, witness event `12`.
- `python -m pytest tests/test_curator_fichas.py tests/test_curator_assistant.py tests/test_operator_panel.py -q` -> 10 passed in 5.68s.
- `python -m pytest -q` -> 107 passed in 44.70s.
- `python -m wabi_sabi.cli.main run-safe-tests --json` -> 107 passed in 46.29s, artefacto `runtime\outputs\safe_test_run_20260506-234209.json`, witness event `13`.
- `python -m wabi_sabi.cli.main operator-status --json` -> `latest_safe_tests.status=passed`, `witness_event_id=13`, `witness.event_count=13`.
