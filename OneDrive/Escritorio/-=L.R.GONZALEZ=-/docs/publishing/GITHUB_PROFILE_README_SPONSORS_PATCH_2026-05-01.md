# GitHub Profile README Sponsors Patch - 2026-05-01

Status: `APPLIED_WITH_HUMAN_OVERRIDE`

Target: `https://github.com/Lutren/Lutren/blob/main/README.md`

Reason: make the live Sponsors profile easier to discover from the public GitHub profile without revealing private technology or promising absolute outcomes.

ActionGate result:

- Dry-run: `PASS`
- Execute before override: `BLOCKED`
- Block reason before override: external publication requires host `APPROVE`; current host gate was `REVIEW`.
- User override: granted explicitly on 2026-05-01.
- Remote README commit: `9403c31695d4c167aa9d3cbcfec3e5a0ad897786`.
- Remote formatting commit: `08f8f7a258763eff22fe0d33d6931b68c43dde83`.
- Remote `.github/FUNDING.yml` commit: `9b807a384af6dcfce85eb158141e9cd7e086fdb4`.

## Insert Before `## Design principles`

```md
## Sponsorship

If this work is useful to you, you can sponsor the public layer: https://github.com/sponsors/Lutren

Sponsorship funds maintenance, tests, docs, security review, and public-safe demos for local-first AI safety gates. It does not include private prompts, the full internal orchestration layer, unreleased books, RPG/TCG material, family data, secrets, or absolute outcome claims.
```

## Add To Links

```md
- [Sponsor](https://github.com/sponsors/Lutren)
```

Recommended position: first item under `## Links`.

## Do Not Add

- Private prompt excerpts.
- Architecture internals that make the paid implementation reproducible.
- RPG/TCG material, lore, card data or game bridge details.
- Family, legal, financial or personal operational data.
- Claims that promise absolute safety, total hallucination removal or solved alignment.
