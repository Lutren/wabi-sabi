# DUAT GEODIA - LClock + WitnessLog Backlog

Fecha: `2026-05-05`

Estado: `BACKLOG_TECNICO_MINIMO / REVIEW`

Fuente absorbida: `C:\Users\L-Tyr\Downloads\ESTADO.txt`

SHA256: `BE32A02C13C572D313D0A09FEFBB3AA1339FC4A2A94E860192636EF808F69875`

Ficha: `docs/intake/curador_fichas/downloads/BE32A02C13C572D3_estado.md`

## Decision

El insight aplicable ya a Claudio/GEODIA no es autonomia avanzada: es causalidad, auditoria e identidad. El primer bloque implementable queda limitado a `LClock` persistente y `WitnessLog v2` con hash-chain verificable. `Cerebro/Router` queda en `REVIEW` hasta resolver como ejecutar emulacion superficial sin LLM y sin reducirlo a lookup estatico.

## Ticket Tecnico Minimo

| id | componente | objetivo | estado | prueba requerida |
|---|---|---|---|---|
| DG-LC-001 | `LClock` | reloj causal persistente con restauracion tras restart | `NEXT_LOCAL` | `test_lclock_survives_restart()` |
| DG-WL-001 | `WitnessLog v2` | append-only local con hash-chain y evento anterior obligatorio | `NEXT_LOCAL` | modificar una entrada y detectar ruptura |
| DG-ENV-001 | `EnvelopeRecord` | contrato comun para EvidenceEnvelope, ActionGate y WitnessLog | `NEXT_LOCAL` | serializacion estable + hash reproducible |
| DG-SIG-001 | `AgentSignature` | identidad operativa con `domain_forbidden` como barrera | `REVIEW` | drift detectado si cambia dominio prohibido |
| DG-CB-001 | `ContextBroker` | transferir resultados sin transferir identidad ni memoria interna | `REVIEW` | filtrado por dominio y evidencia de no contaminacion |
| DG-CR-001 | `Cerebro/Router` | investigar emulacion superficial sin LLM | `BLOCKED_RESEARCH` | definir falsadores antes de implementar |

## Contrato `EnvelopeRecord` V0

Campos minimos no negociables:

| campo | tipo | razon |
|---|---|---|
| `envelope_id` | `str` | identidad estable del evento |
| `lclock` | `int` | orden causal reproducible |
| `timestamp_utc` | `str` | lectura humana y correlacion externa |
| `source_agent` | `str` | emisor responsable |
| `target_agent` | `str \| None` | receptor o consumidor |
| `action` | `str` | accion o decision observada |
| `evidence_refs` | `list[str]` | fuentes verificables |
| `psi_state` | `CERTEZA \| INFERENCIA \| INCOGNITA \| BLOQUEADO` | estado epistemologico |
| `action_gate` | `APPROVE \| REVIEW \| BLOCK` | decision de permiso |
| `risk_flags` | `list[str]` | residuos, secretos, claims o acciones externas |
| `payload_hash` | `str` | fingerprint de contenido sin exponer datos sensibles |
| `previous_hash` | `str` | enlace hash-chain |
| `event_hash` | `str` | hash canonico del registro |

## Invariantes

- `LClock` nunca retrocede; tras crash se restaura como minimo al ultimo valor persistido.
- `WitnessLog` no acepta evento sin `previous_hash`, salvo genesis.
- `event_hash` se calcula con JSON canonico y campos estables.
- `AgentSignature.domain_forbidden` no se relaja por merge automatico.
- `merge_permissions()` usa interseccion de permisos.
- `ContextBroker` pasa resultados y evidencias, no prompts internos, secretos, memoria privada ni identidad Sigma completa.

## Falsadores

- Cambiar una entrada vieja no rompe la verificacion de hash-chain.
- Dos eventos con el mismo contenido producen hashes distintos por serializacion no determinista.
- Un agente recibe `domain_forbidden` o memoria interna de otro agente por ContextBroker.
- Un merge aumenta permisos sin ActionGate `APPROVE`.
- Cerebro/Router responde igual si se reemplaza DUAT GEODIA por cualquier sistema multiagente generico.

## No Implementar Todavia

- Entrenamiento de pesos, LoRA/QLoRA/DPO o alias Ollama.
- Cerebro/Router adaptativo hasta resolver la pregunta de emulacion superficial sin LLM.
- Publicacion externa, red, acciones sobre navegador o Gumroad.
- Claims de conciencia, nueva fisica, diagnostico, prediccion social o seguridad garantizada.
