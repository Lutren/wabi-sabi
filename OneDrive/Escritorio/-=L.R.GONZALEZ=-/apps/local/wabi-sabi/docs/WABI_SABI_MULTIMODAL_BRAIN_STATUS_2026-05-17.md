# WABI SABI MULTIMODAL BRAIN STATUS 2026-05-17

## Estado corto

La construccion va en fase funcional local, no en fase de cerebro multimodal
completo.

Wabi-Sabi ya tiene ruta canonica, CLI, router automatico, memoria append-only,
ActionGate, safe executor, rollback/witness, proveedor local por Ollama,
Codex CLI read-only, adapters cloud bloqueados por defecto, curador, fichas y
modulos `cerebro_*` para inventario/canon.

BRAIN_OS/02_CLAUDIO aporta la capa mas cercana al cerebro multimodal:
`world_model_adapter`, fixtures sinteticos de mundo observado, benchmark,
comparador baseline, `mts_sensor_fusion_agent`, provider policy, BudgetGate y
tests de seguridad para no meter imagen cruda, secretos ni datos privados en
witness.

## Evidencia actual

- `python tools\release\pending_review.py --write --quiet`
  - `pending_review date=2026-05-17 active_dedup=19 claudio_open=0`
- `python -m wabi_sabi.cli.main provider-status --json`
  - `auto_provider=ollama`
  - `base_model=qwen2.5-coder:3b`
  - `fast_model=qwen2.5:0.5b`
  - Codex CLI disponible en modo `read_only_codex_exec`
  - modelos cloud filtrados: 4
  - cloud adapters con red bloqueada por defecto
- `python -m wabi_sabi.cli.main auto /status --json`
  - gate `APPROVE`
  - planos cargados: 7 fuentes
  - worktree sucio: `status_count=544`
- `python -m wabi_sabi.cli.main operator-status --json`
  - gate `REVIEW`
  - motivo operativo: ultimo safe-test artifact viejo falla/no esta fresco,
    aunque witness chain esta OK
- `python -m wabi_sabi.cli.main e2e-smoke --json`
  - ruta local genera artefacto seguro en runtime outputs sin modificar source
- `python -B -m pytest -q -p no:cacheprovider`
  - Wabi local: `209 passed in 98.93s`
- `python -m pytest tests\test_world_model_adapter.py tests\test_world_model_baseline_comparator.py tests\test_world_model_benchmark.py tests\test_wabi_local_server.py tests\test_wabi_provider_registry.py -q`
  - BRAIN_OS/02_CLAUDIO focal: `70 passed in 9.64s`
- `run_benchmark(output_path=None)`
  - fixture_count `9`
  - mode `synthetic_fixture_only`
  - provider_calls `false`
  - network_calls `false`
  - model_training `false`
  - gate_accuracy `1.0`
  - false_approve_rate `0.0`
- `compare_world_model_to_baseline(output_path=None)`
  - status `APPROVE_SYNTHETIC`
  - gate_accuracy_world_model `1.0`
  - gate_accuracy_baseline `0.5555555555555556`
  - false_approve_rate_world_model `0.0`

## Lectura tecnica

El "cerebro" existe como arquitectura operacional y capa de decision:
observa estados resumidos, calcula residuo del mundo, phi efectiva del mundo,
gate, regimen y accion recomendada. Tambien fusiona canales sinteticos y
mantiene fronteras de seguridad.

Lo multimodal real aun no esta cerrado. El schema acepta modalidades `visual`,
`latent`, `ui_state`, `synthetic` y `multimodal`, pero los datos actuales son
fixtures sinteticos y resummenes seguros. No hay ingestion real cerrada de
camara, audio, OCR, capturas vivas o sensores OPPO dentro del flujo Wabi
canonico. Tampoco hay entrenamiento, descarga de dataset, Torch ni llamadas
provider en el benchmark.

## Bloqueos y riesgos

- El worktree global esta sucio; no conviene aplicar cambios amplios ni declarar
  release.
- `operator-status` esta en `REVIEW` hasta refrescar `run-safe-tests` o limpiar
  la lectura del ultimo artifact fallido.
- Cloud providers estan catalogados/configurados parcialmente, pero red y gasto
  siguen bloqueados por politica/BudgetGate.
- BRAIN_OS permite APIs externas temporalmente en una rama de transicion, pero
  con hard stop y fallback local obligatorio.
