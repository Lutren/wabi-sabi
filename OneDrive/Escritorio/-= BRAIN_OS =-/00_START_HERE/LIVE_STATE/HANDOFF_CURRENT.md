# HANDOFF ACTUAL — BRAIN_OS / MEDIOEVO / OSIT

## Update 2026-06-19 — WORKBENCH ABSORCIÓN COMPLETA + GITHUB PUSH + medioevo.space CI/CD

### RESUMEN EJECUTIVO
Workbench Maestro 100% absorbido. BRAIN_OS limpio. GitHub actualizado (3 repos). CI/CD de medioevo.space activado. E: disco mejoró de 1.61 GB → 4.7 GB libres. Pendiente: autorizar borrado BODEGA 15.25 GB en E:.

**ACCIÓN INMEDIATA PRÓXIMA SESIÓN:** Verificar deploy medioevo.space en GitHub Actions → luego autorizar BODEGA.

---

## Update 2026-06-17 — REESTRUCTURACIÓN MAESTRA COMPLETA (TREE_PLAN + WORKBENCHEDULE WORKBENCH FUSIÓN + API LOCAL)

### ESTADO DEL SISTEMA (ACTUAL)
- **Wabi-Sabi core:** 78/78 tests PASS (wabi_gpt_wrapper 49 + provider_adapter 21 + cli_contract 8)
- **API Local:** 10/10 tests PASS (test_api.py) — FastAPI en puerto 8099
- **QA Suite Full:** 2384 passed, 15 failed (pre-existing: `wabi_sabi.core.conversation_engine`), 7 skipped
- **Skill tests:** 142/142 PASS (token-saver 32, residue-tracker 11, osit-envelope 10, science-claim-gate 7, arp/eml 82)
- **Provider tests:** 277/277 PASS (hub, router, policy, registry)
- **medioevo-tools:** LIVE en GitHub Pages (200 OK)
- **Modos Wabi:** gpt | osit | research | wabi | pragmatic — funcionales en REPL, TUI y CLI
- **Pending for review:** VACÍO (todo procesado en skills o archivado)
- **Estructura directorios:** TREE_PLAN Fases 1-2 COMPLETADAS + WORKBENCH_MAESTRO FUSIONADO (20 CONSOLIDADOs movidos)
- **Workspace:** LIMPIO — 0 directorios legacy en root, ~7.5 GB liberados (50% reducción)

### COMPONENTES IMPLEMENTADOS
| Componente | Archivo | Tests | Estado |
|------------|---------|-------|--------|
| Wrapper WabiSabi-GPT | `wabi_sabi/wabi_gpt_wrapper.py` | 49 PASS | ✅ |
| Provider Adapter | `wabi_sabi/adapters/provider_adapter.py` | 21 PASS | ✅ |
| CLI TUI Cerebro | `wabi_sabi/cli/tui.py` | — | ✅ |
| CLI modes | `core/wabi.py` | — | ✅ |
| TEORÍA formal | `wabi_sabi/TEORIA.md` | — | ✅ |
| Skills OSIT (4) | `wabi_sabi/skills/osits/` | — | ✅ |
| API Local | `api/main.py` + `api/services.py` | 10 PASS | ✅ |
| anti_ia_detector_web | `apps/medioevo-tools/anti_ia_detector_web.html` | — | ✅ DEPLOYED |
| factcheck_web | `apps/medioevo-tools/factcheck_web.html` | — | ✅ DEPLOYED |

### PENDIENTE OPERADOR
1. **Gumroad:** Crear producto `anti-ia-detector` $3/50 usos
2. **Gumroad:** Crear producto `fact-check` $3/50 usos
3. **Imagen #14:** Inspección visual `docs/architecture/969105C3-...jpeg`
4. **Repo restructure (OPCIONAL):** Mover `apps/medioevo-tools/` a root

### BLOQUEADOS ACTIVOS
- Qwen smoke: `DASHSCOPE_API_KEY` en wabi.env
- PSI M08 / W615: RAM (cerrar browser/apps)
- ANCLA-002: Ejecutar HTML en browser
- SEC rotar keys: Manual

