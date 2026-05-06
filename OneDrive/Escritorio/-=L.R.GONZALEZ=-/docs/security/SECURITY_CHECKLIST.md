# SECURITY_CHECKLIST

- [x] Run `python tools/release/scan_secrets.py` - 2026-05-01: `reported findings: 200`.
- [x] Check `.env` and token files are excluded from allowlist package manifests - denylist active; scan still finds live local secret files, so public release remains blocked.
- [x] Check private game paths are excluded from allowlist package manifests - dry-run packages reported `blocked=0` and no private package was included.
- [x] Check vendors are excluded from allowlist package manifests - denylist excludes vendors/caches/builds.
- [x] Check pentest repos are excluded from allowlist package manifests - denylist excludes `tools/pentest_repos`.
- [x] Check package manifest paths - 9 manifests generated under `release_manifests/`.
- [x] Check generated archive contents before upload - N/A local 2026-05-05: no `.zip/.7z/.rar/.tar/.gz` files found under `release_manifests/`, `publish_staging/` or `packages/`; no archive was generated or uploaded.
- [x] Record hashes - `python tools/release/product_manifest.py --hash --write` generated per-file SHA256 values.
- [ ] Rotate exposed secrets if any are found in public artifacts - secret rotation remains manual/outside tracker; no public artifact was generated.
