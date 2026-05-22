# Uso de Wabi Sabi CLI

## Comandos principales

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
.\wabi.cmd "crea una funcion que lea un archivo y resuma sus lineas"
.\wabi.cmd "revisa este proyecto y dime que falla"
.\wabi.cmd "arregla los tests"
.\wabi.cmd "crea un README para este modulo"
.\wabi.cmd "ejecuta diagnostico"
.\wabi-window.cmd
.\wabi.cmd hablar
.\wabi.cmd hablar "estas ahi?"
.\wabi.cmd hablar "crea una funcion que lea un archivo y resuma sus lineas en helpers.py"
.\wabi.cmd auto
.\wabi.cmd auto "analiza el estado y decide que conviene usar"
.\wabi.cmd chat "hola wabi, dime que puedes hacer localmente"
.\wabi.cmd codex-status
.\wabi.cmd codex "habla conmigo desde Codex a traves de Wabi-Sabi"
.\wabi.cmd codex "prepara respuesta sin ejecutar modelo" --dry-run
.\wabi.cmd env-status --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd comms-state --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd decide "continuar pendientes locales sin cruzar gates" --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd decision-log --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd comms-append-plan --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd programmer-workpack "preparar programacion multiarchivo como REVIEW sin aplicar" --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd eml 0 0 --json
.\wabi.cmd patch-plan "crea una funcion que lea un archivo y resuma sus lineas" --target helpers.py --json
.\wabi.cmd patch-apply "crea una funcion que lea un archivo y resuma sus lineas" --target helpers.py --json
.\wabi.cmd patch-apply "crea una funcion que lea un archivo y resuma sus lineas" --target helpers.py --test-command "python -m py_compile helpers.py" --json
.\wabi.cmd rollback <plan_id> --json
.\wabi.cmd tools --json
.\wabi.cmd worktree-status --json
.\wabi.cmd operator-status --json
.\wabi.cmd claim-contract docs\wabi_claim_contract.example.json --json
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
.\wabi.cmd agents
.\wabi.cmd logs
.\wabi.cmd e2e-smoke
```

## Programar con parche acotado

```powershell
.\wabi.cmd "crea una funcion que lea un archivo y resuma sus lineas" --apply --target helpers.py --json
```

Reglas del modo `--apply` y `patch-apply`:

- `--target` debe ser un `.py` dentro de `--workspace`.
- No escribe en `.git`, `.env`, `runtime`, `node_modules`, builds, releases,
  TCG, game bridge ni rutas fuera del workspace.
- Antes de escribir crea `PatchPlan` en `runtime/outputs/patch_plans`.
- Siempre escribe un diff en `runtime/outputs`.
- Antes de aplicar captura rollback en `runtime/rollback`.
- Despues de aplicar escribe execution record en `runtime/executions`.
- Cada apply/rollback registra witness en
  `runtime/witness/wabi_patch_witness.sqlite`.
- Verifica sintaxis con `py_compile`.
- `--test-command` permite comandos locales allowlisted:
  `python -m pytest ...`, `python -m py_compile ...` o `pytest ...`.
- No permite composicion shell con `;`, `&&`, `||`, pipes o redireccion.
- Si falla un test command, revierte el snapshot antes de devolver resultado.

Flujo nuevo:

```powershell
.\wabi.cmd patch-plan "crea una funcion que lea un archivo y resuma sus lineas" --target helpers.py --json
.\wabi.cmd patch-apply "crea una funcion que lea un archivo y resuma sus lineas" --target helpers.py --json
.\wabi.cmd patch-apply "crea una funcion que lea un archivo y resuma sus lineas" --target helpers.py --test-command "python -m py_compile helpers.py" --json
.\wabi.cmd rollback <plan_id> --json
.\wabi.cmd tools --json
```

`patch-plan` no toca el fuente. `patch-apply` aplica solo si el plan queda en
`APPROVE`. `rollback` restaura el snapshot exacto de ese `plan_id`, incluyendo
la eliminacion de un archivo nuevo creado por Wabi/Sabi si ese era el estado
previo. Internamente `PatchPlan` ya soporta varios archivos por plan; la CLI
publica mantiene `--target` single-file para evitar ambiguedad operativa.

## Instalacion editable

```powershell
python -m pip install -e . --no-deps --no-build-isolation
wabi "ejecuta diagnostico"
```

## Modo interactivo

```powershell
.\wabi.cmd
```

Luego escribir pedidos en lenguaje natural. Salir con `/exit`.

Tambien puedes usar el alias explicito:

```powershell
.\wabi.cmd chat
```

## Modo conversacional tipo Codex/Claude Code

```powershell
.\wabi.cmd hablar
```

`hablar` abre una sesion con prompt `Tyr>` y respuesta conversacional. Puede
usar cloud providers si estan configurados, luego Codex CLI, Ollama y dry-run
como fallback. No imprime claves ni valores de secretos.

Comandos dentro de la sesion:

```text
/status
/providers
/memory
/plan crea una funcion que lea un archivo y resuma sus lineas en helpers.py
/diff
/apply
/rollback <plan_id>
/exit
```

Regla de programacion: Wabi-Sabi genera primero `PatchPlan` + diff en
`runtime/outputs`; no toca el arbol fuente hasta que escribas `/apply`. El
apply reutiliza `SafeExecutor`, crea rollback, valida sintaxis Python y registra
witness. Si el prompt toca secretos, publicacion, borrado o frontera privada,
queda en `BLOCK` o `REVIEW`.

## Ventana persistente con decision automatica

```powershell
.\wabi-window.cmd
```

Ese launcher abre una PowerShell visible y deja corriendo:

```powershell
.\wabi.cmd hablar --cloud
```

En ese modo puedes escribir pedidos normales. Wabi-Sabi responde como chat,
prefiere provider cloud si esta habilitado/configurado, y baja a Codex, Ollama
o dry-run si falla.

Wabi-Sabi decide ruta:

- agente local para diagnosticos, archivos y artefactos simples;
- modelo base local para respuesta profunda cuando esta disponible;
- Codex CLI en solo lectura como fallback para analisis amplio y decisiones;
- OpenAI Responses si no hay Codex CLI y existe `OPENAI_API_KEY`;
- dry-run/workpack si no hay proveedor ejecutable;
- `BLOCK` si cruza publicacion, secretos o borrado destructivo.

Por defecto la cadena profunda es `ollama,codex,dry-run` cuando el modelo base
instalado esta disponible. El modelo local por defecto es
`qwen2.5-coder:3b`; puede cambiarse con `BASE_MODEL`, `WABI_BASE_MODEL` o
`WABI_OLLAMA_BASE_MODEL`.

Los planos locales siguen bloqueando aliases, benchmarks pesados y mutacion de
modelos. Por eso Wabi-Sabi no precarga Ollama por defecto y filtra modelos
`:cloud`/`-cloud` salvo `WABI_ALLOW_CLOUD_MODELS=1`.

La carga de planos es automatica. En `/status`, Wabi-Sabi reporta:

```text
Planos: OK
Planos fuentes: 7
Politica: ...
```

Si se necesita volver al modo sin modelo local, usar
`WABI_DISABLE_BASE_MODEL=1`; el orquestador conserva `codex,dry-run`.

Directivas utiles dentro de la ventana:

```text
/status
/jobs
/result
/result <job_id>
/local revisa este proyecto
/codex analiza el repo y decide siguiente paso
/dry prepara workpack sin ejecutar modelo
/exit
```

## Usar Codex a traves de Wabi-Sabi

```powershell
.\wabi.cmd codex-status --json
.\wabi.cmd codex "responde en tres lineas que pruebas correrias" --json
```

Reglas del puente:

- Por defecto usa `codex exec` si el comando `codex` esta instalado.
- Codex se invoca con `--sandbox read-only`, `--ephemeral` y
  `--ask-for-approval never`.
- Si no hay Codex CLI y existe `OPENAI_API_KEY`, usa OpenAI Responses API.
- `WABI_OPENAI_MODEL` permite cambiar el modelo; el default es `gpt-5.5`.
- `WABI_PROVIDER_ORDER` permite cambiar el orden; default efectivo:
  `ollama,codex,dry-run` si el modelo base local esta disponible.
- `BASE_MODEL`, `WABI_BASE_MODEL` o `WABI_OLLAMA_BASE_MODEL` cambian el modelo
  base. El default local es `qwen2.5-coder:3b`.
- `WABI_DISABLE_BASE_MODEL=1` desactiva la ruta local y vuelve a
  `codex,dry-run`.
- `WABI_OLLAMA_PREWARM=1` permite precalentar intencionalmente; por defecto no
  se precarga.
- `--dry-run` no llama a ningun modelo: escribe un workpack en
  `runtime/outputs`.
- Prompts con publicacion, secretos o borrado destructivo quedan en `BLOCK`.

## Modelos cloud para programar

Wabi/Sabi ya tiene perfiles de modelos para NVIDIA NIM y Qwen cloud, pero los
trata como fallback bloqueado por defecto. `provider-status --json` muestra el
catalogo y el modelo resuelto sin imprimir claves.

```powershell
.\wabi.cmd provider-status --json
$env:WABI_NVIDIA_NIM_MODEL_ALIAS='ultra'
$env:WABI_QWEN_MODEL_ALIAS='qwen-235b'
.\wabi.cmd provider-status --json
```

Aliases NVIDIA NIM:

| Alias | Modelo |
|---|---|
| `ultra` | `nvidia/llama-3.1-nemotron-ultra-253b-v1` |
| `llama-70b` | `nvidia/llama-3.1-nemotron-70b-instruct` |
| `super` | `nvidia/nemotron-3-super-120b-a12b` |
| `nano-30b` | `nvidia/nemotron-3-nano-30b-a3b` |
| `nano-9b` | `nvidia/nvidia-nemotron-nano-9b-v2` |

Aliases Qwen cloud:

| Alias | Modelo |
|---|---|
| `qwen-plus` | `qwen3.6-plus` |
| `qwen-235b` | `qwen3-235b-a22b` |

Para llamar red hacen falta dos condiciones: clave en entorno/vault y
`WABI_ALLOW_CLOUD_PROVIDERS=1`. Sin eso, Wabi/Sabi informa el modelo elegido y
cae a `dry-run` o proveedor local sin exponer secretos. Tambien puede usarse un
ID exacto con `WABI_NVIDIA_NIM_MODEL` o `WABI_QWEN_MODEL`.

### Uso film con NVIDIA

El modo film no significa que NVIDIA ejecute en la PC. El uso correcto es:

```text
intencion -> Wabi/Sabi sanea contexto -> NVIDIA propone plan/codigo/debug
          -> Wabi/Sabi convierte a TaskSpec/PatchPlan
          -> ActionGate decide -> apply local -> tests -> rollback/evidence
