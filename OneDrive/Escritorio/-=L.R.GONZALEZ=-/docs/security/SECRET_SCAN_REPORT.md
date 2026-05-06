# SECRET_SCAN_REPORT

Fecha: 2026-04-29

Metodo: escaneo no destructivo por nombres de archivo sensibles y conteo de coincidencias de patrones. No se copiaron valores de secretos en este reporte.

## Resultado ejecutivo

Estado: **NO APTO PARA PUBLICACION DIRECTA**.

Hay archivos con nombres y ubicaciones compatibles con secretos reales. Algunos estan ignorados por Git, pero siguen presentes en el workspace y pueden entrar en ZIPs o paquetes si no existe denylist.

## Actualizacion Fase 5

Se creo `tools/release/scan_secrets.py` y se ejecuto una pasada no destructiva:

```powershell
python tools\release\scan_secrets.py
```

Resultado: `reported findings: 200`. El script no imprime valores de secretos,
solo rutas y razones. El escaneo excluye por defecto `_archive`, `_ARCHIVAR`,
`.git`, `node_modules`, `.venv`, caches, builds, vendors y rutas privadas
denegadas. Sigue bloqueada cualquier publicacion hasta revisar o excluir los
hallazgos.

## Archivos sensibles detectados por nombre

| ruta | estado inicial | accion |
|---|---|---|
| `-=MEDIOEVO=-\-=LIBROS\.discord_token` | token probable; `git check-ignore` lo ignora | no empaquetar; rotar si alguna vez se compartio |
| `-=MEDIOEVO=-\-=LIBROS\.discord_client_id` | client id; no se observo ignore match | revisar si debe ser publico o ejemplo |
| `-=MEDIOEVO=-\-=LIBROS\.youtube_token.pickle` | token probable; `git check-ignore` lo ignora | no empaquetar; rotar si hubo exposicion |
| `-=MEDIOEVO=-\-=LIBROS\_gumroad_debug.json` | debug Gumroad | revisar contenido y excluir |
| `-=MEDIOEVO=-\-=LIBROS\claudio\.env` | env real; `git check-ignore` lo ignora | no empaquetar |
| `-=MEDIOEVO=-\-=LIBROS\claudio\.env.gumroad` | env Gumroad; `git check-ignore` lo ignora | no empaquetar |
| `-=MEDIOEVO=-\-=LIBROS\claudio\claudio_secrets.json` | secretos Claudio | no empaquetar; revisar ignore |
| `-=MEDIOEVO=-\-=LIBROS\claudio\claudio_tv_token.json` | token probable | no empaquetar; revisar ignore |
| `-=MEDIOEVO=-\-=LIBROS\claudio\gumroad_api.json` | credenciales/config Gumroad probable | no empaquetar; revisar ignore |
| `-=MEDIOEVO=-\-=LIBROS\claudio\gumroad_products.json` | catalogo Gumroad | revisar si contiene IDs privados o datos comerciales |
| `-=MEDIOEVO=-\-=LIBROS\claudio\stripe_hsbc_bridge.py` | integracion pagos | revisar secretos inline o config externa |
| `-=MEDIOEVO=-\-=LIBROS\claudio\verificar_stripe.py` | script pagos | revisar secretos inline o config externa |

## Archivos `.env` de terceros/vendor

Rutas como `.skills\ruflo\ruflo\src\ruvocal\.env` y `.env.ci` existen dentro de vendors/skills. Aunque sean de terceros o ejemplos, deben excluirse de releases propios por defecto.

## Conteo de patrones por contenido

Se usaron patrones tipo `api_key`, `secret`, `token`, `password`, `private_key`, `bearer`, `gumroad`, `stripe`, `openai`, excluyendo `.git`, `node_modules`, `.venv`, `__pycache__`, `target`, `dist`, `build`, `release` y binarios comunes.

El resultado produjo multiples coincidencias en:

- sesiones locales `.claw\sessions\*.jsonl`;
- `PRODUCTOS_MEDIOEVO`;
- `.claude\settings.local.json`;
- scripts y docs de Gumroad/Stripe/OpenAI;
- `-=CEREBRO=-\-=PSI=-`;
- `CLAUDIO - researchs`;
- `PRODUCTOS_MEDIOEVO\claudio_os_blueprint`;
- `tools\claw-code`.

Este conteo no prueba que cada coincidencia sea secreto real, pero bloquea cualquier release por glob amplio.

## Estado de ignore observado

`-=LIBROS`:

- `.discord_token` esta ignorado por `.gitignore`.
- `.youtube_token.pickle` esta ignorado por `.gitignore`.
- `.discord_client_id` no mostro ignore match en la prueba.
- `_gumroad_debug.json` no mostro ignore match en la prueba.

`claudio`:

- `.env` esta ignorado por `.gitignore`.
- `.env.gumroad` esta ignorado por regla `.env.*`.
- `claudio_secrets.json`, `gumroad_api.json`, `claudio_tv_token.json` no mostraron ignore match en la prueba.

## Riesgos

1. Los secretos pueden estar seguros frente a Git pero inseguros frente a ZIPs/manual packaging.
2. Los archivos de sesiones locales pueden contener prompts, rutas, tokens o contexto privado.
3. Archivos Gumroad/Stripe/Discord/Youtube requieren revision manual antes de publicar.
4. Los vendors pueden traer `.env` de ejemplo o reales; no deben entrar en productos propios.

## Recomendaciones Fase 1

- Crear denylist global para release:
  - `**/.env`, `**/.env.*`, `**/*secret*`, `**/*token*`, `**/*credential*`, `**/settings.local.json`, `**/.claw/**`, `**/.claude/**`.
- Crear allowlist por producto. No usar `Compress-Archive *`.
- Agregar reglas ignore faltantes para:
  - `.discord_client_id` si no debe ser publico.
  - `_gumroad_debug.json`.
  - `claudio_secrets.json`.
  - `gumroad_api.json`.
  - `claudio_tv_token.json`.
- Rotar secretos si alguno fue committeado, compartido o empaquetado antes.
- Usar un scanner dedicado en Fase 3/4 antes de release.
