# Matrix MVP Plan

Estado: `MVP_PLAN / DOCUMENTED`.

## Objetivo

Construir una biblioteca que Wabi-Sabi pueda consultar por demanda sin cargar
todo el canon. El MVP termina cuando existen docs, index, 10 modulos y
validador local.

## Fases

1. Inventario real de piezas existentes.
2. Schema y protocolos.
3. Diez modulos semilla.
4. Validador de index/modulos/dependencias/safety.
5. Handoff a Mission Control/COMMS.

## No entra al MVP

- entrenamiento de pesos;
- internet;
- runtime autonomo;
- publicacion;
- importacion de CEREBRO privado;
- UI nueva;
- base vectorial grande.

## Siguiente paso

Conectar lectura read-only a Mission Control:

- `GET /api/local/matrix/status`;
- `GET /api/local/matrix/modules`;
- `GET /api/local/matrix/modules/<id>`;
- `POST /api/local/matrix/retrieve` con gate `REVIEW`.
