# LLM-Wiki Legacy Host Queue - 2026-05-06

## Decision

The historical `llm-wiki` checklists contained open checkbox tasks for CUDA,
training, PSI ingestion, storage moves and cleanup.

Those are not safe autonomous local closures in the current session. They touch
host configuration, model training, storage layout or destructive cleanup.

## Reconciled Files

| file | old open checks | new marker | reason |
|---|---:|---|---|
| `-=MEDIOEVO=-\-=LIBROS\llm-wiki\INSTALACION_COMPLETA.md` | 3 | `llm-wiki-gate` | CUDA/training/ingestion require host readiness and owner-approved scope |
| `-=MEDIOEVO=-\-=LIBROS\llm-wiki\LIMPIEZA_YVRAM.md` | 8 | `llm-wiki-gate` | moves/deletes require exact source, destination, backup and post-verify |

## Required Gate Before Execution

Any future execution must have:

- current host gate `APPROVE`;
- exact paths for move/delete operations;
- backup or rollback plan;
- disk-space baseline before and after;
- model/training command scoped to an approved dataset;
- post-action evidence written to `qa_artifacts`.

## Boundary

No CUDA install, model training, PSI ingestion, file move, symlink creation,
cache deletion or disk cleanup was executed by this reconciliation.

