# GUÍA DE DESPLIEGUE - MEDIOEVO TOOLS Y SITE
## Estado actual: 2026-06-26

---

## ✅ COMPLETADO AUTOMÁTICAMENTE

### Assets Consolidados
- ✅ `thumbnails/` eliminado (2,387 archivos, 98.7 MB)
- ✅ `img/` → `assets/images/{characters,environments,tcg,ui}`
- ✅ `WABI_VISUALS/` → `assets/images/visuals/`
- ✅ `sprites/` → `assets/images/sprites/`
- ✅ Estructura final: 1,508 archivos en `assets/images/`

### Wabi-Sabi: GLM como proveedor prioritario
- ✅ `provider_capabilities.json`: GLM (`glm-4-plus`) prioritario en TODAS las capacidades
- ✅ `wabi.env`: `WABI_PROVIDER=glm`, `WABI_MODEL=glm-4-plus`
- ✅ `WABI_PROVIDER_ORDER=glm,nvidia,cloudflare,deepseek,groq,openrouter,ollama,dry-run`
- ✅ Tests: 48/48 PASSED (provider_router, registry, hub, policy)

### Despliegue GitHub Pages - medioevo-tools
- ✅ Workflow: `.github/workflows/deploy-medioevo-tools.yml`
- ✅ 404.html para SPA fallback
- ✅ `_shared/brainos-ui.css` copiado a `apps/medioevo-tools/_shared/`
- ✅ Validación HTML: 4/4 archivos OK

### Despliegue Cloudflare Pages - medioevo-site-v2
- ✅ Workflow: `apps/medioevo-site-v2/.github/workflows/lighthouse.yml`
- ✅ CNAME: `medioevo.space` en `public/CNAME`
- ✅ wrangler.toml configurado

---

## 🔴 ACCIONES REQUERIDAS POR EL USUARIO (Tyr)

### 1. STRIPE DASHBOARD - Crear Productos y Price IDs
**Ir a: https://dashboard.stripe.com/products**

#### Productos a crear:
| Producto | Nombre | Precio | Tipo | Metadata |
|----------|--------|--------|------|----------|
| Anti-IA Detector | `Anti-IA Detector` | $3.00 USD | One-time | `product_type=anti_ia, uses=50` |
| Fact-Check OSIT | `Fact-Check OSIT` | $3.00 USD | One-time | `product_type=factcheck, uses=50` |
| Fact-Check OSIT Pro | `Fact-Check OSIT Pro` | $10.00 USD | One-time | `product_type=factcheck_pro, uses=50` |

#### Tras crear cada producto:
1. Copiar el **Price ID** (formato: `price_XXXXXXXXXXXX`)
2. Actualizar `wabi.env` con los Price IDs reales:

```env
# En wabi.env - reemplazar placeholders:
STRIPE_PRICE_ID_ANTI_IA=price_TU_PRICE_ID_AQUI
STRIPE_PRICE_ID_FACTCHECK=price_TU_PRICE_ID_AQUI
STRIPE_PRICE_ID_FACTCHECK_PRO=price_TU_PRICE_ID_AQUI
```

#### Stripe Webhook (requerido para cumplimiento):
- **Endpoint**: `https://medioevo.space/api/stripe-webhook` (o tu dominio)
- **Eventos**: `checkout.session.completed`
- **Secret**: Copiar `whsec_XXXX` a `STRIPE_WEBHOOK_SECRET` en `wabi.env`

---

### 2. STRIPE PAYMENT LINKS (Para despliegue estático en GitHub Pages)
**Ir a: https://dashboard.stripe.com/payment-links**

Crear Payment Link para cada producto:
| Producto | Payment Link URL (formato: `https://buy.stripe.com/XXXXXX`) |
|----------|-------------------------------------------------------------|
| Anti-IA Detector | `https://buy.stripe.com/XXXXXX` |
| Fact-Check OSIT | `https://buy.stripe.com/XXXXXX` |
| Fact-Check OSIT Pro | `https://buy.stripe.com/XXXXXX` |

