# Ficha Curador SETO - 02_SEGUNDA_PERDIDA.md

| campo | valor |
|---|---|
| Ruta original | `C:\Users\L-Tyr\Downloads\New folder\02_SEGUNDA_PERDIDA.md` |
| SHA256 | `BF84C85C11A680A7EB7F06FBA2EEF548D7030F07E76FF45F162DB40DD23ED68C` |
| Bytes | `7151` |
| Tipo | `file` |
| Estado PSI | `CERTEZA` |
| Status | `REGISTRADO` |
| Clasificacion | `TEXT_SOURCE_REVIEW` |
| Lane | `cleanup` |
| Decision | `HOLD_WITH_TECHNICAL_CARD_BEFORE_USE` |
| ActionGate | `REVIEW` |
| Canonico | `C:\Users\L-Tyr\Downloads\New folder\02_SEGUNDA_PERDIDA.md` |

## Resumen

Text source; register before deciding canon, archive or deletion.

## Sinapsis

- Destino: `Curador review queue`.
- Evidencia: SHA256 `BF84C85C11A680A7EB7F06FBA2EEF548D7030F07E76FF45F162DB40DD23ED68C`.
- Uso permitido: local, curado, sin publicacion externa directa.

## Falsadores

- secret/private marker, hash mismatch, unique content loss, strong claim without validation.
- Si aparece secreto, ruta privada o claim fuerte no validado, el estado cambia a `BLOQUEADO`.
