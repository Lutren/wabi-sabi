# Gumroad Channel Update Packet - 2026-05-05

Estado: copy listo para actualizar Gumroad despues de verificar sesion/API. No declara cambios live.

## Perfil de tienda

Tagline:

```text
MEDIOEVO digital products for local-first AI workflows, agent operations, DUAT templates, writing systems and public-safe automation.
```

Descripcion:

```text
MEDIOEVO sells finished layers around Claudio and Observacionismo: templates, checklists, product workflows, support packs, writing tools and commercial wrappers.

The reusable foundations stay open on GitHub when they can be public-safe. Paid products package the method into usable artifacts, examples, support notes and clear delivery boundaries.

Products do not include private prompts, internal runtimes, RPG/TCG material, unreleased books, credentials, datasets or claims of guaranteed safety, diagnosis, prediction or scientific validation.
```

## MEDIOEVO Agent Ops Pack

Status: published product to keep active.

Short description:

```text
Templates and checklists for turning AI agent work into auditable releases: technical cards, curator reports, ActionGate checks, GitHub release prep, Gumroad listing copy and a synthetic audit example.
```

Boundary:

```text
Does not include private Claudio runtime, prompts, books, RPG/TCG assets, credentials, sessions, customer data or guaranteed safety claims.
```

Next listing update:

- Add screenshot or preview image from public-safe templates.
- Confirm artifact SHA256 before uploading any new ZIP.
- Keep price at USD 29 unless a new commercial decision is recorded.

## DUAT Templates

Status: published product to keep active.

Short description:

```text
Template pack for turning DUAT Genesis synthetic simulations into lab cards, scenario briefs, falsifier reports, study notes and non-technical summaries.
```

Boundary:

```text
Does not include DUAT Geodia private engineering, real datasets, RPG/TCG material, medical claims, physical claims, social prediction claims or validated science claims.
```

Next listing update:

- Add public-safe preview of one synthetic lab card.
- Link to `duat-genesis` and `duat.html`.
- Keep price at USD 19 unless a new commercial decision is recorded.

## Draft / founder access products

| product | Gumroad state | allowed Gumroad action |
|---|---|---|
| FlujoCRM | founder access only | no public checkout until clean-machine QA, legal/support, installer/signing decision |
| Asistente Negocio | founder access only | no public checkout until clean-machine QA, legal/support and delivery evidence |
| Mini Office | review | no product page until final package and legal gate |
| Writer Workbench | draft | wait for artifact manifest and sample boundary |
| Wave Collapse | pilot | no sale until sanitized before/after demo and claims boundary |
| EL OBSERVADOR ebook | draft | wait for editorial artifact and sample boundary |

## Gate before live Gumroad update

1. Read current product through Gumroad API or authenticated dashboard.
2. Confirm target product id or URL.
3. Secret scan listing JSON and artifact.
4. Path scrub source package and listing.
5. Claims scan listing.
6. ActionGate target `gumroad:<slug>`.
7. Update listing.
8. Verify public URL returns HTTP 200 and shown copy matches the packet.
