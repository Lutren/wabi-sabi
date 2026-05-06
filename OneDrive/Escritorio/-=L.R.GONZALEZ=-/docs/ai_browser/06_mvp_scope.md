# AI Browser Seguro - 06 MVP Scope

Status: `MVP_DEFINED_AND_PARTIAL_PROTOTYPE_CREATED`

## MVP Must Do

- Accept local HTML file.
- Accept `file://` URL by reading local file.
- Accept `http(s)` URL only when an ActionGate JSON explicitly allows
  `remote_stub`, says `network_mode=stub_only`, matches the URL/domain and a
  domain policy allows read-only mode, then return a stub without network fetch.
- Extract readable text without executing JS.
- Separate hidden DOM text.
- Detect web-origin instruction patterns.
- Detect forms, password inputs, scripts, downloads and meta refresh.
- Produce `SourceSnapshot`.
- Hash raw input, readable text and hidden DOM text.
- Classify `CERTEZA`, `INFERENCIA`, `INCOGNITA`.
- Produce a minimal EvidenceGraph.
- Produce a WitnessLog event with hash.
- Export evidence bundle.
- Validate an existing `source_snapshot.json` without new dependencies.
- Validate an existing `evidence_bundle.json` without new dependencies.
- Validate an existing COMMS handoff message without new dependencies.
- Gate remote URL stubs with both ActionGate and domain policy.
- Emit `GhostGate` memory decision for every snapshot.
- Optionally emit a hash-only COMMS handoff message when `--comms-outbox` is
  explicitly supplied.
- Keep a synthetic risk fixture corpus for regression tests.
- Redact secret-like extracted text and emit `secret_scan.json`.

## MVP Must Not Do

- No login automation.
- No credential storage.
- No download.
- No upload.
- No JS execution.
- No shell execution.
- No external account action.
- No scraping loop.
- No browser profile reuse.
- No Argus private merge.
- No publishing.

## Prototype Files

- `tools/ai_browser/snapshot_url.py`
- `schemas/source_snapshot.schema.json`
- `schemas/ai_browser_action_gate.schema.json`
- `tests/test_source_snapshot.py`
- `schemas/domain_policy.schema.json`
- `schemas/ghostgate_memory.schema.json`
- `schemas/secret_scan_report.schema.json`
- `schemas/comms_source_snapshot_handoff.schema.json`
- `tests/fixtures/ai_browser/*.html`

## CLI Examples

Local HTML:

```powershell
python tools\ai_browser\snapshot_url.py --html-file .\sample.html --bundle-dir .\qa_artifacts\ai_browser\sample --pretty
```

Remote URL stub with gate:

```powershell
python tools\ai_browser\snapshot_url.py --url https://example.com --gate-file .\gate.json --domain-policy .\domain_policy.json --pretty
```

Without a scoped `APPROVE` gate, `http(s)` URLs fail with
`URL_NETWORK_BLOCKED_BY_ACTION_GATE`. The gate must include:

```json
{
  "schema": "ai_browser.action_gate.v1",
  "decision": "APPROVE",
  "operation": "remote_stub",
  "allowed_operations": ["remote_stub"],
  "network_mode": "stub_only",
  "target_url": "https://example.com",
  "allowed_domains": ["example.com"],
  "reason": "operator approved remote stub only"
}
```

Without a matching read-only domain policy, URLs fail with
`URL_NETWORK_BLOCKED_BY_DOMAIN_POLICY`.

Validate snapshot:

```powershell
python tools\ai_browser\snapshot_url.py --validate-snapshot .\source_snapshot.json --pretty
```

Validate bundle:

```powershell
python tools\ai_browser\snapshot_url.py --validate-bundle .\evidence_bundle.json --pretty
```

Validate COMMS handoff:

```powershell
python tools\ai_browser\snapshot_url.py --validate-comms-message .\comms_message.json --pretty
```

Local COMMS handoff, opt-in only:

```powershell
python tools\ai_browser\snapshot_url.py --html-file .\sample.html --bundle-dir .\qa_artifacts\ai_browser\sample --comms-outbox .\COMMS\outbox\ai-browser-secure.jsonl --pretty
```

The COMMS message cites hashes, `ObservationEnvelope`, `ActionGate` and
`GhostGate`. It does not include raw web-origin text.

Secret scan:

- `secret_scan.json` is written in every bundle.
- Secret-like extracted strings are replaced with
  `[REDACTED_SECRET_LIKE_CONTENT]`.
- Secret-like raw source content sets ActionGate/GhostGate to review/block
  posture, while raw HTML remains hash-only.

## Closure Criteria For MVP

- Unit tests pass.
- SourceSnapshot schema exists.
- Threat model exists.
- Remote fetch remains stubbed.
- Docs state blocked actions explicitly.
- Domain policy and GhostGate tests pass.
- COMMS handoff writer remains opt-in and hash-only.
- Secret-like fixture proves redaction and bundle scan behavior.
- Bundle and COMMS message validators reject hash tampering.
- Generic remote `decision=APPROVE` is blocked unless scoped to `remote_stub`.
