from __future__ import annotations

import json
import re
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from wabi_sabi.core.patch_planner import SENSITIVE_PATH_PARTS, resolve_workspace_text_target
from wabi_sabi.core.redaction import redact_mapping, redact_text
from wabi_sabi.core.task_spec_planner import TASK_SPEC_SCHEMA
from wabi_sabi.core.tools import write_artifact


CLOUD_CODE_PROPOSAL_SCHEMA = "wabi.cloud_code_proposal.v0_1"
CLOUD_CODE_PROPOSAL_PROMPT_SCHEMA = "wabi.cloud_code_proposal_prompt.v0_2"
MAX_CHANGES = 20
MAX_CONTENT_CHARS = 250_000
VALID_GATE_RECOMMENDATIONS = {"APPROVE", "REVIEW", "BLOCK"}
PROPOSAL_INPUT_BLOCKED_PARTS = SENSITIVE_PATH_PARTS - {"runtime"}


@dataclass(frozen=True)
class CloudCodeProposalValidation:
    ok: bool
    path: Path
    proposal: dict[str, Any]
    sanitized: dict[str, Any]
    errors: list[str]
    warnings: list[str]
    redacted_fields: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": "wabi.cloud_code_proposal_validation.v0_1",
            "ok": self.ok,
            "path": str(self.path),
            "proposal_schema": self.proposal.get("schema", ""),
            "summary": self.sanitized.get("summary", ""),
            "intent": self.sanitized.get("intent", ""),
            "changes_count": len(self.sanitized.get("changes", [])),
            "test_commands": list(self.sanitized.get("test_commands", [])),
            "gate_recommendation": self.sanitized.get("gate_recommendation", "REVIEW"),
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "redacted_fields": list(self.redacted_fields),
            "cloud_authority": "proposal_only",
        }


def validate_cloud_code_proposal(
    *,
    workspace: str | Path,
    proposal_path: str | Path,
    input_roots: list[str | Path] | None = None,
) -> CloudCodeProposalValidation:
    workspace_path = Path(workspace).resolve()
    path = _resolve_proposal_input(workspace_path, proposal_path, input_roots=input_roots)
    errors: list[str] = []
    warnings: list[str] = []
    raw = _load_json(path, errors)
    if not isinstance(raw, dict):
        raw = {}
    sanitized, redacted_fields = _sanitize_payload(raw)
    schema = sanitized.get("schema")
    if schema != CLOUD_CODE_PROPOSAL_SCHEMA:
        errors.append(f"unsupported_cloud_code_proposal_schema:{schema}")
    summary = str(sanitized.get("summary", "")).strip()
    if not summary:
        errors.append("cloud_proposal_summary_required")
    changes = sanitized.get("changes")
    if not isinstance(changes, list) or not changes:
        errors.append("cloud_proposal_changes_required")
        changes = []
    if len(changes) > MAX_CHANGES:
        errors.append(f"cloud_proposal_too_many_changes:{len(changes)}")
    _validate_string_list(sanitized, "assumptions", errors)
    _validate_string_list(sanitized, "risks", errors)
    _validate_string_list(sanitized, "rollback_notes", errors)
    _validate_string_list(sanitized, "debug_strategy", errors)
    _validate_files_to_read(workspace_path, sanitized.get("files_to_read", []), errors, warnings)
    _validate_changes(workspace_path, changes, errors, warnings, redacted_fields)
    _validate_commands(sanitized.get("commands_requested", []), field="commands_requested", errors=errors)
    _validate_commands(sanitized.get("test_commands", []), field="test_commands", errors=errors)
    gate = str(sanitized.get("gate_recommendation", "REVIEW")).upper()
    if gate not in VALID_GATE_RECOMMENDATIONS:
        warnings.append(f"gate_recommendation_normalized_to_REVIEW:{gate}")
        sanitized["gate_recommendation"] = "REVIEW"
    else:
        sanitized["gate_recommendation"] = gate
    if redacted_fields:
        warnings.append("secret_like_values_redacted")
    return CloudCodeProposalValidation(
        ok=not errors,
        path=path,
        proposal=raw,
        sanitized=sanitized,
        errors=errors,
        warnings=warnings,
        redacted_fields=redacted_fields,
    )


