# Global Curador SETO Dry Audit 2026-05-05

Status: `DRY_RUN_NO_DELETE_NO_MOVE`
Scan mode: `incremental`

This report implements a dry Curador pass over the selected roots. It records evidence for later cleanup gates; it does not approve deletion by itself.

## Artifacts

- JSON summary: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-seto-audit-2026-05-05-downloads_max25.json`
- CSV file manifest: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\release_validation\global-curador-file-manifest-2026-05-05-downloads_max25.csv`
- WitnessLog: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\qa_artifacts\witness_log\curador_seto_witnesslog.jsonl`

## Counts

| metric | value |
|---|---:|
| `files` | 25 |
| `generated_dirs_recorded` | 0 |
| `project_roots_detected` | 0 |
| `errors` | 0 |
| `hashed_files` | 25 |
| `zip_or_archive_files` | 0 |
| `exact_duplicate_groups` | 0 |
| `version_review_groups` | 0 |

## Resume

| field | value |
|---|---|
| `truncated` | `True` |
| `processed_files` | `25` |
| `max_files` | `25` |
| `next_start_after` | `C:\Users\L-Tyr\Downloads\27.png` |

## Root Stats

| root | exists | files | dirs | MB | hashed | hash_skipped | generated_dirs_skipped |
|---|---:|---:|---:|---:|---:|---:|---:|
| `downloads` | True | 25 | 1 | 38.75 | 25 | 0 | 0 |

## Focus Stats

| focus | files | MB | hashed |
|---|---:|---:|---:|
| `psi` | 0 | 0.00 | 0 |
| `downloads` | 25 | 38.75 | 25 |
| `desktop` | 0 | 0.00 | 0 |
| `workspace` | 0 | 0.00 | 0 |
| `e_drive` | 0 | 0.00 | 0 |

## ActionGate Summary

| gate | count |
|---|---:|
| `REVIEW` | 25 |

## Decision Summary

| decision | count |
|---|---:|
| `KEEP_OR_REVIEW` | 25 |

## Exact Duplicate Groups

| sha256 | count | duplicate MB if one kept | gate | examples |
|---|---:|---:|---|---|

## Large Files

| size MB | gate | decision | path |
|---:|---|---|---|
| 2.23 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\11.png` |
| 2.15 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\17.png` |
| 2.08 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\20.png` |
| 2.06 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\27.png` |
| 2.04 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\15.png` |
| 2.01 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\13.png` |
| 1.99 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\24.png` |
| 1.98 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\25.png` |
| 1.97 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\14.png` |
| 1.97 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\2.png` |
| 1.91 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\12.png` |
| 1.86 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\26.png` |
| 1.84 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\10.png` |
| 1.83 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\1.png` |
| 1.83 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\22.png` |
| 1.82 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\19.png` |
| 1.77 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\21.png` |
| 1.59 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\16.png` |
| 1.57 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\23.png` |
| 1.46 | `REVIEW` | `KEEP_OR_REVIEW` | `C:\Users\L-Tyr\Downloads\18.png` |

## Delete Candidate Sample

| gate | decision | path |
|---|---|---|

## Boundaries

- No deletion, movement, extraction or publication was executed.
- `BLOCK` rows require private/secret/claim review and cannot be cleanup targets.
- `REVIEW` rows require ficha, canonical copy or regenerability proof before a later cleanup pass.
- The CSV manifest is the evidence base for follow-up exact-duplicate and generated-residue gates.
