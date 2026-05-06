# SMOKE_TESTS

Draft smoke commands:

```powershell
python tools/release/audit_repo.py
python tools/release/scan_secrets.py
python tools/release/find_large_files.py --limit 20
python tools/release/find_duplicates.py --limit 20
python tools/release/product_manifest.py
```

Product smoke tests pending:

- Claudio runtime pytest: passed, 603 tests.
- Argus typecheck/build/audit: passed after lockfile repair.
- Asistente Negocio public-safe check/audit: passed.
- FlujoCRM package check.
- Mini Office import/launch check.
- Private MetaEvo TCG lint/build in private lane only.
