# Curador SETO Global Operating Contract

Status: `ACTIVE_LOCAL_CONTRACT`

Date: `2026-05-05`

Purpose: convert broad cleanup, duplicate removal and agent handoff work into a
repeatable local protocol. This contract does not authorize direct deletion,
publication, external actions or wholesale source import.

## SETO Folder Protocol

SETO is the local operating layer for dirty or mixed material. The target
folder vocabulary is:

| folder | role | write policy |
|---|---|---|
| `INBOX/` | single entry point for raw incoming material | raw material only; no canon claims |
| `CURADURIA/` | working area for fichas, manifests and review queues | local-only; no release packaging |
| `COMMS/` | agent-to-agent envelopes, handoffs and state packets | append-only or versioned files |
| `evidencia/` | tests, scans, hashes, screenshots and reports | immutable evidence preferred |
| `manifest/` | file manifests, package manifests and hash tables | generated or reviewed artifacts |
| `DELETE_CANDIDATES.md` | removal queue | no deletion without gate |
| `MIGRATION_MAP.md` | movement/rename map | required before any move |
| `WitnessLog` | hash-chain event log | append-only |

These names are contract names first. They may be implemented as physical
folders per project only after a migration map exists. Existing workspace files
remain the source of truth until migration is explicit.

## Epistemic States

| state | meaning | allowed use |
|---|---|---|
| `CERTEZA` | directly observed path, hash, test, scan or file content | can support local decisions |
| `INFERENCIA` | derived interpretation from evidence | can guide backlog, not final truth |
| `INCOGNITA` | not inspected enough or conflicting evidence | cannot be deleted, moved or published |
| `BLOQUEADO` | secret/private/claim/action risk | no external action; no public copy |

Prompts or documents that claim prior audits of repositories, science, public
sources or products are `INFERENCIA` until verified against the actual local or
remote source.

## File Decisions

| decision | required evidence | effect |
|---|---|---|
| `KEEP` | ficha or existing product/canon role | preserve in place |
| `MERGE` | duplicate or related content with a chosen canonical target | prepare migration map |
| `REPLACE_BY_FICHA` | vault/archive can be summarized without losing unique content | create ficha before removal |
| `CANDIDATE_ARCHIVE` | useful history but not active | archive only with map and rollback note |
| `CANDIDATE_DELETE` | generated, exact duplicate or obsolete residue | wait for ActionGate |
| `DELETE_APPROVED_AFTER_HASH` | canonical copy or regenerability proven | deletion allowed in a later cleanup pass |

`INCOGNITA`, private game/TCG, secrets, live customer/product state, book canon
and unique research evidence cannot receive `DELETE_APPROVED_AFTER_HASH`.

## ObservationEnvelope

Every agent handoff or cleanup proposal uses this minimum shape:

```json
{
  "envelope_version": "seto-observation-v1",
  "source_path": "absolute-or-root-relative-path",
  "source_kind": "file|directory|zip|repo|generated_artifact|external_note",
  "sha256": "optional-full-file-hash",
  "size_bytes": 0,
  "evidence": ["test, scan, manifest, line reference or hash"],
  "psi_state": "CERTEZA|INFERENCIA|INCOGNITA|BLOQUEADO",
  "claim_level": "operational|research_only|demo_only|blocked_claim",
  "falsifiers": ["what would disprove or block the claim"],
  "risk_flags": ["secret_like|private_ip|external_action|medical|physics_strong|social_prediction|generated_residue"],
  "action_gate": "APPROVE|REVIEW|BLOCK",
  "decision": "KEEP|MERGE|REPLACE_BY_FICHA|CANDIDATE_ARCHIVE|CANDIDATE_DELETE|DELETE_APPROVED_AFTER_HASH",
  "fingerprint": "stable-event-or-source-fingerprint"
}
```

## ActionGate

ActionGate evaluates the requested action, not only the file.

