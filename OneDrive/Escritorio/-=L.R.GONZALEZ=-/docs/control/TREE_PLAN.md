# TREE_PLAN

Status: proposal only. Do not move files from this plan without updating `MIGRATION_MAP.md`.

## Target Tree

```txt
/
  AGENTS.md
  README.md
  LICENSE
  CHANGELOG.md
  ROADMAP.md
  RELEASE_CHECKLIST.md
  SECURITY.md
  CONTRIBUTING.md

  apps/
    argus-desktop/
    claudio-desktop/
    medioevo-desktop/
    mini-office/

  packages/
    observacionismo-gate/
    psi-ia-toolkit/
    brain-os/
    claudio-os-blueprint/
    codex-agent-pack/

  books/
    el-observador/
    medioevo-samples/
    companion-pdfs/

  game-private/
    README_PRIVATE.md
    DO_NOT_PUBLISH.md

  docs/
    canon/
    developer/
    product/
    publishing/
    business/
    legal/

  tools/
    audit/
    build/
    release/
    codex/

  website/
    landing/
    gumroad/
    buymeacoffee/
    assets/

  releases/
    free-dev/
    paid-apps/
    editorial/

  _archive/
```

## Current-To-Target Mapping Draft

| current | target proposal | status |
|---|---|---|
| `-=MEDIOEVO=-\-=LIBROS\claudio\sdk` | `packages/observacionismo-gate` | candidate |
| `PRODUCTOS_MEDIOEVO\claudio_os_blueprint` | `packages/claudio-os-blueprint` | candidate canon |
| `-=MEDIOEVO=-\-=LIBROS\claudio\brain_os` | `packages/brain-os` | review |
| `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-` | `packages/psi-ia-toolkit` plus `books/el-observador` | split required |
| `-=MEDIOEVO=-\-=LIBROS\claudio\apps\argus_desktop` | `apps/argus-desktop` | commercial/internal review |
| `-=MEDIOEVO=-\-=LIBROS\claudio\mini_office` | `apps/mini-office` | commercial/open-core decision |
| `-=MEDIOEVO=-\-=LIBROS\claudio\products\asistente_negocio` | `apps/medioevo-desktop/asistente-negocio` | commercial |
| `-=MEDIOEVO=-\-=LIBROS\claudio\products\crm` | `apps/commercial/flujocrm` | commercial; source package verified, installer pending |
| `-=MEDIOEVO=-\-=LIBROS\claudio\website` | `website/landing` | public surface review |
| `-=MEDIOEVO=-\-=LIBROS\MEDIOEVO_BESTSELLER_OUTPUT` | `books/medioevo-samples` and `releases/editorial` | split required |
| `-=MEDIOEVO=-\-=LIBROS\metaevo-tcg` | `game-private/metaevo-tcg` | private only; do not move yet |
| `.skills`, `tools/vendor`, `tools/pentest_repos` | `_archive/vendor-review` | do not publish |

## Notes

- This should probably become a new clean release repo, not a history-preserving move of the dirty workspace.
- Root workspace can remain operational while clean release packages are generated from allowlists.
- Game-private should be a separate private repo or excluded subtree, not a public folder in a public repo.
