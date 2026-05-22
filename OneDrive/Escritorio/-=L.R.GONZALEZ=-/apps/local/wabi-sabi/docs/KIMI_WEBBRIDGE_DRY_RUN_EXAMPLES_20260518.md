# Kimi WebBridge Dry-Run Examples 2026-05-18

Estos ejemplos son locales y no llaman Kimi cuando faltan flags de doble opt-in.

## Selector Public Prompt

```powershell
.\wabi.cmd browser-bridge select --payload-class PUBLIC_PROMPT --json
```

Resultado esperado:

- `selected_backend` permanece `dry-run` salvo adapter/gates explicitos.
- `safe_to_send=false` cuando no existe doble opt-in.
- `publication_gate=BLOCK`.

## Council Prepare-Only

```powershell
.\wabi.cmd browser-bridge council --json
```

Resultado esperado:

- Servicios rankeados localmente.
- `live_attempts=0`.
- `online_ai_called=false`.
- Servicios sin adapter probado quedan `PREPARE_ONLY`.

## Kimi Smoke Sin Flags

```powershell
.\wabi.cmd browser-bridge smoke --service kimi --json
```

Resultado esperado:

- `status=KIMI_SEND_FLAGS_MISSING`.
- `online_ai_called=false`.
- `browser_backend_called=false`.
- No se imprime `WABI_KIMI_WEBBRIDGE_URL`.
- No se envia workspace, rutas privadas ni codigo interno.

## Regla De Este Run

`KimiSendGate=BLOCK_THIS_RUN_NO_LIVE_CALL`: ningun ejemplo de este documento debe ejecutarse con `--send` durante el run de setup guide v0.1.
