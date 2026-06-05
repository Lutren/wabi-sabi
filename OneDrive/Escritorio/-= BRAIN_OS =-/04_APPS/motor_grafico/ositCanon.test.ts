/**
 * ositCanon.test.ts — verifica que el shim canónico del motor gráfico concuerde con
 * obsai_core.metrics.estimate_regime. Requiere vitest en la app real (aquí, en staging,
 * no hay runner; la lógica se cross-verificó contra Python al crear el shim).
 *
 *   npx vitest run ositCanon.test.ts
 */
import { describe, it, expect } from "vitest";

import {
  GAME_EVENT_RESIDUE,
  GAME_EVENT_RESIDUE_DEFAULT,
  epistemicStateFromR,
  regimeFromR,
  sessionEndResidue,
} from "./ositCanon";

describe("regimeFromR (espejo de obsai estimate_regime, límites estrictos <)", () => {
  it("clasifica las bandas canónicas en los límites", () => {
    expect(regimeFromR(0.149)).toBe("OPTIMO");
    expect(regimeFromR(0.15)).toBe("FUNCIONAL");
    expect(regimeFromR(0.299)).toBe("FUNCIONAL");
    expect(regimeFromR(0.30)).toBe("PRE_JAMMING");
    expect(regimeFromR(0.449)).toBe("PRE_JAMMING");
    expect(regimeFromR(0.45)).toBe("JAMMING_TEMPRANO");
    expect(regimeFromR(0.599)).toBe("JAMMING_TEMPRANO");
    expect(regimeFromR(0.60)).toBe("JAMMING");
    expect(regimeFromR(1.0)).toBe("JAMMING");
  });

  it("satura entradas fuera de rango / no finitas", () => {
    expect(regimeFromR(-5)).toBe("OPTIMO");
    expect(regimeFromR(99)).toBe("JAMMING");
    expect(regimeFromR(Number.NaN)).toBe("OPTIMO");
  });
});

describe("epistemicStateFromR (puente canónico R -> 4 estados, §2.4 RATIFICADO 0.45/0.60)", () => {
  it("mapea cada banda al estado correcto (límites 0.15/0.45/0.60)", () => {
    expect(epistemicStateFromR(0.10)).toBe("CERTEZA");
    expect(epistemicStateFromR(0.149)).toBe("CERTEZA");
    expect(epistemicStateFromR(0.15)).toBe("INFERENCIA");
    expect(epistemicStateFromR(0.44)).toBe("INFERENCIA");
    expect(epistemicStateFromR(0.45)).toBe("INCOGNITA");
    expect(epistemicStateFromR(0.59)).toBe("INCOGNITA");
    expect(epistemicStateFromR(0.60)).toBe("BLOQUEADO");
    expect(epistemicStateFromR(1.0)).toBe("BLOQUEADO");
  });
});

describe("tabla de residuo por evento de juego", () => {
  const expected: Record<string, string> = {
    boss_killed: "CERTEZA",
    floor_cleared: "CERTEZA",
    level_up: "INFERENCIA",
    item_collected: "INFERENCIA",
    level_generated: "INFERENCIA",
    session_start: "INFERENCIA",
    player_death: "BLOQUEADO",
  };
  it("cada evento cae en su estado canónico documentado", () => {
    for (const [kind, state] of Object.entries(expected)) {
      expect(epistemicStateFromR(GAME_EVENT_RESIDUE[kind])).toBe(state);
    }
  });
  it("el default cae en INCOGNITA (banda JAMMING_TEMPRANO)", () => {
    expect(epistemicStateFromR(GAME_EVENT_RESIDUE_DEFAULT)).toBe("INCOGNITA");
  });
});

describe("sessionEndResidue", () => {
  it("muerte -> BLOQUEADO, HP crítico -> INCOGNITA, sano -> INFERENCIA", () => {
    expect(epistemicStateFromR(sessionEndResidue(0, 100))).toBe("BLOQUEADO");
    expect(epistemicStateFromR(sessionEndResidue(10, 100))).toBe("INCOGNITA");
    expect(epistemicStateFromR(sessionEndResidue(90, 100))).toBe("INFERENCIA");
  });
});
