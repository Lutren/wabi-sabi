# Wabi Observation Claim Adapter - 2026-05-21

## Estado

- Adapter local proposal-only creado.
- Consume `obsai-core` `ClaimClassifier` y su `ObservationEnvelope v2.1`.
- No ejecuta cambios, no aplica TaskSpec, no llama cloud y no publica.

## Archivos

- `wabi_sabi/core/observation_claim_adapter.py`
- `tests/test_observation_claim_adapter.py`
- CLI: `claim-observation`, `claim-adapter`, `claim-fixtures`.

## Evidencia

- `python -B -m pytest tests/test_observation_claim_adapter.py -q -p no:cacheprovider`
  -> `3 passed in 1.87s`.
- `python -B -m pytest tests/test_observation_claim_adapter.py tests/test_hypothesis_packet.py -q -p no:cacheprovider`
  -> `8 passed in 3.03s`.
- `python -B -m py_compile wabi_sabi\core\observation_claim_adapter.py wabi_sabi\cli\main.py tests\test_observation_claim_adapter.py`
  -> PASS.
- Fixture real de 12 claims despues de calibracion:
  `case_count=12`, `pass_count=12`, `review_count=0`, `status=PASS`.

## Interpretacion

El adapter funciona y preserva gates. La calibracion DEMO_ONLY de
`ClaimClassifier` ahora respeta los 12 fixtures canonicos OSIT/Wabi, sin
convertir esos labels en claims cientificos externos.

## Fronteras

- `cloud_provider_called=false`.
- `applied_to_sources=false`.
- `publication_gate=BLOCK`.
- No push, deploy, publicacion ni importacion runtime.
