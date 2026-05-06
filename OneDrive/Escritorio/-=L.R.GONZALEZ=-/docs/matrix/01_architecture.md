# Matrix Architecture

Estado: `MVP_ARCHITECTURE / LOCAL_ONLY`.

## Capas

```text
USUARIO / REALIDAD
  -> WabiSabi Orchestrator
  -> Librarian
  -> Curator
  -> DepartmentHead
  -> SpecialistAgent
  -> Auditor
  -> SecurityGate
  -> Archivist
  -> WabiSabi final output
```

## Roles de sistema

| rol | funcion minima | no debe |
|---|---|---|
| WabiSabi Orchestrator | interpretar intencion, estimar R/Phi_eff/regimen, seleccionar modulos | cargar todo el canon |
| Librarian | recuperar modulos por dominio, primitivas y compatibilidad | inventar contenido |
| Curator | validar actualidad, limpieza, fuentes y decay | aprobar claims fuertes |
| DepartmentHead | dividir workpacks por especialidad | ejecutar sin evidencia |
| SpecialistAgent | producir artefactos acotados | tocar carriles no asignados |
| Auditor | verificar tests, invariantes, handoff | publicar resultados |
| SecurityGate | aplicar ActionGate y fronteras | reemplazar firewall o permisos humanos |
| Archivist | registrar WitnessLog y handoff | reescribir historia |

## Flujo minimo

1. WabiSabi recibe estimulo.
2. Estima `R`, regimen y `Phi_eff`.
3. Aplica DO para separar intencion, evidencia, riesgo y salida.
4. Pide al Librarian modulos minimos.
5. Curator revisa estado, fuentes y decay.
6. WabiSabi recompila IOI en plan ejecutable.
7. DepartmentHead divide tareas.
8. SpecialistAgent ejecuta.
9. Auditor valida.
10. SecurityGate decide `APPROVE`, `REVIEW` o `BLOCK`.
11. Archivist registra WitnessLog.
12. WabiSabi compila output y handoff.

## Regla de contexto

El contexto cargado debe ser el menor conjunto de modulos que cierre la tarea.
Si un modulo no afecta decision, evidencia, riesgo o salida, no se carga.
