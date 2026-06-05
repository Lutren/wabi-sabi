import { defineConfig } from "vitest/config";

// Host mínimo del motor gráfico: corre SOLO los contratos del shim OSIT (ositCanon.test.ts),
// que no dependen del app React (los archivos con imports `@/lib/...` no se recolectan).
export default defineConfig({
  test: {
    include: ["ositCanon.test.ts"],
    environment: "node",
  },
});
