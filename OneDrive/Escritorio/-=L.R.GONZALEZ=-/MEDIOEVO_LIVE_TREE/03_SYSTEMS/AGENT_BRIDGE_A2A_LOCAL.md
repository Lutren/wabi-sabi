# AGENT BRIDGE A2A LOCAL

Fecha: 2026-05-12

Estado: VALIDADO_LOCAL_READMOSTLY

## Proposito

El Agent Bridge agrega una capa local de coordinacion entre agentes sobre el MCP read-only del `MEDIOEVO MessageBus`.

No es una red A2A publica. No abre puertos. No escribe al JSONL durable. No publica ni ejecuta acciones externas.

## Arquitectura

Implementacion Node-only:

- `scripts/agents/agent-bridge-smoke.mjs`
- `scripts/agents/lib/agentCardSchema.mjs`
- `scripts/agents/lib/agentRegistry.mjs`
- `scripts/agents/lib/localA2AEnvelope.mjs`
- `scripts/agents/lib/agentRouter.mjs`
- `scripts/agents/lib/handoffSimulator.mjs`
- `scripts/agents/lib/decisionTrace.mjs`
- `scripts/agents/lib/bridgeHealth.mjs`
- `scripts/agents/lib/mcpClientAdapter.mjs`

Agent Cards:

- `codex-agent`
- `publisher-agent`
- `canon-auditor-agent`
- `security-gate-agent`
- `ui-agent`
- `messagebus-reader-agent`

## Agent Cards

Cada card declara:

- `id`
- `name`
- `version`
- `role`
- `description`
- `capabilities`
- `allowedInputs`
- `allowedOutputs`
- `forbiddenActions`
- `mcpToolsAllowed`
- `handoffTargets`
- `safetyMode`
- `readOnlyByDefault`
- `requiresOperatorApprovalFor`
- `fingerprint`

Regla Run 6: `readOnlyByDefault` debe ser `true`.

## Agent Registry

El registry carga cards desde `scripts/agents/cards/*.card.json`, valida schema y exige los seis agentes minimos.

No escribe archivos. Solo produce una vista en memoria:

- lista de agentes;
- busqueda por `id`;
- verificacion de required agents.

## Envelope A2A local

Schema:

- `envelopeId`
- `protocol: "medioevo-a2a-local"`
- `version`
- `fromAgent`
- `toAgent`
- `intent`
- `taskRef`
- `handoffRef`
- `message`
- `requiredMcpReads`
- `proposedActions`
- `blockedActions`
- `evidence`
- `createdAt`
- `traceId`
- `prevTraceHash`
- `traceHash`

El envelope describe y enruta. No ejecuta acciones.

## Router

Routing minimo:

| Intencion | Agente |
|---|---|
| deploy / GitHub / release / publish | Publisher Agent |
| secret / token / private-public boundary | Security Gate Agent |
| canon / coverage / zip / source trace | Canon Auditor Agent |
| UI / route / visual / `/telecom` | UI Agent |
| MessageBus / MCP / replay / hash / handoff | MessageBus Reader Agent |
| code / tests / implementation | Codex Agent |

Prioridad: seguridad gana sobre publicacion. Un texto como `secret scan before publishing` se enruta a `security-gate-agent`.

## Read-only guard

Acciones bloqueadas:

- `create_remote`
- `append_log`
- `write_log`
- `update_log`
- `delete`
- `remove`
- `mutate`
- `rotate`
- `import`
- `sync_remote`
- `push`
- `deploy`
- `publish`
- `send_external`
- `execute_shell_unapproved`

Acciones permitidas:

- `read`
- `inspect`
- `verify`
- `replay`
- `summarize`
- `route`
- `simulate`
- `propose`
- `export_in_memory`

## MCP read-only dependency

El bridge consume handlers puros de Run 5:

- `messagebus://health`
- `messagebus://agents`
- `messagebus://tasks`
- `messagebus://handoffs`
- `messagebus://witnesslog`
- `get_log_stats`
- `verify_hash_chain`
- `replay_channel`
- `export_handoff`
- `export_witnesslog`

No usa MCP write tools porque no existen en Run 6.

## Handoff Simulator

`handoffSimulator.mjs`:

1. Consulta MCP health/hash/handoffs.
2. Crea envelope local.
3. Enruta al agente correcto.
4. Devuelve `selectedAgent`, `reason`, `allowedActions`, `blockedActions`, `evidence`, `nextSuggestedPrompt`, `traceHash`.

No escribe al log principal.

## Decision Trace

`decisionTrace.mjs` crea hashes deterministas y puede exportar Markdown en memoria.

El trace incluye:

- evidence refs;
- routing reason;
- allowed actions;
- blocked actions;
- timestamp;
- `traceHash`.

## Que NO hace todavia

- No crea write tools MCP.
- No llama `appendMessageToJsonl`.
- No escribe al JSONL durable principal.
- No abre red publica.
- No ejecuta deploy/push/publicacion.
- No reemplaza ActionGate.

## Como prepara Run 7

Run 7 debe crear una capa de propuestas firmadas:

- `append_message proposal`
- `create_task proposal`
- `update_handoff proposal`
- `publish_release proposal`

La propuesta se puede simular y validar, pero su ejecucion requiere aprobacion explicita del operador por ActionGate.