def cloud_proposal_to_task_spec(validation: CloudCodeProposalValidation) -> dict[str, Any]:
    if not validation.ok:
        raise ValueError("cloud_code_proposal_invalid:" + ";".join(validation.errors))
    proposal = validation.sanitized
    return {
        "schema": TASK_SPEC_SCHEMA,
        "summary": str(proposal["summary"]).strip(),
        "changes": [
            {
                "operation": "write_text",
                "target": str(change["target"]),
                **({"suffix": str(change["suffix"])} if change.get("suffix") else {}),
                "content": str(change["content"]),
            }
            for change in proposal.get("changes", [])
        ],
        "test_commands": [str(command) for command in proposal.get("test_commands", [])],
        "metadata": {
            "source_schema": CLOUD_CODE_PROPOSAL_SCHEMA,
            "source_path": str(validation.path),
            "intent": str(proposal.get("intent", "")),
            "files_to_read": list(proposal.get("files_to_read", [])),
            "commands_requested": list(proposal.get("commands_requested", [])),
            "assumptions": list(proposal.get("assumptions", [])),
            "risks": list(proposal.get("risks", [])),
            "rollback_notes": list(proposal.get("rollback_notes", [])),
            "debug_strategy": list(proposal.get("debug_strategy", [])),
            "cloud_gate_recommendation": proposal.get("gate_recommendation", "REVIEW"),
            "cloud_authority": "proposal_only",
            "redacted_fields": list(validation.redacted_fields),
        },
    }


def write_cloud_task_spec_artifact(output_dir: str | Path, task_spec: dict[str, Any]) -> Path:
    text = json.dumps(task_spec, indent=2, ensure_ascii=False) + "\n"
    return write_artifact(Path(output_dir) / "cloud_task_specs", "wabi_cloud_task_spec", ".json", text)


def build_cloud_code_proposal_prompt(*, intent: str, workspace_summary: dict[str, Any] | None = None) -> str:
    summary = redact_mapping(workspace_summary or {})
    schema = {
        "schema": CLOUD_CODE_PROPOSAL_SCHEMA,
        "summary": "short human summary",
        "intent": "operator intent",
        "assumptions": ["explicit assumption"],
        "files_to_read": ["relative/path.py"],
        "changes": [
            {
                "operation": "write_text",
                "target": "relative/path.py",
                "suffix": ".py",
                "content": "complete file text",
            }
        ],
        "commands_requested": ["python -m py_compile relative/path.py"],
        "test_commands": ["python -m py_compile relative/path.py"],
        "risks": ["risk or boundary"],
        "rollback_notes": ["how local Wabi can roll back"],
        "debug_strategy": ["sanitized debug step"],
        "gate_recommendation": "REVIEW",
    }
    return "\n".join(
        [
            f"Schema prompt: {CLOUD_CODE_PROPOSAL_PROMPT_SCHEMA}",
            "Act as a cloud code planner only. You do not execute code and you do not control the PC.",
            "Return exactly one JSON object and no markdown.",
            "The JSON must match this contract:",
            json.dumps(schema, indent=2, ensure_ascii=False),
            "",
            "Hard rules:",
            "- Use only operation=write_text.",
            "- Use relative workspace paths only.",
            "- Omit private values, auth keys, env files, unsafe shell operations, pipe chains, redirects, network send actions, release operations, or file removal.",
            "- Commands must be SafeExecutor-compatible: python -m py_compile, python -m pytest, or pytest.",
            "- Prefer gate_recommendation=REVIEW unless the change is trivial and fully testable.",
            "- Include complete replacement file content for each change.",
            "",
            "Operator intent:",
            redact_text(intent),
            "",
            "Sanitized workspace summary:",
            json.dumps(summary, indent=2, ensure_ascii=False),
        ]
    )


