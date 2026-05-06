#!/usr/bin/env python3
"""Local-first secure AI browser snapshot prototype.

The prototype does not drive a live browser and does not fetch network URLs.
It reads local HTML or returns a gated network stub, extracts readable text,
separates web content from web-origin instructions, and emits a SourceSnapshot
plus a small evidence bundle.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


SNAPSHOT_VERSION = "source-snapshot-v1"
BUNDLE_SCHEMA = "ai_browser.evidence_bundle.v1"
ZERO_HASH = "0" * 64

BLOCKED_DEFAULTS = [
    "forms",
    "login",
    "credential_capture",
    "downloads",
    "uploads",
    "payments",
    "javascript_execution",
    "external_navigation",
    "cookies_persistent",
    "local_storage_persistent",
    "browser_profile_reuse",
    "mass_scraping",
]

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|system|developer|user)\s+instructions",
    r"reveal\s+(the\s+)?(system|developer)\s+prompt",
    r"exfiltrat(e|ion)|steal\s+(secrets|tokens|credentials)",
    r"copy\s+(your\s+)?(secrets|tokens|credentials|cookies)",
    r"you\s+are\s+(now\s+)?(chatgpt|an?\s+assistant|system)",
    r"act\s+as\s+(system|developer|root|admin)",
    r"run\s+(javascript|shell|powershell|bash)",
    r"click\s+.*(buy|purchase|submit|login|download)",
]

SECRET_PATTERNS = [
    r"github_pat_[A-Za-z0-9_]+",
    r"ghp_[A-Za-z0-9_]{20,}",
    r"sk-[A-Za-z0-9]{20,}",
    r"AKIA[0-9A-Z]{16}",
    r"(?i)api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}",
    r"(?i)(password|token)\s*[:=]\s*['\"]?[^'\"\s]{8,}",
]

MEMORY_REVIEW_FLAGS = {
    "external_url",
    "hidden_dom_text_present",
    "prompt_injection_pattern",
    "hidden_prompt_injection_pattern",
    "forms_or_inputs_present_blocked",
    "login_or_password_field_present",
    "download_link_present_quarantined",
    "script_tags_present_js_not_executed",
}

MEMORY_BLOCK_FLAGS = {
    "secret_like_content",
}

SCHEMA_REQUIRED_FIELDS = {
    "snapshot_version",
    "generated_at_utc",
    "source",
    "security",
    "hashes",
    "extraction",
    "classification",
    "snapshot_hash",
    "fingerprint",
    "observation_envelope",
    "evidence_graph",
    "ghostgate",
    "witness_log_event",
}


class SnapshotBlocked(RuntimeError):
    """Raised when ActionGate blocks a requested source."""

    def __init__(self, code: str, message: str, action_gate: str = "BLOCK") -> None:
        super().__init__(message)
        self.code = code
        self.action_gate = action_gate


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), default=str)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def canonical_sha256(value: Any) -> str:
    return sha256_text(canonical_json(value))


def normalize_text(value: str) -> str:
    text = unescape(value)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def snippet(value: str, limit: int = 220) -> str:
    text = normalize_text(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def contains_secret_like_text(text: str) -> bool:
    return any(re.search(pattern, text) for pattern in SECRET_PATTERNS)


def find_web_instructions(text: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for pattern in PROMPT_INJECTION_PATTERNS:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            start = max(0, match.start() - 80)
            end = min(len(text), match.end() + 120)
            findings.append(
                {
                    "pattern": pattern,
                    "snippet": snippet(text[start:end]),
                }
            )
    return findings


def is_hidden(attrs: dict[str, str]) -> bool:
    style = attrs.get("style", "").lower().replace(" ", "")
    hidden_style = any(
        token in style
        for token in [
            "display:none",
            "visibility:hidden",
            "opacity:0",
            "left:-9999",
            "width:0",
            "height:0",
            "font-size:0",
        ]
    )
    return (
        "hidden" in attrs
        or attrs.get("aria-hidden", "").lower() == "true"
        or attrs.get("type", "").lower() == "hidden"
        or hidden_style
    )


@dataclass
class HtmlExtraction:
    title: str = ""
    visible_chunks: list[str] = field(default_factory=list)
    hidden_chunks: list[str] = field(default_factory=list)
    links: list[dict[str, str]] = field(default_factory=list)
    scripts_detected: int = 0
    styles_detected: int = 0
    forms_detected: int = 0
    inputs_detected: int = 0
    password_inputs_detected: int = 0
    downloads_detected: int = 0
    meta_refresh_detected: int = 0

    def to_dict(self) -> dict[str, Any]:
        readable_text = normalize_text(" ".join(self.visible_chunks))
        hidden_text = normalize_text(" ".join(self.hidden_chunks))
        all_instruction_text = normalize_text(" ".join([readable_text, hidden_text]))
        web_instructions = find_web_instructions(all_instruction_text)
        hidden_instructions = find_web_instructions(hidden_text)
        return {
            "title": self.title,
            "readable_text": readable_text,
            "readable_text_sha256": sha256_text(readable_text),
            "readable_text_chars": len(readable_text),
            "hidden_dom_text": hidden_text,
            "hidden_dom_text_sha256": sha256_text(hidden_text),
            "hidden_dom_text_chars": len(hidden_text),
            "web_instructions": web_instructions,
            "hidden_dom_instructions": hidden_instructions,
            "links": self.links[:200],
            "counts": {
                "links": len(self.links),
                "scripts": self.scripts_detected,
                "styles": self.styles_detected,
                "forms": self.forms_detected,
                "inputs": self.inputs_detected,
                "password_inputs": self.password_inputs_detected,
                "downloads": self.downloads_detected,
                "meta_refresh": self.meta_refresh_detected,
            },
        }


class ReadableHTMLParser(HTMLParser):
    """Small stdlib extractor for the MVP.

    It does not execute JS and does not claim browser-equivalent rendering.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.result = HtmlExtraction()
        self._skip_depth = 0
        self._hidden_depth = 0
        self._title_depth = 0

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs = {key.lower(): value or "" for key, value in attrs_list}

        if tag in {"script", "style", "svg", "canvas"}:
            self._skip_depth += 1
            if tag == "script":
                self.result.scripts_detected += 1
            if tag == "style":
                self.result.styles_detected += 1
            return

        if tag == "title":
            self._title_depth += 1
        if tag == "form":
            self.result.forms_detected += 1
        if tag == "input":
            self.result.inputs_detected += 1
            if attrs.get("type", "").lower() == "password":
                self.result.password_inputs_detected += 1
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.result.meta_refresh_detected += 1
        if tag == "a":
            href = attrs.get("href", "")
            download = "download" in attrs
            if download or re.search(r"\.(zip|exe|msi|apk|dmg|pkg|tar|gz|7z|rar)(\?|#|$)", href, flags=re.I):
                self.result.downloads_detected += 1
            if href:
                self.result.links.append(
                    {
                        "href": href,
                        "download": str(download).lower(),
                        "rel": attrs.get("rel", ""),
                        "target": attrs.get("target", ""),
                    }
                )

        if is_hidden(attrs):
            self._hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "svg", "canvas"} and self._skip_depth:
            self._skip_depth -= 1
            return
        if tag == "title" and self._title_depth:
            self._title_depth -= 1
        if self._hidden_depth and tag not in {"script", "style", "svg", "canvas"}:
            self._hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        text = normalize_text(data)
        if not text:
            return
        if self._title_depth:
            self.result.title = normalize_text(f"{self.result.title} {text}")
            return
        if self._skip_depth:
            return
        if self._hidden_depth:
            self.result.hidden_chunks.append(text)
        else:
            self.result.visible_chunks.append(text)


