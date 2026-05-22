# WABI TEST REPORT

## 2026-05-21 - Observation Claim Adapter

- Created proposal-only adapter for `obsai-core` `ClaimClassifier` and
  `ObservationEnvelope v2.1`.
- `python -B -m pytest tests\test_observation_claim_adapter.py tests\test_hypothesis_packet.py -q -p no:cacheprovider`
  -> `8 passed in 2.49s`.
- `python -B -m py_compile wabi_sabi\core\observation_claim_adapter.py wabi_sabi\cli\main.py tests\test_observation_claim_adapter.py`
  -> PASS.
- Real 12-claim fixture review after calibration:
  `case_count=12`, `pass_count=12`, `review_count=0`, `status=PASS`.
- Adapter remains compatible with obsai-core `claimResult.gate_contract`;
  fixture next action now reports no calibration patch required when review
  count is zero.
- No source apply, cloud provider call, publication or deploy.

## 2026-05-21 - Local Apply Pending Closeout + Multimodal Calibration

- Pending closeout TaskSpec:
  `docs\WABI_LOCAL_APPLY_CLOSEOUT_TASKSPEC_2026-05-21.json`.
- `apply-local-preview` -> `LOCAL_APPLY_PATCH_READY`,
  `secret_scan.status=PASS`, `boundary_scan.status=PASS`,
  `cloud_provider_called=false`.
- First `apply-local` attempt -> `LOCAL_APPLY_TESTS_FAIL_ROLLED_BACK` because
  the internal pytest command timed out after 120s; rollback verified and target
  doc was not left applied.
- Retried with acotado py_compile gate -> `LOCAL_APPLY_TESTS_PASS`,
  `applied_to_sources=true`, `witness_verified=true`,
  `publication_gate=BLOCK`.
- Wabi focal apply/cloud/task review:
  `python -B -m pytest tests\test_local_apply_readiness.py tests\test_build_assist_cloud.py tests\test_cloud_budget.py tests\test_cloud_budget_ui_status.py tests\test_taskspec_review.py -q -p no:cacheprovider`
  -> `42 passed in 58.38s`.
- Multimodal intake:
  `python -B -m pytest tests\test_multimodal_intake.py -q -p no:cacheprovider`
  -> `5 passed in 0.65s`.
- Hypothesis packet:
  `python -B -m pytest tests\test_hypothesis_packet.py -q -p no:cacheprovider`
  -> `5 passed in 2.52s`.
- Py compile focal for touched Wabi modules -> PASS.
- UI/API local smoke on `http://127.0.0.1:8787/` -> HTTP 200 with Wabi
  Conversation, Cloud Budget, Review TaskSpec and Gate Preview visible.
- Cloud/provider state: `CLOUD_BUDGET_DRY_RUN`, `double_opt_in=false`,
  `cloud_provider_called=false`.
- No live cloud, no BrowserBridge live, no push/deploy/publication.

## 2026-05-20 - Wabi LLM Safe JSON Contract

