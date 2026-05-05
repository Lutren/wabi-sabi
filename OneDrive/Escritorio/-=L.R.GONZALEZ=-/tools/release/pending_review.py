from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from _common import ROOT, add_common_args, is_denied, print_json, rel, validate_root_arg


SCHEMA = "medioevo.pending_review.v1"

CHECKBOX_RE = re.compile(r"^\s*[-*+]\s+\[(?P<mark>[ xX])\]\s+(?P<text>.*)$")
PRIORITY_RE = re.compile(r"\bP(?P<num>[0-4])(?:\.\d+)?\b", re.IGNORECASE)

PENDING_EXCLUDE_SUBSTRINGS = [
    "/.git/",
    "/.claw/",
    "/.claude/",
    "/.skills/",
    "/node_modules/",
    "/.venv",
    "/__pycache__/",
    "/.pytest_cache/",
    "/target/",
    "/dist/",
    "/build/",
    "/release/",
    "/releases/",
    "/qa_artifacts/",
    "/publish_staging/",
    "/runtime/",
    "/_archive",
    "/_archivar",
    "/_archivo_sesiones/",
    "/archive/",
    "/history/",
    "/historico/",
    "/vault_medioevo/",
    "/_snapshots/",
    "/_trash",
    "/backup_",
    "/tools/vendor/",
    "/tools/pentest_repos/",
    "/tools/claw-code/",
    "/tools/reports/",
    "/github-modules/",
    "/llm-wiki/",
    "/mempalace_seed_convos_",
    "/vault_medioevo/03_pendientes/",
    "/vault_medioevo/04_handoffs/",
    "/skills-pack-content/",
    "/-=libros/claudio/skills/",
    "/.github/issue_template/",
    "/.github/pull_request_template.md",
    "/prompt_maestro_handoff_",
    "/claude.md",
    "/ecosystem_master.md",
    "/automatizacion_configurada.md",
    "/documentacion_maestra.md",
    "/ecosistema_consolidado.md",
    "/estado_actual_",
    "/estado_sistema_",
    "/psi_automation_summary.md",
    "/psi_engine_",
    "/reparar_websearch_bug.md",
    "/servicios_iniciados_",
    "/status.md",
    "/ultrathink_resumen.md",
    "/apps/hormiguero_hub/readme.md",
    "/apps/editorial_web/",
    "/beta/launch_checklist.md",
    "/brain_os/",
    "/brain_os/architecture_unified_",
    "/brain_os/benchmark_",
    "/brain_os/beta_recruitment.md",
    "/brain_os/ceo_briing.md",
    "/brain_os/executive_summary.md",
]

CLAUDIO_ROOT = ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio"
CLAUDIO_PENDING_MASTER = CLAUDIO_ROOT / "PENDIENTES_MASTER.md"
KAIROS_FASTLANE = (
    CLAUDIO_ROOT
    / "runtime"
    / "observacionista"
    / "kairos_attention_hygiene"
    / "pendientes_fastlane_2026-05-01.json"
)


@dataclass(frozen=True)
class PendingItem:
    path: str
    line: int
    text: str
    priority: str
    lane: str
    blocker: str
    normalized: str


def _norm_path(path: Path) -> str:
    return "/" + rel(path).replace("\\", "/").lower().lstrip("/")


def is_pending_denied(path: Path) -> bool:
    value = _norm_path(path)
    return is_denied(path) or any(marker in value for marker in PENDING_EXCLUDE_SUBSTRINGS)


def iter_markdown_files() -> Iterable[Path]:
    for base, dirs, files in os.walk(ROOT):
        base_path = Path(base)
        dirs[:] = [name for name in dirs if not is_pending_denied(base_path / name)]
        for name in files:
            if not name.lower().endswith(".md"):
                continue
            path = base_path / name
            if not is_pending_denied(path):
                yield path


