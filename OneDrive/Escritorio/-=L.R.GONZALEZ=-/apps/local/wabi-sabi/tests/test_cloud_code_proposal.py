import json
import os
import subprocess
import sys
from pathlib import Path

from wabi_sabi.core.cloud_code_proposal import (
    build_cloud_code_proposal_prompt,
    build_dry_run_cloud_code_proposal,
    cloud_proposal_to_task_spec,
    extract_cloud_code_proposal_payload,
    validate_cloud_code_proposal,
    write_cloud_proposal_artifact,
    write_cloud_task_spec_artifact,
)
from wabi_sabi.core.task_spec_planner import build_patch_plan_from_task_spec


APP_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args, workspace: Path, runtime: Path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(APP_ROOT)
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "wabi_sabi.cli.main",
            *args,
            "--workspace",
            str(workspace),
            "--runtime",
            str(runtime),
        ],
        cwd=str(APP_ROOT),
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
    )


def write_proposal(path: Path, **overrides) -> Path:
    payload = {
        "schema": "wabi.cloud_code_proposal.v0_1",
        "summary": "create helper from cloud proposal",
        "intent": "offline cloud proposal contract test",
        "assumptions": ["cloud only proposes"],
        "files_to_read": ["README.md"],
        "changes": [
            {
                "operation": "write_text",
                "target": "helpers.py",
                "suffix": ".py",
                "content": "def answer() -> int:\n    return 42\n",
            },
            {
                "operation": "write_text",
                "target": "test_helpers.py",
                "suffix": ".py",
                "content": "from helpers import answer\n\n\ndef test_answer():\n    assert answer() == 42\n",
            },
        ],
        "commands_requested": ["python -m py_compile helpers.py test_helpers.py"],
        "test_commands": ["python -m py_compile helpers.py test_helpers.py"],
        "risks": ["proposal is not execution authority"],
        "rollback_notes": ["SafeExecutor owns rollback"],
        "debug_strategy": ["send sanitized stderr only"],
        "gate_recommendation": "APPROVE",
    }
    payload.update(overrides)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def test_cloud_proposal_validates_and_converts_to_task_spec(tmp_path):
    (tmp_path / "README.md").write_text("# tmp\n", encoding="utf-8")
    proposal = write_proposal(tmp_path / "proposal.json")

    validation = validate_cloud_code_proposal(workspace=tmp_path, proposal_path=proposal)
    task_spec = cloud_proposal_to_task_spec(validation)

    assert validation.ok is True
    assert task_spec["schema"] == "wabi.task_spec.v1"
    assert [change["target"] for change in task_spec["changes"]] == ["helpers.py", "test_helpers.py"]
    assert task_spec["metadata"]["cloud_gate_recommendation"] == "APPROVE"
    assert task_spec["metadata"]["cloud_authority"] == "proposal_only"


def test_cloud_task_spec_artifact_from_runtime_outputs_can_build_patch_plan(tmp_path):
    (tmp_path / "README.md").write_text("# tmp\n", encoding="utf-8")
    proposal = write_proposal(tmp_path / "proposal.json")
    validation = validate_cloud_code_proposal(workspace=tmp_path, proposal_path=proposal)
    task_spec = cloud_proposal_to_task_spec(validation)

    artifact = write_cloud_task_spec_artifact(tmp_path / "runtime" / "outputs", task_spec)
    spec, plan = build_patch_plan_from_task_spec(workspace=tmp_path, spec_path=artifact)

    assert spec.summary == "create helper from cloud proposal"
    assert [operation.relative_path for operation in plan.operations] == ["helpers.py", "test_helpers.py"]
    assert not (tmp_path / "helpers.py").exists()


def test_cloud_proposal_redacts_secret_like_content(tmp_path):
    (tmp_path / "README.md").write_text("# tmp\n", encoding="utf-8")
    proposal = write_proposal(
        tmp_path / "proposal.json",
        changes=[
            {
                "operation": "write_text",
                "target": "helpers.py",
                "suffix": ".py",
                "content": "TOKEN = 'nvapi-this-should-be-redacted-1234567890'\n",
            }
        ],
    )

    validation = validate_cloud_code_proposal(workspace=tmp_path, proposal_path=proposal)
    task_spec = cloud_proposal_to_task_spec(validation)

    assert validation.ok is True
    assert "changes[0].content" in validation.redacted_fields
    assert "nvapi-this-should" not in json.dumps(task_spec)
    assert "[REDACTED:" in task_spec["changes"][0]["content"]


