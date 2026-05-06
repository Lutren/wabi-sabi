# LICENSES

Este workspace no tiene una licencia unica. La raiz sigue marcada como
`LEGAL_REVIEW_REQUIRED` porque mezcla tooling, apps comerciales, libros,
canon, assets editoriales, videojuego privado, vendors y estado local.

## Decisiones por capa

| capa | licencia operativa | alcance |
|---|---|---|
| `packages/open-dev/*` | MIT | tooling developer public-safe, sin secretos, sin runtime privado, sin libros completos |
| `apps/commercial/*` | Propietaria comercial | apps vendibles o internas: Argus, Asistente Negocio, FlujoCRM y Mini Office si se vende |
| `books/editorial/*` | All rights reserved | libros completos, canon, lore, assets editoriales y muestras no aprobadas |
| `game-private/*` | Propietaria privada | frontera/documentacion del videojuego; no contiene fuente activa por defecto |
| vendors/terceros | licencia upstream | no relicenciar como MEDIOEVO |

## Reglas

- Cada paquete publicable debe tener su propio `LICENSE`.
- Cada app comercial debe tener EULA o `COMMERCIAL_LICENSE.md`.
- Cada paquete con dependencias debe tener `THIRD_PARTY_NOTICES.md`.
- Ninguna licencia de esta carpeta autoriza publicar el workspace completo.
- Si hay duda, mantener `LEGAL_REVIEW_REQUIRED` y bloquear release.
