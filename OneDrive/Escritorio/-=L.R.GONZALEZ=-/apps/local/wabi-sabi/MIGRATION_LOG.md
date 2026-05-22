# MIGRATION_LOG WABI-SABI

## 2026-05-16 - Absorcion de rutas externas

Canon: `apps/local/wabi-sabi`.

Se absorbieron los adapters y perfiles de modelos no secretos desde la raiz del
workspace hacia:

- `apps/local/wabi-sabi/adapters/`
- `apps/local/wabi-sabi/config/`

Despues de validar wrappers y suite, las fuentes antiguas quedaron archivadas
en:

`../../../_archive/legacy/wabi-sabi-external-2026-05-16/`

No se borraron fuentes; el archivo raiz `MIGRATION_LOG.md` conserva el mapa de
migracion completo.
