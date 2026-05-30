/**
 * src/lib/game-engine/gameEventBridge.ts
 * MEDIOEVO — Puente Engine ↔ Studio (Turno 2)
 *
 * Registra eventos del juego como artefactos OSIT en el ArtifactStore.
 * Uso en GameMode.tsx:
 *
 *   import { recordGameEvent } from "@/lib/game-engine/gameEventBridge";
 *   // cuando boss muere:
 *   await recordGameEvent({ kind: "boss_killed", mode: "iso", level: levelMeta.name, payload: { kills, gold } });
 *
 * Los artefactos aparecen en StudioShell → FileExplorer con tag "game".
 * Sin deps extra — usa createV2 del artifactRegistry existente.
 */

import {
  createV2,
  listAllV2,
  type ArtifactV2,
  type EpistemicStateV2,
} from "@/lib/studio/artifactRegistry";
import {
  epistemicStateFromR,
  GAME_EVENT_RESIDUE,
  GAME_EVENT_RESIDUE_DEFAULT,
  sessionEndResidue,
  type OsitEpistemicState,
} from "./ositCanon";

// ─── TIPOS DE EVENTO ──────────────────────────────────────────────────────────
export type GameEventKind =
  | "level_generated"   // NVIDIA generó un nivel nuevo
  | "floor_cleared"     // Todos los enemigos eliminados
  | "boss_killed"       // Boss principal derrotado
  | "player_death"      // Jugador eliminado
  | "item_collected"    // Ítem recogido (cofre, poción rara)
  | "level_up"          // Personaje subió de nivel
  | "session_start"     // Sesión de juego iniciada
  | "session_end";      // Sesión de juego terminada

export type GameEventMode = "iso" | "metro";

export interface GameEvent {
  kind: GameEventKind;
  mode: GameEventMode;
  level: string;       // Nombre del nivel
  floor?: number;
  payload: Record<string, unknown>;
}

export interface GameSession {
  id: string;
  mode: GameEventMode;
  startedAt: string;
  events: (GameEvent & { ts: string })[];
  finalHp: number;
  finalKills: number;
  finalGold: number;
  osit: {
    state: EpistemicStateV2;
    R: number;
  };
}

// ─── COLA EN MEMORIA ─────────────────────────────────────────────────────────
let _sessionId = crypto.randomUUID().slice(0, 8);
let _eventQueue: (GameEvent & { ts: string })[] = [];

export function startGameSession(mode: GameEventMode): void {
  _sessionId = crypto.randomUUID().slice(0, 8);
  _eventQueue = [];
  // fire-and-forget
  void recordGameEvent({ kind: "session_start", mode, level: "—", payload: {} });
}

// ─── CLASIFICADOR OSIT (canónico) ───────────────────────────────────────────────
// El estado epistémico se deriva del residuo R con el puente canónico de ositCanon
// (espejo de obsai_core.metrics). Antes era un switch ad-hoc por tipo de evento.
function epistemicFor(event: GameEvent): OsitEpistemicState {
  return epistemicStateFromR(residueFor(event));
}

// Residuo R por evento, leído de la tabla canónica compartida (ositCanon).
function residueFor(event: GameEvent): number {
  if (event.kind === "session_end") {
    const hp = (event.payload["finalHp"] as number) ?? 100;
    const max = (event.payload["maxHp"] as number) ?? 100;
    return sessionEndResidue(hp, max);
  }
  return GAME_EVENT_RESIDUE[event.kind] ?? GAME_EVENT_RESIDUE_DEFAULT;
}

// ─── REGISTRADOR PRINCIPAL ────────────────────────────────────────────────────
/**
 * Graba un evento de juego como artefacto OSIT en el studio store.
 * Fire-and-forget seguro: nunca lanza hacia el game loop.
 */
export async function recordGameEvent(event: GameEvent): Promise<void> {
  const ts = new Date().toISOString();
  const state = epistemicFor(event);
  const R = residueFor(event);

  _eventQueue.push({ ...event, ts });

  const content = JSON.stringify(
    {
      _schema: "game_event_v1",
      session: _sessionId,
      ts,
      osit: { state, R },
      event: {
        kind: event.kind,
        mode: event.mode,
        level: event.level,
        floor: event.floor ?? 1,
      },
      payload: event.payload,
    },
    null,
    2,
  );

  const label = LABELS[event.kind] ?? event.kind;

  try {
    await createV2({
      name: `[${event.mode.toUpperCase()}] ${label} · ${event.level}`,
      type: "osit",
      content,
      source: "generated",
      tags: ["game", event.mode, event.kind, `session:${_sessionId}`],
      falsifier: `nivel verificable: ${event.level} · modo: ${event.mode} · ts: ${ts}`,
    });
  } catch {
    // Never crash the game loop on store failure
  }
}

const LABELS: Record<GameEventKind, string> = {
  level_generated: "Nivel generado (IA)",
  floor_cleared:   "Piso despejado",
  boss_killed:     "Boss eliminado",
  player_death:    "Jugador eliminado",
  item_collected:  "Ítem recogido",
  level_up:        "Subida de nivel",
  session_start:   "Sesión iniciada",
  session_end:     "Sesión finalizada",
};

// ─── CERRAR SESIÓN ────────────────────────────────────────────────────────────
export async function endGameSession(finalStats: {
  finalHp: number; maxHp: number; kills: number; gold: number; mode: GameEventMode;
}): Promise<void> {
  await recordGameEvent({
    kind: "session_end",
    mode: finalStats.mode,
    level: "resumen de sesión",
    payload: {
      finalHp: finalStats.finalHp,
      maxHp: finalStats.maxHp,
      kills: finalStats.kills,
      gold: finalStats.gold,
      eventCount: _eventQueue.length,
      sessionId: _sessionId,
    },
  });
}

// ─── CONSULTAR EVENTOS DE JUEGO DEL STORE ────────────────────────────────────
export async function listGameArtifacts(): Promise<ArtifactV2[]> {
  try {
    const all = await listAllV2();
    return all
      .filter(a => a.tags.includes("game"))
      .sort((a, b) => b.createdAt.localeCompare(a.createdAt));
  } catch {
    return [];
  }
}

export async function listGameArtifactsByMode(mode: GameEventMode): Promise<ArtifactV2[]> {
  const all = await listGameArtifacts();
  return all.filter(a => a.tags.includes(mode));
}

// ─── ESTADÍSTICAS OSIT AGREGADAS ─────────────────────────────────────────────
export interface GameOSITSummary {
  totalEvents: number;
  bossKills: number;
  deaths: number;
  levelsGenerated: number;
  globalR: number;
  globalState: EpistemicStateV2;
}

export async function computeGameOSITSummary(): Promise<GameOSITSummary> {
  const events = await listGameArtifacts();
  const bossKills    = events.filter(e => e.tags.includes("boss_killed")).length;
  const deaths       = events.filter(e => e.tags.includes("player_death")).length;
  const levelsGen    = events.filter(e => e.tags.includes("level_generated")).length;
  const totalEvents  = events.length;

  // Weighted R: deaths pull up, boss kills pull down
  const base = 0.3;
  const R = Math.min(
    1,
    Math.max(0, base + deaths * 0.12 - bossKills * 0.08 + (levelsGen > 0 ? -0.05 : 0)),
  );

  // Bandas canónicas OSIT (ositCanon) en lugar de los cortes ad-hoc 0.3/0.55/0.8.
  const globalState: EpistemicStateV2 = epistemicStateFromR(R);

  return { totalEvents, bossKills, deaths, levelsGenerated: levelsGen, globalR: parseFloat(R.toFixed(2)), globalState };
}
