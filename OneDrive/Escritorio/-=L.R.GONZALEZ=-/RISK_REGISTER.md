# RISK_REGISTER

Fecha: 2026-04-29

| id | severidad | riesgo | evidencia | impacto | mitigacion |
|---|---|---|---|---|---|
| R-001 | CRITICA | Secretos reales en workspace | `.discord_token`, `.youtube_token.pickle`, `claudio\.env`, `claudio\.env.gumroad`, `claudio\claudio_secrets.json`, `claudio\gumroad_api.json` | filtracion si se empaqueta o publica | mantener fuera de Git/releases, rotar si hubo exposicion, crear `SECRET_SCAN_REPORT` y denylist |
| R-002 | CRITICA | Videojuego/TCG mezclado con workspace publicable | `metaevo-tcg`, `claudio\tcg`, `runtime\game_bridge`, `PRODUCTOS_MEDIOEVO\04_AUDIOVISUAL_Y_TCG` | perdida de IP o publicacion accidental | crear `PRIVATE_GAME_BOUNDARY.md`, denylist de packaging y repo privado separado |
| R-003 | ALTA | Historial Git pesado con archivos grandes | objeto Git de 2447.20 MB en `-=LIBROS\.git\objects`; zips grandes en `claudio\products` | repo dificil de clonar/publicar | no publicar repo actual; crear repo derivado limpio o filtrar historia con revision |
| R-004 | ALTA | Capas mezcladas en `claudio` | runtime, apps, editorial, comercio, vendors, pentest, game bridge | releases inseguros y confusos | dividir por producto con migration map |
| R-005 | ALTA | Repos de pentest/offensive dentro del arbol | `claudio\tools\pentest_repos\*` | riesgo de seguridad/legal/publicacion accidental | aislar como PRIVATE_SECURITY_REVIEW |
| R-006 | ALTA | Vendors y terceros mezclados | `.skills`, `github-modules`, `tools\vendor`, `sadtalker`, `wav2lip` | licencias incompatibles y paquetes enormes | excluir por defecto y revisar licencia por tercero |
| R-007 | ALTA | Working trees sucios y otra sesion activa | multiples modificados/no trackeados en `-=LIBROS`, `claudio`, `metaevo-tcg` | conflicto entre agentes y perdida de trabajo | no mover/borrar; registrar y coordinar por mapa |
| R-008 | MEDIA | Builds y binarios junto a fuente | `.zip`, `.exe`, `.apk`, `target/debug`, release dirs | empaquetado accidental y peso alto | mover a `releases/` o `_archive/` solo en Fase 2 aprobada |
| R-009 | MEDIA | Caches y outputs regenerables | 262 `__pycache__`, `.pytest_cache`, `.wrangler`, `target`, `node_modules` | ruido, falsos duplicados, empaques lentos | excluir y limpiar con script dry-run |
| R-010 | MEDIA | Licencias no centralizadas | falta `LICENSE` raiz, apps con MIT parcial, vendors varios | incertidumbre legal | `LEGAL_REVIEW_REQUIRED` por capa |
| R-011 | MEDIA | Docs de producto/release dispersos | muchos `README`, checklists y prompts viejos, sin README raiz | agentes futuros pierden intencion | crear `AGENTS.md`, README raiz, indices y handoff |
| R-012 | MEDIA | `PRODUCTOS_MEDIOEVO` parece staging correcto pero no es fuente unica | estructura 01-05 mas blueprint/content forge | riesgo de duplicar productos vs fuente | definir si es catalogo de salida o fuente |
| R-013 | MEDIA | Website duplicado/ambiguo | `-=LIBROS\website` casi vacio vs `claudio\website` real | despliegue equivocado | declarar source of truth del sitio |
| R-014 | MEDIA | `mini_office` tiene test placeholder | `test=echo 'No tests yet'` | falsa sensacion de calidad | crear smoke tests reales antes de vender |
| R-015 | BAJA | Archivos con nombres corruptos o raros | ejemplo `C...tempsensor_server.py`; textos con sustituciones raras en outputs observados | baja confianza de limpieza automatica | revisar encoding/nombres antes de migrar |
| R-016 | ALTA | Host gate bloquea publicacion externa por presion de host | `host_observacionista.py` 2026-05-01 antes de offload: `gate=REVIEW`, `disk_pct=87.6`, `disk_free_mb=27842.45`, razon `disco_precaucion`; despues de offload: `disk_pct=84.9`, `disk_free_mb=34031.32`, pero `gate=REVIEW`, `lambda_sat=0.849` | ActionGate real no autoriza `public_publish` aunque los artefactos allowlist esten limpios | evidencia de offload en `qa_artifacts\release_validation\host-gate-offload-2026-05-01.json`; no ejecutar publicacion real hasta host `APPROVE` |
| R-016B | ALTA | Host gate actual en REVIEW para acciones externas | no-write check 2026-05-02: `memory_pct=82.5`, `disk_pct=83.3`, `lambda_sat=0.833`, gate `REVIEW` | push, deploy y Gumroad deben esperar aunque haya autorizacion humana general | publicar solo cuando host gate vuelva a `APPROVE` y el staging especifico pase scans |
| R-017 | MEDIA | `r.txt` aclarado por humano como seguro/no bloqueante | usuario confirmo que el token fue introducido por otra IA en un reporte y es completamente seguro; `SOURCE_INTAKE_REGISTER.md` lo clasifica `USER_ASSERTED_SAFE_NON_BLOCKING` | riesgo residual de copiar texto tipo token por accidente si se usa glob amplio | no publicar ni stagear `r.txt`; registrar solo evidencia redactada; la seguridad de publicacion depende de allowlists y secret scan por staging |
| R-018 | ALTA | Open source maximo puede destruir patrimonio si no se separa | usuario quiere abrir lo maximo posible pero preservar patrimonio para familia | perdida de ingresos, IP, libros, RPG, marca o productos premium | publicar herramientas y docs public-safe; proteger libros, RPG, assets, marca, premium templates, hosted services y soporte |
| R-019 | ALTA | Patrimonio digital sin sucesor operativo | GitHub, dominios, Gumroad/Sponsors, repos, libros y productos dependen de continuidad de cuentas | familia puede perder control o ingresos | configurar sucesor GitHub, inventario privado de activos, y revision legal/contable/notarial |
| R-020 | ALTA | Confundir open core con regalar la UI/wrapper comercial | decision 2026-05-02: abrir tecnologia pero vender UI/agentes, soporte, plantillas e instaladores | perdida de patrimonio si se publica fuente completa de apps comerciales o premium templates sin revision | usar `AGENT_PRODUCT_FICHAS_2026-05-02.md`, `MEDIOEVO_AGENT_CITY_UI_SYSTEM_2026-05-02.md` y allowlists por producto |
| R-021 | ALTA | Instalar dependencias externas sin ficha previa | snapshots GitHub muestran licencias mixtas: MIT/Apache, AGPL, `NOASSERTION`, archivado | contaminacion legal, seguridad o claims exagerados | aplicar `DEPENDENCY_ADOPTION_GATE_2026-05-02.md` antes de instalar, vendorizar o bundlear |
| R-022 | MEDIA | Claims fuertes sin prueba se vuelven copy comercial | DUAT, NEUROSTATE, GEODIA, Wave FC y Observacionismo tienen claims potencialmente fuertes | riesgo legal/reputacional y falsa publicidad | aplicar `CLAIM_FALSIFICATION_REGISTER_2026-05-02.md`; si no se prueba, queda `DEMO_ONLY`, `RESEARCH_ONLY` o `BLOCK` |
| R-023 | MEDIA | Wrappers de `obs-safe-integration-kit` pueden confundirse con ejecucion segura automatica | paquete contiene adaptadores para GPT Researcher, SWE-agent, browser-use y AEGIS-like flows, pero su postura es dry-run/no-execution | integradores podrian venderlo o conectarlo como sistema autonomo garantizado | mantener `CLAIMS.md`, `PRIVATE_EXCLUSIONS.md`, `SECURITY.md`, tests, path scrub y ActionGate antes de cualquier push/publicacion |
| R-024 | ALTA | Limpieza global agresiva puede confundir repos, releases, entornos o archivos privados con basura regenerable | auditoria SETO 2026-05-05 encontro 81,107 archivos, 12,071 grupos de duplicados exactos y 10,242 items `BLOCK`; el primer clasificador tuvo que corregir `.git`, `release(s)` y `env` para no tratarlos como borrado directo | perdida de historia Git, evidencia comercial, entornos necesarios, secretos o IP privada | usar `CURADOR_SETO_GLOBAL_OPERATING_CONTRACT_2026-05-05.md`; borrar solo con ficha, hash, copia canonica/regenerabilidad y ActionGate |

## Riesgos inmediatos antes de publicar

1. No publicar ni subir el workspace completo.
2. No crear ZIP publico por glob amplio.
3. No usar `git push` desde arboles sucios sin revisar.
4. No incluir `metaevo-tcg` ni rutas TCG/game.
5. No incluir `.env`, tokens, Gumroad/Stripe/Discord/Youtube configs.
6. No incluir vendors ni pentest repos en paquetes dev gratuitos.
7. No publicar ningun repo GitHub hasta que el staging allowlist pase secret scan, path scrub, claims scan y ActionGate. `Downloads\r.txt` ya no es blocker por decision humana, pero sigue excluido de staging.

## Gate de salida Fase 0

Fase 1 puede empezar solo con:

- frontera privada documentada;
- estructura propuesta;
- mapa de migracion;
- politica de secrets;
- allowlist/denylist de release.
