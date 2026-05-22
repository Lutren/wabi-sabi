# BrowserBridge Multibackend v0.1 - 2026-05-18

## Estado

BrowserBridge queda implementado como capa local-first para observacion de
navegador, consultas revisables a IAs online y concilio prepare-only.

## Backends

- `dry-run`: fallback determinista, no navegador, no red.
- `chrome-devtools-mcp`: backend primario de lectura/snapshot/extract/screenshot,
  disponible solo si existe `npx` y `WABI_ALLOW_BROWSER_BRIDGE=1`; Wabi no
  instala ni lanza dependencias automaticamente.
- `kimi-webbridge`: adapter opcional detectado por `WABI_KIMI_WEBBRIDGE_URL`;
  primer candidato de benchmark live.
- `hermes`: adapter opcional detectado por CLI; Wabi no usa `--yolo`.

## Doble permiso de envio

`browser-bridge ai-consult` solo envia si se cumplen todas las condiciones:

- CLI `--send`.
- `WABI_ALLOW_BROWSER_SEND=1`.
- servicio allowlisted.
- backend disponible.
- adapter live probado para ese servicio.

Sin esas condiciones, genera artefacto revisable y devuelve `REVIEW` o
`REVIEW_SKIPPED`; `online_ai_called=false`.

## Catalogo

Servicios allowlisted: Kimi, ChatGPT, Claude, Gemini, Gemini Pro, Gemini
Thinking, Perplexity, DeepSearch, Grok, Copilot, Copilot Smart, Qwen Max,
Qwen Agents, DeepSeek 4 Pro, DeepSeek 4 Vision y DeepSeek4.

En v0.1 solo Kimi tiene live backend candidato (`kimi-webbridge`). El resto
queda `prepare-only` hasta tener selector pack probado.

## Concilio

`browser-bridge council <prompt>` prepara consultas para el catalogo completo.
Por defecto no llama red. Si una respuesta live trae codigo, BrowserBridge
intenta extraer un unico `wabi.cloud_code_proposal.v0_1`, escribe el artefacto
en `runtime/outputs/cloud_proposals` y lo valida localmente. No genera apply
automatico, TaskSpec automatico ni PatchPlan automatico.

## Comandos

```powershell
.\wabi.cmd browser-bridge status --json
.\wabi.cmd browser-bridge observe https://example.com/docs --json
.\wabi.cmd browser-bridge ai-consult kimi "responde con propuesta estructurada" --json
.\wabi.cmd browser-bridge ai-consult kimi "responde con propuesta estructurada" --send --browser-backend kimi-webbridge --json
.\wabi.cmd browser-bridge council "compara estrategia de backend" --json
```

## Evidencia

- `python -B -m py_compile wabi_sabi\core\browser_bridge.py wabi_sabi\cli\main.py`: PASS.
- `python -B -m pytest tests\test_browser_bridge.py -q -p no:cacheprovider`: `10 passed`.
- `python -B -m pytest tests\test_cloud_code_proposal.py tests\test_cli.py tests\test_browser_gate.py tests\test_browser_bridge.py -q -p no:cacheprovider`: `37 passed`.
- `python -B -m pytest -q -p no:cacheprovider`: `293 passed`.
- `.\wabi.cmd run-safe-tests --json`: `ok=true`, `293 passed`, `witness_verified=true`, `witness_event_id=35`.
- BRAIN_OS world model synthetic benchmark: `gate_accuracy=1.0`, `false_approve_rate=0.0`, `network_calls=false`.
- BRAIN_OS MTS v0.3 benchmark: `success=True`, `mts_accuracy=0.98`, `critical_fail=0`.
- `python -B -m pytest 02_CLAUDIO\tests -q -p no:cacheprovider`: `688 passed`.

## Gate

PublicationGate: BLOCK. CloudLLMGate: REVIEW unless double opt-in and proven
adapter. Online responses remain proposal-only and never grant execution
permission.

---