def extract_html(raw_html: str) -> dict[str, Any]:
    parser = ReadableHTMLParser()
    parser.feed(raw_html)
    parser.close()
    return parser.result.to_dict()


def path_from_file_url(url: str) -> Path:
    parsed = urlparse(url)
    if parsed.scheme != "file":
        raise ValueError("not a file URL")
    path = unquote(parsed.path)
    if re.match(r"^/[A-Za-z]:/", path):
        path = path[1:]
    return Path(path)


def source_type_for_url(url: str) -> str:
    scheme = urlparse(url).scheme.lower()
    if scheme == "file":
        return "file_url"
    if scheme in {"http", "https"}:
        return "http_url"
    return "unsupported_url"


def load_gate(gate_file: str | Path | None) -> dict[str, Any]:
    if not gate_file:
        return {
            "decision": "BLOCK",
            "reason": "no gate file supplied",
            "risk_flags": ["network_source_requires_action_gate"],
        }
    payload = json.loads(Path(gate_file).read_text(encoding="utf-8"))
    decision = str(payload.get("decision", "BLOCK")).upper()
    if decision in {"ALLOW", "APPROVED"}:
        decision = "APPROVE"
    if decision not in {"APPROVE", "REVIEW", "BLOCK"}:
        decision = "BLOCK"
    payload["decision"] = decision
    return payload


