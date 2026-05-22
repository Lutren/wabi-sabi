# Arquitectura Wabi Sabi Local

## Responsabilidades

```text
wabi_sabi/
  cli/
    main.py      # entrypoint, salida humana/json, modo interactivo
    parser.py    # intencion por reglas locales
    router.py    # registro y seleccion de agentes
  agents/
    base_agent.py
    programmer_agent.py
    debug_agent.py
    research_agent.py
    file_agent.py
  core/
    auto_router.py # decision entre agente local, Codex, dry-run o bloqueo
    blueprint_policy.py # carga planos locales y deriva politica de proveedores
    bridge.py   # puente OSIT: envelope, R, routing, ActionGate, WitnessLog
    comms_append.py # workpack de append COMMS con seto-observation-v1
    codex_bridge.py # puente opcional hacia Codex CLI / OpenAI Responses
    conversational.py # sesion hablar: chat, plan/diff, /apply, rollback
    curator_assistant.py # asistente de orden seco para curador y agentes
    curator_fichas.py # fichas revisables desde reporte seco del curador
    decision_log.py # DecisionLog adapter: TaskManager compatible + WitnessLog
    environment.py # snapshot de entorno y puente COMMS read-only
    provider_orchestrator.py # modelo base local -> Codex -> dry-run
    ollama_bridge.py # BASE_MODEL/MODEL_ENDPOINT sobre Ollama local
    eml.py # helpers EML research-only
    operator_panel.py # panel read-only con provider/worktree/witness/tests
    patch_planner.py # PatchPlan JSON + diff antes de escribir
    safe_executor.py # aplica planes aprobados con verificacion
    rollback_store.py # snapshots exactos para revertir parches
    task_spec_planner.py # spec JSON deterministico hacia PatchPlan multiarchivo
    tool_registry.py # inventario local de herramientas permitidas/bloqueadas
    worktree.py # resumen git read-only sin contenido de archivos
    config.py
    gate.py
    memory.py
    observation.py
    programming.py # generacion Python acotada sobre PatchPlan/SafeExecutor
    programmer_workpack.py # plan multiarchivo REVIEW/PLAN_ONLY
    tools.py
  config/
    agents.json
```

## Flujo

1. El CLI recibe texto en lenguaje natural.
2. `parser.py` clasifica intencion.
3. `gate.py` evalua riesgo local.
4. `router.py` selecciona agente desde `config/agents.json`.
5. El agente ejecuta una accion segura.
6. `memory.py` registra JSONL append-only.
7. La respuesta sale con CERTEZA / INFERENCIA / INCOGNITA.

## Puente OSIT

`core/bridge.py` es la capa bridge-first absorbida desde `ESTADO.txt`. Las
tareas deterministicas no llaman modelos. Cuando se requiere respuesta
profunda, el orquestador usa el modelo base local si esta disponible. El flujo
minimo es:

```text
TaskEnvelope -> ResidueMeter -> ActionGate -> ModelRegistry
             -> RuntimeAdapter -> WitnessLog
```

Modo programador con escritura:

```text
prompt -> parser -> ActionGate -> ProgrammerAgent --apply
       -> PatchPlanner -> SafeExecutor -> RollbackStore
       -> diff/plan/execution -> py_compile -> ObservationEnvelope
```

La escritura esta limitada a archivos `.py` dentro del workspace. Las rutas de
runtime, secretos, vendors, builds, releases, TCG/game bridge y rutas externas
se rechazan antes de escribir.

Los comandos explicitos para esta capa son:

```powershell
.\wabi.cmd patch-plan "pedido" --target helpers.py --json
.\wabi.cmd patch-apply "pedido" --target helpers.py --json
.\wabi.cmd patch-apply "pedido" --target helpers.py --test-command "python -m py_compile helpers.py" --json
.\wabi.cmd rollback <plan_id> --json
.\wabi.cmd tools --json
```

