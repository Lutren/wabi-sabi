# Global Curador SETO Dry Audit 2026-05-05

Status: `DRY_RUN_NO_DELETE_NO_MOVE`

This report implements the first global dry pass for PSI, Downloads, Desktop, the L.R.GONZALEZ workspace and E:. It records evidence for later cleanup gates; it does not approve deletion by itself.

## Artifacts

- JSON summary: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-seto-audit-2026-05-05.json`
- CSV file manifest: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-file-manifest-2026-05-05.csv`
- WitnessLog: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\witness_log\curador_seto_witnesslog.jsonl`

## Counts

| metric | value |
|---|---:|
| `files` | 81107 |
| `generated_dirs_recorded` | 465 |
| `project_roots_detected` | 266 |
| `errors` | 2 |
| `hashed_files` | 56360 |
| `zip_or_archive_files` | 194 |
| `exact_duplicate_groups` | 12071 |
| `version_review_groups` | 5418 |

## Root Stats

| root | exists | files | dirs | MB | hashed | hash_skipped | generated_dirs_skipped |
|---|---:|---:|---:|---:|---:|---:|---:|
| `workspace_lrgonzalez` | True | 45097 | 7532 | 4782.32 | 37313 | 1641 | 449 |
| `downloads` | True | 175 | 2 | 77.13 | 175 | 0 | 0 |
| `desktop_other` | True | 1741 | 306 | 1594.61 | 1629 | 14 | 5 |
| `e_drive` | True | 34094 | 3305 | 89005.07 | 17243 | 8720 | 11 |

## Focus Stats

| focus | files | MB | hashed |
|---|---:|---:|---:|
| `psi` | 136 | 6.38 | 136 |
| `downloads` | 175 | 77.13 | 175 |
| `desktop` | 46838 | 6376.94 | 38942 |
| `workspace` | 45097 | 4782.32 | 37313 |
| `e_drive` | 34094 | 89005.07 | 17243 |

## ActionGate Summary

| gate | count |
|---|---:|
| `REVIEW` | 70865 |
| `BLOCK` | 10242 |

## Decision Summary

| decision | count |
|---|---:|
| `KEEP_OR_REVIEW` | 68919 |
| `KEEP_BLOCKED_BOUNDARY` | 10242 |
| `CANDIDATE_DELETE_EMPTY_REVIEW` | 1412 |
| `CANDIDATE_DELETE_REGENERABLE_REVIEW` | 353 |
| `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | 181 |

## Exact Duplicate Groups

