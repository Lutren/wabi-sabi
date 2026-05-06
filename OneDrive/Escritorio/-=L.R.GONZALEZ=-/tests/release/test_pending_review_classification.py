from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "release"))

import pending_review  # noqa: E402


def test_destructive_cleanup_words_are_gated_not_local() -> None:
    assert pending_review.classify_blocker("`PENDIENTES_MASTER_UNIFICADO.md` - Elichicar (duplicado)") == "external_or_gated"
    assert pending_review.classify_blocker("mover datasets a E:") == "external_or_gated"
    assert pending_review.classify_blocker("Verificar espacio liberado") == "external_or_gated"
    assert pending_review.classify_blocker("Check generated archive contents before upload") == "external_or_gated"


def test_regular_local_evidence_task_remains_local_candidate() -> None:
    assert pending_review.classify_blocker("Actualizar reporte local con evidencia de pytest") == "local_candidate"


def test_procedural_local_candidate_guard_is_not_selected_as_work() -> None:
    assert (
        pending_review.classify_blocker(
            "**REVIEW** Si aparece un nuevo `local_candidate`, resolverlo con el mismo ciclo: diff, prueba, outcome, COMMS y mirror.",
            lane="runtime_claudio",
        )
        == "external_or_gated"
    )
    assert (
        pending_review.classify_blocker(
            "**REVIEW** Si aparece un `local_candidate` real, resolverlo con diff, prueba, outcome, COMMS y mirror.",
            lane="runtime_claudio",
        )
        == "external_or_gated"
    )


def test_commercial_manual_checks_are_not_local_candidates() -> None:
    assert pending_review.classify_blocker("Dashboard de métricas de ventas") == "external_or_gated"
    assert pending_review.classify_blocker("Supabase schema: Requiere acceso a dashboard") == "external_or_gated"
    assert pending_review.classify_blocker("Use a Windows machine or VM without the development repo.") == "legal_or_human"
    assert pending_review.classify_blocker("Support, refund, privacy and terms copy is final.") == "legal_or_human"
    assert pending_review.classify_blocker("Gemini API key nueva") == "private_boundary"
    assert pending_review.classify_blocker("HuggingFace key nueva") == "private_boundary"
    assert pending_review.classify_blocker("Publicar Reddit posts") == "external_or_gated"
    assert pending_review.classify_blocker("muyddit r/freelance - EN version") == "external_or_gated"
    assert pending_review.classify_blocker("ProductHunt launch Tuesday morning") == "external_or_gated"
    assert pending_review.classify_blocker("Facebook ads LATAM market") == "external_or_gated"
    assert pending_review.classify_blocker("Fuentes editoriales books 1-3: 0/30 rutas encontradas") != "local_candidate"
    assert pending_review.classify_blocker("muygistrar marca MEDIOEVO en IMPI") == "legal_or_human"
    assert pending_review.classify_blocker("Obtener RFC en el SAT") == "legal_or_human"
    assert pending_review.classify_blocker("Configurar Google Stitch para UI mockups") == "external_or_gated"
    assert pending_review.classify_blocker("Blueprint art for product", lane="commercial") == "legal_or_human"
    assert pending_review.classify_blocker("`npm audit --omit=dev --audit-level=high` passes.", lane="commercial") == "external_or_gated"
    assert pending_review.classify_blocker("`npm run check` passes.", lane="commercial") == "local_candidate"


def test_private_game_lane_is_never_local_candidate() -> None:
    assert pending_review.classify_lane("claudio/products/V2_FIXES_GAMES.md", "Deck minimo inconsistente") == "private_rpg"
    assert pending_review.classify_blocker("Deck minimo inconsistente", lane="private_rpg") == "private_boundary"
    assert pending_review.classify_lane("claudio/mini_office/README.md", "Plantillas de landing pages") == "commercial"


