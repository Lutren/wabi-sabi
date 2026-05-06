# Matrix Agent Roles

Estado: `ROLE_CONTRACT / DEPARTMENT_MODEL`.

## Jefes de departamento

| departamento | jefe simbolico | responsabilidades |
|---|---|---|
| Biblioteca | Elrond | recuperacion, indice, modulo correcto |
| Archivo | Archivero | archivo frio, WitnessLog, trazabilidad |
| Nexus | Investigadora | busqueda local, evidencia, preguntas abiertas |
| Seguridad | Malika | ActionGate, secretos, frontera privada |
| Auditoria | Juez | tests, falsadores, claims, cierre |
| Builder | Constructor | implementacion local con rollback |
| Telecom | Operador Central | COMMS, handoff, mensajes entre agentes |
| Curaduria | SETO | fichas, sinapsis, estado epistemico |

## Especialistas

Los especialistas consumen un workpack pequeno:

- tarea;
- modulo o modulos cargados;
- entradas;
- limites;
- evidencia requerida;
- validacion;
- handoff.

## Wabi-Sabi

No es jefe de todos los detalles. Coordina traduccion y cierre:

- observa;
- reduce R;
- selecciona modulos;
- delega;
- revisa;
- corrige;
- compila salida.

Si el resultado no reduce R o no produce artefacto verificable, Wabi-Sabi debe
devolver correccion al jefe o especialista responsable.
