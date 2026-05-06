# Website Public Funnel Review 2026-05-05

Status: `LOCAL_REVIEW_COMPLETE / NO_DEPLOY`

Skill used: `seo-growth-medioevo`.

## Audit Result

The first audit target from the skill,
`-=MEDIOEVO=-\-=LIBROS\website`, is not the active public site source. It only
contains a recovery doc and an `img` folder. Its missing SEO basics should not
be treated as the production baseline.

The canonical website source for the live public site is:

```text
C:\Users\L-Tyr\OneDrive\Escritorio\-=L.R.GONZALEZ=-\-=MEDIOEVO=-\-=LIBROS\claudio\website
```

Audit result for the canonical source:

| check | status |
|---|---|
| meta description | OK |
| canonical | OK |
| Open Graph title/description | OK |
| Twitter card | OK |
| JSON-LD | OK |
| WebSite schema | OK |
| alternateName | OK |
| robots.txt | OK |
| sitemap.xml | OK |
| llms.txt | OK |
| company.md | OK |

Finding: no major SEO basics issue in the canonical source.

## Funnel Reading

Current public routes are already useful:

- home: MEDIOEVO brand, books, Gumroad, apps, open source and private-boundary
  language;
- software: GitHub/open-source developer route;
- apps: commercial and lab product route;
- agent-ops-pack: paid Gumroad product route;
- publicacion: publication map route.

Main optimization is not technical SEO. It is visitor routing.

## Recommended Route Hierarchy

Keep the city metaphor, but reduce choice overload:

1. `Start here`: what is MEDIOEVO?
2. `Read`: books and saga.
3. `Use`: apps, templates and Gumroad.
4. `Build`: open-source tools on GitHub.
5. `Support`: GitHub Sponsors.

## Local Patch Applied

Do not deploy during host `BLOCK`.

Applied local-only changes to `-=MEDIOEVO=-\-=LIBROS\claudio\website\index.html`:

- added GitHub Sponsors to the visible top-strip routes;
- added GitHub Sponsors to the store route chips;
- added public `sameAs` links for GitHub, GitHub Sponsors and Gumroad in the
  `Organization` JSON-LD block;
- did not add LinkedIn because the canonical profile URL is still `REVIEW`;
- did not change product claims, prices, checkout or private-boundary language.

Validation after patch:

- JSON-LD parsed successfully: `json_ld_blocks=1 json_ld_ok=true`.
- Canonical website SEO audit still reports all checks `OK` and no major
  findings.
- Focused secret scan on `website/index.html`: `count_reported=0`.

Next local website patch, after this one is reviewed, should only:

- add a small "Start here" strip near the top of the home page if the owner
  wants an even simpler first route;
- avoid adding new product claims;
- keep private RPG/TCG and runtime behind boundary language;
- rerun the SEO audit and local smoke before deploy.

## Deployment Gate

Before Cloudflare or website deploy:

1. host gate `APPROVE`;
2. focused secret scan over changed website files;
3. claims/private-boundary scan;
4. `sitemap.xml` still parses;
5. live post-deploy HTTP 200 checks.