```

Antes de abrir llamadas live:

```powershell
.\wabi.cmd provider-status --json
.\wabi.cmd project-scan --json
.\wabi.cmd test-plan --json
```

Reglas operativas:

- no enviar `.env`, tokens, credenciales, sesiones, cookies ni logs sin
  redaccion;
- no aceptar comandos shell arbitrarios de la respuesta cloud;
- no aplicar cambios que no puedan convertirse a `TaskSpec` o `PatchPlan`;
- no ejecutar push, deploy, publicacion, borrado destructivo ni host control
  global desde el flujo cloud;
- si falla provider live por auth/cuota/rate limit/modelo, usar fallback local
  o dry-run y registrar `quota_failed`/`fallback_used`;
- si tests fallan, usar rollback y pasar a debug loop con logs saneados.

La salida cloud futura debe parecerse a:

```json
{
  "schema": "wabi.cloud_code_proposal.v0_1",
  "summary": "",
  "intent": "",
  "assumptions": [],
  "files_to_read": [],
  "changes": [],
  "commands_requested": [],
  "test_commands": [],
  "risks": [],
  "rollback_notes": [],
  "debug_strategy": [],
  "gate_recommendation": "REVIEW"
}
```

`gate_recommendation` es informativo. El gate final siempre lo calcula Wabi/Sabi
local.

Comandos offline disponibles en v0.1:

```powershell
.\wabi.cmd cloud-proposal-validate docs\wabi_cloud_code_proposal.example.json --json
.\wabi.cmd cloud-proposal-task-spec docs\wabi_cloud_code_proposal.example.json --json
.\wabi.cmd cloud-proposal-plan docs\wabi_cloud_code_proposal.example.json --json
```

`cloud-proposal-validate` valida y sanea el JSON. `cloud-proposal-task-spec`
escribe un `wabi.task_spec.v1` en `runtime/outputs/cloud_task_specs`.
`cloud-proposal-plan` genera TaskSpec, PatchPlan y diff sin tocar fuentes. La
aplicacion sigue separada: usar `task-spec-apply <spec.json>` solo despues de
revisar el gate local.

Comandos provider-gated disponibles en v0.2:

```powershell
.\wabi.cmd cloud-proposal-from-provider "crear helper seguro" --dry-run --json
.\wabi.cmd cloud-proposal-from-provider-task-spec "crear helper seguro" --dry-run --json
.\wabi.cmd cloud-proposal-from-provider-plan "crear helper seguro" --dry-run --json
.\wabi.cmd cloud-proposal-from-provider "crear helper seguro" --codex-provider nvidia --json
```

`--dry-run` usa un fixture local y prueba todo el pipeline sin proveedor. Sin
`--dry-run`, Wabi/Sabi escanea solo metadatos del proyecto, crea un prompt JSON
estricto para el provider seleccionado por `--codex-provider`, guarda la
respuesta redactada, extrae solo un objeto `wabi.cloud_code_proposal.v0_1` y lo
vuelve a pasar por la validacion local. La nube no aplica cambios.

## EML research-only

```powershell
.\wabi.cmd eml 0 0 --json
.\wabi.cmd eml window-load 1 2 3 --json
.\wabi.cmd eml jamming-margin 1 0 --json
```

EML queda como auxiliar de investigacion (`RESEARCH_ONLY`), no como regla diaria
del agente ni prueba fisica.

## Entorno y COMMS

```powershell
.\wabi.cmd env-status --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd comms-state --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

