# ASSUMPTIONS

- La primera corrida debe reducir R sin crear archivo frio ni vault paralelo.
- `ROOT_BRAIN_OS` es canon base vivo, pero necesita validacion de runtime externo a ZIP.
- Las rutas sucias se revisan por valor, no por extraccion profunda completa.
- Candidatos de limpieza requieren confirmacion humana futura con la frase exacta definida.
- `New project 3` es la superficie React/Vite disponible para alojar `/telecom`.
- Run 2 prioriza central local mock antes de backend real.
# Run 3 - supuestos operativos

- La app React disponible para `/telecom` sigue siendo `C:\Users\L-Tyr\OneDrive\Documentos\New project 3`.
- Run 3 prioriza estabilidad y trazabilidad sobre features visuales grandes.
- `localStorage` es aceptable solo como primera capa local; el siguiente paso debe ser JSONL/SQLite.
- MCP debe arrancar read-only y solo desde ledger validado.
- Listar el directorio central del ZIP no equivale a validar contenido ni a autorizar expansion.

# Run 4 - supuestos operativos

- El path canonico del ledger durable es `02_RUNTIME/messagebus/logs/messagebus-main.jsonl`.
- El navegador no escribe a disco; solo puede exportar archivos descargables.
- Los scripts Node-only pueden leer/escribir JSONL local porque corren fuera del cliente.
- Run 5 debe construir MCP read-only sobre el JSONL verificado, no sobre estado browser.

# Run 5 - supuestos operativos

- `@modelcontextprotocol/sdk` es aceptable para MCP local stdio porque el prompt Run 5 autorizo instalarlo si era seguro.
- MCP read-only debe operar solo sobre el ledger JSONL durable y handlers derivados.
- El navegador debe mostrar estado MCP, no conectarse al servidor MCP.
- `messagebus:mcp:smoke` es la prueba minima de salud para Run 6 antes de crear A2A local.
- Run 6 puede crear fixtures/simulaciones locales, pero no debe escribir al ledger principal ni abrir red publica.
