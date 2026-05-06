# Matrix Mission Control Bridge

Estado: `IMPLEMENTADO_LOCAL / CLAUDIO_WORKTREE_DIRTY / COMMIT_REQUIERE_CONSOLIDACION`.

## Objetivo

Conectar Matrix/Biblioteca de Alejandria con Hormiguero Mission Control sin
cargar canon completo y sin publicar material privado.

## Rutas tocadas

| ruta | accion |
|---|---|
| `-=MEDIOEVO=-/-=LIBROS/claudio/core/matrix_library.py` | nuevo lector read-only |
| `-=MEDIOEVO=-/-=LIBROS/claudio/apps/hormiguero_mission_control/app.py` | endpoints locales Matrix |
| `-=MEDIOEVO=-/-=LIBROS/claudio/tests/test_matrix_library_api.py` | tests focalizados |

`app.py` ya estaba modificado por trabajo concurrente antes de esta pasada. Por
eso la integracion quedo aplicada y validada en working tree, pero no se hizo
commit en el repo Claudio para no arrastrar cambios ajenos.

## Endpoints locales

- `GET /api/local/matrix/status`
- `GET /api/local/matrix/library/status`
- `GET /api/local/matrix/modules`
- `GET /api/local/matrix/library/modules`
- `GET /api/local/matrix/modules/<module_id>`
- `GET /api/local/matrix/library/modules/<module_id>`
- `POST /api/local/matrix/retrieve`
- `POST /api/local/matrix/library/retrieve`

Todos requieren loopback y perfil local. `profile=public_safe` devuelve `403`.

## Contrato read-only

El lector devuelve:

- estado del indice `library/index.json`;
- conteo de modulos;
- resumenes minimos;
- modulo individual bajo demanda;
- recuperacion por objetivo/dominio;
- R/Phi_eff estimados;
- handoff para Librarian;
- acciones bloqueadas.

No escribe, no mueve, no borra, no publica, no entrena y no carga CEREBRO en
bloque.

## Validacion ejecutada

```powershell
python -m py_compile core\matrix_library.py apps\hormiguero_mission_control\app.py
python -m pytest tests\test_matrix_library_api.py -q
python -m pytest tests\test_matrix_runtime.py tests\test_hormiguero_mission_control_api.py -q
python ..\..\..\tools\matrix\validate_library.py --root ..\..\.. --json
python ..\..\..\COMMS\tools\validate_seto_comms.py --json --fail-on-errors
```

Resultado:

- Matrix library API: `6 passed`.
- Matrix/Mission Control focal: `32 passed`.
- Biblioteca: `PASS`, 10 modulos, fingerprint `317BE610047A34BC`.
- COMMS: `PASS`.
- Secret scan con rutas absolutas: `0` hallazgos.

## Handoff

Fingerprint: `MATRIX_MISSION_CONTROL_BRIDGE_2026-05-06_317BE610`

Siguiente paso seguro:

1. Consolidar o separar el working tree Claudio.
2. Stagear solo el hunk Matrix de `app.py` o aceptar commit de Mission Control completo.
3. Agregar panel UI si se quiere mostrar Biblioteca en la ciudad.
4. Registrar evento COMMS/WitnessLog cuando el repo Claudio tenga una cola limpia.
