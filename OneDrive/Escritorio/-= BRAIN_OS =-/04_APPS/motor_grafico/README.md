# motor_grafico

Motor grafico local para contratos DUAT/VibeForge/OSIT.

## Smoke Local

```powershell
python smoke_motor_grafico.py
```

El smoke verifica que `VibeForge` pueda crear un mundo y materializar una
escena sin escribir archivos, llamar providers, construir bundles o publicar
artefactos.

## Tests TS (vitest)

```powershell
npm test          # corre ositCanon.test.ts (contratos del shim OSIT) -> 6 passed
```

Host mínimo: `package.json` + `vitest.config.ts` (scopeado al shim; los archivos con imports
`@/lib/...` del app React NO se recolectan). `node_modules/` es un **junction** al de
`02_CLAUDIO/core/pattern_jump` (reuso offline del vitest ya instalado). Para hacerlo autónomo:
`npm install` aquí. Verificado 2026-06-02: 6/6 passed, vitest v1.6.1.

## Gates

- PublicationGate: `BLOCK`
- BuildGate: `REVIEW_REQUIRED`
- ReleaseGate: `BLOCK`
- RuntimeRunGate: `REVIEW_LOCAL_RUN`

## Frontend (UI de la forja) — 2026-06-03

`index.html` + `vibeforge_ui.css` + `vibeforge_ui.js`: UI art-dirigida (identidad DUAT brass/cyan) que
**reimplementa la forja en JS** (espejo de `vibeforge_engine.py`: WorldSeed con hash verificable, biomas
desert/forest/coast/mountain/cavern/void, SketchScene texto→entidades con bioma + estado epistémico) y
**renderiza con el MOTOR compartido** (`engine_web/mv-boot.js` → `MV.createEngine`), con respaldo local si el
motor no está. Muestra MUNDO, ESCENA y la **consola de gates OSIT** (Publication/Build/Release/RuntimeRun).
Abrir `index.html` (offline). Verificado en navegador: motor 16 módulos, forja + escena + gates OK, 0 errores.