def test_path_level_policy_blocks_historical_and_legal_checklists() -> None:
    assert pending_review.classify_blocker("Documentar proceso creativo con IA", path="-=NEGOCIOS=-/Legal/LEGAL_PROTECTION_GUIDE.md") == "legal_or_human"
    assert pending_review.classify_blocker("App name and version", path="APP_STORE_READINESS.md") == "legal_or_human"
    assert pending_review.classify_blocker("App opens.", path="MANUAL_QA_CHECKLIST.md") == "legal_or_human"
    assert pending_review.classify_blocker("Dark/Light mode toggle", path="-=MEDIOEVO=-/-=LIBROS/CHECKLIST_FINAL.md") == "external_or_gated"
    assert pending_review.classify_blocker("Selector de voz en la UI", path="-=MEDIOEVO=-/-=LIBROS/CLAUDIO_EVOLUTION.md") == "host_or_heavy"
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "products" / "skills-pack-content" / "05_marketing_strategist" / "SKILL.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / ".github" / "ISSUE_TEMPLATE" / "bug_report.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "CLAUDE.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "ECOSYSTEM_MASTER.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "vault_medioevo" / "03_pendientes" / "PENDIENTES_MASTER.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "DOCUMENTACION_MAESTRA.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "PSI_ENGINE_COMPLETE.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "apps" / "hormiguero_hub" / "README.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "beta" / "LAUNCH_CHECKLIST.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "brain_os" / "ARCHITECTURE_UNIFIED_2026.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "brain_os" / "BENCHMARK_V3_RESULTS.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "brain_os" / "BETA_RECRUITMENT.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "brain_os" / "EXECUTIVE_SUMMARY.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "brain_os" / "CEO_BRIING.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "brain_os" / "IMPROVEMENT_ANALYSIS.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "city_overlay" / "ESTADO_ACTUAL.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "claudio_os" / "IMPLEMENTACION.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "claudio_os" / "IMPLEMENTACION_COMPLETA.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "claudio_os" / "README_FINAL.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "docs" / "CONCILIO_DARVI.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "docs" / "EL_BARDO.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "docs" / "applications" / "PRODUCT_HUNT_PREP.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "installer" / "BUILD_GUIDE.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "medioevo_agent_hub" / "README.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "mini_office" / "README.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "oppo_deploy" / "ESTADO_FINAL.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "oppo_robot" / "DNS_VIA_HTTP.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "products" / "PROMO_POSTS_SOFTWARE.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "research" / "ANALISIS_RESEARCH_CONSOLIDADO_2026.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "teatro" / "HORMIGUERO_TESTS.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "tv_audio" / "TV_AUDIO_ONLY_ARCHITECTURE.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "website" / "VERIFICACION_WEBMASTER_TOOLS.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "CLAUDIO - researchs" / "ANALISIS_RESEARCH_CONSOLIDADO_2026.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "apps" / "editorial_web" / "marketing" / "PROXIMOS-PASOS.md")
    assert pending_review.is_pending_denied(ROOT / "tools" / "claw-code" / "PARITY.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "tools" / "reports" / "HORMIGUERO_HUB_COMPLETE_REPORT.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "docs" / "root_notes_review" / "OLD.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "tools" / "launchers" / "OLD.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "tools" / "root_scripts_review" / "OLD.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "llm-wiki" / "INSTALACION_COMPLETA.md")
    assert pending_review.classify_blocker("Tests pytest Writer", path="-=MEDIOEVO=-/-=LIBROS/claudio/GAPS_MERCADO.md") == "legal_or_human"
    assert pending_review.classify_blocker("Configurar CI/CD", path="-=MEDIOEVO=-/-=LIBROS/claudio/mini_office/PUBLICAR_EN_GITHUB.md") == "external_or_gated"
    assert pending_review.classify_blocker("Agmuygar sonido ambiente (opcional)") == "legal_or_human"
    assert pending_review.classify_blocker("Implementar `_call_claude` real") == "external_or_gated"
    assert pending_review.classify_blocker("Implementar `_call_openai` real") == "external_or_gated"
    assert pending_review.classify_blocker("Actualizar métricas diarias") == "external_or_gated"
    assert pending_review.classify_blocker("VISIBILITY_MATRIX.md aprobada por humano") == "legal_or_human"
    assert pending_review.classify_blocker("Iniciar servicios: API 47047 + Hub 7474") == "host_or_heavy"
    assert pending_review.classify_blocker("Crear contenido del dia", path="-=MEDIOEVO=-/-=LIBROS/claudio/apps/editorial_web/marketing/PROXIMOS-PASOS.md") == "external_or_gated"


def test_markdown_checkboxes_inside_fenced_examples_are_ignored(tmp_path: Path) -> None:
    pending_doc = tmp_path / "PENDING.md"
    pending_doc.write_text(
        "\n".join(
            [
                "# Example",
                "```markdown",
                "- [ ] FASE Fy en proxima sesion",
                "```",
                "- [ ] Actualizar reporte local con evidencia de pytest",
            ]
        ),
        encoding="utf-8",
    )

    items = pending_review.parse_markdown_checkboxes(pending_doc)

    assert [item.text for item in items] == ["Actualizar reporte local con evidencia de pytest"]


def test_inactive_checkbox_text_is_not_counted_as_open(tmp_path: Path) -> None:
    pending_doc = tmp_path / "CHECKLIST.md"
    pending_doc.write_text(
        "\n".join(
            [
                "- [ ] Fix controles volumen (HECHO)",
                "- [ ] ¿Qué dice la evidencia?",
                "- [ ] Ninguno - El sistema está completo y funcionando",
                "- [ ] Actualizar reporte local con evidencia de pytest",
            ]
        ),
        encoding="utf-8",
    )

    items = pending_review.parse_markdown_checkboxes(pending_doc)

    assert [item.text for item in items] == ["Actualizar reporte local con evidencia de pytest"]


def test_write_artifacts_ignores_generated_at_only_churn(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(pending_review, "ROOT", tmp_path)
    report = {
        "schema": pending_review.SCHEMA,
        "generated_at": "2026-05-05T00:00:00+00:00",
        "date": "2026-05-05",
        "root": str(tmp_path),
        "policy": {},
        "active_markdown": {
            "raw_open": 1,
            "dedup_open": 1,
            "by_priority": {"UNCLASSIFIED": 1},
            "by_lane": {"general": 1},
            "by_blocker": {"local_candidate": 1},
            "top_items": [],
        },
        "claudio_master": {
            "path": "PENDIENTES_MASTER.md",
            "raw_open": 0,
            "dedup_open": 0,
            "by_priority": {},
            "by_blocker": {},
            "top_items": [],
        },
        "kairos_fastlane": {"exists": False, "path": "missing.json"},
    }

    artifacts = pending_review.write_artifacts(report)
    json_path = tmp_path / artifacts["json"]
    first = json_path.read_text(encoding="utf-8")
    report["generated_at"] = "2026-05-05T00:01:00+00:00"
    pending_review.write_artifacts(report)

    assert json_path.read_text(encoding="utf-8") == first


def test_md_table_balances_truncated_code_spans() -> None:
    table = pending_review.md_table(
        ["item"],
        [["Evidencia en `docs\\WAVE_WABI_LOCAL_GATE_..."]],
    )

    row = table.splitlines()[-1]
    assert row.count("`") % 2 == 0
    assert row.endswith(" |")
