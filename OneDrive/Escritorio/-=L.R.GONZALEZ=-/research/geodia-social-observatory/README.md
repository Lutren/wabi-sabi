# GEODIA Social Observatory

Estado: MVP local privado / research-only.

GEODIA Social Observatory simula epocas y cambios sociales desde snapshots
trazables. No predice resultados garantizados y no autoriza publicacion externa.
El flujo v1 es:

1. fuente allowlist -> snapshot con hash, fecha, licencia y rol;
2. normalizacion de indicadores/eventos;
3. modelo de epoca con DUAT, especialistas Conway y gate de Observacionismo;
4. reporte con evidencia por claim, incertidumbres y backtest offline.

## Contratos

- `claudio.social_source_snapshot.v1`
- `claudio.social_epoch_model.v1`
- `claudio.social_scenario_report.v1`
- `motor.duat_v2_intake.v1`

## Fuentes allowlist v1

- World Bank Indicators API
- IMF Data APIs
- OECD API
- Eurostat SDMX API
- FRED API
- Our World in Data Grapher API
- GDELT DOC 2.0

Notas de seguridad:

- GDELT solo cuenta como senal mediatico-narrativa, no como hecho social bruto.
- FRED requiere API key y aviso de no-endoso antes de uso live.
- OWID requiere revisar la licencia del proveedor original por dataset.
- El MVP no hace fetch de red: `--offline` es obligatorio.

## Uso local

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\research\geodia-social-observatory"
python -m geodia_social_observatory.cli intake --pretty
python -m geodia_social_observatory.cli signature --text "Observo evidencia porque quizas conviene pedir otra prueba?" --pretty
python -m geodia_social_observatory.cli route --features-json "{\"uncertainty\":0.7,\"impact\":0.8}" --pretty
python -m geodia_social_observatory.cli simulate-duat --seed 7 --size 12 --steps 5 --pretty
python -m geodia_social_observatory.cli duat-v2-intake --pretty
python -m geodia_social_observatory.cli run --offline --fixture fixtures\social_epoch_fixture.json --pretty
python -m geodia_social_observatory.cli backtest --offline --fixture fixtures\social_epoch_fixture.json --pretty
python -m pytest tests -q
```

## Separacion funcional/laboratorio

- Funcional: intake con SHA256, event store JSONL, artifact graph, router
  `cache/small/strong/sim/human`, firma conductual como riesgo continuo,
  salud DUAT y simulacion DUAT/Conway deterministica.
- Laboratorio: Gemma 4, LoRA/QLoRA, MoE surgery, ADEPT/CLaSp/MoR/SWIFT/MTP,
  world models entrenados, despliegues GPU/cloud y claims cientificos.
- Bloqueo: ningun archivo bruto de `Downloads` se copia al motor; solo se
  destilan contratos, tests y reglas con hashes de origen.

## Intake DUAT v2 2026-05-01

Los archivos `deep-research-report (4).md`, `Esto es material
extraordinariament.txt`, `duat_v2.html` y `deep-research-report (5).md` quedan
registrados como material local privado con SHA256. Lo funcional que entra ahora
es: frontera entre verdad
ultima y adecuacion operacional, separacion fenomeno/observacion/accion, grafo
de artefactos con `supports`, `contradicts` y `verified_by`, vocabulario de
fases DUAT, forma de simulacion offline seeded, roadmap DUAT de tres carriles,
maquina de eventos y frontera de identidad conductual continua.

Queda en laboratorio privado: dashboard DUAT v2, puente EEG, memoria
conformacional, visualizaciones fractales, Mesa/PettingZoo, FAISS/Qdrant y rutas
Gemma/vLLM/Ray/LoRA/world model. Queda bloqueado: prediccion social garantizada,
validacion neurocientifica, publicacion externa, copia de fuentes brutas,
ontologia como prerequisito del MVP y cirugia interna del modelo.

Bloqueos resueltos localmente: mezcla de capas, ingestion bruta de Downloads,
confusion de claims y falta de contratos nucleares. Bloqueos que siguen por
gate: modelos pesados y publicacion externa.

## Claim boundary

Los indicadores del fixture son sinteticos y solo existen para validar el
contrato, hashing, rechazo de fuentes no allowlist y backtest reproducible. Un
uso con datos reales requiere revisar licencia, fecha de captura, hash del
payload y claims bajos por cada fuente.