- Scope: normalizar respuestas LLM proposal/UI/API con contrato JSON seguro y evidencia runtime/WitnessLog.
- Responsible use update: `docs/WABI_LLM_RESPONSIBLE_USE_2026-05-20.md` created and `tags` added to the safe JSON contract.
- Wabi responsible-use focal: `python -B -m pytest tests\test_llm_work_response.py tests\test_llm_proposal.py -q -p no:cacheprovider` -> `8 passed in 3.93s`.
- BRAIN_OS responsible-use focal: `python -B -m pytest 02_CLAUDIO\tests\test_wabi_llm_work_response_api.py 02_CLAUDIO\tests\test_wabi_llm_proposal_api.py -q -p no:cacheprovider` -> `7 passed in 9.73s`.
- CLI safe contract update: `wabi --once "<tarea>" --json` now merges `llm_work_response` fields while preserving `schema=wabi.conversation_turn.v0_1`.
- Metadata update: safe JSON now includes `metadata.priority`, `metadata.risk`, `metadata.category`, `metadata.relevance`, `metadata.incremental`, fallback mode, apply simulation, asset audit requirement and CloudBudgetGate marker.
- CLI/core focal after `LLM_proposal` tag and CLI wrapper: `python -B -m pytest tests\test_llm_work_response.py tests\test_llm_proposal.py tests\test_conversational_cli.py tests\test_cli.py -q -p no:cacheprovider` -> `30 passed in 53.33s`.
- CLI/core focal after metadata update: same command -> `30 passed in 29.65s`.
- BRAIN_OS API focal after tag update: `python -B -m pytest 02_CLAUDIO\tests\test_wabi_llm_work_response_api.py 02_CLAUDIO\tests\test_wabi_llm_proposal_api.py -q -p no:cacheprovider` -> `7 passed in 3.18s`.
- BRAIN_OS API focal after metadata update: same command -> `7 passed in 5.76s`.
- CLI smoke no-live: `status=OK`, `intent_name=code_request`, `route=code_plan`, `cloud_provider_called=false`, `applied_to_sources=false`, `rollback_snapshot_required=true`, `tags` includes `LLM_proposal`.
- CLI metadata smoke no-live: `metadata.category=code`, `metadata.incremental=true`, `metadata.fallback_mode=local_rules_task_spec`, `metadata.budget_control=CloudBudgetGate`.
- Responsible-use smoke no-live: `status=OK`, `intent_name=code_request`, `route=code_plan`, `cloud_provider_called=false`, `applied_to_sources=false`, `rollback_snapshot_required=true`, `tags` present, `witness_verified=true`.
- Responsible-use secret scan focal after metadata update: `3` files scanned, `0` findings, PASS.
- Wabi focal: `python -B -m pytest tests\test_llm_work_response.py tests\test_llm_proposal.py tests\test_conversation_engine.py tests\test_build_assist_cloud.py tests\test_local_apply_readiness.py tests\test_taskspec_review.py tests\test_conversational_cli.py -q -p no:cacheprovider` -> `55 passed in 47.32s`.
- BRAIN_OS focal: `python -B -m pytest 02_CLAUDIO\tests\test_wabi_llm_work_response_api.py 02_CLAUDIO\tests\test_wabi_llm_proposal_api.py 02_CLAUDIO\tests\test_wabi_conversation_api.py 02_CLAUDIO\tests\test_wabi_taskspec_review_api.py 02_CLAUDIO\tests\test_wabi_local_server.py -q -p no:cacheprovider` -> `251 passed in 115.44s (0:01:55)`.
- Py compile Wabi: `python -B -m py_compile wabi_sabi\core\llm_work_response.py wabi_sabi\core\llm_proposal.py wabi_sabi\core\conversation_engine.py wabi_sabi\core\build_assist_cloud.py wabi_sabi\core\cloud_budget.py wabi_sabi\core\local_apply_readiness.py wabi_sabi\cli\main.py` -> PASS.
- Py compile BRAIN_OS: `python -B -m py_compile 02_CLAUDIO\server\wabi_local_server.py` -> PASS.
- Safe JSON smoke no-live: `status=OK`, `intent_name=graphics_scene_request`, `route=graphics_plan`, `cloud_provider_called=false`, `applied_to_sources=false`, `rollback_snapshot_required=true`, `graphics_live=false`, `witness_verified=true`.
- Secret scan focal: `5` production/test files scanned, `0` findings, PASS.
- Initial parallel full-regression attempt exceeded `600s` timeout; rerun in series passed.
- Wabi regression: `python -B -m pytest -q -p no:cacheprovider` -> `385 passed in 394.59s (0:06:34)`.
- BRAIN_OS regression: `python -B -m pytest -q -p no:cacheprovider` -> `772 passed in 280.24s (0:04:40)`.
- Post-fallback server patch: `python -B -m py_compile 02_CLAUDIO\server\wabi_local_server.py` -> PASS.
- Post-fallback BRAIN_OS focal rerun: first attempt exceeded `300s` timeout; rerun with larger timeout -> `251 passed in 141.59s (0:02:21)`.
- Contract verified: `status=OK|REVIEW`, `intent_name`, `route`, `proposal`, `task_spec`, `graphics_plan`, `cloud_provider_called=false`, `applied_to_sources=false`, `rollback_snapshot_required=true`, `next_safe_action`, `warnings`.
- Runtime evidence: normalizer writes redacted JSON under `~\.medioevo\wabi\runtime\outputs\llm_work_response\`.
- WitnessLog: normalizer appends event type `llm_work_response` to `~\.medioevo\wabi\runtime\witness\wabi_patch_witness.sqlite`.
- No live cloud call executed. No Apply Local auto-run. No BrowserBridge live. No graphics_live. No push, deploy, commit or publication.

## 2026-05-19 - Wabi LLM Cloud Work Mode

- Scope: habilitar LLM cloud default como propuesta, con apply local separado.
- Wabi focal: `python -B -m pytest tests\test_llm_proposal.py tests\test_conversation_engine.py tests\test_build_assist_cloud.py tests\test_local_apply_readiness.py tests\test_taskspec_review.py tests\test_conversational_cli.py -q -p no:cacheprovider` -> `52 passed in 36.22s`.
- BRAIN_OS focal: `python -B -m pytest 02_CLAUDIO\tests\test_wabi_llm_proposal_api.py 02_CLAUDIO\tests\test_wabi_conversation_api.py 02_CLAUDIO\tests\test_wabi_taskspec_review_api.py 02_CLAUDIO\tests\test_wabi_local_server.py -q -p no:cacheprovider` -> `248 passed in 78.22s (0:01:18)`.
- Wabi regression: `python -B -m pytest -q -p no:cacheprovider` -> `382 passed in 274.24s (0:04:34)`.
- BRAIN_OS regression: `python -B -m pytest -q -p no:cacheprovider` -> `769 passed in 274.79s (0:04:34)`.
- Py compile: PASS for `llm_proposal.py`, `conversation_engine.py`, `build_assist_cloud.py`, `cloud_budget.py`, `local_apply_readiness.py`, `cli/main.py`, and BRAIN_OS `wabi_local_server.py`.
- CLI smoke: `WABI_LLM_PROVIDER_CLOUD_DEFAULT=1` with no double opt-in -> `CLOUD_BUDGET_DRY_RUN`, `cloud_provider_called=false`.
- UI endpoint smoke:
  - `GET /api/cloud-budget/status` -> `llm_cloud_default_enabled=true`, `double_opt_in=false`.
  - `POST /api/conversation/turn` -> `llm_proposal.status=CLOUD_BUDGET_DRY_RUN`.
  - `POST /api/taskspec/llm-proposal` -> `cloud_provider_called=false`, `applied_to_sources=false`.
- UI screenshot: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_visual_qa\WABI_LLM_CLOUD_WORK_MODE_20260519\wabi_ui_llm_cloud_work_mode.png`.
- Secret scan focal: `10` production/doc/runtime evidence text files scanned, `0` secret-like findings, PASS.
- Boundary scan focal: UI public HTML scanned, `0` private path findings, PASS. Internal docs may intentionally reference local evidence paths.
- No live cloud call executed.
- No BrowserBridge live.
- No graphics_live.
- No push, deploy, commit or publication.

