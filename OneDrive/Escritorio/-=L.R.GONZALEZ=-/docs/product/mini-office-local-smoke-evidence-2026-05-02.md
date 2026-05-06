# Mini Office Local Smoke Evidence - 2026-05-02

Status: `LOCAL_SMOKE_QA / COPY_CLAIMS_BLOCK / DO_NOT_PUBLISH`

Mini Office has a working local static server and passing tests after a runtime
fix. It is not ready for Gumroad, GitHub or website publication because public
copy still contains corrupted text, contradictory MIT/commercial positioning and
strong autonomy/24-7 claims.

## Fixes

- `mini_office.py` now uses `http.server.SimpleHTTPRequestHandler`.
- Added `--status`, `--port` and `--no-browser` runtime flags.
- Server binds to `127.0.0.1` and supports `MINI_OFFICE_NO_BROWSER=1` for QA.
- `package.json` now runs real tests with `python -m pytest -q`.
- `package.json` has `smoke` and lower-claim commercial metadata.
- `pyproject.toml` description/keyword no longer says autonomous agents.

## Validation

```txt
npm test
22 passed in 0.15s

python -m py_compile mini_office.py
ok

npm run smoke
index_exists=true

server smoke
HTTP 200, doctype=true, has_mini_office=true
```

Server smoke evidence:

- Path: `apps\commercial\mini-office\reports\qa_2026-05-02\server-smoke.json`
- Port: `8765`
- Status code: `200`
- Content length: `15580`

## Packaging

- Manifest: `release_manifests\mini-office.json`
- ZIP: `releases\paid-apps\mini-office.zip`
- ZIP bytes: `81978`
- ZIP SHA256: `6780FCDBF6BDB0BA49DE9A6B790FFDC98C393DC926C8CEDAD9326FC3F741715A`
- ZIP members: `53`
- ZIP artifact secret scan: `count_reported=0`
- Product secret scan: `count_reported=0`
- ZIP excludes `__pycache__` and `.pytest_cache`.

## Blockers

- README, landing pages and publish docs contain corrupted words such as `muy`,
  `[elichicado]` and broken file names.
- Public copy still claims autonomous/24-7 operation beyond verified local static
  app behavior.
- MIT/open-source copy conflicts with commercial app positioning.
- Gumroad URL in local HTML/docs is not verified as a live product.
- Install scripts still need cleanup before customer delivery.

## Decision

Keep Mini Office as `LOCAL_SMOKE_QA` only. Do not publish or sell until copy,
claims, license posture and install scripts are cleaned and re-tested.
