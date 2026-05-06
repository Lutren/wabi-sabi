"""Pattern for GPT Researcher integration.

Do not paste this into production blindly. Use it as an adapter pattern:
- conduct_research() output -> ObservationEnvelope
- report claims -> ClaimRegistry
- no unsupported claim leaves without evidence id
"""
from obs_safe_integration_kit import EvidenceStore, EstadoPSI, GPTResearcherObserver

async def run_with_observacionismo(query: str):
    # from gpt_researcher import GPTResearcher
    # researcher = GPTResearcher(query=query)
    # results = await researcher.conduct_research()
    # report = await researcher.write_report()

    # Mock result shape. Replace with GPT Researcher actual outputs.
    results = [
        {"source": "gpt_researcher", "url": "https://example.org", "title": "Example", "content": "Evidence text..."}
    ]
    report = "Claim one supported by example.org. Claim two needs verification."

    store = EvidenceStore("gpt_researcher_obs.sqlite")
    psi = EstadoPSI(topic=query)
    obs = GPTResearcherObserver(store, psi)

    observation_ids = [obs.observe_source(r) for r in results]
    claim_ids = []
    for oid in observation_ids:
        claim_ids.extend(obs.register_report_claims(oid, report))

    return {"observations": observation_ids, "claims": claim_ids, "psi": psi.to_dict(), "store": store.latest_status()}