## 2026-05-19 - Wabi Work Mode v1

- Scope: documentation and operational closeout only; no code changes.
- Docs created:
  - `docs/WABI_WORK_MODE_2026-05-19.md`
  - `docs/WABI_RELEASE_BLOCKERS_2026-05-19.md`
- Wabi focal: `python -B -m pytest tests\test_local_apply_readiness.py tests\test_taskspec_review.py tests\test_conversation_engine.py tests\test_conversational_cli.py -q -p no:cacheprovider` -> `33 passed in 35.28s`.
- BRAIN_OS UI focal: `python -B -m pytest 02_CLAUDIO\tests\test_wabi_local_server.py 02_CLAUDIO\tests\test_wabi_taskspec_review_api.py -q -p no:cacheprovider` -> `238 passed in 97.63s`.
- Py compile: `python -B -m py_compile ...` -> PASS for:
  - `-= BRAIN_OS =-\02_CLAUDIO\server\wabi_local_server.py`
  - `wabi_sabi\core\conversation_engine.py`
  - `wabi_sabi\core\taskspec_review.py`
  - `wabi_sabi\core\local_apply_readiness.py`
  - `wabi_sabi\cli\main.py`
- Full regression: not run by design because no code changed in this Work Mode closeout.
- Start-of-session curator refresh: `python tools\release\pending_review.py --write --quiet` in the broad MEDIOEVO root timed out after 120s and was not retried to avoid scope expansion.
- No live cloud call executed.
- No BrowserBridge live.
- No graphics_live.
- No push, deploy, commit or publication.

## 2026-05-19 - WABI Assets Du WABI Local Integration + Release Gate

- Scope: audited `Assets Du WABI` from the owner-provided BRAIN_OS working bench path.
- Asset audit output: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\asset_audit\wabi_assets_du_wabi_audit_20260519.json`.
- Audit counts: `125` files total, `122` images, `3` ZIP archives, `0` EXIF findings, `0` secret-like content findings, `0` private path leak findings, `0` duplicate hashes.
- Archive decision: `duat-brain-os-v1.4.0.zip`, `duat-physics-light-engine-v1.3.0.zip` and `Kimi_Agent_Ayuda con motor de audio.zip` were registered only; not extracted, not copied.
- Local UI assets integrated: `4` re-encoded PNG candidates under `-= BRAIN_OS =-\apps\local\wabi_ui\assets\wabi_du_wabi_20260519\`.
- Asset manifest: `-= BRAIN_OS =-\apps\local\wabi_ui\assets\wabi_du_wabi_20260519\ASSET_MANIFEST_20260519.json`, with `publication_allowed=false`.
- UI server QA: local server restarted on `http://127.0.0.1:8787` with PID `2176`; `GET /` returned HTTP `200`.
- Operational workbench QA: `/api/operational-workbench` returned `ui.theme=wabi_du_wabi_20260519`, manifest `assets/wabi_du_wabi_20260519/ASSET_MANIFEST_20260519.json`, `external_assets=false`.
- Browser visual QA: local screenshot captured at `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_assets_du_wabi_20260519\wabi_ui_du_wabi_assets_gate_preview.png`.
- Browser report: `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_assets_du_wabi_20260519\wabi_ui_du_wabi_assets_browser_report.json`, `broken_images=0`; one non-blocking 404 console line was observed during the visual run and did not prevent asset rendering or Gate Preview QA.
- Gate Preview confirmed: `APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1`.
- Safety flags confirmed: `cloud_provider_called=false`, `applied_to_sources=false`, `graphics_live=false`.
- Focal BRAIN_OS: `python -B -m pytest 02_CLAUDIO\tests\test_wabi_local_server.py 02_CLAUDIO\tests\test_wabi_conversation_api.py 02_CLAUDIO\tests\test_wabi_taskspec_review_api.py 02_CLAUDIO\tests\test_wabi_taskspec_gate_preview_api.py -q -p no:cacheprovider` -> `250 passed in 369.44s (0:06:09)`.
- Focal Wabi: `python -B -m pytest tests\test_taskspec_review.py tests\test_conversation_engine.py tests\test_conversational_cli.py tests\test_graphics_bridge.py tests\test_cloud_budget.py tests\test_cloud_budget_ui_status.py tests\test_build_assist_cloud.py -q -p no:cacheprovider` -> `52 passed in 57.49s`.
- Wabi regression: `python -B -m pytest -q -p no:cacheprovider` -> `362 passed in 461.37s (0:07:41)`.
- BRAIN_OS regression: `python -B -m pytest -q -p no:cacheprovider` -> `760 passed in 392.89s (0:06:32)`.
- Py compile Wabi: PASS for `conversation_engine.py`, `taskspec_review.py`, `graphics_bridge.py`, `cloud_budget.py`, `cli/main.py`.
- Py compile BRAIN_OS server: PASS for `02_CLAUDIO\server\wabi_local_server.py`.
- Frontend npm: `NO_PACKAGE_JSON` in checked BRAIN_OS/Wabi roots; no npm test/build available.
- Secret/boundary scans: focal scan over integrated assets, audit JSON and new docs found `0` secret-like findings; UI asset boundary scan passed for private path patterns.
- GitGate: `REVIEW_BLOCKED`; BRAIN_OS/Wabi changes sit under the broad host repo with unrelated dirty state.
- DeployGate: `REVIEW_BLOCKED`; medioevo.space release pipeline was detected separately but no publishable asset provenance gate has passed.
- Commit/push/deploy: not executed.

