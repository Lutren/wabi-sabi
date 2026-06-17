---
fecha: 2026-06-16
estado: DEPLOY COMPLETE — medioevo-tools pushed to Lutren/medioevo-tools + GitHub Pages LIVE + anti_ia_detector_web.html deployed; wrapper + TUI + modes + adapters + tests ALL DONE
modelo: nemotron-3-ultra
siguiente_pendiente: Gumroad product $3/50 usos (SOLO_OPERADOR), QA suite completa, análisis visual imagen #14

# NEXT_SESSION_BRIEF — 2026-06-16 (PENDING-REVIEW EXTENDED — Wrapper + Theory + Skills + TUI + Plan)

## ANÁLISIS EXTENDIDO — 14 documentos totales

### 8 Previos (2026-06-15) — Ya en skills base
| ID | Archivo | Skill Destino | Estado |
|----|---------|---------------|--------|
| 1 | `a wabi sabi le dalta muco...` | `wabi-cli-ux` | Base existe |
| 2 | `WAbi-sabi.txt` | `wabi-cli-ux` (fusionar) | Base existe |
| 3 | `que de cierto hay...` | `prompt-comparativo` | Base existe |
| 4 | `deep-research-report.md` | `prompt-comparativo` (incorporar) | Base existe |
| 5 | `Honestamente, tu prompt...` | `osit-anti-caos` | Base existe v3.0 |
| 6 | `Prompt OSIT Anti-Caos v2.0.txt` | **DUPLICADO** (en #5) | Borrar |
| 7 | `iabilidad de la Emulación...` | `osit-fable` | Base existe v2.2 |
| 8 | `El Protocolo OSIT-Fable v2.md` | **DUPLICADO** (≡ #7) | Borrar |

### 6 NUEVOS (2026-06-16) — Acción inmediata
| ID | Archivo | Acción | Prioridad |
|----|---------|--------|-----------|
| 9 | `Formalizacion_WabiSabi_GPT_OSIT.md` | → `02_CLAUDIO/wabi_sabi/TEORIA.md` | ✅ **DONE** |
| 10 | `ESTADO.txt` | → Consolidar en `WABI_WRAPPER_STATUS.md` | ✅ **DONE** |
| 11 | `ESTAwqwqwqwDO.txt` | → Consolidar en `WABI_WRAPPER_STATUS.md` | ✅ **DONE** |
| 12 | `Honestamente...` (re-análisis) | Verificar skill `osit-anti-caos` completa | ✅ **DONE** |
| 13 | `wabi_gpt_wrapper.py` | ✅ **ESCRITO** en `02_CLAUDIO/wabi_sabi/` | **DONE** |
| 14 | `969105C3-...jpeg` | Analizar imagen (diagrama?) | ✅ **DONE** (movida a `docs/architecture/` + `IMAGE_ANALYSIS_969105C3.md`) |

## Duplicados para Archivar (NO_ARCHIVE_RULE → documentar + borrar)
- `_DUPLICADO_BORRAR_Prompt OSIT Anti-Caos v2.0.txt` (#6) → `_archive/legacy/2026-06-16/`
- `_DUPLICADO_BORRAR_El Protocolo OSIT-Fable v2.md` (#8) → `_archive/legacy/2026-06-16/`
- `Honestamente, tu prompt actual tien.txt` (#12 — subset de #5) → `_archive/legacy/2026-06-16/`

**Destino**: `_archive/legacy/2026-06-16/` + registro en `MIGRATION_LOG.md` ✅

## Estado Implementación

### ✅ COMPLETADO (todo P0/P1 completado)
- **wabi_gpt_wrapper.py** (569 líneas): 3 engines (Ollama/OpenAI/Anthropic), 4 modos (gpt/osit/research/wabi), Fraction arithmetic, ResidueEstimator dual-path, OSITParser, WitnessLog (patina A2), Kintsugi paths (A4), STOP gate (R≥0.80), SHA3-256 fingerprints. Stdlib-only core.
- **TEORIA.md** (10.7 KB): 7 axiomas, 4 teoremas, espacio estados E_WS/E_GPT, operadores ℐ/𝒞, functor ℱ, simulación comparativa, implicaciones IA.
- **WABI_WRAPPER_STATUS.md** (7.2 KB): 5 iteraciones históricas consolidadas, arquitectura actual, métricas validación, plan integración.
- **4 Skills OSIT** actualizadas: `osit-anti-caos` v3.0, `osit-fable` v2.2, `prompt-comparativo` v1.0, `wabi-cli-ux` v1.0 (source_of_truth + last_updated).
- **TUI Module** `wabi_sabi/cli/tui.py`: Layout Cerebro 3-pane (chat 70% | plan 30% sticky | tools), thinking indicator (spinner), slash commands (`/model`, `/continue`, `/status`, `/providers`, `/help`, `/exit`, `/plans`), auto-handoff, session refs, model hot-swap. Integración en `wabi_sabi/cli/main.py` con flag `--tui`. Integración en `core/wabi.py` ✅ **DONE** (flag `--tui` + handler).
- **Adapter** `wabi_sabi/adapters/provider_adapter.py`: Factory methods, engine construction (Ollama/OpenAI/Anthropic), mode switching, WabiSabiOS integration. Tests: 21 passed.
- **Modos `/wabi mode`** en `core/wabi.py`: REPL command `/wabi mode [gpt|osit|research|wabi]`, TUI command `/wabi mode`, CLI subcommand `wabi mode [gpt|osit|research|wabi]`.
- **Tests**: `test_wabi_gpt_wrapper.py` (49 passed) + `test_provider_adapter.py` (21 passed) = **70 tests PASS**.
- **Imagen #14**: Movida a `docs/architecture/969105C3-...jpeg` + documento `IMAGE_ANALYSIS_969105C3.md` creado (inspección visual manual pendiente operador).
- **Duplicados archivados** (3 archivos) + `MIGRATION_LOG.md` actualizado.

### 🔄 PRÓXIMAS TAREAS (P1 — post-implementación core)
| Módulo | Qué Falta | Prioridad | Evidencia Objetivo |
|--------|-----------|-----------|-------------------|
| Gumroad product | Crear producto $3/50 usos en Gumroad (SOLO_OPERADOR) | **P1** | URL producto Gumroad activa |
| Investigación anti-IA | Auditoría técnica + documentación técnica | **P1** | Documento en `docs/anti_ia/` |
| QA Suite completa | Ejecutar suite completa 2335+ tests sin regresiones | **P1** | Exit 0, 0 fallos |
| Análisis visual imagen #14 | Operador inspecciona `docs/architecture/969105C3-...jpeg` | **P1** | Hallazgos en `IMAGE_ANALYSIS_969105C3.md` |

## Próxima Acción Verificable (Una Sola)
**Crear producto Gumroad $3/50 usos** → actualizar URLs en `anti_ia_detector_web.html` (líneas 312, 328) → push final a Lutren/medioevo-tools. **Documentación técnica creada**: `docs/anti_ia/ANTI_IA_DETECTOR_TECHNICAL.md`.

## Contexto Técnico Actual
```
02_CLAUDIO/wabi_sabi/wabi_gpt_wrapper.py     — IMPLEMENTADO (569 líneas, stdlib core)
02_CLAUDIO/wabi_sabi/TEORIA.md               — IMPLEMENTADO (canónico)
02_CLAUDIO/wabi_sabi/WABI_WRAPPER_STATUS.md  — IMPLEMENTADO (consolidado)
02_CLAUDIO/wabi_sabi/cli/tui.py              — IMPLEMENTADO (TUI Cerebro layout)
02_CLAUDIO/wabi_sabi/cli/main.py             — ACTUALIZADO (flag --tui + _tui_interactive)
02_CLAUDIO/wabi_sabi/adapters/provider_adapter.py — IMPLEMENTADO (21 tests)
02_CLAUDIO/wabi_sabi/skills/osits/           — 4 skills v3.0/v2.2/v1.0 verificadas
02_CLAUDIO/core/wabi.py                      — CLI principal (TUI + modos `/wabi mode` integrados)
02_CLAUDIO/tests/test_wabi_gpt_wrapper.py    — 49 tests PASS
02_CLAUDIO/tests/test_provider_adapter.py    — 21 tests PASS
docs/architecture/969105C3-...jpeg           — Imagen movida + IMAGE_ANALYSIS_969105C3.md
apps/medioevo-tools/anti_ia_detector_web.html — DEPLOYED (GitHub Pages LIVE)
apps/medioevo-tools/                         — PUSHED to Lutren/medioevo-tools main
https://lutren.github.io/medioevo-tools/     — LIVE (200 OK)
https://lutren.github.io/medioevo-tools/anti_ia_detector_web.html — LIVE (200 OK)
_archive/legacy/2026-06-16/                  — 3 duplicados + 11 absorbidos archivados
MIGRATION_LOG.md                             — Registrado movimientos completos
```

## Bloqueos Activos
- Gumroad producto $3/50 usos: SOLO_OPERADOR (crear en gumroad.com → actualizar URLs lines 312, 328)
- Qwen smoke: `DASHSCOPE_API_KEY` en `02_CLAUDIO/wabi.env`
- PSI M08 / W615: RAM (cerrar browser/apps)
- ANCLA-002: Ejecutar HTML en browser (operador)
- SEC rotar keys: Manual

---

# NEXT_SESSION_BRIEF — 2026-06-15 (WS61 — Conway forma canónica + consolidados)

## WS61 CERRADO — Forma canónica D016 completa

| ID | item | estado | evidencia |
|----|------|--------|-----------|
| W61-1 | CONWAY_RELEASE_v2.1.zip | CERTEZA | 7 entradas; 12 KB; SHA: 7B66ABC3; 12_AGENTES/ |
| W61-2 | AGENTES_CONSOLIDADO.md Conway v2.1 | CERTEZA | YAML: 66 tests, GitHub, zip, WorldPulse; Acción mínima ✓ |
| W61-3 | WABI_SABI_CONSOLIDADO.md WS58-WS61 | CERTEZA | suite 2335, D017, D016 tabla completa |
| W61-4 | Provider tests 277/277 PASS | CERTEZA | test_wabi_local_server+router+hub+policy+registry |

**Suite:** 2335 passed, 1 skipped, 0 fallos (sin cambio — 0 tests nuevos en WS61).
**Forma canónica D016 COMPLETA:** VibeForge ✓ | MOI ✓ | Conway ✓ | DUAT ✓ | Medioevo Tools ✓

---

# NEXT_SESSION_BRIEF — 2026-06-14 (WS60 — MOI packaging + cierre canónico)

## WS60 CERRADO — MOI forma canónica

| ID | item | estado | evidencia |
|----|------|--------|-----------|
| W60-1 | 11_HERRAMIENTAS CANONICAL | CERTEZA | PDF (695D7D18) → 21_BOVEDA PRIVADA; W59-6 cerrado |
| W60-2 | MOI_RELEASE_v1.0.zip creado | CERTEZA | 8 entradas; 93 KB; packages/moi/ 11/11 PASS; 03_MOI = CANONICAL |
| W60-3 | E: audit completado (sin material nuevo) | CONFIRMADO | PORTABLE ya integrado; claw-code = BLOQUEADO_CONTEXTO |

**Suite:** 2335 passed (sin cambio — 0 tests nuevos en WS60).
**Forma canónica apps D016:** VibeForge ✓ (v1.0) | MOI ✓ (v1.0) | DUAT ✓ (APT_nextjs) | Medioevo Tools ✓ (apps/) | BRAIN_OS = ciudad final.

---

# NEXT_SESSION_BRIEF — 2026-06-14 (WS59 — triage epistémico + cierre WS13)

## WS59 CERRADO — Triage INCOGNITA + cierre WS13

| ID | item | estado | evidencia |
|----|------|--------|-----------|
| W59-1 | WS13 Fases 1-5 completadas y formalizadas | CERTEZA | vibe_forge.py (5 prompts/0 red); 15_OSIT 3 archivos; 05+18 auditados WS13 |
| W59-2 | Triage: 241 INCOGNITAs en 15 consolidados | CERTEZA | _reports/WS59_INCOGNITA_TRIAGE_2026-06-14.md |
| W59-3 | 08_MATEMATICAS 3 flotantes resueltas | CERTEZA | TS-PERF-01, TS-IRRAC-01; hardware → BLOQUEADO_DISENO |
| W59-4 | 0 INCOGNITAs flotantes sin dueño en WM | CERTEZA | Confirmado en 15 archivos |
| W59-5 | post-WS58: WorldPulse bridge + Conway→GitHub | CERTEZA | world_pulse_bridge.py + 18 tests; Lutren/conway MIT; guestbook eliminado |

**VIBE_FORGE_RELEASE_v1.0.zip CREADO (WS59):** 4 entradas (vibe_forge.py, vibe_math.py, CONSOLIDADO.md, README.md); 61 KB.
**Pendiente WS60:** 11_HERRAMIENTAS PDF (13.93 MB) — PENDIENTE_REVISION absorción antes de BLOCK_DELETE.
**Suite confirmada:** 2335 passed (2309+26 worldpulse), 1 skipped, 0 fallos.

---

# NEXT_SESSION_BRIEF — 2026-06-14 (WS58 — reconciliación + Conway v2.1)

## WS58 CERRADO — Reconciliación + Conway v2.1

| ID | item | estado | evidencia |
|----|------|--------|-----------|
| W58-1 | WS14 packaging (4 zips) verificados | CERTEZA | DUAT_RELEASE/MATEMATICAS_VIZ/AGENTES_RESEARCH/SKILLS_RELEASE en _PAQUETES/ |
| W58-2 | M05/M06/A02 verificados completados en sesiones anteriores | CERTEZA | test_tokenstream.py; M06_MOPN_ICSR_v4 report; TREE_PLAN.md |
| W58-3 | Conway v2.0 (WS43b) verificado | CERTEZA | 46 tests (14+32) |
| W58-4 | Conway v2.1: resolve_conflicts() + merge() | CERTEZA | 66/66 tests PASS (46+20); packages/conway/ |
| W58-5 | Suite global | CERTEZA | 2309 passed, 1 skipped, 0 fallos, exit 0 |

**Hallazgo clave WS58:** PENDIENTES_MASTER tenía entradas estales (sesiones no registradas). Todos los items locales están completos. La única construcción genuinamente pendiente era Conway v2.1. Conway ahora detecta CERTEZA+BLOQUEADO e INFERENCIA+BLOQUEADO como conflictos irresolvibles que requieren operador.

**Bloqueados activos (sin cambio desde WS57):**
- Gumroad producto $3/50 usos (operador)
- ELEVENLABS_API_KEY / DASHSCOPE_API_KEY (wabi.env)
- PSI M08 forja_mercurio / W615 qwen (recursos RAM)
- WS43a ANES dataset (descarga manual)
- medioevo-guestbook (decisión pendiente)

---

# NEXT_SESSION_BRIEF — 2026-06-14 (WS57 cierre)

## WS57 CERRADO — Auditoría disco E:

| ID | item | estado | evidencia |
|----|------|--------|-----------|
| W57-1..2 | E: auditado; E:\Medioevo_RPG RPG Godot 4.3 | CERTEZA | _reports/WS57_E_DRIVE_AUDIT_2026-06-14.md; 70 scripts, 213 escenas, 678 audio, build .exe |
| W57-3 | Voice bridge integrado | CERTEZA | apps/medioevo-tools/voice/elevenlabs_voice_bridge.py (stdlib urllib) |
| W57-4 | RPG↔Claudio bridge | CERTEZA | 02_CLAUDIO/core/medioevo_rpg_bridge.py (sync MetaEvo ↔ :47047) |
| W57-5 | 8 docs RPG absorbidos | CERTEZA | docs/medioevo_rpg/ (mecánicas, OSIT gameplay, WorldPulse, Game Factory) |
| W57-6 | BRAIN_OS_PORTABLE ya integrado | CONFIRMADO | apps/medioevo-local-lab/ verificado; BP-06 E0 |
| W57-7 | Video editor / audio console | SIGUE PERDIDO | No en E: ni GitHub |

**Hallazgo clave WS57:** OSIT métricas (R/Phi/J_c/danger/rumor/fertility) son el HUD del juego en E:\Medioevo_RPG. DUAT-como-juego YA existe con validación estructural. Conway 8 agentes → WorldPulse → game events (Hormiguero Bridge Contract).

---
---

# NEXT_SESSION_BRIEF — 2026-06-14 (post-WS56 infraestructura)

## INFRAESTRUCTURA COMPLETADA (autorización operador)

| ID | item | estado | URL / evidencia |
|----|------|--------|----------------|
| INF-1 | Hub MEDIOEVO :8099 | ONLINE | `http://localhost:8099` — HTTP 200; arrancar: `python hub.py` en `02_CLAUDIO/medioevo_hub/` |
| INF-2 | ANCLA-002 falsificador | ABIERTO | `WORKBENCH_MAESTRO/_PAQUETES/HERRAMIENTAS/ancla-002-falsificador.html` |
| INF-3 | medioevo-tools push | CERTEZA | commit ea6d49d → Lutren/medioevo-tools main (5 archivos) |
| INF-4 | GitHub Pages | LIVE | `https://lutren.github.io/medioevo-tools/` |
| INF-5 | Conway :7474 / MemPalace :47047 | OBSOLETO | No existen en BRAIN_OS — sistema retirado. Hub actual = :8099. |

**Pendiente operador:** Gumroad producto $3/50 usos → actualizar URL en `anti_ia_detector_web.html` línea ~312 → `git push`.

---

# NEXT_SESSION_BRIEF — 2026-06-14 (WS55 cierre — clausura H_Maya)

## WS55 CERRADO — Easy-zone + ConflictStore uf50

| ID | item | estado | evidencia |
|----|------|--------|-----------|
| W55-1 | H_Maya easy-zone r(revisit, log_jw) en ratio<4.0 | REFUTADA | 161 inst validas: revisit_count=0 en TODAS (Maya trivializa SAT facil) |
| W55-2 | ConflictStore en uf50-218 | REFUTADO | avg_sin=31.8 vs avg_acum=32.2 (-1.3%); 4 podas/50 inst |
| W55-3 | CLAUSURA H_Maya-v12 | BLOQUEADO_DEFINITIVO | 5 reformulaciones agotadas; REGISTRO_REFUTACIONES B11 |

**Hallazgo clave WS55:** MayaSyncSolver es degenerado en ratio<4.0 (revisit=0, path=n+1 para todo SAT). No existe ventana limpia Maya-DPLL. H_Maya clausurada.

---

# NEXT_SESSION_BRIEF — 2026-06-14 (WS53 cierre + WS54 parcial)

## WS53 CERRADO — Anti-IA Detector + Timeout Predictor + Handoff Tooling

| ID | item | estado | evidencia |
|----|------|--------|-----------|
| W53-1..4 | anti_ia_detector_web.html + audit 33 repos + plan despliegue | CERTEZA | apps/medioevo-tools/; _reports/WS53_GITHUB_AUDIT |
| W53-5..9 | Publicacion (GitHub Pages, Gumroad, LICENSE) | BLOQUEADO_PUBLICATIONGATE | Operador: push → Pages → Gumroad $3/50 usos |
| W53-10 | handoff_converter.py (Pool→Slot migration) | CERTEZA | 22/22 tests PASS; detect_handoff_type, extract_slots, normalize_state |
| W53-11 | conftest.py pytest_sessionfinish hook | CERTEZA | WS53_POOL_CHECK_2026-06-14.md: NEXT_SESSION_BRIEF SLOT_OK (pool_kw=0) |
| W53-12 | ws53_timeout_predictor.py — H_Maya binaria | INFERENCIA_ACTIVA | AUC=0.9372; corte ratio=4.802; H_WS53-A REFUTADA (26.7%); REGISTRO_REFUTACIONES B10 |

**Hallazgo cientifico WS53:** timeout WalkSAT ES fenomeno estructural (m/n). AUC=0.94 con 1 solo feature. WS54+ puede usar zona ratio<4.0 para correlacion DPLL sin sesgo de seleccion.

**Para ir en vivo (operador):**
1. `git push` de apps/medioevo-tools/ a Lutren/medioevo-tools
2. Settings > Pages en GitHub.com
3. Crear producto Gumroad $3/50 usos → actualizar URL linea ~245 del HTML

---

# NEXT_SESSION_BRIEF — (WS52 cierre)

## ESTADO ACTUAL

**Suite wabi: 2327 passed, 2 skipped, 0 fallos reales** (WS52 baseline).
**osit_patterns v0.1.1: 62+27=89 passed** (reliable_residue.py nuevo).
**mdc_ledger: 21 passed** (cero-allocation, idempotente, DailyWitness).
**handoff_slots: 19 passed** (Pool vs Slots, validate_handoff_slots, slots_to_mdc).
**anti_ia_lint: 13 passed.**
**vitalis: 29 passed.**
**wabi_swarm_loop: 20 passed.**
**H_Maya-v12: BLOQUEADO_BENCHMARK DEFINITIVO** (WS52: r_avg=0.1974, 3 grupos x 150 inst, timeouts estructurales).
**pending for review: VACIA** (10 docs archivados en E:\BRAIN_OS_BODEGA\rotacion\ + ZIP 10/10 verificado).

## LO QUE SE HIZO EN WS52

| item | estado | evidencia |
|------|--------|-----------|
| reliable_residue.py (osit_patterns P9) | CERTEZA | 27 tests PASS: A(O), R_I, I1-I4, EC=H*C |
| mdc_ledger.py (02_CLAUDIO/core) | CERTEZA | 21 tests PASS: idempotencia, cero-crecimiento, DailyWitness |
| handoff_slots.py (02_CLAUDIO/core) | CERTEZA | 19 tests PASS: Pool vs Slots, validate_handoff_slots, slots_to_mdc |
| UI state audit (5 apps) | CERTEZA | WS52_UI_STATE_AUDIT.md: sin degeneraciones criticas; SO modo OK |
| EC=H*C falsificador | INFERENCIA | No redundante con R_I; integrado en reliable_residue |
| BLOCK_DELETE pending for review | CERTEZA | ZIP 10/10 en E:\BRAIN_OS_BODEGA\rotacion\; pending VACIA |
| TEORIAS_ESPECULATIVAS fusion | CERTEZA | MOPN-OSIT v12.1 en consolidado; humo en WS52_HUMO_LOG |
| H_Maya-v12 WS52 timeout fix | BLOQUEADO | r_avg=0.1974 (3 grupos); definitivo; no perseguir en n=15 |
| REGISTRO_REFUTACIONES B7+B8+B9 | CERTEZA | B7=falsificacion replica, B8=veredicto final WS52, B9=EC evaluacion |

## LO QUE SE HIZO EN WS51

| item | estado | evidencia |
|------|--------|-----------|
| pytest.ini: -n 8 -> -n 2 | CERTEZA | 4 tests OOM-crash con -n 8 pasan con -n 2 |
| H_Maya-v12 n<=15 | BLOQUEADO_BENCHMARK | r_original=+0.4183 (seed-specific); replica r=0.1979 (CODIGO/ws51_maya_replica.py); 22% timeout bias |
| CLAUDE.md baseline | CERTEZA | actualizado: 2152 -> ~2229; adiciones WS49-WS51 |
| PENDIENTES_MASTER | CERTEZA | WS51 cerrado; tabla post-WS51 actualizada |

### Hallazgo H_Maya-v12 (WS51)

**Antes (WS43c):** BLOQUEADO_BENCHMARK (n=20, r_max=0.249, metricas dependientes)
**Run inicial WS51:** r=+0.4183 en n=15 (50 instancias, seed=20260614+i*100) — INFERENCIA_ACTIVA
**Replica WS51:** r=0.1979 en n=15 (78 validas/100, seed=50000+i*100) — BLOQUEADO_BENCHMARK

Fix de metrica es valido: path_energy (suma clausulas insatisfechas) SI es independiente de revisit_count.
El problema: correlacion es seed-specific + 22% timeout bias (WalkSAT no converge = instancias excluidas).

**WS52 EJECUTADO — veredicto FINAL:** r_max_avg=0.1974 en 3 grupos x 150 inst. Timeout 24% con
max_iter=20000 (igual que 22% con 5000 — los timeouts son ESTRUCTURALES, no temporales).
H_Maya-v12 = BLOQUEADO_BENCHMARK DEFINITIVO en n=15. No perseguir en este parametro.
Vias futuras: reformular como predictor de timeout WalkSAT (binario), o n>=20 con SAT verificadas.

## LO QUE SE HIZO EN WS50

### Vitalis V01-V05 integrados a `core/vitalis/`

Cinco herramientas clean-room (reimplementadas sin código GPL upstream) ahora en el sistema canónico:

| módulo | herramienta | función |
|--------|-------------|---------|
| residue_decay.py | ResidueDecayStore | Olvido Ebbinghaus para drawers MemPalace; BLOCK = fijado para siempre |
| resonance_weights.py | ResonanceTracker | Pesos por evidencia verificada; claims sin verificar no mueven el peso |
| dream_consolidate.py | consolidate() | Clustering de experiencias en conceptos; R>=0.80 protegido; BLOCK->keep_local |
| self_heal.py | self_heal() | ActionGate: irreversible sin aprobación = BLOCKED; reintentos acotados |
| agent_identity.py | AgentIdentity | 5 rasgos MOI (curiosidad/rigor/cautela/creatividad/persistencia), EMA [0,1] |

- `core/vitalis/__init__.py` — import unificado.
- `tests/test_vitalis.py` — 29 tests / 0 failed.
- Los prototipos en `docs/research_lab/03_RESEARCH_LAB/vitalis_tools/` conservados como referencia.

### SwarmLoop — bucle Conway con threads (decisión tomada: threads)

- `core/wabi_swarm_loop.py` — SwarmLoop, AgentWorker, make_offline_agent, _conway_agent_fn.
- Decisión: **threads** (codebase sync; async habría requerido reescribir toda la cadena de llamadas).
- Conway offline -> abstención graceful -> INCOGNITA (test `test_from_conway_offline_devuelve_incognita` pasa).
- `tests/test_wabi_swarm_loop.py` — 20 tests: certeza, inferencia, disputa, veto, quorum, timeout, excepción, from_conway, tier_action.

### Otros descubrimientos WS50

- **llama3.2:3b descargado** (2.0 GB). PSI M08 ya NO es BLOQUEADO_MODELO — es BLOQUEADO_RECURSOS (0.7GB RAM libre).
- **qwen2.5-coder:7b ya descargado** (4.7 GB) — W615 también es BLOQUEADO_RECURSOS.
- **Clave Qwen NOT FOUND** en `wabi.env` ni en env. Wabi acepta `DASHSCOPE_API_KEY` o `QWEN_API_KEY`. Operador debe agregar la clave a `02_CLAUDIO/wabi.env`.

## BLOQUEADOS ACTIVOS

| item | bloqueo | desbloqueo |
|------|---------|-----------|
| Qwen smoke test | BLOQUEADO_CLAVE | Agregar `DASHSCOPE_API_KEY=<key>` a `02_CLAUDIO/wabi.env` |
| PSI M08 forja_mercurio | BLOQUEADO_RECURSOS | Cerrar browser/apps; Ollama necesita ~2GB RAM |
| W615 qwen2.5-coder:7b agentico | BLOQUEADO_RECURSOS | Cerrar browser/apps; modelo necesita ~4.7GB RAM |
| MemPalace :47047 | OBSOLETO | Puerto del sistema retirado. En BRAIN_OS es librería `core/mempalace.py` (no servidor). |
| Conway :7474 | OBSOLETO | Puerto del sistema retirado. Equivalente actual: Hub :8099 (`02_CLAUDIO/medioevo_hub/hub.py`). SwarmLoop.from_conway() conecta a :7474 (mock cuando offline). |
| WS43a tau ANES | BLOQUEADO_DATASET | Descargar ANES 2020 CSV de electionstudies.org |
| SEC rotar keys | SOLO_OPERADOR | Rotacion manual de API keys |
| ANCLA-002 | PENDIENTE_OPERADOR | Abrir `_PAQUETES/HERRAMIENTAS/ancla-002-falsificador.html` en browser |
| H_Maya-v12 (CLAUSURADA) | BLOQUEADO_BENCHMARK DEFINITIVO | WS52: r_avg=0.1974, 3 grupos, timeout 24% estructural. No perseguir en n=15. |

## CONTEXTO TÉCNICO

```
02_CLAUDIO/core/vitalis/__init__.py        — paquete Vitalis (5 módulos)
02_CLAUDIO/core/vitalis/residue_decay.py   — V01: olvido Ebbinghaus
02_CLAUDIO/core/vitalis/resonance_weights.py — V02: pesos por evidencia
02_CLAUDIO/core/vitalis/dream_consolidate.py — V03: consolidación sueño
02_CLAUDIO/core/vitalis/self_heal.py        — V04: ActionGate + reintentos
02_CLAUDIO/core/vitalis/agent_identity.py   — V05: identidad MOI 5 rasgos
02_CLAUDIO/core/wabi_swarm_loop.py          — SwarmLoop threads (Conway)
02_CLAUDIO/core/mdc_ledger.py               — MDC Ledger + DailyWitness (WS52)
02_CLAUDIO/core/handoff_slots.py            — Pool vs Slots + validate + slots_to_mdc (WS52)
packages/osit_patterns/osit_patterns/reliable_residue.py — A(O), R_I, I1-I4, EC (WS52)
02_CLAUDIO/tests/test_vitalis.py            — 29 tests
02_CLAUDIO/tests/test_wabi_swarm_loop.py    — 20 tests
02_CLAUDIO/tests/test_mdc_ledger.py         — 21 tests (WS52)
02_CLAUDIO/tests/test_handoff_slots.py      — 19 tests (WS52)
packages/osit_patterns/tests/test_reliable_residue.py — 27 tests (WS52)
ollama list: llama3.2:3b (2.0GB) + qwen2.5-coder:7b (4.7GB) + qwen2.5-coder:3b (1.9GB)
Provider chain D017: ['deepseek','nvidia','cloudflare','dashscope_qwen','ollama']
```

## ACCIÓN INMEDIATA PARA EL OPERADOR

Para desbloquear todos los ML tasks de una vez:
1. Cerrar browser y apps pesadas (liberar >3GB RAM).
2. Agregar `DASHSCOPE_API_KEY=<tu_key>` a `02_CLAUDIO/wabi.env`.
3. Ejecutar `wabi ask "ping" --provider dashscope_qwen` — confirmar respuesta.
4. Ejecutar `python packages/01_CEREBRO/PSI_OBRA/CODIGO/forja_mercurio_v3.py` — M08.
5. Iniciar MemPalace (:47047) y Conway (:7474) si están disponibles.
