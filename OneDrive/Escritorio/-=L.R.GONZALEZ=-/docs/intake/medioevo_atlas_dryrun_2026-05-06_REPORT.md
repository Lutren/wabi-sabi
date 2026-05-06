# Curador SETO Tree Absorption

Generated UTC: `2026-05-06T06:52:48.964057+00:00`

Estado: `FICHADO / ABSORBIDO_A_ATLAS / LIMPIEZA_SEGURA_PARCIAL`

## Rutas

- `medioevo`: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-`

## Resumen

- Archivos registrados: `14806`
- Duplicados exactos detectados: `2816` archivos en grupos duplicados
- Eliminados seguros en este pase: `0`

## Estados

| estado | archivos |
|---|---:|
| `BLOQUEADO` | 1486 |
| `BLOQUEADO_PUBLICACION` | 18 |
| `CANONICAL_DUPLICATE_KEEP` | 749 |
| `DELETE_CANDIDATE` | 42 |
| `FICHADO` | 10952 |
| `REVIEW` | 1559 |

## Carriles

| carril | archivos |
|---|---:|
| `assets` | 477 |
| `claudio-wabisabi` | 10957 |
| `cleanup` | 1 |
| `curaduria` | 438 |
| `duat-geodia` | 373 |
| `privado-bloqueado` | 1486 |
| `psi-observacionismo` | 1045 |
| `publicacion` | 29 |

## Decisiones

| decision | archivos |
|---|---:|
| `ABSORB_AS_RESEARCH_BOUNDARY` | 18 |
| `ABSORB_TO_ATLAS` | 10952 |
| `BLOCK_KEEP_PRIVATE` | 1486 |
| `DELETE_EXACT_DUPLICATE_AFTER_HASH` | 41 |
| `DELETE_REGENERABLE_AFTER_LOG` | 1 |
| `KEEP_CANONICAL` | 749 |
| `REVIEW_DUPLICATE` | 1559 |

## Veredicto

- La absorcion de este pase crea fichas por archivo y manifest estructurado.
- `Downloads` se trata como zona de amenaza: nada descargado se ejecuta, extrae o publica antes de clasificar riesgo.
- Lo unico que puede retirarse automaticamente es duplicado exacto o basura regenerable con hash y gate.
- Los documentos unicos, privados, de claims fuertes o con frontera de publicacion quedan `REVIEW` o `BLOQUEADO`; no se borran.

## Archivos eliminados

Ninguno.

## Siguiente limpieza permitida

1. Revisar `REVIEW_DUPLICATE` que no estaban en carpeta archive/copia.
2. Convertir fuentes unicas grandes en fichas de concepto antes de archivo frio.
3. No publicar ni abrir OSIT-QG/OSIT-AG/GEODIA sin falsadores y claims boundary.
4. Si una carpeta queda solo como archivo frio ya absorbido, moverla completa en una fase separada con rollback.
