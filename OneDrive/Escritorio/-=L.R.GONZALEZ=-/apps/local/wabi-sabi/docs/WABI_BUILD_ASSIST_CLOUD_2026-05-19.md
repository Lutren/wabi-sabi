# Wabi Build Assist Cloud - 2026-05-19

## Objetivo

Wabi sigue siendo local-first como producto final. Durante la etapa de
construccion, puede usar proveedores cloud como andamio temporal para producir
propuestas estructuradas de codigo, planes y debug. La nube no aplica cambios
locales.

## Contrato

```text
operador
-> Wabi local
-> contexto saneado minimo
-> proveedor cloud temporal
-> wabi.cloud_code_proposal.v0_1
-> validacion local
-> TaskSpec/PatchPlan
-> SafeExecutor local con rollback/tests
```

## Comandos

```powershell
.\wabi.cmd build-assist-status --json
.\wabi.cmd build-assist-plan "crear helper seguro" --dry-run --json
.\wabi.cmd build-assist-smoke --provider nvidia --model nano-30b --json
```

Para una llamada live temporal, el operador debe habilitar ambas banderas en la
sesion y tener una clave NVIDIA en entorno/vault:

```powershell
$env:WABI_BUILD_ASSIST_CLOUD='1'
$env:WABI_ALLOW_CLOUD_PROVIDERS='1'
.\wabi.cmd build-assist-plan "crear helper seguro" --codex-provider nano-30b --json
.\wabi.cmd build-assist-smoke --provider nvidia --model nano-30b --live --json
```

## Modelos

- Default build-assist: `nano-30b`.
- Triage barato: `nano-9b`.
- Revision manual: `super`, `ultra`, `llama-70b`, `kimi`, `deepseek`,
  `mistral`, `minimax`, `glm`.

El alias general `WABI_NVIDIA_NIM_MODEL_ALIAS` no cambia el default de
build-assist. Para cambiar solo esta capa usar:

```powershell
$env:WABI_BUILD_ASSIST_NVIDIA_MODEL_ALIAS='nano-9b'
```

## Gates

- `WABI_BUILD_ASSIST_CLOUD=1` activa el modo temporal.
- `WABI_ALLOW_CLOUD_PROVIDERS=1` permite llamada cloud real.
- Sin ambas banderas, `build-assist-plan` fuerza dry-run y no llama red.
- El limite por defecto es 12 llamadas cloud registradas por runtime:
  `WABI_BUILD_ASSIST_MAX_CLOUD_CALLS`.
- Si el presupuesto se agota, el gate queda `BLOCK_BUDGET_EXHAUSTED`.

## Smoke live 2026-05-19

Comando ejecutado con banderas de sesion:

```powershell
$env:WABI_BUILD_ASSIST_CLOUD='1'; $env:WABI_ALLOW_CLOUD_PROVIDERS='1'; .\wabi.cmd build-assist-smoke --provider nvidia --model nano-30b --live --json --workspace "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-"
```

Resultado:

- status: `LIVE_SMOKE_PASS`
- provider: `nvidia`
- model_alias: `nano-30b`
- model: `nvidia/nemotron-3-nano-30b-a3b`
- mode: `proposal_only`
- cloud_provider_called: `true`
- applied_to_sources: `false`
- secrets_printed: `false`
- redaction: `PASS`
- latency_ms: `2308`
- usage/cost: no devueltos por el adapter, quedan `null`

Artefacto local:

`C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\build_assist_smoke\wabi_build_assist_nvidia_smoke_20260519-133139.json`

Scan de redaccion:

- files_scanned: `2`
- secret_value_hits: `0`
- redaction: `PASS`

## Fronteras

- No secretos, `.env`, cookies, canon privado, juego privado ni workspace
  completo en prompts.
- No auto-apply desde cloud.
- No retry automatico en errores de cuota, billing o rate-limit.
- Toda respuesta externa con codigo debe validar como
  `wabi.cloud_code_proposal.v0_1`.
- La aplicacion queda siempre en Wabi local con rollback, tests y WitnessLog.

## Evidencia

Tests focales:

```powershell
python -B -m pytest tests\test_build_assist_cloud.py tests\test_provider_orchestrator.py tests\test_redaction_and_cloud_adapters.py tests\test_cloud_code_proposal.py -q -p no:cacheprovider
```

Evidencia final de esta corrida:

- Focal recomendado: `42 passed in 14.67s`.
- Regresion Wabi: `322 passed in 111.97s`.
- `py_compile`: PASS.
