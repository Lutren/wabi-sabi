# OSIT Resource Optimizer - Runtime Spec

Estado: `SPEC_APLICABLE / POLICY_ONLY / NO_MODEL_ROUTER_CHANGE`

Fuentes:

- `C:\Users\L-Tyr\OneDrive\Escritorio\promts\## ESTADO2.txt`
- `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\.py`

## Proposito

Convertir OSIT en un gobernador de recursos para agentes locales. No decide
verdad fisica ni autonomia. Decide el recurso minimo que mantiene calidad,
seguridad y trazabilidad.

## Entradas

| campo | rango | uso |
|---|---:|---|
| `uncertainty` | 0-1 | residuo cognitivo de la tarea |
| `evidence_strength` | 0-1 | fuerza de evidencia local disponible |
| `goal_clarity` | 0-1 | claridad del objetivo del usuario |
| `contradiction` | 0-1 | conflicto entre fuentes o instrucciones |
| `novelty` | 0-1 | novedad del problema |
| `risk` | 0-1 | riesgo de accion/salida |
| `context_pressure` | 0-1 | presion de contexto/tokens |
| `cost_pressure` | 0-1 | presion de coste/latencia |

## Salidas

| salida | significado |
|---|---|
| `selected_route` | cache, small_model, standard_model, strong_model, retrieval, batch, human_review |
| `retrieval_required` | si se debe buscar evidencia antes de responder |
| `compression_required` | si se debe compactar contexto |
| `memory_write_allowed` | si se puede escribir memoria estable |
| `max_output_tokens` | presupuesto de salida recomendado |
| `retry_policy` | estrategia si falla la primera salida |
| `action_gate` | APPROVE, REVIEW o BLOCK |

## Reglas iniciales

| condicion | decision |
|---|---|
| `risk >= 0.62` | `REVIEW` o modelo fuerte + verificacion |
| `evidence_strength < 0.48` | RAG/evidencia antes de respuesta |
| `0.48 <= evidence_strength < 0.68` | RAG ligero si hay riesgo, novedad o contradiccion |
| `Phi_eff >= 0.76` y riesgo bajo | modelo pequeno o ruta barata primero |
| `context_pressure >= 0.62` | compresion previa |
| similitud cache `>= 0.92` y riesgo bajo | cache permitido |
| accion irreversible | `REVIEW/BLOCK`, no automatizar |
| memoria no estable/util/especifica/consentida | no escribir memoria |
| retry sin cambio de estrategia | maximo 1 |

## Integracion Claudio

Orden seguro:

1. Crear tests de decision con perfiles sinteticos.
2. Crear adapter policy-only que no llame modelos.
3. Conectar a Wabi-Sabi/Sentido Comun como recomendacion.
4. Conectar a Mission Control como lectura.
5. Solo despues evaluar integracion con router real.

No tocar en esta fase:

- `core/model_router.py`
- alias Ollama
- training/LoRA
- llamadas externas
- memorias privadas sin consentimiento explicito

## Falsadores

| claim | falsador |
|---|---|
| Reduce coste sin perder calidad | comparar contra baseline fuerte en fixture sintetico; si baja calidad bajo umbral, falla |
| Reduce R operativo | tareas con contradiccion deben escalar a evidencia/revision; si responde directo, falla |
| Evita cache inseguro | prompt de riesgo alto con similitud alta no debe usar cache; si lo usa, falla |
| Controla contexto | perfil `context_pressure >= 0.62` debe activar compresion; si no, falla |
| No sobreactua | tarea clara/bajo riesgo no debe usar modelo fuerte; si lo usa por defecto, falla |

## Handoff

Fingerprint: `OSIT_RESOURCE_OPTIMIZER_RUNTIME_2026-05-06_76F80E0A`

Brief:

El optimizador OSIT se adopta como politica local de recursos para Claudio y
Wabi-Sabi. Entra por tests y adapter policy-only, no por cambios directos al
router ni por promesas de autonomia.
