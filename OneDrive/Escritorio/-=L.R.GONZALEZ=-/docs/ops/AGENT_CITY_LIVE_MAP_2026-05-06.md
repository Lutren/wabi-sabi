# Agent City Live Map - 2026-05-06

Este reporte ejecuta el `Prompt 17 - Agentes especializados / ciudad Claudio`.
No activa agentes nuevos. No publica. No mueve ni borra archivos.

## ESTADO

- Snapshot pendiente: `active_dedup=389`, `claudio_open=69`.
- Gate general: `REVIEW`.
- Autonomia local: `A0_LOCAL_REVIEW_ONLY`.
- Agentes inventariados: `6`.
- Fuente de coordinacion previa: `docs/ops/AGENT_CITY_COORDINATION_2026-05-06.md`.
- Bus unico: `COMMS/`.

## CERTEZA

Los agentes activos registrados en `COMMS/agents_state` son:

| agente | departamento | estado | gate | ultimo artefacto declarado |
|---|---|---|---|---|
| `claudio-local-agent` | `ayuntamiento` | `ACTIVE_LOCAL_BRIDGE` | `REVIEW` | `COMMS/handoffs/2026-05-05-claudio-local-agent-seto.md` |
| `claudio-local-autonomy` | `wabi_sabi` | `A0_LOCAL_REVIEW_ONLY` | `BLOCK` | `runtime\host_observacionista\latest_report.json` y reportes model-router |
| `curador-seto` | curaduria | `ACTIVE_LOCAL_CONTRACT` | `REVIEW` | WitnessLog hash `141850cac3d72b5d22fc3378e4173bffdf7a38e48eeb5937de89e5b8d1300539` |
| `hormiguero-mission-control` | `logi` | `LOCAL_READ_SURFACE` | `REVIEW` | `CLAUDIO_AGENT_COMMS_BRIDGE_2026-05-05` |
| `publicacion-perfiles-observatorio` | `plaza-mercado` | `ACTIVE_LOCAL_STRATEGY_AGENT` | `REVIEW` | `COMMS/handoffs/2026-05-05-publicacion-perfiles-observatorio.md` |
| `wabi-sabi-sentido-comun` | `patterns` | `POLICY_ONLY_LEARNING_SOURCE` | `REVIEW` | `CLAUDIO_AGENT_COMMS_BRIDGE_2026-05-05` |

## MAPA FUNCIONAL

| funcion | dueño primario | consumidores | limite operativo |
|---|---|---|---|
| Coordinacion local y COMMS bridge | `claudio-local-agent` | todos | Puede coordinar y proponer; no pisa outbox/inbox ajenos sin handoff |
| Autonomia local allowlist | `claudio-local-autonomy` | `claudio-local-agent`, `wabi-sabi-sentido-comun` | Gate `BLOCK`; solo acciones allowlist y no externas |
| Curaduria, fichas, duplicados y fronteras | `curador-seto` | todos | Puede registrar y fichar; no borra/mueve sin gate y evidencia |
| Superficie de lectura ciudad/Mission Control | `hormiguero-mission-control` | operador, agentes | Read-only; no decide ni ejecuta acciones |
| Publicacion/perfiles/copy packets | `publicacion-perfiles-observatorio` | operador, curador | Solo estrategia local; dashboards y publicaciones quedan bloqueados |
| Politica Wabi-Sabi/sentido comun | `wabi-sabi-sentido-comun` | autonomia, Mission Control | Policy-only; no toca pesos, aliases, modelos ni acciones externas |

## SOLAPAMIENTOS

