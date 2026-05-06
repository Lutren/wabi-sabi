# AI Browser Seguro - 00 Inventory

Status: `SPEC_AND_LOCAL_MVP`

Date: `2026-05-06`

Scope: workspace root `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`.

This inventory is evidence for architecture. It is not permission to publish,
fetch remote sites, log in, download files, move private code, or merge Argus
private surfaces into public packages.

## Search Terms

- browser
- navegador
- manifest
- prompt injection
- ActionGate
- WitnessLog
- COMMS
- ObservationEnvelope
- obs-safe
- Argus
- Sabueso
- Onion
- Security
- sandbox
- source_registry
- evidence

## CERTEZA

These components were found in the active workspace.

| Component | Evidence | Read |
|---|---|---|
| Root safety contract | `AGENTS.md` | Workspace is mixed; external actions, secrets, private game/TCG and broad packaging stay gated. |
| SETO contract | `docs/developer/CURADOR_SETO_GLOBAL_OPERATING_CONTRACT_2026-05-05.md` | Defines `ObservationEnvelope`, `ActionGate`, `WitnessLog`, COMMS, epistemic states and cleanup boundaries. |
| COMMS schemas | `COMMS/schemas/*.schema.json` | Existing JSON schemas for `ObservationEnvelope`, `ActionGate` and `WitnessLog` exist. |
| COMMS validator | `COMMS/tools/validate_seto_comms.py` | Validates envelopes and WitnessLog tail hash-chain. |
| WitnessLog store | `qa_artifacts/witness_log/curador_seto_witnesslog.jsonl` | Existing append-only local evidence log with chained hashes. |
| obs-safe-integration-kit | `packages/open-dev/obs-safe-integration-kit` | Existing local-first `ObservationEnvelope`, `EstadoPSI`, `ActionGate`, `EvidenceStore` and browser-use wrapper. |
| Browser-use guard pattern | `packages/open-dev/obs-safe-integration-kit/examples/browser_use_guard.py` | Existing rule: snapshots first; clicks/uploads/eval gated and dry-run. |
| observacionismo-gate browser manifest restriction | `packages/open-dev/observacionismo-gate/observacionismo_gate.py` | Browser automation blocks when `browser=true` and `manifest=false`. |
| Browser manifest example | `packages/open-dev/claudio-os-blueprint/browser-manifests/suno_create_download_track.json` | Existing example of allowed, forbidden and approval-required browser actions. |
| Blocked browser decision example | `packages/open-dev/claudio-os-blueprint/examples/decision_browser_blocked.json` | Browser upload without manifest is blocked. |
| GEODIA source snapshots | `research/geodia-social-observatory/geodia_social_observatory/snapshot.py` | Existing offline source snapshot pattern with SHA256 and no network fetch. |
| GEODIA source registry | `research/geodia-social-observatory/geodia_social_observatory/source_registry.py` | Local source intake/allowlist pattern. |
| AI-Web Gateway product card | `docs/product/AGENT_PRODUCT_FICHAS_2026-05-02.md` and `docs/business/PRODUCT_CATALOG.md` | Candidate exists as spec/whitepaper lane, not as complete browser. |
| Argus Desktop | `apps/commercial/argus-desktop` | Commercial/internal desktop app exists; must not be mixed with public browser spec by default. |
| Wabi-Sabi COMMS state | `COMMS/agents_state/wabi-sabi-sentido-comun.json` | Existing state is `POLICY_ONLY_LEARNING_SOURCE` with ActionGate `REVIEW`. |
| Security/geolocation guard | `tools/security_geolocation_guard.py` | Existing security evidence collector; not a browser runtime. |
| Prompt-injection evidence in tool research | `tools/claw-code/ROADMAP.md` | Contains prompt-injection findings in a dev tool roadmap; use as threat evidence, not browser implementation. |

## INFERENCIA

- The safe browser should be a local-first evidence gateway before it becomes a
  full browser UI.
- The closest existing implementation pattern is:
  `GEODIA offline SourceSnapshot` + `obs-safe ActionGate/EvidenceStore` +
  `COMMS/WitnessLog` + `observacionismo-gate browser manifest rule`.
- `AI-Web Gateway Observacionista` appears as a product/spec candidate, but no
  complete browser implementation was found in the active paths searched.
- Browser automation should remain blocked unless a manifest, domain policy and
  ActionGate approval exist for the exact action.
- The public version must stay generic and must not absorb Argus private assets,
  runtime secrets, browser profiles, cookies or private game/TCG material.

## INCOGNITA

- No active implementation named `Sabueso`, `Onion` or `Malika` was found in
  the active search paths used for this pass.
- `GhostGate` appears as a concept in intake material, but no active runtime
  contract was found. Treat it as a proposed memory-contamination gate until a
  schema/test exists.
- Current licenses and latest security posture for all possible browser stacks
  require destination-specific verification before dependency adoption.
- Live web fetching is not implemented in the MVP. Remote source status,
  robots policy, terms, license and current content remain unknown until a gated
  external research pass runs.

## New Local Artifacts From This Pass

- `docs/ai_browser/*.md`
- `tools/ai_browser/snapshot_url.py`
- `schemas/source_snapshot.schema.json`
- `tests/test_source_snapshot.py`
