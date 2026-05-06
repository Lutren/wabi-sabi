# Global Atlas Absorption Scope

Generated UTC: `2026-05-06T06:56:00Z`

Estado: `GLOBAL_DRYRUN_COMPLETO_POR_BLOQUES`

## Veredicto

El alcance correcto es global, no solo `PSI` ni `CLAUDIO - researchs`.

La estructura queda dividida en entradas operativas:

1. `Downloads`: zona de amenaza. Primero riesgo, despues ficha, despues absorcion.
2. `Lobby de Alejandria`: zona documental. Entran prompts/documentos para ser absorbidos y retirados diariamente.
3. `Desktop`: superficie humana de trabajo. Se ficha y se separa de `-=L.R.GONZALEZ=-`.
4. `-=L.R.GONZALEZ=-`: raiz de control, productos, docs, paquetes y runtime de curaduria.
5. `-=MEDIOEVO=-`: universo principal; canon, Claudio, libros, research, privado y productos.
6. `C:\Users\L-Tyr` sin OneDrive/Downloads: perfil local restante; herramientas, docs, codigo, runtime y residuos.

No se aplico borrado global en estos dry-runs. La unica limpieza fisica previa del dia fue la retirada reversible de 13 duplicados exactos en `PSI + CLAUDIO - researchs` y el rename explicito de `promts` a `Lobby de Alejandria`.

## Resultados por bloque

| bloque | manifest | archivos | retiro aplicado | lectura |
|---|---|---:|---:|---|
| Inbox actual `Downloads + Lobby` | `docs/intake/inbox_downloads_lobby_alejandria_current_2026-05-06_MANIFEST.json` | 16 | 0 | `Downloads` esta vacio; el Lobby tiene 16 archivos fichados/estado |
| Desktop sin `-=L.R.GONZALEZ=-` | `docs/intake/desktop_lobby_atlas_dryrun_2026-05-06_MANIFEST.json` | 1,753 | 0 | superficie con documentos, accesos, prompts y material pendiente |
| `-=L.R.GONZALEZ=-` sin `-=MEDIOEVO=-` | `docs/intake/lrgonzalez_root_atlas_dryrun_2026-05-06_MANIFEST.json` | 6,472 | 0 | raiz de control con duplicados/review y archivo de Downloads ya aislado |
| `-=MEDIOEVO=-` | `docs/intake/medioevo_atlas_dryrun_2026-05-06_MANIFEST.json` | 14,806 | 0 | universo grande con 42 candidatos de delete, 1,559 review y 1,486 bloqueados |
| `C:\Users\L-Tyr` sin OneDrive/Downloads | `docs/intake/user_home_non_onedrive_atlas_dryrun_2026-05-06_MANIFEST.json` | 1,367 | 0 | perfil local restante; 24 candidatos regenerables, 197 review, 52 bloqueados |

## Estados agregados

| bloque | fichado | review | bloqueado | bloqueado publicacion | delete candidate | canonical keep |
|---|---:|---:|---:|---:|---:|---:|
| Inbox actual | 14 | 0 | 1 | 1 | 0 | 0 |
| Desktop | 1,507 | 95 | 74 | 4 | 1 | 72 |
| `-=L.R.GONZALEZ=-` | 3,942 | 1,336 | 70 | 2 | 2 | 1,099 |
| `-=MEDIOEVO=-` | 10,952 | 1,559 | 1,486 | 18 | 42 | 749 |
| Home sin OneDrive/Downloads | 1,048 | 197 | 52 | 0 | 24 | 46 |

## Downloads

Estado actual verificado: `0` archivos directos en `C:\Users\L-Tyr\Downloads`.

Fuente descargada ya archivada/fichada:

- `OSIT-QG Modulos Extendidos - Optimizacion y Nuevas Aplicaciones.pdf`
- Ficha: `docs/intake/curador_fichas/downloads/5253B5F5371FB818_osit-qg-modulos-extendidos---optimizacion-y-nuevas-aplicaciones.md`
- Archivo frio: `runtime/curador_seto/source_archive/downloads/2026-05-06/5253B5F5371FB818_osit-qg-modulos-extendidos---optimizacion-y-nuevas-aplic.pdf`
- SHA256: `5253B5F5371FB8185AF5FBEB11B5D4E30B2D7380583D211AC08D617BE2436A80`
- Estado: `ARCHIVO_FRIO / INFERENCIA / REVIEW`

Politica activa:

- `.exe`, `.msi`, `.bat`, `.cmd`, `.ps1`, `.vbs`, `.jar`, `.apk`, `.dll`, `.lnk` -> `BLOQUEADO_AMENAZA_DOWNLOAD`.
- `.zip`, `.rar`, `.7z`, `.iso`, `.img`, `.dmg`, macros Office -> `REVIEW_AMENAZA_DOWNLOAD`.
- PDF/DOCX/TXT/MD -> ficha y revision documental; no ejecucion ni publicacion.

## Lobby de Alejandria

Movimiento ejecutado:

- Antes: `C:\Users\L-Tyr\OneDrive\Escritorio\promts`
- Ahora: `C:\Users\L-Tyr\OneDrive\Escritorio\Lobby de Alejandria`
- Archivo de reglas creado: `README_LOBBY_DE_ALEJANDRIA.md`
- Conteo actual en el run de inbox: `16` archivos.

El Lobby se limpia solo cuando las fuentes ya tienen ficha, sinapsis y destino. Una fuente unica se mueve a archivo frio; un duplicado exacto seguro puede retirarse; una fuente incierta queda en `REVIEW`.

## Exclusiones conscientes

El pase `home` excluyo zonas que no deben convertirse en canon documental:

- OneDrive y Downloads, porque se procesan por bloques separados.
- AppData, caches, node_modules, .git, entornos, credenciales, perfiles de navegador y dotfolders sensibles.

Esto no significa que no existan; significa que no se leen como documentos del cerebro. Se deben tratar como infraestructura, secretos o residuos tecnicos bajo un pase diferente.

## Siguiente ejecucion segura

1. Revisar `DELETE_CANDIDATE` por bloque y aplicar solo los que sean duplicado exacto o basura regenerable con hash.
2. Crear archivo frio para fuentes unicas ya absorbidas del Lobby.
3. Expandir fichas de los `REVIEW` por prioridad: privados, publicaciones, GEODIA/DUAT, builds, vendors.
4. Conectar este resumen con `ATLAS_MAIN.md` y `CURADOR_MASTER_INDEX.md` cuando no haya conflicto con cambios de otros agentes.
