# DUAT Falsifiers Required

Estado: `FALSIFIER_CANON / REQUIRED_BEFORE_ACTION`.

Cada claim DUAT debe tener falsador antes de usarse en Claudio, Mission Control,
copy publico o producto.

## Falsadores iniciales

| claim_id | falsador | decision si falla |
|---|---|---|
| `duat_public_boundary` | salida publica no contiene fuentes privadas ni gate abierto | `BLOCK` |
| `readonly_adapter` | `write/apply` fallan y no hay metodos de mutacion externa | `BLOCK` |
| `duat_claims_low` | claims publicos no contienen promesas medicas, fisicas, sociales o de seguridad | `BLOCK` |
| `living_world_fixture_contract` | fixture tiene 10 NPCs, 3 zonas, 20 eventos y salida `LivingWorldEvents` | `REVIEW` |
| `source_registry_hashes` | cada fuente existente tiene SHA256 o hash de manifiesto | `REVIEW` |
| `comms_actiongate` | COMMS tiene ObservationEnvelope, ActionGate y WitnessLog | `REVIEW` |

## Claims bloqueados por defecto

- predecir sociedades reales;
- diagnosticar medicina, neurologia, bacterias, proteinas o mercados;
- afirmar nueva fisica validada;
- prometer seguridad garantizada;
- declarar autonomia infalible;
- publicar DUAT/GEODIA interno;
- exportar RPG/TCG, lore, assets, prompts o runtime.

## Regla operativa

Si un claim no aparece en este registro, `falsify(claim_id)` debe devolver
`BLOCK`. La falta de falsador no es evidencia positiva.

## Wabi-Sabi

Wabi-Sabi usa estos falsadores como sensores de cierre: si el resultado falla,
debe traducir una correccion al agente responsable o escalar a humano/REVIEW.
No debe convertir inferencias DUAT en verdad operacional sin evidencia.
