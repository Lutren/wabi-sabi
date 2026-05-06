# MEDIOEVO / Claudio Workspace

This is the local working workspace for MEDIOEVO, Claudio, Observacionismo / PSI-IA, Brain OS tooling, editorial products, commercial apps, websites, release assets, and a private game/TCG.

It is not ready to publish as one repo.

## Current State

The first audit is complete. See:

- `docs/control/AUDIT_REPO_TREE.md`
- `PRODUCT_MAP.md`
- `VISIBILITY_MATRIX.md`
- `RISK_REGISTER.md`
- `docs/security/SECRET_SCAN_REPORT.md`
- `DUPLICATES_AND_DEAD_CODE.md`
- `docs/release/RELEASE_READINESS_SCORE.md`
- `SOURCE_INTAKE_REGISTER.md`
- `docs/control/PORTFOLIO_EXECUTION_LEDGER.md`
- `docs/control/COMMIT_PROTOCOL.md`
- `docs/control/CLAIMS_BOUNDARY.md`
- `docs/control/ROOT_CLEANUP_INDEX_2026-05-06.md`

Release readiness score: `45 / 100` in `docs/release/RELEASE_READINESS_SCORE.md`; public release is still blocked by secrets, legal review and remaining release gates.

## Layer Map

| layer | examples | publish status |
|---|---|---|
| OPEN / developer tools | `claudio\sdk`, Brain OS tooling, selected Observacionismo tools | candidate only after secret/license review |
| COMMERCIAL | MEDIOEVO apps, productivity apps, Gumroad bundles | prepare with QA, legal drafts, support docs |
| BOOKS / EDITORIAL | MEDIOEVO books, El Observador, canon docs | full works private unless explicit publication decision |
| PRIVATE GAME | `metaevo-tcg`, TCG, game bridge | do not publish |
| ARCHIVE / VENDOR | `.skills`, vendors, pentest repos, caches, builds | exclude from releases |

## Important Roots

```txt
C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-
  -=MEDIOEVO=-\-=LIBROS
  -=MEDIOEVO=-\-=LIBROS\claudio
  -=MEDIOEVO=-\-=LIBROS\metaevo-tcg
  PRODUCTOS_MEDIOEVO
  tools\claw-code
```

## Safe Commands

```powershell
python tools/release/audit_repo.py
python tools/release/scan_secrets.py
python tools/release/find_large_files.py
python tools/release/find_duplicates.py
python tools/release/product_manifest.py
```

Packaging scripts default to dry-run. Do not force packaging until `RELEASE_CHECKLIST.md` passes.

## Control Loop

Use `docs/control/PORTFOLIO_EXECUTION_LEDGER.md` and `docs/control/COMMIT_PROTOCOL.md` before product
work. Every cycle must select one lane, verify with evidence and record residue.
Use `SOURCE_INTAKE_REGISTER.md` before absorbing material from `Downloads` or
`E:\`. Use `docs/control/CLAIMS_BOUNDARY.md` before turning research, lore or metrics into
product copy.

## Not Ready Yet

Do not publish or package broadly until:

- private game boundary is enforced;
- secrets are clean;
- license decisions are made;
- allowlist packaging exists;
- product READMEs and tests are product-specific;
- release artifacts are generated from manifests.
