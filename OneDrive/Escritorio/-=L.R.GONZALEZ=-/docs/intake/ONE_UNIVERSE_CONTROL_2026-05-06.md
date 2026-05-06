# One Universe Control - MEDIOEVO

Generated UTC: `2026-05-06T04:22:28.498898+00:00`

Principio: un solo universo, varios carriles. Nada queda huerfano; nada entra al canon sin ruta, gate y evidencia.

## Resumen

| metrica | valor |
|---|---:|
| `total_paths` | 285 |
| `by_lane` | `17` grupos |
| `by_decision` | `4` grupos |
| `by_gate` | `2` grupos |
| `by_git_status` | `2` grupos |
| `flag_counts` | `4` grupos |

## Gates

| gate | rutas |
|---|---:|
| `BLOCK` | 7 |
| `REVIEW` | 278 |

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
| `apps` | 43 |
| `books` | 3 |
| `comms` | 1 |
| `control` | 1 |
| `docs` | 23 |
| `github_ci` | 1 |
| `hackathons` | 16 |
| `licenses` | 4 |
| `packages` | 32 |
| `private_game` | 3 |
| `products_staging` | 66 |
| `qa_evidence` | 16 |
| `research` | 51 |
| `tests` | 3 |
| `tools` | 15 |
| `unknown_review` | 5 |
| `website` | 2 |

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
| `A ` | `REVIEW` | `github_ci` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `.github/FUNDING.yml` |
| `M ` | `REVIEW` | `control` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `.gitignore` |
| `M ` | `REVIEW` | `comms` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `COMMS/topics/seto-observacionismo-decisions.jsonl` |
| `A ` | `REVIEW` | `licenses` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `LICENSES/EDITORIAL_ALL_RIGHTS_RESERVED.txt` |
| `A ` | `REVIEW` | `licenses` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `LICENSES/MIT.txt` |
| `A ` | `REVIEW` | `licenses` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `LICENSES/PROPRIETARY_COMMERCIAL.txt` |
| `A ` | `REVIEW` | `licenses` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `LICENSES/README.md` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/00_LEER_PRIMERO.md` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/01_LIBROS_Y_BUNDLES/README.md` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/02_SOFTWARE_LOCAL/README.md` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/03_OPEN_SOURCE_GITHUB/README.md` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/05_BETAS_Y_PROXIMAMENTE/README.md` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/README.md` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/browser-manifests/suno_create_download_track.json` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/contracts/module_manifest.schema.json` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/docs/ARCHITECTURE.md` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/docs/BRAIN_OS_PRINCIPLES.md` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/docs/COMPATIBILITY_MATRIX.md` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/docs/MODEL_EFFICIENCY.md` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/docs/OBSERVACIONISMO_OS.md` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/docs/ROADMAP.md` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/examples/decision_browser_blocked.json` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/examples/decision_publish_requires_approval.json` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/examples/decision_safe.json` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/examples/model_slimmer_qwen_coder.json` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/examples/module_manifest_content_forge.json` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/examples/module_manifest_openclaw_cli.json` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/examples/observacionista_video.dsl` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/host-profiles/pc2_server_dock.yaml` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/live-build/auto/config` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/live-build/config/hooks/live/001-enable-claudio-services.hook.chroot` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/live-build/config/includes.chroot/etc/claudio/policy.yaml` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/live-build/config/includes.chroot/etc/claudio/provider_registry.yaml` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/live-build/config/includes.chroot/etc/systemd/system/claudio-dashboard.service` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/live-build/config/includes.chroot/etc/systemd/system/claudio-guardian.service` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/live-build/config/includes.chroot/opt/claudio/dashboard/dashboard.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/live-build/config/includes.chroot/opt/claudio/guardian/guardian.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/live-build/config/includes.chroot/usr/local/bin/claudioctl` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/live-build/config/package-lists/claudio.list.chroot` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/policies/default_policy.yaml` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/scripts/00_install_build_deps.sh` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/scripts/01_build_iso.sh` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/scripts/02_test_iso_qemu.sh` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/scripts/windows_backup_to_sd.ps1` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/claudio_os_blueprint/scripts/windows_harden_loopback.ps1` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/README.md` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/assets/public_placeholders/medioevo_placeholder_1.ppm` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/assets/public_placeholders/medioevo_placeholder_2.ppm` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/assets/public_placeholders/medioevo_placeholder_3.ppm` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/__init__.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/app/__init__.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/app/main.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/catalog/__init__.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/catalog/assets_catalog.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/cli.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/core/__init__.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/core/engine.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/core/job_store.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/core/metrics.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/core/models.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/core/observacionismo_state.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/history/__init__.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/history/trends.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/media/__init__.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/media/assets.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/media/captions.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/media/ffmpeg.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/media/transcribe.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/media/visual_qa.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/publish/__init__.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/content_forge/content_forge/publish/queue.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/model_slimmer_evidence.py` |
| `A ` | `REVIEW` | `products_staging` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `PRODUCTOS_MEDIOEVO/observacionismo_dsl.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/README.md` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/commercial/argus-desktop/README.md` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/.gitignore` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/README.md` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/REPORT_WABI_SABI_LOCAL_AGENTS.md` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/docs/ARCHITECTURE.md` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/docs/USAGE.md` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/pyproject.toml` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/tests/test_agents.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/tests/test_cli.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/tests/test_memory.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/tests/test_router.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi.cmd` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi.ps1` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/__init__.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/agents/__init__.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/agents/base_agent.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/agents/debug_agent.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/agents/file_agent.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/agents/programmer_agent.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/agents/research_agent.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/cli/__init__.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/cli/main.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/cli/parser.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/cli/router.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/config/agents.json` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/core/__init__.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/core/config.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/core/gate.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/core/memory.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/core/observation.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/local/wabi-sabi/wabi_sabi/core/tools.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/residueos/.gitignore` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/residueos/README.md` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/residueos/examples/sample_action.json` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/residueos/pyproject.toml` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/residueos/residueos/__init__.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/residueos/residueos/cli.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/residueos/residueos/gate.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/residueos/residueos/metrics.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/residueos/residueos/server.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/residueos/residueos/store.py` |
| `A ` | `REVIEW` | `apps` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `apps/residueos/tests/test_residueos.py` |
| `A ` | `REVIEW` | `books` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `books/README.md` |
| `A ` | `REVIEW` | `books` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `books/editorial/LICENSE` |
| `A ` | `REVIEW` | `books` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `books/editorial/observacionismo-gemma-method.md` |
| `A ` | `REVIEW` | `unknown_review` | `ROUTE_TO_CANON_OR_ARCHIVE` | `data/observacionismo/concepts_seed.jsonl` |
| `M ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/INDEX.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/ai_browser/00_inventory.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/ai_browser/01_problem_definition.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/ai_browser/02_threat_model.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/ai_browser/03_architecture.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/ai_browser/04_security_requirements.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/ai_browser/05_stack_options.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/ai_browser/06_mvp_scope.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/ai_browser/07_user_flows.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/ai_browser/08_agent_protocols.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/ai_browser/09_build_roadmap.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/ai_browser/10_prompt_injection_policy.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/ai_browser/11_evidence_bundle_schema.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/ai_browser/12_risk_resolution_log.md` |
| `M ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/ONE_UNIVERSE_CONTROL_2026-05-06.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/intake/ONE_UNIVERSE_VAULTS_LEDGER_2026-05-06.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/observacionismo/COMMS_L1_ACTIONGATE_BRIDGE_V0_1.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/observacionismo/HANDOFF_OBS_CANON_BRIDGE_V01_2026-05-06.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/observacionismo/HANDOFF_OBS_CANON_SCHEMA_V01_2026-05-06.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/observacionismo/OPERATIONAL_CANON_V0_1.md` |
| `M ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/README.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/content-forge.md` |
| `A ` | `REVIEW` | `docs` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `docs/product/product-staging-ledger-2026-05-06.md` |
| `A ` | `BLOCK` | `private_game` | `KEEP_PRIVATE_BOUNDARY_NOT_PUBLIC_CANON` | `game-private/DO_NOT_PUBLISH.md` |
| `A ` | `BLOCK` | `private_game` | `KEEP_PRIVATE_BOUNDARY_NOT_PUBLIC_CANON` | `game-private/README.md` |
| `A ` | `BLOCK` | `private_game` | `KEEP_PRIVATE_BOUNDARY_NOT_PUBLIC_CANON` | `game-private/README_PRIVATE.md` |
| `A ` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/google-rapid-agent-2026/.github/FUNDING.yml` |
| `A ` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/google-rapid-agent-2026/.gitignore` |
| `A ` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/google-rapid-agent-2026/LICENSE` |
| `A ` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/google-rapid-agent-2026/README.md` |
| `A ` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/google-rapid-agent-2026/docs/HACKATHON_PLAN.md` |
| `A ` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/google-rapid-agent-2026/docs/SUBMISSION_DRAFT.md` |
| `A ` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/google-rapid-agent-2026/examples/release_goal.json` |
| `A ` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/google-rapid-agent-2026/pyproject.toml` |
| `A ` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/google-rapid-agent-2026/rapid_agent_guardian/__init__.py` |
| `A ` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/google-rapid-agent-2026/rapid_agent_guardian/agent.py` |
| `A ` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/google-rapid-agent-2026/rapid_agent_guardian/cli.py` |
| `A ` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/google-rapid-agent-2026/rapid_agent_guardian/mcp_client.py` |
| `A ` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/google-rapid-agent-2026/rapid_agent_guardian/models.py` |
| `A ` | `REVIEW` | `hackathons` | `KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW` | `hackathons/google-rapid-agent-2026/rapid_agent_guardian/readiness.py` |

## Reglas

- One universe does not mean flattening every folder into one directory.
- A route is canon only when it has lane, purpose, gate, evidence and owner.
- Untracked agent output is production residue until integrated into a lane.
- Generated caches can be deleted by rule; unique sources move only with ficha and migration map.
- Private, secret-like and external-action surfaces never become public canon by accident.
