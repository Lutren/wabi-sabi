# One Universe Vaults Ledger - 2026-05-06

Purpose: make the main workspace navigable without pretending that every raw tree
is canon. A folder can remain on disk as source evidence, but it is not part of
the active universe until Curador absorbs it into a lane with ficha, decision and
evidence.

## Rule

One universe means one operational truth:

- Canon lives in `docs/`, `apps/`, `packages/`, `research/`, `runtime/`, `COMMS/`,
  `tests/`, `release_manifests/` and root control files.
- Raw vaults live on disk, but do not compete with the main route.
- Generated QA, screenshots, builds, sessions, local memories, vendor imports and
  publication staging are not primary source.
- Private game, TCG, accounts and external-action payloads stay blocked.

## Vault Decisions

| path | decision | reason | next action |
|---|---|---|---|
| `-=MEDIOEVO=-/` | SOURCE_VAULT_REVIEW | original broad MEDIOEVO tree, too large and mixed for direct canon | extract by system into `docs/canon`, `docs/product`, `apps`, `packages`, `research` |
| `.claw/` | LOCAL_AGENT_HISTORY | session residue from local/third-party agents | keep local; only promote distilled lessons to COMMS or docs |
| `qa_artifacts/` | LOCAL_EVIDENCE_VAULT | screenshots, dry-runs, generated manifests and live-account evidence | keep local; commit only summarized evidence and release manifests |
| `publish_staging/` | GENERATED_PUBLICATION_STAGING | exported copies for GitHub/Gumroad/site workflows | rebuild from canonical packages; do not treat as source |
| `releases/` | GENERATED_RELEASE_OUTPUT | zips/installers/packages | keep hashes and manifests; do not commit binaries by default |
| `_archive/` | ARCHIVO_FRIO | cold archive or prior generated material | preserve until ficha confirms delete/archive policy |
| `tools/vendor/` | THIRD_PARTY_REFERENCE | imported vendor source/build products | use as reference only; extract minimal patterns into our own tools |
| `tools/claw-code/` | THIRD_PARTY_REFERENCE | large external/reference code tree | do not make it foundation; document useful principles only |
| `PRODUCTOS_MEDIOEVO/_ARCHIVAR_2026-04-24/` | LEGACY_PRODUCT_ARCHIVE | old zips/raw product packages | keep local until all hashes/fichas are closed |
| `PRODUCTOS_MEDIOEVO/*.txt` and raw prompt notes | RAW_PRODUCT_NOTES | mixed product strategy and assistant outputs | absorb into `docs/product` or `docs/publishing`, not as canon text |
| `PRODUCTOS_MEDIOEVO/04_AUDIOVISUAL_Y_TCG/` | PRIVATE_PRODUCT_BOUNDARY | TCG/audiovisual lane can touch private canon/assets | keep blocked; summarize through private boundary docs |
| `PRODUCTOS_MEDIOEVO/content_forge/runtime/` | GENERATED_PRODUCT_RUNTIME | rendered media, previews and job logs | keep local; source may be promoted separately |
| `apps/local/wabi-sabi/runtime/` | LOCAL_AGENT_RUNTIME | memory, logs and generated outputs | keep local; promote only tests/contracts/source |
| `game-private/` | PRIVATE_BLOCKED | RPG/TCG/private game boundary | only boundary READMEs may enter repo; no assets/canon dump |

## Fundamental Path

1. Read `README.md`, `docs/INDEX.md`, `docs/intake/ATLAS_MAIN.md`.
2. Use `docs/intake/CURADOR_MASTER_INDEX.md` for source absorption truth.
3. Use `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md` and `RISK_REGISTER.md` for
   public/commercial/private split.
4. Use `docs/product/README.md` for product lanes.
5. Use `apps/`, `packages/` and `research/` only after their tests and scans pass.

## Status

- No raw vault was deleted by this change.
- No external publication was performed by this change.
- The purpose is to reduce tree noise and force every promoted file to have a
  lane, owner, gate and evidence.
