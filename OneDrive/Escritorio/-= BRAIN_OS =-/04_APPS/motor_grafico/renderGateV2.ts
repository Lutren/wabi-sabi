/**
 * RenderGate v2 — OSIT ResidueVector integration (TypeScript mirror).
 *
 * This is the TS mirror of render_gate_v2.py for the React/TS engine.
 * Connects frame performance to R_or (operational residue) and OSIT regime,
 * which then controls render quality level.
 *
 * M-P1 deliverable: RenderGate -> ResidueVector bridge.
 * Self-contained: inlines canonical OSIT thresholds (same as ositCanon.ts / obsai_core.metrics).
 * R_or = 1 - Π(1 - clamp(r_i * w_i, 0, 1))  (Noisy-OR, §2.3 DOCUMENTO_MAESTRO).
 * Quality level: FULL > DEGRADED > MINIMAL > HALT
 *
 * NOTE: regimeFromR and epistemicStateFromR imported from ositCanon.ts (single source of truth).
 * renderGateV2.ts no longer duplicates those functions — DRY refactor 2026-06-02.
 */

import { regimeFromR, epistemicStateFromR, clamp01, type OsitRegime, type OsitEpistemicState } from "./ositCanon";

// ── Types ──────────────────────────────────────────────────────────────
export type RenderQuality = "FULL" | "DEGRADED" | "MINIMAL" | "HALT";
export type EpistemicState = OsitEpistemicState;

function _clamp01(v: number): number {
  return clamp01(v);
}

export interface ResidueVector {
  r_lat: number; // latency gap: frame time deviation (w=0.75)
  r_sem: number; // semantic gap: fidelity drop (w=1.00)
  r_mem: number; // memory gap (w=1.00, unused in render, always 0)
  r_pri: number; // privacy gap (w=1.25, unused in render, always 0)
  r_con: number; // contradiction gap (w=1.25, unused in render, always 0)
  r_cost: number; // cost gap: resource overrun (w=1.00)
  r_act: number; // action gap: pending event pressure (w=1.50)
  rOr(): number;
}

export interface RenderGateResult {
  r_or: number;
  regime: OsitRegime;
  epistemic: EpistemicState;
  quality: RenderQuality;
  allow_render: boolean;
  r_vel: number;
  r_acc: number;
  pre_jamming: boolean;
  rv: ResidueVector;
}

// ── ResidueVector implementation ───────────────────────────────────────

export class ResidueVectorImpl implements ResidueVector {
  r_lat = 0.0;
  r_sem = 0.0;
  r_mem = 0.0;
  r_pri = 0.0;
  r_con = 0.0;
  r_cost = 0.0;
  r_act = 0.0;

  /**
   * Noisy-OR operational residue from all 7 dimensions.
   * R_or = 1 - Π(1 - clamp(r_i * w_i, 0, 1))
   * Canonical formula from DOCUMENTO_MAESTRO §2.3:
   * act=1.50, pri=1.25, con=1.25, sem=mem=cost=1.00, lat=0.75
   */
  rOr(): number {
    const dims: [number, number][] = [
      [this.r_lat, 0.75],
      [this.r_sem, 1.00],
      [this.r_mem, 1.00],
      [this.r_pri, 1.25],
      [this.r_con, 1.25],
      [this.r_cost, 1.00],
      [this.r_act, 1.50],
    ];
    let product = 1.0;
    for (const [val, w] of dims) {
      product *= (1.0 - _clamp01(val * w));
    }
    return _clamp01(1.0 - product);
  }
}

// ── Quality mapping ───────────────────────────────────────────────────

export const QUALITY_FROM_REGIME: Record<OsitRegime, RenderQuality> = {
  OPTIMO: "FULL",
  FUNCIONAL: "FULL",
  PRE_JAMMING: "DEGRADED",
  JAMMING_TEMPRANO: "MINIMAL",
  JAMMING: "HALT",
};

// ── RenderGateV2 ──────────────────────────────────────────────────────

export class RenderGateV2 {
  private frameBudgetMs: number;
  private frameTimeHistory: number[];
  private historyLen: number;
  rv: ResidueVectorImpl;
  private pendingActions = 0;
  private maxActions = 100;
  private ramBudgetGb = 6.0;
  private _prevROr = 0.0;
  private _rVel = 0.0;
  private _rAcc = 0.0;
  private _preJamming = false;

  constructor(frameBudgetMs = 16.67, historyLen = 30) {
    this.frameBudgetMs = frameBudgetMs;
    this.historyLen = historyLen;
    this.frameTimeHistory = [];
    this.rv = new ResidueVectorImpl();
  }

  get rVel(): number { return this._rVel; }
  get rAcc(): number { return this._rAcc; }
  get isPreJamming(): boolean { return this._preJamming; }

