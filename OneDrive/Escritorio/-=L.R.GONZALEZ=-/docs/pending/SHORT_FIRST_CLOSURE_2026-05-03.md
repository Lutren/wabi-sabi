# Short-First Closure - 2026-05-03

## Snapshot

- Pending snapshot refreshed: `active_dedup=1760`, `claudio_open=112`.
- Host gate before security repair: `BLOCK` during a transient CPU spike.
- Host gate after security repair: `REVIEW`, reason `residuo_precaucion`.

## Closed Locally

### 1. Local website server exposure

Problem:

- Security Sentinel reported `Expected-local service exposed off loopback on :::8789`.
- Process was:
  `python -m http.server 8789 --directory ...\claudio\website`.

Action:

- Stopped only that confirmed PID.
- Restarted same server as:
  `python -m http.server 8789 --bind 127.0.0.1 --directory ...\claudio\website`.

Verification:

- `Get-NetTCPConnection -LocalPort 8789 -State Listen` now reports
  `LocalAddress=127.0.0.1`.
- `Invoke-WebRequest http://127.0.0.1:8789/` returned `200`.
- Security Sentinel high issue count dropped from 4 to 3.

### 2. Duplicate verification pass

Commands:

```powershell
python tools\release\find_duplicates.py --mode name --limit 30 --json
python tools\release\find_large_files.py --limit 40 --min-mb 10 --include-denied --json
```

Findings:

- Filename duplicates are mostly expected monorepo noise.
- Global hash duplicate scan initially timed out; after optimizing the tool it
  completed and returned exact duplicate groups.
- Exact duplicate Asistente package copies and Ruflo model vendor copies are
  now documented in `DUPLICATES_AND_DEAD_CODE.md` and `DELETE_CANDIDATES.md`.

Tooling fix:

- `tools\release\find_duplicates.py` now groups by file size before hashing in
  `--mode hash`, avoiding the previous global timeout.
- Validation: `python -m py_compile tools\release\find_duplicates.py` passed.
- Validation: `python tools\release\find_duplicates.py --mode hash --limit 30 --json`
  completed and returned exact duplicate groups.

Action:

