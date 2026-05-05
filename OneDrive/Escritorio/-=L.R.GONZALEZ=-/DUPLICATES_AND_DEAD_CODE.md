# DUPLICATES_AND_DEAD_CODE

Fecha: 2026-04-29

Metodo: inventario no destructivo por nombres duplicados, rutas repetidas, tamano, caches, builds, archivos legacy y marcadores de residuo. No se borraron archivos.

## Duplicacion estructural principal

| grupo | evidencia | lectura | accion recomendada |
|---|---|---|---|
| Blueprint ClaudioOS | `PRODUCTOS_MEDIOEVO\claudio_os_blueprint` 33 archivos; `claudio\_workspace\claudio_os_blueprint` 33 archivos; `claudio\runtime\claudio_os_build\staging\claudio_os_blueprint` 35 archivos | hay 3 copias/candidatos | elegir canon y marcar las otras como staging/archive |
| Skills/agentes | `-=LIBROS\.skills` 9148 archivos / 631.70 MB; `claudio\.skills` 10268 archivos / 192.45 MB | vendors duplicados y pesados | excluir de releases; evaluar si una copia debe archivarse |
| Website | `-=LIBROS\website` 1 archivo; `claudio\website` 571 archivos / 231.46 MB | source of truth ambiguo | declarar ruta canonica |
| Product builds | zips y exe en `claudio\products` y `products/asistente_negocio/release` | builds junto a fuente | mover a `releases/` en Fase 2 si se aprueba |
| Archivos de investigacion | `CLAUDIO - researchs`, `_ARCHIVAR`, `archive`, `_legacy` | historico mezclado con producto activo | crear indices y mantener fuera de releases |
| Pentest repos | varios repos bajo `claudio\tools\pentest_repos` | terceros/riesgo seguridad | aislar y no publicar |

## Duplicados por nombre de archivo

Estos conteos no significan que todos sean duplicados invalidos; indican ruido de repo y vendors.

| filename | count | lectura |
|---|---:|---|
| `SKILL.md` | 615 | skills/vendores/anidados |
| `README.md` | 554 | normal en monorepo, pero excesivo por vendors |
| `index.ts` | 393 | normal en TS, pero se mezcla con vendors |
| `__init__.py` | 232 | normal en Python, incluye archives |
| `package.json` | 165 | muchos proyectos/vendores |
| `types.ts` | 116 | TS vendors |
| `xss_analysis_deliverable.md` | 103 | pentest benchmark output repetido |
| `ssrf_exploitation_queue.json` | 103 | pentest benchmark output repetido |
| `auth_analysis_deliverable.md` | 103 | pentest benchmark output repetido |
| `injection_analysis_deliverable.md` | 102 | pentest benchmark output repetido |
| `tsconfig.json` | 98 | varios packages |
| `.gitignore` | 89 | muchos subrepos |
| `tmp.json` | 66 | temporales |
| `package-lock.json` | 58 | vendors/subprojects |
| `CLAUDE.md` | 33 | continuidad dispersa |
| `requirements.txt` | 32 | varios Python projects |
| `LICENSE` | 32 | licencias de terceros |
| `AGENTS.md` | 18 | no existe en raiz, solo en subarboles/vendor/codex |

## Residuos por tipo

| tipo | count | ejemplos |
|---|---:|---|
| `__pycache__` dirs | 262 | caches Python |
| `.git` dirs | 33 | repos anidados/subrepos/vendors |
| `node_modules` dirs | 12 | dependencias JS |
| `build` dirs | 11 | builds |
| `dist` dirs | 8 | builds |
| `releases` dirs | 5 | releases de vendors/productos |
| `_ARCHIVAR` dirs | 3 | archivo reconocido |
| `archive` dirs | 3 | archivo reconocido |
| `.pyc` files | 1578 | cache Python |
| `.o` files | 1469 | build Rust/C |
| `.log` files | 87 | logs |
| `.zip` files | 78 | paquetes o backups |
| `.exe` files | 91 | binarios |

