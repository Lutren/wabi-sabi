# QA Results

Date: 2026-05-02

Scope: local source package, ZIP artifact and local staging repo. No external publication, push, deploy, browser action or account action was performed.

## Commands

| check | command | result |
|---|---|---|
| tests | `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider` | `4 passed in 0.11s` |
| compile | `python -c "import pathlib, py_compile, tempfile; ..."` | `py_compile ok` |
| CLI smoke | `python -c "from obs_safe_integration_kit ... main(['--help'])"` | import OK, gate returned `HUMAN_REVIEW`, CLI help rendered |
| package secret scan | `python tools\release\scan_secrets.py --path packages\open-dev\obs-safe-integration-kit --json` | `count_reported=0` |
| package path scrub | focused local/private path denylist over `packages\open-dev\obs-safe-integration-kit` | no matches |
| JSON ficha | `python -m json.tool docs\product\agent_product_fichas_2026-05-02.json` | `json ok` |
| cache check | search for `.pytest_cache` and `__pycache__` under package | no matches |
| manifest | `python tools\release\product_manifest.py --product obs-safe-integration-kit --hash --write` | 20 files, 0 blocked, 0 excluded |
| ZIP | `python tools\release\package_free_dev.py --product obs-safe-integration-kit --execute` | `releases\free-dev\obs-safe-integration-kit.zip` written; exact hash is recorded in external release evidence |
| ZIP smoke | `python tools\release\verify_free_dev_release.py --product obs-safe-integration-kit --write` | 20 expected members, 20 actual members, `ok=true` |
| ZIP secret scan | `python tools\release\scan_secrets.py --artifact releases\free-dev\obs-safe-integration-kit.zip --json --fail-on-findings` | `count_reported=0` |
| local staging | `python tools\release\stage_free_dev_repos.py --product obs-safe-integration-kit --write --json` | clean repo, no remote; exact head is recorded in external staging evidence |
| staging secret scan | `python tools\release\scan_secrets.py --path publish_staging\open-dev\obs-safe-integration-kit --json --fail-on-findings` | `count_reported=0` |

## Claim Scan Note

Claim keywords appear only in negative boundary language:

- `README.md` says the kit does not prove new physics.
- `CLAIMS.md` blocks guaranteed safety, autonomous public execution, consciousness, cosmology, medical diagnosis and cognitive diagnosis claims.
- `RELEASE_CHECKLIST.md` requires the same claim review before external release.

This is acceptable for local source and ZIP promotion. External publication remains blocked until a destination-specific ActionGate passes.
