# SETO Duplicate Group Fichas Batch 1 2026-05-05

Status: `REVIEW`. No files were moved, deleted, extracted or published.

This batch converts selected exact-hash duplicate groups into technical fichas.
The equality claim is `CERTEZA` only for the SHA256 match recorded by the
selector. The canonical path remains `INFERENCIA` until the owning lane confirms
source-of-truth lineage.

## Evidence

- Selector report: `docs\intake\SETO_EXACT_DUPLICATE_CANDIDATES_2026-05-05.md`
- Selector JSON:
  `qa_artifacts\release_validation\seto-exact-duplicate-candidates-2026-05-05.json`
- Batch JSON:
  `qa_artifacts\release_validation\seto-duplicate-group-fichas-batch1-2026-05-05.json`
- Source manifest:
  `qa_artifacts\release_validation\global-curador-file-manifest-2026-05-05.csv`

## Batch Summary

| ficha | lane | sha256 | files | state | gate | decision |
|---|---|---|---:|---|---|---|
| `SETO-DUP-B1-001` | Wave FC demo inputs | `88dc4d2132a2b9e2` | 6 | `INFERENCIA` | `REVIEW` | `CANDIDATE_DELETE_AFTER_CANONICAL_CONFIRMATION` |
| `SETO-DUP-B1-002` | Claudio OS blueprint examples | `746f5a28718df9c5` | 4 | `INFERENCIA` | `REVIEW` | `CANDIDATE_DELETE_AFTER_CANONICAL_CONFIRMATION` |
| `SETO-DUP-B1-003` | Claudio OS blueprint examples | `7c715c9f5a758d42` | 4 | `INFERENCIA` | `REVIEW` | `CANDIDATE_DELETE_AFTER_CANONICAL_CONFIRMATION` |
| `SETO-DUP-B1-004` | Asistente Negocio packaging | `1c07945efc4ea394` | 2 | `INFERENCIA` | `REVIEW` | `CANDIDATE_DELETE_AFTER_CANONICAL_CONFIRMATION` |
| `SETO-DUP-B1-005` | Wave FC rollback packs | `956c5dfaafb60ae5` | 10 | `INFERENCIA` | `REVIEW` | `REVIEW_RELEASE_EVIDENCE_BEFORE_DELETE` |
| `SETO-DUP-B1-006` | Claudio OS blueprint examples | `044f93a31daebf3e` | 4 | `INFERENCIA` | `REVIEW` | `CANDIDATE_DELETE_AFTER_CANONICAL_CONFIRMATION` |
| `SETO-DUP-B1-007` | PSI archive redundant vault | `5c7a951213069cd3` | 2 | `INFERENCIA` | `REVIEW` | `REPLACE_BY_FICHA_CANDIDATE_DELETE_AFTER_HASH` |

## Common Gate Rules

- `APPROVE` is not granted by this batch.
- Before deletion: confirm canonical owner, verify every path still has the same
  SHA256, update `DELETE_CANDIDATES.md`, run secret scan on touched docs/scripts,
  and create a deletion log entry.
- Falsifier: if any candidate path changes hash, becomes a package-required
  fixture, or is claimed by another active agent as canonical, this ficha returns
  to `REVIEW`.
- Blockers: secrets, private assets, release evidence, medical/physical/social
  claims, publication or external actions remain `BLOQUEADO`.

## Fichas

### SETO-DUP-B1-001 Wave FC demo input: sales_summary.csv

- SHA256:
  `88dc4d2132a2b9e2b2ec1f63d3aee4179119589d7bdac448392c08e83278747b`
- Exact-hash state: `CERTEZA`.
- Canonical path state: `INFERENCIA`.
- Proposed canonical:
  `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_fc_client_demos\wave_fc_client_demo_2026-04-30\inputs\sales_summary.csv`
- Duplicate candidates:
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_fc_client_demos\wave_fc_evidence_pack_2026-05-01\inputs\sales_summary.csv`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_wabi_release_gates\smoke_gate_2026-04-30\demo_packages\client_demo\inputs\sales_summary.csv`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_wabi_release_gates\wave_wabi_gate_2026-05-01\demo_packages\client_demo\inputs\sales_summary.csv`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_wabi_release_gates\wave_wabi_release_gate_2026-04-30-public-nrp-refresh\demo_packages\client_demo\inputs\sales_summary.csv`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_wabi_release_gates\wave_wabi_release_gate_2026-04-30\demo_packages\client_demo\inputs\sales_summary.csv`
- Decision: keep all paths for now; prepare for later duplicate cleanup after
  Wave FC evidence-pack lineage is mapped.

### SETO-DUP-B1-002 Claudio OS example: decision_safe.json

- SHA256:
  `746f5a28718df9c58f65665ad753df1062c6f6cf2b7240b14eb7f451f25797fc`
- Exact-hash state: `CERTEZA`.
- Canonical path state: `INFERENCIA`.
- Proposed canonical:
  `packages\open-dev\claudio-os-blueprint\examples\decision_safe.json`
- Duplicate candidates:
  - `-=MEDIOEVO=-\-=LIBROS\claudio\_workspace\claudio_os_blueprint\examples\decision_safe.json`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\claudio_os_build\staging\claudio_os_blueprint\examples\decision_safe.json`
  - `PRODUCTOS_MEDIOEVO\claudio_os_blueprint\examples\decision_safe.json`
- Decision: proposed open-dev package copy is likely canonical, but Claudio OS
  owner must confirm before any staged/runtime copy is deleted.

### SETO-DUP-B1-003 Claudio OS example: decision_publish_requires_approval.json

- SHA256:
  `7c715c9f5a758d429505419b690b6cb191191b42517f7ac0d1bf3a8c5d323ea4`
