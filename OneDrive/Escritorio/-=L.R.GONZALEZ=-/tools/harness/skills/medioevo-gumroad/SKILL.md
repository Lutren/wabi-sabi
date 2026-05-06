---
name: medioevo-gumroad
description: Local MEDIOEVO Gumroad skill for product-state audits, publication handoffs, draft cleanup planning, product copy, catalog evidence, and safe separation of Gumroad truth from website uptime.
---

# MEDIOEVO Gumroad

Default to read-only planning unless ActionGate approves live Gumroad actions. Website uptime is not publication proof.

## Reads

- `GUMROAD_CATALOG.md`, `GUMROAD_PRODUCTS.md`, `PUBLISHING_PLAN.md`, `PRODUCT_CATALOG.md`, `RELEASE_EVIDENCE.md`.
- Existing publication scripts/docs only when selected by the task.
- Prior authenticated state paths may be referenced only as paths; do not open or use sessions without ActionGate.

## May Touch

- Local product catalog docs, publication handoff prompts, Gumroad copy drafts, QA checklists, and evidence reports.
- Do not edit live Gumroad products, delete drafts, upload files, or use authenticated browser/session state without gate.
- No usar git add .; stage only owned publication docs/scripts after evidence.

## Required Evidence

- For local-only work: changed file paths and generated handoff/copy artifact.
- For live state verification after gate: API response summary plus public/authenticated URL evidence, with dates.
- For cleanup: product IDs, pre-action count, post-action count, and rollback/residue note.

## ActionGate Blocks

Always require ActionGate plus `host_observacionista` for Gumroad API calls, authenticated UI, product create/update/delete, price changes, file uploads, publication/unpublication, payment or customer data access.
Block if credentials are absent, host state is `JAMMING` or `BLOCK`, or requested evidence cannot be verified.