## Candidatos de dead code / legacy

No borrar aun. Mover solo con mapa y verificacion.

| ruta/patron | razon |
|---|---|
| `claudio\backup.py` | nombre backup |
| `claudio\claudio_tui_legacy.py` | legacy explicito |
| `claudio\CLAUDE.md.backup` | backup explicito |
| `claudio\_temp_oppo_persistent_setup.sh` | temporal |
| `claudio\C...tempsensor_server.py` | nombre corrupto/escape raro |
| `BORRAR_ARCHIVOS_AUDIOBOOK.txt` | lista de borrado pendiente, requiere revision |
| `RC_03_TEMPORADA_9` | archivo sin extension de tamano 0 |
| `.skills\ruflo\v3\**\tmp.json` | temporales repetidos |
| `claudio\tools\pentest_repos\ShannonAI\shannon-core\xben-benchmark-results\**` | salidas benchmark repetitivas |
| `tools\claw-code\rust\target\**` | build local regenerable |

## No archivar automaticamente

- `metaevo-tcg`: privado, pero activo. No mover sin instruccion explicita.
- `claudio\tests`: hay `pytest.ini`; no tocar sin test baseline.
- `claudio\core`: esta modificado en el repo padre; no tocar en Fase 0.
- `PENDIENTES_MASTER.md`, `NEXT_SESSION_BRIEF.md`, `CLAUDE.md`: otra sesion puede estar operando ahi.
- `PRODUCTOS_MEDIOEVO`: ya tiene estructura de producto; no reordenar antes de definir fuente de verdad.

## Conclusion

El residuo principal no es un archivo aislado; es mezcla de capas. La limpieza segura debe empezar con allowlists por producto, no con borrado. El primer movimiento real deberia ser crear `MIGRATION_MAP.md` y un script dry-run de empaquetado/exclusion.

## Actualizacion Fase 5

Se crearon scripts dry-run para residuos:

```powershell
python tools\release\find_large_files.py --limit 15 --min-mb 50
python tools\release\find_duplicates.py --limit 15
```

Hallazgos activos principales:

- Archivos grandes activos: `MEDIOEVO_ULTIMATE_ARCHIVE.zip` 2447 MB,
  `MEDIOEVO_STARTER_PACK.zip` 541.8 MB,
  `MEDIOEVO_SOUNDTRACK_CURATED.zip` 168.13 MB,
  `MEDIOEVO_TCG_PRINTABLE_DECK.zip` 139.21 MB,
  `Termux.apk` 97.03 MB.
- Duplicados por nombre activos: `__init__.py` 138, `README.md` 103,
  `index.html` 28, `SKILL.md` 27, `.gitignore` 20.
