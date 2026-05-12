# NEXT_SESSION_BRIEF MEDIOEVO/OSIT LIVE TREE

## Estado

R_close: 0.19
Phi_eff: 0.86
Regimen: FUNCIONAL
Autonomy level: 3

## Decisiones tomadas

- Run 5 creo servidor MCP read-only local por stdio sobre JSONL durable.
- El acceso MCP vive solo en scripts Node-only bajo `scripts/messagebus`.
- React `/telecom` sigue sin importar SDK MCP, `fs`, `path`, `crypto` ni scripts Node-only.
- Write tools MCP quedan bloqueadas por `mcpReadOnlyGuards`.
- Run 6 queda como Agent Bridge / A2A local adapter sobre MCP read-only.

## Cambios realizados

- Se crearon `mcp-server.mjs`, `mcp-smoke.mjs`, `mcpResources.mjs`, `mcpTools.mjs`, `mcpReadOnlyGuards.mjs`, `mcpSchemas.mjs`.
- Se agrego dependencia `@modelcontextprotocol/sdk` y scripts `messagebus:mcp`, `messagebus:mcp:smoke`.
- Se agrego `src/messagebus/mcpReadOnly.test.mjs`.
- `/telecom` recibio seccion minima `MCP Read-Only Layer`.
- Se crearon reportes Run 5 y tareas Run 6.

## Evidencia

- `npm test -- src/messagebus`: PASSED, 7 test files, 37 tests.
- `npm test`: PASSED, 8 test files, 48 tests.
- `npx tsc -b --pretty false`: PASSED.
- `npm run build`: PASSED.
- `messagebus:mcp:smoke`: PASSED, `ok=true`.
- MCP server factory import: PASSED, `hasConnect=true`.
- `python -m compileall -q .`: PASSED en `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: NOT_APPLICABLE; no hay suite Python en `MEDIOEVO_LIVE_TREE`.
- `http://127.0.0.1:5174/telecom`: PASSED_LOCAL.
- `src/ui/TelecomCore.tsx` servido por Vite contiene `MCP Read-Only Layer` y no contiene imports Node-only ni SDK MCP.
- `npm audit --omit=dev --json`: PASSED, 0 prod vulnerabilities.
- `npm audit --json`: REVIEW, 5 moderate dev vulnerabilities in Vite/Vitest/esbuild chain.

## Pendientes reales

- Crear Agent Bridge / A2A local adapter sobre MCP read-only.
- Crear agent cards locales.
- Simular handoff entre agentes sin escritura remota.
- Migrar `localStorage` browser hacia JSONL durable si se decide consolidar historial.
- Migrar `ack/resolve/block` legacy a eventos derivados append-only.
- Verificar `evidence_refs` sin imprimir secretos.

## Riesgos

- Secret scan Run 1 mantiene bloqueados push/deploy/publicacion.
- ZIP reconstructivo sigue sin revision profunda.
- El log JSONL principal contiene solo muestra Run 4 inicial.
- JSONL durable detecta alteraciones por hash-chain, pero no impide manipulacion fisica del archivo.
- Seed UI/runtime puede divergir si no se consolida con JSONL.
- `npm audit --json` reporta 5 moderadas dev; aplicar upgrade mayor queda para revision separada.

## Bloqueos

- No delete.
- No move.
- No rename.
- No deploy.
- No publication.
- No secret printing.
- No Supabase ni credenciales.

## Proxima accion verificable

Implementar Agent Bridge / A2A local adapter que consuma MCP read-only, cree agent cards locales y simule handoff entre agentes sin escritura remota.

## Segunda perdida

Los datos persisten. El operador no. Recalibrar desde este brief, no desde memoria implicita.