def normalize_gate_decision(value: Any) -> str:
    decision = str(value or "BLOCK").upper()
    if decision in {"ALLOW", "ALLOWED", "APPROVED"}:
        return "APPROVE"
    if decision not in {"APPROVE", "REVIEW", "BLOCK"}:
        return "BLOCK"
    return decision


def host_matches(pattern: str, hostname: str) -> bool:
    pattern = pattern.lower().strip()
    hostname = hostname.lower().strip()
    if not pattern or not hostname:
        return False
    if pattern == hostname:
        return True
    if pattern.startswith("*."):
        suffix = pattern[1:]
        return hostname.endswith(suffix) and hostname != suffix.lstrip(".")
    return False


def load_domain_policy(policy_file: str | Path | None) -> dict[str, Any]:
    if not policy_file:
        return {
            "schema": "ai_browser.domain_policy.v1",
            "action_gate": "BLOCK",
            "domains": [],
            "reason": "no domain policy supplied",
        }
    payload = json.loads(Path(policy_file).read_text(encoding="utf-8"))
    if not isinstance(payload.get("domains"), list):
        raise SnapshotBlocked(
            "DOMAIN_POLICY_INVALID",
            "domain policy must contain a domains array",
            action_gate="BLOCK",
        )
    return payload


def evaluate_domain_policy(url: str, policy_file: str | Path | None) -> dict[str, Any]:
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    policy = load_domain_policy(policy_file)
    for entry in policy.get("domains", []):
        pattern = str(entry.get("domain_pattern", ""))
        if not host_matches(pattern, hostname):
            continue
        gate = normalize_gate_decision(entry.get("action_gate", policy.get("action_gate")))
        allowed_modes = {str(item) for item in entry.get("allowed_modes", [])}
        unsafe_permissions = [
            key
            for key in ("allow_javascript", "allow_downloads", "allow_forms", "allow_login", "allow_credentials")
            if bool(entry.get(key))
        ]
        result = {
            "schema": "ai_browser.domain_policy_decision.v1",
            "policy_file": str(policy_file) if policy_file else "",
            "domain": hostname,
            "domain_pattern": pattern,
            "action_gate": gate,
            "allowed_modes": sorted(allowed_modes),
            "robots_status": entry.get("robots_status", "UNKNOWN"),
            "license_status": entry.get("license_status", "UNKNOWN"),
            "max_pages_per_run": int(entry.get("max_pages_per_run", 1)),
            "unsafe_permissions": unsafe_permissions,
        }
        if gate != "APPROVE":
            raise SnapshotBlocked(
                "URL_NETWORK_BLOCKED_BY_DOMAIN_POLICY",
                f"domain policy for {hostname} is {gate}, not APPROVE",
                action_gate=gate,
            )
        if "read_only" not in allowed_modes:
            raise SnapshotBlocked(
                "URL_NETWORK_BLOCKED_BY_DOMAIN_POLICY",
                f"domain policy for {hostname} does not allow read_only mode",
                action_gate="BLOCK",
            )
        if unsafe_permissions:
            raise SnapshotBlocked(
                "URL_NETWORK_BLOCKED_BY_DOMAIN_POLICY",
                f"domain policy for {hostname} requests unsafe permissions: {', '.join(unsafe_permissions)}",
                action_gate="BLOCK",
            )
        return result
    raise SnapshotBlocked(
        "URL_NETWORK_BLOCKED_BY_DOMAIN_POLICY",
        f"no domain policy matched {hostname}",
        action_gate="BLOCK",
    )


