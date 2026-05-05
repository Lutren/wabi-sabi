from __future__ import annotations

import argparse
import html
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = ROOT / "qa_artifacts" / "control_dashboard" / "system-control-snapshot-2026-05-05.json"
HTML_PATH = ROOT / "docs" / "control" / "CONTROL_DASHBOARD.html"


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def run_command(args: list[str], timeout: int = 30) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        completed = subprocess.run(
            args,
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": "command not found"}
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "returncode": None,
            "stdout": exc.stdout or "",
            "stderr": f"timeout after {timeout}s",
        }
    return {
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def fetch_text(url: str, timeout: int = 10) -> str:
    request = Request(url, headers={"User-Agent": "medioevo-control-dashboard/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="replace")
    except OSError as exc:
        return f"ERROR: {exc}"


def parse_cloudflare_trace(text: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in text.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key in {"ip", "loc", "colo", "warp", "gateway", "rbi"}:
            data[key] = value
    if "ip" in data:
        data["ip_redacted"] = redact_ip(data.pop("ip"))
    return data


def redact_ip(value: str) -> str:
    if ":" in value:
        parts = value.split(":")
        return ":".join(parts[:3]) + "::redacted"
    pieces = value.split(".")
    if len(pieces) == 4:
        return f"{pieces[0]}.{pieces[1]}.x.x"
    return "redacted"


def public_geo() -> dict[str, Any]:
    trace_text = fetch_text("https://www.cloudflare.com/cdn-cgi/trace")
    trace = parse_cloudflare_trace(trace_text)
    ipinfo_raw = fetch_text("https://ipinfo.io/json")
    ipinfo: dict[str, Any] = {}
    try:
        parsed = json.loads(ipinfo_raw)
        if isinstance(parsed, dict):
            ipinfo = {
                "ip_redacted": redact_ip(str(parsed.get("ip", ""))) if parsed.get("ip") else "",
                "city": parsed.get("city", ""),
                "region": parsed.get("region", ""),
                "country": parsed.get("country", ""),
                "org": parsed.get("org", ""),
                "timezone": parsed.get("timezone", ""),
            }
    except json.JSONDecodeError:
        ipinfo = {"error": ipinfo_raw[:160]}
    return {"cloudflare_trace": trace, "ipinfo": ipinfo}


def vpn_snapshot() -> dict[str, Any]:
    status = run_command(["warp-cli", "status"], timeout=15)
    connect = None
    if not status["ok"] or "Connected" not in status.get("stdout", ""):
        connect = run_command(["warp-cli", "connect"], timeout=20)
        status = run_command(["warp-cli", "status"], timeout=15)
    return {
        "provider": "Cloudflare WARP",
        "connect_attempted": connect is not None,
        "connect_result": connect,
        "status_command": status,
        "connected": status["ok"] and "Connected" in status.get("stdout", ""),
        "network_healthy": "healthy" in status.get("stdout", "").lower(),
        "geo": public_geo(),
    }


def git_snapshot() -> dict[str, Any]:
    branch = run_command(["git", "-C", str(ROOT.parent.parent.parent), "branch", "--show-current"], timeout=15)
    head = run_command(["git", "-C", str(ROOT.parent.parent.parent), "log", "-1", "--oneline"], timeout=15)
    return {
        "git_root": str(ROOT.parent.parent.parent),
        "branch": branch.get("stdout", ""),
        "head": head.get("stdout", ""),
        "branch_ok": branch["ok"],
        "head_ok": head["ok"],
    }


def pending_snapshot() -> dict[str, Any]:
    data = read_json(ROOT / "qa_artifacts" / "pending" / "pending_review_latest.json")
    active = data.get("active_markdown", {}) if isinstance(data.get("active_markdown"), dict) else {}
    claudio = data.get("claudio_master", {}) if isinstance(data.get("claudio_master"), dict) else {}
    return {
        "generated_at": data.get("generated_at", ""),
        "active_dedup": active.get("dedup_open", 0),
        "active_by_lane": active.get("by_lane", {}),
        "active_by_blocker": active.get("by_blocker", {}),
        "claudio_open": claudio.get("dedup_open", 0) or data.get("claudio_open", 0),
    }


def comms_snapshot() -> dict[str, Any]:
    validator = run_command([sys.executable, "COMMS/tools/validate_seto_comms.py", "--json", "--fail-on-errors"], timeout=30)
    validator_json: dict[str, Any] = {}
    try:
        validator_json = json.loads(validator.get("stdout", "{}"))
    except json.JSONDecodeError:
        validator_json = {}
    engine = read_json(ROOT / "qa_artifacts" / "release_validation" / "seto-observacionista-engine-result-2026-05-05.json")
    engine_tests = read_json(ROOT / "qa_artifacts" / "release_validation" / "seto-observacionista-engine-tests-2026-05-05.json")
    return {
        "validator": validator_json or {"status": "ERROR", "raw": validator},
        "observacionista_engine": {
            "status": engine.get("status", "UNKNOWN"),
            "action_gate": engine.get("action_gate", "UNKNOWN"),
            "claim_state": engine.get("claim_state", "UNKNOWN"),
            "phi_eff": engine.get("observationist_engineering", {}).get("Phi_eff"),
            "risk_flags": engine.get("observationist_engineering", {}).get("risk_flags", []),
        },
        "engine_tests": {
            "status": engine_tests.get("status", "UNKNOWN"),
            "total": engine_tests.get("tests", {}).get("total", 0),
            "failures": engine_tests.get("tests", {}).get("failures", 0),
            "errors": engine_tests.get("tests", {}).get("errors", 0),
        },
    }


def geo_security_snapshot() -> dict[str, Any]:
    data = read_json(ROOT / "qa_artifacts" / "control_dashboard" / "geolocation-security-guard-2026-05-05.json")
    if not data:
        return {"status": "UNKNOWN", "action_gate": "REVIEW"}
    return {
        "status": data.get("status", "UNKNOWN"),
        "action_gate": data.get("action_gate", "REVIEW"),
        "reported_google_location": data.get("reported_google_location", ""),
        "windows_location": data.get("windows_location", {}),
        "reasons": data.get("reasons", []),
    }


def control_items() -> list[dict[str, str]]:
    return [
        {
            "lane": "Host",
            "gate": "APPROVE",
            "name": "Activar/verificar VPN WARP",
            "command": "warp-cli connect; warp-cli status",
            "effect": "Mantiene la red en Cloudflare WARP y verifica estado.",
        },
        {
            "lane": "Host",
            "gate": "APPROVE",
            "name": "Verificar geolocalizacion publica",
            "command": "Invoke-RestMethod https://www.cloudflare.com/cdn-cgi/trace",
            "effect": "Confirma warp=on, colo y pais sin tocar archivos.",
        },
        {
            "lane": "Host",
            "gate": "REVIEW",
            "name": "Guard geo/privacidad Claudio",
            "command": "python tools\\security_geolocation_guard.py --connect --reported-google-location \"Yucatan\" --write --json",
            "effect": "Compara WARP, IP publica, Windows location y permisos de navegador.",
        },
        {
            "lane": "Curador",
            "gate": "APPROVE",
            "name": "Refrescar pendientes",
            "command": "python tools\\release\\pending_review.py --write --quiet",
            "effect": "Actualiza snapshot de backlog; no cierra tareas.",
        },
        {
            "lane": "COMMS",
            "gate": "APPROVE",
            "name": "Validar protocolo de agentes",
            "command": "python COMMS\\tools\\validate_seto_comms.py --json --fail-on-errors",
            "effect": "Valida envelopes, schemas, ejemplos y WitnessLog tail.",
        },
        {
            "lane": "Observacionismo",
            "gate": "REVIEW",
            "name": "Ejecutar motor observacionista inverso",
            "command": "python COMMS\\tools\\observacionista_engine.py --input COMMS\\inbox\\claudio-local-agent.jsonl --json",
            "effect": "Calcula R, Phi_eff, gate, perfiles de observador y falsadores.",
        },
        {
            "lane": "Observacionismo",
            "gate": "APPROVE",
            "name": "Benchmarks del motor",
            "command": "python -m unittest COMMS\\tests\\test_observacionista_engine.py",
            "effect": "Prueba REVIEW, BLOCK, control de secret scan y Phi_eff.",
        },
        {
            "lane": "Auditoria",
            "gate": "REVIEW",
            "name": "Inventario activo",
            "command": "python tools\\release\\audit_repo.py",
            "effect": "Inventario local sin publicar ni borrar.",
        },
        {
            "lane": "Seguridad",
            "gate": "REVIEW",
            "name": "Escaneo de secretos por ruta",
            "command": "python tools\\release\\scan_secrets.py --path <ruta> --json --fail-on-findings",
            "effect": "Debe usarse antes de publicar o empaquetar.",
        },
        {
            "lane": "Limpieza",
            "gate": "REVIEW",
            "name": "Candidatos de limpieza",
            "command": "Get-Content DELETE_CANDIDATES.md",
            "effect": "Revisar hashes, ficha y reemplazo antes de borrar.",
        },
        {
            "lane": "Limpieza",
            "gate": "BLOCK",
            "name": "Borrado libre",
            "command": "N/A",
            "effect": "Bloqueado sin ActionGate, hash, reemplazo y DELETED_LOG.",
        },
        {
            "lane": "Publicacion",
            "gate": "BLOCK",
            "name": "Push/deploy/publicacion externa",
            "command": "N/A",
            "effect": "Bloqueado hasta secret scan, licencia, checklist y autorizacion de destino.",
        },
        {
            "lane": "Claudio",
            "gate": "REVIEW",
            "name": "Preflight Claudio local",
            "command": "cd \"-=MEDIOEVO=-\\-=LIBROS\\claudio\"; python tools\\host_observacionista.py --no-write",
            "effect": "Verifica host antes de rutas pesadas o daemons.",
        },
        {
            "lane": "Claudio",
            "gate": "REVIEW",
            "name": "Claudio/Wabi-Sabi consume COMMS",
            "command": "Get-Content COMMS\\handoffs\\2026-05-05-claudio-local-agent-seto.md",
            "effect": "Contrato de lectura para agente local; writes siguen gated.",
        },
        {
            "lane": "Privado",
            "gate": "BLOCK",
            "name": "RPG/TCG hacia public/open",
            "command": "N/A",
            "effect": "Bloqueado por frontera privada.",
        },
    ]


def status_class(value: str) -> str:
    value = str(value).upper()
    if value in {"PASS", "APPROVE", "CONNECTED", "CERTEZA"}:
        return "ok"
    if value in {"REVIEW", "INFERENCIA", "UNKNOWN"}:
        return "review"
    return "block"


def build_snapshot() -> dict[str, Any]:
    return {
        "schema": "medioevo.system_control_dashboard.v1",
        "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "root": str(ROOT),
        "vpn": vpn_snapshot(),
        "git": git_snapshot(),
        "pending": pending_snapshot(),
        "comms": comms_snapshot(),
        "geo_security": geo_security_snapshot(),
        "controls": control_items(),
        "policy": {
            "local_only": True,
            "no_daemon_started": True,
            "external_publication_gate": "BLOCK",
            "private_game_boundary": "BLOCK",
            "unknown_sources": "UNKNOWN_REVIEW_REQUIRED",
        },
    }


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def metric_card(label: str, value: object, state: str = "review") -> str:
    return f"""
      <section class="metric">
        <span class="metric-label">{esc(label)}</span>
        <strong class="{status_class(state)}">{esc(value)}</strong>
      </section>
    """


def render_html(snapshot: dict[str, Any]) -> str:
    vpn = snapshot["vpn"]
    geo = vpn.get("geo", {})
    trace = geo.get("cloudflare_trace", {})
    ipinfo = geo.get("ipinfo", {})
    pending = snapshot["pending"]
    comms = snapshot["comms"]
    geo_security = snapshot.get("geo_security", {})
    controls = snapshot["controls"]
    cards = "\n".join(
        f"""
        <article class="control" data-lane="{esc(item['lane'])}" data-gate="{esc(item['gate'])}">
          <div class="control-head">
            <span class="lane">{esc(item['lane'])}</span>
            <span class="badge {status_class(item['gate'])}">{esc(item['gate'])}</span>
          </div>
          <h3>{esc(item['name'])}</h3>
          <p>{esc(item['effect'])}</p>
          <div class="command-row">
            <code>{esc(item['command'])}</code>
            <button type="button" data-copy="{esc(item['command'])}">Copiar</button>
          </div>
        </article>
        """
        for item in controls
    )
    lanes = sorted({item["lane"] for item in controls})
    lane_buttons = "\n".join(f'<button type="button" data-filter="{esc(lane)}">{esc(lane)}</button>' for lane in lanes)
    snapshot_json = json.dumps(snapshot, ensure_ascii=False, indent=2)
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MEDIOEVO Control Dashboard</title>
  <style>
    :root {{
      --bg: #f7f7f2;
      --surface: #ffffff;
      --text: #18201c;
      --muted: #5d665f;
      --line: #d9ddd6;
      --ok: #0f766e;
      --review: #b45309;
      --block: #b91c1c;
      --blue: #1d4ed8;
      --shadow: 0 10px 22px rgba(22, 28, 24, .08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, Segoe UI, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      letter-spacing: 0;
    }}
    header {{
      padding: 28px clamp(16px, 4vw, 52px);
      background: #14211d;
      color: #f7f7f2;
      display: grid;
      gap: 18px;
    }}
    h1 {{
      font-size: clamp(28px, 4vw, 46px);
      line-height: 1.05;
      margin: 0;
      letter-spacing: 0;
    }}
    header p {{ max-width: 980px; margin: 0; color: #dce5dc; line-height: 1.55; }}
    main {{ padding: 22px clamp(16px, 4vw, 52px) 52px; }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      margin: 0 0 22px;
    }}
    .metric, .panel, .control {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }}
    .metric {{ padding: 16px; min-height: 92px; display: grid; align-content: space-between; }}
    .metric-label {{ color: var(--muted); font-size: 13px; }}
    .metric strong {{ font-size: 22px; line-height: 1.1; overflow-wrap: anywhere; }}
    .panel {{ padding: 18px; margin-bottom: 18px; }}
    .panel h2 {{ font-size: 18px; margin: 0 0 12px; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 12px;
    }}
    dl {{ margin: 0; display: grid; gap: 10px; }}
    dt {{ color: var(--muted); font-size: 12px; text-transform: uppercase; }}
    dd {{ margin: 2px 0 0; font-weight: 650; overflow-wrap: anywhere; }}
    .toolbar {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin: 0 0 14px;
    }}
    button {{
      min-height: 44px;
      border: 1px solid #aab3ac;
      background: #fff;
      color: var(--text);
      border-radius: 8px;
      padding: 0 13px;
      cursor: pointer;
      font-weight: 650;
    }}
    button:focus-visible {{ outline: 3px solid #2563eb; outline-offset: 2px; }}
    button:hover {{ border-color: var(--blue); }}
    .controls {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 12px;
    }}
    .control {{ padding: 16px; display: grid; gap: 12px; min-height: 240px; }}
    .control-head {{ display: flex; justify-content: space-between; gap: 10px; align-items: center; }}
    .lane {{ font-size: 12px; color: var(--muted); text-transform: uppercase; font-weight: 700; }}
    .badge {{ border-radius: 999px; padding: 4px 9px; font-size: 12px; font-weight: 800; }}
    .ok {{ color: var(--ok); }}
    .review {{ color: var(--review); }}
    .block {{ color: var(--block); }}
    .badge.ok {{ color: #fff; background: var(--ok); }}
    .badge.review {{ color: #fff; background: var(--review); }}
    .badge.block {{ color: #fff; background: var(--block); }}
    h3 {{ margin: 0; font-size: 18px; line-height: 1.25; }}
    .control p {{ margin: 0; color: var(--muted); line-height: 1.5; }}
    .command-row {{
      align-self: end;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 8px;
      align-items: stretch;
    }}
    code {{
      display: block;
      background: #111827;
      color: #f9fafb;
      padding: 10px;
      border-radius: 6px;
      overflow-wrap: anywhere;
      font-size: 12px;
      line-height: 1.4;
    }}
    details {{ margin-top: 14px; }}
    summary {{ cursor: pointer; font-weight: 700; min-height: 44px; display: flex; align-items: center; }}
    pre {{
      overflow: auto;
      max-height: 420px;
      background: #111827;
      color: #f9fafb;
      padding: 14px;
      border-radius: 8px;
      font-size: 12px;
    }}
    [hidden] {{ display: none; }}
    @media (max-width: 680px) {{
      .command-row {{ grid-template-columns: 1fr; }}
      .control {{ min-height: auto; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>MEDIOEVO Control Dashboard</h1>
    <p>Consola local para SETO, Claudio/Wabi-Sabi, VPN, seguridad, limpieza y publicacion gated. Los botones copian comandos; no ejecutan acciones destructivas ni publican nada.</p>
  </header>
  <main>
    <section class="metrics" aria-label="Resumen">
      {metric_card("VPN WARP", "Connected" if vpn.get("connected") else "Review", "APPROVE" if vpn.get("connected") else "REVIEW")}
      {metric_card("Geo publica", f"{ipinfo.get('city', '')}, {ipinfo.get('region', '')} {ipinfo.get('country', '')}", "APPROVE" if vpn.get("connected") else "REVIEW")}
      {metric_card("Pendientes activos", pending.get("active_dedup", 0), "REVIEW")}
      {metric_card("Claudio abiertos", pending.get("claudio_open", 0), "REVIEW")}
      {metric_card("COMMS", comms.get("validator", {}).get("status", "UNKNOWN"), comms.get("validator", {}).get("status", "UNKNOWN"))}
      {metric_card("Motor obs", comms.get("observacionista_engine", {}).get("action_gate", "UNKNOWN"), comms.get("observacionista_engine", {}).get("action_gate", "UNKNOWN"))}
      {metric_card("Geo guard", geo_security.get("action_gate", "UNKNOWN"), geo_security.get("action_gate", "UNKNOWN"))}
    </section>

    <section class="panel">
      <h2>Estado de red y VPN</h2>
      <div class="grid">
        <dl>
          <div><dt>Proveedor</dt><dd>{esc(vpn.get("provider"))}</dd></div>
          <div><dt>WARP</dt><dd>{esc(trace.get("warp", "unknown"))}</dd></div>
          <div><dt>Cloudflare colo</dt><dd>{esc(trace.get("colo", "unknown"))}</dd></div>
        </dl>
        <dl>
          <div><dt>IP publica</dt><dd>{esc(ipinfo.get("ip_redacted") or trace.get("ip_redacted", "redacted"))}</dd></div>
          <div><dt>Ciudad/region</dt><dd>{esc(ipinfo.get("city", ""))} / {esc(ipinfo.get("region", ""))}</dd></div>
          <div><dt>ASN</dt><dd>{esc(ipinfo.get("org", ""))}</dd></div>
        </dl>
      </div>
    </section>

    <section class="panel">
      <h2>Guard de geolocalizacion</h2>
      <div class="grid">
        <dl>
          <div><dt>ActionGate</dt><dd class="{status_class(geo_security.get('action_gate', 'UNKNOWN'))}">{esc(geo_security.get('action_gate', 'UNKNOWN'))}</dd></div>
          <div><dt>Google observado</dt><dd>{esc(geo_security.get('reported_google_location', ''))}</dd></div>
          <div><dt>Windows HKCU/HKLM</dt><dd>{esc(geo_security.get('windows_location', {}))}</dd></div>
        </dl>
        <dl>
          <div><dt>Lectura</dt><dd>{esc('; '.join(geo_security.get('reasons', [])[:3]))}</dd></div>
        </dl>
      </div>
    </section>

    <section class="panel">
      <h2>Opciones del sistema</h2>
      <div class="toolbar" aria-label="Filtros">
        <button type="button" data-filter="ALL">Todo</button>
        {lane_buttons}
      </div>
      <div class="controls" id="controls">
        {cards}
      </div>
    </section>

    <section class="panel">
      <h2>Snapshot tecnico</h2>
      <details>
        <summary>Ver JSON del dashboard</summary>
        <pre>{esc(snapshot_json)}</pre>
      </details>
    </section>
  </main>
  <script>
    document.querySelectorAll('[data-filter]').forEach((button) => {{
      button.addEventListener('click', () => {{
        const lane = button.getAttribute('data-filter');
        document.querySelectorAll('.control').forEach((card) => {{
          card.hidden = lane !== 'ALL' && card.getAttribute('data-lane') !== lane;
        }});
      }});
    }});
    document.querySelectorAll('[data-copy]').forEach((button) => {{
      button.addEventListener('click', async () => {{
        const command = button.getAttribute('data-copy') || '';
        if (!navigator.clipboard || command === 'N/A') return;
        await navigator.clipboard.writeText(command);
        const old = button.textContent;
        button.textContent = 'Copiado';
        setTimeout(() => {{ button.textContent = old; }}, 1200);
      }});
    }});
  </script>
</body>
</html>
"""


def write_outputs(snapshot: dict[str, Any]) -> None:
    SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    html_text = "\n".join(line.rstrip() for line in render_html(snapshot).splitlines()) + "\n"
    SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    HTML_PATH.write_text(html_text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the local MEDIOEVO system control dashboard.")
    parser.add_argument("--write", action="store_true", help="Write snapshot JSON and static HTML dashboard.")
    parser.add_argument("--json", action="store_true", help="Print snapshot JSON.")
    args = parser.parse_args()
    snapshot = build_snapshot()
    if args.write:
        write_outputs(snapshot)
    if args.json or not args.write:
        print(json.dumps(snapshot, indent=2, ensure_ascii=False))
    else:
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "html": rel(HTML_PATH),
                    "snapshot": rel(SNAPSHOT_PATH),
                    "vpn_connected": snapshot["vpn"]["connected"],
                    "warp": snapshot["vpn"]["geo"]["cloudflare_trace"].get("warp", "unknown"),
                    "geo": snapshot["vpn"]["geo"].get("ipinfo", {}),
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
