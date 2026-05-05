# Public Profile Network Pending - 2026-05-05

Status: `TRACKER_ACTIVO`

Alcance: redes, Gumroad, website, GitHub, GitHub Sponsors, LinkedIn y frontera
publica/privada para MEDIOEVO/Lutren.

Este tracker documenta lo ejecutado localmente y lo que queda pendiente. No es
permiso de publicacion externa.

## Cierre Local Registrado

- [x] Leer continuidad del workspace y reglas de publicacion: `AGENTS.md`,
  `PRODUCT_MAP.md`, `VISIBILITY_MATRIX.md`, `RISK_REGISTER.md`,
  `SECRET_SCAN_REPORT.md`, `PUBLISHING_PLAN.md`, `GUMROAD_CATALOG.md`,
  `GUMROAD_PRODUCTS.md`, `COMMERCIAL_STRATEGY.md` y `OPEN_SOURCE_STRATEGY.md`.
- [x] Ejecutar snapshot de pendientes:
  `python tools\release\pending_review.py --write --quiet`.
- [x] Verificar superficies publicas principales en modo read-only:
  website, Gumroad, GitHub y GitHub Sponsors devolvieron HTTP 200.
- [x] Leer GitHub API para `Lutren`: perfil publico, bio, blog, repos publicos
  y README remoto.
- [x] Crear observatorio de perfiles/redes:
  `docs\publishing\PUBLIC_PROFILE_NETWORK_OBSERVATORY_2026-05-05.md`.
- [x] Crear agente especializado:
  `publicacion-perfiles-observatorio`.
- [x] Registrar agente en COMMS:
  `COMMS\agents_state\publicacion-perfiles-observatorio.json`,
  `COMMS\inbox\publicacion-perfiles-observatorio.jsonl`,
  `COMMS\outbox\publicacion-perfiles-observatorio.jsonl` y
  `COMMS\handoffs\2026-05-05-publicacion-perfiles-observatorio.md`.
- [x] Crear cola externa por target:
  `docs\publishing\PUBLIC_PROFILE_EXTERNAL_ACTION_QUEUE_2026-05-05.md`.
- [x] Crear paquete de copy para Gumroad:
  `docs\publishing\GUMROAD_LISTING_OPTIMIZATION_PACKET_2026-05-05.md`.
- [x] Crear paquete de perfil/post para LinkedIn:
  `docs\publishing\LINKEDIN_PROFILE_PACKET_2026-05-05.md`.
- [x] Crear calendario de redes:
  `docs\publishing\SOCIAL_CONTENT_CALENDAR_2026-05.md`.
- [x] Ejecutar audit SEO con skill `seo-growth-medioevo` sobre la fuente
  canonica `-=MEDIOEVO=-\-=LIBROS\claudio\website`; resultado: todos los
  checks OK, sin findings mayores.
- [x] Parche local en website home:
  `-=MEDIOEVO=-\-=LIBROS\claudio\website\index.html` suma GitHub Sponsors en
  rutas visibles y `sameAs` JSON-LD para GitHub, Sponsors y Gumroad.
- [x] Validar JSON-LD, JSON y JSONL: OK.
- [x] Ejecutar secret scan focalizado sobre docs/COMMS/index tocados:
  `count_reported=0`.

## Estado Actual De Gate

- [ ] P0 - Repetir host gate antes de cualquier accion externa:
  `python tools\host_observacionista.py --no-write` desde Claudio.
- [ ] P0 - No ejecutar push, deploy, Gumroad, LinkedIn ni redes mientras host
  gate este `BLOCK` o `REVIEW` sin override target-specific documentado.

Evidencia mas reciente:

| check | resultado |
|---|---|
| host gate no-write | `BLOCK` |
| timestamp | `2026-05-05T21:31:52Z` |
| razones | memoria alta, proceso dominante CPU, residuo alto |
| GitHub profile README | remoto verificado; sha `5e6aa51388978d7c1405333b37451c6f47646abf`; ya contiene `Publication Lanes`, `Three Public Paths`, Sponsors y frontera privada |
| GitHub Sponsors | HTTP 200; goal y tiers visibles |
| LinkedIn URL observada desde GitHub | `https://www.linkedin.com/in/luis-ren%C3%A9-gonz%C3%A1lez-l%C3%B3pez-64517b20b/`; requiere confirmacion visual autenticada |
| external actions | ninguna ejecutada |

