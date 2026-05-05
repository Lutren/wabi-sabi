# SETO Observacionismo Decision Learning 2026-05-05

Status: local contract for Claudio/Wabi-Sabi. This is not model training and
does not grant external action.

The purpose is to let Claudio learn operational judgment from SETO evidence:
observe, classify, gate, act locally only when justified, then record residue.

## Principle

Claudio should not learn from raw theory as if it were truth. It should learn
from decision envelopes that include evidence, falsifiers, risk, action gate and
post-validation.

## Decision Envelope

Required fields:

| field | role |
|---|---|
| `case_id` | stable local identifier |
| `observation` | what was observed, with paths and hashes when relevant |
| `psi_state` | `CERTEZA`, `INFERENCIA`, `INCOGNITA` or `BLOQUEADO` |
| `action_gate` | `APPROVE`, `REVIEW` or `BLOCK` |
| `risk_flags` | secrets, private IP, external action, publication, claims, data loss |
| `falsifiers` | facts that would reverse the decision |
| `decision` | action or non-action |
| `post_validation` | proof after action, or reason no action was taken |
| `residue` | what remains unresolved |

## Patterns Learned From SETO

| pattern | gate | lesson |
|---|---|---|
| exact duplicate + canonical hash verified + no active references | `APPROVE` | local deletion can proceed with `DELETED_LOG`, `MIGRATION_MAP`, result JSON and WitnessLog |
| exact duplicate group but canonical owner unclear | `REVIEW` | create ficha first, do not delete |
| hash transcription mismatch | `REVIEW` | fix evidence before action; never act on partial hash confidence |
| residual unmatched vault files | `REVIEW` | preserve unique material until canonical replacement or keep decision exists |
| generated cache with workspace containment and approved names | `APPROVE` | delete regenerable residue, then verify absence |
| concurrent language/local-agent lane | `REVIEW` | read-only until handoff; no broad staging |
| secrets/private game/publication/strong claims | `BLOCK` | no local optimization can bypass boundary |

## Claudio Rule

When Claudio is unsure, it should prefer:

1. create or update ficha;
2. record hash and evidence;
3. assign `REVIEW`;
4. leave the file untouched;
5. emit a handoff envelope.

`APPROVE` requires all of: local-only action, canonical proof, no boundary
flags, result artifact, and post-validation.

## Dataset

Machine-readable examples:
`qa_artifacts\release_validation\seto-observacionismo-decision-examples-2026-05-05.jsonl`.
