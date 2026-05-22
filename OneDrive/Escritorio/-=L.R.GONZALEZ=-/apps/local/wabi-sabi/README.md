# Wabi Sabi Local Agents

CLI local-first para hablar con Wabi Sabi y enrutar tareas simples hacia
agentes verificables. No requiere nube ni claves. Si no hay proveedor profundo,
usa fallback determinista basado en reglas, workpacks, artefactos y logs.

## Ruta canonica

La unica ruta de proyecto Wabi-Sabi en este workspace es
`apps/local/wabi-sabi`. Los archivos externos de `scripts/`, `config/`,
`COMMS/`, `docs/ops`, `docs/intake`, `MEDIOEVO_LIVE_TREE` y
`publish_staging` son hooks, fichas, staging o referencias gobernadas desde:

- `docs/WABI_SABI_CANONICAL_ROUTE_2026-05-16.md`
- `docs/WABI_SABI_ABSORPTION_MANIFEST_2026-05-16.md`

No se debe crear otro arbol activo para Wabi-Sabi.

## Film local + cloud bridge

Wabi/Sabi tambien queda documentado como capa film local entre el operador, la
PC y proveedores cloud. En ese modo, la nube no controla la maquina: NVIDIA NIM
u otro proveedor OpenAI-compatible puede planear, proponer codigo y ayudar a
debuggear, pero Wabi/Sabi local conserva el gate final, la escritura, los
tests, el rollback y la evidencia.

Contrato minimo:

```text
operador -> Wabi/Sabi local -> contexto saneado -> proveedor cloud
         -> propuesta estructurada -> ActionGate local
         -> TaskSpec/PatchPlan -> SafeExecutor -> tests/rollback/WitnessLog
```

La implementacion debe reutilizar `ProviderOrchestrator`, `ActionGate`,
`PatchPlan`, `TaskSpec`, `SafeExecutor`, `RollbackStore` y `WitnessLog`. No se
debe crear otro cerebro Wabi ni otro arbol activo. Las llamadas cloud siguen
bloqueadas hasta `WABI_ALLOW_CLOUD_PROVIDERS=1`, credenciales en entorno/vault
y aprobacion de gates.

Flujo offline v0.1:

```powershell
.\wabi.cmd cloud-proposal-validate docs\wabi_cloud_code_proposal.example.json --json
.\wabi.cmd cloud-proposal-task-spec docs\wabi_cloud_code_proposal.example.json --json
.\wabi.cmd cloud-proposal-plan docs\wabi_cloud_code_proposal.example.json --json
```

Estos comandos no llaman proveedores cloud ni aplican codigo fuente. Para
aplicar un spec generado, usar despues `task-spec-apply <spec.json>` bajo el
gate local normal.

Flujo provider-gated v0.2:

```powershell
.\wabi.cmd cloud-proposal-from-provider "crear helper seguro" --dry-run --json
.\wabi.cmd cloud-proposal-from-provider-plan "crear helper seguro" --dry-run --json
.\wabi.cmd cloud-proposal-from-provider "crear helper seguro" --codex-provider nvidia --json
```

`--dry-run` genera una propuesta local compatible con el contrato sin llamar
red. Sin `--dry-run`, Wabi/Sabi construye un prompt JSON estricto para el
proveedor seleccionado, guarda la respuesta redactada y acepta solo un objeto
`wabi.cloud_code_proposal.v0_1` que luego vuelve a pasar por validacion local.
Si `WABI_ALLOW_CLOUD_PROVIDERS` o la clave no estan configurados, el adaptador
no llama red y el resultado queda en `REVIEW`/fallback.

Build-assist temporal:

```powershell
.\wabi.cmd build-assist-status --json
.\wabi.cmd build-assist-plan "crear helper seguro" --dry-run --json
.\wabi.cmd build-assist-smoke --provider nvidia --model nano-30b --json
$env:WABI_BUILD_ASSIST_CLOUD='1'; $env:WABI_ALLOW_CLOUD_PROVIDERS='1'; .\wabi.cmd build-assist-plan "crear helper seguro" --codex-provider nano-30b --json
```

