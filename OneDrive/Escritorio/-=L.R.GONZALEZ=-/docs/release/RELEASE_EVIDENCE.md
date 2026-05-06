# RELEASE_EVIDENCE

Fecha: 2026-04-29

## Licencias y fronteras

- Raiz: workspace multi-licencia, no publicable completo.
- MIT: `packages/open-dev/obsai-core`, `packages/open-dev/residueos`, `packages/open-dev/observacionismo-gate`, `packages/open-dev/claudio-os-blueprint`, `packages/open-dev/gemma-observacionismo-cleanup`.
- Propietario comercial: `apps/commercial/argus-desktop`, `apps/commercial/asistente-negocio`, `apps/commercial/flujocrm`, `apps/commercial/mini-office`.
- All rights reserved: `books/editorial`, canon, libros completos, assets editoriales y frontera del juego.

## Separacion fisica verificada

- `packages/open-dev/` contiene paquetes dev allowlist.
- `apps/commercial/` contiene apps vendibles/internal.
- `books/editorial/` contiene borradores y muestras editorial-safe.
- `game-private/` existe solo como frontera/documentacion; no se movio MetaEvo/TCG.
- `releases/free-dev`, `releases/paid-apps`, `releases/editorial` quedan reservados para paquetes generados.

## Hormiguero Ciudad Viva

Implementado en:

`-=MEDIOEVO=-\-=LIBROS\claudio\apps\hormiguero_mission_control\index.html`

Evidencia:

- primera pantalla con `live-city-shell`;
- capas: superficie, subsuelo, torres, rutas, eventos;
- edificios desde runtime/city registry;
- agentes visibles y rutas;
- fallback offline sin metricas inventadas;
- smoke Flask 200 JSON en endpoints publicos.
- QA visual Playwright: desktop y mobile con 9 edificios, 6 agentes, estado `online`, fallback offline oculto y sin solape entre mapa y panel de detalle.

Documento canonico:

`docs/canon/hormiguero-ciudad-viva.md`

Capturas:

- `qa_artifacts\2026-04-29-hormiguero-city\desktop.png`
- `qa_artifacts\2026-04-29-hormiguero-city\mobile.png`

Servidor local activo para revision: `http://127.0.0.1:5050/`.

## Gemma + Observacionismo

Implementado en:

`packages/open-dev/gemma-observacionismo-cleanup`

Evidencia:

- CLI: `gemma-observe`, `gemma-noise-report`, `gemma-fingerprint`;
- tests sinteticos: `3 passed`;
- sin pesos, prompts privados, secretos, logs sensibles ni runtime Claudio;
- licencia MIT y notices presentes.

Documento editorial:

`books/editorial/observacionismo-gemma-method.md`

## Free-dev release artifacts

Fecha: 2026-05-01

Estado: `LOCAL_ARTIFACTS_READY_FOR_HUMAN_PUBLICATION_REVIEW`.

Artefactos generados:

| producto | ZIP | SHA256 |
|---|---|---|
| `residueos` | `releases\free-dev\residueos.zip` | `F8727267B65E650C71723B7085520D10FDF538D3B3EA78912F2AE3A4966393FC` |
| `obsai-core` | `releases\free-dev\obsai-core.zip` | `37604CB0F106E626C5357F5A152111A01806A502D14F8AD1F0EDB3C48248E46E` |
| `observacionismo-gate` | `releases\free-dev\observacionismo-gate.zip` | `0004AAC74730CFDEF1208B9A6B6BA0F1BA68908B01089855081E32098C47013C` |
| `claudio-os-blueprint` | `releases\free-dev\claudio-os-blueprint.zip` | `C73E6CBD340F1084063317AC99813A58BF7E42DCDCC9BD7F3BBBB1D30CE2C570` |
| `gemma-observacionismo-cleanup` | `releases\free-dev\gemma-observacionismo-cleanup.zip` | `43FEEC450095EA8F7A335FF3D2C87AE907EE7CC0135231C5731810B126AAA93F` |

Verificacion:

