# ClaudioOS Blueprint v0.1

ClaudioOS v0.1 is not a new kernel and not a replacement for Linux.
It is a Debian Live remix blueprint with a cognitive observacionista layer:

- Linux kernel and Debian base
- systemd services
- Claudio Guardian on `127.0.0.1:4787`
- Mission Control dashboard on `127.0.0.1:4444`
- policy gates, provider registry, browser manifests and witness logs

The first objective is small and testable:

1. Build the ISO in Linux, WSL2 or a VM.
2. Boot it in QEMU.
3. Confirm Guardian health.
4. Confirm a dangerous action is blocked or asks approval.
5. Confirm the witness log records the decision.

Do not install this over Windows or production machines. Test in VM first.

## Brain OS Layer

Brain OS is the broader cognitive layer: small durable tools, observable
decisions, local-first execution and human approval for irreversible actions.
ClaudioOS v0.1 is the first Linux body for that layer.

Key blueprint additions:

- `docs/BRAIN_OS_PRINCIPLES.md`
- `docs/COMPATIBILITY_MATRIX.md`
- `docs/MODEL_EFFICIENCY.md`
- `contracts/module_manifest.schema.json`
- `examples/module_manifest_content_forge.json`
- `scripts/windows_harden_loopback.ps1`

## Quick Start

```bash
cd claudio_os_blueprint
bash scripts/00_install_build_deps.sh
bash scripts/01_build_iso.sh
bash scripts/02_test_iso_qemu.sh
```

The ISO will be created under:

```text
live-build/live-image-amd64.hybrid.iso
```

## Local Services

```text
Guardian:        http://127.0.0.1:4787
Mission Control: http://127.0.0.1:4444
CLI:             claudioctl
```

## Safety Defaults

- Paid APIs ask approval.
- Publishing asks approval.
- Voice cloning asks approval.
- Browser automation requires a manifest.
- Browser forbidden actions are blocked.
- High pressure/jamming holds execution.
- High uncertainty degrades execution.

## Host Loopback Check

On Windows, verify local services before exposing any agent workflow:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/windows_harden_loopback.ps1
```

Use `-Apply` to set the user `OLLAMA_HOST` to loopback. Use `-Apply -Machine`
only from an elevated PowerShell if a machine-level value is still `0.0.0.0`.

## Module Contract

Every module must declare its purpose, inputs, outputs, risk, cost, gates,
evidence, witness and recovery path. The first schema lives at:

```text
contracts/module_manifest.schema.json
```

## Claudio Bridge

The Windows/Claudio bridge exposes Brain OS through:

```text
python tools/brain_os_cli.py status
python tools/brain_os_cli.py master-plan
python tools/brain_os_cli.py decide '{"action":"publish","tags":["publish"],"evidence":true}'
python tools/brain_os_cli.py compile-dsl examples/observacionista_video.dsl --gate-payload
python tools/brain_os_cli.py validate-manifest examples/module_manifest_content_forge.json
python tools/brain_os_cli.py kernel-status
python tools/brain_os_cli.py kernel-observe '{"action":"publish","tags":["publish"],"evidence":true}'
python tools/brain_os_cli.py kernel-admit examples/module_manifest_content_forge.json
```

After the next normal Claudio API boot, the local routes are:

```text
GET  /api/brain-os/status
POST /api/brain-os/decide
POST /api/brain-os/dsl/compile
POST /api/brain-os/dsl/decide
POST /api/brain-os/module/validate
POST /api/brain-os/model-slimmer/plan
POST /api/brain-os/model-slimmer/assess
GET  /api/brain-os/kernel/status
POST /api/brain-os/kernel/observe
POST /api/brain-os/kernel/module/admit
POST /api/brain-os/kernel/module/failure
```
