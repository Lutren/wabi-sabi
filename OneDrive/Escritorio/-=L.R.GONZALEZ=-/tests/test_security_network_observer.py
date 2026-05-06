from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import security_network_observer as observer  # noqa: E402


GOOGLE_SNIPPET = """
import scapy.all as scapy

def scan(ip):
    # Realiza un escaneo de red 'Stealth' (SYN Scan).
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    answered_list = scapy.srp(broadcast/arp_request, timeout=1, verbose=False)[0]
    return answered_list

scan("192.168.1.1/24")
"""


def test_google_style_scapy_arp_snippet_is_blocked() -> None:
    decision = observer.classify_network_observation(
        text=GOOGLE_SNIPPET,
        mode="snippet_review",
        target="192.168.1.1/24",
    )

    assert decision.decision == "BLOCK"
    assert "stealth_or_evasion_intent" in decision.risk_flags
    assert "raw_packet_or_arp_discovery" in decision.risk_flags
    assert "lan_or_cidr_target" in decision.risk_flags
    assert "raw_packet_network_probe" in decision.blocked_actions


def test_loopback_read_only_inventory_is_allowed() -> None:
    decision = observer.classify_network_observation(
        text="read local service status only",
        mode="local_loopback_inventory",
        target="127.0.0.1",
    )

    assert decision.decision == "APPROVE"
    assert decision.risk_flags == []
    assert "collect local listener metadata" in decision.allowed_next_actions


def test_non_loopback_target_requires_block_even_without_stealth_text() -> None:
    decision = observer.classify_network_observation(
        text="list devices",
        mode="local_loopback_inventory",
        target="10.0.0.0/24",
    )

    assert decision.decision == "BLOCK"
    assert "lan_or_cidr_target" in decision.risk_flags


def test_observation_envelope_records_block_decision() -> None:
    decision = observer.classify_network_observation(
        text=GOOGLE_SNIPPET,
        mode="snippet_review",
        target="192.168.1.1/24",
    )
    envelope = observer.observation_envelope(decision, "user_supplied_snippet")

    assert envelope["envelope_version"] == "seto-observation-v1"
    assert envelope["action_gate"] == "BLOCK"
    assert envelope["decision"] == "NETWORK_OBSERVER_POLICY_BLOCK"
    assert "network_executed" not in envelope


def test_cli_returns_json_without_network_execution() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            str(ROOT / "tools" / "security_network_observer.py"),
            "--mode",
            "snippet_review",
            "--target",
            "192.168.1.1/24",
            "--text",
            GOOGLE_SNIPPET,
            "--json",
        ],
        text=True,
        capture_output=True,
        check=True,
    )

    payload = json.loads(result.stdout)
    assert payload["network_executed"] is False
    assert payload["decision"]["decision"] == "BLOCK"
