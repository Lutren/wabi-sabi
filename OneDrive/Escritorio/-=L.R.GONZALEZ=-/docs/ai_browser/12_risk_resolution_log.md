# AI Browser Seguro - 12 Risk Resolution Log

Status: `LOCAL_HARDENING_PASS`

Date: `2026-05-06`

## Resolved Locally

| Risk | Resolution | Evidence |
|---|---|---|
| Remote URL accepted with only ActionGate | Remote URL now also requires matching domain policy | `tools/ai_browser/snapshot_url.py`, `tests/test_source_snapshot.py` |
| Overbroad ActionGate approval | Generic `decision=APPROVE` no longer unlocks a remote stub; gate must be scoped to `remote_stub`, `stub_only` and URL/domain | `schemas/ai_browser_action_gate.schema.json`, `test_http_url_with_generic_approve_gate_is_blocked` |
| Unsafe domain permissions | Policy entries that allow JS, downloads, forms, login or credentials block the URL stub | `test_unsafe_domain_policy_is_blocked` |
| Memory contamination | Every snapshot emits `ghostgate`; risky snapshots set `memory_allowed=false` | `schemas/ghostgate_memory.schema.json`, tests |
| Source validation drift | CLI can validate an existing `source_snapshot.json` and verify WitnessLog event hash | `--validate-snapshot`, `test_validate_source_snapshot_reports_ok_for_generated_snapshot` |
| Evidence bundle incomplete | Bundle now includes `ghostgate.json` as an artifact | `write_bundle_dir`, CLI bundle test |
| Agent handoff contamination | COMMS writer is opt-in and emits hash-only handoff with `web_content_included=false` | `--comms-outbox`, `test_comms_handoff_message_is_hash_only_and_append_only` |
| Regression blind spots | Synthetic fixture corpus covers benign, hidden DOM injection, phishing login and fake source/download/script risks | `tests/fixtures/ai_browser/*.html`, `test_fixture_corpus_covers_expected_risks` |
| Secret-like extracted text leakage | Extracted secret-like strings are redacted and every bundle writes `secret_scan.json` | `test_secret_like_content_is_redacted_and_reviewed` |
| Bundle/COMMS schema drift | New schemas and CLI validators verify bundle, secret scan and COMMS message hashes | `schemas/*source_snapshot_handoff*.json`, `schemas/secret_scan_report.schema.json`, `test_cli_validates_bundle_and_comms_message` |

## Still Blocked By Design

| Risk | Current State | Required Future Gate |
|---|---|---|
| Real network fetch | Not implemented | ActionGate, domain policy, robots/terms/license review, ephemeral browser context |
| Login/manual auth | Not implemented | Manual-auth protocol, credential isolation, user-operated login, no credential storage |
| Downloads | Not implemented | Download quarantine, hash, scan, explicit user approval |
| JS execution | Not implemented | Separate high-risk render mode, sandbox, no secret/profile access |
| Massive scraping | Not implemented | Legal/robots/terms review, per-domain quota, rate limit, ActionGate |
| External publication or account action | Not implemented | Target-specific ActionGate and host gate |
| Argus private/public split | Preserved as boundary | Explicit product/legal/public-safe review |

## Current Verification

```powershell
python -m pytest tests\test_source_snapshot.py -q
```

Expected result after this pass:

```text
13 passed
```