def build_dry_run_cloud_code_proposal(*, intent: str) -> dict[str, Any]:
    clean_intent = redact_text(intent).strip() or "dry-run cloud proposal"
    return {
        "schema": CLOUD_CODE_PROPOSAL_SCHEMA,
        "summary": "dry-run provider proposal for Wabi cloud bridge",
        "intent": clean_intent,
        "assumptions": [
            "No cloud provider was called.",
            "This proposal is a local contract fixture for validation and planning.",
        ],
        "files_to_read": [],
        "changes": [
            {
                "operation": "write_text",
                "target": "examples/wabi_cloud_proposal_generated.py",
                "suffix": ".py",
                "content": (
                    "def cloud_proposal_status() -> str:\n"
                    "    return \"proposal_ready\"\n"
                ),
            },
            {
                "operation": "write_text",
                "target": "examples/test_wabi_cloud_proposal_generated.py",
                "suffix": ".py",
                "content": (
                    "from wabi_cloud_proposal_generated import cloud_proposal_status\n\n\n"
                    "def test_cloud_proposal_status() -> None:\n"
                    "    assert cloud_proposal_status() == \"proposal_ready\"\n"
                ),
            },
        ],
        "commands_requested": [
            "python -m py_compile examples/wabi_cloud_proposal_generated.py examples/test_wabi_cloud_proposal_generated.py"
        ],
        "test_commands": [
            "python -m py_compile examples/wabi_cloud_proposal_generated.py examples/test_wabi_cloud_proposal_generated.py"
        ],
        "risks": [
            "A generated proposal is not execution approval.",
            "Apply remains separated behind task-spec-apply and local gates.",
        ],
        "rollback_notes": ["SafeExecutor and RollbackStore own source mutation rollback."],
        "debug_strategy": ["Use sanitized test stderr/stdout only if apply is requested later."],
        "gate_recommendation": "REVIEW",
    }


