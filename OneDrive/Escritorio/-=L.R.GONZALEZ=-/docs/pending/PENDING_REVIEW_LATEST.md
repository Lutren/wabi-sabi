# Pending Review - 2026-05-06

Status: generated snapshot. This file is evidence for triage, not proof that old checkboxes are still valid and not permission to publish, push, deploy or delete.

## Counts

- Active markdown raw open items: `186`.
- Active markdown deduplicated open items: `183`.
- Claudio `PENDIENTES_MASTER.md` raw open items: `19`.
- Claudio deduplicated open items: `19`.

## Active Markdown By Priority

| priority | dedup_count |
| --- | --- |
| P1 | 10 |
| P2 | 6 |
| UNCLASSIFIED | 167 |

## Active Markdown By Lane

| lane | dedup_count |
| --- | --- |
| commercial | 18 |
| general | 20 |
| open_source | 2 |
| private_rpg | 1 |
| research_claims | 1 |
| runtime_claudio | 135 |
| wave_fc | 2 |
| website_marketing | 4 |

## Active Markdown By Blocker

| blocker | dedup_count |
| --- | --- |
| external_or_gated | 118 |
| host_or_heavy | 42 |
| legal_or_human | 18 |
| private_boundary | 5 |

## Claudio Master By Priority

| priority | dedup_count |
| --- | --- |
| P1 | 10 |
| P2 | 6 |
| UNCLASSIFIED | 3 |

## Claudio Master By Blocker

| blocker | dedup_count |
| --- | --- |
| external_or_gated | 7 |
| host_or_heavy | 6 |
| legal_or_human | 3 |
| private_boundary | 3 |

## Top Items

