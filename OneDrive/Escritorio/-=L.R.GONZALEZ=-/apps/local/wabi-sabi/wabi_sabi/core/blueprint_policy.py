from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


BLUEPRINT_PATHS = [
    "docs/ops/WABI_SABI_QWEN_BLUEPRINT_WORKPACK_2026-05-06.md",
    "docs/ops/QWEN_BLUEPRINT_LOCAL_INDEX_2026-05-06.md",
    "docs/ops/WABI_OSIT_BRIDGE_FROM_ESTADO_2026-05-06.md",
    "docs/ops/OSIT_RESOURCE_OPTIMIZER_RUNTIME_SPEC_2026-05-06.md",
    "runtime/prompt_master/prompt_master_execution_controller_2026-05-06.json",
    "COMMS/agents_state/wabi-sabi-sentido-comun.json",
    "COMMS/agents_state/claudio-local-autonomy.json",
]


@dataclass(frozen=True)
class BlueprintSource:
    path: str
    sha256: str
    status: str = "loaded"
    signals: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BlueprintPolicy:
    schema: str = "wabi.blueprint_policy.v1"
    loaded: bool = False
    root: str = ""
    provider_order: list[str] = field(default_factory=lambda: ["codex", "dry-run"])
    ollama_enabled_by_default: bool = False
    prewarm_ollama: bool = False
    reasons: list[str] = field(default_factory=list)
    sources: list[BlueprintSource] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["sources"] = [asdict(source) for source in self.sources]
        return payload


class BlueprintPolicyLoader:
    def __init__(self, *, workspace: str | Path, runtime_root: str | Path) -> None:
        self.workspace = Path(workspace).resolve()
        self.runtime_root = Path(runtime_root).resolve()

    def load(self) -> BlueprintPolicy:
        root = self._find_root()
        if root is None:
            return BlueprintPolicy(
                loaded=False,
                root="",
                reasons=["portfolio_root_not_found", "default_codex_dry_run"],
                missing=list(BLUEPRINT_PATHS),
            )

        sources: list[BlueprintSource] = []
        missing: list[str] = []
        signals: set[str] = set()
        for rel_path in BLUEPRINT_PATHS:
            path = root / rel_path
            if not path.exists():
                missing.append(rel_path)
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            source_signals = _extract_signals(text, suffix=path.suffix.lower())
            signals.update(source_signals)
            sources.append(
                BlueprintSource(
                    path=rel_path,
                    sha256=_sha256(path),
                    signals=sorted(source_signals),
                )
            )

        reasons = _policy_reasons(signals, sources)
        return BlueprintPolicy(
            loaded=bool(sources),
            root=str(root),
            provider_order=["codex", "dry-run"],
            ollama_enabled_by_default=False,
            prewarm_ollama=False,
            reasons=reasons,
            sources=sources,
            missing=missing,
        )

    def _find_root(self) -> Path | None:
        candidates: list[Path] = []
        for base in [self.workspace, self.runtime_root]:
            candidates.extend([base, *base.parents])
        seen: set[Path] = set()
        for candidate in candidates:
            if candidate in seen:
                continue
            seen.add(candidate)
            if (candidate / "docs" / "ops").exists() and (candidate / "COMMS").exists():
                return candidate
            if candidate.name == "-=L.R.GONZALEZ=-":
                return candidate
        return None


def _extract_signals(text: str, *, suffix: str) -> set[str]:
    lowered = text.lower()
    signals: set[str] = set()
    if "ollama queda como backend opcional" in lowered or "ollama es backend opcional" in lowered:
        signals.add("ollama_optional")
    if "alias ollama" in lowered or "ollama aliases" in lowered or "ollama_create_alias" in lowered:
        signals.add("ollama_alias_blocked")
    if "host" in lowered and ("jamming/block" in lowered or "`block`" in lowered):
        signals.add("host_block")
    if "heavy_models_allowed" in lowered and "false" in lowered:
        signals.add("heavy_models_blocked")
    if "no_model_router_change" in lowered or "policy-only" in lowered or "policy_only" in lowered:
        signals.add("policy_only")
    if "no llama modelos por defecto" in lowered or "deterministic_no_llm" in lowered:
        signals.add("deterministic_no_llm")
    if "dry-run" in lowered or "workpack" in lowered:
        signals.add("workpack_fallback")
    if suffix == ".json":
        signals.update(_extract_json_signals(text))
    return signals


def _extract_json_signals(text: str) -> set[str]:
    signals: set[str] = set()
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return signals
    if _contains_value(payload, "JAMMING/BLOCK"):
        signals.add("host_block")
    if _contains_value(payload, "ollama_create_alias"):
        signals.add("ollama_alias_blocked")
    if payload.get("heavy_models_allowed") is False:
        signals.add("heavy_models_blocked")
    if payload.get("action_gate") in {"BLOCK", "REVIEW"}:
        signals.add("gate_not_approve")
    return signals


def _contains_value(value: Any, needle: str) -> bool:
    if isinstance(value, dict):
        return any(_contains_value(item, needle) for item in value.values())
    if isinstance(value, list):
        return any(_contains_value(item, needle) for item in value)
    return str(value) == needle


def _policy_reasons(signals: set[str], sources: list[BlueprintSource]) -> list[str]:
    reasons = ["default_codex_dry_run"]
    if sources:
        reasons.append("blueprints_loaded")
    if "ollama_optional" in signals:
        reasons.append("ollama_optional_by_blueprint")
    if "ollama_alias_blocked" in signals:
        reasons.append("ollama_alias_blocked")
    if "host_block" in signals or "heavy_models_blocked" in signals:
        reasons.append("host_or_heavy_models_blocked")
    if "policy_only" in signals or "deterministic_no_llm" in signals:
        reasons.append("osit_policy_only")
    if "workpack_fallback" in signals:
        reasons.append("workpack_fallback_available")
    return sorted(set(reasons))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()
