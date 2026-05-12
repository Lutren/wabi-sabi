# TASKS RUN 7

Fecha: 2026-05-12

Fingerprint entrada esperado: `MDV-AGENT-BRIDGE-RUN6-4D19`

## Objetivo

Crear ActionGate write proposal layer sobre Agent Bridge y MCP read-only.

No ejecutar escrituras reales todavia. Solo crear propuestas firmadas, validarlas y simular aprobacion/rechazo del operador.

## P0

- Mantener MCP read-only.
- No habilitar write tools MCP operacionales.
- No escribir al JSONL principal sin aprobacion explicita.
- No HTTP publico.
- No push/deploy/publicacion.
- No Supabase.
- No secretos.
- No tocar ZIP canon.

## P1

- Crear schema `WriteProposal` con:
  - `proposalId`
  - `kind`
  - `requestedByAgent`
  - `targetResource`
  - `payload`
  - `riskLevel`
  - `requiredApproval`
  - `evidence`
  - `createdAt`
  - `prevProposalHash`
  - `proposalHash`
- Crear proposal kinds:
  - `append_message`
  - `create_task`
  - `update_handoff`
  - `publish_release`
- Crear ActionGate evaluator:
  - APPROVE_SIMULATED
  - REVIEW_REQUIRED
  - BLOCKED
- Crear simulacion de aprobacion/rechazo del operador.
- Crear tests de bloqueo para deploy/push/publish/delete/secret printing.
- Exportar proposal Markdown en memoria.

## P2

- Diseñar almacenamiento futuro de proposals en JSONL separado:
  `02_RUNTIME/messagebus/proposals/proposals-local.jsonl`.
- Definir resource MCP read-only futuro:
  `messagebus://proposals/pending`.
- Diseñar bridge hacia A2A agent cards public-safe sin red publica.

## Criterio de cierre

- Proposals se crean y validan en memoria.
- `publish_release` queda `REVIEW_REQUIRED` o `BLOCKED` por defecto.
- `append_message` no escribe el ledger principal en Run 7.
- Tests pasan.
- `agents:bridge:smoke` sigue pasando.
- `messagebus:mcp:smoke` sigue pasando.
- `/telecom` sigue respondiendo 200.
