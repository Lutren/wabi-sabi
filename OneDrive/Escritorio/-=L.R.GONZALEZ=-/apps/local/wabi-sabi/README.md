# Wabi Sabi Local Agents

CLI local-first para hablar con Wabi Sabi y enrutar tareas simples hacia
agentes verificables. No requiere nube ni claves. Si no hay modelo local, usa
fallback determinista basado en reglas, artefactos y logs.

## Uso rapido

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
.\wabi.cmd "crea una funcion que lea un archivo y resuma sus lineas"
.\wabi.cmd "ejecuta diagnostico"
.\wabi.cmd agents
.\wabi.cmd e2e-smoke
```

## Instalacion editable opcional

```powershell
cd C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\apps\local\wabi-sabi
python -m pip install -e . --no-deps --no-build-isolation
wabi "crea un README para este modulo"
```

## Seguridad

- No hace push, deploy, publicacion, compras, borrados destructivos ni uso de
  secretos.
- Las escrituras automaticas van a `runtime/outputs` y los logs a
  `runtime/logs`.
- Las acciones riesgosas quedan en `BLOCK` o `REVIEW` con explicacion.

Ver tambien:

- `docs/USAGE.md`
- `docs/ARCHITECTURE.md`
- `REPORT_WABI_SABI_LOCAL_AGENTS.md`
