# Product Staging Ledger - 2026-05-06

Status: `REVIEW / PARTIAL_CANON`

`PRODUCTOS_MEDIOEVO` is a legacy product staging folder. It is not the final
architecture, but some of its contents are useful and tested enough to keep as
source candidates.

## Promoted

| source | lane | reason |
|---|---|---|
| `PRODUCTOS_MEDIOEVO/claudio_os_blueprint` | open/dev blueprint review | low-claim ClaudioOS/Brain OS blueprint with configs, examples and docs |
| `PRODUCTOS_MEDIOEVO/content_forge` | commercial/internal product review | local renderer source and public placeholder assets |
| `PRODUCTOS_MEDIOEVO/model_slimmer_evidence.py` | research/tooling review | measurement contract for replacing model baselines |
| `PRODUCTOS_MEDIOEVO/observacionismo_dsl.py` | language/tooling review | small DSL compiler for observable action contracts |
| product category READMEs | product map support | lightweight product split |

## Kept Out

| pattern | reason |
|---|---|
| `PRODUCTOS_MEDIOEVO/*.pdf` | absorbed/reference artifact, not editable source |
| `PRODUCTOS_MEDIOEVO/*.zip` | release/package artifact, keep hash/manifests instead |
| `PRODUCTOS_MEDIOEVO/*.txt` | raw notes/prompts, absorb into docs before use |
| `PRODUCTOS_MEDIOEVO/_ARCHIVAR_2026-04-24/` | cold archive |
| `PRODUCTOS_MEDIOEVO/04_AUDIOVISUAL_Y_TCG/` | private/TCG boundary |
| `PRODUCTOS_MEDIOEVO/content_forge/runtime/` | generated renders/logs |

## Validation

- Secret scan of promoted product paths: `0` findings.
- Python compile for promoted scripts: pass.
- No external publication, upload, account update or push performed.

## Next Migration

Move source candidates into the cleaner lanes only after a path-specific
migration manifest:

- `PRODUCTOS_MEDIOEVO/content_forge` -> `apps/commercial/content-forge`
- `PRODUCTOS_MEDIOEVO/claudio_os_blueprint` -> `packages/claudio-os-blueprint`
- raw product notes -> `docs/product/legacy/` after summary and claim scan
