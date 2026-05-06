# Agent City Coordination - 2026-05-06

Fuente primaria: `C:\Users\L-Tyr\OneDrive\Escritorio\Lobby de Alejandria\0. Prompt maestro de continuidad ME.txt`

## ESTADO

- Fecha local: `2026-05-06T01:09:46-06:00`.
- Host: `Claudio-Choza`.
- Raiz canonica: `C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-`.
- Gate general: `REVIEW`.
- Regimen: `LOCAL_REVIEW_ONLY`.
- R observado por `host_observacionista --no-write`: `0.442`.
- Phi_eff observado: `0.555`.
- HealthVector dominante: `r_mem=0.842`.
- `pending_review`: `active_dedup=389`, `claudio_open=69`.
- Worktree: sucio/concurrente; no se debe broad-stagear, revertir ni pisar archivos de otros agentes.
- Publicacion, redes, Gumroad, deploy, push, daemons, modelos pesados, entrenamiento, borrado y movimientos siguen bloqueados por gate especifico.

## CERTEZA

- El prompt maestro esta fichado por Curador SETO:
  `docs/intake/inbox_downloads_lobby_alejandria_current_2026-05-06_FICHAS.md`.
- SHA256 del prompt maestro:
  `DB8791BE402BE2F7C41ACD19359AF406776E18BFE16BF4C5D83FE5DBDE500DB7`.
- `pending_review` fue refrescado con:
  `python tools\release\pending_review.py --write --quiet`.
- Artefactos de snapshot:
  `qa_artifacts/pending/pending_review_latest.json`
  SHA256 `F319541839781DFA996E17AD149A5DE029475CFF11AA4F5FE102D33C8B56A2E1`.
- Markdown de snapshot:
  `docs/pending/PENDING_REVIEW_LATEST.md`
  SHA256 `C46B321EF50A87FA2387177B9982F5CF6640B2BEB3B649F3D2DD661855F53C8B`.
- COMMS registra seis agentes existentes:
  `claudio-local-agent`, `claudio-local-autonomy`, `curador-seto`,
  `hormiguero-mission-control`, `publicacion-perfiles-observatorio`,
  `wabi-sabi-sentido-comun`.
- Ningun agente existente tiene gate amplio `APPROVE`: el conjunto opera en `REVIEW` o `BLOCK`.

## INFERENCIA

- La coordinacion correcta no es crear agentes nuevos, sino publicar un contrato local append-only para que los agentes existentes lean la misma prioridad.
- El carril mas seguro para continuar es `Prompt 17 - Agentes especializados / ciudad Claudio`, porque reduce solapamientos y alimenta Mission Control sin cruzar acciones externas.
- El segundo carril util es `Prompt 7 - Claudio Mission Control / COMMS`, limitado a vista/reporte local.
- Los prompts con accion externa o frontera privada deben quedar como `BLOCK` o `REVIEW`, no como ejecucion automatica.

## INCOGNITA / BLOQUEADO

- No se verifico publicacion externa, LinkedIn, Gumroad, GitHub, website ni redes.
- No se ejecuto Qwen 3B, QEMU, alias Ollama, LoRA/QLoRA/DPO ni modelos pesados.
- No se toco `E:\Medioevo_RPG`; el carril RPG queda bloqueado hasta handoff privado explicito.
- No se resolvieron diffs concurrentes en `docs/ai_browser`, `docs/canon`, `research/observacionismo-lab`, `tools/ai_browser` ni otros archivos ya modificados.
- No se hizo limpieza destructiva ni movimiento de archivos.

## MAPA DE AGENTES

| agente | estado | gate | funcion coordinada | siguientes prompts | accion segura inmediata |
|---|---|---|---|---|---|
| `claudio-local-agent` | `ACTIVE_LOCAL_BRIDGE` | `REVIEW` | Nodo coordinador COMMS, pending review, handoffs, Mission Control local | 1, 6, 7, 17, 20 | Leer este handoff, mantener `pending_review` vigente y proponer solo cierre local verificable |
| `claudio-local-autonomy` | `A0_LOCAL_REVIEW_ONLY` | `BLOCK` | Autonomia local permitida solo en acciones allowlist y no-write | 6, 13 | No escalar autonomia; preparar workpacks sin ejecutar externo ni pesos |
| `curador-seto` | `ACTIVE_LOCAL_CONTRACT` | `REVIEW` | Fichas, manifolds, duplicados, fuentes, WitnessLog y fronteras | 11, 12, 14, 16, 17 | Clasificar fuentes y solapamientos; no borrar ni mover sin ficha, hash y gate |
| `hormiguero-mission-control` | `LOCAL_READ_SURFACE` | `REVIEW` | Superficie local de ciudad, agentes, gates y pendientes | 7, 15, 17 | Exponer lectura clara de agentes/gates/pending sin daemon permanente |
| `publicacion-perfiles-observatorio` | `ACTIVE_LOCAL_STRATEGY_AGENT` | `REVIEW` | Estrategia publica, perfiles, copy packets y limites publicos | 9, 10, 18, 19 | Preparar packets/checklists locales; no publicar ni tocar dashboards |
| `wabi-sabi-sentido-comun` | `POLICY_ONLY_LEARNING_SOURCE` | `REVIEW` | Politicas de sentido comun, aprendizaje local y recursos | 8, 13 | Registrar decisiones como politica; no tocar pesos, alias ni externo |

