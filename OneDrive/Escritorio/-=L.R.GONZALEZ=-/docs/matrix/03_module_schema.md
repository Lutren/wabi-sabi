# Matrix Module Schema

Estado: `SCHEMA_DOC / VALIDATED_BY_TOOLS_MATRIX`.

Cada modulo vive en `library/modules/<module_id>.json`.

Campos obligatorios:

| campo | tipo | funcion |
|---|---|---|
| `module_id` | string | id estable y nombre de archivo |
| `name` | string | nombre humano |
| `version` | string | version semantica |
| `fingerprint` | string | huella local no cientifica |
| `domain` | string | dominio de recuperacion |
| `purpose` | string | para que existe |
| `minimal_summary` | string | resumen corto cargable |
| `DO_deconstruction` | array | como separa estimulo/evidencia/riesgo |
| `IOI_recompilation` | array | como recompila tarea ejecutable |
| `primitives` | array | piezas fundamentales |
| `inputs` | array | entradas esperadas |
| `outputs` | array | salidas esperadas |
| `invariants` | array | reglas que no se rompen |
| `interfaces` | object | CLI, files, COMMS o APIs |
| `dependencies` | array | modulos requeridos |
| `compatible_modules` | array | modulos recomendados |
| `forbidden_combinations` | array | mezclas bloqueadas |
| `safety_constraints` | array | limites y gates |
| `evidence_sources` | array | rutas o fuentes locales |
| `examples` | array | ejemplos pequenos |
| `tests` | array | validaciones esperadas |
| `decay_policy` | string | cuando revisar |
| `update_policy` | string | como actualizar |
| `handoff_template` | object | paquete minimo para otro agente |

## Criterio de calidad

Un modulo debe caber en contexto sin arrastrar canon privado. Si requiere mas
de una pagina de conocimiento, debe dividirse en otro modulo mas fundamental.
