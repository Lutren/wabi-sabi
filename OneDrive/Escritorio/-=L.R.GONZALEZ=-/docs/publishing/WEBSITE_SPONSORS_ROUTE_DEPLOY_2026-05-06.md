# Website Sponsors Route Deploy - 2026-05-06

Status: `LIVE_DEPLOYED_VERIFIED`

Target: `medioevo-site`

Production URL: `https://medioevo.space/`

Preview URL: `https://2839b9df.medioevo-site.pages.dev/`

## Scope

Deployed only the canonical `claudio/website` surface to publish the already
prepared GitHub Sponsors route visibility patch.

No GitHub push, Gumroad edit, LinkedIn edit, social post, DNS change or product
artifact upload was executed in this pass.

## Preflight

| check | result |
|---|---|
| host persisted gate | `LIMPIO / APPROVE` at `2026-05-06T12:44:55Z` |
| ActionGate | `pass`, decision `3d978456-204d-4c2b-876f-38ae6257bae2` |
| deploy test | `python -m pytest tests\test_cloudflare_deploy_setup.py -q` -> `13 passed` |
| deploy dry-run | `python tools\deploy_a_cloudflare.py --dry-run` -> OK |
| website secret scan | `count_reported=0` |
| local Sponsors route | `website/index.html` contains `GitHub Sponsors` and `https://github.com/sponsors/Lutren` |

## Deploy Command

```powershell
python tools\deploy_a_cloudflare.py
```

Result:

- Wrangler `4.84.1`;
- uploaded `36` files, `567` already uploaded;
- `_headers` and `_redirects` uploaded;
- deployment complete;
- preview URL: `https://2839b9df.medioevo-site.pages.dev`.

## Live Verification

Production check:

```text
url=https://medioevo.space/
status=200
githubSponsors=True
sponsorUrl=True
sameAs=True
```

Preview check:

```text
url=https://2839b9df.medioevo-site.pages.dev/
status=200
githubSponsors=True
sponsorUrl=True
sameAs=True
```

Sponsors page recheck:

```text
url=https://github.com/sponsors/Lutren
status=200
tier1000=True
tier5000=True
tier10000=True
custom12000=False
```

## Boundary

This deploy only exposes the public-safe Sponsors route and structured public
profile link. It does not publish private research dumps, secrets, full
internal runtime prompts, private books, RPG/TCG material, private datasets or
guaranteed outcomes.