- `_archive` y `_ARCHIVAR` se excluyen por defecto del recorrido activo.
- Los artifacts generados de Argus tienen copia archivada en
  `_archive\legacy\2026-04-29\argus_generated_artifacts\`; tambien siguen
  presentes copias activas ignoradas en `argus_desktop/node_modules` y
  `argus_desktop/dist`, por lo que quedan como candidatos de limpieza.

## Actualizacion 2026-05-03 - Pase corto por duplicados

Comandos ejecutados:

```powershell
python tools\release\find_duplicates.py --mode name --limit 30 --json
python tools\release\find_large_files.py --limit 40 --min-mb 10 --include-denied --json
```

Lectura:

- El modo `name` encontro ruido esperado de monorepo, no basura directa:
  `__init__.py` 158, `README.md` 151, `SKILL.md` 44, `.gitignore` 37,
  `index.html` 36, `LICENSE` 35, `pyproject.toml` 27.
- El modo `hash` global se fue a timeout antes de optimizar el script; se
  actualizo `tools\release\find_duplicates.py` para agrupar primero por tamano
  y hashear solo candidatos. Despues de eso, `--mode hash --limit 30 --json`
  completo en ~71 s.
- `:8789` fue reparado como hallazgo de seguridad asociado a residuo runtime:
  el servidor `python -m http.server 8789` ahora escucha en `127.0.0.1`,
  no en `::`.

Duplicados exactos verificados por hash:

| grupo | copia A | copia B | sha256 | lectura |
|---|---|---|---|---|
| Asistente ZIP final | `apps\commercial\asistente-negocio\qa_artifacts\asistente_negocio_final_package_2026-05-02\Asistente_Negocio_MEDIOEVO_v1.0.0\Windows\Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.zip` | `apps\commercial\asistente-negocio\release\Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.zip` | `8E5B04DFFCF4DF97402DA0542D8BCF2B207CF23816ED9D50A2139755F4C3BF48` | copia exacta; elegir canon antes de borrar |
| Asistente EXE final | `apps\commercial\asistente-negocio\qa_artifacts\asistente_negocio_final_package_2026-05-02\Asistente_Negocio_MEDIOEVO_v1.0.0\Windows\Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.exe` | `apps\commercial\asistente-negocio\release\Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.exe` | `5B01373668EA2990F976963CB245A4C4F98B4420995A65CA1E438409F085654D` | copia exacta; elegir canon antes de borrar |
| Ruflo model ONNX | `-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\models\phi-4-mini\cpu_and_mobile\cpu-int4-rtn-block-32-acc-level-4\model.onnx` | `-=MEDIOEVO=-\-=LIBROS\claudio\.skills\ruflo\v2\models\phi-4-mini\cpu_and_mobile\cpu-int4-rtn-block-32-acc-level-4\model.onnx` | `701AA5D185B6A782BC27104A990DD5B634FA507840B7C42F7EE6F1FB812D0B83` | vendor/cache duplicate; exclude from releases |
| Ruflo model data | `-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\models\phi-4-mini\cpu_and_mobile\cpu-int4-rtn-block-32-acc-level-4\model.onnx.data` | `-=MEDIOEVO=-\-=LIBROS\claudio\.skills\ruflo\v2\models\phi-4-mini\cpu_and_mobile\cpu-int4-rtn-block-32-acc-level-4\model.onnx.data` | `26AE1BCA5E86F44B07AD31A0051F4EA0847C942D60D8A567B90B095C048E9463` | vendor/cache duplicate; exclude from releases |

Cleanup ejecutado en este pase:

- Eliminados solo los dos duplicados exactos bajo
  `apps\commercial\asistente-negocio\release\`, despues de confirmar
  `git check-ignore` por `apps/commercial/asistente-negocio/.gitignore:4:release/`.
- Copias preservadas:
  `apps\commercial\asistente-negocio\qa_artifacts\asistente_negocio_final_package_2026-05-02\Asistente_Negocio_MEDIOEVO_v1.0.0\Windows\...`.
- Espacio recuperado aproximado: 232.08 MB.

No son duplicados exactos aunque comparten nombre/tamano similar:

- `-=MEDIOEVO=-\-=LIBROS\claudio\products\asistente_negocio\release\Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.zip`
  tiene SHA256 `B6F260C231CD2335ACE9BD3690FB5435BE036E8518295CE13DADB37537ED3427`.
- `-=MEDIOEVO=-\-=LIBROS\claudio\products\asistente_negocio\release\Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.exe`
  tiene SHA256 `7CA1B34BF45E50C48E9553FBC9DEECC97FC52BA559370F13754CA0E62D384F84`.

Accion recomendada:

1. Mantener `apps\commercial\asistente-negocio\qa_artifacts\...` como evidencia
   de paquete final.
2. Mantener `.skills\ruflo` y `claudio\.skills\ruflo` fuera de releases. En este
   pase se eligio como canon el clon raiz `.skills\ruflo` porque conserva `.git`
   y remoto upstream; se borraron solo los dos archivos de modelo duplicados en
   `claudio\.skills\ruflo`.
3. No borrar automaticamente duplicados de assets privados/TCG o espejos
   website/E:; varios hash-groups exactos corresponden a imagenes de TCG,
   covers, surfaces y assets compartidos entre `website` y `E:\MEDIOEVO_ASSETS`.
4. `camera_frames\oppo_frame_*.png` ya fue revisado aparte: eran 218 archivos
   ignorados con el mismo SHA256. Queda ficha en
   `docs\intake\CAMERA_FRAMES_OPPO_RUNTIME_FICHA_2026-05-03.md`; se preservo
   una muestra y se borraron 217 duplicados exactos con ActionGate aprobado.

## Actualizacion 2026-05-03 - camera_frames OPPO runtime

Comandos/evidencia:

```powershell
python tools\release\curador_preflight.py --path '.\-=MEDIOEVO=-\-=LIBROS\claudio\camera_frames'
git -C '.\-=MEDIOEVO=-\-=LIBROS\claudio' check-ignore -v -- "camera_frames\oppo_frame_1.png"
```

Dry-run:

`qa_artifacts\release_validation\camera-frames-cleanup-dry-run-2026-05-03.json`

Resultado:

`qa_artifacts\release_validation\camera-frames-cleanup-result-2026-05-03.json`

Resultado:

- `total_files=218`
- `total_bytes=1,735,498`
- `unique_hashes=1`
- `exact_duplicate_delete_candidates_count=217`
- `deleted_count=217`
- `deleted_bytes=1,727,537`
- `preserved_count=1`
- `git_check_ignore_sample=.gitignore:231:camera_frames/`
- `action_gate_decision_id=1587d99b-449c-4b5e-a7e7-36214498a471`

Decision:

- Borrados 217 duplicados exactos dentro de `camera_frames`.
- Preservada una muestra:
  `oppo_frame_20260418_002952.png`.

## Actualizacion 2026-05-03 - Ruflo model duplicate cleanup

Evidencia:

- `qa_artifacts\release_validation\ruflo-model-duplicate-cleanup-dry-run-2026-05-03.json`
- `qa_artifacts\release_validation\ruflo-model-duplicate-cleanup-result-2026-05-03.json`
- `docs\intake\RUFLO_MODEL_DUPLICATE_CLEANUP_FICHA_2026-05-03.md`

Decision:

- Canon preservado: `-=MEDIOEVO=-\-=LIBROS\.skills\ruflo` porque tiene `.git`
  y remoto upstream `https://github.com/ruvnet/ruflo.git`.
