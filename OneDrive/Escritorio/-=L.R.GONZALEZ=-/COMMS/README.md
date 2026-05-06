# SETO COMMS

`COMMS` is the local file protocol for agent coordination.

Canonical streams:

- `inbox/<agent>.jsonl`: messages addressed to one agent;
- `outbox/<agent>.jsonl`: replies and proposed actions emitted by that agent;
- `agents_state/<agent>.json`: current lane ownership, gates and handoff refs;
- `topics/<topic>.jsonl`: shared topic events;
- `handoffs/*.md`: human-readable contracts and transfer notes.

Rules:

- messages are append-only or superseded by a new envelope;
- every action proposal cites an `ObservationEnvelope`;
- `REVIEW` leaves files untouched and emits a handoff;
- `BLOCK` prevents publication, external action, private-boundary access and
  strong claims;
- no agent overwrites another agent's lane without a handoff.

Current schemas:

- `schemas\observation-envelope.schema.json`
- `schemas\action-gate.schema.json`
- `schemas\witness-log-event.schema.json`

Claudio/Hormiguero bridge:

- Claudio reads this folder through `claudio/core/agent_comms.py`;
- Mission Control exposes the local read-only view at `/api/local/comms/state`;
- missing evidence, missing envelopes or uncertain ownership remain `REVIEW`;
- secrets, external publication, private-boundary access and strong claims remain
  `BLOCK`.
