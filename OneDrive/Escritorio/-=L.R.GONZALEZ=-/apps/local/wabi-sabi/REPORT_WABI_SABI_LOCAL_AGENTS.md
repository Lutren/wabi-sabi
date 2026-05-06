# Report Wabi Sabi Local Agents

Fecha de cierre: 2026-05-05

Estado: FUNCIONAL

Closure fingerprint operativo:
`cd2307aeed9e4c2463f4247bb292c16c4d1b4dbe2a21efabc434eba9ae39e06d`

## Resumen ejecutivo

Wabi Sabi queda como CLI local-first aislado en `apps/local/wabi-sabi`, con
router de intencion, registro de agentes, ActionGate, memoria JSONL, wrappers
Windows, entrypoint instalable `wabi`, documentacion y pruebas minimas.

El sistema funciona sin nube y sin claves. No hace push, deploy, publicacion,
borrado destructivo ni lectura de secretos. Las acciones automaticas escriben
artefactos en `runtime/outputs` y registran evidencia append-only en
`runtime/logs/wabi_events.jsonl`.

## Mapa del sistema

- CLI: `wabi_sabi/cli/main.py`
- Parser: `wabi_sabi/cli/parser.py`
- Router: `wabi_sabi/cli/router.py`
- Registro: `wabi_sabi/config/agents.json`
- Gate: `wabi_sabi/core/gate.py`
- Memoria/logs: `wabi_sabi/core/memory.py`
- ObservationEnvelope: `wabi_sabi/core/observation.py`
- Agentes: `wabi_sabi/agents/`
- Tests: `tests/`
- Docs: `docs/`
- Wrapper CMD: `wabi.cmd`
- Wrapper PowerShell: `wabi.ps1`
- Runtime local: `runtime/`

## Agentes registrados

| agente | funcion | gate |
|---|---|---|
| `programmer` | genera codigo local como artefacto seguro | safe_mode true |
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

## Siguiente paso recomendado

Agregar un modo `--apply` con patch local acotado por ruta y diff previo:

- solo dentro de `--workspace`;
- backup o patch reversible;
- secret/path scan antes de escribir;
- test focal obligatorio despues de escribir;
- evento JSONL con hash antes/despues.

Ese paso convertiria el carril actual de "artefactos seguros" a "reparacion
local con escrituras controladas" sin saltar ActionGate.
