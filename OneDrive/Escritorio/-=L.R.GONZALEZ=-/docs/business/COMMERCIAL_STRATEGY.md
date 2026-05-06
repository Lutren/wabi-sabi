# COMMERCIAL_STRATEGY

Status: draft.

## Principle

Give away tools that create community. Sell products that save time, create an experience, or contain the finished work.

Commercial source ZIPs are internal QA artifacts unless a separate reviewed
license explicitly sells source access. Customer-facing paid apps should ship as
installers/apps, documentation, demos and support.

2026-05-02 decision: each paid app is treated as a specialized AI agent inside
the MEDIOEVO/GEODIA city. The open technology can be public; the commercial
value is the UI, wrapper, agent role, packaging, support, templates and guided
workflow.

## 2026-05-02 Patrimony Principle

Open source should create adoption, trust and community. Patrimony should come
from assets that remain controllable by the family:

- brands, domains and official accounts;
- commercial app support and installation;
- premium templates and courses;
- books, bundles, companion PDFs and controlled samples;
- hosted services built on open tools;
- consulting, audits and implementation support;
- RPG/TCG and world IP when separately reviewed.

Immediate non-code actions:

1. Keep `Downloads\r.txt` excluded from staging; it is recorded as `USER_ASSERTED_SAFE_NON_BLOCKING`, while repo-specific secret scans remain mandatory.
2. Add a GitHub successor and document continuity.
3. Keep a private digital-asset inventory outside public repos.
4. Route inheritance, tax, trademark and beneficiary decisions to professional review.

## Candidate Paid Products

| product | audience | path today | notes |
|---|---|---|---|
| Asistente Negocio MEDIOEVO | small business / productivity users | `claudio\products\asistente_negocio` | strongest app release candidate |
| FlujoCRM | business users | `apps\commercial\flujocrm` | standalone first, bundle later; Windows x64 installer QA and listing draft exist; needs clean-machine install, unsigned warning/signing and final legal review |
| Mini Office | creators/devs/productivity users | `claudio\mini_office` | open-core or paid app decision |
| Argus Desktop | Claudio/MEDIOEVO desktop users | `claudio\apps\argus_desktop` | needs UX/public-safe audit |
| MEDIOEVO companion PDFs | readers | `PRODUCTOS_MEDIOEVO\01_LIBROS_Y_BUNDLES` | do not publish full books by accident |
| EL OBSERVADOR | readers/dev-philosophy audience | `-=CEREBRO=-\-=PSI=-\libro` | editorial/legal review |
| Developer Lifetime Bundle | developers/power users | future package | bundle only open-safe and premium templates |
| DUAT Lab Templates | researchers/agent builders | future `duat-lab` package | synthetic lab templates, not RPG/canon or physics proof |
| NEUROSTATE Local Dashboard | creators/agent operators | future split from `#!usrbinenv python3.txt` | local observability UI with privacy and claims review |

## Agent Wrapper Positioning

| product | commercial agent | paid value |
|---|---|---|
| FlujoCRM | Agente Mercado | local CRM workflow, pipeline UI, privacy-first packaging and support |
| Asistente Negocio | Agente Mostrador | response drafting, human approval flow and business setup |
| Mini Office | Oficina de agentes | bundled productivity agents, templates and local setup |
| Argus Desktop | Agente Consola | desktop command surface for Claudio with evidence and ActionGate |
| Wave FC | Agente Curador Documental | document ordering, rollback, audit trail and premium templates |
| DUAT Lab Templates | Agente Laboratorio | synthetic research workflows, artifact memory and guided experiments |
| NEUROSTATE Dashboard | Agente Estado | local observability UI and privacy-safe integrations |

Canonical UI/design spec: `docs\design\MEDIOEVO_AGENT_CITY_UI_SYSTEM_2026-05-02.md`.

## Platforms

- Website: official hub and trust surface.
- Gumroad: digital goods, ebooks, bundles, app downloads. Current official pricing checked 2026-04-29: `10% + $0.50` direct/profile, `30%` marketplace, merchant-of-record tax handling from 2025.
- Buy Me a Coffee: support, memberships, dev logs, small extras. Current official help docs checked 2026-04-29: `5%` platform fee plus Stripe processing.
- GitHub: open/free developer tools only.

## Pricing Draft

All prices are draft and require review:

- Small PDFs/templates: USD 5-15.
- App starter packs: USD 19-39.
- Premium app bundles: USD 49-99.
- Lifetime developer bundle: USD 149-299.
- Founder/sponsor tiers: USD 50-100/month via membership.

## Legal

All legal text is draft only and `LEGAL_REVIEW_REQUIRED`.

Support intake draft: `medioevo.saga@gmail.com` is already used on public site
surfaces. A branded domain alias can replace it later, but no sale should depend
on an unmonitored inbox.

## Open Source To Commercial Bridge

| open surface | paid/patrimony surface |
|---|---|
| `data-curation-observatory` | Data Curation Pack, audits, managed cleanup |
| `residueos-core` | support, hosted gate, commercial integrations |
| `ai-web-gateway-observacionista` | commercial license, managed gateway, implementation |
| `obs-info-kernel-lite` | research consulting, premium templates |
| `observational-calibration-toolkit` | workshops, dashboards, benchmark packs |
| `duat-lab` | private lab setup, research templates, workshops |
| `neurostate-ui` | local dashboard setup, integrations, support |
| whitepapers | Sponsors, courses, credibility and sales funnel |
