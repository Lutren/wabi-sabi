# GitHub Release Checklist

## Before Push

- README exists.
- LICENSE exists.
- CLAIMS or limits section exists.
- PRIVATE_EXCLUSIONS or boundary section exists.
- SECURITY notes exist.
- Secret scan is clean.
- Path scrub is clean.
- Claims scan is clean.
- Staging repo is clean.

## Push

- Create/select exact repo.
- Push `main`.
- Verify public URL.
- Record commit and URL.

## Do Not Include

- Workspace roots.
- Downloads/E: raw sources.
- Private books, game, TCG, lore, assets or runtime.
- Vendors, pentest repos, caches or generated local builds.
