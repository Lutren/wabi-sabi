# TASKS

## P0

- Revisar `10_QUALITY/SECRET_SCAN_REPORT.md` por allowlist de target antes de cualquier publicacion.
- Mantener bloqueado push/deploy/publicacion mientras existan hallazgos enmascarados de secret scan.

## P1

- Migrar MEDIOEVO MessageBus de `localStorage` a JSONL/SQLite local append-only.
- Crear validador de schema/canales/hash-chain para `AgentMessage` y `WitnessEvent`.
- Revisar `08_CLEANUP/UNKNOWN_REVIEW.md`.
- Subir cobertura de candidatos `DELETE_AFTER_COVERAGE` solo con hash, destino claro y no-secretos.

## P2

- Crear MCP read-only local para listar canales, bulletin, handoffs y P0.
- Afinar fichas de `01_SOURCE_CARDS` para los 20 candidatos de mayor valor.
# Run 3 cierre / Run 4 entrada

- [ ] P1 Crear adaptador JSONL local en disco para `appendOnlyLog`.
- [ ] P1 Crear replay test: export JSONL -> import JSONL -> `verifyLog().ok === true`.
- [ ] P1 Migrar `ack/resolve/block` legacy a eventos derivados append-only.
- [ ] P1 Crear MCP read-only local para `medioevo://messagebus/*`.
- [ ] P2 Validar `evidence_refs` sin imprimir secretos.
- [ ] P2 Crear fixture de ledger Run 3 con hash-chain SHA-256.

# Run 4 cierre / Run 5 entrada

- [x] P1 Crear MCP read-only server local sobre `messagebus-main.jsonl`.
- [x] P1 Exponer resource `messagebus://logs`.
- [x] P1 Exponer resource `messagebus://channels`.
- [x] P1 Exponer resource `messagebus://agents`.
- [x] P1 Exponer resource `messagebus://tasks`.
- [x] P1 Exponer resource `messagebus://handoffs`.
- [x] P1 Exponer resource `messagebus://witnesslog`.
- [x] P1 Exponer resource `messagebus://health`.
- [x] P1 Tools read-only: `get_log_stats`, `verify_hash_chain`, `replay_channel`, `get_agent_inbox`, `get_agent_outbox`, `get_task_queue`, `export_handoff`, `export_witnesslog`.
- [ ] P2 Diseñar migracion de historial browser `localStorage` hacia JSONL durable.

# Run 5 cierre / Run 6 entrada

- [ ] P1 Crear Agent Bridge / A2A local adapter sobre MCP read-only.
- [ ] P1 Crear agent cards locales: Codex Agent, Publisher Agent, Canon Auditor Agent, Security Gate Agent, UI Agent.
- [ ] P1 Simular handoff local entre agentes sin escritura remota.
- [ ] P1 Agregar smoke `messagebus:a2a:smoke`.
- [ ] P1 Verificar que `messagebus:mcp:smoke`, `npm test`, `npx tsc -b` y `npm run build` siguen pasando.
- [ ] P2 Disenar resources derivados `messagebus://artifacts`, `messagebus://bulletin/latest`, `messagebus://security/p0`.

# Run 6 cierre / Run 7 entrada

- [x] P1 Crear Agent Bridge / A2A local adapter sobre MCP read-only.
- [x] P1 Crear agent cards locales: Codex Agent, Publisher Agent, Canon Auditor Agent, Security Gate Agent, UI Agent, MessageBus Reader Agent.
- [x] P1 Simular handoff local entre agentes sin escritura remota.
- [x] P1 Agregar smoke `agents:bridge:smoke`.
- [x] P1 Verificar `messagebus:mcp:smoke`, `npm test`, `npx tsc -b` y `npm run build`.
- [ ] P1 Crear ActionGate write proposal layer.
- [ ] P1 Crear proposals firmadas: `append_message`, `create_task`, `update_handoff`, `publish_release`.
- [ ] P1 Simular aprobacion/rechazo del operador.
- [ ] P2 Disenar storage separado de proposals sin tocar `messagebus-main.jsonl`.
