# AGENT BRIDGE RUN 6 TEST REPORT

Fecha: 2026-05-12

Estado final: PASSED_LOCAL.

## Comandos ejecutados

| Comando | Resultado |
|---|---|
| `npm test -- src/messagebus` | PASSED: 8 test files, 51 tests |
| `npm test` | PASSED: 9 test files, 62 tests |
| `npx tsc -b --pretty false` | PASSED |
| `npm run build` | PASSED: 1600 modules transformed |
| `npm run messagebus:mcp:smoke` | PASSED: `ok=true`, resources 7, tools 8 |
| `npm run agents:bridge:smoke` | PASSED: `ok=true`, agents 6 |
| `npm audit --omit=dev --json` | PASSED: 0 prod vulnerabilities |
| `npm audit --json` | REVIEW: 5 moderate dev vulnerabilities |
| `python -m compileall -q .` | PASSED |
| `pytest -q` | NOT_APPLICABLE: no Python tests detected under `MEDIOEVO_LIVE_TREE` |
| `Invoke-WebRequest http://127.0.0.1:5174/telecom` | PASSED_LOCAL: status 200 |
| `Select-String TelecomCore.tsx Agent Bridge / Local A2A Layer` | PASSED_LOCAL |
| `Select-String TelecomCore.tsx forbidden Node/MCP imports` | PASSED_LOCAL: no matches |

## Tests nuevos

Archivo:

`C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\messagebus\agentBridge.test.mjs`

Cobertura:

- Todas las Agent Cards cumplen schema.
- Agent Registry carga agentes esperados.
- Router enruta deploy a Publisher Agent.
- Router enruta secret scan a Security Gate Agent.
- Router enruta canon coverage a Canon Auditor Agent.
- Router enruta UI route smoke a UI Agent.
- Router enruta hash-chain/replay a MessageBus Reader Agent.
- Router enruta code/test implementation a Codex Agent.
- Forbidden actions son bloqueadas.
- Local A2A envelope genera `traceHash`.
- Handoff simulator produce `nextSuggestedPrompt`.
- MCP adapter devuelve health.
- Agent Bridge no modifica JSONL durable principal.
- React build surface no importa modulos Node-only del bridge.

## Smoke Agent Bridge

Script:

`npm run agents:bridge:smoke`

Resultado:

- `ok=true`
- `bridgeStatus=READY`
- `readOnly=true`
- `remoteNetworkEnabled=false`
- `writeToolsEnabled=false`
- `agentCount=6`
- `deploy` enruta a `publisher-agent` y bloquea `deploy`.
- `secret scan before publishing` enruta a `security-gate-agent` y bloquea `publish`.
- `verify MessageBus handoff stream` enruta a `messagebus-reader-agent`.
- JSONL principal: mutation NOT_DETECTED.

## Estado MCP

- MCP read-only: READY.
- MCP adapter: READY, usa handlers puros de Run 5.
- Hash-chain: OK.
- Replay: OK.
- Last hash: `sha256-a3eb743da2b85b1096440c4b406b06f2e9b0141c69d103779a97dcc93c160791`.

## Estado /telecom

- Ruta local: `http://127.0.0.1:5174/telecom`.
- HTTP status: 200.
- Panel agregado: `Agent Bridge / Local A2A Layer`.
- Node-only imports en React: NOT_DETECTED.

## Audit

- `npm audit --omit=dev --json`: 0 prod vulnerabilities.
- `npm audit --json`: 5 moderate dev vulnerabilities en Vite/Vitest/esbuild chain.
- Decision: no bloquea Run 6 local read-mostly; upgrade mayor queda en REVIEW para carril separado.

## Estado final

- Agent Bridge: READY.
- Agent Cards: READY.
- Local A2A envelope: READY.
- Router: READY.
- Handoff Simulator: READY.
- Decision Trace: READY.
- MCP adapter: READY.
- Write actions: BLOCKED.
- Remote network: DISABLED.
