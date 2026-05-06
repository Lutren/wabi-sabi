# AI Browser Seguro - 11 Evidence Bundle Schema

Status: `MVP_SCHEMA`

The prototype emits a bundle with:

- `source_snapshot`;
- `evidence_bundle` manifest;
- `ghostgate`;
- `witness_log_event`;
- readable text artifact when `--bundle-dir` is used.

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
      }
    ],
    "quarantine": {
      "downloads": "blocked_not_downloaded",
      "credentials": "not_collected",
      "cookies": "not_persisted"
    }
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
