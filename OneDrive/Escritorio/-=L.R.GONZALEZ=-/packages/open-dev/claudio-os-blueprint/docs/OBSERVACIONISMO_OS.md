# Observacionismo OS

Core loop:

```text
observe -> classify -> decide -> act -> witness -> verify -> recover
```

States:

- `observando`
- `planificando`
- `ejecutando`
- `esperando`
- `atascado`
- `requiere_aprobacion`
- `listo`
- `fallido`

Rules:

- If evidence is missing, hold.
- If system pressure crosses `J_c`, hold.
- If browser automation has no manifest, block.
- If an action is irreversible, ask.
- If an external paid API is requested, ask.
- If uncertainty is high, degrade.
- If all gates pass, allow with witness.

## DSL v0.1

The first cognitive programming layer is a line-oriented DSL that compiles into
JSON. It is meant to improve human/process comprehension without hiding the
machine-readable contract.

Example:

```text
intent crear_video_medioevo_local
evidence asset_catalog runtime/content_forge/asset_catalog.json
state observando
action local_render tags=render,local
approval publish
witness runtime/content_forge/jobs/demo/witness.jsonl
recovery on_failure conservar_job_logs_y_comando
```

Compiler:

```text
../observacionismo_dsl.py
```

The compiled JSON can become:

- JSON Schema for validation.
- Rego or ObsClaw policy input.
- Python execution payload.
- SQLite or JSONL memory.
- Guardian `/decide` payload.

## Always-Alert Boot Audit

Brain OS treats boot as an observable contract, not a hope. The required
components for v0.1 are:

- scheduled watchdog
- Claudio API
- Brain OS kernel
- Conway agents
- daemon 24/7
- PSI daemon

Commands:

```text
python tools/brain_os_cli.py kernel-boot-contract
python tools/brain_os_cli.py kernel-boot-audit
```

The audit writes a `boot_audit` witness to the kernel SQLite ledger. It returns
`allow/listo` only when every required component is alive; otherwise it returns
`hold/esperando` with recovery instructions. Restart probes should stay light
(`/api/status`), then the full boot audit runs after the system stabilizes.