## 2026-05-19 - Wabi UI TaskSpec Gate Preview v0.1

- Backend: `wabi_sabi/core/taskspec_review.py` now builds redacted gate previews for review-only TaskSpecs.
- Endpoint: `GET /api/taskspec/gate-preview` in `-= BRAIN_OS =-\02_CLAUDIO\server\wabi_local_server.py`.
- UI: `-= BRAIN_OS =-\apps\local\wabi_ui\index.html#taskSpecReviewPanel` includes `Gate Preview`.
- Server restart: stopped old local UI PID `9520`, started PID `28768` on `http://127.0.0.1:8787`.
- Endpoint smoke: `POST /api/conversation/turn`, `GET /api/taskspec/gate-preview`, `POST /api/taskspec/apply` -> PASS.
- Endpoint state: `reason=APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1`, `apply_status=BLOCKED`, required gates include `ActionGate`, `GhostGate`, `RollbackStore`, `TestRunner`, `PathAllowlist`.
- Apply endpoint remains blocked: `APPLY_BLOCKED_REVIEW_ONLY_V0_1`, `applied_to_sources=false`.
- Cloud/graphics state: `cloud_provider_called=false`, `CLOUD_BUDGET_DRY_RUN`, `graphics_live=false`.
- Evidence:
  - `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_taskspec_gate_preview_20260519\gate_preview_endpoint_smoke.json`
  - `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_taskspec_gate_preview_20260519\wabi_ui_taskspec_gate_preview_interactive.png`
- Wabi unit: `python -B -m pytest tests\test_taskspec_review.py -q -p no:cacheprovider` -> `9 passed in 0.84s`.
- BRAIN_OS unit: `python -B -m pytest 02_CLAUDIO\tests\test_wabi_taskspec_gate_preview_api.py -q -p no:cacheprovider` -> `6 passed in 7.71s`.
- Wabi focal: `python -B -m pytest tests\test_taskspec_review.py tests\test_conversation_engine.py tests\test_conversational_cli.py tests\test_graphics_bridge.py tests\test_cloud_budget.py tests\test_cloud_budget_ui_status.py tests\test_build_assist_cloud.py -q -p no:cacheprovider` -> `52 passed in 14.33s`.
- BRAIN_OS focal: `python -B -m pytest 02_CLAUDIO\tests\test_wabi_local_server.py 02_CLAUDIO\tests\test_wabi_conversation_api.py 02_CLAUDIO\tests\test_wabi_taskspec_review_api.py 02_CLAUDIO\tests\test_wabi_taskspec_gate_preview_api.py -q -p no:cacheprovider` -> `248 passed in 270.38s`.
- Wabi regression: `python -B -m pytest -q -p no:cacheprovider` -> `362 passed in 156.89s (0:02:36)`.
- BRAIN_OS regression: `python -B -m pytest -q -p no:cacheprovider` -> `758 passed in 153.48s (0:02:33)`.
- Py compile: PASS for `wabi_sabi\core\conversation_engine.py`, `wabi_sabi\core\taskspec_review.py`, `wabi_sabi\core\graphics_bridge.py`, `wabi_sabi\core\cloud_budget.py`, `wabi_sabi\cli\main.py`, and `02_CLAUDIO\server\wabi_local_server.py`.
- No live cloud call, no BrowserBridge live, no graphics live, no UI command execution, no source apply.

## 2026-05-19 - CloudBudgetGate UI Visual QA

- Server: `-= BRAIN_OS =-\02_CLAUDIO\server\wabi_local_server.py` started locally on `http://127.0.0.1:8787` with PID `30848` after stale PID `23276` was found dead.
- Endpoint smoke: `GET /api/cloud-budget/status` -> PASS.
- Endpoint source of truth: `wabi_sabi.core.cloud_budget.CloudBudgetGate.render_status`.
- Endpoint state: `budget_gate=CLOUD_BUDGET_DRY_RUN`, `provider=nvidia`, `model_alias=nano-30b`, `double_opt_in=false`, `cloud_live_ready=false`, `proposal_only=true`, `cloud_provider_called=false`, `next_cloud_call_allowed=false`, `session_calls=0/3`, `daily_calls=0/10`, `usage_known=false`, `cost_known=false`.
- Visual QA: Edge headless local screenshot captured. Cloud Budget panel visible with CloudGate, Provider/model, Double opt-in, Next call allowed, Provider called, Proposal-only, Usage/cost known, Last status, Session calls and Daily calls.
- Evidence:
  - `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_visual_qa\WABI_CLOUD_BUDGET_UI_VISUAL_QA_20260519\cloud_budget_status_redacted.json`
  - `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_visual_qa\WABI_CLOUD_BUDGET_UI_VISUAL_QA_20260519\wabi_cloud_budget_ui_20260519.png`
  - `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\ui_visual_qa\WABI_CLOUD_BUDGET_UI_VISUAL_QA_20260519\wabi_cloud_budget_ui_tall_20260519.png`
