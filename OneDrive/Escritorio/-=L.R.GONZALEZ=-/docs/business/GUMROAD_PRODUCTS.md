# GUMROAD_PRODUCTS

Status: two paid products published on Gumroad on 2026-05-02.

Fees checked on 2026-04-29 against official Gumroad pricing:

- Direct/profile sales: `10% + $0.50` per transaction.
- Discover marketplace: `30%` per transaction.
- Gumroad states it acts as merchant of record and handles sales tax collection/remittance from 2025.

Source: https://gumroad.com/pricing

## Candidate Products

| name | type | price draft | status | notes |
|---|---|---:|---|---|
| MEDIOEVO Agent Ops Pack | templates/support pack | 29 USD | published, copy updated | URL: https://lrgonzalez.gumroad.com/l/medioevo-agent-ops-pack; ZIP SHA256 `7cf8fdf5c8da49d691947becebdd3feae5f93b7e062212af38e3063404fab948`; copy-only update verified 2026-05-06 in `qa_artifacts\release_validation\gumroad-medioevo-agent-ops-pack.json` |
| DUAT Templates | Agente Laboratorio | 19 USD | published, copy updated | URL: https://lrgonzalez.gumroad.com/l/duat-templates; ZIP SHA256 `03c926b549307ef6106d80117183bb22121354671a10e0f2527473c06f6ca518`; copy-only update verified 2026-05-06 in `qa_artifacts\release_validation\gumroad-duat-templates.json` |
| MEDIOEVO Starter Pack | bundle | 9-19 USD | review | existing ZIP detected; verify contents |
| MEDIOEVO Ultimate Archive | bundle | 49-99 USD | review | huge ZIP detected; verify rights and contents |
| EL OBSERVADOR ebook | ebook | 9-15 USD | draft | legal/editorial review |
| Brain OS Companion PDF | PDF | 7-15 USD | draft | pair with free blueprint |
| ResidueOS Pro Templates | templates | 19-39 USD | draft | define product first |
| Claudio Special Agent Pack | agent pack | 29-79 USD | draft | remove private/secrets |
| MEDIOEVO Writer Toolkit | app/templates | 29-99 USD | draft | align with writer mode |
| Developer Lifetime Bundle | bundle | 149-299 USD | draft | open-core upsell |

## App-Agent Checkout Backlog

These entries are commercial candidates, not live Gumroad products. They should
not be published until their package-specific gates pass.

| name | app-agent | price draft | store status | required before Gumroad |
|---|---|---:|---|---|
| FlujoCRM | Agente Mercado | 49-97 USD | founder access only | current-user install and SQLite storage QA passed; pilot support/refund/privacy/unsigned copy drafted; still needs clean-machine install smoke, legal review and signing decision |
| Asistente Negocio | Agente Mostrador | 49 USD founder | founder access only | Windows installer current-user QA passed; install notes and support/privacy/refund draft included; still needs clean-machine install smoke, final legal review, signing or approved unsigned-warning decision and public checkout verification |
| Mini Office | Agente Oficina | 29-79 USD | founder access review | local smoke/package passed; copy/license/installers/generators cleaned; rebuilt ZIP SHA256 `4315003693566D93F6F48DEF1C5EACE14BBE6531CEDFB878BE121699502D3710`; manifest `blocked_count=0`; still needs legal review, clean-machine install, support/privacy/refund and checkout verification |
| Writer Workbench / Companero Escritura | Agente Editorial | 47 USD draft | request access only | export QA, delivery package, editorial rights boundary |
| Wave Collapse | Agente Curador Documental | pilot pricing TBD | pilot interest only | sanitized document tests, claims review, rollback evidence |
| NEUROSTATE UI | Agente Estado | setup TBD | blocked by split | privacy review, no medical/cognitive diagnosis claims, public-safe UI package |

## Required Before Upload

- Product manifest.
- Secret scan.
- Private game exclusion.
- License/legal review.
- Support/refund/privacy/terms drafts.
- Package hash.
- Human content review.

Applied for `MEDIOEVO Agent Ops Pack`:

- source and artifact secret scans reported `count_reported=0`;
- path scrub and claims scan passed;
- Gumroad API verified `published=true`;
- public product URL returned HTTP `200`.

Applied for `DUAT Templates`:

- source and artifact secret scans reported `count_reported=0`;
- path scrub and claims scan passed;
- Gumroad API verified `published=true`;
- public product URL returned HTTP `200`;
- website links deployed to `medioevo-site` and verified on `medioevo.space`.
