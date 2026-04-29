# ClaudioOS Architecture

```text
Linux
  -> systemd
  -> Claudio Guardian
  -> Policy YAML + Provider Registry
  -> Mission Control HTML
  -> OpenClaw executors
  -> Content Forge / Radiocinema / MedioevoTools
  -> Claudio / Darvi decision layer
```

ClaudioOS asks more than standard UNIX permissions:

- Is there a policy?
- Is there evidence?
- Is there a browser manifest?
- Is there cost?
- Is there human approval?
- Is the system near jamming?
- Is the action irreversible?
- Can the action be witnessed and rolled back?

OpenClaw is treated as hands and channels. Claudio and Guardian decide.

## Module Contract

Every executable module must ship a manifest that can be checked before it is
called. The manifest is intentionally simple:

```text
purpose -> inputs -> outputs -> risk -> cost -> gates -> witness -> recovery
```

This keeps Content Forge, Radiocinema, provider adapters, browser actions and
future PC2 services replaceable. If one module fails or is attacked, the rest
of the system can hold, degrade or block instead of inheriting the failure.

The canonical schema is:

```text
contracts/module_manifest.schema.json
```

## Claudio Bridge Surface

On the current Windows host, Claudio consumes the same Brain OS contract through
`core/brain_os_bridge.py`. It does not replace the Linux blueprint. It lets
agents ask for local decisions, DSL compilation, module validation and model
efficiency plans before the ISO exists.

```text
Claudio agent/tool
  -> BrainOSBridge
  -> BrainOSKernel
  -> observacionismo_gate.py
  -> observacionismo_dsl.py
  -> model_slimmer_evidence.py
  -> witness JSONL
```

`BrainOSKernel` is not a Linux kernel. It is the small cognitive kernel that
persists the loop:

```text
observe -> decide -> contain -> witness -> recover
```

It records kernel events in SQLite, admits modules by manifest, and uses module
containment so an attacked or failed module can be blocked or quarantined
without pulling down the rest of Claudio.