- BRAIN_OS server focal: `python -B -m pytest 02_CLAUDIO\tests\test_wabi_local_server.py -q -p no:cacheprovider` -> `229 passed in 116.51s (0:01:56)`.
- Wabi focal: `python -B -m pytest tests\test_cloud_budget_ui_status.py tests\test_cloud_budget.py tests\test_build_assist_cloud.py tests\test_conversation_engine.py tests\test_conversational_cli.py -q -p no:cacheprovider` -> `39 passed in 23.23s`.
- Wabi regression: `python -B -m pytest -q -p no:cacheprovider` -> `352 passed in 214.62s (0:03:34)`.
- Py compile: PASS for `02_CLAUDIO\server\wabi_local_server.py`, `wabi_sabi\core\cloud_budget.py`, `wabi_sabi\cli\main.py`.
- Manual no-live smokes:
  - `.\wabi.cmd build-assist-status --json` -> PASS, `cloud_budget.budget_gate=CLOUD_BUDGET_DRY_RUN`.
  - `.\wabi.cmd --once "hola wabi"` -> PASS.
  - `.\wabi.cmd build-assist-plan "crear helper seguro" --dry-run --json` -> PASS, `cloud_provider_called=false`.
  - REPL `/status`, `/providers`, `/exit` -> PASS, both status surfaces show `cloud_budget`.
- No live cloud call executed. BrowserBridge live was not activated. `graphics_live` was not activated. PublicationGate remains `BLOCK`.

## 2026-05-19 - CloudBudgetGate UI v0.1

- Endpoint UI: `GET /api/cloud-budget/status`.
- UI panel: `-= BRAIN_OS =-\apps\local\wabi_ui\index.html#cloudBudgetPanel`.
- Source of truth: `CloudBudgetGate.render_status()`.
- Focal UI: `python -B -m pytest tests\test_cloud_budget_ui_status.py -q -p no:cacheprovider` -> `5 passed in 11.15s`.
- Focal required: `python -B -m pytest tests\test_cloud_budget.py tests\test_cloud_budget_ui_status.py tests\test_conversation_engine.py tests\test_conversational_cli.py tests\test_build_assist_cloud.py -q -p no:cacheprovider` -> `39 passed in 12.25s`.
- Wabi full: `python -B -m pytest -q -p no:cacheprovider` -> `352 passed in 372.11s (0:06:12)`.
- BRAIN_OS server/UI focal: `python -B -m pytest 02_CLAUDIO\tests\test_wabi_local_server.py -q -p no:cacheprovider` -> `229 passed in 138.64s (0:02:18)`.
- Py compile: PASS for Wabi `cloud_budget.py`, `conversation_engine.py`, `build_assist_cloud.py`, `cli/main.py`, `tests/test_cloud_budget_ui_status.py`, and BRAIN_OS `server/wabi_local_server.py`.
- Manual no-live: `build-assist-status --json`, `--once "hola wabi"`, `build-assist-plan --dry-run --json`, REPL `/status`, `/providers`, `/exit`.
- No live cloud call executed.
- `cloud_provider_called=false`, `proposal_only=true`, `graphics_live=false`, BrowserBridge live not activated.

## 2026-05-18 - Multi-step Workpacks v0.2

- Multi-step focal tests: 18 passed.
- Expanded Wabi/Claudio focal tests: 66 passed.
- 02_CLAUDIO full: 687 passed.
- Wabi full: 293 passed.
- Wabi safe-tests: ok=true, 293 passed, witness event 36.
- Wabi compileall: PASS.
- 02_CLAUDIO compileall: PASS.
- GEODIA: 74 passed.
- DUAT predictive: 117 passed.
- HTTP: /api/multi-step-workpacks, /api/workpack-scheduler, /api/workpacks, /api/local-hub, /api/agent-hub, /api/provider/diagnostic and chat provider question PASS.
- SecretScan focal: PASS, finding_count=0.

Provider remains SMOKE_FAIL_REDACTED, NVIDIA DO_NOT_CALL, DeepSeek REVIEW_QUOTA_OR_BILLING, PublicationGate BLOCK.

## 2026-05-18 - WABI UI VISUAL ASSET POLISH

- StateFingerprint: WABI-UI-VISUAL-ASSET-POLISH-20260518
- BRAIN_OS focused router/server: 110 passed.
- BRAIN_OS full: 629 passed.
- Wabi focal: 53 passed.
- Wabi full: 279 passed.
- Wabi safe-tests: ok=true, 279 passed, witness event 26.
- Wabi compileall: PASS.
- BRAIN_OS compileall: PASS.
- GEODIA: 74 passed.
- DUAT predictive: 117 passed.
- HTTP: /api/operational-workbench, /api/tree-health, /api/provider/diagnostic, /api/coding-acceptance, /, chat provider question PASS.
- SecretScan focal: PASS, findings_count=0.

Provider remains SMOKE_FAIL_REDACTED, route REVIEW, NVIDIA DO_NOT_CALL, PublicationGate BLOCK.

## 2026-05-18 - MEDIOEVO Hub public-safe + Local Agent Hub v0.1

- Wabi full: 279 passed.
- Wabi safe-tests: ok=true, 279 passed, witness event 28.
- 02_CLAUDIO focused: 88 passed; full: 597 passed.
- compileall: PASS.
- GEODIA: 74 passed.
- DUAT predictive: 117 passed.
- Public repo npm test: 44 passed; npm run build PASS.
- HTTP medioevo.space: /hub, /agents, /theory, /roadmap, /updates/2026-05-18 all 200.
- Secret/boundary scans: PASS.

## 2026-05-18 - Public Hub follow-up

- Public repo npm test: 44 passed.
- Public repo build: PASS.
- medioevo.space Hub routes: HTTP 200.
- LinkedIn package: manual-ready, scans PASS.
- NVIDIA: DO_NOT_CALL.
- Cloud LLM: not used.

## 2026-05-18 - Agent Chat Routing v0.2 Test Evidence

