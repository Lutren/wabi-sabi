# Claudio Root Human Audit - 2026-05-06

Generated UTC: `2026-05-06T10:21:34.763002+00:00`
Target: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio`

## Summary

- Root items: `250`
- Root files: `98`
- Root directories: `152`
- Git pending lines: `922`

## Category Counts

| category | count |
|---|---:|
| `archive_existing` | 6 |
| `cache_regenerable` | 11 |
| `domain_module_or_legacy_dir` | 109 |
| `git_control` | 1 |
| `local_config_tooling` | 7 |
| `local_state_db` | 10 |
| `misc_root_item` | 8 |
| `private_blocked` | 7 |
| `root_data_config` | 48 |
| `root_document` | 6 |
| `root_media_or_ui` | 10 |
| `root_python_script` | 2 |
| `runtime_core_root` | 11 |
| `secret_or_sensitive` | 14 |

## Human Diagnosis

- The root is not human-clean: runtime, docs, launchers, local secrets, device scripts, product scripts and legacy files share one visible level.
- This audit did not move or delete files.
- Immediate safe work is documentation and staged manifests, not broad cleanup.
- Physical moves should be batched by category with rollback manifests.

## High-Risk Visible Items

| name | category | decision | risk | destination hint |
|---|---|---|---|---|
| `-=PSI=-` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `HIGH` | `private/-=PSI=-` |
| `.env` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `HIGH` | `runtime/private_config` |
| `.env.example` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `HIGH` | `runtime/private_config` |
| `.env.gumroad` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `HIGH` | `runtime/private_config` |
| `.env.mova.example` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `HIGH` | `runtime/private_config` |
| `.git` | `git_control` | `KEEP` | `HIGH` | `.git` |
| `claudio_daemon.db` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `HIGH` | `runtime/state` |
| `claudio_memory.db` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `HIGH` | `runtime/state` |
| `claudio_secrets.json` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `HIGH` | `runtime/private_config` |
| `claudio_state.db` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `HIGH` | `runtime/state` |
| `claudio_tv_token.json` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `HIGH` | `runtime/private_config` |
| `feedback.db` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `HIGH` | `runtime/state` |
| `fewshot.db` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `HIGH` | `runtime/state` |
| `fine_tuned_models` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `HIGH` | `private/fine_tuned_models` |
| `generate_gumroad_covers.py` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `HIGH` | `runtime/private_config` |
| `gguf_exports` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `HIGH` | `private/gguf_exports` |
| `gumroad_api.json` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `HIGH` | `runtime/private_config` |
| `gumroad_products.json` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `HIGH` | `runtime/private_config` |
| `gumroad_verificar.py` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `HIGH` | `runtime/private_config` |
| `jellyfin_auth.json` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `HIGH` | `runtime/private_config` |
| `lago.db` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `HIGH` | `runtime/state` |
| `legal_boundaries.sqlite` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `HIGH` | `runtime/state` |
| `medioevo_lore.db` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `HIGH` | `runtime/state` |
| `memory_index.db` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `HIGH` | `runtime/state` |
| `memory_vault` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `HIGH` | `private/memory_vault` |
| `publish_gumroad_6plus1.py` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `HIGH` | `runtime/private_config` |
| `rate_limits.sqlite` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `HIGH` | `runtime/state` |
| `setup_gumroad.py` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `HIGH` | `runtime/private_config` |
| `tcg` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `HIGH` | `private/tcg` |
| `training_datasets` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `HIGH` | `private/training_datasets` |
| `update_gumroad_listings.py` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `HIGH` | `runtime/private_config` |
| `vault_medioevo` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `HIGH` | `private/vault_medioevo` |

## Root Items

| name | kind | category | decision | destination hint | reason |
|---|---|---|---|---|---|
| `-=PSI=-` | `directory` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `private/-=PSI=-` | `private_runtime_or_models` |
| `.agents` | `directory` | `local_config_tooling` | `KEEP_REVIEW` | `.agents` | `local_tool_config` |
| `.aider.chat.history.md` | `file` | `root_document` | `MOVE_CANDIDATE` | `docs/root_notes_review` | `root_doc_noise` |
| `.claude` | `directory` | `local_config_tooling` | `KEEP_REVIEW` | `.claude` | `local_tool_config` |
| `.claudio` | `directory` | `local_config_tooling` | `KEEP_REVIEW` | `.claudio` | `local_tool_config` |
| `.claw` | `directory` | `local_config_tooling` | `KEEP_REVIEW` | `.claw` | `local_tool_config` |
| `.env` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `.env.example` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `.env.gumroad` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `.env.mova.example` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `.git` | `directory` | `git_control` | `KEEP` | `.git` | `repo_control` |
| `.gitignore` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `.pytest_cache` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `.skills` | `directory` | `local_config_tooling` | `KEEP_REVIEW` | `.skills` | `local_tool_config` |
| `.test_research` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `.test_research_storage` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `.test_session_storage` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `.test_sessions` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `.venv_api` | `directory` | `local_config_tooling` | `KEEP_REVIEW` | `.venv_api` | `local_tool_config` |
| `.wrangler` | `directory` | `local_config_tooling` | `KEEP_REVIEW` | `.wrangler` | `local_tool_config` |
| `__pycache__` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `_ARCHIVAR` | `directory` | `archive_existing` | `KEEP_REVIEW_CONSOLIDATE` | `runtime/archivo_frio` | `existing_archive` |
| `_archivo_sesiones` | `directory` | `archive_existing` | `KEEP_REVIEW_CONSOLIDATE` | `runtime/archivo_frio` | `existing_archive` |
| `_legacy` | `directory` | `archive_existing` | `KEEP_REVIEW_CONSOLIDATE` | `runtime/archivo_frio` | `existing_archive` |
| `_local_quarantine` | `directory` | `archive_existing` | `KEEP_REVIEW_CONSOLIDATE` | `runtime/archivo_frio` | `existing_archive` |
| `_ui_uploads` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `_workspace` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `ads` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `agent` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `agentes` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `api` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `apps` | `directory` | `runtime_core_root` | `KEEP` | `apps` | `strong_runtime_route` |
| `archive` | `directory` | `archive_existing` | `KEEP_REVIEW_CONSOLIDATE` | `runtime/archivo_frio` | `existing_archive` |
| `archivo` | `directory` | `archive_existing` | `KEEP_REVIEW_CONSOLIDATE` | `runtime/archivo_frio` | `existing_archive` |
| `argus` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `arte` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `artifacts` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `assets` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `auditor` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `auto_generated` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `autopilot` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `autorepair` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `bardo` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `beneficiarios_config.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `beta` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `bio_tamagotchi_estado.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `bitacora_ataques.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `bomberos` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `brain_os` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `bugs` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `cache` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `camera_frames` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `catalog` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `checklists` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `city_overlay` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `CLAUDE.md.backup` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `claudio` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `Claudio_Accesos_Directos` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `claudio_avatar_web.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `Claudio_Cobain.ico` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `claudio_daemon.db` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `claudio_daemon_247.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `claudio_face.png` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `claudio_memory.db` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `claudio_os` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `claudio_secrets.json` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `claudio_state.db` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `claudio_tui.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `claudio_tv_token.json` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `codex` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `comfyui_config.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `comfyui_workflows` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `commands` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `commercial` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `config` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `config.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `configs` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `consejo_elrond_session.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `contab` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `content` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `content_queue.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `context` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `conway_data` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `conway_miner_data.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `core` | `directory` | `runtime_core_root` | `KEEP` | `core` | `strong_runtime_route` |
| `cost` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `creator_outreach_templates.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `crm.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `d2d_book_metadata.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `daemon` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `dashboard_argus.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `DASHBOARD_ARGUS_UNIFIED.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `data` | `directory` | `runtime_core_root` | `KEEP` | `data` | `strong_runtime_route` |
| `datasets` | `directory` | `runtime_core_root` | `KEEP` | `datasets` | `strong_runtime_route` |
| `device_protection_state.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `devices` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `docs` | `directory` | `runtime_core_root` | `KEEP` | `docs` | `strong_runtime_route` |
| `ecosystem_devices.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `editorial` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `email_signature.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `entities.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `etno` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `feedback` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `feedback.db` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `fewshot` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `fewshot.db` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `finanzas` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `fine_tuned_models` | `directory` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `private/fine_tuned_models` | `private_runtime_or_models` |
| `gateway` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `generate_gumroad_covers.py` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `gguf_exports` | `directory` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `private/gguf_exports` | `private_runtime_or_models` |
| `github-modules` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `grants` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `gumroad_api.json` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `gumroad_products.json` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `gumroad_verificar.py` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `handoffs` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `history` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `hooks` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `i18n` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `installer` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `INTEGRATION_LOCKFILE_2026-04-29.md` | `file` | `root_document` | `MOVE_CANDIDATE` | `docs/root_notes_review` | `root_doc_noise` |
| `integrations` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `ios_companion` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `jellyfin_auth.json` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `kairos_buddy_historial.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `kairos_historial.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `kickstarter` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `lago.db` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `lang` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `legal` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `legal_boundaries.sqlite` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `libros.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `limpieza` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `llm` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `logi` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `logs` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `lore_drops` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `lore_knowledge_base.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `marketing` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `matriz_feedback_lectores.csv` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `media_portal.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `media_routes.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `medioevo_agent_hub` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `medioevo_lore.db` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `memory_index.db` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `memory_vault` | `directory` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `private/memory_vault` | `private_runtime_or_models` |
| `mempalace.yaml` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `mempalace_seed_convos_20260409` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `mini_office` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `mkt` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `Modelfile.claudio` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `Modelfile.gemma4_observador` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `Modelfile.gemma4_observador_balanced` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `Modelfile.gemma4_observador_lite` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `modes` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `MOTOR_GATE_FINAL.md` | `file` | `root_document` | `MOVE_CANDIDATE` | `docs/root_notes_review` | `root_doc_noise` |
| `nemo_reports` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `NEXT_SESSION_BRIEF.md` | `file` | `root_document` | `MOVE_CANDIDATE` | `docs/root_notes_review` | `root_doc_noise` |
| `observacionismo` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `onion` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `oppo_deploy` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `oppo_robot` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `oppo_tv_cast.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `oraculo` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `os` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `output` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `patterns` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `PENDIENTES_MASTER.md` | `file` | `root_document` | `MOVE_CANDIDATE` | `docs/root_notes_review` | `root_doc_noise` |
| `permission_rules.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `philosophy` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `pixel_promo_build` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `platform_setup_status.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `pod_catalog.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `pod_config.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `postas` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `producto_final_codex` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `products` | `directory` | `runtime_core_root` | `KEEP` | `products` | `strong_runtime_route` |
| `promo_build` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `PROYECTO_REAL_35_A_6_MAS_1_MANIFEST.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `psi_state.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `psi_willow_results.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `publish_gumroad_6plus1.py` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `publish_staging` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `pytest.ini` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `qa_artifacts` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `radiocinema` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `raspberry_console` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `rate_limits.sqlite` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `redbubble_batch_1.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `reddit_posts.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `reports` | `directory` | `runtime_core_root` | `KEEP` | `reports` | `strong_runtime_route` |
| `research` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `research_alerts.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `research_data.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `research_implementation_queue.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `research_status.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `research_watch_reports` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `research_watch_state.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `response` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `resultado_simulacion_ataques.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `ritual` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `rnd` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `routing` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `runtime` | `directory` | `runtime_core_root` | `KEEP` | `runtime` | `strong_runtime_route` |
| `SAMPLE_DIALOGUES.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `screen_hub` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `screenshots` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `scripts` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `sdk` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `security` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `self_heal` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `setup_gumroad.py` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `shopify` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `shopify_buy_button.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `skills` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `skills_catalog.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `social_automation.log` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `social_log.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `social_posts` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `social_posts_ready.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `soporte` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `sql` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `store_profiles.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `tamagotchi_estado.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `tasks.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `tcg` | `directory` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `private/tcg` | `private_runtime_or_models` |
| `teatro` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `tech` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `templates` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `tests` | `directory` | `runtime_core_root` | `KEEP` | `tests` | `strong_runtime_route` |
| `tools` | `directory` | `runtime_core_root` | `KEEP` | `tools` | `strong_runtime_route` |
| `training_datasets` | `directory` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `private/training_datasets` | `private_runtime_or_models` |
| `tshirt_designs.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `tv_audio` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `tv_player.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `update_gumroad_listings.py` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `user_profile.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `vault_medioevo` | `directory` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `private/vault_medioevo` | `private_runtime_or_models` |
| `video` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `video_schedule.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `voice_recordings` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `voices` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `web` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `website` | `directory` | `runtime_core_root` | `KEEP` | `website` | `strong_runtime_route` |
| `whatsapp_templates.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `WORKFLOW.symphony.md` | `file` | `root_document` | `MOVE_CANDIDATE` | `docs/root_notes_review` | `root_doc_noise` |
| `workflows` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `writer_data` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `youtube_descriptions.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
