# SECURITY

Status: draft.

## Scope

This workspace is not safe to publish as-is. Security review is required before every package.

## Required Checks

- Run `python tools/release/scan_secrets.py`.
- Verify `docs/control/CLAIMS_BOUNDARY.md` and `docs/private/PRIVATE_GAME_BOUNDARY.md`.
- Exclude `.env`, tokens, sessions, local state, vendors, build outputs, and private game paths.
- Review `claudio\tools\pentest_repos` separately. Do not ship it in public packages.

## Reporting

Record findings in:

- `docs/security/SECRET_SCAN_REPORT.md`
- `RISK_REGISTER.md`
- `docs/release/FIX_PLAN.md`
- `docs/security/SECURITY_CHECKLIST.md`

## Secret Handling

Do not paste or print secret values in reports. Report only path, type, and recommended action.
