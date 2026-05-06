# Uso de Wabi Sabi CLI

## Comandos principales

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
.\wabi.cmd "crea una funcion que lea un archivo y resuma sus lineas"
.\wabi.cmd "revisa este proyecto y dime que falla"
.\wabi.cmd "arregla los tests"
.\wabi.cmd "crea un README para este modulo"
.\wabi.cmd "ejecuta diagnostico"
.\wabi.cmd agents
.\wabi.cmd logs
.\wabi.cmd e2e-smoke
```

## Instalacion editable

```powershell
python -m pip install -e . --no-deps --no-build-isolation
wabi "ejecuta diagnostico"
```

## Modo interactivo

```powershell
.\wabi.cmd
```

Luego escribir pedidos en lenguaje natural. Salir con `/exit`.

## Rutas de evidencia

- Artefactos: `runtime/outputs`
- Logs: `runtime/logs/wabi_events.jsonl`
- Memoria local: `runtime/memory/session_memory.jsonl`

## Fronteras

Wabi Sabi local no ejecuta acciones externas, no publica, no usa secretos y no
borra archivos. Si detecta una solicitud de riesgo, devuelve `BLOCK`.
