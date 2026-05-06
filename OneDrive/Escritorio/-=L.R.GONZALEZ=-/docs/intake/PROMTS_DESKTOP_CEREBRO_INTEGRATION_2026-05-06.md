# Promts Desktop + CEREBRO - Integracion 2026-05-06

Estado: `FICHADO / ABSORCION_SELECTIVA / SIN_MOVIMIENTOS`

Este documento registra el pase local sobre:

- `C:\Users\L-Tyr\OneDrive\Escritorio\promts`
- `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\-=CEREBRO=-`

No se publico, movio, borro ni renombro ninguna fuente. El objetivo fue absorber
la informacion util al sistema operativo de trabajo y dejar decisiones claras
para que Wabi-Sabi, Curador SETO, Mission Control y otros agentes no dupliquen
verdad.

## Resumen operativo

| bloque | evidencia | decision |
|---|---:|---|
| `promts` | 14 TXT, 152076 bytes, preflight `NEEDS_FICHA_BEFORE_USE` | Registrar como INBOX de prompts, extraer trabajo aplicable y no convertir en canon directo |
| `CEREBRO` | 194 archivos, 39 directorios, 35.361 MB, preflight `REGISTERED_CONTINUE_WITH_BOUNDARY` | Mantener como canon humano/research; limpiar por manifest, no por borrado intuitivo |
| `Downloads` | Curador status: 0 archivos actuales, SQLite 186 fuentes, 186 fichas | Descargas ya no son el problema inmediato; el nuevo INBOX es `promts` y CEREBRO reciente |
| `pending_review` | `active_dedup=389`, `claudio_open=69` | Priorizar cierres locales verificables, no expansion nueva |

## Prompts absorbidos

| fuente | sha256 | estado | destino canonico | decision |
|---|---|---|---|---|
| `Actua como AGENTE CANON OBSERVACION.txt` | `4247032BBBB96664D90DBF58B4C015A2BFD2113C07EC20EEB39DFF5F5EEFE5EB` | `REVIEW` | `docs/language`, `-=PSI=-/canon/extensiones_formales` | Convertir a schema, dataset y validador; no inventar canon |
| `Actua como AGENTE AI BROWSER SEGURO.txt` | `7BB6E729CB345BC5D180B0CC2268D9A03B899E5D863E316920F6C78B10F23A07` | `IN_PROGRESS_CONCURRENT` | `docs/ai_browser` | Ya hay trabajo concurrente; no pisar diffs ajenos |
| `Actua como AGENTE DUAT GEODIA OS P3.txt` | `0F7F189B362903ECA89282964251C8CB40E1FCFCD13886CDE3461AC88B6FF065` | `REVIEW` | `docs/duat`, DUAT/GEODIA OS privado | Elegir un solo slice tecnico; no declarar OS generalista |
| `Actua como AGENTE DUAT READ-ONLY AD.txt` | `906B90285824B1DF25CCE0357BE0FAFD84FFE4DD58F477133B3406E896705CAB` | `IMPLEMENTADO_LOCAL` | `docs/duat`, `claudio/adapters/duat_readonly_adapter.py` | Adapter read-only ya quedo como contrato local; mantener frontera publico/privado |
| `Actua como AGENTE LENGUAJE OBSERVAC.txt` | `1E51145CE73413FDECF2B5C7581D981A87C43AD2C9758723C61C75143290451A` | `IN_PROGRESS_CONCURRENT` | `docs/language`, `research/observacionismo-lab` | Mantener lenguaje minimo: observar, documentar, verificar, actuar, handoff |
| `Actua como AGENTE MATRIX BIBLIOTEC.txt` | `46401C252D8B2CAE2A8580B71BA8A4B46216F02C91652CB23560A868E875709F` | `IMPLEMENTADO_LOCAL` | `docs/matrix`, `library/modules`, Claudio Matrix bridge | Biblioteca modular ya existe; siguiente paso es UI/COMMS consolidado |
| `Kernel inicial del reto 1 OSIT-QG v.txt` | `0CD17F706C3E40400F404AE5449A513155C9B25C2060BD78A2FFED30E2848B92` | `BLOQUEADO_PUBLICACION` | `-=PSI=-/canon/extensiones_formales` | Fuente research; claims fisicos solo como hipotesis con falsadores |
| `## ESTADO.txt` | `83A765A63CC41336A09B3B85B6472F36A98AA68A023954522B98B74382E52ACE` | `BLOQUEADO_PUBLICACION / RESEARCH_ONLY` | OSIT-AG ficha futura | No usar como tecnologia fisica; rescatar falsadores, limites y lenguaje de bloqueo |
| `## ESTADO2.txt` | `9E1999E40A6B5BC675E787FC585028E06D6BFF994C123919A76A3FD91ACC5E11` | `APLICABLE_OPERATIVO` | Claudio/Wabi-Sabi resource policy | Aplicar como gobernador de recursos: cache, RAG, cascada de modelos, compresion, batch y memoria gated |
| `Actua como AGENTE PROGRAMADOR SEGUR.txt` | `7F3E194C2E542FBCCE5EE928D2AAC1DCFF552E3242D7F2B945D0A038083589DA` | `P1` | Claudio local autonomy | PatchPlanner, RollbackStore, SafeExecutor y AutonomyController, sin autonomia amplia |
| `Actua como AGENTE RELEASE PUBLIC-S.txt` | `B62C6E001205B32CEBC252C2FDFED48DAF737411155CBE4E8EE72305CAC650E2` | `P1_GATED` | release governance | Allowlist, denylist, claims scan y checklist; no publicar ni hacer push desde prompt |
| `Actua como AGENTE ORQUESTADOR DE CI.txt` | `F3EB20ACC2C6663D8E970E5D65C8A16432517D2A300694DAB4D463D5F1343F79` | `P0` | `docs/ops` o `COMMS/workpacks` | Crear workpack de cierre local para agentes; no crear capas nuevas |
| `Actua como AGENTE MISSION CONTROL.txt` | `D692921B5742E035591477FE8CD2274E447EA2A2DA98B1C50F0B9115E4AB0EA7` | `P1` | Hormiguero Mission Control | Vista clara read-only de agentes, gates, COMMS, WitnessLog y pendientes |
| `Actua como AGENTE MEDIOEVO RPG TOOL.txt` | `9627A14F8A7BAF7520C60861238BFD73D48A32219ADE846F40E99CC5A398F662` | `PRIVATE_REVIEW` | RPG privado / StoryBible | Investigar tooling, no tocar assets, no publicar, no borrar TODOs sin ficha |