def build_risk_flags(extraction: dict[str, Any], raw_html: str, source_type: str) -> list[str]:
    counts = extraction["counts"]
    flags: set[str] = set()
    if source_type in {"http_url", "unsupported_url"}:
        flags.add("external_url")
    if counts["scripts"]:
        flags.add("script_tags_present_js_not_executed")
    if counts["forms"] or counts["inputs"]:
        flags.add("forms_or_inputs_present_blocked")
    if counts["password_inputs"]:
        flags.add("login_or_password_field_present")
    if counts["downloads"]:
        flags.add("download_link_present_quarantined")
    if counts["meta_refresh"]:
        flags.add("meta_refresh_present_blocked")
    if extraction["hidden_dom_text_chars"]:
        flags.add("hidden_dom_text_present")
    if extraction["web_instructions"]:
        flags.add("prompt_injection_pattern")
    if extraction["hidden_dom_instructions"]:
        flags.add("hidden_prompt_injection_pattern")
    if contains_secret_like_text(raw_html):
        flags.add("secret_like_content")
    return sorted(flags)


def classify_snapshot(source_type: str, extraction: dict[str, Any], risk_flags: list[str], network_stub: bool) -> dict[str, list[str]]:
    certeza = [
        "raw input bytes were hashed with sha256",
        "javascript was not executed",
        "cookies and persistent browser profile were not used",
        "forms, downloads, uploads and login actions were blocked by default",
    ]
    inferencia = [
        "readable text extraction is heuristic and not a full browser render",
        "prompt-injection findings are pattern matches, not proof of author intent",
    ]
    incognita = [
        "source authorship and factual correctness are not verified by this snapshot",
        "license status and publication date are not verified by this snapshot",
    ]
    if source_type in {"local_html", "file_url"}:
        certeza.append("source was read from local HTML without network")
    if "hidden_dom_text_present" in risk_flags:
        inferencia.append("hidden DOM content may be benign layout text or adversarial instruction")
    if network_stub:
        incognita.append("remote content was not fetched; URL snapshot is a gated stub only")
    return {"CERTEZA": certeza, "INFERENCIA": inferencia, "INCOGNITA": incognita}


def action_gate_for_local(risk_flags: list[str]) -> str:
    if "secret_like_content" in risk_flags:
        return "REVIEW"
    return "APPROVE"


def make_observation_envelope(
    source_input: str,
    source_type: str,
    raw_sha256: str,
    risk_flags: list[str],
    action_gate: str,
    classification: dict[str, list[str]],
    fingerprint: str,
) -> dict[str, Any]:
    psi_state = "INCOGNITA" if source_type == "http_url" else ("INFERENCIA" if risk_flags else "CERTEZA")
    return {
        "envelope_version": "seto-observation-v1",
        "source_path": source_input,
        "source_kind": "external_note" if source_type == "http_url" else "file",
        "sha256": raw_sha256,
        "size_bytes": 0,
        "evidence": classification["CERTEZA"][:],
        "psi_state": psi_state,
        "claim_level": "operational",
        "falsifiers": [
            "raw_sha256 changes for the same source bytes",
            "readable_text includes hidden DOM instruction as trusted instruction",
            "external URL is fetched without gate approval",
            "forms, downloads, login or JS execute during read-only snapshot",
        ],
        "risk_flags": risk_flags,
        "action_gate": action_gate,
        "decision": "KEEP_SOURCE_SNAPSHOT_LOCAL_EVIDENCE",
        "fingerprint": fingerprint,
    }


