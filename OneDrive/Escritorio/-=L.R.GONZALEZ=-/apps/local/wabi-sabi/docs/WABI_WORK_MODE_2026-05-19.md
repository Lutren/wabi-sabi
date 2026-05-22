# WABI WORK MODE 2026-05-19

Fingerprint: WABI_WORK_MODE_20260519

Estado: WORK_MODE_READY para trabajo local diario.

Este documento cambia el foco de construccion a uso operativo. Wabi ya puede
trabajar sobre tareas pequenas y medianas dentro de rutas allowlisted, con
TaskSpec, preview, apply local, rollback, tests y reporte.

## Abrir Wabi CLI

Desde el entorno donde `wabi` este en PATH:

```powershell
wabi
```

Desde el repo local de Wabi:

```powershell
.\wabi.cmd
```

Para una consulta directa sin abrir sesion interactiva:

```powershell
wabi --once "hola wabi"
```

## Abrir UI local

Servidor local esperado:

```text
http://127.0.0.1:8787/
```

La UI debe mostrar:

- Wabi Conversation.
- Cloud Budget.
- Review TaskSpec.
- Gate Preview.
- Apply Local Preview.
- Apply Local.

## Como pedir programacion

Usa lenguaje natural y tareas pequenas:

```text
programa un helper seguro para validar json
modifica X archivo para hacer Y
debuggea este error
crea tests para este modulo
```

Buenas peticiones incluyen:

- archivo o modulo objetivo si lo conoces;
- comportamiento esperado;
- prueba o evidencia esperada;
- limite claro de lo que no debe tocar.

## Flujo seguro

El flujo diario es:

```text
Conversacion
TaskSpec
Review
Gate Preview
Apply Local Preview
Apply Local
Tests
Report
```

Reglas:

- Review muestra la intencion, rutas afectadas, riesgos y tests.
- Gate Preview explica por que la accion es permitida o bloqueada.
- Apply Local Preview no escribe archivos.
- Apply Local solo escribe si la ruta esta allowlisted y los gates pasan.
- Rollback snapshot se crea antes de escribir.
- Tests y scans corren despues del apply.
- Si los tests fallan, Wabi debe intentar rollback y reportar el resultado.

## Que puede hacer Wabi ahora

- Escribir en rutas allowlisted.
- Crear patch candidate.
- Aplicar cambios locales controlados.
- Crear snapshot de rollback.
- Correr tests definidos.
- Revertir si falla el test gate.
- Guardar evidencia local.
- Emitir WitnessLog.
- Mantener `applied_to_sources`, `cloud_provider_called` y gates visibles.

## Que no debe hacer todavia

- Push.
- Deploy.
- Publicar assets.
- Aplicar cambios fuera de allowlist.
- Activar cloud live por defecto.
- Aplicar salida cloud directamente.
- Activar `graphics_live`.
- Activar BrowserBridge live.
- Publicar en GitHub o medioevo.space.

## Comandos utiles

```powershell
wabi --once "hola wabi"
wabi apply-local-preview --latest --json
wabi apply-local --latest --json
wabi build-assist-status --json
wabi build-assist-plan "crear helper seguro" --dry-run --json
```

Estado cloud:

- NVIDIA/build-assist queda `proposal_only`.
- Cloud live requiere doble opt-in explicito.
- Sin doble opt-in, `cloud_provider_called=false`.

## Rutina diaria recomendada

1. Abrir `wabi` o la UI local.
2. Pedir una tarea pequena o mediana.
3. Revisar TaskSpec.
4. Revisar Gate Preview.
5. Ejecutar Apply Local Preview.
6. Ejecutar Apply Local solo si las rutas y tests son correctos.
7. Leer el reporte de tests, scans y rollback.
8. Si pasa, continuar con la siguiente tarea.
9. Si falla, usar el reporte y rollback antes de abrir mas trabajo.

## Stop rules

Detener y dejar en REVIEW/BLOCK si aparece:

- secreto, token, credential o valor de entorno sensible;
- ruta fuera de allowlist;
- repo incorrecto;
- cambio de licencia;
- publicacion, push o deploy;
- asset sin provenance/licencia;
- tests criticos fallando sin rollback limpio;
- necesidad de login, 2FA o pago.

## Estado operativo final

LOCAL WORK: PASS.

Wabi ya puede usarse como asistente local real de programacion dentro de sus
gates. El release externo sigue separado y bloqueado hasta resolver repo,
worktree, provenance/licencia de assets y publication review.

## LLM cloud proposal por defecto

Work Mode puede usar un LLM cloud como capa de propuesta si el operador activa:

```powershell
$env:WABI_LLM_PROVIDER_CLOUD_DEFAULT='1'
```

Esto no autoriza llamadas live por si solo. Para llamada live siguen siendo
necesarias ambas banderas:

```powershell
$env:WABI_BUILD_ASSIST_CLOUD='1'
$env:WABI_ALLOW_CLOUD_PROVIDERS='1'
```

Sin doble opt-in, el estado esperado es `CLOUD_BUDGET_DRY_RUN` y
`cloud_provider_called=false`.

Con doble opt-in, presupuesto disponible y provider configurado, la salida del
LLM queda `proposal_only` y debe pasar Review TaskSpec, Gate Preview, Apply
Local Preview, rollback, tests y scans antes de modificar archivos.
