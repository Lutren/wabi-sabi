# Next Publication Gate - 2026-05-02

Status: `EXECUTED_AND_VERIFIED / NEW_TARGETS_REQUIRE_FRESH_GATE`

This file records the DUAT publication run so the next run does not repeat or
duplicate live products.

## Executed GitHub Gate

| target | status | evidence |
|---|---|---|
| `Lutren/duat-genesis` | `PUBLIC_REPO_LIVE` | repo `https://github.com/Lutren/duat-genesis`; staging repo `publish_staging\open-dev\duat-genesis`, commit `3488b49`; ZIP `releases\free-dev\duat-genesis.zip`; SHA256 `f672d974d88c3190699ea16caad04b8a6de9839f20aa9513cfd7fdf51c0cbb44`; public URL HTTP `200`; evidence `qa_artifacts\release_validation\free-dev-github-publish.json` and `qa_artifacts\release_validation\duat-publication-live-verification-2026-05-02.json` |

Command executed:

```powershell
python tools\release\publish_free_dev_github.py --product duat-genesis --execute --owner-override-with-evidence --write --json
```

Do not rerun this command unless the intention is an update to the same repo and
the staging diff has been reviewed.

## Executed Gumroad Gate

| target | status | evidence |
|---|---|---|
| `duat-templates` | `GUMROAD_LIVE` | product `DUAT Templates`, URL `https://lrgonzalez.gumroad.com/l/duat-templates`, product id `pdBLzoBdg0DJ-_6hTIerdg==`, price `1900`, artifact `releases\paid\duat-templates.zip`, SHA256 `03c926b549307ef6106d80117183bb22121354671a10e0f2527473c06f6ca518`; Gumroad `published=true`; public URL HTTP `200`; evidence `qa_artifacts\release_validation\gumroad-duat-templates.json` and `qa_artifacts\release_validation\duat-publication-live-verification-2026-05-02.json` |

Command executed:

```powershell
python tools\release\publish_gumroad_listing.py --listing packages\paid\duat-templates\commerce\gumroad_listing.json --create-draft --with-file --publish --owner-override-with-evidence --write --json
```

Do not rerun as a create flow; future changes should update the existing Gumroad
product deliberately.

## Executed Website Deploy

| target | status | evidence |
|---|---|---|
| `medioevo-site` | `CLOUDFLARE_PAGES_LIVE` | deployment `fa4f39aa-93d4-4c38-a3fb-bdda712d6224`, `https://fa4f39aa.medioevo-site.pages.dev`, custom domain `https://medioevo.space/`; home, `software.html` and `apps.html` HTTP `200`; home contains direct DUAT Genesis and DUAT Templates links |

Command executed:

```powershell
wrangler pages deploy . --project-name medioevo-site --branch main --commit-dirty=true --commit-message "Add DUAT Genesis and Templates to landing"
```

Next Gumroad candidates remain product-specific: `FlujoCRM`, `Asistente
Negocio`, `Mini Office` or `Writer Workbench`, each only after its own gate.

## Claims Copy

Allowed public copy:

> DUAT Genesis is a dependency-free synthetic simulation sandbox for observable
> runs, reproducible reports and falsifier examples.

Do not claim:

- real-world prediction;
- medical, neurological, biological or market validation;
- new physics proof;
- access to DUAT Geodia private engineering;
- RPG living-world runtime.

## Evidence Files

- `release_manifests\duat-genesis.json`
- `releases\free-dev\duat-genesis.zip`
- `qa_artifacts\release_validation\free-dev-smoke-duat-genesis-2026-05-02.json`
- `qa_artifacts\release_validation\free-dev-staging-smoke-duat-genesis-2026-05-02.json`
- `qa_artifacts\release_validation\free-dev-github-dry-run-duat-genesis-2026-05-02.json`
- `qa_artifacts\release_validation\free-dev-github-publish.json`
- latest generic copies also exist as `qa_artifacts\release_validation\free-dev-smoke.json`, `qa_artifacts\release_validation\free-dev-staging-smoke.json` and `qa_artifacts\release_validation\free-dev-github-dry-run.json`
- `release_manifests\duat-templates.json`
- `releases\paid\duat-templates.zip`
- `packages\paid\duat-templates\commerce\gumroad_listing.json`
- `qa_artifacts\release_validation\gumroad-duat-templates.json`
- `qa_artifacts\release_validation\duat-publication-live-verification-2026-05-02.json`
- `-=MEDIOEVO=-\-=LIBROS\claudio\website\index.html`
- `-=MEDIOEVO=-\-=LIBROS\claudio\website\software.html`
- `-=MEDIOEVO=-\-=LIBROS\claudio\website\apps.html`
- `PUBLISHING_PLAN.md`
- `RELEASE_READINESS_SCORE.md`
