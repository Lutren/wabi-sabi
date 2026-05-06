# RELEASE_READINESS_MATRIX

| check | status | notes |
|---|---|---|
| Build | PARTIAL | Argus Vite build passed; dry-run build orchestrator created; more product builds pending |
| Tests | PARTIAL | Claudio pytest passed 603 tests; dry-run test orchestrator created; more products pending |
| Typecheck | PARTIAL | Argus typecheck passed; private TCG intentionally not run |
| Lint | PARTIAL | TCG has lint but is private; public lint coverage incomplete |
| Secrets | BLOCKED | secret candidates found |
| Dependency audit | PARTIAL | `npm audit --omit=dev --audit-level=high` passed for Argus and Asistente Negocio |
| Broken imports | NOT_RUN | pending |
| Dead code | PARTIAL | duplicate/dead-code report created |
| Docs | IMPROVING | root docs, product map, release docs and business docs created |
| License | BLOCKED | global license requires review |
| Changelog | CREATED | root draft |
| Install docs | CREATED | root draft |
| Privacy policy | DRAFT | legal review required |
| Terms | DRAFT | legal review required |
| Support channel | DRAFT | support plan created |
| Release versioning | PARTIAL | product versions exist, no central policy |
| Screenshots | UNKNOWN | pending per product |
| Landing copy | DRAFT | created |
| Gumroad assets | PARTIAL | product drafts exist; fees verified against official Gumroad pricing page |
| Buy Me a Coffee tiers | DRAFT | created |

## Free-dev Batch 2026-05-01

| check | status | notes |
|---|---|---|
| Local ZIP artifacts | PASS | 5 ZIPs generated under `releases/free-dev` |
| Product manifests | PASS | manifests regenerated under `release_manifests` |
| Source secret scan | PASS | allowlisted products returned `count_reported=0` |
| ZIP secret scan | PASS | `scan_secrets.py --artifact` inspected internal ZIP members and returned `count_reported=0` |
| Install/extraction smoke | PASS | `verify_free_dev_release.py --write --json` returned `ok=true` |
| External publication | BLOCKED | requires ActionGate, target review and public URL verification |
