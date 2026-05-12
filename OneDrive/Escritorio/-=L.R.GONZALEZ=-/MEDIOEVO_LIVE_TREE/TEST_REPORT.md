# TEST_REPORT

## Comandos ejecutados

- `python tools/live_tree_scan.py`
- `python tools/secret_scan.py`
- Verificacion PowerShell de artefactos requeridos: `MISSING_COUNT=0`

## Resultado

- Inventario vivo: `2592` registros.
- Secret scan: `2601` archivos candidatos escaneados, `475` hallazgos enmascarados.
- Artefactos obligatorios verificados: `18/18`.

## Estado

PASSED para generacion de artefactos locales.

BLOCK para publicacion/push/deploy por hallazgos de secret scan.

## Run 2 - DUAT Telecom Core

- `npm test -- --runInBand`: `FAILED_EXPECTED`; Vitest 2.1.9 no reconoce esa bandera.
- `npm run build`: `PASSED` en `C:\Users\L-Tyr\OneDrive\Documentos\New project 3`.
- `npm test`: `PASSED`, 2 test files, 15 tests.
- `python -m compileall -q .`: `PASSED` en `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: `NOT_APPLICABLE`; no se detecto suite Python `test_*.py` / `*_test.py`.
- `Start-Process npm.cmd run dev -- --port 5174`: `PASSED_LOCAL`; Vite sirve la app nueva.
- `Invoke-WebRequest http://127.0.0.1:5174/telecom`: `PASSED_LOCAL`; root de Vite servido.
- `Invoke-WebRequest http://127.0.0.1:5174/src/App.tsx`: `PASSED_LOCAL`; contiene `TelecomCore` y `/telecom`.
- `Invoke-WebRequest http://127.0.0.1:5174/src/ui/TelecomCore.tsx`: `PASSED_LOCAL`; contiene paneles clave del Telecom Core.

Reporte detallado: `10_QUALITY/TELECOM_CORE_TEST_REPORT.md`.

## Run 3 - MessageBus Validator / Append-only Core

- `npm test -- src/messagebus`: `PASSED`, 5 test files, 15 tests.
- `npx tsc -b --pretty false`: `PASSED`.
- `npm run build`: `PASSED`, 1600 modules transformed.
- `npm test`: `PASSED`, 6 test files, 26 tests.
- `python -m compileall -q .`: `PASSED` en `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: `NOT_APPLICABLE`; no se detecto suite Python `test_*.py` / `*_test.py`.
- `Invoke-WebRequest http://127.0.0.1:5174/telecom`: `PASSED_LOCAL`.
- `Invoke-WebRequest http://127.0.0.1:5174/src/ui/TelecomCore.tsx`: `PASSED_LOCAL`; contiene `MessageBus Health`, `Validate Log` y `Export JSONL`.
- Canon ZIP SHA256: `PASSED_MATCH`; no se extrajo contenido.

Reportes detallados:

- `10_QUALITY/MESSAGEBUS_VALIDATOR_TEST_REPORT.md`
- `10_QUALITY/MESSAGEBUS_HASHCHAIN_REPORT.md`
- `10_QUALITY/MESSAGEBUS_APPEND_ONLY_REPORT.md`
- `10_QUALITY/MESSAGEBUS_MCP_READONLY_PLAN_STATUS.md`
- `10_QUALITY/CANON_ZIP_SECURITY_REVIEW_STATUS.md`

## Run 4 - Durable MessageBus JSONL + Replay Verifier

- `npm test -- src/messagebus`: `PASSED`, 6 test files, 24 tests.
- `npx tsc -b --pretty false`: `PASSED`.
- `npm run build`: `PASSED`, 1600 modules transformed.
- `npm test`: `PASSED`, 7 test files, 35 tests.
- `npm run messagebus:append-sample`: `PASSED`.
- `npm run messagebus:verify`: `PASSED`, `ok=true`, `totalEntries=1`.
- `npm run messagebus:replay`: `PASSED`, `totalEntries=1`.
- `npm run messagebus:stats`: `PASSED`, `fileSizeBytes=2883`.
- `npm run messagebus:export-md`: `PASSED`.
- `python -m compileall -q .`: `PASSED` en `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: `NOT_APPLICABLE`; no se detecto suite Python.
- `/telecom`: `PASSED_LOCAL`.

Reporte detallado: `10_QUALITY/MESSAGEBUS_DURABLE_TEST_REPORT.md`.

## Run 5 - MessageBus MCP Read-only Server

- `npm install @modelcontextprotocol/sdk`: `PASSED`; SDK 1.29.0 instalado.
- `npm test -- src/messagebus`: `PASSED`, 7 test files, 37 tests.
- `npm test`: `PASSED`, 8 test files, 48 tests.
- `npx tsc -b --pretty false`: `PASSED`.
- `npm run build`: `PASSED`, 1600 modules transformed.
- `npm run messagebus:mcp:smoke`: `PASSED`, `ok=true`, resources 7, tools 8.
- MCP server factory import: `PASSED`, `hasConnect=true`.
- `python -m compileall -q .`: `PASSED` en `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: `NOT_APPLICABLE`; no se detecto suite Python.
- `/telecom`: `PASSED_LOCAL`, HTTP 200.
- `TelecomCore.tsx`: `PASSED_LOCAL`; contiene `MCP Read-Only Layer` y no contiene SDK MCP ni Node-only imports.
- `npm audit --omit=dev --json`: `PASSED`, 0 prod vulnerabilities.
- `npm audit --json`: `REVIEW`, 5 moderate dev vulnerabilities in Vite/Vitest/esbuild chain.

Reporte detallado: `10_QUALITY/MESSAGEBUS_MCP_READONLY_TEST_REPORT.md`.

## Run 6 - Agent Bridge / A2A local adapter

- `npm test -- src/messagebus`: `PASSED`, 8 test files, 51 tests.
- `npm test`: `PASSED`, 9 test files, 62 tests.
- `npx tsc -b --pretty false`: `PASSED`.
- `npm run build`: `PASSED`, 1600 modules transformed.
- `npm run messagebus:mcp:smoke`: `PASSED`, `ok=true`, resources 7, tools 8.
- `npm run agents:bridge:smoke`: `PASSED`, `ok=true`, agents 6.
- `python -m compileall -q .`: `PASSED` en `MEDIOEVO_LIVE_TREE`.
- `pytest -q`: `NOT_APPLICABLE`; no se detecto suite Python.
- `/telecom`: `PASSED_LOCAL`, HTTP 200.
- `TelecomCore.tsx`: `PASSED_LOCAL`; contiene `Agent Bridge / Local A2A Layer` y no contiene SDK MCP ni Node-only imports.
- `npm audit --omit=dev --json`: `PASSED`, 0 prod vulnerabilities.
- `npm audit --json`: `REVIEW`, 5 moderate dev vulnerabilities in Vite/Vitest/esbuild chain.

Reporte detallado: `10_QUALITY/AGENT_BRIDGE_RUN_6_TEST_REPORT.md`.