`patch-plan` escribe solo artefactos. `patch-apply` crea snapshot de rollback
antes de tocar el target y revierte automaticamente si la verificacion falla.
`rollback` solo acepta snapshots dentro de `runtime/rollback`. `SafeExecutor`
puede ejecutar comandos de verificacion allowlisted y registra stdout/stderr en
el execution record; la composicion shell queda rechazada antes de ejecutar.
Cada apply y rollback agrega un `ObservationEnvelope` y un evento en
`runtime/witness/wabi_patch_witness.sqlite`, validado con hash-chain.

El contrato interno de `PatchPlan` soporta varias operaciones por plan. La CLI
mantiene un `--target` unico por ahora; las pruebas cubren multiarchivo desde
el API interno.

`core/task_spec_planner.py` expone el carril multiarchivo deterministico:

```text
wabi.task_spec.v1 JSON -> declared changes -> PatchPlan -> SafeExecutor
```

El spec debe vivir dentro del workspace y declarar cada `target` y `content` o
`content_file`. No infiere rutas desde lenguaje natural, no borra archivos y no
soporta moves.

## Film cloud bridge

La arquitectura film coloca a Wabi/Sabi como capa local con estado entre el
operador, la PC y proveedores cloud. El proveedor cloud no recibe autoridad de
ejecucion. Su salida debe ser una propuesta estructurada que Wabi/Sabi valida y
convierte en contratos locales.

```text
prompt humano
  -> project/context scan saneado
  -> ProviderOrchestrator cloud planner/coder/debugger
  -> wabi.cloud_code_proposal.v0_1
  -> redaction + local ActionGate
  -> TaskSpec/PatchPlan
  -> SafeExecutor
  -> py_compile/tests allowlisted
  -> RollbackStore + WitnessLog + handoff
```

Responsabilidades:

- NVIDIA NIM / cloud: plan, codigo propuesto, debug strategy y riesgos.
- Wabi local: redaccion, gate final, path boundary, apply, tests, rollback,
  witness y handoff.
- DUAT/Wabi UI: cockpit read-only/operativo para provider, gates, plan, diff,
  tests, rollback y evidencia.

El gate cloud se separa en estados: `configured`, `enabled`, `live_pass`,
`quota_failed` y `fallback_used`. Un proveedor configurado no equivale a
permiso de llamada live ni a exito de cuota. Si la llamada falla por auth,
cuota, rate limit o modelo, el flujo debe caer a Qwen local, Codex read-only o
dry-run/workpack.

El contrato offline v0.1 usa:

```text
wabi.cloud_code_proposal.v0_1
  -> validate/redact
  -> wabi.task_spec.v1 artifact
  -> PatchPlan/diff
  -> task-spec-apply only as a separate local-gated step
```

Comandos:

```powershell
.\wabi.cmd cloud-proposal-validate docs\wabi_cloud_code_proposal.example.json --json
.\wabi.cmd cloud-proposal-task-spec docs\wabi_cloud_code_proposal.example.json --json
.\wabi.cmd cloud-proposal-plan docs\wabi_cloud_code_proposal.example.json --json
.\wabi.cmd cloud-proposal-from-provider "crear helper seguro" --dry-run --json
.\wabi.cmd cloud-proposal-from-provider-plan "crear helper seguro" --dry-run --json
```

El provider-gated v0.2 agrega:

```text
intent -> project metadata scan -> strict JSON cloud prompt
      -> provider response artifact (redacted)
      -> extracted cloud proposal artifact
      -> local validation -> optional TaskSpec/PatchPlan
```

`--dry-run` usa fixture local y mantiene `cloud_provider_called=false`. El modo
provider real sigue condicionado por `WABI_ALLOW_CLOUD_PROVIDERS`, credenciales
en entorno/vault y ActionGate; si el provider no devuelve JSON valido, el flujo
queda en `REVIEW` y no hay apply.

