from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

from wabi_sabi.core.gate import ActionGate
from wabi_sabi.core.memory import LocalMemory
from wabi_sabi.core.redaction import redact_mapping, redact_text
from wabi_sabi.core.tools import stamp, write_artifact


DEFAULT_CODEX_MODEL = "gpt-5.5"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


@dataclass
class CodexBridgeResult:
    ok: bool
    provider: str
    gate: str
    action: str
    output: str
    artifacts: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    command: list[str] = field(default_factory=list)
    error: str = ""
    status: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return redact_mapping(asdict(self))


def find_codex_command() -> str | None:
    for candidate in ["codex.cmd", "codex.exe", "codex"]:
        path = shutil.which(candidate)
        if path:
            return path
    return None


def codex_status(
    *,
    codex_finder: Callable[[], str | None] = find_codex_command,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    values = env or os.environ
    codex_path = codex_finder()
    openai_key_present = bool(values.get("OPENAI_API_KEY"))
    openai_model = values.get("WABI_OPENAI_MODEL") or DEFAULT_CODEX_MODEL
    if codex_path:
        auto_provider = "codex-cli"
    elif openai_key_present:
        auto_provider = "openai-responses"
    else:
        auto_provider = "dry-run"
    return {
        "codex_cli": {
            "available": bool(codex_path),
            "path": codex_path,
            "mode": "read_only_codex_exec",
        },
        "openai_responses": {
            "available": openai_key_present,
            "env_key": "OPENAI_API_KEY",
            "model": openai_model,
        },
        "auto_provider": auto_provider,
        "safe_default": "read_only_or_dry_run",
    }


class CodexCliAdapter:
    name = "codex-cli"

    def __init__(
        self,
        *,
        codex_command: str,
        workspace: Path,
        runtime_root: Path,
        runner: Callable[..., subprocess.CompletedProcess[Any]] | None = None,
    ) -> None:
        self.codex_command = codex_command
        self.workspace = workspace
        self.runtime_root = runtime_root
        self.runner = runner

    def execute(self, prompt: str, *, timeout: int) -> CodexBridgeResult:
        output_dir = self.runtime_root / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)
        last_message = output_dir / f"codex_last_message_{stamp()}.md"
        prepared_prompt = build_codex_prompt(prompt)
        command = [
            self.codex_command,
            "--ask-for-approval",
            "never",
            "exec",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
            "--ephemeral",
            "--cd",
            str(self.workspace),
            "--output-last-message",
            str(last_message),
            "--color",
            "never",
            "-",
        ]
        try:
            input_bytes = prepared_prompt.encode("utf-8")
            if self.runner is None:
                proc = run_process_with_timeout(command, cwd=self.workspace, input_bytes=input_bytes, timeout=timeout)
            else:
                proc = self.runner(
                    command,
                    cwd=str(self.workspace),
                    input=input_bytes,
                    text=False,
                    capture_output=True,
                    timeout=timeout,
                )
        except subprocess.TimeoutExpired as exc:
            return CodexBridgeResult(
                ok=False,
                provider=self.name,
                gate="REVIEW",
                action="codex_cli_timeout",
                output="Codex CLI no respondio dentro del timeout configurado.",
                command=command,
                error=str(exc),
            )

        text = ""
        artifacts: list[str] = []
        if last_message.exists():
            text = last_message.read_text(encoding="utf-8", errors="replace").strip()
            artifacts.append(str(last_message))
        if not text:
            text = (_decode_process_output(proc.stdout) or _decode_process_output(proc.stderr)).strip()
        return CodexBridgeResult(
            ok=proc.returncode == 0,
            provider=self.name,
            gate="APPROVE",
            action="codex_cli_read_only_response",
            output=text or "Codex CLI termino sin mensaje final.",
            artifacts=artifacts,
            evidence=[
                "codex_exec_sandbox=read-only",
                "approval_policy=never",
                "codex_session=ephemeral",
                f"returncode={proc.returncode}",
            ],
            command=command,
            error="" if proc.returncode == 0 else text[-2000:],
        )


