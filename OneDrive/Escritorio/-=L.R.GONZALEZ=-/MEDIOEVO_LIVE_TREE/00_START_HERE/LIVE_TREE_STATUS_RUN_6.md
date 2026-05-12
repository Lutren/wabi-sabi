# LIVE TREE STATUS RUN 6

Fecha: 2026-05-12

Producto: DUAT Telecom Core

Nombre tecnico: MEDIOEVO MessageBus / Agent Bridge local

Fingerprint entrada: `MDV-MESSAGEBUS-RUN5-91C7`

Fingerprint salida: `MDV-AGENT-BRIDGE-RUN6-4D19`

## Veredicto

Estado Run 6: AGENT_BRIDGE_A2A_LOCAL_VALIDADO.

R_est: 0.18

Phi_eff_est: 0.87

Regimen: FUNCIONAL

ActionGate: APPROVE_LOCAL_READMOSTLY / BLOCK_WRITE_REMOTE_PUBLICATION

## Que se leyo

- `00_START_HERE/LIVE_TREE_STATUS_RUN_5.md`
- `03_SYSTEMS/MESSAGEBUS_MCP_READONLY_SERVER.md`
- `03_SYSTEMS/MESSAGEBUS_DURABLE_JSONL.md`
- `10_QUALITY/MESSAGEBUS_MCP_READONLY_TEST_REPORT.md`
- `09_OPERACION/HANDOFF_RUN_5.md`
- `09_OPERACION/TASKS_RUN_6.md`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\scripts\messagebus\mcp-server.mjs`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\scripts\messagebus\mcp-smoke.mjs`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\scripts\messagebus\lib\*.mjs`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\messagebus\*`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\ui\TelecomCore.tsx`
- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\package.json`
- Auditoria workspace: `AGENTS.md`, `AUDIT_REPO_TREE.md`, `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`, `RISK_REGISTER.md`, `SECRET_SCAN_REPORT.md`, `DUPLICATES_AND_DEAD_CODE.md`, `RELEASE_READINESS_SCORE.md`

## Que se creo

- `scripts/agents/agent-bridge-smoke.mjs`
- `scripts/agents/lib/agentCardSchema.mjs`
- `scripts/agents/lib/agentRegistry.mjs`
- `scripts/agents/lib/localA2AEnvelope.mjs`
- `scripts/agents/lib/agentRouter.mjs`
- `scripts/agents/lib/handoffSimulator.mjs`
- `scripts/agents/lib/decisionTrace.mjs`
- `scripts/agents/lib/bridgeHealth.mjs`
- `scripts/agents/lib/mcpClientAdapter.mjs`
- `scripts/agents/cards/codex-agent.card.json`
- `scripts/agents/cards/publisher-agent.card.json`
- `scripts/agents/cards/canon-auditor-agent.card.json`
- `scripts/agents/cards/security-gate-agent.card.json`
- `scripts/agents/cards/ui-agent.card.json`
- `scripts/agents/cards/messagebus-reader-agent.card.json`
- `src/messagebus/agentBridge.test.mjs`
- `03_SYSTEMS/AGENT_BRIDGE_A2A_LOCAL.md`
- `10_QUALITY/AGENT_BRIDGE_RUN_6_TEST_REPORT.md`
- `09_OPERACION/HANDOFF_RUN_6.md`
- `09_OPERACION/TASKS_RUN_7.md`

## Que se modifico

- `package.json`: script `agents:bridge:smoke`.
- `src/ui/TelecomCore.tsx`: seccion minima `Agent Bridge / Local A2A Layer`.
- `src/styles.css`: clase compartida para `agent-bridge-status`.
- Continuidad: `SESSION_FINGERPRINT.json`, `NEXT_SESSION_BRIEF.md`, `DECISIONS.md`, `TASKS.md`, `RISKS.md`, `ASSUMPTIONS.md`, `TEST_REPORT.md`.

## Resultado tecnico

- Agent Cards locales disponibles para Codex, Publisher, Canon Auditor, Security Gate, UI y MessageBus Reader.
- Agent Registry carga y valida todas las cards requeridas.
- Local A2A envelope genera `traceHash` determinista y no ejecuta acciones.
- Agent Router enruta por intencion y bloquea acciones peligrosas.
- Handoff Simulator consulta MCP read-only y produce `nextSuggestedPrompt` en memoria.
- Decision Trace genera hash y Markdown en memoria.
- MCP adapter reutiliza handlers puros de Run 5; no abre red ni usa HTTP.
- Smoke del bridge confirma que `messagebus-main.jsonl` no cambia durante simulaciones.
- React/Vite no importa `scripts/agents`, `scripts/messagebus`, SDK MCP ni Node-only APIs.

## Tests ejecutados

- `npm test -- src/messagebus`: PASSED, 8 test files, 51 tests.
- `npm test`: PASSED, 9 test files, 62 tests.
- `npx tsc -b --pretty false`: PASSED.
- `npm run build`: PASSED, 1600 modules transformed.
- `npm run messagebus:mcp:smoke`: PASSED, `ok=true`, resources 7, tools 8.
- `npm run agents:bridge:smoke`: PASSED, `ok=true`, agents 6.
- `python -m compileall -q .`: PASSED en `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: NOT_APPLICABLE; no se detecto suite Python `test_*.py` / `*_test.py` en `MEDIOEVO_LIVE_TREE`.
- `http://127.0.0.1:5174/telecom`: PASSED_LOCAL, status 200.
- `src/ui/TelecomCore.tsx`: PASSED_LOCAL; contiene `Agent Bridge / Local A2A Layer` y no contiene SDK MCP ni imports Node-only.
- `npm audit --omit=dev --json`: PASSED, 0 prod vulnerabilities.
- `npm audit --json`: REVIEW, 5 moderate dev vulnerabilities in Vite/Vitest/esbuild chain.

## Bloqueos

- No write tools MCP.
- No append remoto ni write proposal layer todavia.
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
- El Agent Bridge simula routing y handoff; no ejecuta acciones ni escribe al MessageBus.
- Las Agent Cards son locales y no son A2A publico.
- El upgrade de Vite/Vitest/esbuild queda fuera de Run 6 por ser upgrade mayor de dev tooling.

## Proximo paso

Run 7: ActionGate write proposal layer. Crear propuestas firmadas de escritura, simular aprobacion/rechazo del operador y mantener bloqueo de ejecucion automatica.
