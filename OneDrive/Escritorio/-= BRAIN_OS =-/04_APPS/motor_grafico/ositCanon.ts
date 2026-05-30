/**
 * src/lib/game-engine/ositCanon.ts
 * MEDIOEVO — Constantes canónicas OSIT para el motor gráfico.
 *
 * FUENTE DE VERDAD (single source of truth):
 *   packages/open-dev/obsai-core/obsai_core/metrics.py  ->  estimate_regime()
 * Contrato de reuso:
 *   packages/open-dev/obsai-core/docs/OSIT_CANON_REUSE_CONTRACT_2026-05-29.md
 *
 * Estos umbrales están replicados a mano (sin dependencias, sin red) para que el
 * juego concuerde con wabisabi, duat y el firmware. Si cambian en Python, hay que
 * actualizarlos aquí. Calibración: DEMO_ONLY (no son claims de producto).
 */

// Estado epistémico OSIT de 4 niveles. Estructuralmente idéntico a
// EpistemicStateV2 de @/lib/studio/artifactRegistry (la asignación cruzada en
// gameEventBridge.ts actúa como guardia de sincronía en tiempo de compilación).
export type OsitEpistemicState = "CERTEZA" | "INFERENCIA" | "INCOGNITA" | "BLOQUEADO";

export type OsitRegime =
  | "OPTIMO"
  | "FUNCIONAL"
  | "PRE_JAMMING"
  | "JAMMING_TEMPRANO"
  | "JAMMING";

/** Escalera de régimen — espejo exacto de obsai_core.metrics.estimate_regime (límites estrictos `<`). */
export const OSIT_REGIME_R = {
  OPTIMO: 0.15,
  FUNCIONAL: 0.30,
  PRE_JAMMING: 0.45,
  JAMMING_TEMPRANO: 0.60,
} as const;

/**
 * Puente canónico R -> estado epistémico (4 estados). Ver §2.4 del contrato de reuso:
 *   R < 0.15            -> CERTEZA      (OPTIMO)
 *   0.15 <= R < 0.45    -> INFERENCIA   (FUNCIONAL / PRE_JAMMING)
 *   0.45 <= R < 0.60    -> INCOGNITA    (JAMMING_TEMPRANO)
 *   R >= 0.60           -> BLOQUEADO    (JAMMING)
 * Consistente con osit_firmware/uefi/osit_gates.c (R<=0.15 -> CERTEZA). DEMO_ONLY,
 * pendiente de ratificación de canon por L.R.
 */
export const OSIT_STATE_R = {
  CERTEZA_MAX: 0.15,
  INFERENCIA_MAX: 0.45,
  INCOGNITA_MAX: 0.60,
} as const;

export function clamp01(value: number): number {
  if (!Number.isFinite(value)) return 0;
  return Math.max(0, Math.min(1, value));
}

/** Régimen OSIT canónico para un residuo R en [0,1]. */
export function regimeFromR(R: number): OsitRegime {
  const r = clamp01(R);
  if (r < OSIT_REGIME_R.OPTIMO) return "OPTIMO";
  if (r < OSIT_REGIME_R.FUNCIONAL) return "FUNCIONAL";
  if (r < OSIT_REGIME_R.PRE_JAMMING) return "PRE_JAMMING";
  if (r < OSIT_REGIME_R.JAMMING_TEMPRANO) return "JAMMING_TEMPRANO";
  return "JAMMING";
}

/** Estado epistémico canónico para un residuo R en [0,1]. */
export function epistemicStateFromR(R: number): OsitEpistemicState {
  const r = clamp01(R);
  if (r < OSIT_STATE_R.CERTEZA_MAX) return "CERTEZA";
  if (r < OSIT_STATE_R.INFERENCIA_MAX) return "INFERENCIA";
  if (r < OSIT_STATE_R.INCOGNITA_MAX) return "INCOGNITA";
  return "BLOQUEADO";
}

/**
 * Residuo R por tipo de evento de juego. Centraliza los valores que antes estaban
 * ad-hoc en residueFor(). El comentario de banda indica el estado canónico resultante.
 */
export const GAME_EVENT_RESIDUE: Record<string, number> = {
  boss_killed: 0.08,      // OPTIMO       -> CERTEZA
  floor_cleared: 0.14,    // OPTIMO       -> CERTEZA
  level_up: 0.18,         // FUNCIONAL    -> INFERENCIA
  item_collected: 0.22,   // FUNCIONAL    -> INFERENCIA
  level_generated: 0.28,  // FUNCIONAL    -> INFERENCIA
  session_start: 0.32,    // PRE_JAMMING  -> INFERENCIA
  player_death: 0.87,     // JAMMING      -> BLOQUEADO
};

/** R por defecto para eventos no tabulados: banda JAMMING_TEMPRANO -> INCOGNITA. */
export const GAME_EVENT_RESIDUE_DEFAULT = 0.5;

/** Residuo de fin de sesión, derivado de HP en bandas canónicas. */
export function sessionEndResidue(finalHp: number, maxHp: number): number {
  if (finalHp <= 0) return 0.88;                 // muerte    -> JAMMING    -> BLOQUEADO
  if (finalHp < maxHp * 0.25) return 0.55;       // HP crítico -> JAMMING_TEMPRANO -> INCOGNITA
  return 0.25;                                   // sano      -> FUNCIONAL  -> INFERENCIA
}