`env-status` produce `wabi.environment_snapshot.v0_2` en `runtime/outputs`.
El snapshot consolida:

- `qa_artifacts/pending/pending_review_latest.json`;
- `claudio/runtime/host_observacionista/latest_report.json`;
- `COMMS/agents_state/*.json`;
- `COMMS/tools/validate_seto_comms.py --json`;
- `ProviderOrchestrator.status()`.

El resultado incluye `decision.recommended_mode`, acciones permitidas, acciones
bloqueadas y carril de programacion seguro. Bajo host `BLOCK`, el modo esperado
es `A0_LOCAL_REVIEW_ONLY`.

`comms-state` produce `wabi.comms_state.v0_2`, resume agentes, gates,
departamentos, handoffs y resultado del validator. Es lectura local; no publica,
no hace append a COMMS y no cruza ActionGate.

## DecisionLog

```powershell
.\wabi.cmd decide "continuar pendientes locales sin cruzar gates" --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
.\wabi.cmd decision-log --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

`decide` lee el entorno con `EnvironmentSnapshot`, calcula hash del snapshot,
crea un registro `wabi.decision_record.v0_2`, escribe artefacto en
`runtime/outputs`, agrega una linea append-only en
`runtime/decision_log/wabi_decisions.jsonl`, actualiza
`runtime/decision_log/wabi_task_manager.json` con schema
`obsai.task_manager.v1` y agrega un evento en
`runtime/decision_log/wabi_decision_witness.sqlite`.

`decision-log` permite auditar los ultimos registros y el TaskManager local. No
escribe COMMS, no publica y no ejecuta acciones externas.

## Git/worktree read-only

```powershell
.\wabi.cmd worktree-status --json
```

`worktree-status` usa comandos git de lectura para reportar `repo_root`,
`branch`, `base_commit`, `dirty`, `status_sample`, nombres modificados,
untracked y `diff_stat`. No ejecuta `git add`, commit, checkout, reset ni
incluye contenido de archivos.

## Operator status

```powershell
.\wabi.cmd operator-status --json
.\wabi.cmd operator-status docs\wabi_task_spec.example.json --json
```

`operator-status` agrega en una sola salida:

- proveedor activo, modelo base y endpoint;
- worktree read-only;
- herramientas locales permitidas;
- validacion in-memory de un `wabi.task_spec.v1`;
- estado del witness SQLite hash-chain;
- ultimo artefacto `safe_test_run_*.json` si existe, con conteo pass/fail y
  witness.

No aplica task specs, no escribe codigo fuente, no reejecuta tests por si solo
y no ejecuta acciones externas.

## Claim contract

```powershell
.\wabi.cmd claim-contract docs\wabi_claim_contract.example.json --json
```

`claim-contract` convierte ideas de research o DUAT/GEODIA en un contrato
pequeno antes de integrarlas. El contrato declara:

- `claim`;
- `claim_level`;
- `evidence`;
- `falsifiers`;
- `risk_flags`.

Reglas:

- Flags como `secret`, `private_game`, `stealth`, `offensive`,
  `external_publication`, `model_weights` o `destructive` devuelven `BLOCK`.
- Claims `scientific` o `public_scientific` quedan en `REVIEW` aunque tengan
  evidencia local.
- Claims operativos con evidencia y falsadores pueden quedar `APPROVE`.
- El spec `.json` debe vivir dentro del workspace.

## Project scan

```powershell
.\wabi.cmd project-scan --json
```

`project-scan` detecta de forma no destructiva:

- gestores/lockfiles;
- lenguajes probables;
- comandos de test/build sugeridos;
- raiz Git actual y repos anidados;
- configs/entrypoints por nombre.

No incluye contenido de archivos, omite carpetas denegadas como `.git`,
`node_modules`, `runtime`, builds y rutas privadas, y solo escribe el log normal
del CLI en `runtime/logs`.

## Test plan

```powershell
.\wabi.cmd test-plan --json
```

`test-plan` usa `project-scan` para devolver comandos de verificacion
sugeridos. No ejecuta tests y no aplica cambios. Si no detecta una base de
pruebas, devuelve `NO_TEST_BASELINE` con gate `REVIEW`.

## Run safe tests

```powershell
.\wabi.cmd run-safe-tests --json
```

`run-safe-tests` ejecuta solo comandos allowlisted derivados de `test-plan`:

- `python -m pytest ...`;
- `python -m py_compile ...`;
- `pytest ...`.

Bloquea composicion shell, no aplica parches y escribe un artefacto JSON en
`runtime/outputs` junto con un evento witness hash-chain.

## Curador Orden Assistant

```powershell
.\wabi.cmd curator-assistant --json
.\wabi.cmd curator-assistant --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