`build-assist-plan` usa `nano-30b` como default de supervivencia y fuerza
dry-run si no estan activadas las dos banderas. La salida sigue siendo
proposal-only: primero `wabi.cloud_code_proposal.v0_1`, luego validacion local,
TaskSpec/PatchPlan y solo despues apply local con rollback/tests si el operador
lo pide. `build-assist-smoke` valida la ruta NVIDIA con prompt sintetico y no
aplica fuentes. Documento: `docs/WABI_BUILD_ASSIST_CLOUD_2026-05-19.md`.

Documento de insight: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\04_WABI_SABI\docs\WABI_SABI_FILM_CLOUD_BRIDGE_INSIGHTS_2026-05-18.md`.

## Uso rapido

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
.\wabi.cmd "crea una funcion que lea un archivo y resuma sus lineas"
.\wabi.cmd "ejecuta diagnostico"
.\wabi.cmd "crea una funcion que lea un archivo y resuma sus lineas" --apply --target helpers.py
.\wabi.cmd patch-plan "crea una funcion que lea un archivo y resuma sus lineas" --target helpers.py --json
.\wabi.cmd patch-apply "crea una funcion que lea un archivo y resuma sus lineas" --target helpers.py --json
.\wabi.cmd patch-apply "crea una funcion que lea un archivo y resuma sus lineas" --target helpers.py --test-command "python -m py_compile helpers.py" --json
.\wabi.cmd rollback <plan_id> --json
.\wabi.cmd tools --json
.\wabi.cmd worktree-status --json
.\wabi.cmd operator-status --json
.\wabi.cmd multimodal status --json
.\wabi.cmd multimodal smoke-camera --json
.\wabi.cmd multimodal smoke-mic --seconds 2 --json
.\wabi.cmd multimodal observe --seconds 10 --local-only --json
.\wabi.cmd claim-contract docs\wabi_claim_contract.example.json --json
.\wabi.cmd hypothesis "el motor solo debe apoyar claims con falsadores y evidencia" --json
.\wabi.cmd project-scan --json
.\wabi.cmd test-plan --json
.\wabi.cmd run-safe-tests --json
.\wabi.cmd curator-assistant --json
.\wabi.cmd curator-fichas --json
.\wabi.cmd task-spec-plan wabi_task_spec.json --json
.\wabi.cmd task-spec-apply wabi_task_spec.json --json
.\wabi.cmd cloud-proposal-validate docs\wabi_cloud_code_proposal.example.json --json
.\wabi.cmd cloud-proposal-task-spec docs\wabi_cloud_code_proposal.example.json --json
.\wabi.cmd cloud-proposal-plan docs\wabi_cloud_code_proposal.example.json --json
.\wabi.cmd cloud-proposal-from-provider "crear helper seguro" --dry-run --json
.\wabi.cmd cloud-proposal-from-provider-plan "crear helper seguro" --dry-run --json
.\wabi.cmd build-assist-status --json
.\wabi.cmd build-assist-plan "crear helper seguro" --dry-run --json
.\wabi.cmd build-assist-smoke --provider nvidia --model nano-30b --json
.\wabi.cmd
.\wabi-window.cmd
.\wabi.cmd hablar
.\wabi.cmd hablar "estas ahi?"
.\wabi.cmd hablar "crea una funcion que lea un archivo y resuma sus lineas en helpers.py"
.\wabi.cmd auto
.\wabi.cmd auto "analiza esto y decide que conviene usar"
.\wabi.cmd chat "hola wabi, resume el estado local"
.\wabi.cmd codex-status
.\wabi.cmd provider-status --json
.\wabi.cmd codex "responde como Codex desde Wabi-Sabi: que pruebas debo correr?"
.\wabi.cmd codex "genera workpack sin llamar modelo" --dry-run
.\wabi.cmd bridge-plan "clasifica pendientes y genera resumen"
.\wabi.cmd env-status --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd comms-state --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd decide "continuar pendientes locales sin cruzar gates" --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd decision-log --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd comms-append-plan --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd programmer-workpack "preparar programacion multiarchivo como REVIEW sin aplicar" --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd eml 0 0 --json
.\wabi.cmd agents
.\wabi.cmd e2e-smoke
```