| solapamiento | riesgo | limite propuesto |
|---|---|---|
| `claudio-local-agent` y `hormiguero-mission-control` leen COMMS/Mission Control | Doble fuente de verdad de estado | `claudio-local-agent` coordina; `hormiguero-mission-control` solo renderiza lectura local |
| `claudio-local-agent` y `claudio-local-autonomy` mencionan autonomia/workpacks | Declarar autonomia amplia antes de evidencia | `claudio-local-agent` emite handoff; `claudio-local-autonomy` mantiene `A0/BLOCK` hasta gate limpio |
| `curador-seto` puede tocar `COMMS/**` y otros agentes tienen streams propios | Sobrescritura de lanes | Curador usa topics/handoffs append-only; no modifica outbox/inbox de otro agente salvo handoff explicito |
| `publicacion-perfiles-observatorio` y `curador-seto` comparten frontera publica | Preparar copy como si fuera publicacion | Publicacion prepara packets; Curador valida fichas/secrets/claims; ActionGate decide externo |
| `wabi-sabi-sentido-comun` y `claudio-local-autonomy` comparten Wabi-Sabi | Confundir policy con ejecucion | Wabi-Sabi aprende y recomienda; Autonomy ejecuta solo allowlist, con rollback/witness |
| Prompts de lenguaje/observacionismo y diffs existentes en `research/observacionismo-lab` | Pisar trabajo concurrente | Tratar esos archivos como concurrentes; solo leer o crear handoff antes de modificar |

## LIMITES POR AGENTE

### `claudio-local-agent`

- Puede: coordinar COMMS, pending review, workpacks, puente Mission Control.
- No puede: ejecutar publicacion, tocar privado, modificar streams ajenos sin handoff.
- Siguiente accion segura: consumir este mapa y mantener `Prompt 17` como reporte vivo.

### `claudio-local-autonomy`

- Puede: `pending_review`, `host_no_write`, gate reports, ObservaBit, candidato Qwen reversible, `ollama ps`, workpack externo local.
- No puede: `qwen_3b_suite`, alias Ollama, entrenamiento, acciones externas, borrado/movimiento.
- Siguiente accion segura: mantener `Autonomia Amplia` como destino, pero solo en diff-review con rollback.

### `curador-seto`

- Puede: fichar, clasificar, crear manifests, WitnessLog, queues de duplicados.
- No puede: borrar unico, mover usuario, absorber raw sources sin ficha, publicar.
- Siguiente accion segura: reducir solapamientos por ficha, no por limpieza.

### `hormiguero-mission-control`

- Puede: UI/reporte local de agentes, gates, ultimo witness y pendientes.
- No puede: iniciar daemon permanente ni convertir HealthVector en autoridad.
- Siguiente accion segura: leer `COMMS/topics/agent-city-coordination.jsonl` y este mapa.

### `publicacion-perfiles-observatorio`

- Puede: packets locales, estrategia publica, copy seguro y checklists.
- No puede: Gumroad, GitHub, LinkedIn, redes, website deploy, browser auth, sesiones ni tokens.
- Siguiente accion segura: preparar assets/copy como `READY_LOCAL`, nunca `PUBLISHED`.

### `wabi-sabi-sentido-comun`

- Puede: policy inputs, decision ledger, aprendizaje local y senales de sentido comun.
- No puede: pesos, aliases, LoRA/QLoRA/DPO, modelos pesados ni externo.
- Siguiente accion segura: trabajar con `qwen2.5-coder:3b` como blueprint/base conceptual y `qwen2.5:0.5b` como triage, sin tocar pesos.

## FUSIONES O LIMITES RECOMENDADOS

- No fusionar agentes ahora. El riesgo de romper carriles es mayor que el beneficio.
- Crear una sola vista de ciudad en Mission Control consumiendo `COMMS/agents_state`, `COMMS/topics` y `docs/ops`.
- Mantener `curador-seto` como frontera transversal, no como ejecutor de cada lane.
- Mantener `publicacion-perfiles-observatorio` separado del gate de publicacion real.
- Mantener Wabi-Sabi en tres capas:
  1. policy-only (`wabi-sabi-sentido-comun`);
  2. autonomia allowlist (`claudio-local-autonomy`);
  3. modelo local de respaldo (`qwen2.5-coder:3b` con fallback `qwen2.5:0.5b`).

## ACCION EJECUTADA

- Refrescado `pending_review`.
- Leidos los seis `COMMS/agents_state/*.json`.
- Leido el topic `COMMS/topics/agent-city-coordination.jsonl`.
- Creado este mapa vivo en `docs/ops`.
- Publicado evento local append-only en `COMMS/topics/agent-city-coordination.jsonl`.

## SIGUIENTE PASO

Siguiente prompt recomendado: `7. Claudio Mission Control / COMMS`.

Motivo: ya existe mapa de agentes; el paso natural es que Mission Control lo lea como vista local de estado, sin crear otra capa.