class OpenAIResponsesAdapter:
    name = "openai-responses"

    def __init__(
        self,
        *,
        runtime_root: Path,
        env: dict[str, str] | None = None,
        http_post: Callable[[str, dict[str, str], dict[str, Any], int], dict[str, Any]] | None = None,
    ) -> None:
        self.runtime_root = runtime_root
        self.env = env or os.environ
        self.http_post = http_post or _post_json

    def execute(self, prompt: str, *, timeout: int) -> CodexBridgeResult:
        api_key = self.env.get("OPENAI_API_KEY")
        if not api_key:
            return CodexBridgeResult(
                ok=False,
                provider=self.name,
                gate="REVIEW",
                action="openai_api_key_missing",
                output="OPENAI_API_KEY no esta configurada; usa codex-cli o --dry-run.",
                error="missing_OPENAI_API_KEY",
            )
        model = self.env.get("WABI_OPENAI_MODEL") or DEFAULT_CODEX_MODEL
        body = {
            "model": model,
            "reasoning": {"effort": self.env.get("WABI_OPENAI_REASONING_EFFORT", "low")},
            "instructions": (
                "Eres Codex accesible desde Wabi-Sabi. Responde en espanol claro. "
                "No pidas secretos. No afirmes que aplicaste cambios locales si solo respondiste por API."
            ),
            "input": prompt,
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        try:
            response = self.http_post(OPENAI_RESPONSES_URL, headers, body, timeout)
        except Exception as exc:  # pragma: no cover - exact network failures vary by host
            return CodexBridgeResult(
                ok=False,
                provider=self.name,
                gate="REVIEW",
                action="openai_responses_error",
                output="La llamada a OpenAI Responses API fallo.",
                error=redact_text(str(exc), env=self.env),
            )
        output_text = extract_response_text(response)
        artifact = write_artifact(
            self.runtime_root / "outputs",
            "openai_responses_text",
            ".md",
            redact_text(output_text, env=self.env) + "\n",
        )
        return CodexBridgeResult(
            ok=bool(output_text),
            provider=self.name,
            gate="APPROVE",
            action="openai_responses_text",
            output=output_text or "La respuesta no incluyo texto extraible.",
            artifacts=[str(artifact)],
            evidence=[f"model={model}", "endpoint=/v1/responses", f"artifact_written={artifact}"],
        )


class WabiCodexBridge:
    def __init__(
        self,
        *,
        workspace: str | Path,
        runtime_root: str | Path,
        codex_finder: Callable[[], str | None] = find_codex_command,
        runner: Callable[..., subprocess.CompletedProcess[Any]] | None = None,
        env: dict[str, str] | None = None,
    ) -> None:
        self.workspace = Path(workspace).resolve()
        self.runtime_root = Path(runtime_root).resolve()
        self.runtime_root.mkdir(parents=True, exist_ok=True)
        self.codex_finder = codex_finder
        self.runner = runner
        self.env = env or os.environ
        self.memory = LocalMemory(self.runtime_root)

    def status(self) -> dict[str, Any]:
        return codex_status(codex_finder=self.codex_finder, env=self.env)

    def ask(
        self,
        prompt: str,
        *,
        provider: str = "auto",
        dry_run: bool = False,
        timeout: int = 180,
    ) -> CodexBridgeResult:
        gate = ActionGate().evaluate_text(prompt)
        status = self.status()
        if gate.gate == "BLOCK":
            result = CodexBridgeResult(
                ok=False,
                provider=provider,
                gate=gate.gate,
                action="blocked_by_action_gate",
                output="La consulta fue bloqueada por ActionGate local.",
                evidence=gate.reasons,
                error=";".join(gate.reasons),
                status=status,
            )
            self._log(prompt, result)
            return result

        resolved_provider = status["auto_provider"] if provider == "auto" else provider
        if dry_run or resolved_provider == "dry-run":
            result = self._dry_run(prompt, provider=resolved_provider, gate=gate.gate, status=status)
            self._log(prompt, result)
            return result

        if resolved_provider == "codex-cli":
            codex_command = status["codex_cli"]["path"]
            if not codex_command:
                result = self._dry_run(prompt, provider=resolved_provider, gate=gate.gate, status=status)
                result.ok = False
                result.action = "codex_cli_missing"
                result.error = "codex_cli_not_found"
                self._log(prompt, result)
                return result
            adapter = CodexCliAdapter(
                codex_command=codex_command,
                workspace=self.workspace,
                runtime_root=self.runtime_root,
                runner=self.runner,
            )
            result = adapter.execute(prompt, timeout=timeout)
        elif resolved_provider == "openai-responses":
            adapter = OpenAIResponsesAdapter(runtime_root=self.runtime_root, env=self.env)
            result = adapter.execute(prompt, timeout=timeout)
        else:
            result = CodexBridgeResult(
                ok=False,
                provider=resolved_provider,
                gate=gate.gate,
                action="unknown_codex_provider",
                output=f"Proveedor no reconocido: {resolved_provider}",
                error="unknown_provider",
            )
        result.gate = gate.gate
        result.status = status
        self._log(prompt, result)
        return result

    def _dry_run(
        self,
        prompt: str,
        *,
        provider: str,
        gate: str,
        status: dict[str, Any],
    ) -> CodexBridgeResult:
        workpack = {
            "schema": "wabi_codex_workpack.v1",
            "provider": provider,
            "gate": gate,
            "workspace": str(self.workspace),
            "prompt": redact_text(prompt, env=self.env),
            "codex_prompt": redact_text(build_codex_prompt(prompt), env=self.env),
            "status": redact_mapping(status, env=self.env),
        }
        artifact = write_artifact(
            self.runtime_root / "outputs",
            "wabi_codex_workpack",
            ".json",
            json.dumps(workpack, indent=2, ensure_ascii=False),
        )
        return CodexBridgeResult(
            ok=True,
            provider=provider,
            gate=gate,
            action="codex_bridge_dry_run",
            output="Workpack Codex generado sin llamar a modelos ni ejecutar subprocess.",
            artifacts=[str(artifact)],
            evidence=[f"artifact_written={artifact}", "runtime_call=none"],
            status=status,
        )

    def _log(self, prompt: str, result: CodexBridgeResult) -> None:
        self.memory.append_event(
            {
                "channel": "wabi_codex_bridge",
                "prompt": redact_text(prompt, env=self.env),
                "provider": result.provider,
                "gate": result.gate,
                "ok": result.ok,
                "action": result.action,
                "artifacts": result.artifacts,
            }
        )


def build_codex_prompt(prompt: str) -> str:
    return (
        "Origen: Wabi-Sabi local.\n"
        "Modo: solo lectura por defecto.\n"
        "Reglas:\n"
        "- Responde en espanol claro y operativo.\n"
        "- No hagas push, deploy, publicaciones, compras, borrados ni cambios destructivos.\n"
        "- No pidas ni expongas secretos, tokens o .env.\n"
        "- Si el usuario pide escribir archivos, entrega plan o parche sugerido y marca que aplicar requiere ActionGate.\n\n"
        f"Pedido del operador:\n{prompt}\n"
    )


def extract_response_text(response: dict[str, Any]) -> str:
    if isinstance(response.get("output_text"), str):
        return response["output_text"].strip()
    chunks: list[str] = []
    for item in response.get("output", []) or []:
        for content in item.get("content", []) or []:
            text = content.get("text")
            if isinstance(text, str):
                chunks.append(text)
    return "\n".join(chunk.strip() for chunk in chunks if chunk.strip()).strip()


def _decode_process_output(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def run_process_with_timeout(
    command: list[str],
    *,
    cwd: Path,
    input_bytes: bytes,
    timeout: int,
) -> subprocess.CompletedProcess[bytes]:
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    proc = subprocess.Popen(
        command,
        cwd=str(cwd),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,
        creationflags=creationflags,
    )
    try:
        stdout, stderr = proc.communicate(input=input_bytes, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        _kill_process_tree(proc.pid)
        try:
            stdout, stderr = proc.communicate(timeout=3)
        except Exception:
            stdout = exc.output or b""
            stderr = exc.stderr or b""
        raise subprocess.TimeoutExpired(command, timeout, output=stdout, stderr=stderr) from exc
    return subprocess.CompletedProcess(command, proc.returncode, stdout, stderr)


def _kill_process_tree(pid: int) -> None:
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return
    try:
        os.kill(pid, 9)
    except OSError:
        return


def _post_json(url: str, headers: dict[str, str], body: dict[str, Any], timeout: int) -> dict[str, Any]:
    data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[-2000:]
        raise RuntimeError(f"openai_http_{exc.code}: {detail}") from exc