  /**
   * Update ResidueVector from real metrics, derive R_or, regime, quality.
   * Returns an object with: r_or, regime, epistemic, quality, allow_render, rv.
   */
  update(
    frameTimeMs: number,
    pendingActions = 0,
    ramUsedGb = 0.0,
    fidelityRatio = 1.0,
  ): RenderGateResult {
    this.frameTimeHistory.push(frameTimeMs);
    if (this.frameTimeHistory.length > this.historyLen) {
      this.frameTimeHistory.shift();
    }
    this.pendingActions = pendingActions;

    // r_lat: p85 frame time deviation from budget, normalized
    if (this.frameTimeHistory.length >= 5) {
      const sorted = [...this.frameTimeHistory].sort((a, b) => a - b);
      const p85 = sorted[Math.floor(sorted.length * 0.85)];
      this.rv.r_lat = _clamp01(
        (p85 - this.frameBudgetMs) / (this.frameBudgetMs * 3),
      );
    } else {
      this.rv.r_lat = 0.0;
    }

    // r_sem: fidelity drop (1.0 = full, 0.0 = nothing)
    this.rv.r_sem = _clamp01(1.0 - fidelityRatio);

    // r_act: action queue pressure
    this.rv.r_act = _clamp01(pendingActions / Math.max(1, this.maxActions));

    // r_cost: RAM over budget
    this.rv.r_cost = _clamp01(
      Math.max(0, ramUsedGb - this.ramBudgetGb) / 2.0,
    );

    const rOr = this.rv.rOr();
    const regime = regimeFromR(rOr) as OsitRegime;
    const epistemic = epistemicStateFromR(rOr) as EpistemicState;
    const quality = QUALITY_FROM_REGIME[regime];
    const allowRender = quality !== "HALT";

    // R_vel / R_acc: pre-jamming detection (§2.4)
    this._rVel = rOr - this._prevROr;
    if (this._rVel > 0) {
      this._rAcc += this._rVel;
    } else {
      this._rAcc = Math.max(0, this._rAcc * 0.9);
    }
    this._prevROr = rOr;
    this._preJamming = this._rVel > 0.05 && this._rAcc > 0;

    return {
      r_or: Math.round(rOr * 10_000) / 10_000,
      regime,
      epistemic,
      quality,
      allow_render: allowRender,
      r_vel: Math.round(this._rVel * 10_000) / 10_000,
      r_acc: Math.round(this._rAcc * 10_000) / 10_000,
      pre_jamming: this._preJamming,
      rv: this.rv,
    };
  }

  /** Backward-compatible check() — calls update() with defaults. */
  check(frameTimeMs: number): RenderGateResult {
    return this.update(frameTimeMs);
  }

  get currentR(): number {
    return this.rv.rOr();
  }

  get currentRegime(): OsitRegime {
    return regimeFromR(this.rv.rOr()) as OsitRegime;
  }

  get currentQuality(): RenderQuality {
    return QUALITY_FROM_REGIME[this.currentRegime];
  }
}

// ── EML unified gate (§2.5) ──────────────────────────────────────────

export type EmlAction = "ACCEPT" | "EXPAND" | "COMPRESS" | "BLOCK";

const EML_ALPHA = 2.2;
const EML_BETA = 0.65;
const EML_THETA = 0.1;

function _sigmoid(x: number): number {
  if (x >= 0) return 1.0 / (1.0 + Math.exp(-x));
  const ex = Math.exp(x);
  return ex / (1.0 + ex);
}

export function emlGate(
  s: number,
  c: number,
  alpha = EML_ALPHA,
  beta = EML_BETA,
  theta = EML_THETA,
): EmlAction {
  const raw = alpha * s - beta * Math.log(1.0 + c) - theta;
  const eml = _sigmoid(raw);
  if (eml >= 0.75) return "ACCEPT";
  if (eml >= 0.50) return "EXPAND";
  if (eml >= 0.25) return "COMPRESS";
  return "BLOCK";
}

// ── Falsifiers ────────────────────────────────────────────────────────

export const FALSIFIERS: Record<string, string> = {
  F_RG_01:
    "RenderGateV2.update(16.0) returns regime=OPTIMO, quality=FULL, allow_render=true",
  F_RG_02:
    "RenderGateV2.update(80.0) returns quality in (DEGRADED, MINIMAL, HALT)",
  F_RG_03: "RenderGateV2 rv.rOr() is in [0, 1] for any valid input",
  F_RG_04:
    "regimeFromR matches ositCanon.ts regimeFromR for boundary values 0.15, 0.30, 0.45, 0.60",
  F_RG_05:
    "Noisy-OR: new ResidueVectorImpl({r_lat:0.9}).rOr() >= 0.5 (critical dim dominates, old weighted avg gave 0.315)",
  F_RG_06:
    "Noisy-OR: all-zeros => 0, all-ones => 1.0",
  F_RG_07:
    "R_vel > 0.05 and R_acc > 0 triggers pre_jamming=true after sustained R increase",
  F_RG_08:
    "R_vel is 0 when R_or is stable across updates",
  F_RG_09:
    "epistemicStateFromR matches canon ratificado (reuse §2.4, 0.45/0.60): 0.14→CERTEZA, 0.20→INFERENCIA, 0.50→INCOGNITA, 0.85→BLOQUEADO",
  F_EML_01: "emlGate(1.0, 0) === 'ACCEPT' (high signal, zero cost)",
  F_EML_02: "emlGate(0, 100) === 'BLOCK' (zero signal, high cost)",
  F_EML_03: "emlGate returns in ('ACCEPT','EXPAND','COMPRESS','BLOCK') for any s,c >= 0",
};
