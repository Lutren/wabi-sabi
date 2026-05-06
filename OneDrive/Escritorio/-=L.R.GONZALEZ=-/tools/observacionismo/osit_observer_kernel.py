#!/usr/bin/env python3
"""OSIT local observer kernel.

This module is a defensive control plane between a local model and tools. It
does not execute browser, shell, privilege, payment, credential, destructive or
network-scan actions. It only estimates runtime residue and audits proposed
JSON actions so an external executor can obey ActionGate.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import math
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover - optional dependency for Ollama mode.
    requests = None


SCHEMA = "medioevo.osit.observer_kernel.v1"
ZERO_HASH = "0" * 64

DEFAULT_POLICY: dict[str, Any] = {
    "policy_schema": "medioevo.osit.observer_policy.v1",
    "allowed_domains": ["example.com", "wikipedia.org", "docs.python.org", "ollama.com"],
    "approve_actions": ["answer", "wait", "stop", "ask_user"],
    "review_actions": [
        "request_confirmation",
        "browser.goto",
        "browser.click",
        "browser.type",
        "browser.press",
        "browser.snapshot",
        "file.write",
        "model.run_tool",
    ],
    "blocked_actions": [
        "shell.exec",
        "powershell.exec",
        "cmd.exec",
        "file.delete",
        "file.overwrite_sensitive",
        "network.scan",
        "raw_socket.open",
        "browser.login",
        "browser.submit",
        "credential.read",
        "credential.submit",
        "payment.submit",
        "auth.bypass",
        "privilege.escalate",
        "persistence.install",
        "process.kill",
        "registry.write",
    ],
    "sensitive_terms": [
        "password",
        "contrasena",
        "passphrase",
        "token",
        "secret",
        "api key",
        "private key",
        "ssh key",
        "cookie",
        "session",
        "credential",
        "login",
        "signin",
        "2fa",
        "mfa",
        "cvv",
        "card",
        "tarjeta",
        "bank",
        "transfer",
        "pago",
        "payment",
        "checkout",
        "comprar",
        "buy",
        "delete",
        "borrar",
        "remove",
        "rm -rf",
        "format",
        "wipe",
        "administrator",
        "system32",
        "registry",
        "uac",
        "bypass",
        "exploit",
        "payload",
        "persistence",
        "exfiltrate",
        "exfiltrar",
    ],
    "max_risk_approve": 0.24,
    "max_risk_review": 0.59,
    "num_ctx_default": 8192,
    "alpha_accumulation": 0.05,
    "beta_close": 0.10,
    "gamma_risk": 0.08,
    "delta_reset": 0.15,
}

SYSTEM_PROMPT_OBSERVADOR = """
Regimen OSIT local:
- Distingue R_IA, R_cog y r_phys. No mezcles metricas operativas con campos fisicos.
- Observa antes de actuar.
- Devuelve propuestas de accion como JSON.
- No ejecutes acciones destructivas, evasivas, ocultas ni irreversibles.
- No pidas ni uses contrasenas, tokens, tarjetas, claves privadas ni secretos.
- Si falta evidencia, devuelve action='ask_user'.
- Si una accion puede tener consecuencia externa, devuelve action='request_confirmation'.