- No declarar AGI, conciencia, vision real ni sistema multimodal productivo:
  la evidencia actual es local, sintetica y gateada.

## Proxima accion verificable

Cerrar el siguiente incremento como "multimodal intake v0":

1. Crear un adaptador que convierta una captura local o fixture de imagen en
   `WorldModelObservation` sin guardar bytes crudos.
2. Agregar fixture y schema test para modalidad `visual`.
3. Pasar el resultado por `world_model_adapter` y `mts_sensor_fusion_agent`.
4. Registrar witness sin imagen cruda ni secretos.
5. Ejecutar tests focales y actualizar este status.

## Implementacion 2026-05-17 - multimodal intake v0

Estado: implementado como intake local-first operativo dentro de Wabi/Sabi.

Cambios cerrados:

- Nuevo modulo `wabi_sabi/core/multimodal_intake.py`.
- Nuevo comando CLI `wabi multimodal` con subcomandos `status`,
  `smoke-camera`, `smoke-mic` y `observe`.
- Registro local `multimodal_intake` agregado a `wabi tools`.
- Pruebas nuevas en `tests/test_multimodal_intake.py` y cobertura CLI en
  `tests/test_cli.py`.
- README actualizado con comandos operativos y politica cloud/local.

Evidencia real de hardware:

- `python -m wabi_sabi.cli.main multimodal status --json`
  - `camera_present=true`
  - `microphone_present=true`
  - `cv2=true`, `sounddevice=true`, `pyaudio=true`, `numpy=true`,
    `faster_whisper=true`, `whisper=true`, `speech_recognition=true`,
    `mediapipe=true`
  - `brain_os_bridge.available=true`
  - `cloud.enabled=false`
  - `raw_media_to_cloud_allowed=false`
- `python -m wabi_sabi.cli.main multimodal smoke-camera --json`
  - `ok=true`, `gate=APPROVE`, `camera_frame_read=true`
  - artefacto:
    `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\multimodal_smoke_camera_20260516-221243.json`
  - `witness_verified=true`
  - `raw_image_included=false`, `raw_audio_included=false`,
    `cloud_provider_called=false`
- `python -m wabi_sabi.cli.main multimodal smoke-mic --seconds 2 --json`
  - `ok=true`, `gate=APPROVE`, `duration_sec=2.000`, `rms=0.128274`
  - artefacto:
    `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\multimodal_smoke_mic_20260516-221251.json`
  - `witness_verified=true`
  - `raw_audio_included=false`, `cloud_provider_called=false`
- `python -m wabi_sabi.cli.main multimodal observe --seconds 3 --local-only --json`
  - `ok=true`, `gate=APPROVE`
  - 3 muestras de camara + 1 muestra de microfono fusionadas como metadatos
  - artefacto:
    `C:\Users\L-Tyr\.medioevo\wabi\runtime\outputs\multimodal_observe_20260516-221509.json`
  - `witness_verified=true`
  - `raw_image_included=false`, `raw_audio_included=false`,
    `raw_media_saved=false`, `cloud_provider_called=false`
- `python -m wabi_sabi.cli.main multimodal observe --cloud --json`
  - `gate=REVIEW`
  - `cloud_provider_called=false`

Evidencia de pruebas:

- `python -m pytest tests/test_multimodal_intake.py tests/test_cli.py -q`
  - final rerun: `18 passed in 62.86s`
- `python -m py_compile wabi_sabi\core\multimodal_intake.py wabi_sabi\cli\main.py wabi_sabi\core\tool_registry.py`
  - PASS
- `python -m pytest -q`
  - `215 passed in 105.36s`

Verdad actual:

- La entrada local de camara y microfono ya funciona y deja evidencia.
- El bridge con `world_model_adapter` y `mts_sensor_fusion_agent` ya esta
  conectado.
- La fusion ya no falla por excepcion de contrato.
- El gate interpretativo de BRAIN_OS sigue marcando `BLOCK` cuando
  `Phi_eff_world < 0.60`; en la prueba real ocurrio por senal visual muy oscura
  y umbrales estrictos. Eso no bloquea el smoke operativo, pero si indica que
  la observacion multimodal todavia no debe declararse como integracion
  cognitiva aprobada.
- El cloud multimodal queda preparado como superficie de gate, no como llamada:
  no se envio media ni se invoco proveedor externo.