- Duplicado limpiado: `-=MEDIOEVO=-\-=LIBROS\claudio\.skills\ruflo\...\model.onnx*`.
- Borrados: `2` archivos, `96,854,299` bytes.
- ActionGate: `e6623488-ef44-47f1-b7c2-164e7dba9272`.

## Actualizacion 2026-05-03 - triage hash/large-file posterior a Asistente

Comandos ejecutados:

```powershell
python tools\release\find_duplicates.py --mode hash --limit 12 --json
python tools\release\find_large_files.py --limit 30 --min-mb 20 --include-denied --json
```

Estado de gate antes de acciones destructivas:

- `python tools\host_observacionista.py --no-write` desde `-=MEDIOEVO=-\-=LIBROS\claudio`
  devolvio `gate=REVIEW`, razon `residuo_precaucion`.
- No se ejecuto borrado en este subpase.

Lectura del hash scan:

- Los primeros 10 grupos de duplicados exactos son imagenes TCG bajo
  `E:\MEDIOEVO_ASSETS\editorial_web_img\tcg\...`; esto es frontera
  `PRIVATE/TCG`, no basura directa.
- El grupo `LICENSES/MIT.txt` + `packages\open-dev\*\LICENSE` es duplicado
  intencional de licencia; no se debe limpiar por hash.
- El grupo de `__init__.py` vacios en `-=MEDIOEVO=-\CLAUDIO - researchs\futuro\...`
  es estructura Python valida; no aporta ahorro material.

