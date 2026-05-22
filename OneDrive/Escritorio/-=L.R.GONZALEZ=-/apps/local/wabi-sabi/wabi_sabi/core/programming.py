from __future__ import annotations

import py_compile
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

from wabi_sabi.core.patch_planner import build_file_patch_plan, resolve_workspace_text_target, sha256_text
from wabi_sabi.core.safe_executor import SafeExecutor


@dataclass(frozen=True)
class PatchResult:
    target: Path
    backup: Path | None
    diff: Path
    plan: Path | None
    rollback: Path | None
    execution: Path | None
    before_hash: str
    after_hash: str
    changed: bool
    verification: str


def resolve_python_target(workspace: Path, target: str | Path) -> Path:
    return resolve_workspace_text_target(workspace, target, suffix=".py")


def apply_python_patch(
    *,
    workspace: Path,
    runtime_root: Path,
    target: str | Path,
    code: str,
) -> PatchResult:
    target_path = resolve_python_target(workspace, target)
    old_text = target_path.read_text(encoding="utf-8") if target_path.exists() else ""
    before_hash = sha256_text(old_text)
    new_text = build_new_python_text(old_text, code)
    after_hash = sha256_text(new_text)

    compile(new_text, str(target_path), "exec")

    plan = build_file_patch_plan(
        workspace=workspace,
        target=target,
        content=new_text,
        summary="scoped_python_code_patch",
        suffix=".py",
    )
    execution = SafeExecutor(workspace=workspace, runtime_root=runtime_root).execute(plan)
    if not execution.ok:
        raise ValueError(execution.error or execution.verification)
    if target_path.exists():
        py_compile.compile(str(target_path), doraise=True)

    return PatchResult(
        target=target_path,
        backup=execution.rollback_path,
        diff=execution.diff_path,
        plan=execution.plan_path,
        rollback=execution.rollback_path,
        execution=execution.execution_path,
        before_hash=before_hash,
        after_hash=after_hash,
        changed=execution.changed,
        verification=execution.verification,
    )


def build_new_python_text(old_text: str, code: str) -> str:
    normalized_code = code.strip() + "\n"
    if normalized_code.strip() in old_text:
        return old_text
    if not old_text.strip():
        return normalized_code
    header = "\n\n# --- Wabi Sabi generated patch ---\n"
    return old_text.rstrip() + header + normalized_code


def code_for_prompt(prompt: str) -> tuple[str, str, list[str]]:
    lowered = prompt.lower()
    if "normalize_title" in lowered:
        return (
            normalize_title_function(),
            "Genere una funcion Python local normalize_title(text) para normalizar titulos.",
            ["El usuario pidio un helper pequeno y reversible en sandbox."],
        )
    if "archivo" in lowered and ("linea" in lowered or "lineas" in lowered or "línea" in lowered):
        return (
            file_summary_function(),
            "Genere una funcion Python local para leer un archivo y resumir sus lineas.",
            ["El usuario probablemente queria un helper reutilizable para archivos de texto."],
        )
    return (
        generic_module_template(prompt),
        "Genere un borrador de codigo local.",
        ["El pedido necesita revision humana o integracion dirigida para tocar codigo existente."],
    )


def file_summary_function() -> str:
    return dedent(
        '''
        from __future__ import annotations

        from pathlib import Path


        def summarize_file_lines(path: str | Path, preview_lines: int = 5) -> dict:
            """Read a text file and return a compact line summary."""
            file_path = Path(path)
            text = file_path.read_text(encoding="utf-8", errors="replace")
            lines = text.splitlines()
            return {
                "path": str(file_path),
                "line_count": len(lines),
                "empty_lines": sum(1 for line in lines if not line.strip()),
                "first_lines": lines[:preview_lines],
                "last_lines": lines[-preview_lines:] if preview_lines else [],
            }
        '''
    ).lstrip()


def normalize_title_function() -> str:
    return dedent(
        '''
        from __future__ import annotations


        def normalize_title(text: str) -> str:
            """Collapse extra whitespace and return title case text."""
            return " ".join(str(text).split()).title()
        '''
    ).lstrip()


def generic_module_template(prompt: str) -> str:
    escaped = prompt.replace('"""', '\\"\\"\\"')
    return dedent(
        f'''
        """Generated Wabi Sabi code draft.

        Original request:
        {escaped}
        """


        def run() -> str:
            return "TODO: complete this local implementation after selecting a target file."


        if __name__ == "__main__":
            print(run())
        '''
    ).lstrip()
