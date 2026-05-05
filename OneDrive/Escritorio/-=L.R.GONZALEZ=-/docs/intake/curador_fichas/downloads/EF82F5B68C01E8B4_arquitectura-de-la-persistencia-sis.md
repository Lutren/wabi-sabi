# Ficha Curador SETO - Arquitectura de la Persistencia Sis.txt

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\New folder\Arquitectura de la Persistencia Sis.txt` |
| SHA256 | `EF82F5B68C01E8B4F444BF1DAD13CD16C89A65B082CF6BA5E02E8DF47241943D` |
| Bytes | `90429` |
| Tipo | `file` |
| Estado PSI | `CERTEZA` |
| Status | `ARCHIVO_FRIO` |
| Clasificacion | `TEXT_SOURCE_REVIEW` |
| Lane | `cleanup` |
| Decision | `ABSORBIDO_CANONIZADO_ARCHIVO_FRIO` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\runtime\curador_seto\source_archive\downloads\2026-05-05\New folder\EF82F5B68C01E8B4_arquitectura-de-la-persistencia-sis.txt` |
| Atlas | `Curaduria SETO` |

## Resumen

Text source; register before deciding canon, archive or deletion.

## Sinapsis

- Destino: `Curador review queue`.
- Evidencia: SHA256 `EF82F5B68C01E8B4F444BF1DAD13CD16C89A65B082CF6BA5E02E8DF47241943D`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