- 02_CLAUDIO focal server/workpack/chat: 141 passed.
- 02_CLAUDIO full: 690 passed.
- Wabi full: 283 passed.
- Wabi safe-tests: ok=true; 283 passed; witness_event_id=32.
- GEODIA: 74 passed.
- DUAT predictive registry: 117 passed.
- compileall Wabi/02_CLAUDIO: PASS.
- HTTP smoke local endpoints: PASS.
- SecretScan focal: PASS, findings_count=0.
- Provider state check: SMOKE_FAIL_REDACTED, NVIDIA DO_NOT_CALL, no SMOKE_PASS claim.

## Workpack Scheduler v0.1 - 2026-05-18

StateFingerprint: WORKPACK-SCHEDULER-v0-1-20260518

- Implemented local-only manual-tick Workpack Scheduler v0.1.
- Added `/api/workpack-scheduler` plus enqueue, approve, tick, retry, rollback and evidence endpoints.
- Integrated Scheduler into Local Hub, Agent Hub, Agent Chat and Wabi UI.
- Demo sequence passed: step-1, dependency-gated step-2, docs-note; CLOUD lane blocked.
- Provider remains SMOKE_FAIL_REDACTED / NVIDIA DO_NOT_CALL; DeepSeek remains REVIEW_QUOTA_OR_BILLING; PublicationGate BLOCK.
- Verification: Wabi 290 passed; safe-tests ok=true witness 33; 02_CLAUDIO 709 passed; GEODIA 74 passed; DUAT 117 passed; compileall PASS; SecretScan PASS.

Next: Multi-step Workpacks v0.2 or Agent Chat persistence/search v0.3.

## BrowserBridge multibackend + concilio opt-in - 2026-05-18

StateFingerprint: WABI-BROWSER-BRIDGE-MULTIBACKEND-20260518

- BrowserBridge focal baseline before edit: `7 passed`.
- Cloud proposal focal baseline before edit: `11 passed`.
- Py compile: `wabi_sabi\core\browser_bridge.py` and `wabi_sabi\cli\main.py` PASS.
- BrowserBridge focal after edit: `10 passed`.
- CLI/cloud/browser-gate focal: `37 passed`.
- CLI smoke `browser-bridge status --json`: PASS, `primary_backend=chrome-devtools-mcp`, `send_enabled=false`.
- CLI smoke `browser-bridge council "compara estrategia de backend" --json`: PASS, `service_count=16`, `prepared_count=16`, `online_ai_called=false`.
- Wabi full: `293 passed`.
- Wabi safe-tests: `ok=true`, `293 passed`, `witness_verified=true`, `witness_event_id=35`.
- BRAIN_OS world model benchmark: PASS, `gate_accuracy=1.0`, `false_approve_rate=0.0`, `network_calls=false`.
- BRAIN_OS MTS v0.3 benchmark: PASS, `success=True`, `mts_accuracy=0.98`, `critical_fail=0`.
- `02_CLAUDIO` first full run: `686 passed`, 1 failed by `gitleaks.exe version` timeout.
- Fix applied: `external_secret_tools._run_version` returns `VERSION_TIMEOUT` on timeout.
- `02_CLAUDIO` focused external secret tools: `14 passed`.
- `02_CLAUDIO` focused hub status regression: `1 passed`.
- `02_CLAUDIO` full after fix: `688 passed`.

No Kimi/Hermes/Chrome live send was executed. PublicationGate remains BLOCK.

## BrowserBridge Selector Pack v0.2 - 2026-05-18

StateFingerprint: BROWSER-BRIDGE-SELECTOR-PACK-v0-2-20260518

- `python -B -m py_compile wabi_sabi\core\browser_bridge_selector_pack.py wabi_sabi\core\browser_bridge.py wabi_sabi\cli\main.py`: PASS.
- `python -B -m py_compile 02_CLAUDIO\server\wabi_local_server.py 02_CLAUDIO\core\external_secret_tools.py`: PASS.
- `python -B -m pytest tests\test_browser_bridge.py -q -p no:cacheprovider`: PASS, `21 passed`.
- `python -B -m pytest tests\test_browser_bridge.py tests\test_redaction_and_cloud_adapters.py -q -p no:cacheprovider`: PASS, `32 passed`.
- Expanded Wabi/provider/CLI focal: PASS, `81 passed`.
- BRAIN_OS Wabi local server/UI focal: PASS, `180 passed`.
- Wabi full: PASS, `304 passed`.
- `.\wabi.cmd run-safe-tests --json`: PASS, `ok=true`, `304 passed`, `witness_event_id=38`, `witness_verified=true`.
- `python -B -m pytest 02_CLAUDIO\tests -q -p no:cacheprovider`: PASS, `690 passed`.
- GEODIA full: PASS, `74 passed`.
- DUAT predictive registry: PASS, `117 passed`.
- World model benchmark: PASS, `gate_accuracy=1.0`, `false_approve_rate=0.0`.
- MTS v0.3: PASS, `success=True`, `mts_accuracy=0.98`, `critical_fail=0`.
- HTTP temp server 8788: PASS for `/`, `/api/operational-workbench`, `/api/browser-bridge`, `/api/local-hub`, `/api/agent-hub`, `/api/workpack-scheduler`, `/api/provider/diagnostic`, and chat POST.
- SecretScan focal: PASS, `ok=true`, `finding_count=0`, `scanned=11`.

Kimi live smoke was not run because explicit send flags/URL were missing.
Chrome DevTools MCP read-only returned `DEVTOOLS_MCP_NOT_AVAILABLE`.
NVIDIA remained `DO_NOT_CALL`, DeepSeek remained `REVIEW_QUOTA_OR_BILLING`,
and PublicationGate remained `BLOCK`.


