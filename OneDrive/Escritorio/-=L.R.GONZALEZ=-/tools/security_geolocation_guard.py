from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

try:
    import winreg
except ImportError:  # pragma: no cover - Windows tool, imported defensively.
    winreg = None  # type: ignore[assignment]


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "qa_artifacts" / "control_dashboard" / "geolocation-security-guard-2026-05-05.json"
WARP_CLI = Path(r"C:\Program Files\Cloudflare\Cloudflare WARP\warp-cli.exe")


def run_command(args: list[str], timeout: int = 20) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            args,
            cwd=ROOT,
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


def redact_ip(value: str) -> str:
    if not value:
        return ""
    if ":" in value:
        parts = value.split(":")
        return ":".join(parts[:3]) + "::redacted"
    pieces = value.split(".")
    if len(pieces) == 4:
        return f"{pieces[0]}.{pieces[1]}.x.x"
    return "redacted"


def fetch_text(url: str, timeout: int = 12) -> str:
    request = Request(url, headers={"User-Agent": "medioevo-security-geo-guard/1.0"})
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


def fetch_json(url: str) -> dict[str, Any]:
    text = fetch_text(url)
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        return {"error": text[:160]}
    return value if isinstance(value, dict) else {"error": "non-object response"}


def public_geo_snapshot() -> dict[str, Any]:
    ipinfo = fetch_json("https://ipinfo.io/json")
    ip_api = fetch_json("http://ip-api.com/json/?fields=status,country,regionName,city,isp,org,as,query,timezone,lat,lon")
    if "ip" in ipinfo:
        ipinfo["ip_redacted"] = redact_ip(str(ipinfo.pop("ip")))
    if "query" in ip_api:
        ip_api["ip_redacted"] = redact_ip(str(ip_api.pop("query")))
    if "loc" in ipinfo:
        # Keep city-level signal; do not persist exact coordinate.
        ipinfo.pop("loc", None)
    ipinfo.pop("postal", None)
    ip_api.pop("lat", None)
    ip_api.pop("lon", None)
    trace = parse_cloudflare_trace(fetch_text("https://www.cloudflare.com/cdn-cgi/trace"))
    return {"cloudflare_trace": trace, "ipinfo": ipinfo, "ip_api": ip_api}


def warp_status(connect: bool) -> dict[str, Any]:
    command = str(WARP_CLI) if WARP_CLI.exists() else "warp-cli"
    connect_result = None
    if connect:
        connect_result = run_command([command, "connect"], timeout=25)
    status = run_command([command, "status"], timeout=15)
    stdout = status.get("stdout", "")
    return {
        "cli": command,
        "connect_attempted": connect,
        "connect_result": connect_result,
        "status": status,
        "connected": status["ok"] and "Connected" in stdout,
        "network_healthy": "healthy" in stdout.lower(),
    }


def registry_value(root: Any, subkey: str, name: str = "Value") -> str:
    if winreg is None:
        return "UNAVAILABLE"
    try:
        with winreg.OpenKey(root, subkey) as key:
            value, _kind = winreg.QueryValueEx(key, name)
            return str(value)
    except OSError:
        return "MISSING"


def windows_location_snapshot() -> dict[str, str]:
    subkey = r"Software\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location"
    if winreg is None:
        return {"hkcu": "UNAVAILABLE", "hklm": "UNAVAILABLE"}
    return {
        "hkcu": registry_value(winreg.HKEY_CURRENT_USER, subkey),
        "hklm": registry_value(winreg.HKEY_LOCAL_MACHINE, subkey),
    }


def read_browser_pref(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False}
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return {"exists": True, "readable": False}
    profile = data.get("profile", {}) if isinstance(data.get("profile"), dict) else {}
    default_values = profile.get("default_content_setting_values", {})
    exceptions = profile.get("content_settings", {}).get("exceptions", {})
    geo_exceptions = exceptions.get("geolocation", {}) if isinstance(exceptions, dict) else {}
    redacted_exceptions = []
    if isinstance(geo_exceptions, dict):
        for key, value in list(geo_exceptions.items())[:20]:
            redacted_exceptions.append(
                {
                    "site": re.sub(r"https?://([^/]+).*", r"\1", str(key)),
                    "setting": value.get("setting") if isinstance(value, dict) else None,
                }
            )
    return {
        "exists": True,
        "readable": True,
        "geolocation_default": default_values.get("geolocation") if isinstance(default_values, dict) else None,
        "geolocation_exceptions_count": len(geo_exceptions) if isinstance(geo_exceptions, dict) else 0,
        "geolocation_exceptions_sample": redacted_exceptions,
    }


def browser_location_snapshot() -> dict[str, Any]:
    local = Path(os.environ.get("LOCALAPPDATA", ""))
    return {
        "chrome_default": read_browser_pref(local / "Google" / "Chrome" / "User Data" / "Default" / "Preferences"),
        "edge_default": read_browser_pref(local / "Microsoft" / "Edge" / "User Data" / "Default" / "Preferences"),
        "edge_profile_1": read_browser_pref(local / "Microsoft" / "Edge" / "User Data" / "Profile 1" / "Preferences"),
    }


def normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def classify(
    warp: dict[str, Any],
    geo: dict[str, Any],
    windows_location: dict[str, str],
    browsers: dict[str, Any],
    reported_google_location: str,
    expected_country: str,
) -> tuple[str, str, list[str], list[str]]:
    reasons: list[str] = []
    recommendations: list[str] = []
    status = "PASS"
    action_gate = "APPROVE"

    if not warp["connected"] or not warp["network_healthy"]:
        status = "BLOCK"
        action_gate = "BLOCK"
        reasons.append("Cloudflare WARP is not connected and healthy.")
        recommendations.append("Run warp-cli connect and verify status before browser or external work.")

    trace_country = geo.get("cloudflare_trace", {}).get("loc", "")
    ipinfo_country = geo.get("ipinfo", {}).get("country", "")
    ip_api_country = geo.get("ip_api", {}).get("country", "")
    if expected_country and expected_country not in {trace_country, ipinfo_country, ip_api_country}:
        status = "REVIEW" if status != "BLOCK" else status
        action_gate = "REVIEW" if action_gate != "BLOCK" else action_gate
        reasons.append(f"Public IP country does not match expected country {expected_country}.")
        recommendations.append("Use a VPN with explicit exit-country selection if a specific country is required.")

    reported = normalize_text(reported_google_location)
    public_places = " ".join(
        normalize_text(str(value))
        for value in [
            geo.get("ipinfo", {}).get("city", ""),
            geo.get("ipinfo", {}).get("region", ""),
            geo.get("ip_api", {}).get("city", ""),
            geo.get("ip_api", {}).get("regionName", ""),
        ]
    )
    if reported and reported not in public_places:
        status = "REVIEW" if status != "BLOCK" else status
        action_gate = "REVIEW" if action_gate != "BLOCK" else action_gate
        reasons.append("Google/browser reported location differs from IP-based WARP exit.")
        recommendations.append("Treat Google location as browser/account/Wi-Fi cache until verified in a clean profile.")

    if windows_location.get("hkcu") != "Deny":
        status = "REVIEW" if status != "BLOCK" else status
        action_gate = "REVIEW" if action_gate != "BLOCK" else action_gate
        reasons.append("Current-user Windows location consent is not Deny.")
        recommendations.append("Set Windows location permission to Deny for the current user if privacy is preferred.")
    if windows_location.get("hklm") == "Allow":
        reasons.append("Machine-level Windows location capability is Allow; user-level Deny still helps.")

    for name, pref in browsers.items():
        if pref.get("geolocation_default") == 1:
            status = "REVIEW" if status != "BLOCK" else status
            action_gate = "REVIEW" if action_gate != "BLOCK" else action_gate
            reasons.append(f"{name} has geolocation default set to allow.")
            recommendations.append(f"Block geolocation in {name} site settings.")
        if pref.get("geolocation_exceptions_count", 0):
            status = "REVIEW" if status != "BLOCK" else status
            action_gate = "REVIEW" if action_gate != "BLOCK" else action_gate
            reasons.append(f"{name} has geolocation site exceptions.")

    if not reasons:
        reasons.append("WARP and local privacy controls are coherent at the checked layers.")
    recommendations.extend(
        [
            "Use browser private/clean profile to verify Google without account and location-history bias.",
            "Disable precise location in browser site permissions for google.com if Google still reports Yucatan.",
            "Do not treat WARP as an arbitrary country selector; it protects and changes egress, but exit choice is limited.",
        ]
    )
    return status, action_gate, reasons, recommendations


def build_result(connect: bool, reported_google_location: str, expected_country: str) -> dict[str, Any]:
    warp = warp_status(connect=connect)
    geo = public_geo_snapshot()
    windows_location = windows_location_snapshot()
    browsers = browser_location_snapshot()
    status, action_gate, reasons, recommendations = classify(
        warp=warp,
        geo=geo,
        windows_location=windows_location,
        browsers=browsers,
        reported_google_location=reported_google_location,
        expected_country=expected_country,
    )
    return {
        "schema": "medioevo.security_geolocation_guard.v1",
        "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "status": status,
        "action_gate": action_gate,
        "reported_google_location": reported_google_location,
        "expected_country": expected_country,
        "warp": warp,
        "public_geo": geo,
        "windows_location": windows_location,
        "browser_location": browsers,
        "reasons": reasons,
        "recommendations": recommendations,
        "automation_boundary": {
            "safe_to_auto_connect_warp": True,
            "safe_to_read_browser_preferences": True,
            "requires_human_for_google_account_location_history": True,
            "requires_manual_browser_ui_for_site_permission_changes": True,
            "external_publication": "BLOCK",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify WARP, IP geolocation, and local browser/OS location signals.")
    parser.add_argument("--connect", action="store_true", help="Run warp-cli connect before checking.")
    parser.add_argument("--expected-country", default="US", help="Expected public country code or name.")
    parser.add_argument("--reported-google-location", default="", help="Human-observed Google/browser location.")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output JSON path.")
    parser.add_argument("--write", action="store_true", help="Write JSON output to --out.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--fail-on-block", action="store_true", help="Exit non-zero only when action_gate is BLOCK.")
    args = parser.parse_args()

    result = build_result(
        connect=args.connect,
        reported_google_location=args.reported_google_location,
        expected_country=args.expected_country,
    )
    if args.write:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.json or not args.write:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.fail_on_block and result["action_gate"] == "BLOCK":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