`curator-assistant` es el asistente del curador para mantener orden cuando hay
humanos o agentes trabajando en la misma computadora. Produce
`wabi.curator_assistant_report.v1` en `runtime/outputs` y un `.md` hermano.

El comando:

- lee solo metadatos Git, nombres de archivo y `project-scan`;
- clasifica candidatos como `CONCURRENT_TRACKED_CHANGE`,
  `UNTRACKED_REVIEW`, `CACHE_OR_BUILD_REVIEW`, `HANDOFF_EVIDENCE`,
  `RUNTIME_EVIDENCE` o `BOUNDARY_BLOCKED`;
- ensena reglas anti-desorden para agentes y humanos;
- deja `cleanup_performed=false`;
- registra witness hash-chain.

No borra, no mueve, no stagea, no hace commit, no revierte, no publica y no
lee contenido de archivos. Los candidatos `CANDIDATE_DELETE` siguen en
`REVIEW` hasta que exista ficha/hash/regenerabilidad y gate especifico.

## Curador Fichas

```powershell
.\wabi.cmd curator-fichas --json
.\wabi.cmd curator-fichas runtime\outputs\curator_assistant_report_YYYYMMDD-HHMMSS.json --json
```

`curator-fichas` toma el ultimo `curator_assistant_report_*.json` o el reporte
pasado por argumento y genera `wabi.curator_fichas.v1`.

