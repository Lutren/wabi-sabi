"""Pattern for SWE-agent or mini-SWE-agent patch/test loops."""
from obs_safe_integration_kit import EvidenceStore, EstadoPSI, SWEAgentObserver

store = EvidenceStore("swe_obs.sqlite")
psi = EstadoPSI(topic="fix issue #123")
obs = SWEAgentObserver(store, psi)

# Before running any command, gate it.
for command in ["pytest -q", "git diff --stat", "rm -rf /tmp/myproject"]:
    decision = obs.gate_command(command, intent="run safe local validation for issue fix")
    print(command, decision.to_dict())
    # Execute only if decision.status == GateStatus.ALLOW after human policy.

# Store test output as evidence.
obs.observe_step(
    issue="fix issue #123",
    tool="test",
    step_text="pytest result: 12 passed, 0 failed",
    raw={"repo": "local-sandbox", "command": "pytest -q"},
)
print(store.latest_status())
