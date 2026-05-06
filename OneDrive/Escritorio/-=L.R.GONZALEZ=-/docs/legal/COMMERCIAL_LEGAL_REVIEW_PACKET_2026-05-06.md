# Commercial Legal Review Packet - 2026-05-06

Estado: `LOCAL_REVIEW_PACKET_READY / LEGAL_REVIEW_REQUIRED`

Este documento no es asesoria legal, fiscal ni contable. Su funcion es reunir
la evidencia comercial actual y convertir los bloqueos legales en preguntas y
criterios verificables para revision del operador y, cuando aplique, de un
profesional.

No se ejecuto venta, checkout, cambio de pagos, modificacion de impuestos,
subida a Gumroad, publicacion legal, firma, registro de marca, registro de obra,
formulario gubernamental ni cambio de cuenta.

## Resumen Ejecutivo

| area | estado actual | decision operativa |
|---|---|---|
| Productos ya publicados en Gumroad | Agent Ops Pack y DUAT Templates verificados | se pueden mantener vivos con copy low-claim; media opcional |
| FlujoCRM | founder access local con QA actual | no crear checkout publico hasta clean-machine/legal/hash final |
| Asistente Negocio | QA local y paquete Windows previamente verificados | no ampliar venta sin clean-machine/legal/signing decision |
| Mini Office | local smoke QA / founder-access review | no vender hasta legal, clean-machine, manifest y checkout |
| Wave FC / Wabi-Sabi | demo local con datos sinteticos | no publicacion amplia hasta QA visual DOCX, EULA/legal y ActionGate |
| Argus Desktop | build/typecheck local historico | no vender sin UX/public-safe/legal/package review |
| Legal/tax/payment | cola manual activa | no marcar cierre sin evidencia externa no secreta |

## Evidencia Actual

| evidencia | lectura |
|---|---|
| `docs/legal/COMMERCIAL_RELEASE_LEGAL_MATRIX_2026-05-01.md` | matriz base en `DRAFT_GATED / LEGAL_REVIEW_REQUIRED` |
| `docs/legal/LEGAL_OWNER_MANUAL_QUEUE_2026-05-06.md` | cola manual para IMPI, SAT, INDAUTOR, KDP, terminos, privacidad y marcas |
| `docs/product/flujocrm-release-evidence-2026-05-02.md` | FlujoCRM QA current-user, SQLite E2E y uninstall; checkout bloqueado |
| `docs/WAVE_FC_EVIDENCE_PACK_2026-05-01.md` | Wave FC demo local listo; publicacion bloqueada por QA visual/legal/ActionGate |
| `apps/commercial/mini-office/README.md` | Mini Office smoke local; venta bloqueada por legal/clean-machine/manifest/support |
| `docs/pending/REMAINING_GATED_WORKPACK_2026-05-06.md` | gates restantes packetados por target |

## Preguntas Para Revision Legal/Comercial

### 1. Entregable Y Licencia

- Para cada producto, confirmar si el cliente recibe instalador, ZIP fuente,
  plantillas, servicio de soporte, demo o acceso founder.
- Confirmar si el codigo fuente comercial se entrega o se mantiene interno.
- Confirmar si la licencia actual por app cubre uso comercial, redistribucion,
  backups, numero de equipos y transferencia.
- Confirmar si debe existir EULA separada para FlujoCRM, Asistente Negocio,
  Mini Office, Argus y Wave FC.

### 2. Privacidad Y Datos

- Confirmar que cada producto declara si guarda datos localmente, en SQLite,
  browser storage o archivos del usuario.
- Confirmar si hay telemetria, logs, backups, crash reports o integraciones
  externas.
- Confirmar politica para soporte: no pedir secretos, tokens, claves privadas,
  datos fiscales, datos de clientes innecesarios ni material privado del RPG.
- Confirmar tiempo de retencion de mensajes de soporte y adjuntos.

### 3. Reembolsos Y Soporte

- Confirmar ventana de reembolso para productos digitales y excepciones por
  archivo inaccesible, descripcion incorrecta o incompatibilidad tecnica.
- Confirmar limites de soporte: instalacion, acceso al archivo, bugs
  reproducibles, pero no resultados de negocio garantizados.
- Confirmar canal oficial de soporte y si se usara un alias de dominio o correo
  actual.

### 4. Claims Y Riesgo Publicitario

- Mantener fuera de copy: seguridad garantizada, autonomia segura garantizada,
  prediccion social, diagnostico, resultado financiero, validacion cientifica o
  promesas de productividad absoluta.
- Usar copy de bajo claim: local-first, plantillas, evidencia, checklists,
  demos sinteticos, revision humana y limites claros.
- Para DUAT/Wave/Observacionismo, confirmar siempre `synthetic`, `research`,
  `demo`, `falsifier` o `human review` segun corresponda.

### 5. Instaladores, Firma Y Maquina Limpia

- Confirmar si se vendera instalador unsigned con aviso explicito o si se
  esperara code signing.
- Ejecutar clean-machine o clean-profile QA por producto antes de checkout.
- Registrar hash final del instalador/ZIP despues de cualquier rebuild.
- Confirmar uninstall, datos persistentes y carpeta de usuario.

### 6. Pagos, Impuestos Y Plataforma

- No guardar aqui RFC, e.firma, W-8BEN, cuentas bancarias, datos fiscales ni
  secretos.
- Confirmar quien es merchant of record por plataforma y que obligaciones quedan
  fuera de la plataforma.
- Confirmar si Gumroad, GitHub Sponsors, KDP y otros canales requieren textos
  legales distintos.

## Criterio De Promocion Por Producto

| producto | puede seguir como | no promover a |
|---|---|---|
| Agent Ops Pack | Gumroad live low-claim | bundle con runtime privado o safety guarantee |
| DUAT Templates | Gumroad live synthetic templates | DUAT Geodia privado, prediction engine o ciencia validada |
| FlujoCRM | founder/pilot access manual | checkout publico sin clean-machine/legal/hash final |
| Asistente Negocio | founder/pilot access manual | venta amplia sin clean-machine/legal/signing decision |
| Mini Office | local/founder review | venta o repo publico sin gates comerciales |
| Wave FC | demo privada sintetica | publicacion amplia sin DOCX visual QA/EULA/listing |
| Argus Desktop | internal/local demo | venta sin UX/legal/package review |

## Gate De Cierre Legal

Cada producto necesita evidencia antes de cambiar a `BUY_NOW` o publicacion
amplia:

| gate | required evidence |
|---|---|
| licencia/EULA | texto aprobado por operador/legal |
| terminos | texto aprobado por operador/legal |
| privacidad | texto aprobado por operador/legal |
| refund/support | politica aprobada por operador/legal |
| claims scan | sin promesas fuertes ni claims bloqueados |
| clean-machine o clean-profile QA | evidencia de instalacion/uso/desinstalacion |
| artifact hash final | SHA256 despues del ultimo rebuild |
| secret scan de fuente y artifact | `count_reported=0` |
| listing/page | coincide con el entregable real |
| ActionGate target-specific | decision registrada para el target exacto |
| verificacion publica o de entrega | URL, screenshot, API o prueba de descarga posterior |

## Frontera

Este paquete habilita preparacion y revision. No habilita:

- publicar politicas legales;
- cambiar cuentas de pago;
- subir productos nuevos;
- abrir checkout nuevo;
- prometer cumplimiento fiscal o legal;
- registrar marcas u obras;
- almacenar documentos fiscales;
- vender productos bloqueados por clean-machine o legal.