def compress_text(value: str, limit: int = 500) -> str:
    text = re.sub(r"\s+", " ", value).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def normalize_item(text: str) -> str:
    text = re.sub(r"`[^`]+`", "`path`", text)
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"\s+", " ", text).strip().casefold()
    return text


def is_inactive_checkbox_text(text: str) -> bool:
    value = text.strip()
    lowered = value.casefold()
    if not value:
        return True
    if value.startswith("¿") and value.endswith("?"):
        return True
    done_markers = (
        "(hecho)",
        "✅ hecho",
        "listo)",
        "(listo)",
        "completado",
        "ninguno -",
        "sistema está completo",
        "sistema esta completo",
    )
    return any(marker in lowered for marker in done_markers)


def extract_priority(text: str) -> str:
    match = PRIORITY_RE.search(text)
    if not match:
        return "UNCLASSIFIED"
    return f"P{match.group('num')}"


def classify_lane(path: str, text: str) -> str:
    value = f"{path} {text}".casefold()
    if any(marker in value for marker in ("metaevo-tcg", "/tcg", "game_bridge", "rpg", "videojuego", "games", "juegos", "metaevo", "colonies", "arcade")):
        return "private_rpg"
    if any(marker in value for marker in ("wave", "wabi-sabi", "wabi_sabi", "document collapse")):
        return "wave_fc"
    if any(marker in value for marker in ("flujocrm", "asistente-negocio", "asistente_negocio", "mini-office", "argus", "gumroad", "checkout", "venta", "comercial", "commercial")):
        return "commercial"
    if any(marker in value for marker in ("obsai-core", "residueos", "observacionismo-gate", "open-dev", "github", "safe-exec", "agent-handoff", "duat-genesis", "rapid-agent")):
        return "open_source"
    if any(marker in value for marker in ("claudio", "hormiguero", "brain os", "symphony", "ollama", "gemma", "runtime", "actiongate", "host_observacionista")):
        return "runtime_claudio"
    if any(marker in value for marker in ("website", "landing", "marketing", "twitter", "instagram", "tiktok", "linkedin", "discord", "cloudflare", "seo")):
        return "website_marketing"
    if any(marker in value for marker in ("eor", "aia", "fisica", "consciencia", "psi", "claim", "fals", "research", "kernel", "ontologia", "debugtyr")):
        return "research_claims"
    if any(
        marker in value
        for marker in (
            "limpieza",
            "cleanup",
            "migration",
            "migracion",
            "migrar",
            "elichicar",
            "duplic",
            "archive",
            "archivar",
            "delete_candidates",
            "desktop",
            "espacio",
            "disco",
        )
    ):
        return "cleanup_migration"
    return "general"


