# Observacionismo Lab

Status: `LOCAL_RESEARCH_HARNESS`

This lab tests whether model rankings survive declared observer/proxy
transformations. It is not a physics proof and not publication evidence by
itself.

## Current Purpose

- import the local PSI Chi engine (`psi_chi_lab_v9.py`);
- generate synthetic rotation-curve universes;
- apply low-claim observer/proxy transformations;
- run model leaderboards;
- report winner stability and delta BIC margins.

## Safety Boundary

Allowed:

- local synthetic falsifier runs;
- SPARC-related analysis only when dataset citation and claim boundary are
  included;
- AI-engineering extraction into Claudio as a method for claims, sources and
  agent actions.

Blocked:

- claims that RAR, MOND, PSI Chi or any physics theory is proved;
- claims that Sensorium proxies are real electromagnetic, thermal or magnetic
  measurements;
- public release of raw Downloads code or private DUAT Geodia material.

## Smoke Command

```powershell
python research\observacionismo-lab\observacionismo_lab.py demo --truth rar --galaxies 6 --samples 80 --out qa_artifacts\research\observacionismo_lab_demo_2026-05-03.json
```

## Observer Profiles

- `visual_proxy`: visual-style mask with radial inversion, imputation and
  outer-radius uncertainty.
- `component_split_proxy`: gas/disk/bulge component split proxy.
- `phase_proxy`: curve-shape proxy with light velocity quantization.
- `instrument_balanced`: baseline with no deliberate distortion.
- `scientific_community`: conservative peer-review proxy with uncertainty
  inflation and no imputed evidence.
- `adversarial_observer`: stress-test proxy that drops some outer-radius
  evidence, perturbs radii and adds measurement noise.

## Negative Controls

Use `--control` to test whether the harness is finding a real model/data link
or just rewarding a shape bias.

```powershell
python research\observacionismo-lab\observacionismo_lab.py demo --truth rar --control shuffled_baryons --profiles instrument_balanced,scientific_community,adversarial_observer
```

Controls:

- `none`: normal synthetic data.
- `shuffled_baryons`: preserve observed velocities but shuffle baryonic
  components across points.
- `shuffled_velocities`: preserve baryonic components but shuffle observed
  velocities and errors.

Outputs include `winner_rate`, `mean_margin_to_second_delta_bic` and
`rank_stability`. A strong model surviving a broken control should be treated
as a bias warning, not a success.

## Residuals And Held-Out Galaxies

Use `--heldout-frac` to tune on a subset of galaxies and report residuals on
held-out galaxies:

```powershell
python research\observacionismo-lab\observacionismo_lab.py demo --truth rar --heldout-frac 0.2 --profiles instrument_balanced,scientific_community,adversarial_observer
```

Each profile reports:

- `residual_signature`: normalized residual RMS, mean absolute residual,
  radial bias and low-vs-high acceleration bias.
- `heldout_report`: train winner, held-out galaxies and held-out residual
  signature.

## Selftest

```powershell
python research\observacionismo-lab\observacionismo_lab.py selftest --out qa_artifacts\research\observacionismo_lab_selftest_2026-05-03.json
```

The selftest runs one normal synthetic audit and one `shuffled_baryons` negative
control. It validates code paths only; it is not physics evidence.
