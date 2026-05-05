# Global Curador SETO Dry Audit 2026-05-05

Status: `DRY_RUN_NO_DELETE_NO_MOVE`
Scan mode: `incremental`

This report implements a dry Curador pass over the selected roots. It records evidence for later cleanup gates; it does not approve deletion by itself.

## Artifacts

- JSON summary: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-seto-audit-2026-05-05-workspace_lrgonzalez_max500_resumecf45b2507d.json`
- CSV file manifest: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-file-manifest-2026-05-05-workspace_lrgonzalez_max500_resumecf45b2507d.csv`
- WitnessLog: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\witness_log\curador_seto_witnesslog.jsonl`

## Counts

| metric | value |
|---|---:|
| `files` | 500 |
| `generated_dirs_recorded` | 9 |
| `project_roots_detected` | 7 |
| `errors` | 0 |
| `hashed_files` | 51 |
| `zip_or_archive_files` | 0 |
| `exact_duplicate_groups` | 9 |
| `version_review_groups` | 15 |

## Resume

| field | value |
|---|---|
| `truncated` | `True` |
| `processed_files` | `500` |
| `max_files` | `500` |
| `start_after_found` | `True` |
| `next_start_after` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\lib\types\MessageUpdate.ts` |

## Root Stats

| root | exists | files | dirs | MB | hashed | hash_skipped | generated_dirs_skipped |
|---|---:|---:|---:|---:|---:|---:|---:|
| `workspace_lrgonzalez` | True | 500 | 399 | 8.11 | 51 | 6 | 9 |

## Focus Stats

| focus | files | MB | hashed |
|---|---:|---:|---:|
| `psi` | 0 | 0.00 | 0 |
| `downloads` | 0 | 0.00 | 0 |
| `desktop` | 500 | 8.11 | 51 |
| `workspace` | 500 | 8.11 | 51 |
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
| `CANDIDATE_DELETE_EMPTY_REVIEW` | 1 |

## Exact Duplicate Groups

| sha256 | count | duplicate MB if one kept | gate | examples |
|---|---:|---:|---|---|
| `eaa93e65d11b96a2...` | 2 | 0.06 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\docs\adr\ADR-037-AUTOPILOT-CHAT-MODE.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\docs\adr\ADR-037-AUTOPILOT-CHAT-MODE.md` |
| `47160ddcdbda79bb...` | 2 | 0.06 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\docs\adr\ADR-029-HUGGINGFACE-CHAT-UI-CLOUD-RUN.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\docs\adr\ADR-029-HUGGINGFACE-CHAT-UI-CLOUD-RUN.md` |
| `70a909411f1e26d9...` | 2 | 0.02 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\mcp-bridge\test-harness.js`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\mcp-bridge\test-harness.js` |
| `22b5ade511d386fd...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\docs\adr\ADR-035-MCP-TOOL-GROUPS.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\docs\adr\ADR-035-MCP-TOOL-GROUPS.md` |
| `c187e6fffcc392ba...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\docs\adr\ADR-034-OPTIONAL-MCP-BACKENDS.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\docs\adr\ADR-034-OPTIONAL-MCP-BACKENDS.md` |
| `8b73899a6dc88e86...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\mcp-bridge\mcp-stdio-kernel.js`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\mcp-bridge\mcp-stdio-kernel.js` |
| `cd7f7990d5d0ed22...` | 2 | 0.01 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\docs\adr\ADR-033-RUVECTOR-RUFLO-MCP-INTEGRATION.md`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\docs\adr\ADR-033-RUVECTOR-RUFLO-MCP-INTEGRATION.md` |
| `16a0aa1bbd3aac84...` | 2 | 0.00 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\mcp-bridge\Dockerfile`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\mcp-bridge\Dockerfile` |
| `a60352e95bcc6ae6...` | 2 | 0.00 | `REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\mcp-bridge\package.json`<br>`C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\mcp-bridge\package.json` |

## Large Files

| size MB | gate | decision | path |
|---:|---|---|---|
| 1.24 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\chat-ui\static\chatui\omni-welcome.gif` |
| 0.92 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\assets\ruFlo.png` |
| 0.38 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\package-lock.json` |
| 0.30 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\lib\server\fonts\Inter-ExtraBold.ttf` |
| 0.30 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\lib\server\fonts\Inter-Black.ttf` |
| 0.30 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\lib\server\fonts\Inter-Bold.ttf` |
| 0.30 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\lib\server\fonts\Inter-SemiBold.ttf` |
| 0.30 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\lib\server\fonts\Inter-Medium.ttf` |
| 0.30 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\lib\server\fonts\Inter-ExtraLight.ttf` |
| 0.30 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\lib\server\fonts\Inter-Thin.ttf` |
| 0.30 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\lib\server\fonts\Inter-Light.ttf` |
| 0.30 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\lib\server\fonts\Inter-Regular.ttf` |
| 0.13 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\assets\ruflo-small.jpeg` |
| 0.07 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\mcp-bridge\index.js` |
| 0.07 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\.claude\helpers\context-persistence-hook.mjs` |
| 0.07 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\mcp-bridge\index.js` |
| 0.06 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\docs\adr\ADR-037-AUTOPILOT-CHAT-MODE.md` |
| 0.06 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\docs\adr\ADR-037-AUTOPILOT-CHAT-MODE.md` |
| 0.06 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\docs\adr\ADR-029-HUGGINGFACE-CHAT-UI-CLOUD-RUN.md` |
| 0.06 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\docs\adr\ADR-029-HUGGINGFACE-CHAT-UI-CLOUD-RUN.md` |
| 0.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\docs\adr\ADR-014-CHAT-SYSTEM-ARCHITECTURE.md` |
| 0.03 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\.claude\helpers\learning-service.mjs` |
| 0.03 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\.github\workflows\integration-tests.yml` |
| 0.03 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\src\lib\server\database\rvf.ts` |
| 0.03 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\.claude\skills\hooks-automation\SKILL.md` |

## Delete Candidate Sample

| gate | decision | path |
|---|---|---|
| `REVIEW` | `CANDIDATE_DELETE_REGENERABLE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\.pytest_cache` |
| `REVIEW` | `CANDIDATE_ARCHIVE_OR_LINEAGE_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\releases` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.git` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\hooks-mastery\.git` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\humanizer\.git` |
| `BLOCK` | `KEEP_BLOCKED_GIT_HISTORY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\.git` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\bin` |
| `REVIEW` | `REVIEW_BINARY_OR_TOOL_DIR` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\bin` |
| `REVIEW` | `REVIEW_ENV_DIR_SECRET_AND_REGENERABILITY` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\chart\env` |
| `REVIEW` | `CANDIDATE_DELETE_EMPTY_REVIEW` | `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\.skills\ruflo\ruflo\src\ruvocal\scripts\setups\vitest-setup-client.ts` |

## Boundaries

- No deletion, movement, extraction or publication was executed.
- `BLOCK` rows require private/secret/claim review and cannot be cleanup targets.
- `REVIEW` rows require ficha, canonical copy or regenerability proof before a later cleanup pass.
- The CSV manifest is the evidence base for follow-up exact-duplicate and generated-residue gates.
