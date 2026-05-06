# Content Forge

Status: `COMMERCIAL_OR_INTERNAL_REVIEW`

Canonical source candidate: `PRODUCTOS_MEDIOEVO/content_forge`

Content Forge is a local-first MEDIOEVO rendering tool for short videos,
carousels, captions, previews and QA packages. It must not post externally by
itself. Runtime renders stay local-only under the ignored runtime folder.

## What Enters Canon

- Source code under `content_forge/content_forge/`.
- Public placeholder assets under `assets/public_placeholders/`.
- README and local CLI contract.

## What Stays Out

- Rendered videos.
- Previews, thumbnails and job logs.
- Any personal/artist/private assets.
- Publication queues unless converted to public-safe product evidence.

## Validation

- `python -m py_compile PRODUCTOS_MEDIOEVO\content_forge\content_forge\cli.py PRODUCTOS_MEDIOEVO\content_forge\content_forge\core\engine.py`
- `python tools\release\scan_secrets.py --path PRODUCTOS_MEDIOEVO\content_forge --json`

## Decision

Keep as a product source candidate. It should later move to a cleaner canonical
lane such as `apps/commercial/content-forge` with a migration manifest. Until
then, only source and public-safe placeholders are allowed in Git.
