# Matrix Security Model

Estado: `SECURITY_MODEL / ACTIONGATE_FIRST`.

## Bloqueos duros

- No entrenar modelos.
- No descargar internet sin gate.
- No cargar todo el canon.
- No publicar libros/canon privado.
- No mezclar CEREBRO privado con open-dev.
- No crear agente autonomo sin gates.
- No borrar, mover o publicar sin evidencia, rollback y ActionGate.

## Reglas de seguridad

| riesgo | decision |
|---|---|
| secretos, `.env`, tokens, claves | `BLOCK` |
| publicacion externa | `BLOCK` hasta gate especifico |
| claims medicos, fisicos o sociales fuertes | `BLOCK` |
| lectura privada necesaria | `REVIEW` |
| escritura local acotada | `REVIEW` salvo runtime permitido |
| docs public-safe | `APPROVE` si secret scan pasa |
| stealth, evasion, raw packets, ARP/SYN o CIDR discovery | `BLOCK` |
| inventario local loopback read-only | `APPROVE` si no expone IP/MAC/topologia privada |

## Frontera publica/privada

Los modulos pueden describir estructura, schemas y ejemplos sinteticos. No
pueden transportar runtime privado, prompts internos, datasets, assets RPG/TCG,
libros completos ni arquitectura sensible.

## Seguridad por diseno

La biblioteca reduce riesgo al no cargar material innecesario. Menos contexto
significa menor filtracion, menos ruido y menos drift.

## Observacion De Red

Matrix puede cargar `network_observer_defensive` cuando un agente proponga red,
puertos, firewall o descubrimiento de dispositivos. Ese modulo no ejecuta
trafico. Solo clasifica la solicitud, bloquea stealth/raw packets/LAN discovery
y permite inventario local `127.0.0.1` read-only con WitnessLog.
