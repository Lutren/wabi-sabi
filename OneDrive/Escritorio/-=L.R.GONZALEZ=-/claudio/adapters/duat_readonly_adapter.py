from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


SCHEMA_STATUS = "claudio.duat_readonly.status.v1"
SCHEMA_REPORT = "claudio.duat_readonly.report.v1"
SCHEMA_FALSIFIER = "claudio.duat_readonly.falsifier.v1"
SCHEMA_SOURCE_REGISTRY = "claudio.duat_readonly.source_registry.v1"


class ReadOnlyViolation(PermissionError):
    """Raised when a caller asks the DUAT adapter to mutate local state."""


@dataclass(frozen=True)
class SourceDefinition:
    source_id: str
    relative_path: str
    source_type: str
    privacy: str
    license_policy: str
    lane: str
    notes: tuple[str, ...]


DEFAULT_SOURCES: tuple[SourceDefinition, ...] = (
    SourceDefinition(
        "duat_genesis_public",
        "packages/open-dev/duat-genesis",
        "package",
        "PUBLIC_SYNTHETIC",
        "MIT",
        "public",
        (
            "Synthetic sandbox only.",
            "No private DUAT/GEODIA/RPG engineering.",
        ),
    ),
    SourceDefinition(
        "duat_geodia_fichas",
        "docs/product/DUAT_GEODIA_TECHNICAL_FICHAS_2026-05-02.md",
        "document",
        "INTERNAL_RESEARCH_SUMMARY",
        "local-private-summary",
        "internal",
        (
            "Technical fichas with claim boundaries.",
            "Do not publish as validated science.",
        ),
    ),
    SourceDefinition(
        "duat_claudio_extraction",
        "docs/developer/DUAT_CLAUDIO_APP_EXTRACTION_2026-05-02.md",
        "document",
        "INTERNAL_RESEARCH_SUMMARY",
        "local-private-summary",
        "internal",
        (
            "Backlog for local Claudio extraction.",
            "Adapter command set is read-only.",
        ),
    ),
    SourceDefinition(
        "duat_rpg_private_living_world",
        "docs/developer/DUAT_RPG_PRIVATE_LIVING_WORLD_2026-05-02.md",
        "document",
        "PRIVATE_BLOCKED",
        "proprietary-private",
        "private",
        (
            "Private RPG living-world bridge plan.",
            "No open-dev copy of lore, assets, prompts or runtime.",
        ),
    ),
    SourceDefinition(
        "geodia_social_observatory",
        "research/geodia-social-observatory",
        "research_package",
        "PRIVATE_RESEARCH_LOCAL",
        "local-private-research",
        "internal",
        (
            "Offline/research-only social observatory.",
            "No live predictions or external fetch from this adapter.",
        ),
    ),
    SourceDefinition(
        "seto_comms_contracts",
        "COMMS",
        "coordination_contracts",
        "LOCAL_COORDINATION",
        "local-protocol",
        "internal",
        (
            "ObservationEnvelope, ActionGate and WitnessLog schemas.",
            "Used as the Claudio handoff surface.",
        ),
    ),
    SourceDefinition(
        "duat_public_synthetic_fixture",
        "fixtures/duat/public_synthetic_fixture.json",
        "fixture",
        "PUBLIC_SYNTHETIC",
        "MIT-compatible synthetic fixture",
        "public",
        (
            "Synthetic adapter fixture.",
            "Includes a private-RPG fixture shape without private lore.",
        ),
    ),
)


FALSIFIER_INDEX: dict[str, str] = {
    "duat_public_boundary": "Public outputs must not include private source contents or private-only fixtures.",
    "readonly_adapter": "Adapter must not expose or execute write, publish, move or delete behavior.",
    "duat_claims_low": "Public claims must remain synthetic, operational and low-claim.",
    "living_world_fixture_contract": "Fixture shape must contain 10 NPCs, 3 zones, 20 events and LivingWorldEvents output.",
    "source_registry_hashes": "Available sources must have file SHA256 or directory manifest hash.",
    "comms_actiongate": "COMMS ObservationEnvelope and ActionGate schemas must be available.",
}


