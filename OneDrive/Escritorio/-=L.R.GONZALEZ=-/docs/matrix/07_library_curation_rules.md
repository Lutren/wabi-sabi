# Matrix Library Curation Rules

Estado: `CURATION_RULES / SETO_COMPATIBLE`.

## Regla de entrada

Ningun modulo entra por entusiasmo. Entra si tiene:

- proposito minimo;
- evidencia local;
- invariantes;
- limites;
- tests o falsadores;
- handoff;
- decay policy.

## Estados

| estado | significado |
|---|---|
| `ACTIVE` | cargable por WabiSabi |
| `REVIEW` | requiere curacion o evidencia |
| `BLOCK` | no cargar ni delegar |
| `DEPRECATED` | reemplazado por otro modulo |

## Criterios de poda

Un modulo se divide o archiva si:

- mezcla dominios sin necesidad;
- no tiene fuente;
- no tiene salida verificable;
- repite otro modulo;
- aumenta R sin reducir incertidumbre;
- contiene claims privados o fuertes.

## Actualizacion

Cada cambio debe actualizar:

1. modulo JSON;
2. `library/index.json`;
3. prueba del validador;
4. handoff si afecta agentes;
5. WitnessLog si se integra a COMMS.
