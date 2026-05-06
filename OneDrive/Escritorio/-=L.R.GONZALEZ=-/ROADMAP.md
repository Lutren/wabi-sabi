# ROADMAP

## P0: Stop Unsafe Publication

- Keep private game excluded.
- Keep secrets excluded.
- Avoid broad ZIPs or whole-workspace publication.
- Do not push dirty repos until reviewed.

## P1: Structure And Boundaries

- Create canonical tree plan.
- Create migration map.
- Create `docs/private/PRIVATE_GAME_BOUNDARY.md`.
- Create open/commercial/editorial release lanes.
- Create product manifests.

## P2: Product Readiness

- Prepare `observacionismo-gate` as first open developer package.
- Prepare `claudio_os_blueprint` as a developer blueprint, not a finished OS.
- Prepare `asistente_negocio`, `flujocrm`, `mini_office`, and `argus_desktop` as commercial candidates.
- Separate website source of truth.

## P3: Automation

- Dry-run audit scripts.
- Secret scan.
- Duplicate and large-file reports.
- Release notes generation.
- Allowlist packaging.

## P4: Publication

- Gumroad product manifests.
- Buy Me a Coffee tiers.
- Website landing copy.
- Customer support, refund, privacy, terms drafts.
- Human legal review.

## P5: Cleanup

- Archive only with `MIGRATION_MAP.md` and `docs/control/ROOT_CLEANUP_MANIFEST_2026-05-06.json` when root files are moved.
- Remove or move caches/builds only after dry-run approval.
- Split public source from private/commercial source.