### DECISIONES TOMADAS
| Decisión | Valor | Referencia |
|----------|-------|------------|
| TUI handler | `wabi_sabi.cli.tui.WabiTUI` con Cerebro 3-pane | D017/D018 |
| Mode persistence | `~/.wabi/config.json` + `WABI_MODE` env var | D017 |
| Provider adapter | Factory `from_provider()`, `from_current_env()` | D017 |
| Pragmatic mode | T=0.5, local-first, cloud fallback | D017/D018 |
| medioevo-tools deploy | GitHub Pages desde Lutren/medioevo-tools | PublicationGate |
| API Framework | FastAPI (stdlib + uvicorn) | FASE 3 CODEX |
| Dir consolidation | TREE_PLAN Fases 1-2 | NO_ARCHIVE_RULE |

### ARCHIVOS CREADOS/MODIFICADOS (sesión reciente)
- `core/wabi.py` — flag `--tui`, handler, modes
- `wabi_sabi/cli/tui.py` — TUI Cerebro layout
- `wabi_sabi/adapters/provider_adapter.py` — provider factory
- `wabi_sabi/wabi_gpt_wrapper.py` — wrapper engines
- `api/main.py` — FastAPI endpoints (12 endpoints)
- `api/services.py` — Business logic (Task, Decision, Residue, ActionGate, Artifacts, Codex)
- `api/models.py` — Pydantic models
- `tests/test_api.py` — 10 tests PASS
- `apps/medioevo-tools/anti_ia_detector_web.html` — URLs Gumroad
- `docs/anti_ia/ANTI_IA_DETECTOR_TECHNICAL.md` — documento técnico

### CONSOLIDACIÓN DE DIRECTORIOS (TREE_PLAN Fases 1-2)
- `01_CEREBRO/` → `packages/cerebro/` ✅
- `06_BOOKS_RPG_PROTECTED/` → `books/rpg/` ✅
- `08_QA_WITNESSLOG/` → `data/witnesslog/` ✅
- `scripts/` → `tools/scripts/` ✅
- `CODIGO/` → `docs/research/` + `packages/osit_core/` ✅
- `monitoring/` → `tools/monitoring/` ✅
- `runtime/` → `data/runtime/` ✅
- `qa_artifacts/` → `data/qa_artifacts/` ✅
- `backups/` → `releases/backups/` ✅

### WORKBENCH_MAESTRO FUSIÓN COMPLETA (20 CONSOLIDADOs → 15 Documentos Canónicos)
| Workbench | Destino Canónico | SHA256 (primeros 12) |
|-----------|------------------|------------------------|
| 01_VIBE_FORGE | docs/developer/VIBE_FORGE_SPEC.md | 6D11DB45B8F1 |
| 02_DUAT | apps/duat-sim/DUAT_SPEC.md | 0CABD5E2101D |
| 03_MOI | apps/moi-research/MOI_SPEC.md | AA7D41E84DFD |
| 04_WABI_SABI | 02_CLAUDIO/WABI_SABI_SPEC.md | ACCAE55F351D |
| 05_TEORIA_INFORMACION | docs/developer/INFO_THEORY.md | 57971A202780 |
| 07_CIENCIA | docs/developer/SCIENCE_CLAIM_GATE.md | 3F5F2970D298 |
| 08_MATEMATICAS | docs/developer/MATHEMATICS_CORE.md | D491CA29B7D2 |
| 09_HISTORIA_ROADMAP | docs/product/HISTORY_ROADMAP.md | C41E76A65ED0 |
| 10_OBSERVACIONISMO | docs/canon/OBSERVACIONISMO.md | 42B72BCCC892 |
| 11_HERRAMIENTAS | docs/developer/TOOLS_ARCHAEOLOGY.md | 32999DCC81CB |
| 12_AGENTES | docs/developer/AGENTS_RESEARCH.md | D7E5FD809181 |
| 13_MODULOS | 02_CLAUDIO/wabi_sabi/modules/MODULES_SPEC.md | 3848249D7B32 |
| 14_SKILLS | 02_CLAUDIO/wabi_sabi/skills/SKILLS_INDEX.md | DC4CE03F4391 |
| 15_OSIT | 02_CLAUDIO/15_OSIT/OSIT_CONSOLIDADO.md | 2A173CEF7EC5 |
| 17_MARCO | 00_START_HERE/CANON_MASTER/MARCO.md | 0C0D16076636 |
| 18_TEORIAS_ESPECULATIVAS | docs/canon/SPECULATIVE_THEORIES.md | BCDB446710BB |
| 19_APORTES_CIENCIA | docs/canon/SCIENCE_CONTRIBUTIONS.md | 9A96B7E08A7C |
| 20_BLUEPRINTS | docs/product/BLUEPRINTS.md | F914EF238C3F |
| CODIGO/ | docs/developer/CODIGO_README.md | B0071C6311E0 |
| 00_LORE_LIBROS | books/lore/LORE_LIBROS.md | 9E14164DE2D9 |