Lectura de archivos grandes:

- El peso dominante esta en objetos Git de `-=LIBROS`, `metaevo-tcg`,
  `claudio`, `.skills\ruflo` y `core\sadtalker`; no se borra con
  `Remove-Item`. Requiere plan de historia/offload por repo si se decide.
- `E:\MEDIOEVO_ASSETS` y `metaevo-tcg` siguen bajo frontera privada.
- `_archive\legacy\2026-04-29\argus_generated_artifacts_second_pass\...`
  contiene binarios Electron grandes; puede ser candidato futuro solo si una
  ficha confirma que el archivo ya no sirve como evidencia de limpieza.
- `claudio\products\asistente_negocio\release\...` y
  `apps\commercial\asistente-negocio\qa_artifacts\...` tienen nombres/tamanos
  similares, pero hashes distintos; no son duplicados exactos.

Decision:

- Cierre de este subpase: documentacion y clasificacion solamente.
- No borrar assets TCG, licencias, `__init__.py`, objetos Git, builds
  comerciales o archivos de evidencia sin ficha canonica y gate `APPROVE`.

### Argus archive generated artifact ficha

Se inspecciono `_archive\legacy\2026-04-29\argus_generated_artifacts_second_pass`
con curador preflight:

- `node_modules_status_cleanup_112717`: 19,643 archivos, 774,765,902 bytes
  (738.87 MB), ya registrado por `DELETE_CANDIDATES.md`.
- `dist_status_cleanup_112717`: 16 archivos, 3,785,323 bytes (3.61 MB),
  no estaba registrado antes de este pase.

Ficha creada:
`docs\intake\ARGUS_ARCHIVE_GENERATED_ARTIFACTS_FICHA_2026-05-03.md`.

Decision final: ambos folders se borraron despues de confirmar fuente Argus
activa con `package.json`, `package-lock.json` y `src`, crear dry-run, refrescar
host `APPROVE` y pasar ActionGate `322b8392-70a1-4f4b-a1f2-cc3b7171563c`.
Resultado: `19,659` archivos generados, `778,551,225` bytes.

## Downloads / PSI Exact-Duplicate Pass 2026-05-05

No files deleted. `SOURCE_INTAKE_REGISTER.md` was refreshed and a focused
inventory was written to
`qa_artifacts\release_validation\portfolio-curador-inventory-2026-05-05.json`.

Summary:

- `Downloads`: 175 files, 77.13 MB, mostly TXT/PNG/MD/ZIP/PY.
- `-=PSI=-`: 120 files, 6.33 MB, mostly MD/TXT/PY plus DOCX/PDF/ZIP.
- Exact duplicate groups across Downloads and PSI found: 49.
- PSI is the proposed canonical location for OSIT/TUIP research outputs and
  copied formal sources.
- Claudio local code/UI prototypes need a Claudio-specific ficha before cleanup.
- Numbered PNG captures in Downloads remain `REVIEW_REQUIRED_DOWNLOAD`.

Primary duplicate classes:

| class | examples | action |
|---|---|---|
| OSIT/TUIP DOCX/PDF outputs | `Deconstrucción Observacionista...`, `OSIT — Teoría Completa...` | keep PSI copy, mark Downloads copy as cleanup candidate |
| Downloads mirror of PSI docs | `Downloads\New folder\01_OBSERVACIONISMO_CORE.md`, `05_PSI_TEORIA_FORMAL_v2.md` | keep PSI/canon copy |
| Claudio local prototypes | `claudio_ui*.html`, `claudio_local_code_agent*.py`, `claudio_nollm_agent_pack*.zip` | create Claudio ficha before selecting one copy |
| DUAT agent ZIP iterations | `duat_observacionismo_unified_v4_code_agent*.zip` | keep one after DUAT technical card |
| PSI archive/vault duplicate files | `archive\vault_redundante_2026-04-26\**` | not source of truth; only remove after full vault uniqueness check |