- `python tools\release\scan_secrets.py --product obsai-core --product residueos --product observacionismo-gate --product claudio-os-blueprint --product gemma-observacionismo-cleanup --json --fail-on-findings`: `count_reported=0`.
- `python tools\release\package_free_dev.py --execute`: escribio los cinco ZIPs bajo `releases\free-dev`.
- `python tools\release\scan_secrets.py --artifact ... --json --fail-on-findings`: `count_reported=0`; este modo inspecciona miembros internos del ZIP.
- `python tools\release\verify_free_dev_release.py --write --json`: `ok=true`; evidencia persistida en `qa_artifacts\release_validation\free-dev-smoke.json`.
- Smoke de instalacion desde extraccion temporal: `residueos`, `obsai-core`, `observacionismo-gate` y `gemma-observacionismo-cleanup` construyeron wheel, instalaron y pasaron import; `claudio-os-blueprint` paso verificacion de documentos requeridos.

Correcciones aplicadas durante el gate:

- Se agrego `--artifact` a `tools\release\scan_secrets.py` para escanear contenido de ZIPs, no solo nombres de archivo.
- Se agrego `tools\release\verify_free_dev_release.py` para comparar miembros contra allowlist e instalar desde extraccion temporal.
- Se declaro `build-system` con `setuptools`/`wheel` en los paquetes Python open-dev.
- Se limito discovery de `gemma-observacionismo-cleanup` a `gemma_observacionismo_cleanup*` para evitar incluir `fixtures` como paquete Python.

Limite:

- No se publico nada a GitHub, Gumroad, website ni redes. La publicacion externa requiere ActionGate humano y revision final de destino.
- El workspace raiz completo sigue bloqueado para publicacion amplia por hallazgos legacy del secret scan.

### Primer staging GitHub local

Productos:

| producto | staging repo | commit local |
|---|---|---|
| `residueos` | `publish_staging\open-dev\residueos` | `359dbb7 Initial public release staging` |
| `obsai-core` | `publish_staging\open-dev\obsai-core` | `d17d334 Initial public release staging` |
| `observacionismo-gate` | `publish_staging\open-dev\observacionismo-gate` | `ccea7d2 Initial public release staging` |
| `claudio-os-blueprint` | `publish_staging\open-dev\claudio-os-blueprint` | `98e55f2 Initial public release staging` |
| `gemma-observacionismo-cleanup` | `publish_staging\open-dev\gemma-observacionismo-cleanup` | `8f8e080 Initial public release staging` |

Destino preparado: `publish_staging\open-dev`.

Verificacion:

- Host gate refrescado: `gate=REVIEW`, razon `disco_precaucion`.
- Host gate actual del publicador seco: `gate=REVIEW`, razones `memoria_alta`, `disco_precaucion`.
- Host gate directo posterior: `gate=REVIEW`, `disk_pct=87.6`, `disk_free_mb=27842.45`, razon `disco_precaucion`.
- Offload host gate: selected large/generated artifacts moved to `E:\MEDIOEVO_OFFLOAD\2026-05-01-host-gate`; evidence in `qa_artifacts\release_validation\host-gate-offload-2026-05-01.json`.
- Host gate after offload: `gate=REVIEW`, `disk_pct=84.9`, `disk_free_mb=34031.32`, `lambda_sat=0.849`.
- ActionGate real: `public_publish` hacia `github:Lutren/observacionismo-gate` con autorizacion del usuario devolvio `allowed=false`, `status=needs_review`, razon `accion externa requiere host APPROVE, estado actual REVIEW`.
- ActionGate real retry via `python tools\release\publish_free_dev_github.py --product observacionismo-gate --execute --write --json`: blocked before external action with `allowed=false`, `external_actions_performed=false`; evidence in `qa_artifacts\release_validation\free-dev-github-publish.json`.
- ActionGate dry-run: `allowed=true`, `status=pass`, modo `staging_only`.
- `python tools\release\stage_free_dev_repos.py --skip-existing --write --json`: `ok=true`; evidencia en `qa_artifacts\release_validation\free-dev-staging.json`.
- `python tools\release\verify_free_dev_staging.py --write --json`: `ok=true`; evidencia en `qa_artifacts\release_validation\free-dev-staging-smoke.json`.
- `python tools\release\publish_free_dev_github.py --write --json`: `ok=true`, `external_actions_performed=false`; evidencia en `qa_artifacts\release_validation\free-dev-github-dry-run.json`.
- `python tools\release\scan_secrets.py --path publish_staging\open-dev --json --fail-on-findings`: `count_reported=0`.
- Smokes desde copias temporales de staging:
  - `residueos`: install/import + `6 passed`;
  - `obsai-core`: install/import + `9 passed`;
  - `observacionismo-gate`: install/import;
  - `gemma-observacionismo-cleanup`: install/import + `3 passed`;
  - `claudio-os-blueprint`: 35 archivos y documentos requeridos presentes.
