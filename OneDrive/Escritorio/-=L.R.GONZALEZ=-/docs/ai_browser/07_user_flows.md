# AI Browser Seguro - 07 User Flows

Status: `LOCAL_FLOW_SPEC`

## Flow 1 - Local HTML Evidence

1. User provides local HTML.
2. Browser CLI reads bytes.
3. JS is not executed.
4. Forms/downloads/scripts are detected and blocked.
5. Readable text is extracted.
6. Hidden DOM is separated.
7. Web instructions are flagged.
8. SourceSnapshot and WitnessLog event are created.
9. Evidence bundle is exported.

Outcome: `APPROVE` or `REVIEW` for read-only evidence only.

## Flow 2 - Remote URL Requested

1. User provides `https://...`.
2. Browser checks ActionGate.
3. If no gate or gate not `APPROVE`, stop with `BLOCK`.
4. If gate approves, MVP creates `NETWORK_STUB_NOT_FETCHED`.
5. No network request is made.
6. Snapshot records `INCOGNITA` for remote content.

Outcome: no remote evidence yet; follow-up requires a gated fetch engine.

## Flow 3 - Prompt Injection Found

1. Extractor finds instruction-like text.
2. Text goes into `web_instructions`.
3. Hidden instruction text goes into `hidden_dom_instructions`.
4. The agent receives it as evidence of risk, not as instruction.
5. GhostGate blocks memory/canon persistence until reviewed.

Outcome: `REVIEW`.

## Flow 4 - Download Link Found

1. Extractor detects download attribute or risky file extension.
2. No file is downloaded.
3. Risk flag `download_link_present_quarantined` is added.
4. Future download proposal must pass domain policy, ActionGate and quarantine.

Outcome: read-only snapshot can continue; download remains blocked.

## Flow 5 - Future Gated Browser Action

1. Agent proposes click/type/upload/download/login.
2. Proposal includes source snapshot hash, domain policy and intent.
3. ActionGate evaluates exact action.
4. If approved, WitnessLog records before and after.
5. If not approved, action remains queued.

Outcome: no autonomous action without gate.
