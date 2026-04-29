# Brain OS Principles

Brain OS is the long-lived cognitive operating layer above the machine. ClaudioOS
v0.1 is the first practical body for that layer: Linux base, local services,
policy gates and witness logs.

The design target is closer to needle, hammer, spoon and rope than to a bloated
platform. A good tool has a clear shape, can be repaired, keeps working when a
piece fails and does not betray the person who uses it.

## Durable Rules

- Local first. A local file, local API or local model is preferred before paid
  or remote providers.
- Evidence before action. A module does not act only because it can; it acts
  when there is enough evidence to justify the action.
- Small contracts. Every module declares purpose, inputs, outputs, risk, cost,
  gates, witness path and recovery path.
- Human gate for irreversible work. Publishing, paid APIs, account changes,
  voice cloning, destructive writes and browser actions that affect external
  services require approval.
- Witness first. Every decision creates a JSONL record that can be read without
  the original program.
- Graceful degradation. When uncertainty, cost or pressure rises, the system
  switches to a cheaper and safer route instead of forcing the original plan.
- Replaceable organs. OpenClaw, Radiocinema, Content Forge, model providers and
  browser executors are replaceable modules, not the brain.

## Separation Of Roles

```text
Claudio / Darvi     decide and coordinate
Guardian / ObsClaw  gate and witness
OpenClaw            execute hands, channels and tools
Content Forge       render local media packages
Radiocinema         provide audiovisual style and assets
Provider Hub        route models and paid APIs through policy
```

## Module Minimum

Every module must expose a manifest with:

- `id`, `name`, `version`, `owner`
- `purpose`
- `inputs` and `outputs`
- `states`
- `risk`
- `cost`
- `gates`
- `evidence_required`
- `witness`
- `recovery`
- `interfaces`

If a module cannot explain those fields, it is not ready for autonomous use.

## First Win

The first durable win is not a perfect OS. The first win is:

```text
Guardian boots.
Dashboard opens.
Policy blocks danger.
Witness records evidence.
Recovery path is known.
```

