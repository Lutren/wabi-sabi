# Politica Public Safe

El Asistente de Negocio MEDIOEVO publico se vende como herramienta de borrador, aprobacion y apertura de canales reales, no como operador autonomo.

## Reglas de salida publica

- Cada integracion debe tener consentimiento explicito.
- Cada mensaje saliente debe pasar por una accion humana de aprobacion.
- El usuario debe poder revisar, copiar, editar o descartar el borrador antes de enviarlo.
- La beta puede abrir `mailto:` o `wa.me` con el mensaje aprobado. El envio final ocurre fuera de la app, en el cliente de correo o WhatsApp del usuario.
- Los logs publicos solo guardan eventos minimos de consentimiento y aprobacion local.
- Las credenciales se conectaran por OAuth o proveedor oficial, no por tokens pegados.
- La app publica debe ofrecer respaldo local y borrado local de datos.

## WhatsApp

La version publica solo puede usar WhatsApp Business Platform / Cloud API con opt-in, numero dedicado, politica de privacidad y plantillas aprobadas cuando apliquen.

WhatsApp Web, Playwright, cookies de navegador y sesiones locales quedan en `local_unrestricted`.

## Correo

Correo publico debe usar OAuth de Gmail o Microsoft Graph con scopes minimos, o un proveedor transaccional verificado como Resend. El envio automatico sin aprobacion queda fuera de la v1 publica.

## Bloqueado en publico

- Shell local o agentes con permisos amplios.
- Automatizacion de escritorio.
- Automatizacion de pagos o paneles de tienda.
- Scraping o APIs privadas.
- Secretos embebidos en paquetes.