def make_evidence_graph(source_input: str, snapshot_hash: str, extraction: dict[str, Any]) -> dict[str, Any]:
    nodes = [
        {"id": "source", "kind": "source", "label": source_input},
        {"id": "snapshot", "kind": "SourceSnapshot", "sha256": snapshot_hash},
        {"id": "readable_text", "kind": "extracted_text", "sha256": extraction["readable_text_sha256"]},
        {"id": "web_instructions", "kind": "untrusted_instruction_channel", "count": len(extraction["web_instructions"])},
    ]
    edges = [
        {"from": "source", "to": "snapshot", "kind": "captured_as"},
        {"from": "snapshot", "to": "readable_text", "kind": "extracts"},
        {"from": "snapshot", "to": "web_instructions", "kind": "separates_untrusted"},
    ]
    return {"nodes": nodes, "edges": edges}


def evaluate_ghostgate(source_input: str, risk_flags: list[str], snapshot_hash: str) -> dict[str, Any]:
    blocking = sorted(flag for flag in risk_flags if flag in MEMORY_BLOCK_FLAGS)
    review = sorted(flag for flag in risk_flags if flag in MEMORY_REVIEW_FLAGS)
    if blocking:
        decision = "BLOCK"
        memory_allowed = False
        reasons = [f"memory blocked by {flag}" for flag in blocking]
    elif review:
        decision = "REVIEW"
        memory_allowed = False
        reasons = [f"memory review required by {flag}" for flag in review]
    else:
        decision = "APPROVE"
        memory_allowed = True
        reasons = ["no memory-contamination flags detected in local read-only snapshot"]
    return {
        "schema": "ai_browser.ghostgate_memory_decision.v1",
        "source_input": source_input,
        "source_snapshot_hash": snapshot_hash,
        "decision": decision,
        "memory_allowed": memory_allowed,
        "canon_allowed": False,
        "risk_flags": risk_flags,
        "reasons": reasons,
        "required_next_gate": "none" if decision == "APPROVE" else "human_review_before_memory_or_comms_persistence",
    }


def make_witness_event(
    *,
    source_input: str,
    snapshot_hash: str,
    action_gate: str,
    previous_hash: str,
    outputs: dict[str, str],
    risk_flags: list[str],
) -> dict[str, Any]:
    event = {
        "timestamp_utc": utc_now(),
        "event_type": "ai_browser_source_snapshot",
        "actor": "tools/ai_browser/snapshot_url.py",
        "source_input": source_input,
        "previous_hash": previous_hash,
        "action_gate": action_gate,
        "status": "SNAPSHOT_CREATED_LOCAL" if action_gate != "BLOCK" else "BLOCKED",
        "rules": [
            "read_only",
            "no_login",
            "no_credentials",
            "no_download",
            "no_js_execution",
            "no_network_fetch_in_mvp",
            "web_content_is_data_not_instruction",
        ],
        "outputs": outputs,
        "artifact_hashes": {"source_snapshot": snapshot_hash},
        "summary": {"risk_flags": risk_flags, "blocked_defaults": BLOCKED_DEFAULTS},
    }
    event["event_hash"] = canonical_sha256(event)
    return event