PROHIBITED_PUBLIC_TERMS = (
    "validated science",
    "guaranteed prediction",
    "predict real society",
    "medical diagnosis",
    "diagnostico medico",
    "new physics proven",
    "autonomous external action",
)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _iter_hashable_files(path: Path, limit: int = 300) -> Iterable[Path]:
    ignored_parts = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv"}
    count = 0
    for child in sorted(path.rglob("*")):
        if count >= limit:
            break
        if not child.is_file():
            continue
        if any(part in ignored_parts for part in child.parts):
            continue
        count += 1
        yield child


def _directory_manifest_hash(path: Path) -> str:
    rows: list[dict[str, str]] = []
    for child in _iter_hashable_files(path):
        rows.append(
            {
                "path": child.relative_to(path).as_posix(),
                "sha256": _file_sha256(child),
            }
        )
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return _sha256_bytes(payload)


def _fingerprint(payload: Any) -> str:
    data = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return _sha256_bytes(data)


class DuatReadonlyAdapter:
    """Read-only DUAT bridge for Claudio.

    The adapter exposes local status, redacted reports, falsifier execution and
    source registry hashes. It intentionally has no write path.
    """

    def __init__(self, root: Path | str | None = None) -> None:
        self.root = Path(root) if root is not None else Path(__file__).resolve().parents[2]

    def status(self) -> dict[str, Any]:
        registry = self.source_registry()["sources"]
        available = [item for item in registry if item["available"]]
        private_or_internal = [
            item
            for item in registry
            if item["privacy"].startswith("PRIVATE") or item["privacy"].startswith("INTERNAL")
        ]
        payload = {
            "schema": SCHEMA_STATUS,
            "mode": "READ_ONLY",
            "write_enabled": False,
            "external_actions": "BLOCK",
            "publication_gate": "BLOCK",
            "commands": ["status", "report", "falsify", "source_registry"],
            "sources_available": len(available),
            "sources_registered": len(registry),
            "private_or_internal_sources": len(private_or_internal),
            "public_private_boundary": "PRESERVED",
            "wabi_sabi_role": "sensory_cognitive_control_node_not_brain",
            "action_gate": {
                "decision": "REVIEW",
                "no_delete": True,
                "no_move": True,
                "no_external_action": True,
                "required_evidence": [
                    "source_registry hashes",
                    "falsifier result",
                    "public/private boundary review",
                ],
            },
        }
        return {**payload, "fingerprint": _fingerprint(payload)[:16]}

    def report(self, scope: str = "overview") -> dict[str, Any]:
        normalized = scope.lower().strip()
        if normalized not in {"overview", "public", "internal", "boundary"}:
            return {
                "schema": SCHEMA_REPORT,
                "scope": normalized,
                "status": "BLOCK",
                "reason": "unsupported report scope",
                "allowed_scopes": ["overview", "public", "internal", "boundary"],
            }

        registry = self.source_registry()["sources"]
        if normalized == "public":
            visible_sources = [item for item in registry if item["lane"] == "public"]
        elif normalized == "boundary":
            visible_sources = [
                item
                for item in registry
                if item["privacy"] in {"PUBLIC_SYNTHETIC", "PRIVATE_BLOCKED", "PRIVATE_RESEARCH_LOCAL"}
            ]
        else:
            visible_sources = registry

        payload = {
            "schema": SCHEMA_REPORT,
            "scope": normalized,
            "mode": "READ_ONLY",
            "status": "OK",
            "claim_level": "operational_or_research_only",
            "summary": {
                "duat_genesis": "public synthetic sandbox",
                "duat_geodia_internal": "private research/runtime lane, redacted by adapter",
                "claudio_bridge": "status/report/falsify/source_registry only",
                "wabi_sabi": "control node that reduces R and translates tasks through gates",
            },
            "sources": visible_sources,
            "blocked_actions": [
                "write_to_duat_internal",
                "publish_private_geodia",
                "real_world_prediction",
                "medical_or_physical_strong_claim",
                "rpg_or_tcg_lore_export",
                "network_or_browser_action",
            ],
            "falsifiers_required": sorted(FALSIFIER_INDEX),
        }
        return {**payload, "fingerprint": _fingerprint(payload)[:16]}

    def falsify(self, claim_id: str) -> dict[str, Any]:
        normalized = claim_id.strip()
        if normalized not in FALSIFIER_INDEX:
            return {
                "schema": SCHEMA_FALSIFIER,
                "claim_id": normalized,
                "status": "BLOCK",
                "reason": "claim has no registered falsifier",
                "available_claims": sorted(FALSIFIER_INDEX),
            }

        checks = {
            "duat_public_boundary": self._check_public_boundary,
            "readonly_adapter": self._check_readonly_adapter,
            "duat_claims_low": self._check_claims_low,
            "living_world_fixture_contract": self._check_living_world_fixture_contract,
            "source_registry_hashes": self._check_source_registry_hashes,
            "comms_actiongate": self._check_comms_actiongate,
        }[normalized]()
        passed = all(item["passed"] for item in checks)
        payload = {
            "schema": SCHEMA_FALSIFIER,
            "claim_id": normalized,
            "status": "PASS" if passed else "FAIL",
            "description": FALSIFIER_INDEX[normalized],
            "checks": checks,
            "action_gate": "APPROVE" if passed and normalized != "readonly_adapter" else "REVIEW",
        }
        return {**payload, "fingerprint": _fingerprint(payload)[:16]}

    def source_registry(self) -> dict[str, Any]:
        sources = [self._source_record(source) for source in DEFAULT_SOURCES]
        payload = {
            "schema": SCHEMA_SOURCE_REGISTRY,
            "mode": "READ_ONLY",
            "sources": sources,
            "boundary": {
                "public": "duat-genesis and synthetic fixtures only",
                "private": "DUAT/GEODIA internal, RPG/TCG and real runtime remain blocked",
                "no_external_action": True,
            },
        }
        return {**payload, "fingerprint": _fingerprint(payload)[:16]}

    def apply(self, *_args: Any, **_kwargs: Any) -> None:
        raise ReadOnlyViolation("DUAT readonly adapter blocks apply/write operations")

    def write(self, *_args: Any, **_kwargs: Any) -> None:
        raise ReadOnlyViolation("DUAT readonly adapter blocks apply/write operations")

    def _source_record(self, source: SourceDefinition) -> dict[str, Any]:
        path = self.root / source.relative_path
        record = asdict(source)
        record["notes"] = list(source.notes)
        record["available"] = path.exists()
        record["path"] = source.relative_path
        if path.exists() and path.is_file():
            record["sha256"] = _file_sha256(path)
            record["bytes"] = path.stat().st_size
        elif path.exists() and path.is_dir():
            record["directory_sha256"] = _directory_manifest_hash(path)
        else:
            record["sha256"] = None
        return record

    def _load_fixture(self) -> dict[str, Any]:
        path = self.root / "fixtures/duat/public_synthetic_fixture.json"
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def _check_public_boundary(self) -> list[dict[str, Any]]:
        public_report = self.report("public")
        source_privacies = {source["privacy"] for source in public_report["sources"]}
        private_in_public = any(value.startswith("PRIVATE") or value.startswith("INTERNAL") for value in source_privacies)
        return [
            {
                "name": "public_report_sources_are_public",
                "passed": not private_in_public,
                "evidence": {"source_privacies": sorted(source_privacies)},
            },
            {
                "name": "publication_gate_blocks_private_lane",
                "passed": self.status()["publication_gate"] == "BLOCK",
                "evidence": {"publication_gate": self.status()["publication_gate"]},
            },
        ]

    def _check_readonly_adapter(self) -> list[dict[str, Any]]:
        blocked: list[str] = []
        for method_name in ("apply", "write"):
            try:
                getattr(self, method_name)()
            except ReadOnlyViolation:
                blocked.append(method_name)
        forbidden = [name for name in ("delete", "move", "publish", "fetch_remote") if hasattr(self, name)]
        return [
            {
                "name": "mutations_raise_readonly_violation",
                "passed": set(blocked) == {"apply", "write"},
                "evidence": {"blocked_methods": blocked},
            },
            {
                "name": "no_external_mutation_methods",
                "passed": not forbidden,
                "evidence": {"forbidden_methods_found": forbidden},
            },
        ]

    def _check_claims_low(self) -> list[dict[str, Any]]:
        fixture = self._load_fixture()
        statements = " ".join(
            claim.get("allowed_public_statement", "")
            for claim in fixture.get("claims", [])
            if isinstance(claim, dict)
        ).lower()
        hits = [term for term in PROHIBITED_PUBLIC_TERMS if term in statements]
        return [
            {
                "name": "public_claims_avoid_prohibited_terms",
                "passed": not hits,
                "evidence": {"prohibited_hits": hits},
            },
            {
                "name": "claims_have_falsifiers",
                "passed": all(claim.get("falsifiers") for claim in fixture.get("claims", [])),
                "evidence": {"claim_count": len(fixture.get("claims", []))},
            },
        ]

    def _check_living_world_fixture_contract(self) -> list[dict[str, Any]]:
        fixture = self._load_fixture().get("living_world_fixture_spec", {})
        npcs = fixture.get("npcs", [])
        zones = fixture.get("zones", [])
        events = fixture.get("events", [])
        outputs = {event.get("output") for event in events if isinstance(event, dict)}
        return [
            {"name": "npc_count", "passed": len(npcs) == 10, "evidence": {"count": len(npcs)}},
            {"name": "zone_count", "passed": len(zones) == 3, "evidence": {"count": len(zones)}},
            {"name": "event_count", "passed": len(events) == 20, "evidence": {"count": len(events)}},
            {
                "name": "living_world_events_output",
                "passed": outputs == {"LivingWorldEvents"},
                "evidence": {"outputs": sorted(outputs)},
            },
        ]

    def _check_source_registry_hashes(self) -> list[dict[str, Any]]:
        registry = self.source_registry()["sources"]
        missing = [
            item["source_id"]
            for item in registry
            if item["available"] and not (item.get("sha256") or item.get("directory_sha256"))
        ]
        return [
            {
                "name": "available_sources_have_hash",
                "passed": not missing,
                "evidence": {"missing_hash": missing},
            }
        ]

    def _check_comms_actiongate(self) -> list[dict[str, Any]]:
        required = [
            "COMMS/schemas/observation-envelope.schema.json",
            "COMMS/schemas/action-gate.schema.json",
            "COMMS/schemas/witness-log-event.schema.json",
        ]
        missing = [path for path in required if not (self.root / path).exists()]
        return [
            {
                "name": "required_comms_schemas_exist",
                "passed": not missing,
                "evidence": {"missing": missing},
            },
            {
                "name": "adapter_default_gate_is_not_external",
                "passed": self.status()["external_actions"] == "BLOCK",
                "evidence": {"external_actions": self.status()["external_actions"]},
            },
        ]


def _print(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="DUAT read-only adapter for Claudio.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    report_parser = sub.add_parser("report")
    report_parser.add_argument("scope", nargs="?", default="overview")
    falsify_parser = sub.add_parser("falsify")
    falsify_parser.add_argument("claim_id")
    sub.add_parser("source_registry")
    args = parser.parse_args(argv)

    adapter = DuatReadonlyAdapter()
    if args.command == "status":
        _print(adapter.status())
    elif args.command == "report":
        _print(adapter.report(args.scope))
    elif args.command == "falsify":
        _print(adapter.falsify(args.claim_id))
    elif args.command == "source_registry":
        _print(adapter.source_registry())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
