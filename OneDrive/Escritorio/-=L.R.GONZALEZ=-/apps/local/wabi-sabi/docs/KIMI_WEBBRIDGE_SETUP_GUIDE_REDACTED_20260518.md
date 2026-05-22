# Kimi WebBridge Setup Guide Redacted 2026-05-18

## Estado Actual

- BrowserBridge v0.2 mantiene `dry-run` como backend por defecto.
- Kimi no fue llamado en este run.
- Estado actual esperado: `KIMI_SEND_FLAGS_MISSING`.
- No hay URL Kimi WebBridge configurada en el entorno de esta sesion.
- Council permanece en modo prepare-only/ranking local salvo adapter probado y doble opt-in futuro.
- Las respuestas externas con codigo quedan como `wabi.cloud_code_proposal.v0_1` proposal-only; nunca se aplican automaticamente.

## Requisitos Para Un Smoke Futuro

Un smoke vivo de Kimi solo puede considerarse en otro run si existen todas estas condiciones:

- `WABI_ALLOW_BROWSER_SEND=1`.
- `WABI_ALLOW_BROWSER_BRIDGE=1`.
- `WABI_KIMI_WEBBRIDGE_URL` configurada solo en entorno local.
- Comando explicito con `--send`.
- Payload publico y sintetico.
- Cero workspace privado.
- Cero rutas privadas.
- Cero codigo interno.
- Cero credenciales impresas o guardadas.

## Payload Permitido

El unico payload permitido para el primer smoke publico sintetico es:

```text
Return exactly this JSON:
{"ok":true,"service":"kimi","bridge":"smoke"}
```

La respuesta solo se acepta como `KIMI_SMOKE_PASS` si parsea JSON y coincide exactamente con:

```json
{"ok": true, "service": "kimi", "bridge": "smoke"}
```

## Que No Hacer

- No pegar tokens, cookies, claves, sesiones ni credenciales en chat.
- No commitear `.env` ni archivos con valores de entorno.
- No publicar la URL privada de WebBridge.
- No enviar workspace privado.
- No enviar archivos internos.
- No enviar rutas locales completas.
- No enviar codigo interno.
- No usar Kimi para aplicar patches.
- No ejecutar codigo devuelto por Kimi.
- No usar Kimi con Fragmentos, canon completo, libros, RPG/TCG, datasets, raw prompts ni material protegido.

## Estados Esperados

- `KIMI_SMOKE_PASS`: JSON esperado recibido en smoke futuro con doble opt-in completo.
- `KIMI_SEND_FLAGS_MISSING`: faltan flags de envio o puente; no se llama Kimi.
- `KIMI_BRIDGE_URL_MISSING`: flags presentes, URL ausente; no se llama Kimi.
- `KIMI_AUTH_REQUIRED_REDACTED`: Kimi requiere login, 2FA, pago o upgrade; no registrar valores sensibles.
- `KIMI_TIMEOUT_REVIEW`: timeout o latencia requiere revision; no reintentar sin gate.
- `KIMI_SMOKE_FAIL_REDACTED`: respuesta invalida o fallo redactado; no elevar a PASS.

## Checklist Manual Segura

1. Configurar `WABI_KIMI_WEBBRIDGE_URL` solo en el entorno local de la sesion.
2. No imprimir el valor de `WABI_KIMI_WEBBRIDGE_URL`.
3. Confirmar que `WABI_ALLOW_BROWSER_BRIDGE=1` y `WABI_ALLOW_BROWSER_SEND=1` estan activos solo para el smoke.
4. Ejecutar una sola vez el smoke con `--send` y payload publico sintetico.
5. Revisar que la respuesta sea JSON exacto.
6. Guardar un reporte redactado sin URL real, sin rutas privadas y sin valores sensibles.
7. Dejar `live_attempts=1` solo si hubo evidencia real del smoke; nunca marcar PASS por inferencia.

## Comando De Referencia Redactado

```powershell
$env:WABI_ALLOW_BROWSER_BRIDGE = "1"
$env:WABI_ALLOW_BROWSER_SEND = "1"
$env:WABI_KIMI_WEBBRIDGE_URL = "<local-kimi-webbridge-url-redacted>"
.\wabi.cmd browser-bridge smoke --service kimi --send --json
```

Este run no ejecuta ese comando. La guia solo deja el procedimiento redactado y los gates de revision.