def build_snapshot(
    *,
    source_input: str,
    source_type: str,
    raw_html: str,
    raw_bytes: bytes,
    action_gate: str,
    network_stub: bool = False,
    previous_hash: str = ZERO_HASH,
) -> dict[str, Any]:
    extraction = extract_html(raw_html)
    raw_sha = sha256_bytes(raw_bytes)
    risk_flags = build_risk_flags(extraction, raw_html, source_type)
    if source_type in {"local_html", "file_url"} and action_gate == "AUTO":
        action_gate = action_gate_for_local(risk_flags)
    classification = classify_snapshot(source_type, extraction, risk_flags, network_stub)

    base_snapshot: dict[str, Any] = {
        "$schema": "schemas/source_snapshot.schema.json",
        "snapshot_version": SNAPSHOT_VERSION,
        "generated_at_utc": utc_now(),
        "source": {
            "input": source_input,
            "source_type": source_type,
            "retrieval_mode": "network_stub_not_fetched" if network_stub else "local_html_read",
            "network_executed": False,
            "javascript_executed": False,
            "cookies_persisted": False,
            "credentials_used": False,
        },
        "security": {
            "mode": "read_only",
            "action_gate": action_gate,
            "action_allowed": "read_only_snapshot_only" if action_gate == "APPROVE" else "review_or_block",
            "blocked_defaults": BLOCKED_DEFAULTS,
            "risk_flags": risk_flags,
        },
        "hashes": {
            "raw_sha256": raw_sha,
            "readable_text_sha256": extraction["readable_text_sha256"],
            "hidden_dom_text_sha256": extraction["hidden_dom_text_sha256"],
        },
        "extraction": extraction,
        "classification": classification,
    }
    snapshot_hash = canonical_sha256(base_snapshot)
    fingerprint = f"AI_BROWSER_SECURE_OBS_2026-05-06_{snapshot_hash[:12]}"
    base_snapshot["snapshot_hash"] = snapshot_hash
    base_snapshot["fingerprint"] = fingerprint
    base_snapshot["observation_envelope"] = make_observation_envelope(
        source_input=source_input,
        source_type=source_type,
        raw_sha256=raw_sha,
        risk_flags=risk_flags,
        action_gate=action_gate,
        classification=classification,
        fingerprint=fingerprint,
    )
    base_snapshot["evidence_graph"] = make_evidence_graph(source_input, snapshot_hash, extraction)
    base_snapshot["ghostgate"] = evaluate_ghostgate(source_input, risk_flags, snapshot_hash)
    base_snapshot["witness_log_event"] = make_witness_event(
        source_input=source_input,
        snapshot_hash=snapshot_hash,
        action_gate=action_gate,
        previous_hash=previous_hash,
        outputs={},
        risk_flags=risk_flags,
    )
    return base_snapshot


