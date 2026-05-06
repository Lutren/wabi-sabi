# Asistente Negocio Lane Unification - 2026-05-06

Status: `COMMERCIAL / FOUNDER_ACCESS / PUBLICATION_BLOCK`

Asistente Negocio queda como una sola lane comercial en
`apps\commercial\asistente-negocio`. La fuente historica de Claudio se conserva
solo como referencia de origen; no debe competir con esta ruta activa.

## Funcion Fundamental

Asistente local para negocios pequenos: perfil del negocio, borradores de
respuesta, aprobacion humana y handoff manual por email/WhatsApp. No envia
mensajes automaticamente, no promete ventas, no opera cuentas externas y no
expone tecnologia privada de Claudio/Wabi-Sabi.

## Canon Activo

- App: `apps\commercial\asistente-negocio`.
- Ficha: `docs\product\asistente-negocio.md`.
- Evidencia release: `docs\product\asistente-negocio-release-evidence-2026-05-02.md`.
- Evidencia Windows: `docs\product\asistente-negocio-windows-installer-evidence-2026-05-02.md`.
- Notas cliente: `apps\commercial\asistente-negocio\CUSTOMER_INSTALL_NOTES.md`.
- Draft soporte/privacidad/reembolso:
  `apps\commercial\asistente-negocio\SUPPORT_PRIVACY_REFUND_DRAFT.md`.

## Validacion 2026-05-06

Comandos ejecutados:

```txt
npm ci
npm run check
npm audit --omit=dev --audit-level=high
npm run pack:win
npm run smoke:e2e-render
npm run preview
python tools\release\scan_secrets.py --path apps\commercial\asistente-negocio --json --fail-on-findings
```

Resultados:

- `npm ci`: `0 vulnerabilities`.
- `npm run check`: `public_safe check passed`.
- `npm run pack:win`: genero build local `release\win-unpacked`.
- `npm run smoke:e2e-render`: paso y produjo evidencia local en `qa_artifacts`.
- `npm run preview`: genero preview HTML local.
- Secret scan focalizado: `count_reported=0`.

## Decision

- `KEEP`: fuente de app, scripts, iconos de packaging, notas cliente y docs de soporte.
- `GENERATED`: `release/`, `preview/` y `qa_artifacts/` quedan fuera de Git.
- `REVIEW`: clean-machine QA, firma/aviso unsigned y revision legal final.
- `BLOCK`: Gumroad checkout, website buy-now y publicacion externa.

## Siguiente Cierre

Congelar artefacto final despues de clean-machine QA. Solo entonces se puede
pasar de founder access controlado a venta limitada.