Rutas de host control global, overlay siempre activo, teclado/mouse y UI
Automation quedan en REVIEW hasta existir adaptadores locales allowlisted,
tests y rollback. El primer film soportado es el cockpit `hablar` y paneles
DUAT/Wabi de solo lectura sobre evidencia real.

## Git/worktree read-only

`core/worktree.py` agrega introspeccion segura del arbol:

```text
git rev-parse/status/diff --stat/diff --name-only/ls-files --others
```

El comando CLI `worktree-status` no hace stage, commit, checkout ni reset. Solo
devuelve metadatos, nombres de archivo y diff stat; no lee contenido de
archivos.

## Operator panel

`core/operator_panel.py` agrega las superficies verificadas en un estado de
operador:

```text
ProviderOrchestrator.status
  + git_worktree_summary
  + tool_registry_payload
  + task spec plan in-memory
  + WitnessLog.verify_chain
  + latest safe_test_run_*.json
  -> wabi.operator_panel.v1
```

El comando `operator-status` es solo lectura. Valida el task spec sin aplicar
parches, resume witness sin modificar el hash-chain y muestra la ultima
verificacion `run-safe-tests` sin reejecutarla.

## Claim contract

`core/claim_contract.py` es el contrato pequeno extraido del carril
DUAT/GEODIA/falsifier sin importar el export Replit:

```text
wabi.claim_contract.v1
  -> evidence + falsifiers + risk_flags
  -> wabi.claim_contract_evaluation.v1
```

El contrato no intenta probar claims cientificos. Los mantiene en `REVIEW` y
bloquea flags de secretos, privado, stealth, ofensivo, publicacion externa,
pesos de modelo o destruccion.

## Project scan

`core/project_scan.py` cubre el scanner no destructivo del intake PSI:

```text
workspace filenames + package.json scripts + git metadata
  -> wabi.project_scan.v1
```

Detecta gestores, lenguajes, comandos de test y fronteras repo. Omite carpetas
denegadas y no incluye contenido de archivos para evitar secretos.

`core/test_plan.py` convierte esa salida en `wabi.test_plan.v1`:

```text
wabi.project_scan.v1 -> suggested verification commands
```

El plan no ejecuta comandos ni aplica cambios; solo deja la ruta segura para un
executor allowlisted.

`core/safe_test_runner.py` ejecuta ese plan solo cuando los comandos pasan por
la misma allowlist usada por `SafeExecutor`:

```text
wabi.test_plan.v1 -> run_allowlisted_test_command -> wabi.safe_test_run.v1
```

La ejecucion registra artefacto JSON, `ObservationEnvelope` y witness
hash-chain. No aplica parches.

## Curador Orden Assistant

`core/curator_assistant.py` convierte el contrato Curador SETO en una
herramienta local de orden para sesiones con varios agentes:

```text
git metadata + project_scan metadata
  -> wabi.curator_assistant_report.v1
  -> JSON + Markdown + ObservationEnvelope + WitnessLog
```

El comando CLI es:

```powershell
.\wabi.cmd curator-assistant --json
```

La salida clasifica metadatos de worktree en categorias operativas:

- `CONCURRENT_TRACKED_CHANGE`: no revertir ni sobrescribir;
- `UNTRACKED_REVIEW`: crear ficha/owner antes de mover o stagear;
- `CACHE_OR_BUILD_REVIEW`: posible limpieza futura, todavia `REVIEW`;
- `HANDOFF_EVIDENCE`: conservar briefs, fingerprints y reportes;
- `RUNTIME_EVIDENCE`: conservar evidencia salvo politica de retencion;
- `BOUNDARY_BLOCKED`: secretos, privado, pagos o game/TCG.

El asistente no lee contenido de archivos, no borra, no mueve, no usa
`git add`, no hace commit, no revierte y no publica. Su responsabilidad es
ensenar higiene de workspace y dejar candidatos verificables para un pase de
curadoria posterior.

