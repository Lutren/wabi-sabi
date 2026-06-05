/**
 * DUAT Render Specification — Single Source of Truth
 *
 * Canonical render specification contract that all 4 DUAT graphics engines
 * (Python, Forge, Game, Web) must consume. Pure TS types + constants.
 * No dependencies. No runtime logic beyond spec resolution.
 *
 * OSIT epistemic state: CERTEZA (contract), INFERENCIA (defaults),
 * falsifiable via F_UNIFY_01 and F_SPEC_01.
 *
 * M-P0 deliverable — BRAIN_OS / motor_grafico
 */

export type DUATProjection = "dimetric_2to1" | "isometric_30" | "orthogonal";

export type MOIMode = "MOI_FAST" | "MOI_DEEP";

export interface DUATRenderSpec {
  schema_version: "duat.render_spec.v1";
  projection: DUATProjection;
  tileW: number;
  tileH: number;
  chunkSize: number;
  targetFPS: number;
  frameBudgetMs: number;
  ositCanonRef: string;
  moiMode: MOIMode;
}

export const CANONICAL_SPECS: Record<string, DUATRenderSpec> = {
  ISO_PYTHON: {
    schema_version: "duat.render_spec.v1",
    projection: "isometric_30",
    tileW: 64,
    tileH: 32,
    chunkSize: 16,
    targetFPS: 30,
    frameBudgetMs: 33.33,
    ositCanonRef: "ositCanon.ts / obsai_core.metrics",
    moiMode: "MOI_FAST",
  },
  ISO_FORGE: {
    schema_version: "duat.render_spec.v1",
    projection: "dimetric_2to1",
    tileW: 128,
    tileH: 128,
    chunkSize: 10,
    targetFPS: 60,
    frameBudgetMs: 16.67,
    ositCanonRef: "ositCanon.ts / obsai_core.metrics",
    moiMode: "MOI_FAST",
  },
  ISO_GAME: {
    schema_version: "duat.render_spec.v1",
    projection: "isometric_30",
    tileW: 64,
    tileH: 32,
    chunkSize: 16,
    targetFPS: 60,
    frameBudgetMs: 16.67,
    ositCanonRef: "ositCanon.ts / obsai_core.metrics",
    moiMode: "MOI_FAST",
  },
};

const MODE_MAP: Record<string, string> = {
  python: "ISO_PYTHON",
  forge: "ISO_FORGE",
  game: "ISO_GAME",
};

export function resolveSpec(mode: string): DUATRenderSpec {
  const key = MODE_MAP[mode] ?? "ISO_GAME";
  return CANONICAL_SPECS[key];
}

export const FALSIFIERS: Record<string, string> = {
  F_UNIFY_01:
    "All 4 engines produce same iso projection for (0,0)->canvas and (1,1)->canvas given same spec",
  F_SPEC_01:
    "resolveSpec('forge').tileW === 128 && resolveSpec('forge').tileH === 128",
};
