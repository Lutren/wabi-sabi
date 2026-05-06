# External Provider Manual Gates - 2026-05-06

## Decision

The historical inventory
`-=MEDIOEVO=-\-=LIBROS\claudio\docs\root_notes_review\INVENTARIO_MAESTRO_2026-04-20.md`
listed external credentials and dashboard access as open checkboxes.

Those are not Codex-executable tasks. They are manual owner/security gates.

## Manual Gates

| item | required owner action | agent boundary |
|---|---|---|
| Twitter Consumer Key/Secret | owner creates or rotates credentials in provider UI | do not request, store or paste secrets |
| Reddit Password/2FA/OAuth | owner completes manual provider setup | do not bypass 2FA or store password |
| Supabase schema/dashboard | owner confirms project/dashboard access | no dashboard mutation without target gate |
| Real benchmark with 100 sessions | host must be ready and dataset approved | no heavy run while host gate is REVIEW/BLOCK |

## Tracker Action

Those four historical open checkboxes were converted to `manual-gate` markers.
This does not mean credentials, dashboards or benchmarks are complete. It means
they are no longer active local execution tasks.

## Boundary

No credential was read, requested, created, copied, rotated or stored. No
dashboard was opened or changed. No benchmark was executed.
