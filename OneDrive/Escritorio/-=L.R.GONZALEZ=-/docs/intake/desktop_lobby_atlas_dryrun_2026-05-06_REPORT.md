# Curador SETO Tree Absorption

Generated UTC: `2026-05-06T07:02:32.432179+00:00`

Estado: `FICHADO / ABSORBIDO_A_ATLAS / LIMPIEZA_SEGURA_PARCIAL`

## Rutas

- `desktop`: `C:\Users\L-Tyr\OneDrive\Escritorio`

## Resumen

- Archivos registrados: `1753`
- Duplicados exactos detectados: `169` archivos en grupos duplicados
- Eliminados seguros en este pase: `0`

## Estados

| estado | archivos |
|---|---:|
| `BLOQUEADO` | 74 |
| `BLOQUEADO_PUBLICACION` | 4 |
| `CANONICAL_DUPLICATE_KEEP` | 72 |
| `DELETE_CANDIDATE` | 1 |
| `FICHADO` | 1507 |
| `REVIEW` | 95 |

## Carriles

| carril | archivos |
|---|---:|
| `claudio-wabisabi` | 922 |
| `cleanup` | 1 |
| `curaduria` | 243 |
| `duat-geodia` | 24 |
| `privado-bloqueado` | 74 |
| `psi-observacionismo` | 437 |
| `publicacion` | 52 |

## Decisiones

| decision | archivos |
|---|---:|
| `ABSORB_AS_RESEARCH_BOUNDARY` | 4 |
| `ABSORB_TO_ATLAS` | 1507 |
| `BLOCK_KEEP_PRIVATE` | 74 |
| `DELETE_REGENERABLE_AFTER_LOG` | 1 |
| `KEEP_CANONICAL` | 72 |
| `REVIEW_DUPLICATE` | 95 |

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
