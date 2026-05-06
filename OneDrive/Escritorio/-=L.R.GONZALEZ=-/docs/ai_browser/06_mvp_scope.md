# AI Browser Seguro - 06 MVP Scope

Status: `MVP_DEFINED_AND_PARTIAL_PROTOTYPE_CREATED`

## MVP Must Do

- Accept local HTML file.
- Accept `file://` URL by reading local file.
- Accept `http(s)` URL only when an ActionGate JSON says `APPROVE`, then return
  a stub without network fetch.
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
- Gate remote URL stubs with both ActionGate and domain policy.
- Emit `GhostGate` memory decision for every snapshot.

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
- `tests/test_source_snapshot.py`
- `schemas/domain_policy.schema.json`
- `schemas/ghostgate_memory.schema.json`

## CLI Examples

Local HTML:

```powershell
python tools\ai_browser\snapshot_url.py --html-file .\sample.html --bundle-dir .\qa_artifacts\ai_browser\sample --pretty
```

Remote URL stub with gate:

```powershell
python tools\ai_browser\snapshot_url.py --url https://example.com --gate-file .\gate.json --domain-policy .\domain_policy.json --pretty
```

Without an `APPROVE` gate, `http(s)` URLs fail with
`URL_NETWORK_BLOCKED_BY_ACTION_GATE`. Without a matching read-only domain
policy, they fail with `URL_NETWORK_BLOCKED_BY_DOMAIN_POLICY`.

Validate snapshot:

```powershell
python tools\ai_browser\snapshot_url.py --validate-snapshot .\source_snapshot.json --pretty
```

## Closure Criteria For MVP

- Unit tests pass.
- SourceSnapshot schema exists.
- Threat model exists.
- Remote fetch remains stubbed.
- Docs state blocked actions explicitly.
- Domain policy and GhostGate tests pass.