| gate | conditions |
|---|---|
| `APPROVE` | evidence is complete, no hard risk, action is local and reversible or already proven safe |
| `REVIEW` | evidence is partial, duplicate lineage is unclear, target canon is undecided or generated status is plausible but not proven |
| `BLOCK` | secrets, private IP, game/TCG, strong medical/physics/social claims, publication, external action, data loss risk or unknown source |

Cleanup defaults:

- exact duplicate with canonical copy: `REVIEW` until the canonical path is
  documented, then `DELETE_APPROVED_AFTER_HASH`;
- cache/build/temp with proof of regenerability: `REVIEW`, then possible
  `DELETE_APPROVED_AFTER_HASH`;
- raw `Downloads`, ZIPs, vaults and research prompts: `REVIEW` or `BLOCK`;
- private game/TCG, secrets and external publication: `BLOCK`.

## WitnessLog

WitnessLog is local append-only evidence. Each event records:

- timestamp UTC;
- event type;
- actor/tool;
- input roots;
- outputs written;
- hashes of generated artifacts;
- previous event hash;
- current event hash.

The hash is computed over the canonical JSON event without the `event_hash`
field. If an old log cannot be parsed, the next event must record that as a
`REVIEW` condition rather than rewriting history.

## Agent Communication Protocol

`COMMS/` is a file-based protocol for agents that cannot share live state.

| path | role |
|---|---|
| `COMMS/inbox/<agent>.jsonl` | envelopes waiting for an agent |
| `COMMS/outbox/<agent>.jsonl` | envelopes emitted by an agent |
| `COMMS/agents_state/<agent>.json` | current local state and capabilities |
| `COMMS/topics/<topic>.jsonl` | shared topic stream |
| `COMMS/handoffs/<date>-<agent>.md` | human-readable handoff |

Every message must include an `ObservationEnvelope` or cite one. Agents do not
overwrite another agent's output; they append, supersede by new envelope, or
mark a prior item as blocked with evidence.

## Concurrent Agent Boundaries

When multiple agents are active, SETO treats each lane as owned until a handoff
is written. Current lanes:

| lane | owner responsibility | SETO posture |
|---|---|---|
| Observacionismo language | L0 bit machine, L1 five-verb IR, language tests and falsifiers | read-only until handoff; use only envelopes, tests and hashes |
| Local agent builder | Claudio local-agent contracts, safe execution, repo observation and handoff compiler | read-only until handoff; no write automation without ActionGate |
| Curador SETO | manifests, fichas, duplicate queues, ActionGate, WitnessLog and cleanup evidence | may write only SETO docs/tools/registers |

Coordination artifact:
`docs\developer\SETO_CONCURRENT_AGENT_COORDINATION_2026-05-05.md`.

No agent should broad-stage the workspace, delete another lane's files, or treat
raw `Downloads`/ZIP/prototype material as canon without ficha, hash, claim
state and ActionGate.

## Cleanup Boundaries

Allowed after dry-run and gate:

- duplicate exact copies with the same SHA256 and a chosen canonical copy;
- generated caches and builds: `__pycache__`, `.pytest_cache`, `node_modules`,
  `target`, `dist`, `build`, ignored release residues and temp logs;
- empty folders created by prior generated cleanup, if a result artifact proves
  they are empty and disposable.

Blocked:

- private RPG/TCG/game assets, lore, bridge code and builds;
- full books, canon vaults and unique editorial drafts;
- secrets, sessions, local credentials and browser/auth state;
- ZIPs/packages whose lineage is not documented;
- scientific, medical or social prediction claims without falsifier evidence;
- pushes, deploys, Gumroad, social posting or browser/mouse actions.

## Validation

Implementation passes must produce:

- dry-run inventory manifest;
- duplicate and large-file summary;
- candidate delete/archive table;
- updated ficha/register entries;
- focused secret scan over touched docs/tools;
- valid JSON for generated registers;
- WitnessLog event for the pass.

No pass may claim files were removed unless `DELETED_OR_ARCHIVED.md` and a
result artifact name the exact paths, hashes and gate decision.
