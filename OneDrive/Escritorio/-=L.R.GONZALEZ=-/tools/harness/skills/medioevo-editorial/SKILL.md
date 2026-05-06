---
name: medioevo-editorial
description: Local MEDIOEVO editorial skill for canon/book continuation, story-bible repair, lore review queues, manuscript-to-scene mapping, and editorial closeout. Use when working on MEDIOEVO books, canon docs, story_bible, LoreCompiler, donor capsules, or editorial runtime evidence.
---

# MEDIOEVO Editorial

Operate as a local editorial harness. Do not publish, upload, move, delete, or package book/canon material.

## Reads

- Root controls: `AGENTS.md`, `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`, `RISK_REGISTER.md`, `SECRET_SCAN_REPORT.md`.
- Editorial state: `-=MEDIOEVO=-\-=LIBROS\**` continuity docs when working there.
- RPG lore state when relevant: `E:\Medioevo_RPG\data\story_bible.json`, `data/lore/LoreReviewQueue.json`, `data/lore/LoreCompilerPlayableContract.json`, `docs/private/*LORE*`.

## May Touch

- Editorial ledgers, story-bible/lore manifests, validation reports, and handoff docs explicitly selected for the task.
- Never move or delete manuscripts, book folders, vaults, private game source, or user files.
- No usar git add .; stage only owned paths from the correct repo if a commit is explicitly part of the loop.

## Required Evidence

- File evidence: exact paths changed plus before/after status.
- Validator/report evidence when available: lore compiler validation, story-bible completion validator, or a generated review report.
- For book closeout: prove donor material was absorbed into scenes/codas/presage; do not close if a section still ends as raw donor capsules.

## ActionGate Blocks

Block and request ActionGate plus `host_observacionista` when the task involves publication, Gumroad, website release, external APIs, moving/deleting user files, full-book export, or any public sample decision.
Block if host state is `JAMMING` or `BLOCK`.
