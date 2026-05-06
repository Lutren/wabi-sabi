# AI Browser Seguro - 09 Build Roadmap

Status: `ROADMAP`

## Phase 0 - Specification And Local Prototype

Status: `DONE_IN_THIS_PASS`

- Inventory active components.
- Threat model.
- Architecture.
- Security requirements.
- Stack options.
- MVP scope.
- Prompt injection policy.
- Evidence bundle schema.
- Local CLI SourceSnapshot prototype.
- Unit tests.

## Phase 1 - Harden Local Extractor

Status: `PARTIAL_DONE_LOCAL`

Done:

- Add schema validation command.
- Add domain policy JSON schema.
- Add explicit GhostGate memory decision schema.
- Enforce domain policy for `http(s)` remote stubs.
- Block unsafe domain policy permissions in MVP.
- Write `ghostgate.json` inside exported evidence bundles.

Still pending:

- Add COMMS message writer for snapshot handoff.
- Add fixture corpus with benign, hidden-DOM, phishing and fake-source samples.
- Add secret-scan integration for evidence bundles.

## Phase 2 - Controlled Fetch Engine

Status: `BLOCKED_BY_GATE`

- Choose Playwright only after dependency adoption gate.
- Use ephemeral BrowserContext.
- Disable JS by default.
- Block downloads, popups, service workers, permissions and cross-origin action.
- Route/block trackers and binary resources where possible.
- Fetch only domains allowed by policy.
- Record request/response metadata and content hash.

## Phase 3 - UI / Extension Surface

Status: `REVIEW`

- Browser extension with `activeTab` and optional host permissions.
- Side panel to capture current page as SourceSnapshot.
- Tauri local app shell for evidence review if needed.
- No Electron for untrusted remote content unless strict security checklist is
  met and Node integration is never exposed to remote content.

## Phase 4 - Agent Integration

Status: `REVIEW`

- COMMS packet emission.
- Wabi-Sabi control node review.
- Department handoffs.
- EvidenceGraph query interface.
- Claim registry and falsifier tracking.

## Phase 5 - Optional Public Package

Status: `BLOCK`

Requires:

- clean allowlist package;
- license review;
- focused secret scan;
- path scrub;
- claims scan;
- tests;
- private exclusion check;
- ActionGate for exact publication target.
