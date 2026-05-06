# DUAT Public / Private Boundary

Estado: `BOUNDARY_CANON / ENFORCED_BY_ADAPTER`.

## Regla central

No mezclar publico y privado.

`duat-genesis` es un sandbox publico sintetico. DUAT/GEODIA interno, Brain OS,
Claudio local, RPG, TCG, prompts, datasets, runtime y arquitectura completa son
carriles privados o de revision.

## Publico permitido

| tipo | permitido | condicion |
|---|---|---|
| Codigo | contratos pequenos, SDKs, ejemplos sinteticos | MIT, sin datos privados |
| Docs | low-claim, falsadores, frontera, ejemplos | sin rutas privadas ni secretos |
| Fixtures | sinteticos, genericos, reproducibles | sin lore, assets ni datos reales |
| Copy | "synthetic sandbox" y "evidence before action" | sin promesas fuertes |

## Privado o bloqueado

| tipo | decision |
|---|---|
| DUAT/GEODIA interno | privado, local, research-only |
| RPG/TCG | propietario, no publicar |
| WorldPulse/LivingWorld real | privado |
| Prompts internos y thresholds | privado |
| Datasets reales o con licencia pendiente | REVIEW/BLOCK |
| Claims de prediccion social real | BLOCK |
| Medicina, diagnostico, seguridad garantizada o nueva fisica probada | BLOCK |

## Formato de decision

- Estado actual: dos carriles DUAT existen en el repo.
- Problema: sin adapter, Claudio podia confundir fuente publica con motor privado.
- Principio aplicado: separar por funcion, licencia, privacidad y claim level.
- Accion propuesta: usar `DuatReadonlyAdapter` como unica interfaz DUAT hacia Claudio por ahora.
- Riesgo: filtracion de ingenieria privada o claims altos si se lee bruto.
- Reversibilidad: alta; el adapter no escribe ni mueve archivos.
- Resultado esperado: reportes, hashes y falsadores disponibles sin mezclar carriles.

## Criterio de salida publica

Antes de publicar cualquier pieza DUAT:

1. `source_registry` debe clasificarla como publica o sintetica.
2. `falsify("duat_public_boundary")` debe pasar.
3. `falsify("duat_claims_low")` debe pasar.
4. Secret scan debe reportar `0` hallazgos no permitidos.
5. ActionGate debe aprobar el target exacto.