## Pendientes Por Target

| prioridad | target | pendiente | estado | evidencia/base |
|---|---|---|---|---|
| P0 | Website | desplegar el parche local de home solo cuando host gate este `APPROVE`; luego verificar HTTP 200 y sitemap | `BLOCKED_BY_HOST_GATE` | `WEBSITE_PUBLIC_FUNNEL_REVIEW_2026-05-05.md`, `website/index.html` |
| P0 | Gumroad Agent Ops Pack | actualizar copy "what you get / what you do not get" y media, sin cambiar artefacto/precio | `READY_AFTER_GATE` | `GUMROAD_LISTING_OPTIMIZATION_PACKET_2026-05-05.md` |
| P0 | Gumroad DUAT Templates | reforzar `synthetic_only` y exclusion de DUAT/GEODIA privado | `READY_AFTER_GATE` | `GUMROAD_LISTING_OPTIMIZATION_PACKET_2026-05-05.md` |
| P0 | LinkedIn | confirmar visualmente URL canonica autenticada antes de editar perfil | `REVIEW` | `LINKEDIN_PROFILE_PACKET_2026-05-05.md` |
| P0 | LinkedIn | pegar headline/about/featured links solo despues de confirmar URL y gate | `READY_AFTER_URL_CONFIRMATION` | `LINKEDIN_PROFILE_PACKET_2026-05-05.md` |
| P1 | GitHub profile | no cambiar README por ahora; revisar pins si se confirma que no estan alineados | `NO_CHANGE_NEEDED_NOW` | README remoto ya esta alineado y Sponsors visible |
| P1 | GitHub Sponsors | no cambiar copy por ahora; verificar dashboard solo si se necesita screenshot/evidencia nueva | `NO_CHANGE_NEEDED_NOW` | Sponsors publico HTTP 200 |
| P2 | Instagram/TikTok/YouTube | publicar posts del calendario solo con cuenta autenticada, assets public-safe y gate | `DRAFT_READY_AFTER_GATE` | `SOCIAL_CONTENT_CALENDAR_2026-05.md` |

## Frontera Publica/Secreta

- [ ] Mantener publicos: metodo, interfaces, schemas, CLIs, checklists,
  plantillas, demos sinteticos, articulos low-claim, rutas a GitHub/Gumroad y
  Sponsors.
- [ ] Mantener privados: formulas exactas, thresholds, prompts, runtime local,
  datasets reales, DUAT/GEODIA privado, GEODIA Social Observatory con datos
  reales, libros completos no aprobados, RPG/TCG, secretos, sesiones,
  credenciales, playbooks premium y soporte privado.
- [ ] No publicar claims de seguridad garantizada, anti-hallucination total,
  prediccion social, diagnostico medico, nueva fisica validada ni autonomia
  externa sin revision humana.

## Proximo Paso Ejecutable

1. Repetir host gate.
2. Si da `APPROVE`, ejecutar solo un target externo por tanda. Orden sugerido:
   website, Gumroad Agent Ops, Gumroad DUAT, LinkedIn, redes.
3. Si no da `APPROVE`, continuar solo con trabajo local: capturas public-safe,
   screenshots Gumroad/website, pruebas de copy, validacion de assets y fichas.

## Archivos Relacionados

- `docs\publishing\PUBLIC_PROFILE_NETWORK_OBSERVATORY_2026-05-05.md`
- `docs\publishing\PUBLIC_PROFILE_EXTERNAL_ACTION_QUEUE_2026-05-05.md`
- `docs\publishing\GUMROAD_LISTING_OPTIMIZATION_PACKET_2026-05-05.md`
- `docs\publishing\LINKEDIN_PROFILE_PACKET_2026-05-05.md`
- `docs\publishing\SOCIAL_CONTENT_CALENDAR_2026-05.md`
- `docs\publishing\WEBSITE_PUBLIC_FUNNEL_REVIEW_2026-05-05.md`
- `qa_artifacts\release_validation\github-linkedin-public-safe-positioning-2026-05-05.json`
- `COMMS\agents_state\publicacion-perfiles-observatorio.json`