| sha256 | count | duplicate MB if one kept | gate | examples |
|---|---:|---:|---|---|
| `171efa004f3ef7f0...` | 8 | 99.53 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\products\asistente_negocio\preview\ABRE_AQUI_PREVIEW_MEDIOEVO.html`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\commercial\asistente-negocio\preview\ABRE_AQUI_PREVIEW_MEDIOEVO.html`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\commercial\asistente-negocio\qa_artifacts\asistente_negocio_final_package_2026-05-02\Asistente_Negocio_MEDIOEVO_v1.0.0\ABRE_AQUI_DEMO_MEDIOEVO.html` |
| `bb9f8df61474d25e...` | 11 | 40.00 | `REVIEW` | `E:\MEDIOEVO\sesiones\.medioevo_bmac_session\BrowserMetrics-spare.pma`<br>`E:\MEDIOEVO\sesiones\.medioevo_d2d_session\BrowserMetrics-spare.pma`<br>`E:\MEDIOEVO\sesiones\.medioevo_elevenlabs_session\BrowserMetrics-spare.pma` |
| `797b0454974de578...` | 2 | 24.58 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\agentes\_archivo_escritorio_2026-04-28\_ESCRITORIO_ORDEN_2026-04-28\archivado_visible\carpetas\MEDIOEVO_10_LIBROS_EDICION_ILUSTRADA_2026-04-23\_paquetes_gumroad\04 - Calibración - EDICION ILUSTRADA.zip`<br>`E:\MEDIOEVO_OFFLOAD\2026-05-01-host-gate\-=MEDIOEVO=-\-=LIBROS\claudio\products\gumroad_live\canon10_illustrated_2026-04-23\packages\04 - Calibración - EDICION ILUSTRADA.zip` |
| `b33fbbb7674082ee...` | 2 | 23.87 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\tools\pentest_repos\shannon-noapi\assets\shannon-action.gif`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\tools\pentest_repos\ShannonAI\shannon-core\assets\shannon-action.gif` |
| `adac69e04a459e18...` | 2 | 23.75 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\agentes\_archivo_escritorio_2026-04-28\_ESCRITORIO_ORDEN_2026-04-28\archivado_visible\carpetas\MEDIOEVO_10_LIBROS_EDICION_ILUSTRADA_2026-04-23\_paquetes_gumroad\06 - Umbral - EDICION ILUSTRADA.zip`<br>`E:\MEDIOEVO_OFFLOAD\2026-05-01-host-gate\-=MEDIOEVO=-\-=LIBROS\claudio\products\gumroad_live\canon10_illustrated_2026-04-23\packages\06 - Umbral - EDICION ILUSTRADA.zip` |
| `1fb87a85a82043bf...` | 8 | 23.39 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\website\img\surfaces\plano_astral_map_v3.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\maps\plano_astral_map_v3.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\sources\plano_astral_map_textpass_v3.png` |
| `fa838bd919a739dc...` | 2 | 21.41 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\agentes\_archivo_escritorio_2026-04-28\_ESCRITORIO_ORDEN_2026-04-28\archivado_visible\carpetas\MEDIOEVO_10_LIBROS_EDICION_ILUSTRADA_2026-04-23\_paquetes_gumroad\10 - Historias Ocultas - EDICION ILUSTRADA.zip`<br>`E:\MEDIOEVO_OFFLOAD\2026-05-01-host-gate\-=MEDIOEVO=-\-=LIBROS\claudio\products\gumroad_live\canon10_illustrated_2026-04-23\packages\10 - Historias Ocultas - EDICION ILUSTRADA.zip` |
| `16b6c029251f115a...` | 2 | 20.29 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\agentes\_archivo_escritorio_2026-04-28\_ESCRITORIO_ORDEN_2026-04-28\archivado_visible\carpetas\MEDIOEVO_10_LIBROS_EDICION_ILUSTRADA_2026-04-23\_paquetes_gumroad\03 - Fragmentos - EDICION ILUSTRADA.zip`<br>`E:\MEDIOEVO_OFFLOAD\2026-05-01-host-gate\-=MEDIOEVO=-\-=LIBROS\claudio\products\gumroad_live\canon10_illustrated_2026-04-23\packages\03 - Fragmentos - EDICION ILUSTRADA.zip` |
| `ea280d8f9eabc3a7...` | 8 | 19.60 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\products\asistente_negocio\app\assets\geodia_hub_scenario_v2.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\website\img\surfaces\geodia_hub_scenario_v2.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\scenarios\geodia_hub_scenario_v2.png` |
| `6caafd5a0011982c...` | 2 | 18.11 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\agentes\_archivo_escritorio_2026-04-28\_ESCRITORIO_ORDEN_2026-04-28\archivado_visible\carpetas\MEDIOEVO_10_LIBROS_EDICION_ILUSTRADA_2026-04-23\_paquetes_gumroad\02 - Deriva - EDICION ILUSTRADA.zip`<br>`E:\MEDIOEVO_OFFLOAD\2026-05-01-host-gate\-=MEDIOEVO=-\-=LIBROS\claudio\products\gumroad_live\canon10_illustrated_2026-04-23\packages\02 - Deriva - EDICION ILUSTRADA.zip` |
| `60b23c5bf02783df...` | 6 | 16.25 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\website\img\surfaces\ciudad_control_city_map_v3.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\maps\ciudad_control_city_map_v3.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\sources\ciudad_control_city_map_textpass_v3.png` |
| `aa07fd4c7ee7aaac...` | 6 | 16.22 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\website\img\surfaces\republica_dragones_lobos_map_v3.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\maps\republica_dragones_lobos_map_v3.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\sources\republica_dragones_lobos_map_textpass_v3.png` |
| `f32b3c71e088e5a8...` | 6 | 15.99 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\website\img\surfaces\plano_medio_map_v3.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\maps\plano_medio_map_v3.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\sources\plano_medio_map_textpass_v3.png` |
| `655d3bc14995be00...` | 6 | 15.67 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\website\img\surfaces\plano_base_map_v3.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\maps\plano_base_map_v3.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\sources\plano_base_map_textpass_v3.png` |
| `4f119bbad919e43c...` | 2 | 15.66 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\agentes\_archivo_escritorio_2026-04-28\_ESCRITORIO_ORDEN_2026-04-28\archivado_visible\carpetas\MEDIOEVO_10_LIBROS_EDICION_ILUSTRADA_2026-04-23\_paquetes_gumroad\05 - Transición - EDICION ILUSTRADA.zip`<br>`E:\MEDIOEVO_OFFLOAD\2026-05-01-host-gate\-=MEDIOEVO=-\-=LIBROS\claudio\products\gumroad_live\canon10_illustrated_2026-04-23\packages\05 - Transición - EDICION ILUSTRADA.zip` |
| `424e8d1d180fa8e7...` | 3 | 15.32 | `REVIEW` | `E:\-=Medioevo=-\-=Libros\-=RADIOCINEMA=-\-=MUSICA_MEDIOEVO=-\Background_Noise\Ashes of the Hallelujah.mp3`<br>`E:\-=Medioevo=-\-=Libros\03_FRAGMENTOS\soundtrack\19.- Dispersion 432.mp3`<br>`E:\Suno Downloads\Ashes of the Hallelujah\Ashes of the Hallelujah.mp3` |
| `0adb5bfead9d5472...` | 5 | 15.20 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\runtime_mirror\maps\ciudad_control_city_map_v2.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\world_atlas_v2\maps\ciudad_control_city_map_v2.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\world_atlas_v2\sources\ciudad_control_city_map_render_v2.png` |
| `719cb7226e70297c...` | 6 | 14.67 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\website\img\surfaces\nexus_cafe_scenario_v2.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\scenarios\nexus_cafe_scenario_v2.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\sources\nexus_cafe_scenario_render_v2.png` |
| `4e4c0b9038804ed1...` | 2 | 14.22 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\agentes\_archivo_escritorio_2026-04-28\_ESCRITORIO_ORDEN_2026-04-28\archivado_visible\carpetas\BETA_TESTERS_MEDIOEVO\Asistente_Negocio_MEDIOEVO_v0.1.3\ABRE_AQUI_PREVIEW_MEDIOEVO.html`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\agentes\_archivo_escritorio_2026-04-28\_ESCRITORIO_ORDEN_2026-04-28\archivado_visible\carpetas\BETA_TESTERS_MEDIOEVO\Asistente_Negocio_MEDIOEVO_v0.1.3\Preview_HTML_multiplataforma\app\index.html` |
| `eff32e0b062703dd...` | 6 | 14.12 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\website\img\surfaces\radiocinema_studio_facade_v2.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\runtime_mirror\buildings\radiocinema_studio_facade_v2.png`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Assets\MEDIOEVO_batch06\world_atlas_v2\buildings\radiocinema_studio_facade_v2.png` |

## Large Files

| size MB | gate | decision | path |
|---:|---|---|---|
| 9163.23 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\ollama\models\blobs\sha256-4c27e0f5b5adf02ac956c7322bd2ee7636fe3f45a8512c9aba5385242cb6e09a` |
| 9016.00 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\-=Medioevo=-\c_drive_relief_2026-04-30\appdata_roaming\Claude\vm_bundles\claudevm.bundle\rootfs.vhdx` |
| 6651.00 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\wsl\Ubuntu\ext4.vhdx` |
| 2884.00 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\-=Medioevo=-\c_drive_relief_2026-04-30\appdata_roaming\Claude\vm_bundles\claudevm.bundle\sessiondata.failed_move_copy_2026-04-30.vhdx` |
| 2884.00 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\-=Medioevo=-\c_drive_relief_2026-04-30\appdata_roaming\Claude\vm_bundles\claudevm.bundle\sessiondata.vhdx` |
| 2447.00 | `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `E:\MEDIOEVO_OFFLOAD\2026-05-01-host-gate\-=MEDIOEVO=-\-=LIBROS\claudio\products\MEDIOEVO_ULTIMATE_ARCHIVE.zip` |
| 2233.93 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\-=Medioevo=-\c_drive_relief_2026-04-30\appdata_roaming\Claude\vm_bundles\claudevm.bundle\rootfs.vhdx.zst` |
| 1840.50 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\ollama-models\models\blobs\sha256-4a188102020e9c9530b687fd6400f775c45e90a0d7baafe65bd0a36963fbb7ba` |
| 1840.50 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\ollama\models\blobs\sha256-4a188102020e9c9530b687fd6400f775c45e90a0d7baafe65bd0a36963fbb7ba` |
| 1757.42 | `BLOCK` | `KEEP_BLOCKED_BOUNDARY` | `E:\Medioevo_RPG\builds\MEDIOEVO_RPG.exe` |
| 1701.55 | `BLOCK` | `KEEP_BLOCKED_BOUNDARY` | `E:\Medioevo_RPG\builds\MEDIOEVO_RPG_current_20260424_171157.exe` |
| 1699.94 | `BLOCK` | `KEEP_BLOCKED_BOUNDARY` | `E:\Medioevo_RPG\builds\MEDIOEVO_RPG_export_fixed_20260424.exe` |
| 1697.48 | `BLOCK` | `KEEP_BLOCKED_BOUNDARY` | `E:\Medioevo_RPG\builds\MEDIOEVO_RPG_validated_20260424.exe` |
| 1697.48 | `BLOCK` | `KEEP_BLOCKED_BOUNDARY` | `E:\Medioevo_RPG\builds\MEDIOEVO_RPG_pre_bomfix_20260424_153000.exe` |
| 1023.51 | `BLOCK` | `KEEP_BLOCKED_BOUNDARY` | `E:\Medioevo_RPG\tools\godot\Godot_v4.3-stable_export_templates.tpz` |
| 843.62 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\-=Medioevo=-\-=Libros\-=RADIOCINEMA=-\MEDIOEVO_03_FRAGMENTOS_AUDIOBOOK_POSTPROD_ES.mp3` |
| 840.89 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\-=Medioevo=-\-=Libros\-=RADIOCINEMA=-\MEDIOEVO_17_JUEGO_DE_ROL_AUDIOBOOK_POSTPROD_ES.mp3` |
| 739.51 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\-=Medioevo=-\-=Libros\-=RADIOCINEMA=-\MEDIOEVO_06_UMBRAL_AUDIOBOOK_REMASTER_ES.mp3` |
| 721.04 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\-=Medioevo=-\-=Libros\-=RADIOCINEMA=-\MEDIOEVO_09_NOSOTROS_USTEDES_LOS_OTROS_AUDIOBOOK_REMASTER_ES.mp3` |
| 704.83 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\-=Medioevo=-\-=Libros\-=RADIOCINEMA=-\MEDIOEVO_18_VOYNICH_AUDIOBOOK_REMASTER_ES.mp3` |
| 700.61 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\-=Medioevo=-\-=Libros\-=RADIOCINEMA=-\MEDIOEVO_05_TRANSICIÓN_AUDIOBOOK_REMASTER_ES.mp3` |
| 661.61 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\-=Medioevo=-\-=Libros\-=RADIOCINEMA=-\MEDIOEVO_07_BABEL_AUDIOBOOK_REMASTER_ES.mp3` |
| 660.62 | `BLOCK` | `KEEP_BLOCKED_BOUNDARY` | `E:\Medioevo_RPG\builds\MEDIOEVO_RPG_prevalidated_20260424_072218.exe` |
| 653.02 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\-=Medioevo=-\-=Libros\-=RADIOCINEMA=-\MEDIOEVO_01_DESPERTAR_AUDIOBOOK_REMASTER_ES.mp3` |
| 602.69 | `REVIEW` | `KEEP_OR_REVIEW` | `E:\-=Medioevo=-\-=Libros\-=RADIOCINEMA=-\MEDIOEVO_11_FRONTERA_AUDIOBOOK_REMASTER_ES.mp3` |

