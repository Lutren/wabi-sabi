# One Universe Control - MEDIOEVO

Generated UTC: `2026-05-06T03:34:41.888492+00:00`

Principio: un solo universo, varios carriles. Nada queda huerfano; nada entra al canon sin ruta, gate y evidencia.

## Resumen

| metrica | valor |
|---|---:|
| `total_paths` | 187 |
| `by_lane` | `18` grupos |
| `by_decision` | `6` grupos |
| `by_gate` | `2` grupos |
| `by_git_status` | `2` grupos |
| `flag_counts` | `7` grupos |

## Gates

| gate | rutas |
|---|---:|
| `BLOCK` | 6 |
| `REVIEW` | 181 |

## Carriles Canonicos

| carril | prefijos |
|---|---|
| `control` | `.gitignore, AGENTS.md, README.md, AUDIT_REPO_TREE.md, TREE_PLAN.md, MIGRATION_MAP.md, DELETE_CANDIDATES.md, DELETED_OR_ARCHIVED.md, SOURCE_INTAKE_REGISTER.md` |
| `github_ci` | `.github/` |
| `comms` | `COMMS/` |
| `docs` | `docs/` |
| `runtime_state` | `runtime/` |
| `qa_evidence` | `qa_artifacts/, release_manifests/` |
| `apps` | `apps/` |
| `packages` | `packages/` |
| `books` | `books/` |
| `research` | `research/` |
| `website` | `website/` |
| `tools` | `tools/` |
| `tests` | `tests/` |
| `licenses` | `LICENSES/` |
| `hackathons` | `hackathons/` |
| `publish_staging` | `publish_staging/` |
| `products_staging` | `PRODUCTOS_MEDIOEVO/` |
| `medioevo_core` | `-=MEDIOEVO=-/` |
| `agent_sessions` | `.claw/` |
| `private_game` | `game-private/, -=MEDIOEVO=-/-=LIBROS/metaevo-tcg/, -=MEDIOEVO=-/-=LIBROS/claudio/tcg/` |
| `archive` | `_archive/, releases/` |

## Decisiones Por Carril

| carril | rutas |
|---|---:|
| `agent_sessions` | 1 |
| `apps` | 4 |
| `archive` | 2 |
| `books` | 1 |
| `control` | 2 |
| `docs` | 86 |
| `github_ci` | 1 |
| `hackathons` | 1 |
| `licenses` | 1 |
| `medioevo_core` | 1 |
| `packages` | 3 |
| `private_game` | 1 |
| `products_staging` | 1 |
| `publish_staging` | 1 |
| `qa_evidence` | 76 |
| `research` | 1 |
| `tools` | 3 |
| `website` | 1 |

## Acciones Siguientes

| orden | accion | gate | decision |
|---:|---|---|---|
| 1 | Root control | `REVIEW` | Mantener AGENTS, Atlas, MIGRATION_MAP, DELETE_CANDIDATES y reportes como sistema nervioso del universo. |
| 2 | Regenerable residue | `APPROVE if path-specific cache rule passes` | Borrar o ignorar solo caches/builds regenerables con reporte; no borrar fuentes unicas. |
| 3 | MEDIOEVO core extraction | `REVIEW` | No mover todo -=MEDIOEVO=- de golpe; extraer a root lanes solo piezas con ficha, hash y destino canonico. |
| 4 | Private boundary | `BLOCK` | Juego, TCG, sesiones, secretos y cuentas quedan bloqueados fuera de open/commercial. |
| 5 | Vendor/imported trees | `REVIEW` | Referenciar, archivar o excluir; no convertirlos en tecnologia principal salvo modulo minimo extraido. |

## Muestra De Rutas

