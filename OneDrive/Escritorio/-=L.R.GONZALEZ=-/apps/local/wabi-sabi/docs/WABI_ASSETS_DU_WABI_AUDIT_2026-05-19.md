# WABI Assets Du WABI Audit - 2026-05-19

Fingerprint: `WABI_ASSETS_DU_WABI_AUDIT_20260519`

## Scope

Source audited:

`C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\-=LR WORKING BENCH=-\Assets Du WABI`

Public artifacts redact the source root as:

`<BRAIN_OS>/LR_WORKING_BENCH/Assets Du WABI`

## Gate Result

- ActionGate: `APPROVE_LOCAL_UNTIL_RELEASE`
- AssetGate: `REVIEW_PUBLIC_SAFE_ASSETS_REQUIRED`
- RawAdoption: `BLOCK`
- ZipExtraction: `BLOCK_THIS_RUN`
- PublicationGate: `REVIEW`

`curador_preflight.py` returned `NEEDS_FICHA_BEFORE_USE` for the exact source path. A prior partial match exists for `POST\Assets Du WABI`, and that ficha explicitly keeps raw adoption, runtime import and publication blocked until provenance review. This run therefore allows only metadata audit and a small local UI copy of selected, re-encoded candidates. It does not approve external publication.

## Audit Counts

| metric | count |
|---|---:|
| total files | 125 |
| images | 122 |
| archives | 3 |
| images with EXIF present | 0 |
| secret-like content findings | 0 |
| private path leak findings | 0 |
| duplicate hashes | 0 |
| local internal-reviewed image candidates | 122 |
| review-required archives | 3 |

## Archive Findings

Archives were registered but not extracted or copied:

| filename | size bytes | zip entries | decision |
|---|---:|---:|---|
| `duat-brain-os-v1.4.0.zip` | 23536 | 29 | `REVIEW_REQUIRED` |
| `duat-physics-light-engine-v1.3.0.zip` | 41537 | 34 | `REVIEW_REQUIRED` |
| `Kimi_Agent_Ayuda con motor de audio.zip` | 193452 | 124 | `REVIEW_REQUIRED` |

Some ZIP entry names matched review terms such as `gameMechanics`, `ui` or `audio`; this is not a secret finding, but it blocks raw public adoption until source, license and target lane are reviewed.

## Selected Local UI Candidates

Four PNGs were selected after metadata scan and visual contact-sheet review:

| target | use case | publication allowed |
|---|---|---|
| `assets/wabi_du_wabi_20260519/duat-control-surface.png` | hero background | false |
| `assets/wabi_du_wabi_20260519/image-reactor-workstation.png` | asset ribbon | false |
| `assets/wabi_du_wabi_20260519/tool-forge-gate.png` | asset ribbon | false |
| `assets/wabi_du_wabi_20260519/causal-frame-orb-v2.png` | accent | false |

They were re-encoded as PNG without metadata for local UI use. The manifest records redacted source path, source hash, target hash, dimensions and boundary.

Manifest:

`C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\apps\local\wabi_ui\assets\wabi_du_wabi_20260519\ASSET_MANIFEST_20260519.json`

Runtime audit JSON:

`C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\asset_audit\wabi_assets_du_wabi_audit_20260519.json`

Contact sheets:

`C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\asset_audit\contact_sheets_20260519\`

## Public Boundary

These assets are not yet public-safe for GitHub or medioevo.space release because provenance/licensing is not established in a release-ready ficha. The local UI can render them as internal reviewed candidates; external publication remains `REVIEW`.

Before external publication:

1. Owner confirms provenance/license for the four selected targets.
2. Manifest field `publication_allowed` is updated only after review.
3. Secret/path/metadata scan runs on the final public staging output.
4. Build/test route checks pass.
5. GitGate and DeployGate confirm repo/domain.

## Decision

Local UI integration: `APPROVE_LOCAL_REVIEWED_CANDIDATE`.

External GitHub/medioevo.space publication with these assets: `REVIEW_BLOCKED_UNTIL_PUBLIC_SAFE_PROVENANCE`.

## QA Closure

- Manifest and copied assets were validated by `02_CLAUDIO\tests\test_wabi_local_server.py`.
- Local UI rendered the selected assets with `broken_images=0`.
- Gate Preview remained active: `APPLY_NOT_AVAILABLE_REVIEW_ONLY_V0_1`.
- Safety flags remained unchanged: `cloud_provider_called=false`, `applied_to_sources=false`, `graphics_live=false`.
- Secret-like scan over integrated asset directory, audit JSON and new docs found `0` findings.
- Boundary scan over the UI file and integrated asset manifest found no private source path leaks.
