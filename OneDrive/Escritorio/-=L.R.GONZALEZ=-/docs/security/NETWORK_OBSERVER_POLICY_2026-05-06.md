# Network Observer Policy - 2026-05-06

Status: `DEFENSIVE_POLICY / STEALTH_BLOCKED`

## Fuente Analizada

El fragmento recibido se presenta como un escaner "stealth" o SYN scan con
Scapy. La lectura tecnica es distinta:

- importa `scapy`;
- crea paquetes `ARP` y `Ether`;
- usa broadcast `ff:ff:ff:ff:ff:ff`;
- llama `srp(...)`;
- apunta a `192.168.1.1/24`.

Eso es descubrimiento ARP de red local. No es una observacion pasiva pura y no
es una capacidad que Claudio deba ejecutar autonomamente.

## Decision

| componente | decision | razon |
|---|---|---|
| "stealth", evasion o intrusion | `BLOCK` | convierte seguridad defensiva en comportamiento ambiguo/ofensivo |
| Scapy/raw packets/ARP/SYN/broadcast | `BLOCK` | envia trafico y puede alterar el entorno observado |
| CIDR o LAN discovery | `BLOCK` por defecto | requiere scope de mantenimiento y autorizacion explicita |
| inventario local `127.0.0.1` | `APPROVE` si es read-only | observa servicios locales sin tocar terceros |
| reporte public-safe | `REVIEW` | no debe exponer IP/MAC/topologia privada |

## Aplicacion A Claudio

Se integra como contrato de seguridad, no como scanner:

- `tools/security_network_observer.py` clasifica requests de observacion de red
  sin enviar paquetes.
- `library/modules/network_observer_defensive.json` permite que Wabi-Sabi cargue
  este criterio solo cuando el usuario o un agente proponga red/puertos/scans.
- `SecurityAgent` puede consumir el output como `ObservationEnvelope`.
- Conway/Hormiguero puede recibir senal `security.blocked_network_probe`.

## Regla Operativa

Claudio no ejecuta descubrimiento de red sigiloso. La forma fundamental y segura
es:

1. observar intencion;
2. detectar scope;
3. bloquear raw packets, stealth y CIDR;
4. permitir solo estado local/loopback read-only;
5. registrar evidencia y falsadores.

## Falsadores

La politica falla si ocurre cualquiera de estos eventos:

- el runtime importa Scapy para escaneo;
- se emite ARP, SYN o broadcast;
- se escanea una LAN/CIDR o host no-loopback;
- se publica un inventario de IP/MAC/topologia privada;
- se presenta "sigilo" como feature valida del agente.

## Prompt Para Otras IA

Usa este prompt para recolectar informacion sin pedir codigo ofensivo:

```text
Actua como auditor defensivo de seguridad local. Analiza el siguiente fragmento
solo para extraer patrones de riesgo y controles defensivos. No propongas codigo
de escaneo, evasion, intrusiones, bypass ni stealth. Entrega:
1. que hace realmente el codigo;
2. que claims son incorrectos o exagerados;
3. riesgos operativos;
4. como convertirlo en un contrato local read-only;
5. ActionGate APPROVE/REVIEW/BLOCK;
6. falsadores;
7. pruebas unitarias seguras sin trafico de red.
```