El comando:

- selecciona candidatos `REVIEW`/`UNKNOWN_REVIEW_REQUIRED`;
- omite candidatos `BLOCK`;
- crea fichas con `source_path`, `psi_state`, `decision`, `action_gate`,
  riesgos, evidencia, `owner`, `owner_assignment`, `curation` y siguiente
  accion;
- escribe JSON y Markdown en `runtime/outputs`;
- si existe `docs/intake`, escribe una copia fechada para continuidad del
  workspace;
- mantiene `cleanup_performed=false` y `delete_approved_count=0`.

No inspecciona contenido de archivos y no autoriza limpieza fisica. La ficha
asigna un owner-agente por carril para poder rutear el trabajo. Esa asignacion
no autoriza limpieza fisica; solo define quien debe revisar, agregar
hash/provenance y decidir en un pase posterior.

Regla de procesamiento:

- `owner` no equivale a curacion completada;
- `owner_assignment.assigned_by_actor_type` debe ser `agent` antes de usar la
  ficha para cualquier movimiento o archivo;
- la ficha solo queda procesada cuando `curation.last_record.actor_type=agent`;
- si el ultimo registro es humano, el estado correcto es
  `NEEDS_AGENT_PROCESSING`;
- despues de una edicion humana o reasignacion manual, debe correr otro pase de
  agente para cerrar `owner_assignment` y `curation` como registros de agente.

## Task spec multiarchivo

```powershell
.\wabi.cmd task-spec-plan wabi_task_spec.json --json
.\wabi.cmd task-spec-apply wabi_task_spec.json --json
```

