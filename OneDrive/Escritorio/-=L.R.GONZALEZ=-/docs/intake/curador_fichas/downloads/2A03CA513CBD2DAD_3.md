# Ficha Curador SETO - 3.txt

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\3.txt` |
| SHA256 | `2A03CA513CBD2DADAA9C9E04176EF5F685C5A99B7A5135F04F0EAAD06F07B8A3` |
| Bytes | `31514` |
| Tipo | `file` |
| Estado PSI | `CERTEZA` |
| Status | `ARCHIVO_FRIO` |
| Clasificacion | `TEXT_SOURCE_REVIEW` |
| Lane | `cleanup` |
| Decision | `ABSORBIDO_CANONIZADO_ARCHIVO_FRIO` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\runtime\curador_seto\source_archive\downloads\2026-05-05\2A03CA513CBD2DAD_3.txt` |
| Atlas | `Curaduria SETO` |

## Resumen

Text source; register before deciding canon, archive or deletion.

## Sinapsis

- Destino: `Curador review queue`.
- Evidencia: SHA256 `2A03CA513CBD2DADAA9C9E04176EF5F685C5A99B7A5135F04F0EAAD06F07B8A3`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
