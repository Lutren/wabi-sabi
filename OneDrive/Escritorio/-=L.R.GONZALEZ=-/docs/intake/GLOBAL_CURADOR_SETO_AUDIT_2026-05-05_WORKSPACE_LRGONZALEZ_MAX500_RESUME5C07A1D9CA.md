# Global Curador SETO Dry Audit 2026-05-05

Status: `DRY_RUN_NO_DELETE_NO_MOVE`
Scan mode: `incremental`

This report implements a dry Curador pass over the selected roots. It records evidence for later cleanup gates; it does not approve deletion by itself.

## Artifacts

- JSON summary: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-seto-audit-2026-05-05-workspace_lrgonzalez_max500_resume5c07a1d9ca.json`
- CSV file manifest: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-file-manifest-2026-05-05-workspace_lrgonzalez_max500_resume5c07a1d9ca.csv`
- WitnessLog: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\witness_log\curador_seto_witnesslog.jsonl`

## Counts

| metric | value |
|---|---:|
| `files` | 500 |
| `generated_dirs_recorded` | 32 |
| `project_roots_detected` | 78 |
| `errors` | 0 |
| `hashed_files` | 60 |
| `zip_or_archive_files` | 0 |
| `exact_duplicate_groups` | 17 |
| `version_review_groups` | 23 |

## Resume

| field | value |
|---|---|
| `truncated` | `True` |
| `processed_files` | `500` |
| `max_files` | `500` |
| `start_after_found` | `True` |
| `next_start_after` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\EJECUTAR_ALCATEL_AUTO.bat` |

## Root Stats

| root | exists | files | dirs | MB | hashed | hash_skipped | generated_dirs_skipped |
|---|---:|---:|---:|---:|---:|---:|---:|
| `workspace_lrgonzalez` | True | 500 | 1110 | 10.66 | 60 | 6 | 32 |

## Focus Stats

| focus | files | MB | hashed |
|---|---:|---:|---:|
| `psi` | 0 | 0.00 | 0 |
| `downloads` | 0 | 0.00 | 0 |
| `desktop` | 500 | 10.66 | 60 |
| `workspace` | 500 | 10.66 | 60 |
| `e_drive` | 0 | 0.00 | 0 |

## ActionGate Summary

| gate | count |
|---|---:|
| `REVIEW` | 494 |
| `BLOCK` | 6 |

## Decision Summary

| decision | count |
|---|---:|
| `KEEP_OR_REVIEW` | 493 |
| `KEEP_BLOCKED_BOUNDARY` | 6 |
| `CANDIDATE_DELETE_REGENERABLE_REVIEW` | 1 |

## Exact Duplicate Groups