# BrowserBridge Selector Pack v0.2 - 2026-05-18

## Estado

BrowserBridge v0.2 agrega selector pack probado, smoke Kimi controlado por
doble opt-in, snapshot Chrome DevTools MCP solo lectura, ranking de council sin
ejecucion automatica, endurecimiento de respuesta-a-propuesta, CLI extendido y
estado visible en Wabi UI / Operational Workbench.

## Selector Pack

- `ServiceCapability` define servicio, adapter, modo, soporte lectura/envio,
  soporte de codigo, requisitos de URL/auth, gate, riesgo y clases de payload.
- `dry-run` siempre esta disponible y sigue como default.
- `chrome-devtools-mcp` solo entra como `READ_ONLY` si existe herramienta local
  y `WABI_ALLOW_BROWSER_BRIDGE=1`.
- `kimi-webbridge` queda `SEND_REVIEW` y requiere `--send`,
  `WABI_ALLOW_BROWSER_SEND=1`, `WABI_ALLOW_BROWSER_BRIDGE=1`,
  `WABI_KIMI_WEBBRIDGE_URL`, URL local segura y payload publico/sanitizado.
- `hermes` queda adapter opcional no-live, sin `--yolo`.
- Servicios sin adapter probado quedan `PREPARE_ONLY`.

Clases de payload: `PUBLIC_PROMPT`, `SANITIZED_TASK`, `SNAPSHOT_READONLY`,
`CODE_PROPOSAL`, `PRIVATE_WORKSPACE_BLOCKED`, `CREDENTIAL_BLOCKED` y
`PROTECTED_MATERIAL_BLOCKED`.

## CLI v0.2

```powershell
.\wabi.cmd browser-bridge select --service kimi --payload-class PUBLIC_PROMPT --json
.\wabi.cmd browser-bridge smoke --service kimi --json
.\wabi.cmd browser-bridge snapshot --backend chrome-devtools-mcp --json
.\wabi.cmd browser-bridge council --json
.\wabi.cmd browser-bridge proposal-from-response --input <file> --json
```

## Resultados de esta corrida

- Kimi smoke: `KIMI_SEND_FLAGS_MISSING`; no se llamo Kimi.
- DevTools MCP: `DEVTOOLS_MCP_NOT_AVAILABLE`; fallback dry-run preservado.
- Council: `service_count=16`, `prepared_count=16`, `live_attempts=0`,
  `online_ai_called=false`, recomendado `kimi/SEND_REVIEW`.
- Proposal sample: `VALIDATED`; sin TaskSpec, PatchPlan ni auto-apply.
- UI/API: `/api/browser-bridge` y panel BrowserBridge agregados.

## Evidencia v0.2

- BrowserBridge focal: `21 passed`.
- BrowserBridge + redaction/cloud adapters: `32 passed`.
- Wabi/provider/CLI expanded: `81 passed`.
- Wabi full: `304 passed`.
- `.\wabi.cmd run-safe-tests --json`: `ok=true`, `304 passed`,
  `witness_verified=true`, `witness_event_id=38`.
- BRAIN_OS Wabi local server/UI: `180 passed`.
- `02_CLAUDIO` full: `690 passed`.
- GEODIA: `74 passed`.
- DUAT predictive registry: `117 passed`.
- World model: `gate_accuracy=1.0`, `false_approve_rate=0.0`.
- MTS v0.3: `success=True`, `mts_accuracy=0.98`, `critical_fail=0`.
- HTTP temporal 8788: endpoints solicitados PASS.
- SecretScan focal: `ok=true`, `finding_count=0`, `scanned=11`.

## Gate v0.2

PublicationGate: BLOCK. CloudLLMGate: BLOCK_PRIVATE_WORKSPACE.
BrowserSendGate: REVIEW_SEND_ONLY_WITH_DOUBLE_OPT_IN. NvidiaSmokeGate:
DO_NOT_CALL. DeepSeekGate: REVIEW_QUOTA_OR_BILLING.