## Delete Candidate Sample

| gate | decision | path |
|---|---|---|
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.pytest_cache` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\build` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\annotated_doc\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\annotated_types\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\anyio\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\anyio\abc\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\anyio\streams\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\anyio\_backends\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\anyio\_core\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\attr\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\attrs\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\bcrypt\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\blinker\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\certifi\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\charset_normalizer\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\charset_normalizer\cli\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\api\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\api\models\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\auth\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\auth\basic_authn\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\auth\simple_rbac_authz\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\auth\token_authn\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\auth\utils\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\cli\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\db\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\db\impl\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\db\impl\grpc\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\db\mixins\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\execution\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\execution\executor\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\execution\expression\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\ingest\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\ingest\impl\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\logservice\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\migrations\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\proto\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\quota\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\quota\simple_quota_enforcer\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\rate_limit\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\rate_limit\simple_rate_limit\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\segment\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\segment\distributed\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\segment\impl\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\segment\impl\distributed\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\segment\impl\manager\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\segment\impl\manager\cache\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.venv_api\Lib\site-packages\chromadb\segment\impl\metadata\__pycache__` |

## Boundaries

- No deletion, movement, extraction or publication was executed.
- `BLOCK` rows require private/secret/claim review and cannot be cleanup targets.
- `REVIEW` rows require ficha, canonical copy or regenerability proof before a later cleanup pass.
- The CSV manifest is the evidence base for follow-up exact-duplicate and generated-residue gates.
