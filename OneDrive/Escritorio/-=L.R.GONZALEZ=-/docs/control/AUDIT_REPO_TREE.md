# AUDIT_REPO_TREE

Fecha de auditoria: 2026-04-29

Raiz auditada: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`

Alcance: inventario Fase 0. No se movieron, borraron ni modificaron archivos de codigo.

## Resumen ejecutivo

La raiz no es un repo unico. Es un workspace de producto con varios repos y arboles anidados:

## Actualizacion Fase 5

Los scripts de auditoria ya existen en `tools/release/` y el recorrido activo
excluye `_archive`, `_ARCHIVAR`, vendors, caches, builds y rutas privadas
denegadas por defecto. Ultima verificacion activa:

- `python tools\release\audit_repo.py`: 9056 archivos, 1317 directorios.
- `-=MEDIOEVO=-`: 8555 archivos activos, 7294.57 MB.
- `PRODUCTOS_MEDIOEVO`: 159 archivos activos, 13.66 MB.
- `tools`: 237 archivos activos, 8.72 MB.
- Repos Git activos detectados: `-=LIBROS`, `claudio`, `mini_office`,
  `llm-wiki`, `metaevo-tcg`, staging GEODIA y `tools/claw-code`.

Para inventario completo incluyendo `_archive`, caches y builds:

```powershell
python tools\release\audit_repo.py --include-denied
```

| ruta | tipo observado | estado inicial |
|---|---|---|
| `-=MEDIOEVO=-\-=LIBROS` | repo Git padre / canon / productos / website / Claudio / juego | muy sucio, muchos no trackeados |
| `-=MEDIOEVO=-\-=LIBROS\claudio` | repo Git principal de runtime/producto | rama `fix/claudio-cli-latency`, ahead 10, sucio |
| `-=MEDIOEVO=-\-=LIBROS\metaevo-tcg` | repo Git de juego/TCG | sucio, tratar como PRIVATE |
| `-=MEDIOEVO=-\-=LIBROS\claudio\website` | website dentro de Claudio, no repo propio aqui | 571 archivos, 231.46 MB |
| `-=MEDIOEVO=-\-=LIBROS\website` | website padre minimo | 1 archivo |
| `PRODUCTOS_MEDIOEVO` | staging/catalogo de productos | estructura ya segmentada por capa |
| `tools\claw-code` | repo Git de herramienta dev | sucio por `rust/.claw/plugins/` |

## Tamano por carpeta raiz

| carpeta | dirs | archivos | MB aprox | lectura |
|---|---:|---:|---:|---|
| `-=MEDIOEVO=-` | 8024 | 76560 | 16640.37 | nucleo del workspace, incluye libros, Claudio, website, juego, vendors y archivos grandes |
| `.claw` | 10 | 12 | 0.00 | sesiones/configuracion local |
| `PRODUCTOS_MEDIOEVO` | 100 | 188 | 13.86 | catalogo/staging de productos |
| `tools` | 419 | 3408 | 2041.44 | toolchain externo, Rust target pesado |

## Repos Git detectados

Repos principales:

- `-=MEDIOEVO=-\-=LIBROS`
- `-=MEDIOEVO=-\-=LIBROS\claudio`
- `-=MEDIOEVO=-\-=LIBROS\metaevo-tcg`
- `tools\claw-code`

Repos o subrepos anidados de baja confianza para publicacion directa:

- `.skills\*`
- `claudio\.skills\*`
- `claudio\core\sadtalker`
- `claudio\core\wav2lip`
- `claudio\github-modules\open-higgsfield-ai`
- `claudio\tools\pentest_repos\*`
- `claudio\tools\vendor\*`
- `CLAUDIO - researchs\GEODIA\_github_staging\*`

## Estado Git observado

`-=MEDIOEVO=-\-=LIBROS`:

- Rama: `imagenes`
- Cambios modificados visibles: `claudio/CLAUDE.md`, `claudio/NEXT_SESSION_BRIEF.md`, `claudio/PENDIENTES_MASTER.md`, `claudio/claudio_api_server.py`, `claudio/core/*`, `claudio/website/*`.
- Muchos archivos no trackeados en la raiz: `-=Artistas=-`, `-=CEREBRO=-`, `-=NEGOCIOS=-`, `.claude`, `.skills`, `.wrangler`, docs y scripts sueltos.

`-=MEDIOEVO=-\-=LIBROS\claudio`:

- Rama: `fix/claudio-cli-latency...origin/fix/claudio-cli-latency [ahead 10]`
- Modificados visibles: `NEXT_SESSION_BRIEF.md`, `PENDIENTES_MASTER.md`, `claudio_tui.py`.
- Muchos no trackeados: `.env.example`, `.env.mova.example`, `.gitignore`, `CLAUDE.md`, launchers, docs, scripts y assets.

`-=MEDIOEVO=-\-=LIBROS\metaevo-tcg`:

- Rama: `main...origin/main`
- Muchos archivos modificados en app, assets, datos, Android/iOS/Electron.
- Clasificacion inicial: PRIVATE / NO PUBLICAR.

`tools\claw-code`:

- Rama: `main...origin/main`
- No trackeado: `rust/.claw/plugins/`.

## Arbol funcional actual

```txt
C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
  -=MEDIOEVO=-
    -=LIBROS
      -=CEREBRO=-
      -=NEGOCIOS=-
      _ARCHIVAR
      _SNAPSHOTS
      _trash_revisar
      assets
      claudio
      llm-wiki
      MEDIOEVO_BESTSELLER_OUTPUT
      metaevo-tcg
      products
      radiocinema
      runtime
      vault_medioevo
      website
    CLAUDIO - researchs
  PRODUCTOS_MEDIOEVO
    01_LIBROS_Y_BUNDLES
    02_SOFTWARE_LOCAL
    03_OPEN_SOURCE_GITHUB
    04_AUDIOVISUAL_Y_TCG
    05_BETAS_Y_PROXIMAMENTE
    claudio_os_blueprint
    content_forge
  tools
    claw-code
```

## Claudio: subarbol observado

`claudio` contiene muchas capas mezcladas:

- Runtime/API: `api`, `core`, `runtime`, `brain_os`, `claudio_os`, `sdk`, `tests`, `tools`.
- Apps: `apps`, `argus`, `mini_office`, `products/asistente_negocio`, `products/crm`, `website`.
- Editorial/canon: `editorial`, `observacionismo`, `-=PSI=-`, `docs`, `teatro`, `radiocinema`.
- Comercial: `commercial`, `products`, `marketing`, `gumroad_*`, `stripe_*`, `shopify`.
- Riesgo/privado/revision: `tcg`, `runtime/game_bridge`, `tools/pentest_repos`, `github-modules`, `tools/vendor`.
- Residuos ya reconocidos: `_ARCHIVAR`, `_legacy`, `_archivo_sesiones`, `archive`, `logs`, `__pycache__`, `.pytest_cache`.

## Archivos grandes relevantes

| archivo | MB aprox | lectura |
|---|---:|---|
| `-=MEDIOEVO=-\-=LIBROS\claudio\products\MEDIOEVO_ULTIMATE_ARCHIVE.zip` | 2447.00 | producto/archivo enorme; no debe entrar a repo publico |
| `-=MEDIOEVO=-\-=LIBROS\claudio\products\MEDIOEVO_STARTER_PACK.zip` | 541.80 | producto comercial o bundle; revisar licencia/contenido |
| `-=MEDIOEVO=-\-=LIBROS\claudio\products\MEDIOEVO_SOUNDTRACK_CURATED.zip` | 168.13 | asset comercial/audiovisual; revisar derechos |
| `-=MEDIOEVO=-\-=LIBROS\claudio\products\MEDIOEVO_TCG_PRINTABLE_DECK.zip` | 139.21 | TCG/juego; tratar como privado/revision |
| `-=MEDIOEVO=-\-=LIBROS\claudio\products\asistente_negocio\release\*.zip` | 133.62 | build comercial ya generado |
| `-=MEDIOEVO=-\-=LIBROS\claudio\products\asistente_negocio\release\*.exe` | 98.71 | build comercial ya generado |
| `tools\claw-code\rust\target\debug\*.pdb` | 135.52 c/u | build local, no publicable |
| `-=MEDIOEVO=-\-=LIBROS\claudio\Termux.apk` | 97.03 | binario externo/local, revisar origen |

Tambien hay objetos Git enormes en `-=LIBROS\.git\objects`, incluyendo un objeto de 2447.20 MB. Esto sugiere que archivos pesados pudieron haber entrado al historial Git.

## Tipos de archivo principales

| extension | cantidad |
|---|---:|
| sin extension | 37597 |
| `.json` | 9495 |
| `.md` | 7417 |
| `.py` | 7050 |
| `.ts` | 4277 |
| `.js` | 2438 |
| `.pyc` | 1578 |
| `.o` | 1469 |
| `.png` | 1170 |
| `.zip` | 78 |
| `.exe` | 91 |
| `.log` | 87 |

## Build/test signals

Senales positivas:

- `claudio\pytest.ini` existe y excluye `.venv`, `.skills`, `_ARCHIVAR`, `release`, `dist`, `build`, `node_modules`, `tools/vendor`, `core/sadtalker`.
- `claudio\apps\argus_desktop` tiene scripts `dev`, `build`, `typecheck`, `electron:build:win`.
- `metaevo-tcg` tiene scripts `dev`, `build`, `lint`, `preview`, empaquetado desktop/mobile. Tratar como PRIVATE.
- `claudio\products\asistente_negocio` tiene `check`, `package:final`, `build:win`, `build:mac`.
- `claudio\sdk` declara `observacionismo-gate` con licencia MIT por archivo `LICENSE`.

Senales negativas:

- Al inicio no habia `AGENTS.md`, `README.md`, `LICENSE`, `CHANGELOG.md`, `ROADMAP.md` ni `RELEASE_CHECKLIST.md` en la raiz auditada; ahora existen como documentos de gobierno/release.
- La raiz ya contiene documentos de control, skeleton de capas y scripts de release. Siguen siendo borradores hasta aprobacion humana.
- Hay multiples sitios y productos duplicados o semi-duplicados entre `-=LIBROS`, `claudio`, `PRODUCTOS_MEDIOEVO` y `CLAUDIO - researchs`.
- Hay builds, caches, vendors y zip/exe mezclados con fuente.

## Conclusion Fase 0

No declarar nada listo para publicar aun. La estructura puede ordenarse, pero antes se necesita:

1. Aprobar `VISIBILITY_MATRIX.md` y `PRIVATE_GAME_BOUNDARY.md`.
2. Completar migracion por repo/subrepo solo desde `MIGRATION_MAP.md`.
3. Resolver hallazgos de `SECRET_SCAN_REPORT.md`.
4. Separar builds y bundles de fuente usando allowlists por producto.
5. Definir si la raiz publica sera `-=LIBROS`, `claudio`, `PRODUCTOS_MEDIOEVO`, o un repo nuevo derivado.
