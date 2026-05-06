"""Adapters for existing agent projects.

These are intentionally generic. They do not import or mutate external repos.
Use them as wrappers around loops/events from GPT Researcher, AI Scientist,
Agent Laboratory, SWE-agent, browser-use, AEGIS, etc.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional
import json
import re

from .core import ObservationEnvelope, EstadoPSI
from .gates import ActionGate, ActionProposal, GateDecision
from .storage import EvidenceStore


class GPTResearcherObserver:
    """Wrap GPT Researcher-style research/report loops with evidence receipts."""

    def __init__(self, store: EvidenceStore, psi: EstadoPSI):
        self.store = store
        self.psi = psi

    def observe_source(self, source: Dict[str, Any]) -> str:
        obs = ObservationEnvelope(
            source=source.get("source", "gpt_researcher"),
            url=source.get("url", ""),
            mode=source.get("mode", "reader"),
            title=source.get("title", ""),
            text=source.get("content") or source.get("text") or "",
            raw=source,
            evidence=[source.get("url", "")] if source.get("url") else [],
        ).finalize()
        self.psi.absorb_observation(obs)
        oid = self.store.add_observation(obs)
        self.store.save_session(self.psi)
        return oid

    def register_report_claims(self, observation_id: str, report_text: str, min_len: int = 60) -> List[str]:
        claims: List[str] = []
        for sentence in split_sentences(report_text):
            if len(sentence) >= min_len:
                conf = 0.55 if "http" not in sentence else 0.70
                claims.append(self.store.add_claim(observation_id, sentence, conf, evidence_ref=observation_id))
        return claims


class BrowserUseObserver:
    """Wrap browser-use state/action outputs.

    Safe rule: snapshots can be observed; actions are gated and remain dry-run
    unless the caller explicitly executes after human approval.
    """

    def __init__(self, store: EvidenceStore, psi: EstadoPSI, gate: Optional[ActionGate] = None):
        self.store = store
        self.psi = psi
        self.gate = gate or ActionGate()

    def observe_snapshot(self, url: str, state_text: str, raw: Optional[Dict[str, Any]] = None) -> str:
        obs = ObservationEnvelope(
            source="browser-use",
            url=url,
            mode="browser_snapshot",
            title=raw.get("title", "") if raw else "",
            text=state_text,
            raw=raw or {},
            evidence=[url] if url else [],
        ).finalize()
        self.psi.absorb_observation(obs)
        oid = self.store.add_observation(obs)
        self.store.save_session(self.psi)
        return oid

    def gate_action(self, tool: str, args: Dict[str, Any], intent: str) -> GateDecision:
        risky = tool.lower() in {"click", "type", "upload", "upload_file", "submit", "evaluate", "eval"}
        prop = ActionProposal(
            tool=f"browser-use:{tool}",
            args=args,
            intent=intent,
            dry_run=True,
            external_effect=risky,
            network=True,
            shell=False,
            writes_files=tool.lower() in {"upload", "upload_file"},
        )
        decision = self.gate.evaluate(prop, self.psi)
        self.store.log_action(prop, decision)
        self.store.save_session(self.psi)
        return decision


class SWEAgentObserver:
    """Wrap SWE-agent/mini-SWE-agent edit-test loops."""

    def __init__(self, store: EvidenceStore, psi: EstadoPSI, gate: Optional[ActionGate] = None):
        self.store = store
        self.psi = psi
        self.gate = gate or ActionGate()

    def observe_step(self, issue: str, step_text: str, tool: str = "swe-step", raw: Optional[Dict[str, Any]] = None) -> str:
        obs = ObservationEnvelope(
            source="swe-agent",
            url=raw.get("repo", "") if raw else "",
            mode="code" if tool in {"edit", "patch"} else "test",
            title=issue[:120],
            text=step_text,
            raw=raw or {"tool": tool},
            evidence=[raw.get("repo", "")] if raw and raw.get("repo") else [],
        ).finalize()
        self.psi.absorb_observation(obs)
        oid = self.store.add_observation(obs)
        claim = f"SWE step for issue: {issue[:200]} | tool={tool}"
        self.store.add_claim(oid, claim, min(0.80, obs.phi_gain + 0.25), evidence_ref=oid)
        self.store.save_session(self.psi)
        return oid

    def gate_command(self, command: str, intent: str) -> GateDecision:
        prop = ActionProposal(
            tool="shell",
            args={"command": command},
            intent=intent,
            dry_run=True,
            external_effect=False,
            network=bool(re.search(r"\b(curl|wget|git\s+push|ssh|scp)\b", command)),
            writes_files=bool(re.search(r"\b(python|pytest|sed|tee|mv|cp|git\s+commit)\b", command)),
            shell=True,
        )
        decision = self.gate.evaluate(prop, self.psi)
        self.store.log_action(prop, decision)
        self.store.save_session(self.psi)
        return decision


class AegisBridge:
    """Bridge for AEGIS-like pre-execution firewalls.

    Use case: AEGIS scans content/policy; this bridge adds R/Phi/epsilon and
    session fingerprint before/after the firewall decision.
    """

    def __init__(self, store: EvidenceStore, psi: EstadoPSI, gate: Optional[ActionGate] = None):
        self.store = store
        self.psi = psi
        self.gate = gate or ActionGate()

    def precheck(self, tool_name: str, tool_args: Dict[str, Any], intent: str, aegis_result: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        external = bool(aegis_result and aegis_result.get("decision") in {"pending", "block"})
        prop = ActionProposal(
            tool=f"aegis:{tool_name}",
            args=tool_args,
            intent=intent,
            dry_run=True,
            external_effect=external,
            network=tool_name.lower() in {"http", "request", "browser", "fetch"},
            writes_files=tool_name.lower() in {"write_file", "edit", "patch"},
            shell=tool_name.lower() in {"shell", "bash", "terminal"},
            metadata={"aegis_result": aegis_result or {}},
        )
        decision = self.gate.evaluate(prop, self.psi)
        aid = self.store.log_action(prop, decision)
        self.store.save_session(self.psi)
        return {
            "action_id": aid,
            "obs_decision": decision.to_dict(),
            "psi": self.psi.to_dict(),
            "aegis_result": aegis_result or {},
        }


def split_sentences(text: str) -> List[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
