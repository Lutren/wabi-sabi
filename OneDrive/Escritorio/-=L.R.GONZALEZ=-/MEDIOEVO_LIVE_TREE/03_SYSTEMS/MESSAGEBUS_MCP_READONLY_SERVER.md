# MESSAGEBUS MCP READ-ONLY SERVER

Fecha: 2026-05-12

Producto: DUAT Telecom Core

Nombre tecnico: MEDIOEVO MessageBus

Estado: MCP_READONLY_STDIO_VALIDADO

## Proposito

El servidor MCP read-only permite que otros agentes consulten el ledger durable del `MEDIOEVO MessageBus` sin capacidad de mutacion.

Fuente unica Run 5:

`MEDIOEVO_LIVE_TREE/02_RUNTIME/messagebus/logs/messagebus-main.jsonl`

## Arquitectura

Implementacion Node-only:

- `scripts/messagebus/mcp-server.mjs`
- `scripts/messagebus/mcp-smoke.mjs`
- `scripts/messagebus/lib/mcpResources.mjs`
- `scripts/messagebus/lib/mcpTools.mjs`
- `scripts/messagebus/lib/mcpReadOnlyGuards.mjs`
- `scripts/messagebus/lib/mcpSchemas.mjs`

Reutiliza Run 4:

- JSONL reader y stats.
- Replay desde cero.
- Verificador de schema/canales/hash-chain.
- Export Markdown.

El cliente React no importa estos modulos.

## Transporte

Transporte activo: `stdio/local`.

Script:

```powershell
npm run messagebus:mcp
```

No se crea servidor HTTP publico. No se abre puerto externo. No hay deploy.

## Resources

| Resource | Devuelve |
|---|---|
| `messagebus://logs` | ruta logica, conteos, timestamps, tamano, ultimo hash, health summary |
| `messagebus://channels` | canales detectados, conteo por canal, kinds, ultimo mensaje por canal |
| `messagebus://agents` | agentes detectados, inbox/outbox count, ultimo mensaje por agente |
| `messagebus://tasks` | task queue reconstruida desde replay |
| `messagebus://handoffs` | handoff stream y ultimo handoff |
| `messagebus://witnesslog` | eventos observables, decisiones y hashes relacionados |
| `messagebus://health` | schema, channels, hash-chain, duplicate ids, replay, read-only mode |

## Tools read-only

| Tool | Mutacion | Resultado |
|---|---|---|
| `get_log_stats` | No | stats del log principal |
| `verify_hash_chain` | No | validez, linea rota, duplicados, errores schema/canal |
| `replay_channel` | No | mensajes reconstruidos de un canal |
| `get_agent_inbox` | No | mensajes dirigidos a un agente |
| `get_agent_outbox` | No | mensajes emitidos por un agente |
| `get_task_queue` | No | tareas reconstruidas y agrupadas por estado |
| `export_handoff` | No | handoff Markdown o JSON devuelto en memoria |
| `export_witnesslog` | No | WitnessLog Markdown o JSON devuelto en memoria |

## Read-only guard

Archivo:

`scripts/messagebus/lib/mcpReadOnlyGuards.mjs`

Bloquea tools que contengan estos verbos:

`create`, `append`, `write`, `update`, `delete`, `remove`, `mutate`, `rotate`, `import`, `sync`, `push`, `deploy`, `publish`, `send`, `execute`.

Tambien se prueba que:

- las tools registradas no usen verbos de escritura;
- los modulos MCP no llamen `appendMessageToJsonl`;
- los handlers no modifiquen el JSONL durante consultas;
- React no importe MCP SDK ni modulos Node-only.

## Por que no escribe

- No se importa `appendMessageToJsonl` desde MCP.
- No se registran tools write.
- `export_handoff` y `export_witnesslog` devuelven contenido en memoria; no escriben archivos.
- El smoke envuelve llamadas en una verificacion de archivo sin cambios.
- Las futuras write tools quedan fuera de Run 5 y requieren ActionGate.

## Uso por agentes externos

Un agente externo puede configurar el proceso local:

```powershell
node scripts/messagebus/mcp-server.mjs
```

Lecturas recomendadas:

1. Leer `messagebus://health`.
2. Ejecutar `verify_hash_chain`.
3. Leer `messagebus://tasks` o `get_agent_inbox`.
4. Exportar handoff con `export_handoff`.

Regla: si `health.hashChainStatus != OK`, el agente debe detener decisiones operativas y reportar `REVIEW`.

## Estado SDK

SDK usado:

- `@modelcontextprotocol/sdk` 1.29.0
- Licencia upstream: MIT
- Transporte usado: stdio

Audit:

- `npm audit --omit=dev --json`: 0 vulnerabilidades prod.
- `npm audit --json`: 5 moderadas dev en Vite/Vitest/esbuild; upgrade mayor pendiente, no bloquea MCP local read-only.