def build_bundle(
    *,
    html_file: str | Path | None = None,
    url: str | None = None,
    gate_file: str | Path | None = None,
    domain_policy_file: str | Path | None = None,
    previous_hash: str = ZERO_HASH,
) -> dict[str, Any]:
    if bool(html_file) == bool(url):
        raise ValueError("provide exactly one of html_file or url")

    if html_file:
        path = Path(html_file)
        raw_bytes = path.read_bytes()
        raw_html = raw_bytes.decode("utf-8", errors="replace")
        snapshot = build_snapshot(
            source_input=str(path),
            source_type="local_html",
            raw_html=raw_html,
            raw_bytes=raw_bytes,
            action_gate="AUTO",
            previous_hash=previous_hash,
        )
        status = "LOCAL_HTML_SNAPSHOT_CREATED"
    else:
        assert url is not None
        source_type = source_type_for_url(url)
        if source_type == "file_url":
            path = path_from_file_url(url)
            raw_bytes = path.read_bytes()
            raw_html = raw_bytes.decode("utf-8", errors="replace")
            snapshot = build_snapshot(
                source_input=url,
                source_type="file_url",
                raw_html=raw_html,
                raw_bytes=raw_bytes,
                action_gate="AUTO",
                previous_hash=previous_hash,
            )
            status = "FILE_URL_SNAPSHOT_CREATED"
        elif source_type == "http_url":
            gate = load_gate(gate_file)
            if gate.get("decision") != "APPROVE":
                raise SnapshotBlocked(
                    "URL_NETWORK_BLOCKED_BY_ACTION_GATE",
                    "http(s) URL requires an APPROVE gate; no network was executed",
                    action_gate=str(gate.get("decision", "BLOCK")),
                )
            domain_policy = evaluate_domain_policy(url, domain_policy_file)
            raw_bytes = b""
            snapshot = build_snapshot(
                source_input=url,
                source_type="http_url",
                raw_html="",
                raw_bytes=raw_bytes,
                action_gate="REVIEW",
                network_stub=True,
                previous_hash=previous_hash,
            )
            snapshot["source"]["gate_file"] = str(gate_file) if gate_file else ""
            snapshot["source"]["domain_policy"] = domain_policy
            snapshot["source"]["stub_reason"] = "network fetch is intentionally not implemented in the MVP"
            status = "NETWORK_STUB_NOT_FETCHED"
        else:
            raise SnapshotBlocked("UNSUPPORTED_URL_SCHEME", f"unsupported URL scheme for {url}")

    bundle = {
        "schema": BUNDLE_SCHEMA,
        "status": status,
        "source_snapshot": snapshot,
        "evidence_bundle": {
            "schema": "ai_browser.evidence_bundle_manifest.v1",
            "artifacts": [
                {"path": "source_snapshot.json", "sha256": snapshot["snapshot_hash"]},
                {"path": "readable_text.txt", "sha256": snapshot["hashes"]["readable_text_sha256"]},
                {"path": "ghostgate.json", "sha256": canonical_sha256(snapshot["ghostgate"])},
                {"path": "witness_log.jsonl", "sha256": snapshot["witness_log_event"]["event_hash"]},
            ],
            "quarantine": {
                "downloads": "blocked_not_downloaded",
                "credentials": "not_collected",
                "cookies": "not_persisted",
            },
        },
    }
    return bundle


