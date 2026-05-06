"""Demo: local-only, no network, no external side effects."""
from obs_safe_integration_kit import (
    EvidenceStore,
    EstadoPSI,
    ObservationEnvelope,
    GPTResearcherObserver,
    SWEAgentObserver,
    BrowserUseObserver,
    AegisBridge,
)

store = EvidenceStore("demo_obs.sqlite")
psi = EstadoPSI(topic="demo observacionista seguro")

# 1) Store a source as an ObservationEnvelope.
obs = ObservationEnvelope(
    source="manual",
    mode="manual",
    title="Nota de diseño",
    text="ActionGate debe bloquear acciones destructivas y registrar evidencia antes de actuar.",
    evidence=["local-note"],
).finalize()
psi.absorb_observation(obs)
oid = store.add_observation(obs)
store.add_claim(oid, "ActionGate debe ejecutarse antes de herramientas con efectos externos.", 0.75, evidence_ref=oid)

# 2) Gate a dangerous shell command. It must BLOCK.
swe = SWEAgentObserver(store, psi)
decision = swe.gate_command("rm -rf ~/.ssh", intent="limpiar archivos temporales del proyecto")
print("dangerous decision:", decision.to_dict())

# 3) Gate a benign test command. It remains DRY_RUN by default.
decision2 = swe.gate_command("pytest -q", intent="ejecutar pruebas locales del proyecto")
print("test decision:", decision2.to_dict())

# 4) Browser action: snapshot allowed as observation, click escalated.
browser = BrowserUseObserver(store, psi)
browser.observe_snapshot("http://localhost:3000", "button: Save\nlink: Docs")
print("browser click:", browser.gate_action("click", {"index": 1}, "abrir documentación local" ).to_dict())

# 5) AEGIS bridge: add PSI to a firewall result.
bridge = AegisBridge(store, psi)
print("aegis bridge:", bridge.precheck("shell", {"command": "pytest -q"}, "probar localmente", {"decision": "allow"}))

store.save_session(psi)
print("status:", store.latest_status())