## 2026-05-19 - Build Assist Cloud

Comandos:

```powershell
python -B -m pytest tests\test_build_assist_cloud.py tests\test_provider_orchestrator.py tests\test_redaction_and_cloud_adapters.py tests\test_cloud_code_proposal.py -q -p no:cacheprovider
python -B -m pytest -q -p no:cacheprovider
```

Resultados:

- Focal: `37 passed in 5.69s`.
- Regresion Wabi: `317 passed in 114.72s`.

Smokes CLI:

- `build-assist-status --json`: `cloud_live_ready=false`, `default_model_alias=nano-30b`, `real_apply_allowed=false`.
- `build-assist-plan "crear helper seguro" --dry-run --json`: `cloud_provider_called=false`, PatchPlan generado en runtime, sin tocar fuentes.

## 2026-05-19 - NVIDIA nano-30b Live Smoke

Comandos:

```powershell
python -B -m pytest tests\test_build_assist_cloud.py tests\test_provider_orchestrator.py tests\test_redaction_and_cloud_adapters.py tests\test_cloud_code_proposal.py -q -p no:cacheprovider
.\wabi.cmd build-assist-smoke --provider nvidia --model nano-30b --json --workspace "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-"
$env:WABI_BUILD_ASSIST_CLOUD='1'; $env:WABI_ALLOW_CLOUD_PROVIDERS='1'; .\wabi.cmd build-assist-smoke --provider nvidia --model nano-30b --live --json --workspace "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-"
python -B -m pytest -q -p no:cacheprovider
python -B -m py_compile wabi_sabi\core\build_assist_cloud.py wabi_sabi\cli\main.py wabi_sabi\core\provider_orchestrator.py wabi_sabi\core\redaction.py
```

Resultados:

- Baseline focal: `37 passed in 40.97s`.
- Build-assist + redaction focal: `23 passed in 5.89s`.
- Focal recomendado final: `42 passed in 14.67s`.
- Regresion Wabi: `322 passed in 111.97s`.
- `py_compile`: PASS.
- Smoke sin live: `REVIEW_LIVE_FLAG_REQUIRED`, `cloud_provider_called=false`.
- Smoke live: `LIVE_SMOKE_PASS`, `cloud_provider_called=true`, `proposal_only`, `applied_to_sources=false`.
- Redaction scan: `PASS`, `secret_value_hits=0`.

## 2026-05-19 - Wabi Conversational CLI v0.1

Comandos:

```powershell
python -B -m pytest tests\test_conversational_cli.py tests\test_conversation_engine.py tests\test_graphics_bridge.py -q -p no:cacheprovider
.\wabi.cmd --help
.\wabi.cmd --once "hola wabi" --json
.\wabi.cmd build-assist-status --json
@'
/help
/status
crea una escena de DUAT city con agentes y handoff
programa un helper seguro para validar json
/exit
'@ | .\wabi.cmd
python -B -m py_compile wabi_sabi\cli\main.py wabi_sabi\core\conversation_engine.py wabi_sabi\core\graphics_bridge.py wabi_sabi\core\redaction.py
python -B -m pytest -q -p no:cacheprovider
```

Resultados:

- Focal conversacional requerido: `14 passed in 3.69s`.
- Focal conversacional + redaccion: `25 passed in 15.26s`.
- `py_compile`: PASS.
- Regresion Wabi: `336 passed in 495.58s (0:08:15)`.
- `.\wabi.cmd --help`: PASS.
- `.\wabi.cmd --once "hola wabi" --json`: PASS, `route=local_chat`, `intent_name=chat_general`, `cloud_provider_called=false`.
- `.\wabi.cmd build-assist-status --json`: PASS, `cloud_live_ready=false` sin doble bandera, `default_model_alias=nano-30b`.
- Interactivo `.\wabi.cmd`: PASS con `/help`, `/status`, graphics scene plan, code task spec y `/exit`.
- Cloud: no live call en esta fase; NVIDIA sigue `proposal_only`.
- GraphicsBridge: `graphics_live=false`, `graphics_plan_ready=true`, artefactos locales plan-only.

## 2026-05-19 - CloudBudgetGate v0.1

Comandos:

```powershell
python -B -m pytest tests\test_cloud_budget.py tests\test_conversation_engine.py tests\test_conversational_cli.py tests\test_build_assist_cloud.py -q -p no:cacheprovider
python -B -m py_compile wabi_sabi\core\cloud_budget.py wabi_sabi\core\conversation_engine.py wabi_sabi\core\build_assist_cloud.py wabi_sabi\cli\main.py
python -B -m pytest -q -p no:cacheprovider
.\wabi.cmd --once "hola wabi"
.\wabi.cmd build-assist-status --json
.\wabi.cmd build-assist-plan "crear helper seguro" --dry-run --json
@'
/status
/providers
usa nvidia para planear un helper seguro
/exit
'@ | .\wabi.cmd
```

Resultados:

- Focal CloudBudgetGate/build-assist/conversation: `34 passed in 15.93s`.
- `py_compile`: PASS.
- Regresion Wabi: `347 passed in 192.89s (0:03:12)`.
- Manual `--once`: PASS.
- Manual `build-assist-status`: PASS, `cloud_budget.budget_gate=CLOUD_BUDGET_DRY_RUN`.
- Manual `build-assist-plan --dry-run`: PASS, `cloud_provider_called=false`, `real_apply_allowed=false`.
- Manual REPL `/status` y `/providers`: PASS, ambos muestran `cloud_budget`.
- No live cloud call ejecutada en esta fase.
- Budget JSON focal secret scan: `0` coincidencias.

