"""Pattern for browser-use integration.

Use snapshots first. Browser actions stay gated and dry-run until explicitly approved.
"""
from obs_safe_integration_kit import EvidenceStore, EstadoPSI, BrowserUseObserver

store = EvidenceStore("browser_obs.sqlite")
psi = EstadoPSI(topic="browser-use safe wrapper")
obs = BrowserUseObserver(store, psi)

snapshot_id = obs.observe_snapshot(
    url="http://localhost:3000",
    state_text="clickable[1]: Login\nclickable[2]: Docs\ninput[3]: Search",
    raw={"title": "Local app"},
)
print("snapshot:", snapshot_id)

for tool, args in [("click", {"index": 2}), ("upload_file", {"path": "./secret.txt"}), ("evaluate", {"js": "localStorage.clear()"})]:
    decision = obs.gate_action(tool, args, intent="navegar documentación local sin efectos externos")
    print(tool, decision.to_dict())
