# OSIT Observer Kernel Local Gate Fix - 2026-05-06

Status: local closure with evidence. No external action, no model alias mutation,
no browser/tool execution and no publication.

## Scope

- `tools/observacionismo/osit_observer_kernel.py`
- `tests/test_osit_observer_kernel.py`
- `configs/ollama/Modelfile.observador`
- Curador fichas for the source materials under
  `docs/intake/curador_fichas/downloads/`

## Source Boundary

The source materials were already classified by Curador SETO as `ARCHIVO_FRIO`
with `ActionGate=REVIEW`:

- `8016127A31A8E330_osit_observer_kernel.md`
- `55A7E980BDBD5B3E_readme_osit_observer.md`
- `82B77221A430CAF1_osit_qg_observacionismo.md`

The operational extraction remains local and low-claim. It must not be treated
as proof of OSIT-QG physics, autonomous execution safety, or publication
readiness.

## Fix

Initial test evidence showed `browser.goto` to an allowed read-only domain was
incorrectly classified as `APPROVE` because the `review_action` risk increment
was lower than `max_risk_approve`.

The kernel now:

- keeps `request_confirmation` in `review_actions`;
- forces any `review_action` to score above the approval threshold;
- leaves blocked actions, credentials, payment, privilege and scan attempts at
  `BLOCK`;
- records an `ObservationEnvelope`;
- reports `tool_executed=false`.

## Evidence

Commands executed from workspace root:

```powershell
python -m pytest tests\test_osit_observer_kernel.py -q
python -m py_compile tools\observacionismo\osit_observer_kernel.py
python tools\observacionismo\osit_observer_kernel.py audit --action-json '{"action":"browser.goto","target":"https://wikipedia.org/wiki/Observability","reason":"read source"}'
python tools\observacionismo\osit_observer_kernel.py audit --action-json '{"action":"payment.submit","target":"checkout","value":"card"}'
```

Observed results:

- `7 passed in 0.44s`
- `py_compile` passed
- `browser.goto` result: `action_gate=REVIEW`, `risk=0.3`,
  `tool_executed=false`
- `payment.submit` result: `action_gate=BLOCK`, `risk=1.0`,
  `tool_executed=false`

Host gate recheck from Claudio:

- timestamp: `2026-05-06T12:11:42Z`
- host status: `MIXTO`
- host gate: `REVIEW`
- reason: `residuo_precaucion`
- memory: `73.9%`
- disk: `80.4%`

## Gate Boundary

This closes only the local deterministic gate bug. It does not unlock:

- Qwen/Gemma heavy suites;
- Ollama alias creation;
- WSL ISO build or QEMU boot;
- browser automation against real accounts;
- Gumroad, LinkedIn, social, website or Git publication;
- customer ZIP/installers;
- credential, payment or destructive execution.

The next allowed work remains local, reversible and evidence-backed unless a
target-specific ActionGate reaches `APPROVE`.
