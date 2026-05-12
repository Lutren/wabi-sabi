# DECISIONS

- 2026-05-12T01:31:46: Primera corrida `MDV-LIVE-TREE-NO-ARCHIVE-v2` queda no destructiva.
- `ROOT_BRAIN_OS` queda como canon base `PARTIAL`, no como reemplazo completo del runtime vivo.
- `DELETE_AFTER_COVERAGE` es una categoria de revision, no permiso de borrado.
- Publicacion, push y deploy quedan bloqueados mientras `10_QUALITY/SECRET_SCAN_REPORT.md` tenga hallazgos.
- 2026-05-12 Run 2: `DUAT Telecom Core` queda definido como bus local mock, no como backend externo.
- 2026-05-12 Run 2: `/telecom` en React/Vite es la consola local del MessageBus.
- 2026-05-12 Run 2: A2A y MCP quedan como adaptadores futuros, no como red publica ni servidor remoto en esta corrida.
# Run 3 - MessageBus Validator / Append-only Core

- `MEDIOEVO MessageBus` queda endurecido localmente con validador TypeScript, registry de canales, hash-chain y append-only log.
- La persistencia Run 3 sigue en `localStorage`; JSONL/SQLite durable queda para Run 4.
- El hash preferido es Web Crypto SHA-256; el fallback existe solo como `NOT_CRYPTOGRAPHIC` para runtimes sin soporte.
- MCP queda como plan read-only; no se implementan tools de escritura sin ActionGate.
- El ZIP reconstructivo v12.2.1 sigue en `SECURITY_REVIEW`; se calculo SHA256 y se listaron nombres internos sin extraccion.

# Run 4 - Durable JSONL

- El acceso durable a disco del MessageBus se implementa solo en scripts Node-only; no entra al bundle React/Vite.
- `messagebus-main.jsonl` queda como ledger durable inicial para Run 5.
- `/telecom` conserva `localStorage` y solo muestra estado/plan durable.
- MCP read-only queda como siguiente run; no se crea servidor en Run 4.

# Run 5 - MCP read-only

- `MEDIOEVO MessageBus` queda expuesto por servidor MCP real stdio/local usando `@modelcontextprotocol/sdk`.
- Los handlers MCP son Node-only y viven bajo `scripts/messagebus`; React no importa SDK MCP ni acceso a disco.
- Resources habilitadas: `messagebus://logs`, `messagebus://channels`, `messagebus://agents`, `messagebus://tasks`, `messagebus://handoffs`, `messagebus://witnesslog`, `messagebus://health`.
- Tools habilitadas son solo lectura: `get_log_stats`, `verify_hash_chain`, `replay_channel`, `get_agent_inbox`, `get_agent_outbox`, `get_task_queue`, `export_handoff`, `export_witnesslog`.
- Cualquier tool con verbo write queda bloqueada por `mcpReadOnlyGuards`.
- Run 6 debe construir Agent Bridge / A2A local adapter sobre MCP read-only, no sobre backend externo.