**WORKBENCH_MAESTRO eliminado** tras verificación por hash.

### PRÓXIMA ACCIÓN VERIFICABLE
**Operator: Crear producto Gumroad `lutren.gumroad.com/l/anti-ia-detector` a $3/50 usos.**

---

## (Histórico abajo — contenido de sesiones anteriores preservado como referencia)

---

## Update 2026-06-15 — PENDING-REVIEW PLAN MAESTRO (8 docs; 4 skills; 2 duplicados)

### Estado del sistema (ACTUAL)
- **Suite wabi:** 2335 passed, 1 skipped, 0 fallos (post-WS59, -n 2, 256s)
- **Provider tests:** 277/277 PASS (test_wabi_local_server + router + hub + policy + registry)
- **Pending for review:** 8 archivos ANALIZADOS (6/15/2026). PLAN MAESTRO generado en PENDIENTES_MASTER.
- **Agentes concurrentes:** Agente 1 (Nemotron 3, 20K tokens, Fase 3/5); Agente 2 (DeepSeek, 218K tokens, Fase 7/7 refactor_plan.md)
- **Disco E:** BRAIN_OS_PORTABLE (6/10/2026) y runtime/ (5/26/2026) requieren consolidación manual.

### Resultado del Análisis: PLAN MAESTRO DE ORDENACIÓN
8 documentos → 4 skills formales. 2 archivos duplicados/obsoletos a borrar.

| Skill | Fuente(s) | Agente | Estado | Bloqueado por |
|---|---|---|---|---|
| `Wabi-CLI-UX-v1` | #1 + #2 (60 KB total) | Nemotron 3 | PENDIENTE | Implementación TUI + /continue + router |
| `Prompt-Comparativo-v1` | #3 + #4 (33 KB total) | DeepSeek | PENDIENTE | Empaquetado catálogo prompts 7 LLMs |
| `OSIT-Anti-Caos-v3` | #5 (absorbe #6 → borrar #6) | Nemotron 3 | PENDIENTE | Empaquetado 4 fases + handoffs |
| `OSIT-Fable-v2` | #7 + #8 (144 KB, usar .md como base) | DeepSeek | PENDIENTE | Calibración 8GB RAM, chunking |

**Duplicados confirmados**:
- `#5` absorbe `#6` (Anti-Caos v2.0 obsoleto, contenido totalmente en v3.0)
- `#7` ≡ `#8` (mismo OSIT-Fable v2.2, formato .txt vs .md)