Formato minimo:

```json
{
  "schema": "wabi.task_spec.v1",
  "summary": "create helper and tests",
  "changes": [
    {
      "target": "helpers.py",
      "suffix": ".py",
      "content": "def answer() -> int:\n    return 42\n"
    },
    {
      "target": "test_helpers.py",
      "suffix": ".py",
      "content": "from helpers import answer\n\n\ndef test_answer():\n    assert answer() == 42\n"
    }
  ],
  "test_commands": ["python -m pytest test_helpers.py -q"]
}
```

Reglas:

- El spec `.json` debe estar dentro del workspace.
- Cada cambio debe declarar `target` y exactamente una fuente: `content` o
  `content_file`.
- No hay inferencia de targets desde lenguaje natural.
- No soporta delete/move: solo `write_text`.
- Las mismas fronteras de rutas sensibles y comandos allowlisted aplican antes
  de escribir.
- Hay una plantilla validable en `docs/wabi_task_spec.example.json`.

## Plan de append COMMS

```powershell
.\wabi.cmd comms-append-plan --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

`comms-append-plan` toma el ultimo `DecisionRecord` y genera un mensaje COMMS
con `seto-observation-v1`, `message_id`, `recipient`, evidencia, falsadores y
risk flags. Por defecto no escribe en COMMS. Si se usa `--apply`, solo intenta
append cuando `append_allowed=true`; con host `BLOCK`, el plan queda bloqueado y
`append_performed=false`.

## Workpack de programacion

```powershell
.\wabi.cmd programmer-workpack "preparar programacion multiarchivo como REVIEW sin aplicar" --json --workspace C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
```

`programmer-workpack` crea `wabi.programmer_workpack.v0_1` en
`runtime/outputs`. Es siempre `PLAN_ONLY`: propone condiciones, pruebas y
falsadores, pero no genera ni aplica parches multiarchivo. Con host `BLOCK`,
`application_gate=BLOCK` y `patches=[]`.

## Rutas de evidencia

- Artefactos: `runtime/outputs`
- Patch plans: `runtime/outputs/patch_plans`
- Execution records: `runtime/executions`
- Rollback snapshots: `runtime/rollback`
- Patch witness SQLite: `runtime/witness/wabi_patch_witness.sqlite`
- Logs: `runtime/logs/wabi_events.jsonl`
- Memoria local: `runtime/memory/session_memory.jsonl`
- Decision ledger: `runtime/decision_log/wabi_decisions.jsonl`
- TaskManager compatible: `runtime/decision_log/wabi_task_manager.json`
- WitnessLog SQLite: `runtime/decision_log/wabi_decision_witness.sqlite`

## BrowserBridge Multibackend

```powershell
.\wabi.cmd browser-bridge status --json
.\wabi.cmd browser-bridge observe https://example.com/docs --json
.\wabi.cmd browser-bridge ai-consult kimi "responde con propuesta estructurada" --json
.\wabi.cmd browser-bridge council "compara estrategia de backend" --json
```

`dry-run` es el fallback determinista. `chrome-devtools-mcp` queda como backend
primario de lectura si existe `npx` y `WABI_ALLOW_BROWSER_BRIDGE=1`; Wabi no
instala ni lanza dependencias automaticamente. `kimi-webbridge` se detecta por
`WABI_KIMI_WEBBRIDGE_URL`; `hermes` se detecta por CLI y nunca se invoca con
`--yolo`.

El envio real exige `--send`, `WABI_ALLOW_BROWSER_SEND=1`, servicio
allowlisted, backend disponible y adapter live probado. Si falta cualquier
condicion, el comando devuelve `REVIEW` o `REVIEW_SKIPPED` y solo escribe un
artefacto revisable. El concilio prepara Kimi, ChatGPT, Claude, Gemini,
Gemini Pro, Gemini Thinking, Perplexity, DeepSearch, Grok, Copilot, Copilot
Smart, Qwen Max, Qwen Agents, DeepSeek 4 Pro, DeepSeek 4 Vision y DeepSeek4.

Si una respuesta live trae codigo, debe convertirse a
`wabi.cloud_code_proposal.v0_1` y validarse localmente. No hay auto-apply.

## Fronteras

Wabi Sabi local no ejecuta acciones externas, no publica, no usa secretos y no
borra archivos. Si detecta una solicitud de riesgo, devuelve `BLOCK`.
