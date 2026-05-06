# Commercial Release Legal Matrix

Fecha: 2026-05-01

Estado: `DRAFT_GATED / LEGAL_REVIEW_REQUIRED`.

Este documento no es asesoria legal y no autoriza venta, publicacion, Gumroad,
deploy ni release externo. Su funcion es dejar el carril comercial ordenado para
revision humana/legal.

## Documentos Base

| Documento | Estado | Uso |
|---|---|---|
| `TERMS_DRAFT.md` | draft gated | terminos generales de compra/uso |
| `REFUND_POLICY_DRAFT.md` | draft gated | politica de reembolso digital |
| `PRIVACY_POLICY_DRAFT.md` | draft gated | privacidad y datos por producto |
| `CUSTOMER_SUPPORT_PLAN.md` | draft gated | canales, tiempos de soporte y correo provisional |
| `apps\commercial\*\COMMERCIAL_LICENSE.md` | draft gated | licencia propietaria por app |
| `docs\product\paid-app-deliverable-boundary-2026-05-01.md` | draft gated | separa source ZIP interno de entregable cliente |

## Matriz Por Producto

| Producto | Licencia | Privacy | Refund | Terms | Support | Estado |
|---|---|---|---|---|---|---|
| Argus Desktop | app license draft | root draft | root draft | root draft | support plan draft | `REVIEW` |
| Asistente Negocio | app license draft | root draft | root draft | root draft | support plan draft | `REVIEW` |
| FlujoCRM | app license draft | root draft | root draft | root draft | support plan draft | `REVIEW` |
| Mini Office | app license draft | root draft | root draft | root draft | support plan draft | `REVIEW` |
| Wave FC / Wabi-Sabi | no final app EULA | root draft | root draft | root draft | support plan draft | `LOCAL_DEMO_READY / LEGAL_BLOCK` |

## Frontera Comercial

- La compra de productos publicos no incluye IP privada, RPG, lore no publicado,
  secretos, datos familiares, repos privados ni codigo fuente comercial salvo
  que una oferta final lo diga explicitamente.
- Los productos se deben vender con claims bajos y verificables. No prometer
  seguridad garantizada, eliminacion de errores, resultados medicos,
  financieros o laborales garantizados.
- Las herramientas locales pueden procesar archivos del usuario solo cuando el
  flujo del producto lo requiere y debe explicarse en la politica de privacidad
  final.
- Soporte no debe pedir ni aceptar secretos, tokens, claves privadas, documentos
  sensibles innecesarios ni datos del RPG privado.

## Bloqueos Antes De Venta

- Revisar jurisdiccion, impuestos, plataforma de pago y datos fiscales.
- Confirmar si `medioevo.saga@gmail.com` queda como inbox comercial o si se crea
  un alias de dominio dedicado.
- Definir ventana y excepciones de reembolso por plataforma.
- Revisar privacidad por app: telemetria, logs, archivos locales, backups y
  retencion.
- Agregar aviso de instalador unsigned o code signing por app.
- Alinear cada listing con el entregable real: source ZIP, instalador, demo o
  servicio.