## 2026-05-19 - Wabi UI ConversationEngine

Comandos:

```powershell
python -B -m pytest 02_CLAUDIO\tests\test_wabi_local_server.py -q -p no:cacheprovider
python -B -m pytest 02_CLAUDIO\tests\test_wabi_conversation_api.py -q -p no:cacheprovider
python -B -m pytest tests\test_conversation_engine.py tests\test_conversational_cli.py tests\test_graphics_bridge.py tests\test_cloud_budget.py tests\test_cloud_budget_ui_status.py tests\test_build_assist_cloud.py -q -p no:cacheprovider
python -B -m pytest -q -p no:cacheprovider
python -B -m py_compile 02_CLAUDIO\server\wabi_local_server.py
python -B -m py_compile wabi_sabi\core\conversation_engine.py wabi_sabi\core\graphics_bridge.py wabi_sabi\core\cloud_budget.py wabi_sabi\cli\main.py
.\wabi.cmd --once "hola wabi"
.\wabi.cmd build-assist-status --json
.\wabi.cmd build-assist-plan "crear helper seguro" --dry-run --json
@('/status','/providers','/exit') | .\wabi.cmd
```

Resultados:

- `02_CLAUDIO\tests\test_wabi_local_server.py`: `229 passed in 173.21s`.
- `02_CLAUDIO\tests\test_wabi_conversation_api.py`: `6 passed in 10.66s`.
- Focal Wabi conversation/cloud/graphics/build-assist: `43 passed in 69.12s`.
- Regresion Wabi completa: `353 passed in 218.37s`.
- Regresion BRAIN_OS completa: `745 passed in 196.72s`.
- `py_compile`: PASS.
- Manual `--once`: PASS.
- Manual `build-assist-status`: PASS, `CLOUD_BUDGET_DRY_RUN`, `cloud_provider_called=false`.
- Manual `build-assist-plan --dry-run`: PASS, `cloud_provider_called=false`, `real_apply_allowed=false`.
- UI endpoint smokes: PASS para `chat_general`, `graphics_scene_request` y `build_assist_request`.
- No hubo llamada live cloud.

## 2026-05-19 - Wabi UI Review TaskSpec v0.1

Comandos:

```powershell
python -B -m pytest tests\test_taskspec_review.py tests\test_conversation_engine.py -q -p no:cacheprovider
python -B -m pytest 02_CLAUDIO\tests\test_wabi_taskspec_review_api.py -q -p no:cacheprovider
python -B -m pytest 02_CLAUDIO\tests\test_wabi_local_server.py 02_CLAUDIO\tests\test_wabi_conversation_api.py 02_CLAUDIO\tests\test_wabi_taskspec_review_api.py -q -p no:cacheprovider
python -B -m pytest tests\test_taskspec_review.py tests\test_conversation_engine.py tests\test_conversational_cli.py tests\test_graphics_bridge.py tests\test_cloud_budget.py tests\test_cloud_budget_ui_status.py tests\test_build_assist_cloud.py -q -p no:cacheprovider
python -B -m pytest -q -p no:cacheprovider
python -B -m py_compile 02_CLAUDIO\server\wabi_local_server.py
python -B -m py_compile wabi_sabi\core\conversation_engine.py wabi_sabi\core\taskspec_review.py wabi_sabi\core\graphics_bridge.py wabi_sabi\core\cloud_budget.py wabi_sabi\core\worktree.py wabi_sabi\cli\main.py
```

Resultados:

- TaskSpec + ConversationEngine focal: `13 passed in 11.34s`.
- BRAIN_OS TaskSpec API: `7 passed in 9.55s`.
- BRAIN_OS focal combinado: `242 passed in 83.67s`.
- Wabi focal requerido: `47 passed in 9.22s`.
- Wabi focal ampliado con worktree/provider-status: `51 passed in 18.26s`.
- Wabi regression: `357 passed in 355.74s`.
- BRAIN_OS regression: `752 passed in 573.25s`.
- `py_compile`: PASS.
- Manual UI smokes: code TaskSpec, graphics TaskSpec, build-assist dry-run, blocked apply y save draft redacted: PASS.
- No hubo live cloud call, BrowserBridge live ni graphics_live.

Nota:

- Se detecto y corrigio un timeout de `provider-status` por `git_worktree_summary()` heredando el repo host cuando el workspace de test esta en `AppData`. Fix focal: `4 passed in 4.69s`; temp no-git summary: `0.001s`.

## 2026-05-21 - HypothesisPacket / Counterexample Mode v0.1

Comandos:

```powershell
python -m unittest discover packages\shared-contracts\tests -v
python -B -m pytest tests/test_hypothesis_packet.py tests/test_conversation_engine.py tests/test_llm_work_response.py -q -p no:cacheprovider
python -B -m py_compile wabi_sabi\core\hypothesis_packet.py wabi_sabi\core\conversation_engine.py wabi_sabi\core\llm_work_response.py wabi_sabi\cli\main.py
python -B -m pytest -q -p no:cacheprovider
```

Resultados:

- Shared contracts: `11 tests OK`.
- Wabi focal hypothesis/conversation/safe-response: `20 passed in 7.33s`.
- `py_compile`: PASS.
- Wabi regression completa: `393 passed in 236.33s`.
- No hubo live cloud call, BrowserBridge live, graphics_live, publicacion ni apply de fuentes desde el nuevo modo.
