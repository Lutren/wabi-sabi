# MESSAGEBUS MCP READ-ONLY TEST REPORT

Fecha: 2026-05-12

Estado final: PASSED_LOCAL.

## Estado MCP SDK

- `@modelcontextprotocol/sdk`: instalado.
- Version observada: 1.29.0.
- Transporte implementado: stdio/local.
- Server factory: PASSED (`hasConnect=true`).
- `MCP_SDK_BLOCKED.md`: NOT_APPLICABLE.

## Comandos ejecutados

| Comando | Resultado |
|---|---|
| `npm install @modelcontextprotocol/sdk` | PASSED; dependencia agregada |
| `npm test -- src/messagebus` | PASSED: 7 test files, 37 tests |
| `npm test` | PASSED: 8 test files, 48 tests |
| `npx tsc -b --pretty false` | PASSED |
| `npm run build` | PASSED: 1600 modules transformed |
| `npm run messagebus:mcp:smoke` | PASSED: `ok=true`, 7 resources, 8 tools |
| `node -e import('./scripts/messagebus/mcp-server.mjs')...` | PASSED: SDK server factory carga |
| `python -m compileall -q .` | PASSED |
| `pytest -q` | NOT_APPLICABLE: no Python tests detected under `MEDIOEVO_LIVE_TREE` |
| `Invoke-WebRequest http://127.0.0.1:5174/telecom` | PASSED_LOCAL: status 200 |
| `Invoke-WebRequest http://127.0.0.1:5174/src/ui/TelecomCore.tsx` | PASSED_LOCAL: contiene `MCP Read-Only Layer` y no importa Node-only |
| `npm audit --omit=dev --json` | PASSED: 0 prod vulnerabilities |
| `npm audit --json` | REVIEW: 5 moderate dev vulnerabilities in Vite/Vitest/esbuild chain |

## Tests nuevos

Archivo:

`C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\messagebus\mcpReadOnly.test.mjs`

Cobertura:

- `messagebus://health` devuelve `readOnly=true`.
- `get_log_stats` no modifica JSONL.
- `verify_hash_chain` acepta fixture valido.
- `verify_hash_chain` rechaza fixture con hash roto.
- `replay_channel` devuelve solo canal solicitado.
- `get_agent_inbox` filtra correctamente.
- `get_agent_outbox` filtra correctamente.
- `get_task_queue` reconstruye tareas desde replay.
- `export_handoff` devuelve Markdown sin escribir archivo.
- `export_witnesslog` devuelve JSON sin escribir archivo.
- Read-only guard rechaza tools con verbos prohibidos.
- Modulos MCP no exportan funciones write-like ni llaman writers del log.
- React UI no importa MCP SDK ni modulos Node-only.

## Smoke MCP

Script:

`npm run messagebus:mcp:smoke`

Resultado:

- `ok=true`
- `readOnly=true`
- `writeToolsEnabled=false`
- resources: `logs`, `channels`, `agents`, `tasks`, `handoffs`, `witnesslog`, `health`
- tools: `get_log_stats`, `verify_hash_chain`, `replay_channel`, `get_agent_inbox`, `get_agent_outbox`, `get_task_queue`, `export_handoff`, `export_witnesslog`
- main log total entries: 1
- last hash: `sha256-a3eb743da2b85b1096440c4b406b06f2e9b0141c69d103779a97dcc93c160791`
- file mutation during smoke: NOT_DETECTED

## Estado final

- MCP read-only: READY.
- MCP write tools: DISABLED.
- JSONL durable: readable and verified.
- Hash-chain: OK.
- Replay: OK.
- `/telecom`: OK.

## Riesgos pendientes

- El log principal contiene solo sample Run 4.
- `npm audit --json` mantiene 5 vulnerabilidades moderadas dev; aplicar upgrade mayor requiere revision separada.
- Run 6 debe mantener modo read-only al introducir Agent Bridge / A2A adapter.