`core/curator_fichas.py` toma ese reporte y lo transforma en fichas:

```text
wabi.curator_assistant_report.v1
  -> REVIEW/UNKNOWN candidates
  -> wabi.curator_fichas.v1
  -> runtime JSON/Markdown + optional docs/intake copy + WitnessLog
```

Las fichas tienen `owner` asignado por agente segun carril (`wabi-sabi`,
`docs/developer`, `docs/intake`, evidencia runtime/cache o gobierno del
workspace), evidencia de que no se leyo contenido, acciones bloqueadas y
proxima accion segura. No aprueban borrado: `delete_approved_count` queda
siempre en `0`.

`owner` y procesamiento son campos distintos. La curacion queda procesada solo
cuando `curation.last_record.actor_type=agent`; si el ultimo registro es
`human`, el estado debe ser `NEEDS_AGENT_PROCESSING`. Esto evita confundir una
asignacion manual con cierre operativo: despues de una intervencion humana,
otro pase de agente debe dejar el ultimo registro como `AGENT_PROCESSED`.
La asignacion de owner tambien debe quedar registrada por agente:
`owner_assignment.assigned_by_actor_type=agent` y
`owner_assignment.status=AGENT_ASSIGNED`.

## Puente Codex

`core/codex_bridge.py` permite hablar con Codex desde Wabi-Sabi sin convertir
el CLI local en un agente externo sin control:

```text
prompt -> ActionGate -> provider auto
       -> base-model/ollama | codex-cli read-only | openai-responses | dry-run workpack
       -> runtime/logs/wabi_events.jsonl
```

Proveedor `auto`:

1. `ollama` con `BASE_MODEL` o `qwen2.5-coder:3b` si el modelo base local esta instalado.
2. `codex-cli` si `codex` esta instalado.
3. `openai-responses` si existe `OPENAI_API_KEY`.
4. `dry-run` si no hay proveedor ejecutable.

El adaptador `codex-cli` ejecuta:

```text
codex --ask-for-approval never exec --sandbox read-only --skip-git-repo-check --ephemeral
```

Esto permite conversar o pedir analisis desde Wabi-Sabi, pero no aplica cambios
por si solo. Los cambios locales siguen pasando por `--apply` o por un gate
humano/ActionGate posterior.

## Modo Auto y ventana persistente

`wabi auto` agrega una capa de decision para uso diario:

```text
prompt -> parser -> ActionGate -> auto_router
       -> local_agent | codex_bridge | codex_dry_run | BLOCK
```

Rutas:

- `local_agent`: diagnosticos, operaciones de archivo y codigo simple;
- `codex`: analisis amplio, decisiones, organizacion, priorizacion o tareas
  ambiguas cuando hay proveedor disponible;
- `codex_dry_run`: workpack local cuando se pide `--dry-run` o no hay proveedor;
- `blocked`: fronteras de publicacion, secretos o borrado destructivo.

`wabi-window.cmd` abre una PowerShell visible y ejecuta `wabi hablar --cloud`
para dejar una ventana persistente tipo consola conversacional.

`wabi hablar` agrega una capa tipo Codex/Claude Code:

```text
Tyr> prompt
  -> ConversationSession
  -> ActionGate + boundary local
  -> local_chat | provider_orchestrator | PatchPlan
  -> /apply explicito -> SafeExecutor -> RollbackStore -> WitnessLog
```

La sesion conserva contexto reciente en memoria JSONL, puede usar cloud solo si
esta habilitado en el proceso, y baja a Codex/Ollama/dry-run si el provider
falla. Para programar, genera plan/diff primero; `/apply` es la unica ruta que
toca el arbol fuente.

En modo interactivo, las rutas `codex` no bloquean el prompt:

```text
codex route -> JobStore(runtime/jobs) -> job_runner subprocess
            -> provider_orchestrator -> ollama_bridge | codex_bridge | dry-run workpack
            -> job result JSON
```

