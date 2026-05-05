# Global Curador SETO Dry Audit 2026-05-05

Status: `DRY_RUN_NO_DELETE_NO_MOVE`
Scan mode: `incremental`

This report implements a dry Curador pass over the selected roots. It records evidence for later cleanup gates; it does not approve deletion by itself.

## Artifacts

- JSON summary: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-seto-audit-2026-05-05-workspace_lrgonzalez_max500.json`
- CSV file manifest: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-file-manifest-2026-05-05-workspace_lrgonzalez_max500.csv`
- WitnessLog: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\witness_log\curador_seto_witnesslog.jsonl`

## Counts

| metric | value |
|---|---:|
| `files` | 500 |
| `generated_dirs_recorded` | 4 |
| `project_roots_detected` | 0 |
| `errors` | 0 |
| `hashed_files` | 147 |
| `zip_or_archive_files` | 11 |
| `exact_duplicate_groups` | 7 |
| `version_review_groups` | 11 |

## Resume

| field | value |
|---|---|
| `truncated` | `True` |
| `processed_files` | `500` |
| `max_files` | `500` |
| `next_start_after` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\hooks-mastery\.claude\agents\crypto\crypto-market-agent-sonnet.md` |

## Root Stats

| root | exists | files | dirs | MB | hashed | hash_skipped | generated_dirs_skipped |
|---|---:|---:|---:|---:|---:|---:|---:|
| `workspace_lrgonzalez` | True | 500 | 60 | 83.02 | 147 | 11 | 4 |

## Focus Stats

| focus | files | MB | hashed |
|---|---:|---:|---:|
| `psi` | 130 | 6.37 | 130 |
| `downloads` | 0 | 0.00 | 0 |
| `desktop` | 500 | 83.02 | 147 |
| `workspace` | 500 | 83.02 | 147 |
| `e_drive` | 0 | 0.00 | 0 |

## ActionGate Summary

| gate | count |
|---|---:|
| `REVIEW` | 494 |
| `BLOCK` | 6 |

## Decision Summary

| decision | count |
|---|---:|
| `KEEP_OR_REVIEW` | 477 |
| `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | 11 |
| `KEEP_BLOCKED_BOUNDARY` | 6 |
| `CANDIDATE_DELETE_EMPTY_REVIEW` | 4 |
| `CANDIDATE_DELETE_REGENERABLE_REVIEW` | 2 |

## Exact Duplicate Groups

| sha256 | count | duplicate MB if one kept | gate | examples |
|---|---:|---:|---|---|
| `3dd1271b04e21e30...` | 2 | 0.02 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\PROMPT_MAESTRO_HANDOFF_2026-04-25.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\archive\extra_psi_pre_final_v1_1\PROMPT_MAESTRO_HANDOFF_2026-04-25.md` |
| `08a5093e039f0381...` | 2 | 0.02 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\claudio_daemon.db`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio_daemon.db` |
| `7f18344ab924a5be...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\archive\raiz_2026-04-26\09_MAGIA_PRACTICA.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\libro\09_MAGIA_PRACTICA.md` |
| `6d452217e61a4175...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\04_BRAIN_OS.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\archive\raiz_2026-04-26\04_BRAIN_OS.md` |
| `bf84c85c11a680a7...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\02_SEGUNDA_PERDIDA.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\archive\raiz_2026-04-26\02_SEGUNDA_PERDIDA.md` |
| `5a30c1fa3152eb2d...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\08_POSICIONAMIENTO_EL_OBSERVADOR.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\archive\raiz_2026-04-26\08_POSICIONAMIENTO_EL_OBSERVADOR.md` |
| `17a337c761955d2e...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\archive\raiz_2026-04-26\07_PROMPT_MAESTRO_HANDOFF.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\libro\07_PROMPT_MAESTRO_HANDOFF.md` |

## Large Files

| size MB | gate | decision | path |
|---:|---|---|---|
| 15.11 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.chroma_db\chroma.sqlite3` |
| 10.54 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\grok-video-4d563a03-3e1b-40ec-bd3c-a80214c7ee0b.MP4` |
| 8.90 | `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\packages\OBSERVACIONISMO_ARTEFACT_RUN_v0_2.zip` |
| 7.08 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\assets\piri\piri_reis_world_map_01.jpg` |
| 5.36 | `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\packages\VOYNICH_MUSIC_MICRORUN_v0_8b.zip` |
| 3.73 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.chroma_db\2143d7eb-4303-47af-9cdf-d02277ab8564\data_level0.bin` |
| 3.58 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\face_landmarker.task` |
| 2.81 | `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\packages\VOYNICH_PIRI_REAL_RUN_v0_3.zip` |
| 2.75 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Claudiocobain.png` |
| 2.37 | `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\website_deploy.zip` |
| 2.29 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=Artistas=-\Raul Herrera\Raul HM.pdf` |
| 1.33 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\10e44f41-1247-4e17-9b19-d122cb12a72c-video.MP4` |
| 1.25 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=Artistas=-\Luis Rene Tren Tyr\CV LUIS RENÉ GONZÁLEZ LÓPEZ.pdf` |
| 0.93 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\Logo.png` |
| 0.80 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\OSIT — Teoría Completa de Información con Estado y Tesis del Agente Local sin LLM.pdf` |
| 0.68 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista de Modelos de IA y Matemáticas Unificadas TUIP-Σ OSIT.pdf` |
| 0.67 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=Artistas=-\Evelyn Estrada\IMG_8436.jpeg` |
| 0.57 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista de la Inteligencia — TUIP-Σ OSIT.pdf` |
| 0.50 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\Deconstrucción Observacionista de la Física — TUIP-Σ OSIT.pdf` |
| 0.45 | `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\OBSERVACIONISMO_TUI_R3_PACK (1).zip` |
| 0.43 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=Artistas=-\Evelyn Estrada\IMG_8433.jpeg` |
| 0.40 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\MEdioevosagalore\MUNDO_MEDIOEVO_v27.md` |
| 0.38 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=Artistas=-\S Aeme\b8d8a3eb-deb4-4a4f-8e35-49ee2575e339.jpg` |
| 0.33 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\archive\extra_psi_pre_final_v1_1\PSI Paper v2 - Observer-State-Dependent Measurement Quality.pdf` |
| 0.31 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\investigacion\voynich_piri\assets\piri\piri_rhumb_lines_annotated_small.jpg` |

## Delete Candidate Sample

| gate | decision | path |
|---|---|---|
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\.pytest_cache` |
| `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\releases` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.git` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\hooks-mastery\.git` |
| `REVIEW` | `CANDIDATE_DELETE_EMPTY_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.claudio_consciousness.json` |
| `REVIEW` | `CANDIDATE_DELETE_EMPTY_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.image_download_log.json` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\discord_bot.log` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\download_monitor.log` |
| `REVIEW` | `CANDIDATE_DELETE_EMPTY_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\RC_03_TEMPORADA_9` |
| `REVIEW` | `CANDIDATE_DELETE_EMPTY_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\hooks-mastery\CLAUDE.md` |

## Boundaries

- No deletion, movement, extraction or publication was executed.
- `BLOCK` rows require private/secret/claim review and cannot be cleanup targets.
- `REVIEW` rows require ficha, canonical copy or regenerability proof before a later cleanup pass.
- The CSV manifest is the evidence base for follow-up exact-duplicate and generated-residue gates.
