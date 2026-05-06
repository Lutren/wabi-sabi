# BUILD

Build commands are product-specific. Do not build or package the whole workspace.

## Candidate Commands

### Claudio tests

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio"
python -m pytest tests/ -x --quiet
```

### Argus desktop

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\argus_desktop"
npm run typecheck
npm run build
```

### Asistente Negocio

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\products\asistente_negocio"
npm run check
```

### Private game

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\metaevo-tcg"
npm run lint
npm run build
```

Private game builds are not public releases.
