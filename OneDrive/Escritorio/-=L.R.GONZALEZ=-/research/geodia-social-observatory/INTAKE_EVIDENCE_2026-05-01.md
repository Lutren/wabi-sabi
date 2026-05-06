# GEODIA Intake Evidence 2026-05-01

Estado: integrado como material local privado. No autoriza publicacion externa.

## Fuentes revisadas

| archivo | SHA256 | decision |
| --- | --- | --- |
| `C:\Users\L-Tyr\Downloads\deep-research-report (4).md` | `0545a13b03ef48e16c12166765ac054ccace8143213c9817db45025ac2814485` | funcional + laboratorio |
| `C:\Users\L-Tyr\Downloads\Esto es material extraordinariament.txt` | `38786a7d410eb2dbebd9f78a153e107bc29ff6df52965c03acf6b144bad55620` | laboratorio con extractos funcionales |
| `C:\Users\L-Tyr\Downloads\duat_v2.html` | `899bf280a1f0c2f8fceea8ac0834bfd7b21df3d0fc10da9455c4dfe1c431a094` | laboratorio con extractos funcionales |
| `C:\Users\L-Tyr\Downloads\deep-research-report (5).md` | `39ebd04ed7baf9d083560d8c7e2783da0ddae6393140d779d8b7c574b090a6d5` | funcional + laboratorio |

Politica: `do_not_copy_raw`. Los archivos originales permanecen en Downloads.

## Entra al motor funcional

- Frontera de claim: adecuacion operacional, no verdad ultima.
- Separacion fenomeno / observacion / accion.
- Grafo de artefactos con aristas `supports`, `contradicts`, `verified_by` y `derived_from`.
- Vocabulario de fases DUAT como descripcion: `ordered`, `griffiths`, `disordered`, `chaotic`.
- Forma de simulacion offline seeded para fixtures y backtests.
- Roadmap DUAT de tres carriles: ingenieria/producto, metricas falsables y
  laboratorio ontologico.
- Maquina de eventos para observacion, propuesta, objecion, verificacion,
  simulacion, override humano y cambio de politica.
- Firma conductual como scoring continuo, no como raiz de identidad.

## Queda en laboratorio privado

- Dashboard DUAT v2 y visualizaciones fractales.
- Puente EEG y memoria conformacional.
- Gemma/vLLM/LoRA/world model.
- Predictores de futuro y mapas visuales.
- Mesa/PettingZoo y FAISS/Qdrant como experimentos posteriores, no prerequisitos
  del MVP.

## Bloqueos resueltos localmente

- `layer_mixing`: resuelto por carriles separados.
- `raw_download_ingestion`: resuelto por SHA256 y politica `do_not_copy_raw`.
- `claim_confusion`: resuelto por frontera de claims y clasificacion de
  evidencia.
- `missing_core_contracts`: resuelto manteniendo event store, artifact graph,
  router, behavior, health y simulation como nucleo.

## Bloqueos que siguen por gate

- `heavy_model_path`: Gemma/vLLM/Ray/LoRA requiere host gate, latencia, memoria y
  QA.
- `external_publication_path`: requiere ActionGate, paquete limpio, legal y
  secret scan del artefacto.

## Queda bloqueado

- Prediccion social garantizada.
- Validacion neurocientifica o EEG real sin dataset, licencia, consentimiento y protocolo.
- Publicacion externa.
- Copia bruta de Downloads a paquetes publicos o comerciales.

## Verificacion

```powershell
python -m pytest tests -q
# 15 passed

python -m geodia_social_observatory.cli duat-v2-intake --pretty
# schema: motor.duat_v2_intake.v1
# source_count: 4
# decision_sha256: b912296e1603826f0414e8833f5579712ed5ec24abcc7b2e0a72b27fa9586681

python tools\release\scan_secrets.py --product geodia-social-observatory --json --fail-on-findings
# count_reported: 0

python tools\release\product_manifest.py --product geodia-social-observatory --hash
# blocked_count: 0
# file_count: 21
```