def extract_cloud_code_proposal_payload(text: str) -> dict[str, Any]:
    redacted = redact_text(text)
    direct = _try_json_object(redacted.strip())
    if direct is not None:
        return direct
    for match in re.finditer(r"```(?:json)?\s*(\{.*?\})\s*```", redacted, re.IGNORECASE | re.DOTALL):
        fenced = _try_json_object(match.group(1).strip())
        if fenced is not None:
            return fenced
    decoder = json.JSONDecoder()
    for index, char in enumerate(redacted):
        if char != "{":
            continue
        try:
            candidate, _ = decoder.raw_decode(redacted[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict):
            return candidate
    raise ValueError("cloud_proposal_json_not_found")


def write_cloud_proposal_artifact(output_dir: str | Path, proposal: dict[str, Any], *, source: str) -> Path:
    payload = redact_mapping(proposal)
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    safe_source = source.replace(":", "_")
    return write_artifact(Path(output_dir) / "cloud_proposals", f"wabi_cloud_proposal_{safe_source}", ".json", text)


def _try_json_object(text: str) -> dict[str, Any] | None:
    if not text:
        return None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _resolve_proposal_input(
    workspace: Path,
    proposal_path: str | Path,
    *,
    input_roots: list[str | Path] | None = None,
) -> Path:
    raw = Path(proposal_path)
    candidate = raw.resolve() if raw.is_absolute() else (workspace / raw).resolve()
    allowed_roots = [workspace.resolve()]
    allowed_roots.extend(Path(root).resolve() for root in (input_roots or []))
    if not any(candidate == root or root in candidate.parents for root in allowed_roots):
        raise ValueError(f"target_outside_workspace:{candidate}")
    lowered_parts = {part.lower() for part in candidate.parts}
    blocked = sorted(PROPOSAL_INPUT_BLOCKED_PARTS.intersection(lowered_parts))
    if blocked:
        raise ValueError("cloud_proposal_path_blocked:" + ",".join(blocked))
    if candidate.suffix.lower() != ".json":
        raise ValueError("only_json_cloud_proposals_supported")
    return candidate


def _load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"cloud_proposal_json_error:{exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append("cloud_proposal_must_be_json_object")
        return {}
    return payload


def _sanitize_payload(payload: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    sanitized = redact_mapping(payload)
    redacted_fields: list[str] = []
    _collect_redacted_fields(payload, sanitized, "", redacted_fields)
    return sanitized, redacted_fields


def _collect_redacted_fields(before: Any, after: Any, path: str, fields: list[str]) -> None:
    if isinstance(before, dict) and isinstance(after, dict):
        for key, value in before.items():
            child = f"{path}.{key}" if path else str(key)
            _collect_redacted_fields(value, after.get(key), child, fields)
        return
    if isinstance(before, list) and isinstance(after, list):
        for index, value in enumerate(before):
            child = f"{path}[{index}]"
            _collect_redacted_fields(value, after[index] if index < len(after) else None, child, fields)
        return
    if before != after:
        fields.append(path or "<root>")


def _validate_string_list(payload: dict[str, Any], key: str, errors: list[str]) -> None:
    value = payload.get(key, [])
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        errors.append(f"cloud_proposal_{key}_must_be_string_list")


def _validate_files_to_read(workspace: Path, files: Any, errors: list[str], warnings: list[str]) -> None:
    if not isinstance(files, list):
        errors.append("cloud_proposal_files_to_read_must_be_list")
        return
    for index, item in enumerate(files):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"cloud_proposal_files_to_read_item_invalid:{index}")
            continue
        try:
            resolve_workspace_text_target(workspace, item)
        except ValueError as exc:
            errors.append(f"cloud_proposal_file_to_read_blocked:{index}:{exc}")
    if files:
        warnings.append("files_to_read_are_references_only_not_auto_read")


def _validate_changes(
    workspace: Path,
    changes: list[Any],
    errors: list[str],
    warnings: list[str],
    redacted_fields: list[str],
) -> None:
    seen: set[str] = set()
    for index, item in enumerate(changes):
        if not isinstance(item, dict):
            errors.append(f"cloud_proposal_change_must_be_object:{index}")
            continue
        operation = str(item.get("operation", "write_text"))
        if operation != "write_text":
            errors.append(f"unsupported_cloud_proposal_operation:{index}:{operation}")
        target = item.get("target")
        if not isinstance(target, str) or not target.strip():
            errors.append(f"cloud_proposal_target_required:{index}")
            continue
        if f"changes[{index}].target" in redacted_fields:
            errors.append(f"cloud_proposal_target_redacted:{index}")
        suffix = item.get("suffix")
        if suffix is not None and not isinstance(suffix, str):
            errors.append(f"cloud_proposal_suffix_must_be_string:{index}")
        try:
            resolved = resolve_workspace_text_target(workspace, target, suffix=suffix if isinstance(suffix, str) else None)
            rel = resolved.relative_to(workspace).as_posix()
            if rel in seen:
                errors.append(f"duplicate_cloud_proposal_target:{rel}")
            seen.add(rel)
        except ValueError as exc:
            errors.append(f"cloud_proposal_target_blocked:{index}:{exc}")
        content = item.get("content")
        if not isinstance(content, str):
            errors.append(f"cloud_proposal_content_required:{index}")
        elif len(content) > MAX_CONTENT_CHARS:
            errors.append(f"cloud_proposal_content_too_large:{index}")
        if f"changes[{index}].content" in redacted_fields:
            warnings.append(f"cloud_proposal_content_redacted:{index}")


def _validate_commands(commands: Any, *, field: str, errors: list[str]) -> None:
    if not isinstance(commands, list):
        errors.append(f"cloud_proposal_{field}_must_be_list")
        return
    for index, command in enumerate(commands):
        if not isinstance(command, str) or not command.strip():
            errors.append(f"cloud_proposal_{field}_item_invalid:{index}")
            continue
        if redact_text(command) != command:
            errors.append(f"cloud_proposal_{field}_redacted:{index}")
            continue
        if not _is_safe_executor_test_command(command):
            errors.append(f"cloud_proposal_{field}_not_allowlisted:{index}:{command}")


def _is_safe_executor_test_command(command: str) -> bool:
    if any(token in command for token in [";", "&&", "||", "|", ">", "<"]):
        return False
    try:
        args = shlex.split(command)
    except ValueError:
        return False
    if not args:
        return False
    normalized = list(args)
    executable = Path(normalized[0]).name.lower()
    if executable in {"python", "python.exe", "py", "py.exe"}:
        normalized[0] = sys.executable
    allowed_python = (
        len(normalized) >= 3
        and Path(normalized[0]).name.lower().startswith("python")
        and normalized[1:3] in (["-m", "pytest"], ["-m", "py_compile"])
    )
    return allowed_python or executable in {"pytest", "pytest.exe"}
