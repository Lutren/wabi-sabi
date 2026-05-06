# Matrix Mission Control Bridge

Estado: `IMPLEMENTADO_LOCAL / CLAUDIO_COMMIT_PARCIAL / WORKTREE_CONCURRENTE_PRESERVADO`.

## Objetivo

Conectar Matrix/Biblioteca de Alejandria con Hormiguero Mission Control sin
cargar canon completo y sin publicar material privado.

## Rutas tocadas

| ruta | accion |
|---|---|
| `-=MEDIOEVO=-/-=LIBROS/claudio/core/matrix_library.py` | nuevo lector read-only |
| `-=MEDIOEVO=-/-=LIBROS/claudio/core/matrix_delegation.py` | compilador Matrix -> COMMS |
| `-=MEDIOEVO=-/-=LIBROS/claudio/apps/hormiguero_mission_control/app.py` | endpoints locales Matrix |
| `-=MEDIOEVO=-/-=LIBROS/claudio/tests/test_matrix_library_api.py` | tests focalizados |
| `-=MEDIOEVO=-/-=LIBROS/claudio/tests/test_matrix_delegation.py` | tests de paquetes COMMS |

`app.py` ya estaba modificado por trabajo concurrente antes de esta pasada. La
integracion Matrix se separo con staging sintetico sobre `HEAD + solo Matrix`,
se valido y se hizo commit en Claudio sin arrastrar COMMS, Telecom, autonomia u
otros cambios ajenos.

Commit Claudio: `0f0f69f Connect Matrix library to Mission Control`.

Commit Claudio delegacion: `0bbeb05 Add Matrix delegation packages for COMMS`.

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

El compilador de delegacion convierte una intencion en mensajes COMMS
validados para jefes de departamento. Por defecto no escribe en COMMS; el append
queda separado y bloquea paquetes `BLOCK`.

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
- Matrix delegation + COMMS: `16 passed`.

## Handoff

Fingerprint: `MATRIX_MISSION_CONTROL_BRIDGE_2026-05-06_317BE610`

Siguiente paso seguro:

1. Consolidar el resto del working tree Claudio por modulo.
2. Agregar panel UI si se quiere mostrar Biblioteca en la ciudad.
3. Registrar evento COMMS/WitnessLog cuando el repo Claudio tenga una cola limpia.
4. Exponer los paquetes de delegacion en Mission Control cuando el UI este
   consolidado.