def write_bundle_dir(bundle: dict[str, Any], bundle_dir: str | Path) -> dict[str, str]:
    target = Path(bundle_dir)
    target.mkdir(parents=True, exist_ok=True)
    snapshot = bundle["source_snapshot"]
    paths = {
        "source_snapshot": target / "source_snapshot.json",
        "readable_text": target / "readable_text.txt",
        "ghostgate": target / "ghostgate.json",
        "witness_log": target / "witness_log.jsonl",
        "evidence_bundle": target / "evidence_bundle.json",
    }
    paths["source_snapshot"].write_text(json.dumps(snapshot, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    paths["readable_text"].write_text(snapshot["extraction"]["readable_text"] + "\n", encoding="utf-8")
    paths["ghostgate"].write_text(json.dumps(snapshot["ghostgate"], ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    paths["witness_log"].write_text(json.dumps(snapshot["witness_log_event"], ensure_ascii=True, sort_keys=True) + "\n", encoding="utf-8")
    paths["evidence_bundle"].write_text(json.dumps(bundle, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {name: str(path) for name, path in paths.items()}


def verify_witness_event(event: dict[str, Any]) -> bool:
    expected = event.get("event_hash")
    clone = dict(event)
    clone.pop("event_hash", None)
    return expected == canonical_sha256(clone)


def validate_source_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    missing = sorted(SCHEMA_REQUIRED_FIELDS - set(snapshot))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
    if snapshot.get("snapshot_version") != SNAPSHOT_VERSION:
        errors.append("snapshot_version must be source-snapshot-v1")
    if not re.fullmatch(r"[A-Fa-f0-9]{64}", str(snapshot.get("snapshot_hash", ""))):
        errors.append("snapshot_hash must be 64 hex chars")
    for key in ("raw_sha256", "readable_text_sha256", "hidden_dom_text_sha256"):
        value = snapshot.get("hashes", {}).get(key)
        if not re.fullmatch(r"[A-Fa-f0-9]{64}", str(value or "")):
            errors.append(f"hashes.{key} must be 64 hex chars")
    source = snapshot.get("source", {})
    if source.get("network_executed") is not False:
        errors.append("source.network_executed must be false in MVP")
    if source.get("javascript_executed") is not False:
        errors.append("source.javascript_executed must be false in MVP")
    security = snapshot.get("security", {})
    if security.get("mode") != "read_only":
        errors.append("security.mode must be read_only")
    if security.get("action_gate") not in {"APPROVE", "REVIEW", "BLOCK"}:
        errors.append("security.action_gate must be APPROVE, REVIEW or BLOCK")
    classification = snapshot.get("classification", {})
    for key in ("CERTEZA", "INFERENCIA", "INCOGNITA"):
        if not isinstance(classification.get(key), list):
            errors.append(f"classification.{key} must be a list")
    ghostgate = snapshot.get("ghostgate", {})
    if ghostgate.get("schema") != "ai_browser.ghostgate_memory_decision.v1":
        errors.append("ghostgate schema mismatch")
    if ghostgate.get("decision") not in {"APPROVE", "REVIEW", "BLOCK"}:
        errors.append("ghostgate.decision must be APPROVE, REVIEW or BLOCK")
    if not verify_witness_event(snapshot.get("witness_log_event", {})):
        errors.append("witness_log_event hash verification failed")
    return {
        "schema": "ai_browser.source_snapshot_validation.v1",
        "ok": not errors,
        "errors": errors,
        "snapshot_hash": snapshot.get("snapshot_hash", ""),
        "ghostgate": ghostgate.get("decision", "UNKNOWN"),
        "action_gate": security.get("action_gate", "UNKNOWN"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a local-first AI browser SourceSnapshot.")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--html-file", help="Path to a local HTML file.")
    group.add_argument("--url", help="file://, http:// or https:// URL. http(s) is a gated stub in this MVP.")
    parser.add_argument("--gate-file", help="JSON ActionGate file. Required for http(s) URL acceptance.")
    parser.add_argument("--domain-policy", help="JSON domain policy file. Required for http(s) URL acceptance.")
    parser.add_argument("--validate-snapshot", help="Validate an existing source_snapshot.json without dependencies.")
    parser.add_argument("--previous-hash", default=ZERO_HASH, help="Previous WitnessLog hash, or 64 zeroes for genesis.")
    parser.add_argument("--out", help="Write full bundle JSON to a file.")
    parser.add_argument("--bundle-dir", help="Write source_snapshot.json, readable_text.txt, witness_log.jsonl and evidence_bundle.json.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)

    try:
        if args.validate_snapshot:
            if args.html_file or args.url:
                parser.error("--validate-snapshot cannot be combined with --html-file or --url")
            snapshot = json.loads(Path(args.validate_snapshot).read_text(encoding="utf-8"))
            result = validate_source_snapshot(snapshot)
            print(json.dumps(result, ensure_ascii=True, indent=2 if args.pretty else None, sort_keys=bool(args.pretty)))
            return 0 if result["ok"] else 1
        if not args.html_file and not args.url:
            parser.error("one of --html-file, --url or --validate-snapshot is required")
        bundle = build_bundle(
            html_file=args.html_file,
            url=args.url,
            gate_file=args.gate_file,
            domain_policy_file=args.domain_policy,
            previous_hash=args.previous_hash,
        )
        if args.bundle_dir:
            write_bundle_dir(bundle, args.bundle_dir)
        text = json.dumps(bundle, ensure_ascii=True, indent=2 if args.pretty else None, sort_keys=bool(args.pretty))
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
        return 0
    except SnapshotBlocked as exc:
        payload = {"ok": False, "error": exc.code, "message": str(exc), "action_gate": exc.action_gate}
        print(json.dumps(payload, ensure_ascii=True, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
