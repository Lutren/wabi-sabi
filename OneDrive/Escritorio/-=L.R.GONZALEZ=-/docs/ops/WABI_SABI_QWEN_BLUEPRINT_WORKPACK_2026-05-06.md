# Wabi-Sabi Qwen Blueprint Workpack - 2026-05-06

## ESTADO

- Prompt relacionado: `13. OSIT Resource Optimizer` y carril Wabi-Sabi.
- Gate: `REVIEW_POLICY_ONLY`.
- Host: `JAMMING/BLOCK`.
- Modelo base conceptual: `qwen2.5-coder:3b`.
- Fallback local de triage: `qwen2.5:0.5b`.
- Prohibido: cloud routes, aliases Ollama, LoRA/QLoRA/DPO, mutacion de pesos, benchmarks pesados.

## DECISION

Wabi-Sabi debe modificar primero el entorno operacional alrededor del modelo, no el peso:

1. `ObservationEnvelope` antes de prompt.
2. `ActionGate` antes de tool/use/write.
3. `WitnessLog` despues de cada decision.
4. `Residue/R/Phi_eff` como senales de control.
5. Dataset chosen/rejected observacionista.
6. Evals/falsadores.
7. Solo despues evaluar adapters/pesos fuera de este host o con gate limpio.

## BLUEPRINTS LOCALES A BUSCAR

Sin navegacion externa en este gate. Buscar primero en disco:

- `runtime/model_router/Modelfile.qwen_observador_candidate`
- `runtime/model_router/qwen_observacion_contract.json`
- `runtime/model_router/qwen_observacion_gate_report.json`
- `runtime/model_router/qwen_health.json`
- `runtime/model_router/qwen_triage_health.json`
- `core/model_router.py`
- `core/qwen_observacion_engine.py`
- `tools/qwen_observacion_gate_report.py`
- `tools/benchmark_qwen_observador.py`
- `datasets/qwen_observacion_seed_preferences.jsonl`

## HIPOTESIS DE MODIFICACION

| capa | cambio | riesgo | evidencia requerida |
|---|---|---|---|
| prompt/system | compactar instrucciones observacionistas | bajo | test de no hidden-thought, formato CERTEZA/INFERENCIA |
| router | degradar por host gate y task risk | bajo/medio | test router + gate report |
| action gate | bloquear externo/private/heavy/destructive | bajo | falsadores BLOCK |
| dataset | pares chosen/rejected revisados | medio | 20+ ejemplos aceptados |
| eval | medir evidencia, ruido, accion, handoff | medio | suite reproducible |
| adapter/pesos | no tocar en este host | alto | gate futuro + maquina limpia |

## SIGUIENTE ACCION SEGURA

Crear un `QWEN_BLUEPRINT_INDEX` local desde archivos existentes, con hashes y limites. No ejecutar benchmark pesado ni navegar web mientras host este `BLOCK`.
