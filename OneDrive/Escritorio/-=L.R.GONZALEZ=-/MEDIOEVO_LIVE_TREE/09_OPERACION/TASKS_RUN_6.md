# TASKS RUN 6

Fecha: 2026-05-12

Fingerprint entrada esperado: `MDV-MESSAGEBUS-RUN5-91C7`

## Objetivo

Crear Agent Bridge / A2A local adapter sobre MCP read-only sin escritura remota.

## P0

- Mantener MCP read-only.
- No habilitar write tools.
- No HTTP publico.
- No push/deploy/publicacion.
- No Supabase.
- No secretos.
- No tocar ZIP canon.

## P1

- Crear agent cards locales:
  - Codex Agent
  - Publisher Agent
  - Canon Auditor Agent
  - Security Gate Agent
  - UI Agent
- Crear adaptador A2A local que consuma:
  - `messagebus://health`
  - `messagebus://agents`
  - `messagebus://tasks`
  - `messagebus://handoffs`
  - `messagebus://witnesslog`
- Crear simulacion local de handoff entre agentes usando solo lectura MCP y fixtures.
- Crear tests para routing de agentes, lectura de inbox/outbox y bloqueo de acciones write.
- Agregar smoke `messagebus:a2a:smoke`.

## P2

- Diseñar migracion de historial browser `localStorage` hacia JSONL durable.
- Agregar resources derivados:
  - `messagebus://artifacts`
  - `messagebus://bulletin/latest`
  - `messagebus://security/p0`
- Diseñar ActionGate para futuras write tools, sin implementarlas.

## Criterio de cierre

- Agent cards locales existen.
- A2A adapter local no escribe archivos.
- Smoke A2A pasa.
- `messagebus:mcp:smoke` sigue pasando.
- `npm test`, `npx tsc -b`, `npm run build` pasan.
- `/telecom` sigue respondiendo 200.
- Handoff Run 6 creado.