def test_cloud_proposal_rejects_sensitive_target_and_unsafe_commands(tmp_path):
    proposal = write_proposal(
        tmp_path / "proposal.json",
        files_to_read=[".env"],
        changes=[
            {
                "operation": "write_text",
                "target": ".env/helpers.py",
                "suffix": ".py",
                "content": "x = 1\n",
            }
        ],
        commands_requested=["python -m py_compile helpers.py && del secret.txt"],
        test_commands=["npm run test"],
    )

    validation = validate_cloud_code_proposal(workspace=tmp_path, proposal_path=proposal)

    assert validation.ok is False
    joined = ";".join(validation.errors)
    assert "cloud_proposal_file_to_read_blocked" in joined
    assert "cloud_proposal_target_blocked" in joined
    assert "cloud_proposal_commands_requested_not_allowlisted" in joined
    assert "cloud_proposal_test_commands_not_allowlisted" in joined


def test_cloud_proposal_validate_cli_does_not_touch_sources(tmp_path):
    (tmp_path / "README.md").write_text("# tmp\n", encoding="utf-8")
    proposal = write_proposal(tmp_path / "proposal.json")

    proc = run_cli("cloud-proposal-validate", str(proposal), "--json", workspace=tmp_path, runtime=tmp_path / "runtime")

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert payload["cloud_provider_called"] is False
    assert not (tmp_path / "helpers.py").exists()


def test_cloud_proposal_task_spec_and_plan_cli_do_not_touch_sources(tmp_path):
    (tmp_path / "README.md").write_text("# tmp\n", encoding="utf-8")
    proposal = write_proposal(tmp_path / "proposal.json")

    spec_proc = run_cli(
        "cloud-proposal-task-spec",
        str(proposal),
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
    )
    assert spec_proc.returncode == 0, spec_proc.stderr
    spec_payload = json.loads(spec_proc.stdout)
    assert Path(spec_payload["task_spec_artifact"]).exists()
    assert not (tmp_path / "helpers.py").exists()

    plan_proc = run_cli(
        "cloud-proposal-plan",
        str(proposal),
        "--json",
        workspace=tmp_path,
        runtime=tmp_path / "runtime",
    )
    assert plan_proc.returncode == 0, plan_proc.stderr
    plan_payload = json.loads(plan_proc.stdout)
    assert plan_payload["operations"] == ["helpers.py", "test_helpers.py"]
    assert Path(plan_payload["plan_artifact"]).exists()
    assert Path(plan_payload["diff_artifact"]).exists()
    assert not (tmp_path / "helpers.py").exists()


def test_provider_prompt_redacts_secret_like_intent():
    prompt = build_cloud_code_proposal_prompt(
        intent="usa nvapi-this-should-be-redacted-1234567890 para programar",
        workspace_summary={"files_sampled": 1},
    )

    assert "nvapi-this-should" not in prompt
    assert "[REDACTED:" in prompt
    assert "wabi.cloud_code_proposal.v0_1" in prompt


def test_extract_cloud_proposal_payload_from_fenced_json():
    provider_text = (
        "plan listo\n```json\n"
        + json.dumps(build_dry_run_cloud_code_proposal(intent="crear helper"))
        + "\n```"
    )

    payload = extract_cloud_code_proposal_payload(provider_text)

    assert payload["schema"] == "wabi.cloud_code_proposal.v0_1"
    assert payload["changes"][0]["target"] == "examples/wabi_cloud_proposal_generated.py"


def test_write_provider_proposal_artifact_validates(tmp_path):
    runtime_root = tmp_path.parent / f"{tmp_path.name}_runtime"
    proposal = build_dry_run_cloud_code_proposal(intent="crear helper")
    artifact = write_cloud_proposal_artifact(runtime_root / "outputs", proposal, source="nvidia-nim")

    validation = validate_cloud_code_proposal(workspace=tmp_path, proposal_path=artifact, input_roots=[runtime_root])

    assert validation.ok is True
    assert "runtime" in str(artifact)


def test_cloud_proposal_from_provider_dry_run_cli_generates_valid_proposal(tmp_path):
    runtime_root = tmp_path.parent / f"{tmp_path.name}_runtime"
    proc = run_cli(
        "cloud-proposal-from-provider",
        "crear helper seguro",
        "--dry-run",
        "--json",
        workspace=tmp_path,
        runtime=runtime_root,
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert payload["provider"] == "dry-run"
    assert payload["cloud_provider_called"] is False
    assert Path(payload["proposal_artifact"]).exists()
    assert not (tmp_path / "examples" / "wabi_cloud_proposal_generated.py").exists()


def test_cloud_proposal_from_provider_plan_dry_run_cli_does_not_touch_sources(tmp_path):
    runtime_root = tmp_path.parent / f"{tmp_path.name}_runtime"
    proc = run_cli(
        "cloud-proposal-from-provider-plan",
        "crear helper seguro",
        "--dry-run",
        "--json",
        workspace=tmp_path,
        runtime=runtime_root,
    )

    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert payload["operations"] == [
        "examples/wabi_cloud_proposal_generated.py",
        "examples/test_wabi_cloud_proposal_generated.py",
    ]
    assert Path(payload["task_spec_artifact"]).exists()
    assert Path(payload["plan_artifact"]).exists()
    assert not (tmp_path / "examples" / "wabi_cloud_proposal_generated.py").exists()