## Instalacion editable opcional

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
python -m pip install -e . --no-deps --no-build-isolation
wabi "crea un README para este modulo"
```

## Seguridad

- No hace push, deploy, publicacion, compras, borrados destructivos ni uso de
  secretos.
- Las escrituras automaticas van a `runtime/outputs` y los logs a
  `runtime/logs`.
- `wabi-window.cmd` abre una ventana PowerShell persistente en modo `hablar`
  conversacional: responde como chat, puede razonar con provider cloud/Codex/
  Ollama y solo escribe codigo cuando confirmas con `/apply`.
- `wabi hablar` es el modo recomendado para usarlo como Codex/Claude Code por
  CLI. Comandos: `/status`, `/providers`, `/memory`, `/plan`, `/diff`,
  `/apply`, `/rollback` y `/exit`.
- `wabi auto` decide entre agente local, modelo base local, Codex CLI,
  OpenAI Responses o dry-run segun el pedido, proveedor disponible y
  ActionGate.
- Si el modelo base instalado esta disponible, la ruta profunda primaria es
  Ollama con `qwen2.5-coder:3b` por defecto. `BASE_MODEL`,
  `WABI_BASE_MODEL` o `WABI_OLLAMA_BASE_MODEL` pueden cambiarlo.
- Los modelos `:cloud`/`-cloud` quedan filtrados salvo
  `WABI_ALLOW_CLOUD_MODELS=1`.
- `provider-status` muestra Ollama, Codex CLI, OpenAI Responses y adapters
  cloud sin imprimir secretos. NVIDIA NIM y Qwen cloud existen como adapters
  mockeables, pero no llaman red salvo `WABI_ALLOW_CLOUD_PROVIDERS=1`.
- `provider-status --json` tambien expone el catalogo seguro de modelos cloud
  configurados para programar. NVIDIA NIM acepta aliases
  `ultra`, `llama-70b`, `super`, `nano-30b` y `nano-9b` por
  `WABI_NVIDIA_NIM_MODEL_ALIAS`. Qwen cloud acepta `qwen-plus` y
  `qwen-235b` por `WABI_QWEN_MODEL_ALIAS`.
- La seleccion exacta tambien puede fijarse con `WABI_NVIDIA_NIM_MODEL` o
  `WABI_QWEN_MODEL`. La red sigue bloqueada hasta definir
  `WABI_ALLOW_CLOUD_PROVIDERS=1` y pasar ActionGate; las claves deben vivir en
  el entorno/vault, nunca en docs ni logs.
- `chat` conserva la conversacion local simple; `hablar` es la sesion
  conversacional programadora con plan primero y `/apply` explicito.
- `WABI_DISABLE_BASE_MODEL=1` vuelve al modo `codex,dry-run`.
- Al arrancar, el orquestador carga automaticamente los planos locales de
  `docs/ops`, `runtime/prompt_master` y `COMMS/agents_state`; `/status` muestra
  si los encontro y que politica activaron.
- `env-status` genera un `EnvironmentSnapshot` local en `runtime/outputs`:
  lee `pending_review`, host observacionista, COMMS, validator y proveedores.
- `comms-state` lee `COMMS/agents_state/*.json`, resume gates/handoffs y corre
  el validator sin publicar ni escribir mensajes externos.
- `decide` registra una decision local con `EnvironmentSnapshot`,
  `TaskManager` compatible y `WitnessLog` SQLite hash-chain.
- `decision-log` lista el ledger append-only y el estado
  `runtime/decision_log/wabi_task_manager.json`.
- `comms-append-plan` genera el mensaje COMMS con
  `seto-observation-v1` como workpack; bajo host `BLOCK` no escribe outbox.
- `programmer-workpack` genera el plan de programacion multiarchivo en
  `PLAN_ONLY`; bajo host `BLOCK` no aplica parches.
- `wabi codex` ejecuta Codex CLI en modo `read-only` cuando esta instalado. Si
  no existe CLI, puede usar OpenAI Responses API con `OPENAI_API_KEY`; sin
  proveedor disponible genera un workpack local con `--dry-run`.
- El modo `--apply --target <archivo.py>` y `patch-apply` escriben codigo
  Python dentro del workspace mediante `PatchPlan -> SafeExecutor ->
  RollbackStore`: dejan plan JSON, diff, snapshot de rollback, execution record
  y `py_compile`.
- `patch-plan` genera el plan/diff sin tocar codigo fuente.
- `rollback <plan_id>` restaura exactamente un snapshot creado por Wabi/Sabi.
- `--test-command` acepta verificaciones locales allowlisted como
  `python -m pytest ...` o `python -m py_compile ...`; si fallan, el executor
  revierte el plan.
- Apply y rollback quedan registrados con `ObservationEnvelope` y witness
  SQLite hash-chain en `runtime/witness`.
- `tools` expone el registro local de herramientas permitidas y patrones
  bloqueados.
- `worktree-status` resume git en modo solo lectura: branch, commit,
  status/diff por nombres y sin contenido de archivos.
- `operator-status` agrega proveedor, modelo base, worktree, registry,
  task spec, witness y el ultimo `run-safe-tests` en un panel CLI de solo
  lectura.
- `multimodal status` verifica librerias, dispositivos Windows PnP y el puente
  BRAIN_OS disponible. `smoke-camera`, `smoke-mic` y `observe` capturan solo
  metadatos locales de camara/microfono, generan artefactos JSON en
  `runtime/outputs` y registran `WitnessLog`; no guardan imagen/audio crudo y
  no llaman cloud por defecto.
- El modo multimodal cloud queda en `REVIEW`: `--cloud` no envia media ni llama
  proveedores hasta que exista un camino revisado y explicito. La transcripcion
  local tambien queda apagada por defecto y requiere
  `WABI_ENABLE_LOCAL_TRANSCRIPTION=1`.
- `claim-contract` evalua claims con evidencia/falsadores para mantener ideas
  DUAT/GEODIA en carriles verificables antes de integrarlas o publicarlas.
- `project-scan` detecta stack, gestores, comandos de test y fronteras Git sin
  incluir contenido de archivos ni escribir fuente.
- `test-plan` convierte `project-scan` en comandos de verificacion sugeridos,
  sin ejecutarlos ni aplicar cambios.
- `run-safe-tests` ejecuta solo comandos allowlisted desde `test-plan` y
  registra artefacto + witness; mantiene `auto_apply=false`.
- `curator-assistant` genera un reporte seco de orden para el curador:
  clasifica candidatos por metadatos, ensena reglas anti-desorden y no borra,
  mueve, stagea ni revierte archivos.
- `curator-fichas` toma el reporte seco mas reciente y crea fichas revisables
  para candidatos ambiguos; mantiene `delete_approved_count=0`.
- `task-spec-plan` y `task-spec-apply` construyen/aplican PatchPlan
  multiarchivo desde un JSON explicito `wabi.task_spec.v1`.
- `docs/wabi_task_spec.example.json` queda como plantilla operativa minima.
- `cloud-proposal-from-provider` prepara el prompt estructurado para NVIDIA/
  Qwen/etc., extrae solo JSON valido, redacta la respuesta y escribe la
  propuesta en `runtime/outputs/cloud_proposals`; `cloud-proposal-from-provider-plan`
  llega hasta PatchPlan sin tocar fuentes.
- `browser-bridge` expone status, observacion dry-run/read-only,
  `ai-consult` y `council`. El envio a IAs online requiere doble permiso:
  `--send` mas `WABI_ALLOW_BROWSER_SEND=1`, servicio allowlisted y adapter
  probado disponible. Sin eso solo escribe artefactos revisables. Ver
  `docs/BROWSER_BRIDGE_MULTIBACKEND_2026-05-18.md`.
- Las acciones riesgosas quedan en `BLOCK` o `REVIEW` con explicacion.
- El puente OSIT registra decisiones en SQLite con hash-chain y no llama modelos
  para tareas deterministicas.

Ver tambien:

- `docs/USAGE.md`
- `docs/ARCHITECTURE.md`
- `REPORT_WABI_SABI_LOCAL_AGENTS.md`
