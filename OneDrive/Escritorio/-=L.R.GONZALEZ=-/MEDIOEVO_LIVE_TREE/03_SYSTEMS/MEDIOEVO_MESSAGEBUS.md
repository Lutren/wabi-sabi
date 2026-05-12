# MEDIOEVO MessageBus

Estado: mock local con `localStorage` en React.

Actualizacion Run 3: core local validable con schema validator, channel registry, hash-chain, append-only log y exportadores. La UI mock sigue existiendo, pero el siguiente contrato operativo es el ledger append-only.

Actualizacion Run 4: existe ledger durable JSONL en disco y scripts Node-only para append, verify, replay, stats y export-md. React/Vite no importa acceso a disco.

Actualizacion Run 5: existe servidor MCP read-only local por stdio sobre el ledger durable JSONL. Las resources y tools MCP viven fuera de React y quedan bloqueadas para escritura por `mcpReadOnlyGuards`.

Implementacion UI: `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\src\messagebus`

## Flujo

1. Un agente crea un `AgentMessage`.
2. El mensaje entra como `draft` o `queued`.
3. `sendMessage(messageId)` cambia el estado a `sent`.
4. El receptor usa `ackMessage(messageId, agentId)`.
5. Si cierra la accion, `resolveMessage(messageId, agentId)`.
6. Si hay riesgo, `blockMessage(messageId, reason)`.
7. Cada cierre relevante puede llamar `appendWitnessEvent(event)`.
8. Exports locales: `exportBulletinMarkdown()` y `exportMessageBusJson()`.

## Funciones implementadas

| Funcion | Estado | Descripcion |
|---|---|---|
| `createMessage(input)` | Implementada | Crea mensaje con id y hash deterministico simple. |
| `sendMessage(messageId)` | Implementada | Marca mensaje como `sent`. |
| `ackMessage(messageId, agentId)` | Implementada | Agrega ACK; pasa a `acknowledged` si todos los destinatarios confirmaron. |
| `resolveMessage(messageId, agentId)` | Implementada | Marca mensaje como `resolved`. |
| `blockMessage(messageId, reason)` | Implementada | Marca mensaje como `blocked` y agrega razon. |
| `createHandoffMessage(handoff)` | Implementada | Crea handoff P1 con fingerprint. |
| `appendWitnessEvent(event)` | Implementada | Agrega evento hash-chain mock. |
| `getInbox(agentId)` | Implementada | Filtra por `to_agents` y `cc_agents`. |
| `getChannel(channelId)` | Implementada | Devuelve canal por id. |
| `getOpenP0()` | Implementada | Devuelve P0 no resueltos ni archivados. |
| `exportBulletinMarkdown()` | Implementada | Export local Markdown. |
| `exportMessageBusJson()` | Implementada | Export local JSON. |

## Persistencia

Run 2 usa:

- `localStorage` key: `duat-telecom-core:messagebus:v1`.
- Seed mock: `src/messagebus/seed.ts`.
- Estado en memoria dentro de `createMessageBusStore()`.

No usa:

- Supabase.
- API externa.
- Credenciales.
- Red.

## MCP read-only Run 5

Servidor:

- `C:\Users\L-Tyr\OneDrive\Documentos\New project 3\scripts\messagebus\mcp-server.mjs`

Smoke:

- `npm run messagebus:mcp:smoke`

Resources:

- `messagebus://logs`
- `messagebus://channels`
- `messagebus://agents`
- `messagebus://tasks`
- `messagebus://handoffs`
- `messagebus://witnesslog`
- `messagebus://health`

Tools read-only:

- `get_log_stats`
- `verify_hash_chain`
- `replay_channel`
- `get_agent_inbox`
- `get_agent_outbox`
- `get_task_queue`
- `export_handoff`
- `export_witnesslog`

No implementa:

- write tools;
- servidor HTTP publico;
- backend externo;
- Supabase;
- push/deploy/publicacion.

## Contrato futuro

La migracion recomendada es:

1. Mantener tipos TypeScript como contrato de UI.
2. Crear adaptador local SQLite o JSONL append-only.
3. Guardar `AgentMessage` y `WitnessEvent` como registros hash-chain.
4. Agregar validador CLI que compruebe:
   - hash previo;
   - canales permitidos;
   - `MessageKind` permitido por canal;
   - evidencia existente;
   - rutas secret-like bloqueadas.