def classify_blocker(text: str, lane: str | None = None, path: str | None = None) -> str:
    value = text.casefold()
    path_value = str(path or "").replace("\\", "/").casefold()
    if any(marker in path_value for marker in ("/legal/", "legal_protection_guide")):
        return "legal_or_human"
    if any(marker in path_value for marker in ("release_checklist.md", "app_store_readiness.md")):
        return "legal_or_human"
    if "gaps_mercado.md" in path_value:
        return "legal_or_human"
    if "publicar_en_github.md" in path_value:
        return "external_or_gated"
    if "manual_qa_checklist.md" in path_value:
        return "legal_or_human"
    if "checklist_final.md" in path_value:
        return "external_or_gated"
    if "claudio_evolution.md" in path_value:
        return "host_or_heavy"
    if any(marker in path_value for marker in ("/apps/editorial_web/marketing/", "/marketing/", "/video/")):
        return "external_or_gated"
    if any(marker in path_value for marker in ("video_tools_guide.md", "/grants/")):
        return "external_or_gated"
    if lane == "private_rpg":
        return "private_boundary"
    local_verification_markers = (
        "pytest",
        "npm run check",
        "node --check",
        "smoke local",
        "local smoke",
        "unit test",
    )
    private_markers = (
        "private",
        "privado",
        "rpg",
        "tcg",
        "secreto",
        "secret",
        "credential",
        "credencial",
        "token",
        "api key",
        " key",
    )
    external_markers = (
        "actiongate",
        "host approve",
        "host `approve`",
        "host en approve",
        "publicar",
        "publicacion",
        "publication",
        "upload",
        "deploy",
        "push",
        "github",
        "gumroad",
        "kdp",
        "redes",
        "twitter",
        "instagram",
        "tiktok",
        "discord",
        "linkedin",
        "cloudflare",
        "sponsors",
        "devpost",
        "youtube",
        "reddit",
        "substack",
        "fiverr",
        "sora",
        "suno",
        "adobe podcast",
        "product hunt",
        "show hn",
        "hacker news",
        "huggingface",
        "ko-fi",
        "bmac",
        "lemon squeezy",
        "spotify",
        "redbubble",
        "patreon",
        "twilio",
        "telegram",
        "sentry",
        "cloudflamuy",
        "n8n",
        "google stitch",
        "notebooklm",
        "mailerlite",
        "goodmuyads",
        "goodreads",
        "dall-e",
        "capcut",
        "whatsapp",
        "grants",
        "becas",
        "contactar",
        "posthog",
        "checkout",
        "stripe",
        "billing",
        "npm audit",
        "ventas",
        "sales",
        "primeras ventas",
        "5 ventas",
        "metricas de ventas",
        "métricas de ventas",
        "monitorear primeras ventas",
        "supabase",
        "acceso a dashboard",
        "landing page de ventas",
        "checkout",
        "externa",
        "acciones externas",
        "hold_external",
        "hold_metrics",
        "retweet",
        "re-tweet",
        "tweetear",
        "menciones",
        "comentarios en",
        "metricas diarias",
        "metricas semanales",
        "métricas",
        "metricas",
        "dashboard",
        "comentarios",
        "conversiones",
        "blog post",
        "contenido del día",
        "contenido del dia",
        "programar posts",
        "comunidad",
        "community",
        "stripe",
        "kofi",
        "ko-fi",
        "umami",
        "analytics",
        "testimonios",
        "amazon",
        "reseñas",
        "resenas",
        "lectores",
        "booktuber",
        "colaborad",
        "guest post",
        "blogs de",
        "podcast",
        "cross-promo",
        "mailer",
        "mailerlite",
        "goodreads",
        "goodmuyads",
        "author central",
        "dall-e",
        "dalle",
        "payout",
        "payouts",
        "checkout",
        "deploy",
        "grants",
        "becas",
        "contactar",
        "contenido en muy",
        "publicar contenido",
        "block_cleanup_gate",
        "block_live_ui_gate",
        "block_publication",
        "block_model_training_gate",
    )
    destructive_or_cleanup_markers = (
        "elichicar",
        "eliminar",
        "borrar",
        "delete",
        "remove ",
        "mover ",
        "mover `",
        "move ",
        "archivar",
        "archivo dudoso",
        "duplicado",
        "backup",
        "liberar espacio",
        "espacio liberado",
        "limpieza",
        "cleanup",
        "migration",
        "migracion",
        "migrar a",
        "mover datasets",
        "mover mempalace",
    )
    legal_markers = (
        "legal",
        "asesor",
        "jurisdiccion",
        "impuestos",
        "tax",
        "firma",
        "signing",
        "unsigned",
        "maquina limpia",
        "clean vm",
        "clean-machine",
        "payout",
        "bank",
        "banc",
        "2fa",
        "mfa",
        "datos anonimizados reales",
        "datos reales anonimizados",
        "datos reales de cliente",
        "real client data",
        "customer data",
        "oauth",
        "manual tren",
        "pendiente de tren",
        "tren:",
        "fuentes editoriales",
        "registrar marca",
        "muygistrar marca",
        "registrar los",
        "muygistrar los",
        "marcas adicionales",
        "rfc",
        "sat",
        "indautor",
        "terms of service",
        "privacy policy",
        "content id",
        "s.a.s",
        "propiedad intelectual",
        "abogado",
        "manual qa",
        "qa manual",
        "clean install",
        "windows machine",
        "machine or vm",
        "installer/download",
        "support link",
        "privacy/terms",
        "support, refund, privacy and terms",
        "refund",
        "terms copy",
        "soporte",
        "politica",
        "política",
        "aprobada por humano",
        "aprobado por humano",
        "sonido ambiente",
        "ambient sound",
        "opcional",
    )
    host_markers = (
        "gemma",
        "ollama",
        "modelo pesado",
        "modelos cloud",
        "daemon",
        "qemu",
        "wsl",
        "disco",
        "cpu",
        "gpu",
        "host",
        "qwen",
        "cuda",
        "vpn",
        "tor",
        "hardware",
        "hardwamuy",
        "entrenamiento",
        "entmuynamiento",
        "lora",
        "qlora",
        "dpo",
        "pesos",
        "weights",
        "entrenamiento",
        "entmuynamiento",
        "cuda",
        "hardwamuy",
        "hardware",
        "iniciar servicios",
        "cron",
        "openwebui",
        "api 47047",
        "hub 7474",
        "vpn",
        "tor",
        "hold_host",
        "hold_data",
        "hold_weights",
        "block_host_gate",
        "block_qwen_gate",
    )
    if any(marker in value for marker in private_markers):
        return "private_boundary"
    if any(marker in value for marker in external_markers):
        return "external_or_gated"
    if any(marker in value for marker in destructive_or_cleanup_markers):
        return "external_or_gated"
    if any(marker in value for marker in legal_markers):
        return "legal_or_human"
    if any(marker in value for marker in host_markers):
        return "host_or_heavy"
    if lane == "commercial" and not any(marker in value for marker in local_verification_markers):
        return "legal_or_human"
    return "local_candidate"


