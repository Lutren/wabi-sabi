---
name: hormiguero-surface
description: Local Hormiguero/GEODIA surface skill for living-city UI, mission-control/hub comparison, city registry APIs, observability panels, and public/private split without touching Claudio runtime internals.
---

# Hormiguero Surface

Preserve the Hormiguero/GEODIA city metaphor. Build UI/API-consumer surfaces; treat Claudio runtime/model routing as a dependency.

## Reads

- Hormiguero app roots such as `hormiguero_mission_control`, `hormiguero_hub`, `apps`, `website`, and related docs when present.
- `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`, `PRIVATE_GAME_BOUNDARY.md`.
- API contracts such as `/api/city-registry` or `/api/observastack/snapshot` if implemented locally.

## May Touch

- Hormiguero UI, docs, mock snapshots, city-registry manifests, and local tests in the selected surface lane.
- Do not touch private game, Gumroad publication, Claudio core runtime, or model daemons unless selected and gated.
- No usar git add .; stage only Hormiguero-owned paths after tests.

## Required Evidence

- Local UI/build/test command, screenshot/report, or API mock output.
- File inventory showing which surface was chosen as source of truth.
- If no implementation exists, produce analysis-only artifact and mark status `candidate`, not complete.

## ActionGate Blocks

Require ActionGate plus `host_observacionista` for deploys, public website changes, live API calls, external screenshots, authenticated browser actions, or model/daemon launch.
Block if host state is `JAMMING` or `BLOCK`.