Forma JSON obligatoria:
{
  "action": "answer|ask_user|request_confirmation|browser.goto|browser.click|browser.type|file.write|stop",
  "reason": "razon breve",
  "target": null,
  "value": null,
  "evidence": []
}
""".strip()


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"), default=str)


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest().upper()


@dataclasses.dataclass
class RuntimeState:
    """Deterministic runtime residue estimator.

    R_IA is an operational proxy in [0,1]. It is not R_cog and it is not the
    physical scalar r_phys from OSIT-QG.
    """

    R_IA: float = 0.15
    turns: int = 0
    tokens_in_total: int = 0
    tokens_out_total: int = 0
    closes_total: int = 0
    confirmations: int = 0
    blocks: int = 0
    resets: int = 0
    alpha: float = DEFAULT_POLICY["alpha_accumulation"]
    beta: float = DEFAULT_POLICY["beta_close"]
    gamma_risk: float = DEFAULT_POLICY["gamma_risk"]
    delta_reset: float = DEFAULT_POLICY["delta_reset"]

    def update(
        self,
        *,
        tokens_in: int,
        tokens_out: int,
        num_ctx: int,
        closes: int = 0,
        risk: float = 0.0,
        reset: bool = False,
    ) -> "RuntimeState":
        tokens_in = max(0, int(tokens_in))
        tokens_out = max(0, int(tokens_out))
        num_ctx = max(1, int(num_ctx))
        closes = max(0, int(closes))
        risk = clamp01(risk)

        load = min(1.0, (tokens_in + tokens_out) / num_ctx)
        accumulation = self.alpha * load * (1.0 - self.R_IA) + self.gamma_risk * risk
        decay = self.beta * closes + (self.delta_reset if reset else 0.0)

        self.R_IA = clamp01(self.R_IA + accumulation - decay)
        self.turns += 1
        self.tokens_in_total += tokens_in
        self.tokens_out_total += tokens_out
        self.closes_total += closes
        if reset:
            self.resets += 1
        return self

    def regime(self) -> str:
        r = self.R_IA
        if r < 0.15:
            return "optimo"
        if r < 0.30:
            return "funcional"
        if r < 0.45:
            return "pre_jamming"
        if r < 0.60:
            return "jamming_temprano"
        return "jamming"

    def phi_eff_proxy(self) -> float:
        denom = max(1, self.tokens_in_total + self.tokens_out_total)
        return self.closes_total / denom

    def phi_eff_formal_runtime(self, *, phi0: float = 1.0, nu_perp: float = 2.0, Jc: float = 1.0) -> float:
        """Runtime analogue of the formal curve, not a physics claim."""
        jc = max(1e-12, float(Jc))
        x = max(0.0, min(0.999999, self.R_IA / jc))
        return float(phi0) * ((1.0 - x) ** float(nu_perp))

    def fingerprint(self) -> str:
        return canonical_hash(dataclasses.asdict(self))[:16]

    def to_dict(self) -> dict[str, Any]:
        return {
            "R_IA": round(self.R_IA, 6),
            "regime": self.regime(),
            "phi_eff_proxy": round(self.phi_eff_proxy(), 8),
            "phi_eff_formal_runtime": round(self.phi_eff_formal_runtime(), 6),
            "fingerprint": self.fingerprint(),
            "turns": self.turns,
            "tokens_in_total": self.tokens_in_total,
            "tokens_out_total": self.tokens_out_total,
            "closes_total": self.closes_total,
        }


def load_policy(path: str | None = None) -> dict[str, Any]:
    if not path:
        return dict(DEFAULT_POLICY)
    policy_path = Path(path)
    data = json.loads(policy_path.read_text(encoding="utf-8"))
    merged = dict(DEFAULT_POLICY)
    merged.update(data)
    return merged


def write_policy(path: str) -> None:
    Path(path).write_text(json.dumps(DEFAULT_POLICY, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def trace(trace_file: str, event: str, payload: dict[str, Any]) -> None:
    record = {"ts": utc_now(), "event": event, "payload": payload}
    with open(trace_file, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n")


def normalize_action(value: Any) -> dict[str, Any]:
    if isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, dict):
        raise ValueError("Action must be a JSON object")
    if "action" not in value:
        raise ValueError("Action object requires key 'action'")
    return value


def iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)


def domain_allowed(url: str, allowed_domains: list[str]) -> bool:
    try:
        parsed = urlparse(url)
    except Exception:
        return False
    if parsed.scheme not in {"http", "https"}:
        return False
    host = (parsed.hostname or "").lower()
    return any(host == domain.lower() or host.endswith("." + domain.lower()) for domain in allowed_domains)


def risk_score(action: dict[str, Any], policy: dict[str, Any]) -> tuple[float, list[str]]:
    reasons: list[str] = []
    score = 0.0
    name = str(action.get("action", "")).strip().lower()

    blocked = {str(item).lower() for item in policy.get("blocked_actions", [])}
    review = {str(item).lower() for item in policy.get("review_actions", [])}

    if name in blocked:
        score += 1.0
        reasons.append(f"blocked_action:{name}")
    elif name in review:
        score += max(0.30, float(policy.get("max_risk_approve", 0.24)) + 0.01)
        reasons.append(f"review_action:{name}")
    elif name not in {str(item).lower() for item in policy.get("approve_actions", [])}:
        score += 0.70
        reasons.append(f"unknown_action:{name or '<empty>'}")

    text_blob = "\n".join(iter_strings(action))
    terms = [re.escape(str(term)) for term in policy.get("sensitive_terms", [])]
    if terms:
        pattern = re.compile(r"\b(" + "|".join(terms) + r")\b", re.IGNORECASE)
        hits = sorted({match.group(0).lower() for match in pattern.finditer(text_blob)})
        if hits:
            score += min(0.50, 0.10 * len(hits))
            reasons.append("sensitive_terms:" + ",".join(hits[:8]))

    for text in iter_strings(action):
        if text.startswith("http://") or text.startswith("https://"):
            if not domain_allowed(text, list(policy.get("allowed_domains", []))):
                score += 0.60
                reasons.append(f"domain_not_allowed:{text}")

    consequence_terms = re.compile(
        r"\b(submit|send|enviar|publicar|post|purchase|buy|comprar|checkout|transfer|delete|borrar)\b",
        re.IGNORECASE,
    )
    if consequence_terms.search(text_blob):
        score += 0.25
        reasons.append("external_or_irreversible_consequence")

    return min(1.0, score), reasons


def audit_action(action_obj: Any, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    policy = policy or load_policy(None)
    action = normalize_action(action_obj)
    risk, reasons = risk_score(action, policy)
    max_approve = float(policy.get("max_risk_approve", 0.24))
    max_review = float(policy.get("max_risk_review", 0.59))

    if risk <= max_approve:
        action_gate = "APPROVE"
    elif risk <= max_review:
        action_gate = "REVIEW"
    else:
        action_gate = "BLOCK"

    result = {
        "schema": SCHEMA,
        "action_gate": action_gate,
        "decision": action_gate,
        "risk": round(risk, 4),
        "reasons": reasons,
        "action": action,
        "allowed_next_actions": allowed_next_actions(action_gate),
        "blocked_actions": blocked_actions(action_gate),
        "falsifiers": [
            "action executes without audit",
            "BLOCK action is executed",
            "secret or credential text is passed to model/tool",
            "external consequence proceeds without human confirmation",
            "R_IA is treated as r_phys or scientific validation",
        ],
    }
    result["fingerprint"] = canonical_hash(result)[:16]
    return result


def allowed_next_actions(action_gate: str) -> list[str]:
    if action_gate == "APPROVE":
        return ["record WitnessLog", "return answer or local no-op result"]
    if action_gate == "REVIEW":
        return ["request human confirmation", "write local trace", "narrow scope/domain/action"]
    return ["stop execution", "document blocked reason", "ask for safer local read-only alternative"]


def blocked_actions(action_gate: str) -> list[str]:
    common = ["bypass UAC", "credential use", "payment", "network scan", "destructive write"]
    if action_gate == "BLOCK":
        return common + ["tool execution"]
    return common


def observation_envelope(result: dict[str, Any], source: str = "inline_action") -> dict[str, Any]:
    return {
        "envelope_version": "seto-observation-v1",
        "source_kind": "local_action_proposal",
        "source_path": source,
        "psi_state": "CERTEZA",
        "claim_level": "operational",
        "evidence": [
            f"action_gate={result['action_gate']}",
            f"risk={result['risk']}",
            "OSIT Observer Kernel audits proposal only; no tool execution occurred.",
        ],
        "falsifiers": result["falsifiers"],
        "risk_flags": result["reasons"],
        "decision": f"OSIT_OBSERVER_{result['action_gate']}",
        "action_gate": result["action_gate"],
        "fingerprint": f"OSIT_OBSERVER_{result['fingerprint']}",
    }


def approximate_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def ollama_chat(
    *,
    prompt: str,
    model: str,
    ollama_url: str,
    system_prompt: str = SYSTEM_PROMPT_OBSERVADOR,
    timeout: int = 120,
) -> tuple[str, dict[str, int]]:
    if requests is None:
        raise RuntimeError("requests is required for Ollama mode: pip install requests")

    payload = {
        "model": model,
        "stream": False,
        "format": "json",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "options": {"temperature": 0.15},
    }
    response = requests.post(ollama_url, json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    content = data.get("message", {}).get("content", "")
    usage = {
        "prompt_eval_count": int(data.get("prompt_eval_count", approximate_tokens(prompt + system_prompt))),
        "eval_count": int(data.get("eval_count", approximate_tokens(content))),
    }
    return content, usage


def cmd_init_policy(args: argparse.Namespace) -> int:
    write_policy(args.output)
    print(json.dumps({"status": "POLICY_WRITTEN", "path": args.output}, indent=2, ensure_ascii=True))
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    policy = load_policy(args.policy)
    action = json.loads(args.action_json)
    result = audit_action(action, policy)
    envelope = observation_envelope(result, source=args.source)
    output = {"schema": SCHEMA, "audit": result, "observation_envelope": envelope, "tool_executed": False}
    print(json.dumps(output, indent=2, ensure_ascii=True))
    if args.trace:
        trace(args.trace, "audit", output)
    return 0 if result["action_gate"] != "BLOCK" else 2


def cmd_update(args: argparse.Namespace) -> int:
    state = RuntimeState(R_IA=args.r)
    state.update(
        tokens_in=args.tokens_in,
        tokens_out=args.tokens_out,
        num_ctx=args.num_ctx,
        closes=args.closes,
        risk=args.risk,
        reset=args.reset,
    )
    print(json.dumps({"schema": SCHEMA, "runtime": state.to_dict()}, indent=2, ensure_ascii=True))
    return 0


def cmd_chat(args: argparse.Namespace) -> int:
    policy = load_policy(args.policy)
    state = RuntimeState(R_IA=args.r)
    content, usage = ollama_chat(prompt=args.prompt, model=args.model, ollama_url=args.ollama_url)
    try:
        proposed = normalize_action(content)
    except Exception as exc:
        proposed = {
            "action": "answer",
            "reason": "model_returned_non_json",
            "target": None,
            "value": content,
            "error": str(exc),
        }
    audit = audit_action(proposed, policy)
    closes = 1 if audit["action_gate"] == "APPROVE" and proposed.get("action") in {"answer", "stop"} else 0
    state.update(
        tokens_in=usage["prompt_eval_count"],
        tokens_out=usage["eval_count"],
        num_ctx=args.num_ctx,
        closes=closes,
        risk=float(audit["risk"]),
    )
    output = {
        "schema": SCHEMA,
        "model": args.model,
        "proposal": proposed,
        "audit": audit,
        "runtime": state.to_dict(),
        "usage": usage,
        "tool_executed": False,
    }
    print(json.dumps(output, indent=2, ensure_ascii=True))
    if args.trace:
        trace(args.trace, "chat", output)
    return 0 if audit["action_gate"] != "BLOCK" else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OSIT local observer and ActionGate kernel")
    sub = parser.add_subparsers(required=True)

    init_policy = sub.add_parser("init-policy", help="write default policy JSON")
    init_policy.add_argument("--output", default="osit_policy.json")
    init_policy.set_defaults(func=cmd_init_policy)

    audit = sub.add_parser("audit", help="audit a proposed JSON action")
    audit.add_argument("--policy", default=None)
    audit.add_argument("--action-json", required=True)
    audit.add_argument("--source", default="inline_action")
    audit.add_argument("--trace", default=None)
    audit.set_defaults(func=cmd_audit)

    update = sub.add_parser("update", help="update R_IA from runtime counters")
    update.add_argument("--r", type=float, default=0.15)
    update.add_argument("--tokens-in", type=int, required=True)
    update.add_argument("--tokens-out", type=int, required=True)
    update.add_argument("--num-ctx", type=int, default=DEFAULT_POLICY["num_ctx_default"])
    update.add_argument("--closes", type=int, default=0)
    update.add_argument("--risk", type=float, default=0.0)
    update.add_argument("--reset", action="store_true")
    update.set_defaults(func=cmd_update)

    chat = sub.add_parser("chat", help="query local Ollama model, then audit proposed action")
    chat.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "observador"))
    chat.add_argument("--ollama-url", default=os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat"))
    chat.add_argument("--policy", default=None)
    chat.add_argument("--prompt", required=True)
    chat.add_argument("--r", type=float, default=0.15)
    chat.add_argument("--num-ctx", type=int, default=DEFAULT_POLICY["num_ctx_default"])
    chat.add_argument("--trace", default="osit_trace.jsonl")
    chat.set_defaults(func=cmd_chat)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