La ventana responde con un `job_id` y permite consultar `/jobs` o
`/result <job_id>`. Esto evita el problema de esperar varios minutos mientras
`codex exec` arranca o espera red/modelo.

La cadena por defecto efectiva es:

```text
ollama -> codex-cli/openai-responses -> dry-run workpack
```

Ollama/Qwen queda como backend primario solo para el modelo base instalado. Los planos locales
`WABI_SABI_QWEN_BLUEPRINT_WORKPACK_2026-05-06.md`,
`QWEN_BLUEPRINT_LOCAL_INDEX_2026-05-06.md` y
`OSIT_RESOURCE_OPTIMIZER_RUNTIME_SPEC_2026-05-06.md` indican que bajo host
`BLOCK` no se crean aliases, no se corren benchmarks pesados ni se mutan
pesos. Por eso Wabi-Sabi no precarga Ollama, no usa modelos cloud por defecto y
solo llama el modelo base como proveedor normal de respuesta.

`core/blueprint_policy.py` busca automaticamente estos planos desde el
workspace o el runtime hasta encontrar la raiz `-=L.R.GONZALEZ=-`. Calcula
SHA256, extrae senales operativas y entrega una politica al
`ProviderOrchestrator`:

```text
blueprints -> signals -> provider_order=ollama,codex,dry-run si base local existe
                       -> ollama_enabled_by_default=false
                       -> prewarm_ollama=false
```

El modelo base se resuelve por `BASE_MODEL`, `WABI_BASE_MODEL`,
`WABI_OLLAMA_BASE_MODEL` o `qwen2.5-coder:3b`. Para volver al modo sin modelo
local, usar `WABI_DISABLE_BASE_MODEL=1`.

## Plano de control de entorno

`core/environment.py` convierte Wabi-Sabi en punto de decision operacional sin
crear daemons ni depender de modelos pesados:

```text
workspace/runtime -> find_portfolio_root
                  -> pending_review_latest
                  -> host_observacionista/latest_report
                  -> COMMS agents_state + validator
                  -> ProviderOrchestrator.status
                  -> EnvironmentSnapshot JSON
```

Comandos:

