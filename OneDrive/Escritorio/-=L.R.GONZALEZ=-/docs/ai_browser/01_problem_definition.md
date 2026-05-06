# AI Browser Seguro - 01 Problem Definition

Status: `LOCAL_SPEC`

## Problem

Current agent/browser patterns tend to collapse three different things into one
stream:

1. Web content as evidence.
2. Web-origin instructions as untrusted data.
3. Agent/operator instructions as authority.

That collapse creates prompt injection, bad evidence, accidental external
actions and contaminated memory. The AI browser must reduce those risks before
it offers convenience.

## Goal

Build a controlled evidence browser for AI work:

- verifiable reading;
- controlled extraction;
- hard separation between web content and instructions;
- SourceSnapshot with hashes;
- EvidenceGraph;
- WitnessLog;
- ActionGate before any action;
- quarantine for downloads;
- domain permissions;
- read-only mode;
- no credentials by default.

## Non-Goal

This is not a general autonomous web agent. It must not become a browser that
logs in, clicks, downloads, scrapes or posts without a target-specific gate.

## Success Criteria

- A source can be captured as a stable `SourceSnapshot`.
- The raw input, extracted readable text and hidden DOM text have hashes.
- Web-origin instructions are stored as untrusted findings, not executed.
- The snapshot is classified into `CERTEZA`, `INFERENCIA` and `INCOGNITA`.
- A WitnessLog event records the capture and hash.
- Any form/login/download/action is blocked by default.
- Remote URL fetching is blocked or stubbed unless ActionGate permits it.

## Required Output Shape

The browser produces evidence, not just a summary:

```text
Source input
  -> controlled capture
  -> readable text extraction
  -> web instruction separation
  -> SourceSnapshot
  -> EvidenceGraph
  -> WitnessLog
  -> ActionGate state
  -> evidence bundle
```

## Operating Constraint

If the input requires network, login, payment, download, upload, captcha,
private account access or external publication, the system stops at `REVIEW` or
`BLOCK` until the exact target passes gate.
