# Pending Review - 2026-05-05

Status: generated snapshot. This file is evidence for triage, not proof that old checkboxes are still valid and not permission to publish, push, deploy or delete.

## Counts

- Active markdown raw open items: `457`.
- Active markdown deduplicated open items: `452`.
- Claudio `PENDIENTES_MASTER.md` raw open items: `72`.
- Claudio deduplicated open items: `72`.

## Active Markdown By Priority

| priority | dedup_count |
| --- | --- |
| P1 | 11 |
| P2 | 6 |
| P3 | 3 |
| P4 | 4 |
| UNCLASSIFIED | 428 |

## Active Markdown By Lane

| lane | dedup_count |
| --- | --- |
| cleanup_migration | 1 |
| commercial | 79 |
| general | 155 |
| open_source | 2 |
| private_rpg | 3 |
| runtime_claudio | 192 |
| wave_fc | 3 |
| website_marketing | 17 |

## Active Markdown By Blocker

| blocker | dedup_count |
| --- | --- |
| external_or_gated | 262 |
| host_or_heavy | 55 |
| legal_or_human | 126 |
| private_boundary | 9 |

## Claudio Master By Priority

| priority | dedup_count |
| --- | --- |
| P1 | 11 |
| P2 | 6 |
| P3 | 3 |
| P4 | 4 |
| UNCLASSIFIED | 48 |

## Claudio Master By Blocker

| blocker | dedup_count |
| --- | --- |
| external_or_gated | 43 |
| host_or_heavy | 18 |
| legal_or_human | 6 |
| private_boundary | 5 |

## Top Items

| priority | lane | blocker | item | first evidence | occurrences |
| --- | --- | --- | --- | --- | --- |
| P1 | commercial | legal_or_human | **P1** No declarar FlujoCRM listo para venta final hasta probar el instalador Windows en maquina limpia, resolver icono final, code signing o aviso unsigned, docs de instalacion y legal/soporte. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1116 | 1 |
| P1 | commercial | external_or_gated | P1 - Gumroad Claudio software: `pack-empresarial`, `writer-workbench` y `claudio-full` existen como drafts (`published=false`) y sin archivos/covers; no publicarlos hasta adjuntar paquete, portada y prueba de checkout. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1698 | 1 |
| P1 | runtime_claudio | host_or_heavy | **P1** Ejecutar suite Qwen 3B cuando el host permita ruta pesada: `python tools\qwen_observacion_benchmark_suite.py --execute --write-dataset`. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:804 | 1 |
| P1 | runtime_claudio | external_or_gated | **P1** Confirmar visualmente cual URL de LinkedIn es la canonica antes de editar el perfil. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1085 | 1 |
| P1 | runtime_claudio | external_or_gated | **P1** Pegar headline/about/experience/featured links desde `LINKEDIN_PROFILE_PACKET_2026-05-01.md` en LinkedIn autenticado, cuidando no regalar tecnologia privada ni claims fuertes. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1086 | 1 |
| P1 | runtime_claudio | host_or_heavy | **P1** Resolver QA visual DOCX; `artifact-tool` y `soffice/libreoffice` no estan disponibles en este host. Recheck 2026-05-03: `winget` detecta LibreOffice 26.2.2.2, pero `--scope user` no tiene instalador aplicable y el intento no interactivo estandar hizo timeout; no quedo instalado. Evidencia en `docs\DOCX_VISUAL_QA_RENDERER_ATTEMPT_2026-05-03.md`. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1140 | 1 |
| P1 | runtime_claudio | legal_or_human | **P1** Revisar jurisdiccion, impuestos, plataforma de pago y politica final con asesor legal. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1159 | 1 |
| P1 | runtime_claudio | private_boundary | **P1** Usar `release_manifests/` como base de QA, pero no crear paquetes ZIP hasta que secret scan, legal y release checklist pasen. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1192 | 1 |
| P1 | runtime_claudio | external_or_gated | **P1** Convertir packaging interno en landing/copy publico solo despues de licencia, capturas, instalacion y ActionGate de publicacion. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1262 | 1 |
| P1 | runtime_claudio | external_or_gated | **P1** Generar capturas/video local de demo y decidir artefactos publicos despues de ActionGate. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1263 | 1 |
| P1 | wave_fc | external_or_gated | **P1** Cerrar licencia/EULA, instalacion, landing copy y ActionGate antes de vender o publicar Wave FC. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1141 | 1 |
| P2 | runtime_claudio | legal_or_human | **P2** Conector a checador fisico solo como read-only, con consentimiento, logs, fallback manual y aprobacion legal/laboral. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1266 | 1 |
| P2 | runtime_claudio | host_or_heavy | **P2** Crear alias Ollama optimizados con `python tools\gemma4_observacion_optimizer.py --create-aliases --execute` solo cuando el host este `APPROVE`; luego correr `python tools\benchmark_gemma4_observador.py --profile lite`. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1369 | 1 |
| P2 | runtime_claudio | host_or_heavy | **P2** Ejecutar `python tools\gemma4_observacion_benchmark_suite.py --execute --write-dataset` solo cuando el host este `APPROVE`; aceptar candidatos `input -> respuesta observacionista` en `datasets/gemma4_observacion_candidates.jsonl` antes de cualquier LoRA/QLoRA. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1370 | 1 |
| P2 | runtime_claudio | private_boundary | **P2** Validar sesiones/credenciales sociales reales por plataforma antes de activar publicacion automatica; hoy solo se comprobo dry-run/capacidad tecnica, no post real. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1373 | 1 |
| P2 | runtime_claudio | host_or_heavy | **P2** Instalar dependencias faltantes en Ubuntu WSL (`live-build/lb`, `qemu-system-x86_64`, `xorriso`) y ejecutar `runtime/claudio_os_build/staging/claudio_os_blueprint/BUILD_IN_WSL.sh` para producir la ISO. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1596 | 1 |
| P2 | runtime_claudio | host_or_heavy | **P2** Bootear ISO en QEMU antes de cualquier USB/PC2. | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:1597 | 1 |
| P3 | runtime_claudio | external_or_gated | **P3.5** Discord Q&A session | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:2495 | 1 |
| P3 | runtime_claudio | external_or_gated | **P3.6** Reseñas de Amazon (pedir a lectores) | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:2496 | 1 |
| P3 | runtime_claudio | external_or_gated | **P3.7** Colaboración con booktubers | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:2497 | 1 |
| P4 | runtime_claudio | external_or_gated | **P4.3** Testimonios reales | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:2506 | 1 |
| P4 | runtime_claudio | external_or_gated | **P4.5** Guest post en blogs de sci-fi | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:2510 | 1 |
| P4 | runtime_claudio | external_or_gated | **P4.6** Podcasts de literatura | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:2511 | 1 |
| P4 | runtime_claudio | external_or_gated | **P4.7** Colaboraciones cross-promo | -=MEDIOEVO=-/-=LIBROS/claudio/PENDIENTES_MASTER.md:2512 | 1 |
| UNCLASSIFIED | cleanup_migration | external_or_gated | `MIGRATION_MAP.md` para cualquier movimiento futuro. | RELEASE_READINESS_SCORE.md:83 | 1 |

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
