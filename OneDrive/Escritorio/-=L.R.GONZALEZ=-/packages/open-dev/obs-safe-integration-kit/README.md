# OBS Safe Integration Kit

Kernel local-first para integrar tecnología observacionista con proyectos de agentes sin riesgo operacional.

## Qué incluye

- `ObservationEnvelope`: formato universal para observaciones.
- `EstadoPSI`: R, Phi_eff, J_c, epsilon, régimen y fingerprint.
- `ActionGate`: compuerta pre-ejecución. No ejecuta nada.
- `EvidenceStore`: SQLite con observaciones, claims, acciones, sesiones y hash-chain.
- Adaptadores:
  - `GPTResearcherObserver`
  - `SWEAgentObserver`
  - `BrowserUseObserver`
  - `AegisBridge`

## Principios de seguridad

1. Dry-run por defecto.
2. No red, no browser action, no shell execution desde este paquete.
3. Bloquea secretos, `.env`, `credentials.json`, `.ssh`, comandos destructivos y `curl | bash`.
4. Acciones con efecto externo van a `HUMAN_REVIEW`.
5. Todo queda registrado en SQLite con hash-chain.

## Instalación local

```bash
cd obs-safe-integration-kit
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m pytest -q
```

## CLI

```bash
obs-safe --db demo.sqlite observe-text --source manual --title "nota" --text "ActionGate antes de ejecutar herramientas"
obs-safe --db demo.sqlite gate-action --tool shell --intent "ejecutar pruebas" --args-json '{"command":"pytest -q"}' --shell
obs-safe --db demo.sqlite status
```

## Flujo seguro de integración

```text
fork/clone local
  ↓
no tokens / no push / no prod
  ↓
insertar wrapper observacionista
  ↓
registrar ObservationEnvelope
  ↓
calcular R / Phi_eff / epsilon
  ↓
ActionGate dry-run
  ↓
EvidenceStore + SessionFingerprint
  ↓
tests locales
```

## Targets recomendados

1. AEGIS-like firewall: agregar EstadoPSI y SessionFingerprint.
2. GPT Researcher: claim registry + evidence receipts antes de `write_report()`.
3. Browser-use: snapshot primero; clicks/uploads/eval pasan por ActionGate.
4. SWE-agent / mini-SWE-agent: gate por patch/test/command y claims por traceback/test.
5. Agent Laboratory / AI Scientist: gates por fase y drift entre ideación, experimento y escritura.

## Límite honesto

Esto no prueba una nueva teoría física. Es ingeniería operacional: reduce acciones peligrosas, pérdida de contexto, claims sin evidencia y drift entre intención y ejecución.

## Documentos de release

- `CLAIMS.md`: claims permitidos, demo-only y bloqueados.
- `PRIVATE_EXCLUSIONS.md`: fronteras privadas que no entran al paquete.
- `SECURITY.md`: postura local-first y manejo de secretos.
- `RELEASE_CHECKLIST.md`: gate previo a cualquier publicacion externa.
- `QA_RESULTS.md`: evidencia local de pruebas, smoke y scans.
