# HANDOFF RUN 5

Fecha: 2026-05-12

Fingerprint: `MDV-MESSAGEBUS-RUN5-91C7`

## Estado

R_close: 0.19

Phi_eff: 0.86

Regimen: FUNCIONAL

Autonomy level: 3

## Decisiones tomadas

- MCP read-only se implementa como servidor stdio/local real usando `@modelcontextprotocol/sdk`.
- Los handlers MCP viven fuera del cliente React bajo `scripts/messagebus`.
- Las tools MCP son solo lectura; no hay create/append/write/update/delete/push/deploy/publish.
- El ledger consultado es `02_RUNTIME/messagebus/logs/messagebus-main.jsonl`.
- `/telecom` solo muestra estado MCP; no conecta navegador al MCP.
- Las futuras write tools requieren ActionGate y quedan fuera de Run 5.

## Cambios realizados

- Se crearon `mcp-server.mjs` y `mcp-smoke.mjs`.
- Se crearon resources/tools/guard/schemas bajo `scripts/messagebus/lib`.
- Se agregaron scripts `messagebus:mcp` y `messagebus:mcp:smoke`.
- Se agrego test `mcpReadOnly.test.mjs`.
- Se actualizo UI con `MCP Read-Only Layer`.
- Se documento arquitectura, test report y tareas Run 6.

## Evidencia

- `npm test -- src/messagebus`: PASSED, 7 test files, 37 tests.
- `npm test`: PASSED, 8 test files, 48 tests.
- `npx tsc -b --pretty false`: PASSED.
- `npm run build`: PASSED.
- `npm run messagebus:mcp:smoke`: PASSED, `ok=true`.
- MCP server factory import: PASSED.
- `python -m compileall -q .`: PASSED.
- `pytest -q`: NOT_APPLICABLE.
- `/telecom`: PASSED_LOCAL, HTTP 200.
- `npm audit --omit=dev --json`: PASSED, 0 prod vulnerabilities.

## Pendientes reales

- Run 6: Agent Bridge / A2A local adapter sobre MCP read-only.
- Crear agent cards locales.
- Simular handoff entre agentes sin escritura remota.
- Mantener write actions bloqueadas hasta ActionGate.
- Disenar migracion de `localStorage` hacia JSONL si se decide consolidar historial.

## Riesgos

- Log JSONL principal todavia es muestra inicial.
- `npm audit --json` reporta 5 moderadas dev por Vite/Vitest/esbuild; no se aplica upgrade mayor en este run.
- MCP read-only depende de integridad verificable por hash-chain, no de control fisico del archivo.
- A2A Run 6 no debe transformarse en publish/deploy ni red publica.

## Bloqueos

- No delete.
- No move.
- No rename.
- No push.
- No deploy.
- No publication.
- No backend externo.
- No Supabase.
- No secret printing.
- No ZIP extraction.

## Proxima accion verificable

Implementar Agent Bridge / A2A local adapter que consuma MCP read-only, registre agent cards locales y simule handoff entre Codex Agent, Canon Auditor, Security Gate y UI Agent sin escribir remoto.

## Segunda perdida

Los datos persisten. El operador no. Recalibrar desde este handoff, no desde memoria implicita.