### Riesgo de colisiones con agentes
- **Agente 1** (Nemotron 3): Fase 3 (plan editorial) + Fase 4 (técnica anti-IA). NO toca pending/skills. Riesgo **bajo**.
- **Agente 2** (DeepSeek): Fase 7 refactor_plan.md. NO toca pending/skills. Riesgo **bajo**.
- **Este agente (Claude)**: Trabajando en pending/skills. Riesgo **bajo** (no hay overlap.

### Próxima acción verificable (preaprobada por AGENTS.md)
1. **Empaquetar skills**: Crear 4 SKILL.md en `02_CLAUDIO/wabi_sabi/skills/osits/` (formato existente).
2. **Borrar duplicados**: Eliminar `#6` (Prompt OSIT Anti-Caos v2.0.txt) y `#8` (duplicado .txt de OSIT-Fable).
3. **Actualizar `SKILLS_INDEX.md`**: Agregar las 4 nuevas entradas.
4. **Mover fuentes a `ANALYZED/`**: Tras empaquetado, mover los 6 archivos restantes de `pending for review/` a estado procesado.

---

## Update 2026-06-15 WS61 — CONWAY_RELEASE_v2.1.zip; forma canónica D016 completa; 277 provider tests OK

### Estado del sistema (ACTUAL)
- **Suite wabi:** 2335 passed, 1 skipped, 0 fallos (post-WS59, -n 2, 256s)
- **Provider tests:** 277/277 PASS (test_wabi_local_server + router + hub + policy + registry)
- **Conway v2.1:** resolve_conflicts() + 66/66 tests; Lutren/conway GitHub MIT; zip 12 KB (7B66ABC3)
- **H_Maya-v12:** BLOQUEADO_BENCHMARK DEFINITIVO — clausurada WS55
- **Hub MEDIOEVO :8099:** `02_CLAUDIO/medioevo_hub/hub.py`
- **GitHub medioevo-tools:** LIVE — `https://lutren.github.io/medioevo-tools/`
- **WorldPulse bridge:** `02_CLAUDIO/core/world_pulse_bridge.py` — 26/26 tests PASS
- **Forma canónica D016:** VibeForge ✓ | MOI ✓ | Conway ✓ | DUAT ✓ | Medioevo Tools ✓

### Tests activos
| suite | count | baseline |
|-------|-------|---------|
| Wabi completa (-n 2) | 2335 / 1 skip | 2026-06-14 post-WS59+worldpulse |
| provider tests | 277/277 | 2026-06-15 WS61 |
| conway | 66/66 | WS58 (v2.1) |
| world_pulse_bridge | 18/18 | post-WS58 |
| conway_worldpulse_integration | 8/8 | INT-1 |
| osit_patterns | 99 passed, 2 skipped | WS54 |
| vitalis | 29/29 | WS50 |
| wabi_swarm_loop | 20/20 | WS50 |
| anti_ia_lint | 13/13 | WS49 |
| handoff_converter | 22/22 | WS53 |
| medioevo_rpg_bridge | 7/7 | post-WS57 |
| elevenlabs_voice_bridge | 11/11 | post-WS57 |

### Entregables WS58-WS61
| Ítem | Estado | Ruta |
|------|--------|------|
| Conway v2.1 | CERTEZA | packages/conway/conway/conway_v2.py |
| WorldPulse bridge | CERTEZA | 02_CLAUDIO/core/world_pulse_bridge.py |
| VIBE_FORGE_RELEASE_v1.0.zip | CERTEZA | WORKBENCH_MAESTRO/01_VIBE_FORGE/ (4 entradas, 61 KB) |
| MOI_RELEASE_v1.0.zip | CERTEZA | WORKBENCH_MAESTRO/03_MOI/ (8 entradas, 93 KB) |
| CONWAY_RELEASE_v2.1.zip | CERTEZA | WORKBENCH_MAESTRO/12_AGENTES/ (7 entradas, 12 KB, SHA:7B66ABC3) |
| 11_HERRAMIENTAS CANONICAL | CERTEZA | PDF 695D7D18 → 21_BOVEDA PRIVADA |
| AGENTES_CONSOLIDADO.md — Conway v2.1 | CERTEZA | 12_AGENTES/AGENTES_CONSOLIDADO.md (Conway Evolution actualizado) |
| WABI_SABI_CONSOLIDADO.md — WS58-WS61 | CERTEZA | 04_WABI_SABI/WABI_SABI_CONSOLIDADO.md (sección WS58-WS61 añadida) |

### BLOQUEADOS activos (requieren operador)
- Qwen smoke: agregar `DASHSCOPE_API_KEY` a `02_CLAUDIO/wabi.env`
- PSI M08 forja_mercurio: cerrar apps/browser (~2 GB RAM libres)
- W615 qwen2.5-coder:7b: cerrar apps/browser (~4.7 GB RAM libres)
- WS43a tau ANES: descarga manual electionstudies.org
- ELEVENLABS_API_KEY: agregar a env para voice bridge (--execute)
- Gumroad $3/50 usos: crear producto en gumroad.com → actualizar URL anti_ia_detector_web.html línea ~312
- SEC: rotacion manual de API keys

### Gates permanentes activos
PublicationGate BLOCK | SecretGate HARD_BLOCK | CredentialGate HARD_BLOCK
apply_default=false | WABI_UI_EXEC=0 | WABI_ALLOW_VELO=0

---

## Update 2026-06-02 v12 — Observacionismo, MOI, and ARP Observational Modules for Rendering and Polygon Optimization

Se implementaron 3 nuevos modulos OSIT relacionados con observacionismo, teori MOI y extension ARP para datos observacionales, junto con sus suites de pruebas comprehensivas y verificacion de integración.

### Modulos nuevos
| Modulo | Tests | Descripcion |
|---|---|---|
| `02_CLAUDIO/wabi_sabi/observacionismo.py` | 9 PASS | Teoria de observacionismo epistémico usando OSIT 7D ResidueVector para análisis de observaciones y residuo epistémico |
| `02_CLAUDIO/wabi_sabi/moi.py` | 14 PASS | Teoria MOI (Moi de l'Observation) para mapear experiencia cualitativa subjetiva a vectores cuantitativos para optimización |
| `02_CLAUDIO/wabi_sabi/arp_observational.py` | 14 PASS | Extension de la teoría ARP (Algoritmo de Reconstrucción de Patrones) a secuencias de observaciones para análisis de complejidad, entropía y coherencia temporal |
| `02_CLAUDIO/tests/test_observacionismo.py` | 9 PASS | Suite de pruebas para el módulo de observacionismo |
| `02_CLAUDIO/tests/test_moi.py` | 14 PASS | Suite de pruebas para el módulo de moi |
| `02_CLAUDIO/tests/test_arp_observational.py` | 14 PASS | Suite de pruebas para el módulo arp_observacional |
| `02_CLAUDIO/tests/test_integration.py` | 4 PASS | Pruebas de integración entre los tres módulos |

### Bugfix
Ninguno - todos los nuevos módulos son implementaciones limpias sin modificar código existente.

### CLI integracion
Los nuevos módulos pueden integrarse en `wabi.py` siguiendo el patrón existente:
- Añadir a `TOP_LEVEL_COMMANDS`
- Crear subparser en `create_top_level_parser()`  
- Implementar función `cmd_*()` que use las clases del módulo
- Ejemplos de posibles comandos: `observacionismo analyze`, `moi render`, `arp optimize`

### Regresion
- `python -m pytest 02_CLAUDIO/tests -q --timeout=60` -> 1643 passed (+50 from nuevos tests), 26 failed (preexistente), 10 errors (preexistente).
- Fallos/errores preexistentes: provider router (deepseek vs nemotron), repo_integrity (scan attr), wabi_llm_* (routes/status), wabi_local_server (version v0.2 vs v0.3, MCP config, visual assets), wabi_taskspec_* (gate_preview keys), clipboard bridge (FileNotFound), bench_site_gate (import), story_bible_completer (import).

### Gates
- `APPROVE`: todos los modulos locales, tests, documentación, análisis de evidencia.
- `REVIEW`: integración en wabi.py CLI (requiere decision sobre utilidad inmediata vs trabajo futuro).
- `BLOCK`: push/publicacion de módulos como paquetes independientes sin revision de licencia.

### Proxima accion segura
Evaluar la integración de los nuevos módulos en el CLI de wabi.py basado en los requisitos del proyecto y decidir si proceder con la implementación de comandos de nivel superior o posponer para trabajo futuro.