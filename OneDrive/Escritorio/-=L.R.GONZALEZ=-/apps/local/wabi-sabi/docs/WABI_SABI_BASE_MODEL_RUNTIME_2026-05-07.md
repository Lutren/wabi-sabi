# Wabi/Sabi Base Model Runtime - 2026-05-07

## Decision

Wabi/Sabi must use the installed base model as the primary deep provider when it is available.

Runtime resolution order:

1. `BASE_MODEL`
2. `WABI_BASE_MODEL`
3. `WABI_OLLAMA_BASE_MODEL`
4. default local base: `qwen2.5-coder:3b`

Endpoint resolution:

1. explicit constructor host
2. `MODEL_ENDPOINT` when `MODEL_PROVIDER` is `ollama`, `local` or `installed_base_model`
3. `OLLAMA_HOST`
4. `http://127.0.0.1:11434`

Provider fallback:

```text
ollama -> codex -> dry-run
```

Only if the base model is unavailable or disabled does Wabi/Sabi fall back without claiming model access.

## Safety Defaults

- Cloud models ending in `:cloud` or `-cloud` are filtered unless `WABI_ALLOW_CLOUD_MODELS=1`.
- No Ollama prewarm by default. Use `WABI_OLLAMA_PREWARM=1` only when intentional.
- Disable local base model route with `WABI_DISABLE_BASE_MODEL=1`.
- Fallback is reported in Ollama evidence as `fallback_used=true|false`.

## Verified Host State

Command:

```powershell
python -m wabi_sabi.cli.main auto /status --json
```

Result:

```text
auto_provider=ollama
provider_order=ollama,codex,dry-run
base_model=qwen2.5-coder:3b
endpoint=http://127.0.0.1:11434
local_models=qwen2.5-coder:3b,qwen2.5:0.5b
cloud_models_filtered=4
running_models=none
```

Smoke:

```powershell
$env:WABI_OLLAMA_KEEP_ALIVE='0'
$env:WABI_OLLAMA_NUM_CTX='256'
@'
from pathlib import Path
from wabi_sabi.core.ollama_bridge import OllamaBridge
bridge = OllamaBridge(runtime_root=Path('runtime'))
print(bridge.generate('Responde solamente: OK', timeout=150, num_predict=4).to_dict())
'@ | python -
```

Result:

```text
ok=True
provider=ollama
model=qwen2.5-coder:3b
output=OK
fallback_used=false
artifact=runtime\outputs\ollama_response_20260506-190108.md
```

Post-smoke:

```powershell
ollama ps
```

Result:

```text
no running models
```

## EML Boundary

EML is integrated as a research-only helper, not as the daily agent core.

CLI:

```powershell
python -m wabi_sabi.cli.main eml 0 0 --json
```

Result:

```text
domain_ok=True
value=1.0
epistemic_status=RESEARCH_ONLY
```

## Verification

```powershell
python -m pytest -q
```

Result:

```text
64 passed
```
