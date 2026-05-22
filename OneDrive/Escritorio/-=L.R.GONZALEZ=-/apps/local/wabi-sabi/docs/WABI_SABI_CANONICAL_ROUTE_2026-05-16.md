# WABI-SABI CANONICAL ROUTE

Fecha: 2026-05-16

## Decision

La unica ruta de proyecto Wabi-Sabi es:

`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi`

Todo codigo activo, tests, adapters, configuracion no secreta, docs operativos,
fingerprints y handoffs de Wabi-Sabi deben vivir dentro de esa ruta.

## Contrato

| regla | estado |
|---|---|
| Proyecto activo | `apps/local/wabi-sabi` |
| Paquete Python activo | `apps/local/wabi-sabi/wabi_sabi` |
| Tests activos | `apps/local/wabi-sabi/tests` |
| Config no secreta activa | `apps/local/wabi-sabi/config` |
| Adapters/stubs activos | `apps/local/wabi-sabi/adapters` |
| Evidencia local | `apps/local/wabi-sabi/runtime` ignorado por Git |
| Docs canonicos Wabi | `apps/local/wabi-sabi/docs` |
| Hooks externos permitidos | solo wrappers de host, COMMS, staging o fichas con referencia a esta ruta |
| Acciones publicas | `BLOCK/REVIEW`; no push, deploy, publicacion ni Gumroad desde este carril |

## Absorcion ejecutada

- Se absorbieron los adapters/stubs de root `adapters/` hacia
  `apps/local/wabi-sabi/adapters/`.
- Se absorbio el perfil de modelos no secreto de root `config/` hacia
  `apps/local/wabi-sabi/config/`.
- `scripts/select_model.ps1` ahora lee el perfil canonico en
  `apps/local/wabi-sabi/config/models.wabisabi.yaml`.
- `scripts/wabi_sabi_startup.ps1` ahora usa los adapters canonicos y escribe
  logs bajo `apps/local/wabi-sabi/runtime/logs`.
- Root `adapters/` y root `config/` fueron movidos a
  `_archive/legacy/wabi-sabi-external-2026-05-16/` con registro en
  `MIGRATION_LOG.md`.
- `README_WABISABI.md` quedo como redireccion, no como segundo README de
  proyecto.
- Las fuentes dispersas de docs, intake, atlas, COMMS, live tree, staging y
  assets quedaron inventariadas en `WABI_SABI_ABSORPTION_MANIFEST_2026-05-16.md`.

## Lo Que No Se Movio

- No se borraron fuentes originales; las copias legacy alejadas se archivaron
  de forma reversible.
- No se copiaron secretos ni loaders de secretos al proyecto canonico.
- No se tocaron rutas privadas de juego/TCG.
- No se publico, hizo push, deploy ni release externo.
- No se absorbio contenido protegido completo desde `MEDIOEVO_LIVE_TREE` ni
  desde source cards; solo se registro frontera y referencia.

## Rutas Externas Clasificadas

| ruta externa | decision | razon |
|---|---|---|
| `scripts/wabi_sabi_startup.ps1` | HOST_WRAPPER | launcher Windows; llama ruta canonica |
| `scripts/wabi_sabi_startup_hidden.vbs` | HOST_WRAPPER | autostart oculto; mantener como wrapper |
| `scripts/select_model.ps1` | HOST_WRAPPER | selector de sesion; lee config canonica |
| `scripts/load_secrets.ps1` y relacionados | REVIEW_SECRET_HOOK | no copiar a canon; presencia local solamente |
| `_archive/legacy/wabi-sabi-external-2026-05-16/config/models.wabisabi*.yaml` | ARCHIVED_LEGACY | config antigua superada por copia canonica |
| `_archive/legacy/wabi-sabi-external-2026-05-16/adapters/*.py` | ARCHIVED_LEGACY | codigo absorbido en `apps/local/wabi-sabi/adapters` |
| `COMMS/agents_state/wabi-sabi-sentido-comun.json` | BRIDGE_STATE | estado de agente compartido, no proyecto |
| `docs/ops/WABI*` | REFERENCE_ONLY | handoffs historicos, no runtime activo |
| `docs/intake/*WABI*` | SOURCE_CARD_REFERENCE | fichas/intake, no runtime activo |
| `MEDIOEVO_OBSERVACIONISMO_MASTER/10_WABI_SABI_CLAUDIO_AGI.md` | THEORY_REFERENCE | canon conceptual; no codigo activo |
| `MEDIOEVO_LIVE_TREE/*WABISABI*` | GOVERNANCE_REFERENCE | boundary/source cards protegidas |
| `packages/open-dev/duat-genesis/assets/pets/wabi-sabi-k-07` | ASSET_REFERENCE | asset publico separado, no motor Wabi |
| `publish_staging/system_integration_review/integration_specs/wabi_sabi` | STAGING_REFERENCE | staging public-safe, no source activo |

## Evidencia

- `python tools\release\pending_review.py --write --quiet` ->
  `active_dedup=18`, `claudio_open=0`.
- `rg --files ... | rg -i 'wabi|wabisabi|wabi-sabi|wabi_sabi|agora-wabi'`
  encontro 141 archivos dentro de la ruta canonica y, despues del archivo
  legacy, 34 coincidencias externas directas por nombre.
- `Get-ChildItem -Directory -Recurse ...` encontro solo cuatro directorios con
  nombre Wabi-Sabi: la ruta canonica, su paquete interno, un asset pet y un
  staging spec.
- `curador_preflight.py` marco `docs/ops` como registrado y varias fuentes
  externas como `NEEDS_FICHA_BEFORE_USE`, por eso quedaron en referencia o
  REVIEW, no en importacion masiva.
- Verificacion posterior al archivo: root `adapters=False`, root
  `config=False`, archivo legacy y canon `True`.
- Startup reejecutado: proceso `pythonw.exe` activo desde
  `apps/local/wabi-sabi/adapters/stub_nemotron.py`.

## Regla De Continuidad

Cuando aparezca una ruta nueva Wabi-Sabi fuera de `apps/local/wabi-sabi`:

1. No crear otro proyecto.
2. Clasificar con Curador/ActionGate.
3. Si es codigo util y no secreto, mover la implementacion hacia la ruta
   canonica o crear un wrapper que apunte a ella.
4. Si es teoria, ficha, staging o asset externo, registrarlo en el manifiesto.
5. No borrar la fuente original sin migration map y gate explicito.
