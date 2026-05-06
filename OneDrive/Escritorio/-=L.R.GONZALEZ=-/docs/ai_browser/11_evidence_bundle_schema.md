# AI Browser Seguro - 11 Evidence Bundle Schema

Status: `MVP_SCHEMA`

The prototype emits a bundle with:

- `source_snapshot`;
- `evidence_bundle` manifest;
- `ghostgate`;
- `witness_log_event`;
- readable text artifact when `--bundle-dir` is used.
- optional hash-only COMMS message when `--comms-outbox` is used.
- `secret_scan.json` for every bundle.

## SourceSnapshot Contract

Machine schema:

- `schemas/source_snapshot.schema.json`

Required top-level fields:

```json
{
  "snapshot_version": "source-snapshot-v1",
  "generated_at_utc": "2026-05-06T00:00:00Z",
  "source": {},
  "security": {},
  "hashes": {},
  "extraction": {},
  "classification": {},
  "snapshot_hash": "sha256",
  "fingerprint": "AI_BROWSER_SECURE_OBS_2026-05-06_<12hex>",
  "observation_envelope": {},
  "evidence_graph": {},
  "ghostgate": {},
  "witness_log_event": {}
}
```

## Evidence Bundle Contract

```json
{
  "schema": "ai_browser.evidence_bundle.v1",
  "status": "LOCAL_HTML_SNAPSHOT_CREATED",
  "source_snapshot": {},
  "evidence_bundle": {
    "schema": "ai_browser.evidence_bundle_manifest.v1",
    "artifacts": [
      {
        "path": "source_snapshot.json",
        "sha256": "snapshot_hash"
      },
      {
        "path": "readable_text.txt",
        "sha256": "readable_text_sha256"
      },
      {
        "path": "ghostgate.json",
        "sha256": "ghostgate_hash"
      },
      {
        "path": "witness_log.jsonl",
        "sha256": "event_hash"
      },
      {
        "path": "secret_scan.json",
        "sha256": "secret_scan_report_hash"
      }
    ],
    "quarantine": {
      "downloads": "blocked_not_downloaded",
      "credentials": "not_collected",
      "cookies": "not_persisted",
      "secrets": "not_detected"
    },
    "secret_scan": {}
  }
}
```

## EvidenceGraph Minimum

```json
{
  "nodes": [
    {"id": "source", "kind": "source"},
    {"id": "snapshot", "kind": "SourceSnapshot"},
    {"id": "readable_text", "kind": "extracted_text"},
    {"id": "web_instructions", "kind": "untrusted_instruction_channel"}
  ],
  "edges": [
    {"from": "source", "to": "snapshot", "kind": "captured_as"},
    {"from": "snapshot", "to": "readable_text", "kind": "extracts"},
    {"from": "snapshot", "to": "web_instructions", "kind": "separates_untrusted"}
  ]
}
```

## WitnessLog Minimum

```json
{
  "timestamp_utc": "2026-05-06T00:00:00Z",
  "event_type": "ai_browser_source_snapshot",
  "actor": "tools/ai_browser/snapshot_url.py",
  "previous_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "action_gate": "APPROVE",
  "status": "SNAPSHOT_CREATED_LOCAL",
  "artifact_hashes": {
    "source_snapshot": "sha256"
  },
  "event_hash": "sha256"
}
```

The `event_hash` is computed over canonical JSON without the `event_hash` field.

## COMMS Handoff Minimum

Machine schema:

- `schemas/comms_source_snapshot_handoff.schema.json`

The CLI emits this only when `--comms-outbox` is explicitly supplied:

```json
{
  "schema": "ai_browser.comms.source_snapshot_handoff.v1",
  "created_at_utc": "2026-05-06T00:00:00Z",
  "from": "ai-browser-secure",
  "to": "wabi-sabi-sentido-comun",
  "intent": "handoff_source_snapshot",
  "status": "APPROVE",
  "source_snapshot": {
    "hash": "sha256",
    "fingerprint": "AI_BROWSER_SECURE_OBS_2026-05-06_<12hex>",
    "path_hint": "source_snapshot.json"
  },
  "observation_envelope": {},
  "action_gate": "APPROVE",
  "ghostgate": {},
  "evidence_bundle": {},
  "web_content_included": false,
  "requested_next_action": "consume_read_only_evidence_only",
  "message_hash": "sha256"
}
```

The message intentionally cites evidence hashes and gate status instead of
pasting raw or hidden web-origin text into COMMS.

## Secret Scan Minimum

Machine schema:

- `schemas/secret_scan_report.schema.json`

```json
{
  "schema": "ai_browser.secret_scan_report.v1",
  "status": "PASS",
  "snapshot_hash": "sha256",
  "scanned_artifacts": [
    "source_raw_html_hash_only",
    "source_snapshot.extraction.readable_text",
    "source_snapshot.extraction.hidden_dom_text"
  ],
  "redaction": {
    "secret_like_content_redacted": false,
    "secret_redaction_count": 0,
    "redaction_token": "[REDACTED_SECRET_LIKE_CONTENT]"
  },
  "findings": [],
  "action_gate": "APPROVE",
  "report_hash": "sha256"
}
```

When secret-like content is detected, extracted text is redacted, the scan
status becomes `REVIEW`, and GhostGate blocks memory/canon persistence.

## Local Validators

```powershell
python tools\ai_browser\snapshot_url.py --validate-snapshot .\source_snapshot.json --pretty
python tools\ai_browser\snapshot_url.py --validate-bundle .\evidence_bundle.json --pretty
python tools\ai_browser\snapshot_url.py --validate-comms-message .\comms_message.json --pretty
```

The validators are stdlib-only and verify hash fields for `WitnessLog`,
`secret_scan.report_hash` and `comms_message.message_hash`.

## ActionGate Minimum

Machine schema:

- `schemas/ai_browser_action_gate.schema.json`

```json
{
  "schema": "ai_browser.action_gate.v1",
  "decision": "APPROVE",
  "operation": "remote_stub",
  "allowed_operations": ["remote_stub"],
  "network_mode": "stub_only",
  "target_url": "https://example.com/source",
  "allowed_domains": ["example.com"],
  "reason": "operator approved remote stub only"
}
```

A generic `decision=APPROVE` is not enough for `http(s)` sources.

## Domain Policy Minimum

Machine schema:

- `schemas/domain_policy.schema.json`

```json
{
  "schema": "ai_browser.domain_policy.v1",
  "action_gate": "APPROVE",
  "domains": [
    {
      "domain_pattern": "example.com",
      "allowed_modes": ["read_only", "fetch_stub"],
      "action_gate": "APPROVE",
      "robots_status": "UNKNOWN",
      "license_status": "UNKNOWN",
      "max_pages_per_run": 1,
      "allow_javascript": false,
      "allow_downloads": false,
      "allow_forms": false,
      "allow_login": false,
      "allow_credentials": false
    }
  ]
}
```

## GhostGate Minimum

Machine schema:

- `schemas/ghostgate_memory.schema.json`

```json
{
  "schema": "ai_browser.ghostgate_memory_decision.v1",
  "source_input": "path-or-url",
  "source_snapshot_hash": "sha256",
  "decision": "APPROVE",
  "memory_allowed": true,
  "canon_allowed": false,
  "risk_flags": [],
  "reasons": ["no memory-contamination flags detected in local read-only snapshot"],
  "required_next_gate": "none"
}
```

## Handoff Fingerprint

Format:

```text
AI_BROWSER_SECURE_OBS_2026-05-06_<hash corto>
```

The MVP uses the first 12 hex characters of the SourceSnapshot hash.