| priority | lane | blocker | item | first evidence | occurrences |
| --- | --- | --- | --- | --- | --- |
| P1 | commercial | legal_or_human | **P1** No declarar FlujoCRM listo para venta final hasta probar instalador Windows en maquina limpia/VM, cerrar legal/soporte final y verificar rebuild/hash del instalador cliente activo. Aviso unsigned e instrucciones piloto quedaron documentados localmente en `docs\product\flujocrm-local-gate-recheck-2026-05-05.md`. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1454 | 1 |
| P1 | runtime_claudio | host_or_heavy | **P1** Ejecutar suite Qwen 3B cuando el host permita ruta pesada: `python tools\qwen_observacion_benchmark_suite.py --execute --write-dataset`. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1142 | 1 |
| P1 | runtime_claudio | external_or_gated | **P1** Confirmar visualmente cual URL de LinkedIn es la canonica antes de editar el perfil. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1423 | 1 |
| P1 | runtime_claudio | external_or_gated | **P1** Pegar headline/about/experience/featured links desde `LINKEDIN_PROFILE_PACKET_2026-05-01.md` en LinkedIn autenticado, cuidando no regalar tecnologia privada ni claims fuertes. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1424 | 1 |
| P1 | runtime_claudio | legal_or_human | **P1** Revisar jurisdiccion, impuestos, plataforma de pago y politica final con asesor legal. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1497 | 1 |
| P1 | runtime_claudio | private_boundary | **P1** Usar `release_manifests/` como base de QA, pero no crear paquetes ZIP hasta que secret scan, legal y release checklist pasen. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1530 | 1 |
| P1 | runtime_claudio | external_or_gated | **P1** Convertir packaging interno en landing/copy publico solo despues de licencia, capturas, instalacion y ActionGate de publicacion. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1600 | 1 |
| P1 | runtime_claudio | external_or_gated | **P1** Generar capturas/video local de demo y decidir artefactos publicos despues de ActionGate. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1601 | 1 |
| P1 | wave_fc | host_or_heavy | **P1** Resolver QA visual DOCX; `artifact-tool` y `soffice/libreoffice` no estan disponibles en este host. Recheck 2026-05-03: `winget` detecta LibreOffice 26.2.2.2, pero `--scope user` no tiene instalador aplicable y el intento no interactivo estandar hizo timeout; no quedo instalado. Recheck 2026-05-06: `winget list --name LibreOffice` reporta `No installed package found matching input criteria`. Evidencia en `docs\DOCX_VISUAL_QA_RENDERER_ATTEMPT_2026-05-03.md` y `docs\WAVE_WABI_LOCAL_GATE_...` | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1478 | 1 |
| P1 | wave_fc | external_or_gated | **P1** Cerrar licencia/EULA, instalacion, landing copy y ActionGate antes de vender o publicar Wave FC. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1479 | 1 |
| P2 | runtime_claudio | legal_or_human | **P2** Conector a checador fisico solo como read-only, con consentimiento, logs, fallback manual y aprobacion legal/laboral. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1604 | 1 |
| P2 | runtime_claudio | host_or_heavy | **P2** Crear alias Ollama optimizados con `python tools\gemma4_observacion_optimizer.py --create-aliases --execute` solo cuando el host este `APPROVE`; luego correr `python tools\benchmark_gemma4_observador.py --profile lite`. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1707 | 1 |
| P2 | runtime_claudio | host_or_heavy | **P2** Ejecutar `python tools\gemma4_observacion_benchmark_suite.py --execute --write-dataset` solo cuando el host este `APPROVE`; aceptar candidatos `input -> respuesta observacionista` en `datasets/gemma4_observacion_candidates.jsonl` antes de cualquier LoRA/QLoRA. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1708 | 1 |
| P2 | runtime_claudio | private_boundary | **P2** Validar sesiones/credenciales sociales reales por plataforma antes de activar publicacion automatica; hoy solo se comprobo dry-run/capacidad tecnica, no post real. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1711 | 1 |
| P2 | runtime_claudio | host_or_heavy | **P2** Instalar dependencias faltantes en Ubuntu WSL (`live-build/lb`, `qemu-system-x86_64`, `xorriso`) y ejecutar `runtime/claudio_os_build/staging/claudio_os_blueprint/BUILD_IN_WSL.sh` para producir la ISO. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1934 | 1 |
| P2 | runtime_claudio | host_or_heavy | **P2** Bootear ISO en QEMU antes de cualquier USB/PC2. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1935 | 1 |
| UNCLASSIFIED | commercial | external_or_gated | Sincronizar dashboard de Gumroad con el catalogo local ahora que la autenticacion API ya responde. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:2766 | 1 |
| UNCLASSIFIED | commercial | external_or_gated | Argus hardwamuy integration | -=MEDIOEVO=-/-=LIBROS/claudio/grants/LACMA_APPLICATION_2026.md:95 | 1 |
| UNCLASSIFIED | commercial | external_or_gated | Configurar Gumroad/Patmuyon con tiers | -=MEDIOEVO=-/-=LIBROS/claudio/marketing/DECISION_MARKETING_SaaS_20260410.md:102 | 1 |
| UNCLASSIFIED | commercial | external_or_gated | Hook en primeros 3 segundos: ruido digital + pantalla oscura (cumplido en escena 1) | -=MEDIOEVO=-/-=LIBROS/claudio/marketing/TRAILER_ARGUS_20260417.md:166 | 1 |
| UNCLASSIFIED | commercial | external_or_gated | Problema muyconocible en 0-6s (abrumamiento) | -=MEDIOEVO=-/-=LIBROS/claudio/marketing/TRAILER_ARGUS_20260417.md:167 | 1 |
| UNCLASSIFIED | commercial | external_or_gated | Solucion clara en 6-24s (ciudad que cmuyce) | -=MEDIOEVO=-/-=LIBROS/claudio/marketing/TRAILER_ARGUS_20260417.md:168 | 1 |
| UNCLASSIFIED | commercial | external_or_gated | Identificacion emocional en 24-36s (personas muyales) | -=MEDIOEVO=-/-=LIBROS/claudio/marketing/TRAILER_ARGUS_20260417.md:169 | 1 |
| UNCLASSIFIED | commercial | external_or_gated | Climax + CTA en 48-60s (runa + url) | -=MEDIOEVO=-/-=LIBROS/claudio/marketing/TRAILER_ARGUS_20260417.md:170 | 1 |
| UNCLASSIFIED | commercial | external_or_gated | Audio contrastante con silencio inicial | -=MEDIOEVO=-/-=LIBROS/claudio/marketing/TRAILER_ARGUS_20260417.md:171 | 1 |

## Kairos Fastlane

- Path: `-=MEDIOEVO=-/-=LIBROS/claudio/runtime/observacionista/kairos_attention_hygiene/pendientes_fastlane_2026-05-01.json`.
- Generated at: `2026-05-01T00:08:52+00:00`.
- Stale against this snapshot date: `True`.
- Decision count: `478`.

| action | count |
| --- | --- |
| defer | 325 |
| hold_calibration | 103 |
| queue_next | 50 |

## Operational Rule

At the start of each run/day execute `python tools\release\pending_review.py --write --quiet`, then choose work from shortest verified local closure first. External/publication tasks stay blocked until their specific gate is clean.
