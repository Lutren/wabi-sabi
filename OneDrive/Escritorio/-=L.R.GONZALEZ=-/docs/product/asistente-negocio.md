# Asistente Negocio MEDIOEVO

Classification: `COMMERCIAL`

Current path: `apps\commercial\asistente-negocio`

Legacy/source-of-history path: `-=MEDIOEVO=-\-=LIBROS\claudio\products\asistente_negocio`

Status 2026-05-06: `FOUNDER_ACCESS_RENDER_QA_PASS / CLEAN_MACHINE_QA_PENDING / PUBLICACION_BLOCK`

Detected scripts:

- `npm run dev`
- `npm run check`
- `npm run smoke:e2e-render`
- `npm run preview`
- `npm run package:final`
- `npm run build:win`
- `npm run build:mac`
- `npm run pack:win`
- `npm run pack:mac`

Closed locally:

- `npm ci` passed with `0 vulnerabilities`.
- `npm run check` passed: `public_safe check passed`.
- `npm run pack:win` generated local `release\win-unpacked`.
- `npm run smoke:e2e-render` passed against the Electron build.
- `npm run preview` generated a standalone HTML preview.
- Focused secret scan on `apps\commercial\asistente-negocio` reported `0` findings.

Canon:

- Product source: `apps\commercial\asistente-negocio`.
- Lane evidence: `docs\product\asistente-negocio-lane-unification-2026-05-06.md`.
- Release evidence: `docs\product\asistente-negocio-release-evidence-2026-05-02.md`.
- Windows evidence: `docs\product\asistente-negocio-windows-installer-evidence-2026-05-02.md`.

Before release:

- clean Windows VM install smoke;
- code-signing certificate or explicit unsigned-installer warning;
- final support/privacy/refund/terms legal review;
- final artifact hash freeze;
- no Gumroad/website checkout until ActionGate passes.
