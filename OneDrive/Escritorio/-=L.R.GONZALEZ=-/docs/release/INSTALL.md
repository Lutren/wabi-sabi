# INSTALL

This workspace has multiple install paths. Do not run installs globally from the root.

## Audit Tools

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-"
python tools/release/audit_repo.py
```

## Claudio Python Runtime

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio"
python -m pip install -r requirements.txt
```

Only run this if `requirements.txt` is verified for the target runtime.

## Argus Desktop

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\apps\argus_desktop"
npm install
```

## MetaEvo TCG

Private only:

```powershell
cd "C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\metaevo-tcg"
npm install
```

Do not use this path for public release packaging.