```powershell
.\wabi.cmd env-status --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd comms-state --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

`env-status` escribe `wabi_environment_snapshot_*.json` y registra evento
append-only en `runtime/logs/wabi_events.jsonl`. El snapshot contiene
`pending`, `host`, `comms`, `providers`, `programming_lane` y
`decision.recommended_mode`.

`CommsBridge` es read-only en esta version: lee `COMMS/agents_state/*.json`,
resume `action_gate`, `status`, `department`, `may_touch`,
`must_not_touch_without_handoff`, `allowed_actions` y `blocked_actions`, y corre
`COMMS/tools/validate_seto_comms.py --json` si existe. No escribe mensajes COMMS
ni ejecuta acciones externas.

## DecisionLog adapter

`core/decision_log.py` toma el snapshot de entorno y lo vuelve una decision
auditable:

```text
EnvironmentSnapshot -> snapshot_hash -> DecisionRecord
                    -> runtime/decision_log/wabi_decisions.jsonl
                    -> runtime/decision_log/wabi_task_manager.json
                    -> WitnessLog SQLite hash-chain
```

Comandos:

```powershell
.\wabi.cmd decide "continuar pendientes locales sin cruzar gates" --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd decision-log --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

El `TaskManager` usa schema `obsai.task_manager.v1` para que el runtime pueda
consumir decisiones sin depender de chat. El ledger JSONL es append-only y el
WitnessLog SQLite valida hash-chain con `verify_chain()`.

En host `BLOCK`, una decision se registra como `BLOCKED/P1`, con acciones
externas, modelos pesados, aliases y movimientos destructivos bloqueados. Eso no
cierra pendientes por inferencia; solo deja evidencia consultable para el
siguiente ciclo.

## COMMS append plan

`core/comms_append.py` implementa el paso previo al append real:

```text
DecisionRecord -> seto-observation-v1 message
               -> validation local
               -> wabi_comms_append_plan_*.json
               -> append only if --apply and append_allowed=true
```

Comando:

```powershell
.\wabi.cmd comms-append-plan --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

Bajo host `BLOCK`, el plan queda con `action_gate=BLOCK`,
`append_allowed=false` y `append_performed=false`. No crea
`COMMS/outbox/wabi-sabi-sentido-comun.jsonl`; solo produce un artefacto de
revision.

## Programmer workpack

`core/programmer_workpack.py` cierra el carril multiarchivo sin aplicar cambios:

```text
EnvironmentSnapshot -> ProgrammerWorkpack PLAN_ONLY
                    -> application_gate BLOCK|REVIEW
                    -> wabi_programmer_workpack_*.json
```

Comando:

```powershell
.\wabi.cmd programmer-workpack "preparar programacion multiarchivo como REVIEW sin aplicar" --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

El workpack declara `allowed_now`, `blocked_now`, `required_before_apply`,
`falsifiers`, `tests`, `proposed_files` y `patches`. Bajo host `BLOCK`, queda
`application_gate=BLOCK`, `patches=[]` y no llama a `apply_patch`.

Reglas actuales:

- tareas deterministicas usan `deterministic_no_llm`;
- triage/modelos Qwen son recomendaciones `ollama_optional`, no runtime por
  defecto;
- tareas tecnicas/codigo pueden recomendar `qwen2.5-coder:3b` solo como carril
  opcional/manual;
- publicacion, secretos, acciones externas, borrado destructivo, aliases,
  descargas, LoRA o fine-tuning quedan en `BLOCK`;
- `WitnessLog` usa SQLite con hash-chain y `verify_chain()`.

## Contrato de agente

Cada agente declara:

- nombre
- descripcion
- capacidades
- limites
- entrypoint
- `safe_mode`

Entrada: `AgentInput(prompt, parsed, options)`.

Salida: `AgentResult` con `ok`, `action`, `output`, `artifacts`, `evidence`,
`certainty`, `inference`, `unknown` y `error`.

## Extension

1. Crear un nuevo archivo en `wabi_sabi/agents`.
2. Heredar de `BaseAgent`.
3. Agregar entrypoint y capacidades en `wabi_sabi/config/agents.json`.
4. Agregar ruta de intencion si corresponde.
5. Crear test focal en `tests/`.

## BrowserBridge

`core/browser_bridge.py` separa backend, catalogo de servicios, gate de envio y
validacion local de propuestas.

```text
browser-bridge status
  -> backends: dry-run, chrome-devtools-mcp, kimi-webbridge, hermes
  -> no install, no launch, no external call by default

browser-bridge ai-consult <service> <prompt>
  -> redact prompt
  -> write review artifact
  -> send only if --send + WABI_ALLOW_BROWSER_SEND=1 + available proven adapter
  -> response remains proposal-only

browser-bridge council <prompt>
  -> prepare allowlisted service requests
  -> live only for proven adapter candidates
  -> no execution permission
```

`chrome-devtools-mcp` es el backend primario para lectura/snapshot/extract/
screenshot cuando el operador ya tiene la herramienta local disponible. Wabi
solo detecta disponibilidad; no instala dependencias ni ejecuta `npx` por si
mismo. `kimi-webbridge` es el primer candidato live, condicionado a
`WABI_KIMI_WEBBRIDGE_URL`, `WABI_ALLOW_BROWSER_BRIDGE=1`, `--send` y
`WABI_ALLOW_BROWSER_SEND=1`. Hermes queda como adapter opcional sin `--yolo`.

Las respuestas con codigo pasan por `wabi.cloud_code_proposal.v0_1` y
`validate_cloud_code_proposal`. TaskSpec, PatchPlan y apply siguen en carriles
separados y gateados.
