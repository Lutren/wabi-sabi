# LIVE TREE STATUS RUN 5

Fecha: 2026-05-12

Producto: DUAT Telecom Core

Nombre tecnico: MEDIOEVO MessageBus

Fingerprint entrada: `MDV-MESSAGEBUS-RUN4-8E2B`

Fingerprint salida: `MDV-MESSAGEBUS-RUN5-91C7`

## Veredicto

Estado Run 5: MESSAGEBUS_MCP_READONLY_SERVER_VALIDADO.

R_est: 0.19

Phi_eff_est: 0.86

Regimen: FUNCIONAL

ActionGate: APPROVE_LOCAL_READONLY / BLOCK_WRITE_REMOTE_PUBLICATION

## Que se leyo

- `00_START_HERE/LIVE_TREE_STATUS_RUN_4.md`
- `03_SYSTEMS/MESSAGEBUS_DURABLE_JSONL.md`
- `03_SYSTEMS/MESSAGEBUS_MCP_READONLY_PLAN.md`
- `10_QUALITY/MESSAGEBUS_DURABLE_TEST_REPORT.md`
- `09_OPERACION/HANDOFF_RUN_4.md`
- `09_OPERACION/TASKS_RUN_5.md`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\scripts\messagebus\*.mjs`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\scripts\messagebus\lib\*.mjs`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\messagebus\*`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\ui\TelecomCore.tsx`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\package.json`
- Auditoria workspace: `AGENTS.md`, `AUDIT_REPO_TREE.md`, `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`, `RISK_REGISTER.md`, `SECRET_SCAN_REPORT.md`, `DUPLICATES_AND_DEAD_CODE.md`, `RELEASE_READINESS_SCORE.md`

## Que se creo

- `scripts/messagebus/mcp-server.mjs`
- `scripts/messagebus/mcp-smoke.mjs`
- `scripts/messagebus/lib/mcpResources.mjs`
- `scripts/messagebus/lib/mcpTools.mjs`
- `scripts/messagebus/lib/mcpReadOnlyGuards.mjs`
- `scripts/messagebus/lib/mcpSchemas.mjs`
- `src/messagebus/mcpReadOnly.test.mjs`
- `03_SYSTEMS/MESSAGEBUS_MCP_READONLY_SERVER.md`
- `10_QUALITY/MESSAGEBUS_MCP_READONLY_TEST_REPORT.md`
- `09_OPERACION/HANDOFF_RUN_5.md`
- `09_OPERACION/TASKS_RUN_6.md`

## Que se modifico

- `package.json`: scripts `messagebus:mcp` y `messagebus:mcp:smoke`; dependencia `@modelcontextprotocol/sdk`.
- `package-lock.json`: lock del SDK MCP.
- `src/ui/TelecomCore.tsx`: seccion minima `MCP Read-Only Layer`.
- `src/styles.css`: estilo compartido para estado MCP.
- Continuidad: `SESSION_FINGERPRINT.json`, `NEXT_SESSION_BRIEF.md`, `TEST_REPORT.md`, `DECISIONS.md`, `TASKS.md`, `RISKS.md`, `ASSUMPTIONS.md`, `03_SYSTEMS/MEDIOEVO_MESSAGEBUS.md`.

## Resultado tecnico

- Servidor MCP real por stdio/local disponible via `npm run messagebus:mcp`.
- Handlers puros testeables disponibles para resources/tools.
- Resources disponibles: `messagebus://logs`, `messagebus://channels`, `messagebus://agents`, `messagebus://tasks`, `messagebus://handoffs`, `messagebus://witnesslog`, `messagebus://health`.
- Tools read-only disponibles: `get_log_stats`, `verify_hash_chain`, `replay_channel`, `get_agent_inbox`, `get_agent_outbox`, `get_task_queue`, `export_handoff`, `export_witnesslog`.
- Read-only guard rechaza tools con verbos de escritura.
- El smoke test verifica que el JSONL principal no cambia durante consultas.
- React/Vite no importa SDK MCP ni modulos Node-only.

## Tests ejecutados

- `npm test -- src/messagebus`: PASSED, 7 test files, 37 tests.
- `npm test`: PASSED, 8 test files, 48 tests.
- `npx tsc -b --pretty false`: PASSED.
- `npm run build`: PASSED, 1600 modules transformed.
- `npm run messagebus:mcp:smoke`: PASSED, `ok=true`, resources 7, tools 8.
- `node -e import('./scripts/messagebus/mcp-server.mjs')...`: PASSED, server factory carga SDK.
- `python -m compileall -q .`: PASSED en `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: NOT_APPLICABLE; no hay suite Python en `MEDIOEVO_LIVE_TREE`.
- `http://127.0.0.1:5174/telecom`: PASSED_LOCAL, status 200.
- `http://127.0.0.1:5174/src/ui/TelecomCore.tsx`: PASSED_LOCAL, contiene `MCP Read-Only Layer` y no contiene SDK MCP ni Node-only imports.
- `npm audit --omit=dev --json`: PASSED, 0 prod vulnerabilities.
- `npm audit --json`: REVIEW, 5 moderate dev vulnerabilities existentes en Vite/Vitest/esbuild chain; no se ejecuto `audit fix --force`.

## Bloqueos

- No write tools MCP.
- No backend externo.
- No HTTP publico.
- No push.
- No deploy.
- No publicacion.
- No Supabase.
- No secret printing.
- No extraccion ZIP canon.

## Limitaciones

- El log principal sigue con una entrada sample Run 4.
- El MCP read-only consulta JSONL durable; no migra `localStorage`.
- El servidor MCP queda local stdio; no hay bridge A2A todavia.
- La seguridad de integridad es deteccion por hash-chain, no bloqueo fisico del archivo.
- El audit completo mantiene 5 vulnerabilidades moderadas dev por Vite/Vitest que requieren revision de upgrade mayor.

## Proximo paso

Run 6: Agent Bridge / A2A local adapter sobre MCP read-only, con agent cards locales y simulacion de handoff entre agentes sin escritura remota.
