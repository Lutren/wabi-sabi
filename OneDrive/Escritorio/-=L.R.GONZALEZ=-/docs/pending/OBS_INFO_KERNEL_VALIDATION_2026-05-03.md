# Obs Info Kernel Validation - 2026-05-03

Status: internal validation on sanitized local corpus. This is not public copy
and does not validate new physics, consciousness, medicine, finance or security
claims.

## Corpus

The corpus was copied into
`qa_artifacts/obs_info_kernel_validation_2026-05-03/corpus/` from already
curated/sanitized local docs:

| file | role |
|---|---|
| `OBS_INFO_KERNEL_REVIEW_2026-05-01.md` | internal technical review |
| `OBS_EOR_AIA_TOPOLOGY_REVIEW_2026-05-01.md` | EOR/AIA/topology review |
| `OBS_ANTIGRAVITY_RUNTIME_REVIEW_2026-05-01.md` | runtime review |
| `OBS_INFO_KERNEL_README.md` | kernel boundary and module map |

No raw Downloads source, private RPG/TCG material, family data, credentials or
commercial secrets were copied into this validation corpus.

## Command

```powershell
cd research\obs-info-kernel
python -m obs_info_kernel.cli --corpus "..\..\qa_artifacts\obs_info_kernel_validation_2026-05-03\corpus" --query "EOR graph proxy K_source Operator Atlas anti-informacion claims boundary" --out-dir "..\..\qa_artifacts\obs_info_kernel_validation_2026-05-03\out" --min-coverage 0.34
```

## Result

| metric | value |
|---|---:|
| run_status | OK |
| source_count | 4 |
| R | 0.5319 |
| Phi_eff | 0.1135 |
| regimen | JAMMING_TEMPRANO |
| operator_profiles | 4 |
| mean_r_source | 0.5909 |
| topology_status | OPERATIONAL_PROXY_NOT_PROOF |
| topology_edges | 6 |
| top_findings | 19 |

Artifacts:

- `qa_artifacts/obs_info_kernel_validation_2026-05-03/out/observacionismo_research_report.md`
- `qa_artifacts/obs_info_kernel_validation_2026-05-03/out/observacionismo_research_report.json`
- `qa_artifacts/obs_info_kernel_validation_2026-05-03/out/SESSION_FINGERPRINT.json`
- `qa_artifacts/obs_info_kernel_validation_2026-05-03/out/NEXT_SESSION_BRIEF.md`

## C_ij Edges

| left | right | C_ij | shared operators |
|---|---|---:|---|
| OBS_ANTIGRAVITY_RUNTIME_REVIEW_2026-05-01.md | OBS_INFO_KERNEL_README.md | 0.5175 | continuidad, distorsion, umbral |
| OBS_EOR_AIA_TOPOLOGY_REVIEW_2026-05-01.md | OBS_INFO_KERNEL_REVIEW_2026-05-01.md | 0.4855 | oscuridad, umbral |
| OBS_INFO_KERNEL_README.md | OBS_INFO_KERNEL_REVIEW_2026-05-01.md | 0.4710 | calibracion, oscuridad, umbral |
| OBS_EOR_AIA_TOPOLOGY_REVIEW_2026-05-01.md | OBS_INFO_KERNEL_README.md | 0.3363 | operador, oscuridad, umbral |
| OBS_ANTIGRAVITY_RUNTIME_REVIEW_2026-05-01.md | OBS_EOR_AIA_TOPOLOGY_REVIEW_2026-05-01.md | 0.1761 | umbral |
| OBS_ANTIGRAVITY_RUNTIME_REVIEW_2026-05-01.md | OBS_INFO_KERNEL_REVIEW_2026-05-01.md | 0.1661 | umbral |

## Closure Interpretation

Closed locally:

- EOR graph proxy has a traceable internal-corpus run with explicit source
  count, `R`, `Phi_eff`, regime, artifacts and fingerprint.
- `K_source` / Operator Atlas has a traceable internal-corpus run with 4
  profiles, mean source residue and `C_ij` topology.

Still not closed for publication:

- no primary-source scientific validation;
- no licensed external corpus audit;
- no product/open-dev release gate;
- no claims that the topology proves equivalence, consciousness or physics.

Next scientific step would be a larger licensed corpus with frozen source
manifest and expected falsifiers.
