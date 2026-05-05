# SETO Concurrent Agent Coordination

Status: `ACTIVE_COORDINATION_CONTRACT`

Date: `2026-05-05`

Purpose: keep the current multi-agent run coherent while separate agents work
on the Observacionismo language layer and the local-code-agent layer. This
document is a coordination envelope only. It does not import, overwrite, stage
or approve the concurrent agents' files.

## Observed Concurrent Work

| lane | observed artifact | sha256 | state | decision |
|---|---|---|---|---|
| language | `docs\developer\OBSERVACIONISMO_MINIMAL_MACHINE_LANGUAGE_2026-05-05.md` | `5E4F04AC5FC91CD9AC3A8855E0B1D4F1B5E44FEF32D88C5C9D5952E4A3CA6185` | `CERTEZA` | `READ_ONLY_CONCURRENT_OWNER` |
| language intake | `docs\intake\OBSERVACIONISMO_LANGUAGE_DOWNLOADS_PSI_INTAKE_2026-05-05.md` | `60635C6E9B29A948FC68736F4EBDE01D206C5E34540F74254E3E70A81F8C5316` | `CERTEZA` | `READ_ONLY_CONCURRENT_OWNER` |
| language evidence | `qa_artifacts\observacionismo_language\observacionismo_language_inventory_2026-05-05.json` | `0560040C8F7255FD80F3DA6E982C89312747971168C1E9E44AD04FC68C4D5EAB` | `CERTEZA` | `READ_ONLY_EVIDENCE` |
| language test | `qa_artifacts\observacionismo_language\obs_bit_machine_pytest_2026-05-05.txt` | `B5D6E93EDFEF9651EA8FE2D85E7703637CF819791AB0E790872B49799E89A013` | `CERTEZA` | `READ_ONLY_EVIDENCE` |
| local agent intake | `docs\intake\OBSERVACIONISTA_LOCAL_CODE_AGENT_INTAKE_2026-05-04.md` | `57967DDC6E95B192529BB70FF8B52DFE8DA7C0B35ED6CEE6EF3D3DCFB4DF82E8` | `CERTEZA` | `READ_ONLY_CONCURRENT_OWNER` |

## Ownership

| agent lane | owns | may touch | must not touch |
|---|---|---|---|
| Language agent | Observacionismo L0/L1/L2 language design, `ObsBitMachine`, language inventory and tests | `research\observacionismo-lab`, `qa_artifacts\observacionismo_language`, language docs | cleanup/delete registers, release packaging, local-agent automation |
| Local-agent builder | conversational local agent, RepoObserver/SymbolGraph/PatchPlanner/SafeExecutor contract, Claudio local chat/workpacks | Claudio-local agent tools and tests after ActionGate | language VM internals, SETO cleanup gates, public release actions |
| Curador SETO | manifests, fichas, duplicate queues, ActionGate, WitnessLog, coordination and cleanup evidence | `docs\developer\CURADOR_SETO_*`, SETO reports, `tools\release\*seto*`, intake/register files | concurrent language/local-agent source files unless explicitly handed off |

## Integration Contract

Language output may enter SETO only as:

- `ObservationEnvelope` schemas and state-transition tests.
- L1 verb definitions: `OBSERVAR`, `DOCUMENTAR`, `VERIFICAR`, `ACTUAR`,
  `HANDOFF`.
- Falsifiers for claims and residue measurement.

Local-agent output may enter SETO only as:

- Repo observation and patch-planning contracts.
- Safe execution policies.
- WitnessLog append events.
- HandoffCompiler output that references evidence, not chat-only memory.

SETO output enters both lanes as:

- source hashes, fichas and cleanup decisions;
- `ActionGate` results;
- duplicate/canonical review queues;
- blockers for private, secret, publication, medical, physics or social claims.

## Hard Boundaries

- No agent broad-stages the workspace.
- No agent deletes, moves, extracts ZIPs, publishes or pushes from another lane.
- No `Downloads` source becomes canon without ficha, hash, claim state and
  ActionGate.
- No local-agent prototype is treated as autonomous code editor until security
  review and tests cover write actions.
- No language document is treated as executable truth until tests enforce the
  semantics.

## Current Queue Split

| queue | current state | next safe action |
|---|---|---|
| language | `LOCAL_RESEARCH_DRAFT`; 3 local tests reported passed | let language agent continue parser L1; SETO reads only after committed or handed off |
| local agent | `SELECTIVE_ABSORPTION_DONE / RAW_SOURCE_NOT_CANON` | let local-agent builder continue Claudio-local implementation; SETO keeps deletion blocked |
| SETO | global dry audit, cache cleanup and exact duplicate selector committed | create fichas for selected duplicate groups before any delete |

## ObservationEnvelope

```json
{
  "envelope_version": "seto-observation-v1",
  "source_path": "multi-agent workspace",
  "source_kind": "coordination_contract",
  "sha256": "see observed artifact table",
  "size_bytes": 0,
  "evidence": [
    "observed language artifacts with hashes",
    "observed local-agent intake with hash",
    "existing SETO global audit and duplicate selector"
  ],
  "psi_state": "CERTEZA",
  "claim_level": "operational",
  "falsifiers": [
    "a concurrent agent changes ownership without handoff",
    "a lane stages or deletes another lane's files",
    "an artifact is used as canon without ficha/hash/gate"
  ],
  "risk_flags": [
    "concurrent_work",
    "raw_downloads",
    "local_agent_write_risk",
    "language_runtime_claims"
  ],
  "action_gate": "REVIEW",
  "decision": "KEEP_COORDINATION_BOUNDARY",
  "fingerprint": "SETO_CONCURRENT_AGENT_COORDINATION_2026-05-05"
}
```
