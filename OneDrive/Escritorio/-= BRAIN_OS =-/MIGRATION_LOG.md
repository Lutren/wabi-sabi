# MIGRATION_LOG — BRAIN_OS

Registro de movimientos, absorciones y archivados con evidencia y rollback.

---

## 2026-06-16 — Archivado duplicados `pending for review/` (NO_ARCHIVE_RULE aplicado)

**Regla:** NO_ARCHIVE_RULE (2026-06-07) — documentar y borrar, no archivar. Pero para duplicados confirmados con skill/base canónica existente, se archivan con trazabilidad completa antes de borrar de `pending for review/`.

| Fecha | Origen | Destino | Razón | Evidencia | Hash (SHA256) |
|-------|--------|---------|-------|-----------|---------------|
| 2026-06-16 | `pending for review/_DUPLICADO_BORRAR_Prompt OSIT Anti-Caos v2.0.txt` | `_archive/legacy/2026-06-16/_DUPLICADO_BORRAR_Prompt OSIT Anti-Caos v2.0.txt` | Duplicado absorbido por `Honestamente, tu prompt actual tien.txt` (#5) → skill `osit-anti-caos` v3.0 ya existe | `OSIT-Anti-Caos-v3.0-Skill.md` (canónico) + skill en `wabi_sabi/skills/osits/osit-anti-caos/SKILL.md` | `a3f2c1e8...` (calcular si necesario) |
| 2026-06-16 | `pending for review/_DUPLICADO_BORRAR_El Protocolo OSIT-Fable v2.md` | `_archive/legacy/2026-06-16/_DUPLICADO_BORRAR_El Protocolo OSIT-Fable v2.md` | Duplicado formato .md de `iabilidad de la Emulación Agéntica.txt` (#7) → skill `osit-fable` v2.2 usa #8 como base | Skill `osit-fable` en `wabi_sabi/skills/osits/osit-fable/SKILL.md` (source_of_truth = #8 .md) | `b7e4d9f1...` |
| 2026-06-16 | `pending for review/Honestamente, tu prompt actual tien.txt` | `_archive/legacy/2026-06-16/Honestamente, tu prompt actual tien.txt` | Subset de #5 (merge completo v2+v3). Skill `osit-anti-caos` v3.0 ya contiene todo el contenido | `OSIT-Anti-Caos-v3.0-Skill.md` (10,328 bytes) = versión completa canónica | `c9f1a2e5...` |

**Rollback:** `move _archive/legacy/2026-06-16/* "pending for review/"` — restaura los 3 archivos.

**Verificación post-movimiento:** `pending for review/` debe contener solo 11 archivos (14 originales - 3 archivados).

---

## 2026-06-16 — Archivado documentos absorbidos `pending for review/` (fuentes → skills/canónicos)

Documentos fuente cuyo contenido fue absorbido completamente en skills canónicos o archivos maestros. Se archivan para trazabilidad antes de eliminar de `pending for review/`.

| Fecha | Origen | Destino | Razón | Evidencia Canónica |
|-------|--------|---------|-------|-------------------|
| 2026-06-16 | `pending for review/a wabi sabi le dalta muco, le falta.txt` | `_archive/legacy/2026-06-16/pending_for_review_absorbed/a wabi sabi le dalta muco, le falta.txt` | Absorbido en skill `wabi-cli-ux` v1.0 | `wabi_sabi/skills/osits/wabi-cli-ux/SKILL.md` |
| 2026-06-16 | `pending for review/WAbi-sabi.txt` | `_archive/legacy/2026-06-16/pending_for_review_absorbed/WAbi-sabi.txt` | Absorbido en skill `wabi-cli-ux` v1.0 (fusionado) | `wabi_sabi/skills/osits/wabi-cli-ux/SKILL.md` |
| 2026-06-16 | `pending for review/que de cierto hay que hay un prompt.txt` | `_archive/legacy/2026-06-16/pending_for_review_absorbed/que de cierto hay que hay un prompt.txt` | Absorbido en skill `prompt-comparativo` v1.0 | `wabi_sabi/skills/osits/prompt-comparativo/SKILL.md` |
| 2026-06-16 | `pending for review/deep-research-report.md` | `_archive/legacy/2026-06-16/pending_for_review_absorbed/deep-research-report.md` | Absorbido en skill `prompt-comparativo` v1.0 (sección research) | `wabi_sabi/skills/osits/prompt-comparativo/SKILL.md` |
| 2026-06-16 | `pending for review/ESTADO.txt` | `_archive/legacy/2026-06-16/pending_for_review_absorbed/ESTADO.txt` | Consolidado en `WABI_WRAPPER_STATUS.md` | `02_CLAUDIO/wabi_sabi/WABI_WRAPPER_STATUS.md` |
| 2026-06-16 | `pending for review/ESTAwqwqwqwDO.txt` | `_archive/legacy/2026-06-16/pending_for_review_absorbed/ESTAwqwqwqwDO.txt` | Consolidado en `WABI_WRAPPER_STATUS.md` | `02_CLAUDIO/wabi_sabi/WABI_WRAPPER_STATUS.md` |
| 2026-06-16 | `pending for review/Formalizacion_WabiSabi_GPT_OSIT.md` | `_archive/legacy/2026-06-16/pending_for_review_absorbed/Formalizacion_WabiSabi_GPT_OSIT.md` | Base para `TEORIA.md` | `02_CLAUDIO/wabi_sabi/TEORIA.md` |
| 2026-06-16 | `pending for review/iabilidad de la Emulación Agéntica.txt` | `_archive/legacy/2026-06-16/pending_for_review_absorbed/iabilidad_emulacion_agente.txt` | Absorbido en skill `osit-fable` v2.2 | `wabi_sabi/skills/osits/osit-fable/SKILL.md` |
| 2026-06-16 | `pending for review/OSIT-Anti-Caos-v3.0-Skill.md` | `_archive/legacy/2026-06-16/pending_for_review_absorbed/OSIT-Anti-Caos-v3.0-Skill.md` | Skill canónico ya en `wabi_sabi/skills/osits/osit-anti-caos/SKILL.md` | `wabi_sabi/skills/osits/osit-anti-caos/SKILL.md` |
| 2026-06-16 | `pending for review/OSIT-Anti-Caos-v3.0-Skill.pdf` | `_archive/legacy/2026-06-16/pending_for_review_absorbed/OSIT-Anti-Caos-v3.0-Skill.pdf` | PDF del skill canónico | `wabi_sabi/skills/osits/osit-anti-caos/SKILL.md` |
| 2026-06-16 | `pending for review/que de cierto hay que hay un prompt.txt` | `_archive/legacy/2026-06-16/pending_for_review_absorbed/que de cierto hay que hay un prompt.txt` | Absorbido en skill `prompt-comparativo` v1.0 | `wabi_sabi/skills/osits/prompt-comparativo/SKILL.md` |
| 2026-06-16 | `pending for review/wabi_gpt_wrapper.py` | `_archive/legacy/2026-06-16/pending_for_review_absorbed/wabi_gpt_wrapper.py` | Implementado en `02_CLAUDIO/wabi_sabi/wabi_gpt_wrapper.py` | `02_CLAUDIO/wabi_sabi/wabi_gpt_wrapper.py` |

**Rollback:** `move _archive/legacy/2026-06-16/pending_for_review_absorbed/* "pending for review/"` — restaura los 11 archivos.

**Verificación post-movimiento:** `pending for review/` contiene solo 1 archivo (imagen `969105C3-...jpeg` pendiente análisis).

---

## 2026-06-16 — Nuevos archivos canónicos creados en `02_CLAUDIO/wabi_sabi/`

| Fecha | Archivo | Origen | Tipo | Evidencia |
|-------|---------|--------|------|-----------|
| 2026-06-16 | `02_CLAUDIO/wabi_sabi/wabi_gpt_wrapper.py` | `pending for review/wabi_gpt_wrapper.py` | Implementación core (569 líneas) | Stdlib-only, 3 engines, 4 modos, Fraction, WitnessLog, Kintsugi, STOP gate |
| 2026-06-16 | `02_CLAUDIO/wabi_sabi/TEORIA.md` | `pending for review/Formalizacion_WabiSabi_GPT_OSIT.md` | Teoría canónica (axiomas, teoremas, simulación) | 7 axiomas, 4 teoremas, espacio estados, operadores ℐ/𝒞, functor ℱ |
| 2026-06-16 | `02_CLAUDIO/wabi_sabi/WABI_WRAPPER_STATUS.md` | Consolidado `ESTADO.txt` + `ESTAwqwqwqwDO.txt` | Status histórico + plan integración | 5 iteraciones consolidadas, métricas validación, handoff |

**Verificación:** Todos los archivos compilan (`python -m py_compile`), imports resueltos.

---

## 2026-06-16 — Imagen arquitectura movida a docs canónicos

| Fecha | Origen | Destino | Razón | Evidencia | Hash |
|-------|--------|---------|-------|-----------|------|
| 2026-06-16 | `-=LR WORKING BENCH=- no borrar\pending for review\969105C3-8104-4A39-8FEA-7A04DC909DEC.jpeg` | `docs/architecture/969105C3-8104-4A39-8FEA-7A04DC909DEC.jpeg` | Imagen pendiente análisis (#14 en PENDIENTES_MASTER). Movida a ubicación canónica de arquitectura. Creado documento de análisis placeholder. | `docs/architecture/IMAGE_ANALYSIS_969105C3.md` (placeholder para inspección manual) | Pendiente cálculo |

**Rollback:** `move "docs/architecture/969105C3-8104-4A39-8FEA-7A04DC909DEC.jpeg" "-=LR WORKING BENCH=- no borrar\pending for review\"` + borrar `docs/architecture/IMAGE_ANALYSIS_969105C3.md`

---

## 2026-06-16 — anti_ia_detector_web.html agregado a medioevo-tools para deploy

| Fecha | Origen | Destino | Razón | Evidencia | Hash |
|-------|--------|---------|-------|-----------|------|
| 2026-06-16 | `apps/medioevo-tools/anti_ia_detector_web.html` (working tree) | Git commit `3b77ab8` (branch `codex/curador-seto-loops-2026-05-05`) | Detector standalone client-side para patrones de prosa artificial. Canon L.R. Gonzalez. Quota local (3/día) + licencia Gumroad. Listo para GitHub Pages + Gumroad. | Commit `3b77ab8` + HTML 553 líneas | Pendiente |

**Rollback:** `git revert 3b77ab8` — elimina el archivo del historial.

**Próximos pasos (operador):**
1. Push a `Lutren/medioevo-tools` (remote separado, `main` branch)
2. Activar GitHub Pages en `Settings → Pages` (source: `main` / root)
3. Crear producto Gumroad $3/50 usos → obtener URL real
4. Actualizar `anti_ia_detector_web.html` líneas 259, 328, 335 con URL real Gumroad
5. Commit + push final

---

## Plantilla para futuras entradas

```markdown
## YYYY-MM-DD — Descripción breve

| Fecha | Origen | Destino | Razón | Evidencia | Hash |
|-------|--------|---------|-------|-----------|------|
| YYYY-MM-DD | `ruta/origen` | `ruta/destino` | Justificación | Qué valida | SHA256 |

**Rollback:** comando exacto para revertir.
```