# CHANGELOG

## 2026-05-01

- Redacted literal credential values from the active Claudio pending tracker while keeping rotation/review tasks open.
- Generated allowlist product manifests with SHA256 hashes under `release_manifests/`.
- Added the missing Argus Desktop README and verified all 9 product manifests include README coverage.
- Closed the web source-of-truth decision: `claudio/website` is canonical for `medioevo-site`; `claudio/apps/editorial_web` is legacy/experimental.
- Ran non-private product tests and smoke checks: Claudio `834 passed`, open-dev packages passed, Mini Office passed, Argus dry-run install passed, Asistente Negocio and FlujoCRM checks passed, Hormiguero smoke passed.
- Generated draft release notes without publishing.

## 2026-04-29

- Created Phase 0 audit reports for repo cleanup and release readiness.
- Created root agent instructions and release governance docs.
- Marked global release state as not ready.
- Established private game boundary and layer separation as release gates.

## Unreleased

- Root structure migration pending.
- Secret scan still reports findings; public release remains blocked.
- Legal review pending for all public/commercial licenses and policies.
- Generated archive contents still need review before any upload because no ZIP/archive was created in this pass.
