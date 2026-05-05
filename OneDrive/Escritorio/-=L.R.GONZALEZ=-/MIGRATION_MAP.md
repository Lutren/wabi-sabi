# MIGRATION_MAP

Status: initialized with safe archive moves only.

| date | source | destination | action | reason | verification |
|---|---|---|---|---|---|
| 2026-04-29 | n/a | n/a | report-only | Fase 0 and governance docs created | files exist in workspace root |
| 2026-04-29 | `-=MEDIOEVO=-\-=LIBROS\claudio\apps\argus_desktop\package-lock.json` | `_archive\legacy\2026-04-29\argus_desktop_lockfile_repair\package-lock.corrupt-2026-04-29.json` | archived corrupt lockfile | original lock had corrupted package names/integrities (`[elichicado]`, `terchical`, `chokdar`, `pves`) | new lock generated; `npm ci --dry-run`, `npm run typecheck`, `npm run build` passed |
| 2026-04-29 | `-=MEDIOEVO=-\-=LIBROS\claudio\apps\argus_desktop\node_modules` | `_archive\legacy\2026-04-29\argus_generated_artifacts\node_modules` | archived generated artifact | dependency install generated during verification | archive copy exists; active ignored copy remains and is release-denied |
| 2026-04-29 | `-=MEDIOEVO=-\-=LIBROS\claudio\apps\argus_desktop\dist` | `_archive\legacy\2026-04-29\argus_generated_artifacts\dist` | archived generated artifact | Vite build output generated during verification | archive copy exists; active ignored copy remains and is release-denied |
| 2026-04-29 | `packages\obsai-core` | `packages\open-dev\obsai-core` | copied allowlist | final open-dev physical separation; legacy source left in place | 12 files copied; denied caches/builds excluded |
| 2026-04-29 | `apps\residueos` | `packages\open-dev\residueos` | copied allowlist | ResidueOS fixed as MIT open-dev tooling | 11 files copied; runtime state excluded |
| 2026-04-29 | `-=MEDIOEVO=-\-=LIBROS\claudio\sdk` | `packages\open-dev\observacionismo-gate` | copied allowlist | SDK fixed as MIT open-dev package | 7 files copied |
| 2026-04-29 | `PRODUCTOS_MEDIOEVO\claudio_os_blueprint` | `packages\open-dev\claudio-os-blueprint` | copied allowlist | canonical open blueprint package; no ISO claim | 33 files copied |
| 2026-04-29 | `-=MEDIOEVO=-\-=LIBROS\claudio\apps\argus_desktop` | `apps\commercial\argus-desktop` | copied allowlist | commercial/internal app separation | 52 files copied; `node_modules`, `dist`, logs and screenshots excluded |
| 2026-04-29 | `-=MEDIOEVO=-\-=LIBROS\claudio\products\asistente_negocio` | `apps\commercial\asistente-negocio` | copied allowlist | commercial app separation | 28 files copied; build/release/preview artifacts excluded |
| 2026-04-29 | `-=MEDIOEVO=-\-=LIBROS\claudio\products\crm` | `apps\commercial\flujocrm` | copied allowlist | commercial app separation | 9 files copied; generated artifacts excluded |
| 2026-04-29 | `-=MEDIOEVO=-\-=LIBROS\claudio\mini_office` | `apps\commercial\mini-office` | copied allowlist | commercial app candidate separation | 50 files copied; `.git` and caches excluded |
| 2026-04-29 | n/a | `packages\open-dev\gemma-observacionismo-cleanup` | created package | public-safe Gemma + Observacionismo cleanup toolkit | MIT license, synthetic fixtures, tests and CLI created |
| 2026-04-29 | `-=MEDIOEVO=-\-=LIBROS\claudio\apps\argus_desktop\{node_modules,dist}` and `apps\commercial\argus-desktop\{node_modules,dist}` | `_archive\legacy\2026-04-29\argus_generated_artifacts_second_pass\*` | archived generated artifacts | keep Argus source free of generated dependencies/build output after QA | final dry-run reports all four active artifact paths missing |
| 2026-05-01 | large generated/product artifacts under `tools\claw-code\rust\target`, `apps\commercial\argus-desktop\node_modules`, `-=MEDIOEVO=-\-=LIBROS\claudio\products\*.zip`, `gumroad_live\*.zip`, `Termux.apk`, `voices\piper\en_US-lessac-medium.onnx` | `E:\MEDIOEVO_OFFLOAD\2026-05-01-host-gate\...` | offloaded with relative paths preserved | reduce C: disk pressure before gated publication attempt | evidence in `qa_artifacts\release_validation\host-gate-offload-2026-05-01.json`; C: free space rose to 33.23 GB; no public upload |
| 2026-05-05 | n/a | n/a | report-only | Curador SETO global dry audit created manifests only; no move/delete/extract | `docs\intake\GLOBAL_CURADOR_SETO_AUDIT_2026-05-05.md`, `qa_artifacts\release_validation\global-curador-seto-audit-2026-05-05.json`, WitnessLog event `8189746031215a2705ffda47760c16285f982dc651ce6f89ecb6be54c2ea9388` |

## Proposed Moves Pending Approval

| source | destination | reason | status |
|---|---|---|---|
| `PRODUCTOS_MEDIOEVO\claudio_os_blueprint` | `packages/claudio-os-blueprint` | likely canonical blueprint | pending canonical decision |
| `-=MEDIOEVO=-\-=LIBROS\claudio\sdk` | `packages/observacionismo-gate` | open developer SDK candidate | pending secret/license/test review |
| `-=MEDIOEVO=-\-=LIBROS\metaevo-tcg` | private repo or `game-private/metaevo-tcg` | private boundary | do not move in public workspace yet |
| `-=MEDIOEVO=-\-=LIBROS\claudio\products\asistente_negocio` | `apps/medioevo-desktop/asistente-negocio` | commercial app | pending QA/legal |
| `-=MEDIOEVO=-\-=LIBROS\claudio\products\crm` | `apps\commercial\flujocrm` | commercial app | copied allowlist; installer QA/legal pending |

## Rule

Every future move must be recorded here before and after execution.