Canonical ficha:

- `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\00_FICHA_TECNICA_PSI_2026-05-05.md`

## PSI Downloads Canon Contract Pass 2026-05-05

No files deleted. This follow-up separated unique `Downloads` insights from
exact duplicates and formalized only the useful operational patterns.

New evidence:

- `docs\intake\PSI_DOWNLOADS_CANON_CONTRACT_INTAKE_2026-05-05.md`
- `-=PSI=-\canon\extensiones_formales\15_OSIT_TUIP_TUI_CANON_OPERATIVO_2026-05-05.md`
- `-=PSI=-\canon\extensiones_formales\16_PSI_CLAIM_REGISTER_DOWNLOADS_2026-05-05.md`
- `-=PSI=-\canon\extensiones_formales\17_PSI_TO_CLAUDIO_WABI_TECHNICAL_CONTRACT_2026-05-05.md`

Hash comparison result:

- Unique to `Downloads` for now: `TUIP_SIGMA_R2_1_PRAGMATIC_CANON.md`,
  `tuip_sigma_core.py`, `claudio_nollm_final_integrated.zip`,
  `duat_living_matrix_v07.zip`, `observacionismo_v8_1_addons.txt`,
  `sensorium_psi_bridge_pack.zip`, `sensorium_inversion_lab.py`,
  `psi_chi_lab_v2.py`, `psi_chi_lab_v8.py`.
- Exact duplicate across `Downloads` and PSI: `OBSERVACIONISMO_TUI_R3_PACK.zip`
  with SHA256
  `34DC55FAA8686AF0276CBC26EA345327FF5A1F7AA4E4AFEA8D24BDEC5FC379CC`.

Decision:

- Keep unique `Downloads` sources as `RESEARCH_ONLY` or
  `READ_REVIEW_TEST_BEFORE_IMPORT`.
- Keep the duplicate TUI R3 ZIP until package lineage is chosen.
- Do not delete code prototypes, prompt-like sources or ZIPs from `Downloads`
  until a later cleanup pass confirms canonical copy, full hash and ActionGate.

## Global Curador SETO Dry Audit 2026-05-05

No files deleted. A global dry-run manifest was generated with the SETO
contract and WitnessLog:

- Report: `docs\intake\GLOBAL_CURADOR_SETO_AUDIT_2026-05-05.md`
- JSON: `qa_artifacts\release_validation\global-curador-seto-audit-2026-05-05.json`
- CSV: `qa_artifacts\release_validation\global-curador-file-manifest-2026-05-05.csv`
- WitnessLog event: `8189746031215a2705ffda47760c16285f982dc651ce6f89ecb6be54c2ea9388`

Counts:

| metric | value |
|---|---:|
| files inventoried | 81,107 |
| hashed files | 56,360 |
| exact duplicate groups | 12,071 |
| version-review groups | 5,418 |
| ZIP/archive files | 194 |
| project roots | 266 |
| `BLOCK` rows | 10,242 |

Largest cleanup-relevant classes observed:

| class | reading | action |
|---|---|---|
| E-drive VM/model blobs | multi-GB VHDX and Ollama blob files | review host/offload plan; not workspace delete |
| private RPG builds | large `E:\Medioevo_RPG\builds\*.exe` | `BLOCK`; private boundary |
| commercial/editorial audio and book ZIPs | large MP3/ZIP products across E: and offload | rights/source-of-truth review before move/delete |
| website/assets duplicated by hash | repeated surface/map/scenario images | choose asset source of truth; do not delete private/TCG assets |
| `Downloads` PSI/code prototypes | all 175 files hashed | keep under intake until Claudio/PSI ficha closes lineage |
| Python caches and local env caches | many `__pycache__` and cache dirs | first safe cleanup lane after focused gate |

Classifier correction:

- `.git`, Git objects, `release(s)` folders, `env` folders and `bin` folders
  are not direct delete candidates.
