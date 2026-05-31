---
name: curador-operativo
description: Always-on curator workflow for dirty repos, unknown sources, Downloads, duplicated folders, useful tech extraction, discard candidates and no-orphan-residue closure.
---

# Curador Operativo

Use this skill whenever a task discovers a broad/dirty repo, unknown folder,
external source, ZIP/TXT, duplicated code, vendor tree, cache/build output or
possible discard candidate.

## Reads

- `AGENTS.md`
- `docs/developer/CURADOR_ALWAYS_ON_PROTOCOL_2026-05-03.md`
- `SOURCE_INTAKE_REGISTER.md` and `source_intake_register.json`
- `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`, `RISK_REGISTER.md`
- `DUPLICATES_AND_DEAD_CODE.md`, `DELETE_CANDIDATES.md`, `MIGRATION_MAP.md`
- Claudio `CLAUDE.md`, `PENDIENTES_MASTER.md`, `NEXT_SESSION_BRIEF.md`

## May Touch

- Curator/register docs listed above.
- `docs/memoria_viva/fichas` and relevant governance docs.
- Read-only preflight tooling under `tools/release`.
- Never copy raw private sources, RPG/TCG, sessions, credentials, paid product
  source or dirty repos into public lanes.
- No usar git add .; use `git add -- <owned paths>` only from the correct repo, never from `C:\Users\L-Tyr`.

## Required Evidence

Run:

```powershell
python tools/release/curador_preflight.py --path <path>
```

From Claudio:

```powershell
python tools/curador_preflight.py --path <path>
```

Then one of these must be true before closure:

- existing ficha is cited;
- new ficha/register entry is created;
- useful tech is copied selectively with provenance and tests/smoke plan;
- private/secret boundary is documented;
- discard candidate is listed without direct deletion.

## ActionGate Blocks

Block publication, broad copy, file moves, deletion, ZIP creation or dependency
adoption until the path has a ficha, secret/path/claim/license review where
relevant, and cleanup/publish ActionGate if the action is external or
destructive.
Require ActionGate plus `host_observacionista` for any external or destructive action; block if host state is `JAMMING` or `BLOCK`.