| git | gate | carril | decision | ruta |
|---|---|---|---|---|
| ` M` | `REVIEW` | `control` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `AGENTS.md` |
| ` M` | `REVIEW` | `control` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `SOURCE_INTAKE_REGISTER.md` |
| `??` | `REVIEW` | `medioevo_core` | `KEEP_AS_CORE_SOURCE_UNTIL_EXTRACTED_TO_ROOT_LANES` | `-=MEDIOEVO=-/` |
| `??` | `BLOCK` | `agent_sessions` | `KEEP_LOCAL_AGENT_SESSION_HISTORY_NOT_MAIN_CANON` | `.claw/` |
| `??` | `REVIEW` | `github_ci` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `.github/` |
| `??` | `REVIEW` | `licenses` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `LICENSES/` |
| `??` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/` |
| `??` | `REVIEW` | `archive` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `_archive/` |
| `??` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/README.md` |
| `??` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/argus-desktop/README.md` |
| `??` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/` |
| `??` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/residueos/` |
| `??` | `REVIEW` | `books` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `books/` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/GITHUB_PROFILE_BIO_PATCH_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/GITHUB_PROFILE_README_SPONSORS_PATCH_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/GITHUB_SPONSORS_DASHBOARD_MANUAL_AUTH_EVIDENCE_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/GITHUB_SPONSORS_EXTERNAL_ACTIONS_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/GITHUB_SPONSORS_LIVE_AUDIT_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/GITHUB_SPONSORS_PREP_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/GITHUB_SPONSORS_TIERS_GOALS_PATCH_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/GOOGLE_RAPID_AGENT_HACKATHON_2026.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/INDEX.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/OBS_ANTIGRAVITY_RUNTIME_REVIEW_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/OBS_EOR_AIA_TOPOLOGY_REVIEW_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/OBS_INFO_KERNEL_REVIEW_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/PAID_APPS_LOCAL_PACKAGES_EVIDENCE_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/PRODUCT_CONTINUATION_FLUJOCRM_WAVE_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/SPONSORS_PROFILE_COPY_LIVE_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/WAVE_FC_EVIDENCE_PACK_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/business/INDEX.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/business/PATRIMONIO_DIGITAL_PRIVATE_ACTIONS_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/canon/INDEX.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/canon/hormiguero-ciudad-viva.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/design/` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/CEREBRO_DUAT_BRAIN_OS_OBSERVACIONISMO_HANDOFF_2026-05-05.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/CLAIM_FALSIFICATION_REGISTER_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/CURADOR_ALWAYS_ON_PROTOCOL_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/DEPENDENCY_ADOPTION_GATE_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/DUAT_CLAUDIO_APP_EXTRACTION_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/DUAT_RPG_PRIVATE_LIVING_WORLD_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/E_DRIVE_PUBLICATION_BOUNDARY_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/OBSERVACIONISMO_LAB_FALSIFICATION_BRIEF_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/OBSERVACIONISMO_LAB_SMOKE_RESULTS_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/OBSERVACIONISMO_MINIMAL_MACHINE_LANGUAGE_2026-05-05.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/OPEN_SOURCE_MAX_PATRIMONY_IMPLEMENTATION_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/PSI_CHI_SPARC_RESULTS_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/SENSORIUM_CLAUDIO_AI_ENGINEERING_EXTRACTION_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/TECHNOLOGY_IMPLEMENTATION_BACKLOG_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/UNIFIED_WORKTREE_OBSERVACIONISTA_PLAN_2026-05-04.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/developer/psi_chi_results/` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/editorial/` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/ARGUS_ARCHIVE_GENERATED_ARTIFACTS_FICHA_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/ASISTENTE_WIN_UNPACKED_CLEANUP_FICHA_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/CAMERA_FRAMES_OPPO_RUNTIME_FICHA_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/CEREBRO_DUAT_BRAIN_OS_OBSERVACIONISMO_FICHAS_2026-05-05.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/DOWNLOADS_CLEANUP_MANIFEST_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/DOWNLOADS_RECENT_PASTED_SOURCES_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/DOWNLOADS_REMAINING_REVIEW_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/DUAT_GEODIA_DOWNLOADS_INTAKE_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/OBSERVACIONISMO_LAB_V3_INSIGHTS_INTAKE_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/OBSERVACIONISMO_LANGUAGE_DOWNLOADS_PSI_INTAKE_2026-05-05.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/OBSERVACIONISTA_LOCAL_CODE_AGENT_INTAKE_2026-05-04.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/PORTFOLIO_CURADOR_AUDIT_2026-05-05.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/PSI_CHI_SPARC_LAB_INTAKE_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/PSI_DOWNLOADS_CANON_CONTRACT_INTAKE_2026-05-05.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/RUFLO_MODEL_DUPLICATE_CLEANUP_FICHA_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/SENSORIUM_INVERSION_LAB_INTAKE_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/SENSORIUM_PSI_BRIDGE_INTAKE_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/legal/COMMERCIAL_RELEASE_LEGAL_MATRIX_2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/legal/INDEX.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/AGENT_PRODUCT_FICHAS_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/COMMERCIAL_AGENT_PUBLICATION_MATRIX_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/DUAT_GEODIA_TECHNICAL_FICHAS_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/README.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/agent_product_fichas_2026-05-02.json` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/argus-desktop.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/books-editorial.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/brain-os-lite.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/claudio-os-blueprint.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/duat-genesis.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/geodia-social-observatory.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/hormiguero-rpg-command-center-analysis.md` |
| `??` | `BLOCK` | `docs` | `KEEP_PRIVATE_BOUNDARY_NOT_PUBLIC_CANON` | `docs/product/metaevo-tcg-private.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/observacionismo-gate.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/paid-app-deliverable-boundary-2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/product-listing-deliverable-alignment-2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/wave-collapse.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/wave-fc-client-operating-model.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/wave-fc-public-safe-release-closure-2026-05-01.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/publishing/GITHUB_LINKEDIN_PUBLICATION_PACKET_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/publishing/GITHUB_PUBLIC_SANITIZED_WHITEPAPERS_2026-05-02.md` |
| `??` | `BLOCK` | `docs` | `BLOCK_SECRET_OR_ACCOUNT_SURFACE` | `docs/publishing/GUMROAD_LISTING_OPTIMIZATION_PACKET_2026-05-05.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/publishing/LEGACY_PUBLICATION_SCRIPT_INVENTORY_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/publishing/LUIS_RENE_GONZALEZ_LOPEZ_PUBLIC_PROFILE_ANALYSIS_2026-05-03.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/publishing/NEXT_PUBLICATION_GATE_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/publishing/OPEN_CORE_UI_PAID_PUBLICATION_RUNBOOK_2026-05-02.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/publishing/PUBLICACION_PERFILES_OBSERVATORIO_AGENT_2026-05-05.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/publishing/SOCIAL_CONTENT_CALENDAR_2026-05.md` |
| `??` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/publishing/WEBSITE_PUBLIC_FUNNEL_REVIEW_2026-05-05.md` |
| `??` | `BLOCK` | `private_game` | `KEEP_PRIVATE_BOUNDARY_NOT_PUBLIC_CANON` | `game-private/` |
| `??` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/` |
| `??` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/README.md` |
| `??` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/obsai-core/` |
| `??` | `REVIEW` | `packages` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `packages/paid/` |
| `??` | `REVIEW` | `publish_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `publish_staging/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/2026-04-29-hormiguero-city/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/2026-04-29-wave-collapse-name-test.md` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/2026-05-01-wave-fc-captures/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/asistente_negocio_final_package_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/asistente_negocio_windows_install_2026-05-02-r2/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/asistente_negocio_windows_install_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/duat_audit_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/flujocrm_current_user_install_2026-05-02-r2/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/flujocrm_current_user_install_2026-05-02-r3/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/flujocrm_current_user_install_2026-05-02-r4-final/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/flujocrm_current_user_install_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/flujocrm_sqlite_install_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/flujocrm_win_unpacked_repro_2026-05-02/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/github_sponsors_dashboard_2026-05-01/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/obs_info_kernel_validation_2026-05-03/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/observacionismo_language/` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/aggressive-cleanup-publication-gate-2026-05-03.md` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/argus-archive-generated-artifacts-second-pass-cleanup-dry-run-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/argus-archive-generated-artifacts-second-pass-cleanup-result-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-release-empty-dir-actiongate-metadata-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-release-empty-dir-cleanup-result-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-release-residue-actiongate-metadata-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-release-residue-cleanup-dry-run-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-release-residue-cleanup-result-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-win-unpacked-actiongate-metadata-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-win-unpacked-cleanup-dry-run-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/asistente-win-unpacked-cleanup-result-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/camera-frames-actiongate-metadata-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/camera-frames-cleanup-dry-run-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/camera-frames-cleanup-result-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/curador-audit-2026-05-05-sponsors-cleanup.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/downloads-cleanup-manifest-2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/downloads-cleanup-result-2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/duat-publication-live-verification-2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/duplicate-hash-dry-run-2026-05-05.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/external_repos_verification_2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-github-dry-run-duat-genesis-2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-github-dry-run.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-github-publish.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-smoke-duat-genesis-2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-smoke.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-staging-smoke-duat-genesis-2026-05-02.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-staging-smoke.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/free-dev-staging.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/github-impact-improvements-2026-05-03.md` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/github-public-sanitized-dry-run.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/github-public-sanitized-publish.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/github-public-sanitized-staging.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/github-publication-live-verification-2026-05-03.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/global-curador-file-manifest-2026-05-05-workspace_lrgonzalez_max5000.csv` |
| `??` | `BLOCK` | `qa_evidence` | `BLOCK_SECRET_OR_ACCOUNT_SURFACE` | `qa_artifacts/release_validation/gumroad-duat-templates.json` |
| `??` | `BLOCK` | `qa_evidence` | `BLOCK_SECRET_OR_ACCOUNT_SURFACE` | `qa_artifacts/release_validation/gumroad-medioevo-agent-ops-pack.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/host-gate-offload-2026-05-01.json` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/local-cli-security-gate-2026-05-03.md` |
| `??` | `REVIEW` | `qa_evidence` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `qa_artifacts/release_validation/mini-office-cleanup-2026-05-03.json` |

## Reglas

- One universe does not mean flattening every folder into one directory.
- A route is canon only when it has lane, purpose, gate, evidence and owner.
- Untracked agent output is production residue until integrated into a lane.
- Generated caches can be deleted by rule; unique sources move only with ficha and migration map.
- Private, secret-like and external-action surfaces never become public canon by accident.
