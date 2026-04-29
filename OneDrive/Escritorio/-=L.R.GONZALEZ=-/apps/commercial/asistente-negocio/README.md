# Asistente de Negocio MEDIOEVO

Producto publico reducido para CRM ligero, voz, avisos, respuestas de negocio, correo y WhatsApp real con aprobacion humana. La v1.0.0 usa una interfaz guiada con estetica MEDIOEVO/GEODIA y abre la app de correo del usuario o WhatsApp con el texto ya escrito; la persona pulsa Enviar en su propia app.

## Estado comercial

- Perfil: `public_safe`
- Modo de venta: `lead_first`
- Autonomia: `human_approved_external_send`
- Version: `1.0.0`
- Windows: `.exe` NSIS y ZIP portable con icono GEODIA.
- macOS: `.dmg` y `.app.zip` con icono GEODIA cuando exista build en macOS y notarizacion si se vende fuera de una tienda.

## Que hace la v1

- Pide datos del negocio y consentimiento en la primera ejecucion.
- Crea una respuesta sugerida para mensajes de clientes.
- Guarda un registro local de consentimiento y aprobaciones.
- Abre correo real por `mailto:` despues de aprobar.
- Abre WhatsApp real por `wa.me` despues de aprobar.
- Dicta mensajes con voz cuando el equipo lo soporta.
- Lee respuestas con voz.
- Avisa cuando detecta un mensaje nuevo copiado al portapapeles.
- Responde preguntas comunes usando precios, horarios, pagos y notas del negocio.
- Usa un flujo visual de tres pasos con assets MEDIOEVO reales para usuarios no tecnicos.
- Incluye barra superior con instrucciones, tutorial, saltos de paso, prueba y modo compacto.
- Permite descargar respaldo local de datos.
- Permite borrar datos locales desde la app.

## Que no incluye

- No usa WhatsApp Web.
- No usa cookies del navegador.
- No incluye agentes con shell.
- No incluye tokens, `.env`, llaves privadas ni rutas internas de la maquina del operador.
- No automatiza pagos, sesiones o paneles de terceros.
- No envia nada solo; el envio final ocurre en la app del usuario.

## Comandos

```powershell
npm install
npm run check
npm run preview
npm run dev
npm run build:win
npm run package:final
```

```bash
npm install
npm run check
npm run build:mac
```

El build de macOS debe ejecutarse en macOS para producir `.dmg`/`.app.zip` y notarizar.
