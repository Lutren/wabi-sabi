# GUMROAD_CATALOG

Status: two entries published; app-agent candidates are separated by buyer-facing
lane so the website can sell without implying unverified checkout delivery.

Each product must have:

```txt
name
audience
free_or_paid
price
platform
what_it_includes
what_it_excludes
upsell
risk
next_action
```

## Catalog Entries

### MEDIOEVO Agent Ops Pack

name: MEDIOEVO Agent Ops Pack
audience: creators, developers and operators shipping public-safe agent products
free_or_paid: paid
price: 29 USD
platform: Gumroad
url: https://lrgonzalez.gumroad.com/l/medioevo-agent-ops-pack
deliverable_status: published_artifact
deliverable_evidence: `releases\paid\medioevo-agent-ops-pack.zip`, SHA256 `7cf8fdf5c8da49d691947becebdd3feae5f93b7e062212af38e3063404fab948`, aligned in `docs\product\product-listing-deliverable-alignment-2026-05-03.md`
what_it_includes: technical card template, curator report template, ActionGate checklist, GitHub release checklist, Gumroad listing template, synthetic audit example and support notes
what_it_excludes: private Claudio runtime, books, RPG, TCG, assets, lore, credentials, sessions, customer data and high-risk claims
upsell: support, implementation help and future UI/agent wrappers
risk: published package must stay synchronized with artifact hash and support policy
next_action: add website landing and customer-facing screenshots/copy

### FlujoCRM

name: FlujoCRM
audience: small teams and solo operators that need a simple local CRM
free_or_paid: paid founder access
price: 49-97 USD draft
platform: website contact first, Gumroad only after installer evidence
deliverable_status: founder_access_only
deliverable_evidence: Windows/local QA evidence exists, but public checkout remains blocked; source ZIP is internal QA only per `docs\product\product-listing-deliverable-alignment-2026-05-03.md`
what_it_includes: CRM workflow, contacts, pipeline, local business memory and setup support
what_it_excludes: autonomous external sending, private Claudio runtime, customer data migration guarantees
upsell: support, setup and future Agent Ops bundle
risk: current-user install and SQLite storage QA passed; pilot copy drafted; clean VM/legal review/signing decision incomplete
next_action: clean-machine smoke, legal review, unsigned-warning/signing decision

### Asistente Negocio

name: Asistente Negocio MEDIOEVO
audience: small businesses that want a human-approved assistant for customer replies and follow-up
free_or_paid: paid founder access
price: 49 USD founder draft
platform: website contact first, Gumroad only after QA/legal/support closure
deliverable_status: founder_access_only
deliverable_evidence: Windows/current-user QA evidence exists, but public checkout remains blocked; source ZIP is internal QA only per `docs\product\product-listing-deliverable-alignment-2026-05-03.md`
what_it_includes: business workflow assistant, response drafting and CRM-adjacent organization
what_it_excludes: autonomous WhatsApp/email sending, regulated advice, private runtime
upsell: setup, templates and FlujoCRM
risk: Windows current-user installer QA passed; install notes and support/privacy/refund draft exist, but clean-machine QA, final legal review and signing/unsigned warning approval remain open
next_action: clean-machine smoke, approve support/refund/privacy/terms, decide signing vs unsigned warning, verify checkout after upload

### Wave Collapse

name: Wave Collapse
audience: operators with messy document folders who need curation, evidence and rollback
free_or_paid: pilot / paid setup later
price: TBD
platform: website interest only
deliverable_status: private_demo_only
deliverable_evidence: synthetic local evidence pack and captures exist; no public sale/download until DOCX visual QA, legal/listing and ActionGate per `docs\product\product-listing-deliverable-alignment-2026-05-03.md`
what_it_includes: document-collapse workflow, audit trail and rollback-oriented curation
what_it_excludes: guaranteed truth, legal discovery guarantees, private documents in public demos
upsell: custom setup and Agent Ops Pack
risk: claims and sanitized test evidence required before paid checkout
next_action: run sanitized before/after sample and write claims boundary

### DUAT Templates

name: DUAT Templates
audience: developers, researchers and teams using synthetic simulation labs
free_or_paid: paid template pack
price: 19 USD
platform: Gumroad
url: https://lrgonzalez.gumroad.com/l/duat-templates
deliverable_status: published_artifact
deliverable_evidence: `releases\paid\duat-templates.zip`, SHA256 `03c926b549307ef6106d80117183bb22121354671a10e0f2527473c06f6ca518`, aligned in `docs\product\product-listing-deliverable-alignment-2026-05-03.md`
what_it_includes: DUAT Genesis lab card, synthetic scenario brief, falsifier report template, example synthetic lattice study and support notes
what_it_excludes: DUAT Geodia private engineering, MEDIOEVO RPG/TCG, private runtime, credentials, datasets, validated science, diagnosis or real-world prediction claims
upsell: implementation support, custom wrappers and Agent Ops Pack
risk: listing must not imply private DUAT Geodia access or scientific validation
next_action: monitor listing, add screenshots or demo media, and keep artifact `releases\paid\duat-templates.zip` synchronized with SHA256 `03c926b549307ef6106d80117183bb22121354671a10e0f2527473c06f6ca518`

### EL OBSERVADOR ebook

name: EL OBSERVADOR ebook
audience: readers, builders, Observacionismo audience
free_or_paid: paid
price: 9-15 USD draft
platform: Gumroad, website
deliverable_status: draft_blocked
deliverable_evidence: no approved sale artifact in `docs\product\product-listing-deliverable-alignment-2026-05-03.md`
what_it_includes: ebook/PDF after editorial review
what_it_excludes: PSI toolkit source, private game lore
upsell: companion PDF, developer toolkit
risk: legal/editorial review
next_action: approve final manuscript and sample boundary

### MEDIOEVO Starter Pack

name: MEDIOEVO Starter Pack
audience: new readers
free_or_paid: paid or lead-magnet variant
price: 9-19 USD draft
platform: Gumroad
deliverable_status: draft_blocked
deliverable_evidence: ZIP detected but not verified for sale in `docs\product\product-listing-deliverable-alignment-2026-05-03.md`
what_it_includes: curated entry bundle
what_it_excludes: full archive, game source
upsell: Ultimate Archive
risk: ZIP contents not yet verified
next_action: generate manifest and hash

### Claudio Special Agent Pack

name: Claudio Special Agent Pack
audience: developers and power users
free_or_paid: paid
price: 29-79 USD draft
platform: Gumroad, website
deliverable_status: draft_blocked
deliverable_evidence: no clean package allowlist yet in `docs\product\product-listing-deliverable-alignment-2026-05-03.md`
what_it_includes: premium templates/workflows
what_it_excludes: secrets, private game, offensive tooling
upsell: Developer Lifetime Bundle
risk: must separate from vendors
next_action: create clean package allowlist