## Insights aplicables a Claudio / Wabi-Sabi

### CERTEZA

- Wabi-Sabi debe seguir como nodo de control, no como cerebro total: interpreta,
  reduce R, recupera modulos Matrix, delega y compila salida.
- Matrix/Biblioteca ya esta definida como modulo bajo demanda: no se carga todo
  CEREBRO en contexto.
- DUAT read-only debe permanecer separado del carril publico `duat-genesis`.
- El arbol completo no es publicable; releases y perfiles externos siguen bajo
  ActionGate/manual-auth.
- Los prompts nuevos confirman el estilo operativo correcto: lectura real,
  evidencia, hash, fichas, tests y handoff.

### INFERENCIA

- `ESTADO2` y `-=PSI=-\.py` son el mismo carril conceptual: `OSIT Resource
  Optimizer`. Debe convertirse en politica de runtime para:
  - seleccion de modelo por R, riesgo, evidencia y novedad;
  - compresion de contexto cuando `context_pressure >= 0.62`;
  - cache semantico solo con bajo riesgo y similitud alta;
  - RAG solo cuando hay deuda de evidencia;
  - una repeticion maxima sin cambio de estrategia;
  - escritura de memoria solo si es estable, util, especifica y consentida.
- El archivo `.py` no debe quedarse como fuente anonima en CEREBRO. Debe
  renombrarse o absorberse con manifest como `osit_resource_optimizer.py`.
- AI Browser, lenguaje y programador seguro ya estan en curso por otros agentes
  o salidas concurrentes; el trabajo correcto es integrarlos por fichas y no
  duplicar implementaciones.

### BLOQUEADO

- OSIT-QG/OSIT-AG no se puede publicar ni vender como fisica validada.
- No se permite declarar antigravedad utilizable, propulsion, diagnostico,
  prediccion social real o seguridad absoluta.
- No se permite mover CEREBRO completo a open-dev ni copiar prompts crudos a
  productos publicos.

## CEREBRO: estado y limpieza

Inventario focal 2026-05-06:

- Archivos: `194`
- Directorios: `39`
- Peso: `35.361 MB`
- Extensiones: `.md` 95, `.txt` 30, `.py` 18, `.json` 12, `.docx` 10, `.pdf` 10,
  `.zip` 9, `.csv` 5, `.html` 3, `.jpg` 2.

Fuentes recientes de alto valor:

