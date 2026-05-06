# Matrix Delegation Protocol

Estado: `DELEGATION_PROTOCOL / COMMS_COMPATIBLE`.

## Workpack

Un workpack para jefe o especialista debe incluir:

- `task_id`;
- `sender`;
- `receiver`;
- `goal`;
- `selected_modules`;
- `inputs`;
- `allowed_paths`;
- `forbidden_actions`;
- `evidence_required`;
- `tests`;
- `handoff_expected`;
- `action_gate`.

## Secuencia

1. WabiSabi compila workpack.
2. Telecom lo manda por COMMS o handoff local.
3. DepartmentHead separa subtareas.
4. SpecialistAgent ejecuta solo su scope.
5. Auditor verifica tests e invariantes.
6. SecurityGate revisa riesgo residual.
7. Archivist registra WitnessLog.
8. WabiSabi compila salida final.

## Correccion

Si falta evidencia, el agente no debe improvisar cierre. Debe responder con:

- que falta;
- donde se busco;
- que modulo se necesita;
- que falsador fallo;
- siguiente accion segura.
