# AI Browser Seguro - 03 Architecture

Status: `RECOMMENDED_ARCHITECTURE`

## Compact Architecture

```text
USUARIO / REALIDAD
  -> WABI-SABI control node
  -> ActionGate / GhostGate
  -> AI Browser Capture Layer
  -> SourceSnapshot
  -> EvidenceGraph
  -> WitnessLog
  -> COMMS / agent consumers
  -> final evidence-backed output
```

## Core Components

| Component | Responsibility |
|---|---|
| Capture Controller | Opens only allowed source modes: local HTML, file URL, or gated remote stub in MVP. |
| Readability Extractor | Extracts visible text without executing JS. |
| Instruction Separator | Stores web-origin instructions separately from readable content. |
| SourceSnapshot | Records raw hash, readable-text hash, hidden-DOM hash, source mode and security state. |
| EvidenceGraph | Links source, snapshot, extraction and instruction channel. |
| ActionGate | Blocks or reviews network, login, download, click, upload, publish and shell actions. |
| GhostGate | Proposed memory-contamination gate before durable memory/COMMS/canon persistence. |
| WitnessLog | Append-only local hash-chain event for capture/action decisions. |
| Domain Policy Store | Future allowlist/denylist/quota/permissions per domain. |
| Quarantine Store | Future destination for downloads after explicit approval. |

## Data Flow

1. User asks for a source read.
2. Wabi-Sabi estimates R, regime and Phi_eff.
3. ActionGate evaluates source mode.
4. Capture Controller reads local HTML or returns gated remote stub.
5. Extractor separates visible text, hidden DOM and web instructions.
6. SourceSnapshot hashes all relevant channels.
7. EvidenceGraph links snapshot artifacts.
8. WitnessLog records event hash and previous hash.
9. Agent consumers receive only normalized evidence, not raw authority.

## Security Modes

| Mode | Network | JS | Cookies | Credentials | Actions |
|---|---:|---:|---:|---:|---:|
| `read_only_local` | no | no | no | no | no |
| `remote_stub` | no | no | no | no | no |
| `gated_fetch_future` | gate | no by default | ephemeral | none by default | no |
| `gated_action_future` | gate | restricted | ephemeral | manual auth only | gate + witness |

## Browser Content Authority Rule

Web content never becomes system, developer or user instruction. It can become:

- `web_content`: readable evidence;
- `web_instruction`: untrusted instruction found in the source;
- `hidden_dom_text`: separated risk channel;
- `claim_candidate`: statement requiring source evidence;
- `blocked_action`: proposed action that needs gate.

## Wabi-Sabi Placement

Wabi-Sabi is the sensory-cognitive control node, not the whole brain and not an
AGI. In this architecture it:

- receives source request, project state, environment signals and gates;
- estimates R, regime and Phi_eff;
- deconstructs the request using DO;
- recompiles the task using IOI;
- selects modules from Matrix/Biblioteca only when needed;
- delegates to specialist agents;
- checks evidence, gates, residual R and user objective;
- compiles the final output.

It does not publish, delete, browse autonomously, log in or modify external
state without ActionGate.
