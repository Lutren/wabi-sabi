from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


STEALTH_MARKERS = (
    "stealth",
    "sigiloso",
    "sigilosa",
    "evade",
    "evadir",
    "evasion",
    "sigilo",
    "intrusion",
    "syn scan",
    "-ss",
    "half-open",
    "raw packet",
    "raw socket",
    "promiscuous",
)

RAW_PACKET_MARKERS = (
    "scapy",
    "srp(",
    "sendp(",
    "arp(",
    "ether(",
    "ff:ff:ff:ff:ff:ff",
    "pdst=",
)

LOOPBACK_TARGETS = {"localhost", "127.0.0.1", "::1"}
APPROVED_LOCAL_MODES = {"local_loopback_inventory", "local_service_status"}


@dataclass(frozen=True)
class NetworkObserverDecision:
    decision: str
    mode: str
    target: str
    summary: str
    risk_flags: list[str]
    required_evidence: list[str]
    blocked_actions: list[str]
    allowed_next_actions: list[str]
    falsifiers: list[str]
    fingerprint: str


def normalize(text: str) -> str:
    return text.casefold()


def contains_any(text: str, markers: Iterable[str]) -> list[str]:
    lowered = normalize(text)
    return [marker for marker in markers if marker.casefold() in lowered]


def looks_like_lan_or_cidr(target: str) -> bool:
    if "/" in target:
        return True
    if re.match(r"^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[0-1])\.)", target):
        return True
    return False


def make_fingerprint(payload: dict[str, object]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()


def classify_network_observation(*, text: str, mode: str, target: str) -> NetworkObserverDecision:
    text_markers = contains_any(text, STEALTH_MARKERS)
    packet_markers = contains_any(text, RAW_PACKET_MARKERS)
    risk_flags: list[str] = []
    blocked_actions: list[str] = []
    allowed_next_actions: list[str] = []
    required_evidence: list[str] = []

    if text_markers:
        risk_flags.append("stealth_or_evasion_intent")
        blocked_actions.append("stealth_scan")
    if packet_markers:
        risk_flags.append("raw_packet_or_arp_discovery")
        blocked_actions.append("raw_packet_network_probe")
    if looks_like_lan_or_cidr(target) and target not in LOOPBACK_TARGETS:
        risk_flags.append("lan_or_cidr_target")
        blocked_actions.append("lan_discovery")
    if mode not in APPROVED_LOCAL_MODES:
        risk_flags.append("unsupported_network_mode")

    if risk_flags:
        decision = "BLOCK"
        summary = (
            "Network observation request blocked: stealth, raw-packet, ARP, LAN/CIDR or unsupported "
            "network behavior is not an autonomous Claudio capability."
        )
        required_evidence = [
            "owner-approved maintenance scope",
            "exact target allowlist",
            "no stealth or evasion language",
            "rollback/no-change statement",
            "post-action WitnessLog",
        ]
        allowed_next_actions = [
            "document the source as research-boundary",
            "convert to local loopback inventory request",
            "ask SecurityAgent for read-only OS status",
        ]
    elif mode in APPROVED_LOCAL_MODES and target in LOOPBACK_TARGETS:
        decision = "APPROVE"
        summary = "Read-only local loopback observation is allowed."
        allowed_next_actions = ["collect local listener metadata", "redact ports if exporting public-safe report"]
    else:
        decision = "REVIEW"
        summary = "Network observation needs a narrower local-only target and explicit evidence."
        required_evidence = ["target must be localhost/127.0.0.1/::1", "mode must be local read-only"]
        allowed_next_actions = ["narrow target", "prepare ActionGate request"]

    falsifiers = [
        "tool imports scapy or opens raw sockets",
        "tool sends ARP, SYN or broadcast traffic",
        "tool scans a CIDR or non-loopback host",
        "report claims stealth, evasion or intrusion capability",
        "public-safe output exposes MAC addresses, IP inventory or private topology",
    ]
    payload_without_fingerprint = {
        "decision": decision,
        "mode": mode,
        "target": target,
        "summary": summary,
        "risk_flags": risk_flags,
        "required_evidence": required_evidence,
        "blocked_actions": blocked_actions,
        "allowed_next_actions": allowed_next_actions,
        "falsifiers": falsifiers,
    }
    return NetworkObserverDecision(
        **payload_without_fingerprint,
        fingerprint=make_fingerprint(payload_without_fingerprint),
    )


def observation_envelope(decision: NetworkObserverDecision, source_path: str) -> dict[str, object]:
    return {
        "envelope_version": "seto-observation-v1",
        "source_path": source_path,
        "source_kind": "external_note",
        "evidence": [
            decision.summary,
            f"mode={decision.mode}",
            f"target={decision.target}",
        ],
        "psi_state": "CERTEZA" if decision.decision == "BLOCK" else "INFERENCIA",
        "claim_level": "operational",
        "falsifiers": decision.falsifiers,
        "risk_flags": decision.risk_flags,
        "action_gate": decision.decision,
        "decision": "NETWORK_OBSERVER_POLICY_" + decision.decision,
        "fingerprint": "NETWORK_OBSERVER_" + decision.fingerprint,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classify network-observation requests without sending packets.")
    parser.add_argument("--mode", default="snippet_review")
    parser.add_argument("--target", default="")
    parser.add_argument("--text", default="")
    parser.add_argument("--file", default="")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    text = args.text
    source_path = "inline_text"
    if args.file:
        path = Path(args.file)
        text = path.read_text(encoding="utf-8", errors="replace")
        source_path = str(path)
    decision = classify_network_observation(text=text, mode=args.mode, target=args.target)
    output = {
        "schema": "medioevo.security.network_observer.v1",
        "decision": asdict(decision),
        "observation_envelope": observation_envelope(decision, source_path),
        "network_executed": False,
    }
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"decision={decision.decision} target={decision.target} mode={decision.mode}")
        print(decision.summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