- Remotos: ninguno configurado en los cinco repos; no hubo `gh repo create`, `git push`, upload ni publicacion externa.

Herramientas agregadas:

- `tools\release\stage_free_dev_repos.py`: crea repos Git locales desde allowlists sin remoto.
- `tools\release\verify_free_dev_staging.py`: verifica repos staging limpios, sin remoto y con smoke desde copia temporal.
- `tools\release\publish_free_dev_github.py`: publicador GitHub gated; en modo default solo dry-run, registra ActionGate y no hace `gh`, remoto ni `git push`.

## GEODIA Social Observatory

Implementado en:

`research\geodia-social-observatory`

Estado:

- `INTERNAL_RESEARCH / LOCAL_PRIVATE_MVP`;
- contratos `claudio.social_source_snapshot.v1`, `claudio.social_epoch_model.v1`, `claudio.social_scenario_report.v1`;
- contratos locales `motor.local_source_intake.v1`, `motor.observation_event.v1`, `motor.artifact_record.v1`, `motor.route_decision.v1`, `motor.behavior_signature.v1`, `motor.duat_health_window.v1`, `motor.duat_conway_simulation.v1`;
- fixture sintetico offline con hashes estables;
- intake local de 10 archivos de `Downloads` sin copiar contenido bruto;
- event store JSONL, artifact graph, firma conductual, router, salud DUAT y simulacion seeded;
- fuente allowlist con World Bank, IMF, OECD, Eurostat, FRED, OWID y GDELT;
- GDELT limitado a senal mediatico-narrativa;
- publication gate fijo en `BLOCK`.

Verificacion:

- `python -m pytest tests -q`: `14 passed`;
- `python -m geodia_social_observatory.cli run --offline --fixture fixtures\social_epoch_fixture.json --pretty`: reporte generado con `publication_gate.status=BLOCK`;
- `python -m geodia_social_observatory.cli intake --pretty`: registro generado con `source_count=10`;
- `python -m geodia_social_observatory.cli simulate-duat --seed 7 --size 12 --steps 5 --pretty`: simulacion deterministica con `motor.duat_conway_simulation.v1`;
- `python tools\release\product_manifest.py --product geodia-social-observatory --hash --write`: `file_count=19`, `blocked_count=0`;
- `python tools\release\scan_secrets.py --product geodia-social-observatory --json --fail-on-findings`: `count_reported=0`;
- `python tools\release\scan_secrets.py --path release_manifests\geodia-social-observatory.json --json --fail-on-findings`: `count_reported=0`.

## Argus

Estado:

- `node_modules` y `dist` no quedan activos en legacy ni en `apps/commercial/argus-desktop`;
- artifacts archivados bajo `_archive/legacy/2026-04-29/argus_generated_artifacts_second_pass`;
- `.gitignore` mantiene `node_modules/`, `dist/`, `release/`, `.vite/`;
- `tools/release/clean_generated_artifacts.py` requiere `--execute` para mover artifacts.

Verificacion:

- `npm ci` con cache temporal paso;
- `npm rebuild` paso;
- `npm run typecheck` paso;
- `npm run build` paso;
- `npm audit --omit=dev --audit-level=high` paso con `found 0 vulnerabilities`.

## Release blockers

- No publicar workspace raiz completo: `scan_secrets.py` detecta marcadores de secretos en legacy.
- No publicar MetaEvo/TCG desde esta linea de trabajo.
- No declarar ClaudioOS como ISO terminado; el paquete actual es blueprint/handoff.