- Exact-hash state: `CERTEZA`.
- Canonical path state: `INFERENCIA`.
- Proposed canonical:
  `packages\open-dev\claudio-os-blueprint\examples\decision_publish_requires_approval.json`
- Duplicate candidates:
  - `-=MEDIOEVO=-\-=LIBROS\claudio\_workspace\claudio_os_blueprint\examples\decision_publish_requires_approval.json`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\claudio_os_build\staging\claudio_os_blueprint\examples\decision_publish_requires_approval.json`
  - `PRODUCTOS_MEDIOEVO\claudio_os_blueprint\examples\decision_publish_requires_approval.json`
- Decision: same as B1-002; keep pending Claudio OS owner confirmation.

### SETO-DUP-B1-004 Asistente Negocio packaging: build-macos.sh

- SHA256:
  `1c07945efc4ea394fb091e88d7ac781330b9c8719b922846fb1f560c9d988ea8`
- Exact-hash state: `CERTEZA`.
- Canonical path state: `INFERENCIA`.
- Proposed canonical:
  `apps\commercial\asistente-negocio\packaging\build-macos.sh`
- Duplicate candidate:
  - `-=MEDIOEVO=-\-=LIBROS\claudio\products\asistente_negocio\packaging\build-macos.sh`
- Decision: keep both until the commercial app lane confirms whether
  `apps\commercial\asistente-negocio` is the maintained product root.

### SETO-DUP-B1-005 Wave FC rollback pack: RESTORE.md

- SHA256:
  `956c5dfaafb60ae58739ee0efb188991930b7f7007a78e6e978faa18984706d6`
- Exact-hash state: `CERTEZA`.
- Canonical path state: `INFERENCIA`.
- Proposed canonical:
  `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_fc_client_demos\wave_fc_client_demo_2026-04-30\runs\20260430_042318_acme_case_2a9b713e65\rollback_pack\RESTORE.md`
- Duplicate candidates:
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_fc_client_demos\wave_fc_evidence_pack_2026-05-01\runs\20260501_123821_acme_case_2a9b713e65\rollback_pack\RESTORE.md`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_fc_client_demos\wave_fc_evidence_pack_2026-05-01\runs\20260501_123821_operations_brief_d5f6877377\rollback_pack\RESTORE.md`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_function_collapse\docx_qa_smoke\runs\20260429_223453_wave_docx_smoke_source_ff7528fec4\rollback_pack\RESTORE.md`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_function_collapse\runs\20260429_221036_WAVE_DOCUMENT_COLLAPSE_CLI_2026-04-29_10a3dffc2a\rollback_pack\RESTORE.md`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_wabi_release_gates\smoke_gate_2026-04-30\demo_packages\client_demo\runs\20260430_043030_acme_case_2a9b713e65\rollback_pack\RESTORE.md`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_wabi_release_gates\wave_wabi_gate_2026-05-01\demo_packages\client_demo\runs\20260501_124009_acme_case_2a9b713e65\rollback_pack\RESTORE.md`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_wabi_release_gates\wave_wabi_gate_2026-05-01\demo_packages\client_demo\runs\20260501_124009_operations_brief_336102c90d\rollback_pack\RESTORE.md`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_wabi_release_gates\wave_wabi_release_gate_2026-04-30-public-nrp-refresh\demo_packages\client_demo\runs\20260430_045303_acme_case_2a9b713e65\rollback_pack\RESTORE.md`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\wave_wabi_release_gates\wave_wabi_release_gate_2026-04-30\demo_packages\client_demo\runs\20260430_043051_acme_case_2a9b713e65\rollback_pack\RESTORE.md`
- Decision: stricter `REVIEW`; rollback packs may be historical evidence even
  when identical. Do not delete before the Wave FC release-evidence map exists.

### SETO-DUP-B1-006 Claudio OS example: decision_browser_blocked.json

- SHA256:
  `044f93a31daebf3e243a3acfdb74156153830bd1309510f3540ef811f63a0a73`
- Exact-hash state: `CERTEZA`.
- Canonical path state: `INFERENCIA`.
- Proposed canonical:
  `packages\open-dev\claudio-os-blueprint\examples\decision_browser_blocked.json`
- Duplicate candidates:
  - `-=MEDIOEVO=-\-=LIBROS\claudio\_workspace\claudio_os_blueprint\examples\decision_browser_blocked.json`
  - `-=MEDIOEVO=-\-=LIBROS\claudio\runtime\claudio_os_build\staging\claudio_os_blueprint\examples\decision_browser_blocked.json`
  - `PRODUCTOS_MEDIOEVO\claudio_os_blueprint\examples\decision_browser_blocked.json`
- Decision: keep pending Claudio OS owner confirmation.

### SETO-DUP-B1-007 PSI redundant vault template: NEXT_SESSION_BRIEF.md

- SHA256:
  `5c7a951213069cd31f6ecda115fe00789cb380ce63a51c296bbbb765ea928b7b`
- Exact-hash state: `CERTEZA`.
- Canonical path state: `INFERENCIA`.
- Proposed canonical:
  `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\archive\templates\NEXT_SESSION_BRIEF.md`
- Duplicate candidate:
  - `-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-\-=PSI=-\archive\vault_redundante_2026-04-26\templates\NEXT_SESSION_BRIEF.md`
- Decision: replace redundant vault copy by ficha only after PSI owner confirms
  `archive\templates` is the canonical template root and no session handoff
  points to the redundant vault path.

## Next Actions

1. Confirm owning lane for Wave FC, Claudio OS, Asistente and PSI.
2. Refresh SHA256 before any cleanup execution.
3. Add approved rows to `DELETE_CANDIDATES.md` only after owner confirmation.
4. Write `DELETED_LOG` entries only when deletion actually occurs.