## RUTEO DEL PROMPT MAESTRO

| prompt | carril | dueño primario | gate |
|---:|---|---|---|
| 1 | Pending Review / cierre P0 | `claudio-local-agent` | `REVIEW` |
| 2 | Lenguaje Observacionista L0/L1/L2 | `claudio-local-agent` + `curador-seto` | `REVIEW_CONCURRENT_DIFF` |
| 3 | RPG MEDIOEVO privado | sin agente COMMS local asignado | `BLOCK_PRIVATE_BOUNDARY` |
| 4 | DUAT / GEODIA read-only | `claudio-local-agent` + `hormiguero-mission-control` | `REVIEW` |
| 5 | DUAT GEODIA OS | `claudio-local-agent` | `REVIEW_HOST_QEMU` |
| 6 | Agente programador local | `claudio-local-autonomy` + `claudio-local-agent` | `BLOCK_TO_DIFF_REVIEW` |
| 7 | Claudio Mission Control / COMMS | `hormiguero-mission-control` | `REVIEW` |
| 8 | Ingenieria Observacionista operacional | `wabi-sabi-sentido-comun` + `curador-seto` | `REVIEW` |
| 9 | Open-dev / paquetes public-safe | `publicacion-perfiles-observatorio` + `curador-seto` | `REVIEW_NO_PUBLICATION` |
| 10 | Productos comerciales | `publicacion-perfiles-observatorio` | `REVIEW_LEGAL` |
| 11 | Editorial / canon / CEREBRO | `curador-seto` | `BLOCK_PUBLICATION` |
| 12 | carpeta promts / INBOX operativo | `curador-seto` | `REVIEW` |
| 13 | OSIT Resource Optimizer | `wabi-sabi-sentido-comun` + `claudio-local-autonomy` | `REVIEW_POLICY_ONLY` |
| 14 | limpieza PSI + CLAUDIO researchs | `curador-seto` | `REVIEW_NO_DELETE` |
| 15 | Matrix / Biblioteca / Mission Control | `hormiguero-mission-control` | `REVIEW` |
| 16 | AI Browser | `claudio-local-agent` + `curador-seto` | `REVIEW_NO_WEB_ACTION` |
| 17 | Agentes especializados / ciudad Claudio | `hormiguero-mission-control` + `claudio-local-agent` | `REVIEW` |
| 18 | publicacion publica controlada | `publicacion-perfiles-observatorio` | `BLOCK_EXTERNAL` |
| 19 | Wave FC / DOCX QA | `publicacion-perfiles-observatorio` + `curador-seto` | `REVIEW_HOST_TOOLING` |
| 20 | cierre de sesion / handoff obligatorio | `claudio-local-agent` | `REVIEW` |

## ACCION EJECUTADA

- Leido el prompt maestro completo.
- Ejecutado Curador preflight sobre el prompt maestro.
- Refrescado `pending_review` raiz.
- Leidas reglas raiz `AGENTS.md`, COMMS, estados de agentes, snapshot pendiente, auditoria raiz disponible y continuidad Claudio.
- Ejecutado `host_observacionista.py --no-write`.
- Creado este reporte de coordinacion.
- Creado handoff COMMS correspondiente:
  `COMMS/handoffs/2026-05-06-agent-city-coordination.md`.
- Publicado evento local en:
  `COMMS/topics/agent-city-coordination.jsonl`.
- Enviado mensaje append-only a:
  `COMMS/inbox/claudio-local-agent.jsonl`.

## HANDOFF

- Siguiente prompt recomendado: `17. Prompt de continuidad: Agentes especializados / ciudad Claudio`.
- Criterio de cierre siguiente: Mission Control o reporte `docs/ops` debe mostrar agente, departamento, funcion, estado, gate, ultimo artefacto, dependencias, riesgos y solapamientos.
- Regla de ejecucion: ninguna accion externa ni privada; todo como lectura, COMMS, docs, tests y evidencia.
- Falsadores:
  - `pending_review` cambia y aparecen `selected_items` reales sin clasificacion.
  - COMMS validator falla.
  - Un agente intenta escribir fuera de `may_touch`.
  - Un carril `BLOCK` se ejecuta como `APPROVE`.
  - La coordinacion borra, mueve, publica o arranca daemons.
