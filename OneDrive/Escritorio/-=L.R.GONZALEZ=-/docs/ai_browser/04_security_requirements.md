# AI Browser Seguro - 04 Security Requirements

Status: `BASELINE_REQUIREMENTS`

## Hard Requirements

| ID | Requirement |
|---|---|
| SEC-001 | Web content must be treated as untrusted data. |
| SEC-002 | Web-origin instructions must be stored separately from user/system instructions. |
| SEC-003 | JavaScript execution is disabled by default. |
| SEC-004 | No persistent cookies, cache, local storage or browser profile by default. |
| SEC-005 | No credentials, password capture, token capture or credential storage. |
| SEC-006 | Login automation is prohibited unless future manual-auth gate defines a narrow flow. |
| SEC-007 | Forms, submit, click, upload and account actions are blocked by default. |
| SEC-008 | Downloads are blocked by default; future downloads go to quarantine with hash and scan. |
| SEC-009 | Remote URL fetch requires ActionGate and domain policy. |
| SEC-010 | Massive scraping is prohibited without legal/robots/terms review and explicit gate. |
| SEC-011 | Every capture creates SourceSnapshot with raw and extracted hashes. |
| SEC-012 | Every action proposal creates a WitnessLog or equivalent local receipt. |
| SEC-013 | Hidden DOM text is separated and flagged. |
| SEC-014 | Prompt injection patterns produce `REVIEW`, not execution. |
| SEC-015 | Private Argus/game/TCG/editorial sources cannot enter public bundles. |
| SEC-016 | Public/browser code must not include real tokens, cookies, profiles or account data. |

## Domain Permission Model

Each domain record should include:

- domain pattern;
- allowed modes: `read_only`, `fetch`, `screenshot`, `action`;
- disallowed selectors/actions;
- robots/terms status;
- data license status;
- rate/quota;
- requires manual auth: true/false;
- ActionGate state;
- last SourceSnapshot hash.

MVP implementation:

- machine schema: `schemas/domain_policy.schema.json`;
- `tools/ai_browser/snapshot_url.py --url https://...` requires both
  `--gate-file` and `--domain-policy`;
- matching domain policy must include `read_only` and ActionGate `APPROVE`;
- `allow_javascript`, `allow_downloads`, `allow_forms`, `allow_login` and
  `allow_credentials` must remain false.

## Download Quarantine Model

Future downloads require:

- explicit user intent;
- ActionGate `APPROVE`;
- domain policy allows downloads;
- destination is quarantine, not normal Downloads;
- SHA256 before use;
- size/MIME/extension recorded;
- malware/secret scan where available;
- no execution from quarantine.

## Secret Handling

- Do not read `.env`, token files, browser profiles, session stores or password
  managers as browser sources.
- Secret-like content in a source is evidence of risk, not permission to expose
  it.
- Evidence bundles must not include credentials or cookie jars.

## Memory Safety

Before a snapshot enters durable memory:

1. SourceSnapshot hash exists.
2. `web_instruction` channel is separated.
3. Prompt-injection flags are reviewed.
4. GhostGate checks whether the content can contaminate canon or agent policy.
5. COMMS message cites the snapshot, not raw web authority.

MVP implementation:

- machine schema: `schemas/ghostgate_memory.schema.json`;
- each SourceSnapshot includes `ghostgate`;
- `ghostgate.memory_allowed=false` whenever the snapshot has external URL,
  hidden DOM, prompt-injection, form/login/download/script or secret-like risk.