- They require `BLOCK` or `REVIEW` because they may contain repo history,
  commercial evidence, secrets, runtimes or tools.

Next exact-duplicate pass:

1. Filter CSV to `action_gate=REVIEW`, `decision=KEEP_OR_REVIEW`, same SHA256,
   no private/secret flags.
2. Choose one canonical path per group.
3. Create ficha and ActionGate metadata.
4. Only then mark a path `DELETE_APPROVED_AFTER_HASH`.

## SETO Regenerable Cache Cleanup 2026-05-05

This pass closed the first safe cleanup lane from the global audit: generated
local cache directories only. It did not touch duplicate content, source
archives, releases, private assets, env folders, Git history or unique
Downloads/PSI research sources.

Evidence:

- Dry-run: `qa_artifacts\release_validation\seto-cache-cleanup-dry-run-2026-05-05.json`
- Result: `qa_artifacts\release_validation\seto-cache-cleanup-result-2026-05-05.json`
- Post-validation residue check:
  `qa_artifacts\release_validation\seto-cache-cleanup-post-validation-result-2026-05-05.json`
- Selector-validation residue cleanup:
  `qa_artifacts\release_validation\seto-cache-cleanup-selector-validation-result-2026-05-05.json`
- Final tools-release cache cleanup:
  `qa_artifacts\release_validation\seto-cache-cleanup-tools-release-final-result-2026-05-05.json`
- Self-cache final cleanup with `PYTHONDONTWRITEBYTECODE=1`:
  `qa_artifacts\release_validation\seto-cache-cleanup-self-cache-final-result-2026-05-05.json`
- Tool: `tools\release\cleanup_regenerable_cache.py`
- WitnessLog event: `01f328781e05ccb667001b6e41f2516bd2b7db250657b60e2a0bceabc110d9eb`

Result:

| class | deleted dirs | deleted files | deleted bytes | status |
|---|---:|---:|---:|---|
| Python/test/lint/typecheck cache dirs | 122 | 879 | 11,194,250 | `EXECUTED` |
| post-validation cache residue | 0 | 0 | 0 | `CLEAN` |
| selector-validation cache residue | 7 | 25 | 279,254 | `EXECUTED` |
| tools-release final cache residue | 2 | 14 | 206,789 | `EXECUTED` |
| self-cache final residue | 6 | 19 | 208,999 | `EXECUTED` |

Allowed names were limited to `__pycache__`, `.pytest_cache`, `.ruff_cache`
and `.mypy_cache`. Every target was resolved under the workspace root before
deletion.

Remaining duplicate/dead-code lanes:

- Exact hash duplicates from
  `qa_artifacts\release_validation\global-curador-file-manifest-2026-05-05.csv`
  remain `REVIEW`.
- Large build outputs require product-specific rebuild evidence before cleanup.
- Empty files/folders require parent-project role review.

## SETO Exact Duplicate Candidate Selector 2026-05-05

No files deleted. The selector reads the global SETO CSV and produces a
smaller review queue for exact duplicate groups that are textual, under the
workspace root, below `1 MB`, and outside blocked boundaries.

Artifacts:

- `tools\release\select_exact_duplicate_candidates.py`
- `docs\intake\SETO_EXACT_DUPLICATE_CANDIDATES_2026-05-05.md`
- `qa_artifacts\release_validation\seto-exact-duplicate-candidates-2026-05-05.json`

Counts:

| metric | value |
|---|---:|
| manifest rows | 81,107 |
| exact duplicate groups | 12,071 |
| eligible low-risk groups | 157 |
| selected groups | 80 |
| blocked or hard-review groups | 11,914 |

Decision:

- `INFERENCIA`: proposed canonical path per group.
- `REVIEW`: all duplicate candidates.
- `BLOQUEADO`/excluded: `E:\`, `Downloads`, Desktop, evidence/staging folders,
  tool/vendor/offensive paths, releases, envs, archives, private markers,
  secret-like names and boilerplate files.