- Removed only the two ignored exact duplicates under
  `apps\commercial\asistente-negocio\release\`.
- Preserved the QA final package copies under
  `apps\commercial\asistente-negocio\qa_artifacts\asistente_negocio_final_package_2026-05-02\Asistente_Negocio_MEDIOEVO_v1.0.0\Windows\`.

Verification:

- `git check-ignore` confirmed `apps/commercial/asistente-negocio/.gitignore:4:release/`.
- Both QA copies still exist.
- C: free space after deletion: about `40.50 GB`.

## Still Blocked

- Website deploy/social/Gumroad remain blocked until target-specific scans and
  ActionGate pass. GitHub pushes for `duat-lab` and `Lutren/Lutren` were later
  approved and executed.
- Remaining Security Sentinel high issues are Windows RPC/NetBIOS surfaces:
  `:::135`, `0.0.0.0:135`, `172.30.32.1:139`. These require admin/network
  policy review; they are not safe to mutate blindly from the workspace.

## Curador Correction

- `camera_frames\oppo_frame_*.png` was checked as a suspected quick duplicate
  cleanup. Corrected result: 218 files, 1,735,498 bytes total, 1 unique SHA256.
- ActionGate approved deletion:
  `1587d99b-449c-4b5e-a7e7-36214498a471`.
- Deleted 217 exact duplicates, 1,727,537 bytes, preserving
  `oppo_frame_20260418_002952.png`. Registered as
  `docs\intake\CAMERA_FRAMES_OPPO_RUNTIME_FICHA_2026-05-03.md`.
- Evidence:
  `qa_artifacts\release_validation\camera-frames-cleanup-dry-run-2026-05-03.json`;
  `qa_artifacts\release_validation\camera-frames-cleanup-result-2026-05-03.json`.

## Ruflo Duplicate Closure

- Verified root `-=LIBROS\.skills\ruflo` is the canonical copy for this pass:
  it has `.git` and upstream remote. The duplicate under
  `claudio\.skills\ruflo` has no `.git`.
- Deleted only `model.onnx` and `model.onnx.data` from the Claudio duplicate
  model folder after exact-hash comparison and ActionGate
  `e6623488-ef44-47f1-b7c2-164e7dba9272`.
- Recovered `96,854,299` bytes; canonical model files remain in the root
  `.skills\ruflo` clone.
- Evidence:
  `docs\intake\RUFLO_MODEL_DUPLICATE_CLEANUP_FICHA_2026-05-03.md`;
  `qa_artifacts\release_validation\ruflo-model-duplicate-cleanup-result-2026-05-03.json`.

## Cache Residue

- Deleted regenerated ignored cache `tools\release\__pycache__` after
  ActionGate `89f8deb8-2306-4fe3-ad83-49d0398563f4`.
- Removed 17 `.pyc` files, 269,826 bytes.
- Evidence:
  `qa_artifacts\release_validation\pycache-cleanup-result-2026-05-03.json`.

## Asistente Generated Output Closure

- Deleted generated ignored Electron output:
  `apps\commercial\asistente-negocio\release\win-unpacked`.
- Removed 75 files, 353,080,065 bytes, after ActionGate
  `cd4344b5-700e-4cd4-9863-ec5de3b42c98`.
- Preserved final QA package files under
  `apps\commercial\asistente-negocio\qa_artifacts\asistente_negocio_final_package_2026-05-02\Asistente_Negocio_MEDIOEVO_v1.0.0\Windows`.
- Evidence:
  `docs\intake\ASISTENTE_WIN_UNPACKED_CLEANUP_FICHA_2026-05-03.md`;
  `qa_artifacts\release_validation\asistente-win-unpacked-cleanup-result-2026-05-03.json`.
- Remaining small residue later closed:
  `Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.exe.blockmap` and
  `builder-debug.yml`, 117,232 bytes total. Deleted after ActionGate
  `3b117372-f8a9-4e6a-bab3-cccd326a46e6`; empty `release/` folder removed
  after ActionGate `7d32f84f-a535-4f5e-86a7-e0dbfa4909ac`.
  Evidence:
  `qa_artifacts\release_validation\asistente-release-residue-cleanup-result-2026-05-03.json`;
  `qa_artifacts\release_validation\asistente-release-empty-dir-cleanup-result-2026-05-03.json`.

## Next Short Tasks

1. Do not repeat Ruflo model cleanup; it is closed and documented.
2. If host gate returns `APPROVE`, the only tiny safe cleanup candidate left
   from this loop is regenerated `tools\release\__pycache__`, but it should be
   deleted only at the very end because Python verification recreates it.
3. For larger savings, review `_archive\legacy\2026-04-29\argus_generated_artifacts_second_pass\...`
   with curador preflight before any delete; do not treat it as trash until its
   evidence value is closed.
4. Prepare website deploy only after resolving current website dirty tree,
   focused scans, and ActionGate.

## Triage Added After Latest Continue

- Pending snapshot refreshed: `active_dedup=1760`, `claudio_open=112`.
- Security Sentinel remains defensive/read-only; Windows Defender is enabled.
- Remaining high security issues are Windows RPC/NetBIOS listeners:
  `:::135`, `0.0.0.0:135`, `172.30.32.1:139`.
- `find_duplicates.py --mode hash --limit 12 --json` now returns mostly
  private TCG assets, valid license duplicates and empty Python package
  markers. No new safe delete was chosen.
- `find_large_files.py --limit 30 --min-mb 20 --include-denied --json` shows
  the largest payload is Git history/vendor/private packs. Do not delete
  `.git\objects` directly.

## Observacionismo Lab Closure Added

- Added per-profile `residual_signature`.
- Added `heldout_report` via `--heldout-frac`.
- Added negative controls and no-network `selftest`.
- Latest heldout smoke:
  `qa_artifacts\research\observacionismo_lab_heldout_smoke_2026-05-03.json`.
- Latest selftest:
  `qa_artifacts\research\observacionismo_lab_selftest_2026-05-03.json`.
- Validation:
  `python -m py_compile research\observacionismo-lab\observacionismo_lab.py`;
  `python tools\release\scan_secrets.py --path research\observacionismo-lab --json --fail-on-findings`
  returned `count_reported=0`.

## Final Cache Cleanup Added

- Host runtime report refreshed with `gate=APPROVE`.
- ActionGate `file_delete` approved with receptor `repo_cleanup_receptor`:
  `4e71b814-16bd-4210-a909-ff3dbeb13fb5`.
- Deleted regenerated caches only:
  - `tools\release\__pycache__`
  - `research\observacionismo-lab\__pycache__`
- Evidence:
  `qa_artifacts\release_validation\pycache-final-cleanup-result-2026-05-03.json`.
- Result: `6` regenerated `.pyc` files across the final validation passes,
  `118,310` bytes, both directories absent after delete.

## GitHub Push Closure

- `duat-lab`: pushed `37aeeacf00d9fed96a24544ff36c278271c0bb51`; remote verified.
- `Lutren/Lutren`: remote had new commits, so local branch was fetched and
  rebased without force; pushed `9a2e5d6eca3e4e8169792caeaf232db03e9907dc`;
  remote verified.
