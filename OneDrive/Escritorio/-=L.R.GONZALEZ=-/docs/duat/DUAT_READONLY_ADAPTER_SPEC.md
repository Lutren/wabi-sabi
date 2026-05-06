# DUAT Read-Only Adapter Spec

Estado: `LOCAL_ADAPTER_SPEC / READ_ONLY / ACTIONGATE_REVIEW`.

## Proposito

El adapter DUAT hacia Claudio existe para leer estado, fuentes, reportes
resumidos y falsadores sin mezclar el carril publico `duat-genesis` con el
DUAT/GEODIA interno. No es un runtime DUAT completo, no publica, no escribe y
no ejecuta predicciones reales.

## Carriles

| carril | ruta | decision |
|---|---|---|
| DUAT Genesis publico | `packages/open-dev/duat-genesis` | publico, sintetico, MIT, bajo claim |
| DUAT/GEODIA interno | `docs/product`, `docs/developer`, `research/geodia-social-observatory` | privado/research, local, no publicacion |
| COMMS/ActionGate | `COMMS` | contrato de coordinacion local |
| Fixture sintetica | `fixtures/duat/public_synthetic_fixture.json` | datos genericos para pruebas, sin lore privado |

## Interfaz minima

```python
from claudio.adapters.duat_readonly_adapter import DuatReadonlyAdapter

adapter = DuatReadonlyAdapter()
adapter.status()
adapter.report("overview")
adapter.report("public")
adapter.falsify("readonly_adapter")
adapter.source_registry()
```

CLI:

```powershell
python -m claudio.adapters.duat_readonly_adapter status
python -m claudio.adapters.duat_readonly_adapter report public
python -m claudio.adapters.duat_readonly_adapter falsify readonly_adapter
python -m claudio.adapters.duat_readonly_adapter source_registry
```

## Contrato de salida

`status()` devuelve:

- modo `READ_ONLY`;
- acciones externas `BLOCK`;
- publication gate `BLOCK`;
- comandos disponibles;
- conteo de fuentes;
- frontera publica/privada;
- rol de Wabi-Sabi como nodo sensorial-cognitivo de control, no cerebro total.

`report(scope)` devuelve:

- resumen por scope: `overview`, `public`, `internal`, `boundary`;
- fuentes visibles segun scope;
- acciones bloqueadas;
- falsadores obligatorios.

`falsify(claim_id)` devuelve:

- `PASS`, `FAIL` o `BLOCK`;
- lista de checks;
- evidencia minima;
- fingerprint local.

`source_registry()` devuelve:

- fuentes registradas;
- tipo;
- privacidad;
- licencia/politica;
- hash SHA256 o hash de manifiesto de directorio cuando existe.

## Wabi-Sabi

Wabi-Sabi no se modela aqui como cerebro central ni AGI. En este adapter queda
como `sensory_cognitive_control_node`: observa el estado DUAT, estima riesgo,
lee falsadores y traduce el resultado a Claudio/COMMS. No contiene todo el
conocimiento DUAT ni ejecuta acciones fuera de ActionGate.

## Bloqueos

- No escribir en DUAT/GEODIA interno.
- No copiar GEODIA real a `packages/open-dev`.
- No publicar claims cientificos, medicos, sociales o fisicos fuertes.
- No exportar RPG/TCG, lore, assets, prompts o runtime.
- No hacer fetch de red ni acciones de browser.
- No crear puente MCP con escritura.

## Fingerprint operativo

El adapter genera fingerprint por payload con SHA256. Ese fingerprint es
evidencia local para handoffs, no prueba cientifica externa.