| sha256 | count | duplicate MB if one kept | gate | examples |
|---|---:|---:|---|---|
| `9b5089dcde899933...` | 2 | 0.14 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\styles.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\styles.csv` |
| `9043c3f06faa9b43...` | 2 | 0.10 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\design.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\design.csv` |
| `6ea44a7725d708a2...` | 2 | 0.06 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\products.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\products.csv` |
| `41976082ecae1100...` | 2 | 0.05 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\ui-reasoning.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\ui-reasoning.csv` |
| `a393558b7acc7919...` | 2 | 0.05 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\typography.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\typography.csv` |
| `ef67afdbd03f9517...` | 2 | 0.04 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\scripts\design_system.py`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\scripts\design_system.py` |
| `b8d7bc2b2f9865a1...` | 2 | 0.02 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\_sync_all.py`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\_sync_all.py` |
| `ebb565308115f955...` | 2 | 0.02 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\charts.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\charts.csv` |
| `1870ee048f2a2bdd...` | 2 | 0.02 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\ux-guidelines.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\ux-guidelines.csv` |
| `47c0a454cb73bf32...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\react-performance.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\react-performance.csv` |
| `a08ca77fcf6b6d95...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\stacks\react-native.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\stacks\react-native.csv` |
| `ef89f856b7245be2...` | 2 | 0.00 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\_SNAPSHOTS\2026-04-28_curaduria_humana\hashes_canon_post.csv`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\_SNAPSHOTS\2026-04-28_curaduria_humana\hashes_canon_pre.csv` |
| `b66b97d3956ec13e...` | 3 | 0.00 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\healthcare-clinical\vitest.config.ts`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\legal-contracts\vitest.config.ts`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\test-intelligence\vitest.config.ts` |
| `08db0bf37b222f9d...` | 3 | 0.00 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\neural-coordination\vitest.config.ts`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\perf-optimizer\vitest.config.ts`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\quantum-optimizer\vitest.config.ts` |
| `41b0ae6e54c8a63a...` | 2 | 0.00 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\hyperbolic-reasoning\tsconfig.json`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\quantum-optimizer\tsconfig.json` |
| `b2ecad7bcd1a258c...` | 2 | 0.00 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\perf-optimizer\tsconfig.json`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\test-intelligence\tsconfig.json` |
| `4177a5064b1deacf...` | 2 | 0.00 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\_SNAPSHOTS\2026-04-26\canonicos_post_purga.sha256`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\_SNAPSHOTS\2026-04-26\canonicos_pre.sha256` |

## Large Files

| size MB | gate | decision | path |
|---:|---|---|---|
| 2.01 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\claudio_face.png` |
| 1.08 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\screenshots\website.png` |
| 0.71 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\google-fonts.csv` |
| 0.31 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\claudio_api_server.py` |
| 0.15 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\claudio_avatar_web.html` |
| 0.14 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\styles.csv` |
| 0.14 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\styles.csv` |
| 0.13 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\Claudio_Cobain.ico` |
| 0.13 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\teammate-plugin\package-lock.json` |
| 0.11 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\_ARCHIVAR\2026-04-25_raiz_cleanup\KDP_METADATA.json` |
| 0.10 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\draft.csv` |
| 0.10 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\design.csv` |
| 0.10 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\src\ui-ux-pro-max\data\design.csv` |
| 0.09 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\_SNAPSHOTS\2026-04-28_curaduria_humana\validation_2026-04-28.txt` |
| 0.07 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\_SNAPSHOTS\2026-04-28_curaduria_humana\git_status_libros_pre.txt` |
| 0.07 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\teammate-plugin\src\teammate-bridge.ts` |
| 0.07 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\neural-coordination\package-lock.json` |
| 0.07 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\test-intelligence\package-lock.json` |
| 0.07 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\perf-optimizer\package-lock.json` |
| 0.06 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\hyperbolic-reasoning\package-lock.json` |
| 0.06 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\claudio_tui.py` |
| 0.06 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\prime-radiant\package-lock.json` |
| 0.06 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\quantum-optimizer\package-lock.json` |
| 0.06 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\healthcare-clinical\package-lock.json` |
| 0.06 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\cli\assets\data\products.csv` |

## Delete Candidate Sample

| gate | decision | path |
|---|---|---|
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\.claw` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\.pytest_cache` |
| `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\releases` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.claude` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.git` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\hooks-mastery\.claude` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\hooks-mastery\.git` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\humanizer\.git` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\.claude` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\.git` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\bin` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\bin` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\.claude` |
| `REVIEW` | `REVIEW_ENV_DIR_SECRET_AND_REGENERABILITY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\chart\env` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\.claude` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\bin` |
| `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\docs\releases` |
| `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\docs\reports\releases` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\examples\litellm\.claude` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\cli\simple-commands\init\.claude` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v2\src\templates\claude-optimized\.claude` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\cli\.claude` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\cli\bin` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\hooks\bin` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\@claude-flow\mcp\.claude` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\.claude` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ui-ux-pro-max\.git` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.claude` |
| `BLOCK` | `KEEP_BLOCKED_AGENT_SESSION_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.claw` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.git` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\.pytest_cache` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\__pycache__` |
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\v3\plugins\teammate-plugin\tmp.json` |

## Boundaries

- No deletion, movement, extraction or publication was executed.
- `BLOCK` rows require private/secret/claim review and cannot be cleanup targets.
- `REVIEW` rows require ficha, canonical copy or regenerability proof before a later cleanup pass.
- The CSV manifest is the evidence base for follow-up exact-duplicate and generated-residue gates.
