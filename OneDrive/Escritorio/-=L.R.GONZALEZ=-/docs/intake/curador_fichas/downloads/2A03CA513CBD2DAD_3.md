# Ficha Curador SETO - 3.txt

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\3.txt` |
| SHA256 | `2A03CA513CBD2DADAA9C9E04176EF5F685C5A99B7A5135F04F0EAAD06F07B8A3` |
| Bytes | `31514` |
| Tipo | `file` |
| Estado PSI | `CERTEZA` |
| Status | `REGISTRADO` |
| Clasificacion | `TEXT_SOURCE_REVIEW` |
| Lane | `cleanup` |
| Decision | `HOLD_WITH_TECHNICAL_CARD_BEFORE_USE` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\Downloads\3.txt` |

## Resumen

Text source; register before deciding canon, archive or deletion.

## Sinapsis

- Destino: `Curador review queue`.
- Evidencia: SHA256 `2A03CA513CBD2DADAA9C9E04176EF5F685C5A99B7A5135F04F0EAAD06F07B8A3`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
