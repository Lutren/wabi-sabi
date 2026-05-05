# Ficha Curador SETO - Untitled.txt

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\Untitled.txt` |
| SHA256 | `76C6B475C95CF2988010FE12B2B3CCD7DA0F959932EAB6A1FEB22135AA2FF676` |
| Bytes | `127410` |
| Tipo | `file` |
| Estado PSI | `CERTEZA` |
| Status | `REGISTRADO` |
| Clasificacion | `TEXT_SOURCE_REVIEW` |
| Lane | `cleanup` |
| Decision | `HOLD_WITH_TECHNICAL_CARD_BEFORE_USE` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\Downloads\Untitled.txt` |

## Resumen

Text source; register before deciding canon, archive or deletion.

## Sinapsis

- Destino: `Curador review queue`.
- Evidencia: SHA256 `76C6B475C95CF2988010FE12B2B3CCD7DA0F959932EAB6A1FEB22135AA2FF676`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
