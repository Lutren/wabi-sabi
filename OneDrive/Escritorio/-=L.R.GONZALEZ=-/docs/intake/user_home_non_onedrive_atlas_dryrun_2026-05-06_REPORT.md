# Curador SETO Tree Absorption

Generated UTC: `2026-05-06T06:55:02.445923+00:00`

Estado: `FICHADO / ABSORBIDO_A_ATLAS / LIMPIEZA_SEGURA_PARCIAL`

## Rutas

- `home_non_onedrive`: `C:\Users\L-Tyr`

## Resumen

- Archivos registrados: `1367`
- Duplicados exactos detectados: `247` archivos en grupos duplicados
- Eliminados seguros en este pase: `0`

## Estados

| estado | archivos |
|---|---:|
| `BLOQUEADO` | 52 |
| `CANONICAL_DUPLICATE_KEEP` | 46 |
| `DELETE_CANDIDATE` | 24 |
| `FICHADO` | 1048 |
| `REVIEW` | 197 |

## Carriles

| carril | archivos |
|---|---:|
| `assets` | 116 |
| `claudio-wabisabi` | 330 |
| `cleanup` | 9 |
| `curaduria` | 837 |
| `privado-bloqueado` | 52 |
| `psi-observacionismo` | 21 |
| `publicacion` | 2 |

## Decisiones

| decision | archivos |
|---|---:|
| `ABSORB_TO_ATLAS` | 1048 |
| `BLOCK_KEEP_PRIVATE` | 52 |
| `DELETE_REGENERABLE_AFTER_LOG` | 24 |
| `KEEP_CANONICAL` | 46 |
| `REVIEW_DUPLICATE` | 197 |

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