Actualizar en HTML files (`apps/medioevo-tools/`):
```javascript
// anti_ia_detector_web.html - CONFIG object:
STRIPE_PAYMENT_LINK: 'https://buy.stripe.com/TU_LINK_AQUI',

// factcheck_web.html - agregar Payment Link:
const STRIPE_PAYMENT_LINK_FACTCHECK_PRO = 'https://buy.stripe.com/TU_LINK_AQUI';
```

---

### 3. GITHUB PAGES - Configurar dominio personalizado (Opcional)
Si se quiere `tools.medioevo.space` o similar:

1. En repo `Lutren/medioevo-tools` → Settings → Pages
2. Custom domain: `tools.medioevo.space`
3. En DNS (Cloudflare/registrador): CNAME `tools` → `lutren.github.io`
4. Crear `apps/medioevo-tools/CNAME`:
```
tools.medioevo.space
```

---

### 4. CLOUDFLARE PAGES - Verificar despliegue medioevo-site-v2
El workflow en `apps/medioevo-site-v2/.github/workflows/lighthouse.yml` despliega a Cloudflare Pages.

**Secrets requeridos en GitHub (repo `Lutren/wabi-sabi`):**
```
CLOUDFLARE_API_TOKEN=cfut_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
CLOUDFLARE_ACCOUNT_ID=2b7d685bb38b0badcfb48e9d221f6e73
```

**Verificar en Cloudflare Dashboard:**
- Project: `medioevo-site`
- Custom domain: `medioevo.space` (ya en `public/CNAME`)
- Build command: `npm run build`
- Output directory: `dist`

---

### 5. VARIABLES DE ENTORNO - Verificar wabi.env
Archivo: `C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\02_CLAUDIO\wabi.env`

**Ya configurado (no tocar):**
- ✅ `NVIDIA_API_KEY`, `NVIDIA_MODEL=qwen/qwen3-coder-480b-a35b-instruct`
- ✅ `ZHIPU_API_KEY`, `GLM_API_KEY`, `GLM_MODEL=glm-4-flash`, `GLM_PRO_MODEL=glm-4-plus`
- ✅ `DEEPSEEK_API_KEY`, `DEEPSEEK_MODEL=deepseek-v4-flash`
- ✅ `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`
- ✅ `CLOUDFLARE_AI_BASE_URL`, `CLOUDFLARE_AI_MODEL=@cf/qwen/qwen2.5-coder-32b-instruct`
- ✅ `HIGGSFIELD_API_KEY`, `HIGGSFIELD_SECRET`
- ✅ `GUMROAD_APP_ID`, `GUMROAD_APP_SECRET`, `GUMROAD_ACCESS_TOKEN`
- ✅ `STRIPE_RESTRICTED_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_SECRET_KEY`
- ✅ `WABI_PROVIDER=glm`, `WABI_MODEL=glm-4-plus`
- ✅ `WABI_PROVIDER_ORDER=glm,nvidia,cloudflare,deepseek,groq,openrouter,ollama,dry-run`

**Pendiente (Tyr debe completar):**
```
STRIPE_PRICE_ID_ANTI_IA=price_XXXXXXXXXXXX
STRIPE_PRICE_ID_FACTCHECK=price_XXXXXXXXXXXX
STRIPE_PRICE_ID_FACTCHECK_PRO=price_XXXXXXXXXXXX
STRIPE_WEBHOOK_SECRET=whsec_XXXXXXXXXXXX
```

---

## 📋 CHECKLIST DE DESPLIEGUE

### Pre-despliegue
- [ ] Stripe: 3 productos creados con Price IDs
- [ ] Stripe: 3 Payment Links creados
- [ ] Stripe: Webhook configurado → `medioevo.space/api/stripe-webhook`
- [ ] wabi.env: Price IDs y Webhook Secret actualizados
- [ ] HTML files: Payment Links agregados
- [ ] GitHub: Secrets `CLOUDFLARE_API_TOKEN` y `CLOUDFLARE_ACCOUNT_ID` configurados

### Despliegue medioevo-tools (GitHub Pages)
- [ ] Push a `main` dispara workflow `deploy-medioevo-tools.yml`
- [ ] Verificar en Actions: build + deploy exitosos
- [ ] Probar en `https://lutren.github.io/wabi-sabi/medioevo-tools/` (o dominio custom)
- [ ] Probar Anti-IA Detector y Fact-Check
- [ ] Probar botón Stripe → redirige a Payment Link

