# Public Content Ready Packet - 2026-05-06

Status: `LOCAL_CONTENT_READY / PNG_RENDERED / ACCOUNT_AUTH_REQUIRED / NO_POST_EXECUTED`

This packet prepares public-safe content for social posts and optional Gumroad
media. It does not publish, schedule, upload, edit accounts, change listings or
claim live social activity.

## Assets

| asset | use | boundary |
|---|---|---|
| `docs/publishing/assets/social/2026-05-06/evidence-before-action-card.svg` / `.png` | general evidence-gate post | public method only |
| `docs/publishing/assets/social/2026-05-06/sponsors-high-tier-card.svg` / `.png` | Sponsors update | no private access promise |
| `docs/publishing/assets/social/2026-05-06/agent-ops-pack-card.svg` / `.png` | Gumroad Agent Ops Pack | templates/checklists only |
| `docs/publishing/assets/social/2026-05-06/duat-templates-card.svg` / `.png` | Gumroad DUAT Templates | synthetic templates only |

All assets are locally authored SVGs plus Chrome-headless PNG exports with no
external images, no private paths, no dashboard screenshots, no account data and
no RPG/TCG material.

## PNG Render Evidence

Render method: Chrome headless screenshot, `1200x630`, from local `file://`
SVG sources.

| PNG asset | dimensions | bytes | sha256 |
|---|---:|---:|---|
| `docs/publishing/assets/social/2026-05-06/agent-ops-pack-card.png` | `1200x630` | `49867` | `d8257e9adeebc1d4c64fddfbe15b03d04ecc7b4c9f2311f7293e9db0b05c5bc3` |
| `docs/publishing/assets/social/2026-05-06/duat-templates-card.png` | `1200x630` | `45994` | `b70f2510b4db0d6dfc8979038022cbd0b3bcaa84fb7f901929ca52820268f558` |
| `docs/publishing/assets/social/2026-05-06/evidence-before-action-card.png` | `1200x630` | `46239` | `54a21965e55469652612b6b3558ee0a803350a10c98b87cf52582aa248ad7579` |
| `docs/publishing/assets/social/2026-05-06/sponsors-high-tier-card.png` | `1200x630` | `51745` | `464fcc8e432921dae7b55c2bc691f75db7a279460c1252366fc978827ff22de0` |

## Ready Captions

### Evidence Gate

```text
Rule for MEDIOEVO public work:

No source without ficha.
No claim without evidence.
No risky action without gate.
No public copy without a private-boundary check.

The open tools are on GitHub. The private runtime stays private.
https://github.com/Lutren
```

### Sponsors

```text
MEDIOEVO now has a high-tier GitHub Sponsors lane for institutions and strategic patrons.

It supports curated research packets, public-safe demos and strategic briefings around local-first AI, ActionGate, Observacionismo and evidence-before-action systems.

No raw private archives. No secrets. No RPG/TCG IP. Public tools stay public; private IP stays protected.

https://github.com/sponsors/Lutren
```

### Agent Ops Pack

```text
MEDIOEVO Agent Ops Pack is for builders turning agent work into public-safe releases:

- technical fichas
- curator reports
- ActionGate checklist
- GitHub release checklist
- Gumroad listing template

It does not include private prompts, runtime or guaranteed outcomes.
https://lrgonzalez.gumroad.com/l/medioevo-agent-ops-pack
```

### DUAT Templates

```text
DUAT Templates is a synthetic lab pack:

scenario cards, falsifier reports and observation notes for public-safe simulation work.

It is not private DUAT Geodia, not a prediction engine and not scientific validation.
https://lrgonzalez.gumroad.com/l/duat-templates
```

## Posting Gate

Before any live post:

1. confirm authenticated account and target platform;
2. scan this packet and selected asset;
3. run ActionGate for the exact platform/action;
4. post only one target per run;
5. capture live URL or screenshot;
6. write evidence JSON and COMMS event.

## Optional Gumroad Media Gate

The product cards can be used as optional media only after:

- product-specific Gumroad ActionGate;
- selected SVG/source scan;
- confirmation that the action is media-only;
- post-upload public page verification.

Do not replace delivery ZIPs, prices, titles or payout/settings from this media
packet.
