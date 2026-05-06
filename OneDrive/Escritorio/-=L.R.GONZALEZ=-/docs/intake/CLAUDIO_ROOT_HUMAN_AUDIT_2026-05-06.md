# Claudio Root Human Audit - 2026-05-06

Generated UTC: `2026-05-06T10:06:23.004593+00:00`
Target: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio`

## Summary

- Root items: `554`
- Root files: `402`
- Root directories: `152`
- Git pending lines: `1223`

## Category Counts

| category | count |
|---|---:|
| `archive_existing` | 6 |
| `cache_regenerable` | 11 |
| `domain_module_or_legacy_dir` | 109 |
| `git_control` | 1 |
| `launcher_script` | 101 |
| `local_config_tooling` | 7 |
| `local_state_db` | 10 |
| `misc_root_item` | 8 |
| `private_blocked` | 7 |
| `root_data_config` | 48 |
| `root_document` | 6 |
| `root_media_or_ui` | 10 |
| `root_python_script` | 205 |
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
| ` Claudio_Startup.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
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
| `__init__.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `__pycache__` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `_ARCHIVAR` | `directory` | `archive_existing` | `KEEP_REVIEW_CONSOLIDATE` | `runtime/archivo_frio` | `existing_archive` |
| `_archivo_sesiones` | `directory` | `archive_existing` | `KEEP_REVIEW_CONSOLIDATE` | `runtime/archivo_frio` | `existing_archive` |
| `_legacy` | `directory` | `archive_existing` | `KEEP_REVIEW_CONSOLIDATE` | `runtime/archivo_frio` | `existing_archive` |
| `_local_quarantine` | `directory` | `archive_existing` | `KEEP_REVIEW_CONSOLIDATE` | `runtime/archivo_frio` | `existing_archive` |
| `_temp_oppo_persistent_setup.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `_ui_uploads` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `_workspace` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `activar_autopilot.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `activar_tienda.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `adb_wrapper.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `add_cloudflare_dns.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `ads` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `agent` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `agent_runner.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `agentes` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `agentes_conectores.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `ALCATEL_AUTO_SETUP.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `api` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `apps` | `directory` | `runtime_core_root` | `KEEP` | `apps` | `strong_runtime_route` |
| `archive` | `directory` | `archive_existing` | `KEEP_REVIEW_CONSOLIDATE` | `runtime/archivo_frio` | `existing_archive` |
| `archivo` | `directory` | `archive_existing` | `KEEP_REVIEW_CONSOLIDATE` | `runtime/archivo_frio` | `existing_archive` |
| `argus` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `argus_art.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `argus_dearpygui.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `argus_gui_launcher.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `argus_hub.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `argus_integrator.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `argus_main.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `argus_tamagotchi.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `argus_tui.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `arte` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `artifacts` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `assets` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `audio_distortion.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `auditor` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `auto_fix_claudio.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `auto_generated` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `AUTOMATE_SESSION.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `AUTOMATED_SESSION.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `autopilot` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `autorepair` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `autorun_oppo.ps1` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `backup.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `bardo` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `beneficiarios_config.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `beta` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `bio_feedback.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `bio_tamagotchi_bridge.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `bio_tamagotchi_estado.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `bitacora_ataques.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `bomberos` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `brain_os` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `brain_os.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `browser_agent.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `buddy_hud.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `bugs` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `build_6plus1_publication_package.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `build_lore_db.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `cache` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `camera_frames` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `catalog` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `ceo_exec.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `chat_endpoint.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `check_sendgrid_dns.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `checklists` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `city_overlay` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `CLAUDE.md.backup` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `claudio` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `claudio.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `Claudio_Accesos_Directos` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `claudio_api_server.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `claudio_audio.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `claudio_avatar_web.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `claudio_camera_vision.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `CLAUDIO_CHAT.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `claudio_cli.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `Claudio_Cobain.ico` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `claudio_daemon.db` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `claudio_daemon.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `claudio_daemon_247.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `claudio_daemon_psi.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `claudio_face.png` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `claudio_harness.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `claudio_llm.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `claudio_memory.db` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `Claudio_MODO_RAPIDO.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `claudio_os` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `claudio_pipeline.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `claudio_secrets.json` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `claudio_state.db` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `claudio_tui.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `claudio_tui_legacy.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `claudio_tv_token.json` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `claudio_voice.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `cleanup_phase1.ps1` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `codex` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `comfyui_config.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `comfyui_setup.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `comfyui_workflows` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `commands` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `commercial` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `common_sense.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `conductor.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `config` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `config.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `config_autopilot.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `configs` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `configurar_autostart.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `CONFIGURAR_RED_POD.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `configurar_scheduler.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `consejo_cli.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `consejo_elrond.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `consejo_elrond_session.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `consolidar_35_a_6mas1.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `consolidar_env.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `contab` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `content` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `content_calendar.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `content_queue.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `context` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `continuous_research_watch.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `conway_buddy.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `conway_data` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `conway_economico.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `conway_miner_data.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `conway_observador.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `conway_online.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `conway_reporte_local.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `conway_start.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `conway_tamagotchi.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `core` | `directory` | `runtime_core_root` | `KEEP` | `core` | `strong_runtime_route` |
| `coremetrics.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `coreollama_psi_runtime.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `cost` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `crear_accesos.ps1` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `crear_accesos_directos.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `crear_productos_shopify.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `create_demo_clip.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `create_kocca_deck.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `creator_outreach_templates.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `crm.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `crm.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `Ctempsensor_server.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `d2d_book_metadata.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `d2d_upload.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `d2d_upload_v2.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `daemon` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `daily_content_generator.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `daily_heygen.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `daily_suno.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `daily_youtube.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `dashboard_argus.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `dashboard_argus_unificado.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `DASHBOARD_ARGUS_UNIFIED.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `data` | `directory` | `runtime_core_root` | `KEEP` | `data` | `strong_runtime_route` |
| `datasets` | `directory` | `runtime_core_root` | `KEEP` | `datasets` | `strong_runtime_route` |
| `deepseek_chat.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `deploy_oppo_new_env.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `deploy_sensor_oppo.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `descargar_chimera_fijo.ps1` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `device_protection_state.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `devices` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `DIAGNOSTICO_COMPLETO.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `diana_profile_builder.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `diana_voice_patch.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `docs` | `directory` | `runtime_core_root` | `KEEP` | `docs` | `strong_runtime_route` |
| `download_unc0ver_fix.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `dream_system.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `dual_brain.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `ECOSISTEMA_MASTER_DEPLOY.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `ECOSISTEMA_MASTER_SETUP.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `ecosystem_commands.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `ecosystem_devices.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `ecosystem_launcher.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `ecosystem_orchestrator.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `editorial` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `EJECUTAR_ALCATEL_AUTO.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `EJECUTAR_COMO_ADMIN.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `EJECUTAR_IPHONE_AUTO.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `EJECUTAR_MASTER_SETUP.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `EJECUTAR_OPPO_AUTO.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `EJECUTAR_TODO_P0.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `ejemplo_tools.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `elevenreader_prep.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `email_signature.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `emotional_arc.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `enable_adb_wifi.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `entities.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `error_priority.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `etno` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `fcu_handoff.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `fcu_init.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `feedback` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `feedback.db` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `fewshot` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `fewshot.db` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `finanzas` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `fine_tuned_models` | `directory` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `private/fine_tuned_models` | `private_runtime_or_models` |
| `fingerprint_matcher.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `fix_adb.ps1` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `fix_all_corruption.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `fix_como_si.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `fix_ecosystem.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `fix_oppo_sensors.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `FIX_OPPO_TERMINAL.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `fix_screen_hub.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `fix_writer_module.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `gateway` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `generate_6plus1_volume_landings.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `generate_assets.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `generate_cartridge_images.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `generate_cartridges.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `generate_character_merch.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `generate_en_covers.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `generate_gumroad_covers.py` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `generate_kofi_covers.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `generate_missing_assets.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `generate_redbubble_designs.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `gguf_exports` | `directory` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `private/gguf_exports` | `private_runtime_or_models` |
| `git_insights.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `github-modules` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `grants` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `gumroad_api.json` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `gumroad_products.json` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `gumroad_verificar.py` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `HABILITAR_POD_REMOTO.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `handoffs` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `history` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `hook_gateway.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `hooks` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `humor_engine.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `i18n` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `INICIAR_API_SERVER.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `INICIAR_CLAUDIO.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `INICIAR_CON_WINDOWS.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `INICIAR_CON_WINDOWS_HIDDEN.vbs` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `iniciar_conway_economico.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `INICIAR_PUBLICACION_AUTOMATICA.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `INICIAR_SESION.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `INICIAR_SISTEMA_247.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `instagram_uploader.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `INSTALAR_APPLE_DRIVERS.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `instalar_sadtalker.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `INSTALAR_TODO.ps1` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `install_all_security_tools.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `install_n8n.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `install_research_pc2.ps1` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `installer` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `INTEGRATION_LOCKFILE_2026-04-29.md` | `file` | `root_document` | `MOVE_CANDIDATE` | `docs/root_notes_review` | `root_doc_noise` |
| `integrations` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `ios_companion` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `iphone_auto_post_jb.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `IPHONE_AUTO_SETUP.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `IPHONE_CONNECT_192.168.1.96.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `IPHONE_DIAGNOSTICO.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `iphone_post_jb_setup.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `IPHONE_VERIFICAR.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `jellyfin_auth.json` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `kairos_buddy_daemon.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `kairos_buddy_historial.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `kairos_daemon.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `kairos_historial.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `kalman_orientation.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `kickstarter` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `kofi_cdp_upload.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `lago.db` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `lago.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `lang` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `launch_argus.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `launch_argus_web.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `launch_claudio_auto.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `launch_coach.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `launch_crm.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `launch_hormiguero_hub.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `launch_hub_7474.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `launch_medioevo_console.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `launch_radiocinema.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `launch_startup_sequence.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `LAUNCH_THESIS.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `launch_voice_direct.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `launch_writer.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `legal` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `legal_boundaries.sqlite` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `libros.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `limpiar_espacio.ps1` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `limpieza` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `llm` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `logi` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `logs` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `lore_db.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `lore_drops` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `lore_knowledge_base.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `magisk_opo_patch.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `marble_connector.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
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
| `mempalace_wrapper.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `mini_office` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `mkt` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `model_switcher.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `Modelfile.claudio` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `Modelfile.gemma4_observador` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `Modelfile.gemma4_observador_balanced` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `Modelfile.gemma4_observador_lite` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `modes` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `molbook_connector.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `MONITOR_OPPO.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `MOTOR_GATE_FINAL.md` | `file` | `root_document` | `MOVE_CANDIDATE` | `docs/root_notes_review` | `root_doc_noise` |
| `mover_a_E.ps1` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `mover_modelos_e.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `narrative_engine.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `nemo_literary_analysis.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `nemo_reports` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `nemo_research_loop.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `NEXT_SESSION_BRIEF.md` | `file` | `root_document` | `MOVE_CANDIDATE` | `docs/root_notes_review` | `root_doc_noise` |
| `observacionismo` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `obsidian_integration.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `ollama_optimized_config.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `onion` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `oppo_clean.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `oppo_deploy` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `OPPO_DEPLOY_FIX.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `oppo_fix_permissions.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `oppo_install_python.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `oppo_new_env.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `oppo_one_tap.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `oppo_robot` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `oppo_root_check.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `oppo_root_mtk.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `oppo_sensor_patch.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `oppo_sensor_server.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `oppo_setup.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `oppo_setup_termux.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `oppo_tv_cast.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `optimize_profiles.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `oraculo` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `os` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `output` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `panel_server.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `patch_defensa.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `patch_ethical_core.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `patch_sqlite.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `patterns` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `pc2_research_daemon.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `PENDIENTES_MASTER.md` | `file` | `root_document` | `MOVE_CANDIDATE` | `docs/root_notes_review` | `root_doc_noise` |
| `permission_rules.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `persistence_manager.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `philosophy` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `philosophy_middleware.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `phone_rescue.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `pika_connector.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `piper_tts.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `pixel_promo_build` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `platform_setup_status.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `pod_catalog.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `pod_config.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `pod_designs.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `Pod_RDP.rdp` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `pod_server_setup.ps1` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `post_next.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `post_to_reddit.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `postas` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `postmortem_protocol.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `POWERFUL_START.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `prepare_voice.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `producto_final_codex` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `products` | `directory` | `runtime_core_root` | `KEEP` | `products` | `strong_runtime_route` |
| `promo_build` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `PROYECTO_REAL_35_A_6_MAS_1_MANIFEST.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `psi_ethical_core.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `psi_monitor.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `psi_monitor_local.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `psi_observador.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `psi_standalone_server.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `psi_state.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `psi_willow_circuit.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `psi_willow_results.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `publish_despertar_final.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `publish_gumroad_6plus1.py` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `publish_staging` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `push_images.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `pytest.ini` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `qa_artifacts` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `quantum_buffer.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `radiocinema` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `radiocinema_bridges.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `raspberry_console` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `rate_limits.sqlite` | `file` | `local_state_db` | `KEEP_REVIEW_RETENTION` | `runtime/state` | `local_state_database` |
| `redbubble_batch_1.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `reddit_posts.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `remote_oppo_deploy.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `repair_corruption.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `REPARAR_ECOSISTEMA.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `reports` | `directory` | `runtime_core_root` | `KEEP` | `reports` | `strong_runtime_route` |
| `research` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `research_alerts.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `research_data.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `research_implementation_queue.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `research_status.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `research_watch_reports` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `research_watch_state.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `resend_email.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `response` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `resultado_simulacion_ataques.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `rh_mariposa_v2.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `ritual` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `rnd` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `routing` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `RUFUS_DOWNLOAD_ALT.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `RUN_ALL_AUTOMATIONS.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `RUN_CANON10_EDITORIAL_PIPELINE.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `run_claudio_research_watch.cmd` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `run_conway.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `runtime` | `directory` | `runtime_core_root` | `KEEP` | `runtime` | `strong_runtime_route` |
| `SAMPLE_DIALOGUES.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `samsung_tv.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `screen_hub` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `screenshots` | `directory` | `cache_regenerable` | `CANDIDATE_DELETE_AFTER_GATE` | `runtime/cache_or_artifacts` | `cache_or_generated_runtime` |
| `scripts` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `sdk` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `security` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `security_hardening.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `security_panel.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `security_tools_installer.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `self_eval.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `self_heal` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `sensor_server.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `setup_adguardhome_pc2.ps1` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `setup_auto_publish.ps1` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `setup_cloudflare_dns.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `setup_gumroad.py` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `setup_jellyfin.ps1` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `setup_jellyfin_libraries.ps1` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `setup_payments.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `setup_pc2_env.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `setup_scheduler_simple.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `setup_termux.sh` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `shopify` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `shopify_buy_button.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `shopify_cdp_auto.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `shopify_connector.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `simulacro_diario.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `skills` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `skills_catalog.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `social_agent.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `social_automation.log` | `file` | `misc_root_item` | `REVIEW` | `docs/intake/claudio_root_review` | `fallback` |
| `social_automation.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `social_log.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `social_posts` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `social_posts_ready.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `soporte` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `sql` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `start_all_agents.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `start_api_clean.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `start_avatar.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `start_chrome_debug.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `start_claudio.bat - Shortcut.lnk` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `start_claudio_boot.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `start_daemon_247.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `start_daemon_psi.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `start_n8n.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `start_openmythos_adapter.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `start_social_agent.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `start_whatsapp.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `store_profiles.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `stripe_hsbc_bridge.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `sunday_featured_artist.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `symbiotic_field.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `system_cleaner.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `tamagotchi_estado.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `task_planner.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `tasks.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `tasks.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `tcg` | `directory` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `private/tcg` | `private_runtime_or_models` |
| `teatro` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `tech` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `templates` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `TERMUX_AUTO_BRIDGE.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `test_3t_integration.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `test_ethical_core.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `test_whatsapp.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `tests` | `directory` | `runtime_core_root` | `KEEP` | `tests` | `strong_runtime_route` |
| `tiktok_uploader.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `tool_registry.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `tools` | `directory` | `runtime_core_root` | `KEEP` | `tools` | `strong_runtime_route` |
| `trafficker_report.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `training_datasets` | `directory` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `private/training_datasets` | `private_runtime_or_models` |
| `tshirt_designs.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `turboquant_monitor.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `tv_audio` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `tv_player.html` | `file` | `root_media_or_ui` | `MOVE_CANDIDATE` | `assets/root_media_review` | `root_asset_noise` |
| `umami_monitor.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `update_gumroad_listings.py` | `file` | `secret_or_sensitive` | `BLOCK_MOVE_TO_PRIVATE_CONFIG` | `runtime/private_config` | `secret_marker` |
| `upload_redbubble.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `user_profile.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `vault_medioevo` | `directory` | `private_blocked` | `KEEP_PRIVATE_REVIEW` | `private/vault_medioevo` | `private_runtime_or_models` |
| `verificar_stripe.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `verify_autopilot.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `verify_ecosystem.bat` | `file` | `launcher_script` | `MOVE_CANDIDATE` | `tools/launchers` | `root_launcher_noise` |
| `verify_memory.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `video` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `video_pipeline.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `video_schedule.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `video_scheduler.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `voice_clone.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `voice_recordings` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `voices` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `vpn_toggle.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `web` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `web4_conway_miner.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `website` | `directory` | `runtime_core_root` | `KEEP` | `website` | `strong_runtime_route` |
| `whatsapp_agent.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `whatsapp_downloader.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `whatsapp_templates.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `whisper_stt.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `WORKFLOW.symphony.md` | `file` | `root_document` | `MOVE_CANDIDATE` | `docs/root_notes_review` | `root_doc_noise` |
| `workflows` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `world_engine.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `writer_data` | `directory` | `domain_module_or_legacy_dir` | `REVIEW_DESTINATION` | `docs/intake/claudio_root_review` | `noncanonical_root_dir` |
| `writer_module.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `writer_psi_adapter.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
| `youtube_descriptions.json` | `file` | `root_data_config` | `MOVE_CANDIDATE_REVIEW` | `data/root_config_review` | `root_data_noise` |
| `youtube_uploader.py` | `file` | `root_python_script` | `MOVE_CANDIDATE` | `tools/root_scripts_review` | `root_python_noise` |
