# Observacionismo Operational Canon v0.1

Fecha: 2026-05-06

Estado: `CANON_OPERATIVO_INTERNO / NO_PUBLIC_CLAIMS`

Este documento define como Observacionismo pasa de teoria/documentos a objetos
verificables: schema, dataset semilla, validador, reportes y conexion conceptual
con COMMS, lenguaje L1 y ActionGate.

No publica claims. No reemplaza CEREBRO. No mueve fuentes. No mezcla material
privado con paquetes open-dev.

## 1. Que Es Canon

Canon operativo es un concepto que tiene:

- nombre canonico y aliases;
- capa de uso;
- clasificacion epistemica;
- definicion operacional;
- DO: deconstruccion observacionista;
- IOI: recompilacion como objeto validable;
- inputs, transformaciones y outputs;
- invariantes;
- evidencia requerida;
- falsadores;
- gates;
- rutas fuente reales;
- pruebas o motivo de ausencia de pruebas;
- frontera de claim publico.

El canon no es una frase bonita ni una teoria repetida. Un concepto entra al
canon operativo cuando se puede validar, falsar, degradar o bloquear.

## 2. Estados Epistemicos

| Estado en schema | Lectura humana | Uso permitido |
|---|---|---|
| `verificado_por_prueba` | verificado por prueba | Puede usarse como contrato local si las pruebas citadas siguen pasando. |
| `proxy_operacional` | proxy operacional | Puede usarse para controlar flujo local, pero no como verdad cientifica publica. |
| `hipotesis` | hipotesis | Puede guiar investigacion o diseno; no puede tener gate `APPROVE`. |
| `metafora_canon` | metafora/canon | Puede orientar lenguaje y arquitectura; no autoriza ejecucion ni claims tecnicos. |

Regla: si un concepto no tiene evidencia suficiente, se clasifica hacia abajo.
No se asciende por intuicion.

## 3. Como Pasa A Uso Tecnico

Un concepto pasa a uso tecnico solo si cumple esta ruta:

1. Fuente real encontrada en codigo, docs, schema, test o reporte.
2. DO separa narrativa, hipotesis y funcion tecnica.
3. IOI recompila el concepto como objeto validable.
4. El objeto queda registrado en `data/observacionismo/concepts_seed.jsonl`.
5. El schema valida forma y campos obligatorios.
6. El validador falla si falta evidencia, falsador, gate o path real.
7. Si el concepto controla accion, debe conectar con ActionGate.
8. Si viaja entre agentes, debe conectar con COMMS/ObservationEnvelope.
9. Si se expresa como lenguaje, debe bajar a L1 o quedar en REVIEW.

## 4. Artefactos Canonicos

- Schema: `schemas/observacionismo_concepts.schema.json`
- Dataset: `data/observacionismo/concepts_seed.jsonl`
- Validador: `tools/observacionismo/validate_concepts.py`
- Puente COMMS/L1/ActionGate: `tools/observacionismo/bridge_concepts.py`
- Reporte JSON: `qa_artifacts/observacionismo/validate_concepts_report.json`
- Reporte Markdown: `qa_artifacts/observacionismo/validate_concepts_report.md`
- Reporte puente JSON: `qa_artifacts/observacionismo/bridge_concepts_report.json`
- Reporte puente Markdown: `qa_artifacts/observacionismo/bridge_concepts_report.md`
- Tests: `tests/test_observacionismo_concepts.py`

## 5. Conexion Con COMMS

COMMS usa `ObservationEnvelope` como unidad de evidencia. El canon operativo
define conceptos que pueden alimentar esos envelopes:

```text
concepto canonico -> evidence_required/falsifiers/gates
                 -> ObservationEnvelope
                 -> COMMS topic/outbox/handoff
                 -> Mission Control / agente receptor
```

Reglas:

- Un concepto sin `source_paths` validos no puede entrar a COMMS como claim.
- Un concepto `hipotesis` o `metafora_canon` no puede salir con gate `APPROVE`.
- Un envelope viejo sin evidencia debe ser supersedido, no reescrito.
- COMMS sigue local; no publica ni ejecuta acciones externas.

## 6. Conexion Con Lenguaje L1

L1 es el IR de cinco verbos:

```text
observar -> documentar -> verificar -> actuar -> handoff
```

El schema aporta a L1:

- `inputs`: que observa.
- `transforms`: que operacion permite.
- `outputs`: que debe producir.
- `evidence_required`: que evidencia necesita.
- `falsifiers`: que rompe el claim.
- `gates`: que permite, revisa o bloquea.

Regla de bajada:

```text
Si un concepto no puede bajar a L1 con evidencia y falsador,
queda como canon humano o hipotesis, no como accion.
```

## 7. Conexion Con ActionGate

ActionGate decide si una accion puede avanzar. El canon operacional no autoriza
acciones; solo prepara los datos para que ActionGate decida.

Ruta:

```text
concepto validado
  -> ObservationEnvelope
  -> propuesta de accion
  -> ActionGate
  -> APPROVE / REVIEW / BLOCK
  -> WitnessLog / handoff
```

Bloqueos duros:

- publicacion externa sin gate;
- accion destructiva sin gate;
- secreto, credencial o token;
- material RPG/TCG/canon privado hacia open-dev;
- claim medico, fisico, social o cientifico sin evidencia verificada;
- modelo pesado, pesos, alias o entrenamiento sin gate especifico.

