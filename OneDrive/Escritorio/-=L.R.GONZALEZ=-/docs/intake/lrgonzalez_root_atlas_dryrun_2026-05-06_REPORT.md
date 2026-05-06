# Curador SETO Tree Absorption

Generated UTC: `2026-05-06T06:53:54.947286+00:00`

Estado: `FICHADO / ABSORBIDO_A_ATLAS / LIMPIEZA_SEGURA_PARCIAL`

## Rutas

- `lrgonzalez`: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`

## Resumen

- Archivos registrados: `6472`
- Duplicados exactos detectados: `2459` archivos en grupos duplicados
- Eliminados seguros en este pase: `0`

## Estados

| estado | archivos |
|---|---:|
| `BLOQUEADO` | 70 |
| `BLOQUEADO_PUBLICACION` | 2 |
| `CANONICAL_DUPLICATE_KEEP` | 1099 |
| `DELETE_CANDIDATE` | 2 |
| `FICHADO` | 3942 |
| `REVIEW` | 1336 |
| `REVIEW_AMENAZA_DOWNLOAD` | 21 |

## Carriles

| carril | archivos |
|---|---:|
| `assets` | 110 |
| `claudio-wabisabi` | 282 |
| `cleanup` | 1 |
| `curaduria` | 5373 |
| `duat-geodia` | 105 |
| `privado-bloqueado` | 70 |
| `psi-observacionismo` | 349 |
| `publicacion` | 182 |

## Decisiones

| decision | archivos |
|---|---:|
| `ABSORB_AS_RESEARCH_BOUNDARY` | 2 |
| `ABSORB_TO_ATLAS` | 3942 |
| `BLOCK_KEEP_PRIVATE` | 70 |
| `DELETE_EXACT_DUPLICATE_AFTER_HASH` | 1 |
| `DELETE_REGENERABLE_AFTER_LOG` | 1 |
| `KEEP_CANONICAL` | 1099 |
| `REVIEW_DOWNLOAD_BEFORE_EXTRACT_OR_EXECUTE` | 21 |
| `REVIEW_DUPLICATE` | 1336 |

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