def parse_markdown_checkboxes(path: Path) -> list[PendingItem]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []

    items: list[PendingItem] = []
    rel_path = rel(path)
    in_fence = False
    for idx, line in enumerate(lines):
        if re.match(r"^\s{0,3}(```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = CHECKBOX_RE.match(line)
        if not match or match.group("mark").lower() == "x":
            continue
        if is_inactive_checkbox_text(match.group("text")):
            continue
        parts = [match.group("text").strip()]
        cursor = idx + 1
        while cursor < len(lines):
            nxt = lines[cursor]
            if CHECKBOX_RE.match(nxt) or re.match(r"^\s{0,3}#{1,6}\s+", nxt):
                break
            if not nxt.strip():
                break
            if re.match(r"^\s{2,}\S", nxt) and not re.match(r"^\s*[-*+]\s+", nxt):
                parts.append(nxt.strip())
                cursor += 1
                continue
            break
        text = compress_text(" ".join(parts))
        lane = classify_lane(rel_path, text)
        items.append(
            PendingItem(
                path=rel_path,
                line=idx + 1,
                text=text,
                priority=extract_priority(text),
                lane=lane,
                blocker=classify_blocker(text, lane=lane, path=rel_path),
                normalized=normalize_item(text),
            )
        )
    return items


def count_items(items: list[PendingItem]) -> dict[str, object]:
    dedup: dict[str, PendingItem] = {}
    occurrences = Counter()
    for item in items:
        occurrences[item.normalized] += 1
        dedup.setdefault(item.normalized, item)

    dedup_items = list(dedup.values())
    top = sorted(
        dedup_items,
        key=lambda item: (
            {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}.get(item.priority, 9),
            item.blocker != "local_candidate",
            item.lane,
            item.path,
            item.line,
        ),
    )[:40]
    return {
        "raw_open": len(items),
        "dedup_open": len(dedup_items),
        "by_priority": dict(sorted(Counter(item.priority for item in dedup_items).items())),
        "by_lane": dict(sorted(Counter(item.lane for item in dedup_items).items())),
        "by_blocker": dict(sorted(Counter(item.blocker for item in dedup_items).items())),
        "top_items": [
            {
                "priority": item.priority,
                "lane": item.lane,
                "blocker": item.blocker,
                "item": item.text,
                "first_evidence": f"{item.path}:{item.line}",
                "occurrences": occurrences[item.normalized],
            }
            for item in top
        ],
    }


def read_kairos_snapshot(now_date: str) -> dict[str, object]:
    if not KAIROS_FASTLANE.exists():
        return {"exists": False, "path": rel(KAIROS_FASTLANE)}
    try:
        data = json.loads(KAIROS_FASTLANE.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"exists": True, "path": rel(KAIROS_FASTLANE), "error": str(exc)}
    decisions = data.get("decisions") if isinstance(data, dict) else []
    if not isinstance(decisions, list):
        decisions = []
    action_counts = Counter(str(row.get("action", "unknown")) for row in decisions if isinstance(row, dict))
    priority_counts = Counter()
    for row in decisions:
        if not isinstance(row, dict):
            continue
        item = row.get("item")
        if isinstance(item, dict):
            priority_counts[str(item.get("priority", "UNCLASSIFIED"))] += 1
    generated_at = str(data.get("generated_at", "")) if isinstance(data, dict) else ""
    generated_date = generated_at[:10] if len(generated_at) >= 10 else ""
    return {
        "exists": True,
        "path": rel(KAIROS_FASTLANE),
        "schema": data.get("schema") if isinstance(data, dict) else None,
        "generated_at": generated_at,
        "stale": generated_date != now_date,
        "decision_count": len(decisions),
        "by_action": dict(sorted(action_counts.items())),
        "by_priority": dict(sorted(priority_counts.items())),
    }


def build_report() -> dict[str, object]:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    now_date = generated_at[:10]

    active_items: list[PendingItem] = []
    for path in iter_markdown_files():
        active_items.extend(parse_markdown_checkboxes(path))

    claudio_items = parse_markdown_checkboxes(CLAUDIO_PENDING_MASTER) if CLAUDIO_PENDING_MASTER.exists() else []
    claudio_counts = count_items(claudio_items)

    return {
        "schema": SCHEMA,
        "generated_at": generated_at,
        "date": now_date,
        "root": str(ROOT),
        "policy": {
            "status": "snapshot_only_not_closure",
            "rule": "Run at the start of each session/day before changing backlog-driven work.",
            "external_actions": "remain gated by host_observacionista/ActionGate.",
            "curador": "unknown sources and residues still require curador_preflight before use or discard.",
        },
        "active_markdown": count_items(active_items),
        "claudio_master": {
            "path": rel(CLAUDIO_PENDING_MASTER),
            **claudio_counts,
        },
        "kairos_fastlane": read_kairos_snapshot(now_date),
    }


def md_table(headers: list[str], rows: list[list[object]]) -> str:
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |")
    return "\n".join(output)


def render_markdown(report: dict[str, object]) -> str:
    active = report["active_markdown"]
    claudio = report["claudio_master"]
    kairos = report["kairos_fastlane"]
    assert isinstance(active, dict)
    assert isinstance(claudio, dict)
    assert isinstance(kairos, dict)

    lines = [
        f"# Pending Review - {report['date']}",
        "",
        "Status: generated snapshot. This file is evidence for triage, not proof that old checkboxes are still valid and not permission to publish, push, deploy or delete.",
        "",
        "## Counts",
        "",
        f"- Active markdown raw open items: `{active['raw_open']}`.",
        f"- Active markdown deduplicated open items: `{active['dedup_open']}`.",
        f"- Claudio `PENDIENTES_MASTER.md` raw open items: `{claudio['raw_open']}`.",
        f"- Claudio deduplicated open items: `{claudio['dedup_open']}`.",
        "",
        "## Active Markdown By Priority",
        "",
        md_table(["priority", "dedup_count"], [[k, v] for k, v in dict(active["by_priority"]).items()]),
        "",
        "## Active Markdown By Lane",
        "",
        md_table(["lane", "dedup_count"], [[k, v] for k, v in dict(active["by_lane"]).items()]),
        "",
        "## Active Markdown By Blocker",
        "",
        md_table(["blocker", "dedup_count"], [[k, v] for k, v in dict(active["by_blocker"]).items()]),
        "",
        "## Claudio Master By Priority",
        "",
        md_table(["priority", "dedup_count"], [[k, v] for k, v in dict(claudio["by_priority"]).items()]),
        "",
        "## Claudio Master By Blocker",
        "",
        md_table(["blocker", "dedup_count"], [[k, v] for k, v in dict(claudio["by_blocker"]).items()]),
        "",
        "## Top Items",
        "",
        md_table(
            ["priority", "lane", "blocker", "item", "first evidence", "occurrences"],
            [
                [
                    row["priority"],
                    row["lane"],
                    row["blocker"],
                    row["item"],
                    row["first_evidence"],
                    row["occurrences"],
                ]
                for row in list(active["top_items"])[:25]
            ],
        ),
        "",
        "## Kairos Fastlane",
        "",
    ]
    if kairos.get("exists"):
        lines.extend(
            [
                f"- Path: `{kairos.get('path')}`.",
                f"- Generated at: `{kairos.get('generated_at')}`.",
                f"- Stale against this snapshot date: `{kairos.get('stale')}`.",
                f"- Decision count: `{kairos.get('decision_count')}`.",
                "",
                md_table(["action", "count"], [[k, v] for k, v in dict(kairos.get("by_action", {})).items()]),
            ]
        )
    else:
        lines.append(f"- Not found: `{kairos.get('path')}`.")
    lines.extend(
        [
            "",
            "## Operational Rule",
            "",
            "At the start of each run/day execute `python tools\\release\\pending_review.py --write --quiet`, then choose work from shortest verified local closure first. External/publication tasks stay blocked until their specific gate is clean.",
            "",
        ]
    )
    return "\n".join(lines)


def write_artifacts(report: dict[str, object]) -> dict[str, str]:
    date = str(report["date"])
    docs_dir = ROOT / "docs" / "pending"
    qa_dir = ROOT / "qa_artifacts" / "pending"
    docs_dir.mkdir(parents=True, exist_ok=True)
    qa_dir.mkdir(parents=True, exist_ok=True)

    json_path = qa_dir / f"pending_review_{date}.json"
    json_latest = qa_dir / "pending_review_latest.json"
    md_path = docs_dir / f"PENDING_REVIEW_{date}.md"
    md_latest = docs_dir / "PENDING_REVIEW_LATEST.md"

    payload = json.dumps(report, indent=2, ensure_ascii=False)
    markdown = render_markdown(report)

    json_path.write_text(payload + "\n", encoding="utf-8")
    json_latest.write_text(payload + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    md_latest.write_text(markdown, encoding="utf-8")

    return {
        "json": rel(json_path),
        "json_latest": rel(json_latest),
        "markdown": rel(md_path),
        "markdown_latest": rel(md_latest),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a daily/run pending-work snapshot without closing tasks.")
    add_common_args(parser)
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.add_argument("--write", action="store_true", help="write markdown and JSON artifacts")
    parser.add_argument("--quiet", action="store_true", help="only print artifact paths or compact summary")
    args = parser.parse_args()
    validate_root_arg(args)

    report = build_report()
    artifacts: dict[str, str] | None = None
    if args.write:
        artifacts = write_artifacts(report)
        report["artifacts"] = artifacts

    if args.json:
        print_json(report)
    elif args.quiet:
        active = report["active_markdown"]
        claudio = report["claudio_master"]
        assert isinstance(active, dict)
        assert isinstance(claudio, dict)
        print(
            f"pending_review date={report['date']} active_dedup={active['dedup_open']} "
            f"claudio_open={claudio['raw_open']}"
        )
        if artifacts:
            for key, value in artifacts.items():
                print(f"{key}: {value}")
    else:
        print(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