### Despliegue medioevo-site-v2 (Cloudflare Pages)
- [ ] Push a `main` dispara workflow en `apps/medioevo-site-v2/.github/workflows/lighthouse.yml`
- [ ] Verificar Lighthouse CI pasa
- [ ] Verificar deploy a Cloudflare Pages
- [ ] Probar en `https://medioevo.space`

### Post-despliegue
- [ ] Probar compra Stripe end-to-end (modo test)
- [ ] Verificar webhook recibe `checkout.session.completed`
- [ ] Verificar licencia se valida correctamente
- [ ] Probar Gumroad fallback
- [ ] Documentar URLs finales en `NEXT_SESSION_BRIEF.md`

---

## 🔗 URLs ESPERADAS TRAS DESPLIEGUE

| Servicio | URL |
|----------|-----|
| MEDIOEVO Site | `https://medioevo.space` |
| MEDIOEVO Tools | `https://lutren.github.io/wabi-sabi/medioevo-tools/` (o `tools.medioevo.space`) |
| Anti-IA Detector | `/anti_ia_detector_web.html` |
| Fact-Check OSIT | `/factcheck_web.html` |
| Stripe Success | `/success.html` |
| API Stripe Checkout | `https://medioevo.space/api/create-checkout-session` |
| API Stripe Webhook | `https://medioevo.space/api/stripe-webhook` |
| API License Verify | `https://medioevo.space/api/license/{key}` |

---

## 🚨 COMANDOS ÚTILES

### Probar Stripe localmente (con ngrok):
```bash
# Terminal 1: API local
cd 02_CLAUDIO && python -m uvicorn api.main:app --port 47047

# Terminal 2: ngrok
ngrok http 47047

# Actualizar webhook en Stripe Dashboard con URL ngrok + /api/stripe-webhook
```

### Desplegar manualmente medioevo-tools:
```bash
cd apps/medioevo-tools
# Verificar archivos
python validate_html.py

# Para GitHub Pages manual (si no usa Actions):
# git subtree push --prefix apps/medioevo-tools origin gh-pages
```

### Verificar logs Cloudflare Pages:
```bash
# En Cloudflare Dashboard → Pages → medioevo-site → Deployments
# O via wrangler:
npx wrangler pages deployment list --project-name=medioevo-site
```

### Tests Stripe (modo test):
```bash
cd 02_CLAUDIO
python stripe_manager.py --create-checkout anti_ia_detector
python stripe_manager.py --list-prices
```

---

## 📁 ARCHIVOS MODIFICADOS RECIENTEMENTE

| Archivo | Cambio |
|---------|--------|
| `.github/workflows/deploy-medioevo-tools.yml` | Nuevo workflow GitHub Pages |
| `apps/medioevo-tools/404.html` | Nuevo SPA fallback |
| `apps/medioevo-tools/_shared/brainos-ui.css` | Copiado desde `apps/_shared/` |
| `apps/medioevo-tools/validate_html.py` | Script de validación |
| `02_CLAUDIO/config/provider_capabilities.json` | GLM prioritario |
| `02_CLAUDIO/wabi.env` | WABI_PROVIDER=glm, orden actualizado |
| `scripts/validate_workflow.py` | Validador YAML |

---

## ⚠️ RIESGOS Y NOTAS

1. **Stripe Test Mode**: Las claves en `wabi.env` son `sk_test_` y `pk_test_`. Cambiar a live cuando estés listo.
2. **Webhook URL**: Debe ser HTTPS público. En desarrollo usar ngrok.
3. **GitHub Pages Base Path**: Si se usa subdominio custom, el base path es `/`. Si es `lutren.github.io/wabi-sabi/medioevo-tools/`, los assets relativos funcionan.
4. **CORS**: La API en `medioevo.space` debe permitir CORS desde el dominio de tools.
5. **Rate Limiting**: Configurar KV namespace en Cloudflare para rate limiting de API.

---

*Generado automáticamente - 2026-06-26*
*Actualizar tras cada acción completada*