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


def test_commercial_manual_checks_are_not_local_candidates() -> None:
    assert pending_review.classify_blocker("Dashboard de métricas de ventas") == "external_or_gated"
    assert pending_review.classify_blocker("Supabase schema: Requiere acceso a dashboard") == "external_or_gated"
    assert pending_review.classify_blocker("Use a Windows machine or VM without the development repo.") == "legal_or_human"
    assert pending_review.classify_blocker("Support, refund, privacy and terms copy is final.") == "legal_or_human"
    assert pending_review.classify_blocker("Gemini API key nueva") == "private_boundary"
    assert pending_review.classify_blocker("HuggingFace key nueva") == "private_boundary"
    assert pending_review.classify_blocker("Publicar Reddit posts") == "external_or_gated"
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
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "apps" / "editorial_web" / "marketing" / "PROXIMOS-PASOS.md")
    assert pending_review.is_pending_denied(ROOT / "tools" / "claw-code" / "PARITY.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio" / "tools" / "reports" / "HORMIGUERO_HUB_COMPLETE_REPORT.md")
    assert pending_review.is_pending_denied(ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "llm-wiki" / "INSTALACION_COMPLETA.md")
    assert pending_review.classify_blocker("Tests pytest Writer", path="-=MEDIOEVO=-/-=LIBROS/claudio/GAPS_MERCADO.md") == "legal_or_human"
    assert pending_review.classify_blocker("Configurar CI/CD", path="-=MEDIOEVO=-/-=LIBROS/claudio/mini_office/PUBLICAR_EN_GITHUB.md") == "external_or_gated"
    assert pending_review.classify_blocker("Agmuygar sonido ambiente (opcional)") == "legal_or_human"
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