| fuente | sha256 | estado | decision |
|---|---|---|---|
| `-=PSI=-\.py` | `76F80E0A9A273CBE2EC9CE009FAD39086390E4D942C4955CDE480BDF78FCE9CD` | `APLICABLE_OPERATIVO` | absorber como OSIT Resource Optimizer; renombre pendiente con manifest |
| `OSIT-AG-K1.0 - Antigravedad Residual...docx` | `9242F35CB2DB5E9CA3240264AC1AE482266B7EB23BEFBEB705DAD6785BEAFF6A` | `BLOQUEADO_PUBLICACION` | conservar hasta ficha; no usar como claim publico |
| `OSIT-AG-K1.0 - Antigravedad Residual...pdf` | `2DC54A35885FC08FEADE77F26B84BC08A5B76B3CB22B9EC3C96F0D544A07C1B5` | `BLOQUEADO_PUBLICACION` | salida generada; candidato archivo frio tras ficha |
| `OSIT-QG - Teoria Efectiva...docx` | `ACBE0A53CD7583EA2DEBBBFBF7EC4A3DD5BBAF5CCC3715A3206CA7DB54D4F86D` | `BLOQUEADO_PUBLICACION` | research fisico con falsadores |
| `OSIT-QG - Teoria Efectiva...pdf` | `4C2972DB33ADB41595D0D73736DB70B1A16C17178920E78F1182B17EAAB3CBF1` | `BLOQUEADO_PUBLICACION` | salida generada; no canon directo |
| `AUDITORIA_OBSERVACIONISTA_INVERSA_MEDIOEVO_v2.md` | `A400E1CC740F791845993EE25A807AC485DB1266F30586246C63CC9025C2978D` | `CANON_AUDIT` | usar como guia de limites y faltantes |
| `00_FICHA_TECNICA_PSI_2026-05-05.md` | `A953573D22AE47425E0F20FA5E28793E6A500981B67BD8EC461E7D914107E340` | `CANON_ENTRY` | mantener como puerta PSI |
| `19_PSI_WABI_SABI_ABSORCION_OPERATIVA_2026-05-05.md` | `075C0A64D335C9CA52A56ABDD6C21EE55078A563E4560DF3382A8CBA9CC98740` | `RUNTIME_POLICY_CONNECTED` | evidencia de absorcion PSI -> Wabi-Sabi |

Duplicados exactos internos detectados:

| sha256 | copias | decision |
|---|---:|---|
| `17A337C761955D2EAC5F1161AF683800B220E5C4AB253E0E9BB67EC3382F83E3` | 2 | conservar `libro\07_PROMPT_MAESTRO_HANDOFF.md`; archivo duplicado queda candidato tras ficha |
| `5A30C1FA3152EB2D623D0275673F3BBDABA17116F53596B81F815F796CA5E9CB` | 2 | conservar raiz `08_POSICIONAMIENTO_EL_OBSERVADOR.md`; archive duplicado candidato |
| `6D452217E61A4175F1525A27F98E250C678F333C85D7CB1CD876A113035F1463` | 2 | conservar raiz `04_BRAIN_OS.md`; archive duplicado candidato |
| `7F18344AB924A5BE168046C6DD3B5185CAC659C30E236C3F8C40F09BBF3BF3F1` | 2 | conservar `libro\09_MAGIA_PRACTICA.md`; archive duplicado candidato |
| `BF84C85C11A680A7EB7F06FBA2EEF548D7030F07E76FF45F162DB40DD23ED68C` | 2 | conservar raiz `02_SEGUNDA_PERDIDA.md`; archive duplicado candidato |

## Accion inmediata recomendada

1. Crear `docs/ops/WORKPACK_CIERRE_LOCAL_2026-05-06.md` desde el prompt de
   Orquestador de Cierre.
2. Convertir `OSIT Resource Optimizer` en spec de Claudio antes de tocar
   `model_router.py`: primero policy doc, luego tests, despues adapter.
3. Ejecutar limpieza CEREBRO en dos pasos:
   - Fase A: renombrar/mover solo con `MANIFEST_CAMBIOS` y rollback.
   - Fase B: retirar duplicados exactos de `archive\raiz_2026-04-26` solo si
     el archivo canonico sigue presente y el hash coincide.
4. No tocar AI Browser/lenguaje si otro agente ya tiene diffs; integrar por
   lectura y handoff cuando esos cambios queden cerrados.

## Fingerprint

`PROMTS_CEREBRO_INTEGRATION_2026-05-06_9E1999E4`