## 8. CEREBRO Indexado Por Sistemas

La indexacion no mueve archivos. Solo referencia rutas canonicas existentes.

| Sistema | Funcion | Ruta CEREBRO | Ruta runtime |
|---|---|---|---|
| Sistema Cognitivo | Vision, decision, continuidad, A-S-R-O | `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\01_OBSERVACIONISMO_CORE.md`, `04_BRAIN_OS.md` | `-=MEDIOEVO=-\-=LIBROS\claudio\core\brain_os_bridge.py` |
| Sistema Nervioso | Eventos, agentes, envelopes, ejecucion local | `-=PSI=-\03_PSI_AI_FRAMEWORK.md` | `COMMS\`, `claudio\core\agent_comms.py` |
| Sistema Inmunologico | Gates, secretos, licencias, frontera privada | `-=PSI=-\canon\extensiones_formales\15_OSIT_TUIP_TUI_CANON_OPERATIVO_2026-05-05.md` | `observacion_action_gate.py`, `scan_secrets.py`, `VISIBILITY_MATRIX.md` |
| Sistema Endocrino / Regulacion | R, Phi_eff, J_c, Sigma, GhostGate | `-=PSI=-\05_PSI_TEORIA_FORMAL.md` | `observacion_engineering.py`, `obsai-core`, `residueos` |
| Sistema Digestivo / Metabolico | Curaduria, fuentes, ZIPs, duplicados | `fuentes_conversacionales\`, fichas PSI | `SOURCE_INTAKE_REGISTER.md`, `curador_preflight.py` |
| Sistema Circulatorio | COMMS, WitnessLog, handoffs | mapas CEREBRO y fichas | `COMMS\schemas\*.json`, `qa_artifacts\witness_log\*.jsonl` |
| Sistema Musculoesqueletico | OS, kernel, QEMU, build pipeline | `01_MAPA_SISTEMAS_CEREBRO_DUAT_BRAIN_OS_2026-05-05.md` | `claudio\os\duat_geodia_kernel`, `runtime\duat_geodia_*` |
| Memoria / Hipocampo | Fichas, manifests, snapshots, hashes | `_MANIFIESTOS\`, `00_FICHA_TECNICA_PSI_2026-05-05.md` | `qa_artifacts`, `docs\pending`, `runtime` |
| Lenguaje | L0/L1/L2, ObservaBit, DSL | `OBSERVACIONISMO_MINIMAL_MACHINE_LANGUAGE_2026-05-05.md` | `research\observacionismo-lab`, `claudio\core\observabit.py` |
| Juego Privado | WorldPulse, LivingWorldEvent, observacion encarnada | docs de frontera privada | `E:\Medioevo_RPG` y docs privados, no open-dev |

## 9. Wabi-Sabi En Este Canon

Wabi-Sabi queda clasificado como:

```text
ControlNode / SensoryCognitiveOrchestrator / TranslationCompiler
```

No es:

- cerebro central;
- agente especialista;
- memoria total;
- AGI completa;
- autoridad absoluta;
- reemplazo del usuario.

Si es:

- interfaz entre usuario, realidad, agentes y salida;
- detector de patrones;
- decompilador DO;
- recompilador IOI;
- traductor inter-agente;
- regulador de R;
- supervisor de coherencia;
- compilador de output.

Wabi-Sabi carga modulos desde Matrix/Biblioteca solo cuando los necesita. No
publica, borra, ejecuta, entrena o modifica fuera de permiso. Toda accion pasa
por ActionGate. Su objetivo no es "ser sabio"; es reducir R, traducir patrones
y producir artefactos verificables.

Arquitectura compacta:

```text
USUARIO / REALIDAD
  -> WABI-SABI: sensor + DO + IOI + traduccion + delegacion
  -> JEFES DE DEPARTAMENTO
  -> AGENTES ESPECIALISTAS
  -> RETORNO DE TRABAJO
  -> WABI-SABI: revision + correccion + compilacion
  -> OUTPUT FINAL AL USUARIO
```

## 10. Regla De Publicacion

Este canon es interno. `public_claim_allowed=false` por defecto.

Para permitir un claim publico en una version futura se necesitara:

- status `verificado_por_prueba`;
- minimo dos fuentes;
- minimo un test;
- sin rutas privadas;
- secret scan limpio;
- claims scan limpio;
- ActionGate especifico;
- copy publico de bajo claim.

Hasta entonces, Observacionismo se presenta como metodo operativo local,
evidence gate, workflow de agentes o simulacion sintetica, no como validacion
cientifica fuerte.

## 11. Puente Ejecutable v0.1

El puente ejecutable queda definido en
`docs/observacionismo/COMMS_L1_ACTIONGATE_BRIDGE_V0_1.md`.

Ruta:

```text
concepts_seed.jsonl
  -> validate_concepts.py
  -> bridge_concepts.py
  -> ObservationEnvelope local
  -> L1 safe plan
  -> ActionGate payload
  -> reporte / COMMS topic / WitnessLog
```

Reglas:

- `source_kind` para el bridge COMMS es `generated_artifact`.
- `ACTUAR` en L1 queda como `nop` hasta que exista ActionGate concreto.
- los payloads ActionGate mantienen `no_external_action`, `no_delete` y
  `no_move`;
- hipotesis, metaforas y matematicas proxy no salen con claim publico;
- el registro COMMS/WitnessLog es append-only, no edicion historica.
