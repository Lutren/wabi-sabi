# WABI-SABI ABSORPTION MANIFEST

Fecha: 2026-05-16

Canon: `apps/local/wabi-sabi`

Este manifiesto convierte rutas Wabi-Sabi dispersas en una sola verdad
operativa. Absorcion aqui significa: codigo/config seguro entra al canon; docs,
fichas, staging, assets y material protegido quedan como referencia registrada.
No hubo borrado fisico.

## Resumen

| grupo | conteo observado | accion |
|---|---:|---|
| `apps/local/wabi-sabi` | 141 coincidencias por nombre | CANON |
| root `adapters/*.py` | 6 archivos | ABSORBIDO_A_CANON y archivado en `_archive/legacy/wabi-sabi-external-2026-05-16/adapters` |
| root `config/models.wabisabi*.yaml` | 2 archivos | ABSORBIDO_A_CANON y archivado en `_archive/legacy/wabi-sabi-external-2026-05-16/config` |
| root `scripts/wabi_sabi*` y `select_model.ps1` | 3 wrappers | WRAPPER_HOST hacia canon |
| `COMMS/agents_state` | 1 estado | BRIDGE_STATE |
| `docs/intake` y `docs/ops` | 18 docs Wabi por nombre | REFERENCE_ONLY |
| `MEDIOEVO_OBSERVACIONISMO_MASTER` | 1 canon conceptual | THEORY_REFERENCE |
| `MEDIOEVO_LIVE_TREE` | 7 source/boundary cards | GOVERNANCE_REFERENCE |
| `packages/open-dev/duat-genesis/assets/pets` | 2 asset files | ASSET_REFERENCE |
| `publish_staging/.../wabi_sabi` | 1 staging spec | STAGING_REFERENCE |

## Absorbido Como Codigo/Config

| fuente anterior | destino canonico | estado |
|---|---|---|
| `adapters/adapter_deepsee4.py` | `apps/local/wabi-sabi/adapters/adapter_deepsee4.py` | absorbido |
| `adapters/adapter_nemotron.py` | `apps/local/wabi-sabi/adapters/adapter_nemotron.py` | absorbido |
| `adapters/adapter_qwen.py` | `apps/local/wabi-sabi/adapters/adapter_qwen.py` | absorbido |
| `adapters/stub_deepsee4.py` | `apps/local/wabi-sabi/adapters/stub_deepsee4.py` | absorbido |
| `adapters/stub_nemotron.py` | `apps/local/wabi-sabi/adapters/stub_nemotron.py` | absorbido |
| `adapters/stub_qwen.py` | `apps/local/wabi-sabi/adapters/stub_qwen.py` | absorbido |
| `config/models.wabisabi.yaml` | `apps/local/wabi-sabi/config/models.wabisabi.yaml` | absorbido |
| `config/models.wabisabi_extra.yaml` | `apps/local/wabi-sabi/config/models.wabisabi_extra.yaml` | absorbido |

## Wrappers Externos Que Permanecen

| path | accion | hash16 antes |
|---|---|---|
| `scripts/wabi_sabi_startup.ps1` | actualizado para usar adapters/logs canonicos | `6C9EF2381FB88EA8` |
| `scripts/wabi_sabi_startup_hidden.vbs` | wrapper host intacto | `C66619B2822B59CA` |
| `scripts/select_model.ps1` | actualizado para leer config canonica | n/a |
| `README_WABISABI.md` | convertido en redireccion a canon | `3E71842320F8FB3F` |

## Archivo Reversible Ejecutado

| source | destination | status |
|---|---|---|
| `adapters/` | `_archive/legacy/wabi-sabi-external-2026-05-16/adapters/` | moved |
| `config/` | `_archive/legacy/wabi-sabi-external-2026-05-16/config/` | moved |

Verificacion posterior: root `adapters=False`, root `config=False`, archivo
legacy `True`, canon `True`.

## Inventario Externo Por Nombre Wabi

| path | bytes | hash16 | decision |
|---|---:|---|---|
| `COMMS/agents_state/wabi-sabi-sentido-comun.json` | 824 | `1662AE0D136C3DA8` | BRIDGE_STATE |
| `_archive/legacy/wabi-sabi-external-2026-05-16/config/models.wabisabi_extra.yaml` | 737 | `E932F8D37178FD4F` | ARCHIVED_LEGACY |
| `_archive/legacy/wabi-sabi-external-2026-05-16/config/models.wabisabi.yaml` | 2119 | `1B12A54621162413` | ARCHIVED_LEGACY |
| `docs/canon/atlas/claudio-wabisabi.md` | 261 | `4C64513E384D0D86` | ATLAS_REFERENCE |
| `docs/intake/curador_fichas/downloads/693A35C7ECCE7BBF_wabisabi_cli_provider_patch_v0_1.md` | 1286 | `723FCD2112994D34` | SOURCE_CARD_REFERENCE |
| `docs/intake/curador_fichas/downloads/C9312402FAC54A92_10_wabi_sabi_claudio_agi.md` | 1188 | `91E755B6F3CFB536` | SOURCE_CARD_REFERENCE |
| `docs/intake/FORMAL_CODE_RESCAN_CLAUDIO_WABI_2026-05-08.md` | 7403 | `DB2DECF8713090A4` | REFERENCE_ONLY |
| `docs/intake/FORMAL_WABI_CONTRACT_COMPARISON_2026-05-13.md` | 3514 | `7651DE8F5F2F7281` | REFERENCE_ONLY |
| `docs/intake/LOVABLE_TO_WABI_DUAT_INTEGRATION_TASKS.md` | 4241 | `CDD2ABC796EB2069` | REFERENCE_ONLY |
| `docs/intake/PSI_WABI_SABI_TECH_INTAKE_2026-05-07.md` | 5396 | `AE6A398212059199` | REFERENCE_ONLY |
| `docs/ops/STABILITY_FREEZE_WABI_CEREBRO_2026-05-07.md` | 6593 | `1A933980CC3CE5DA` | REFERENCE_ONLY |
| `docs/ops/TECH_PRIORITY_WABI_ENTORNO_PROGRAMAR_COMMS_2026-05-06.md` | 13666 | `BAD761C0EB64A022` | REFERENCE_ONLY |
| `docs/ops/WABI_CEREBRO_CONTINUATION_HANDOFF_2026-05-07.md` | 11591 | `57F561217087A86E` | REFERENCE_ONLY |
| `docs/ops/WABI_CEREBRO_FUNCTIONAL_HANDOFF_2026-05-07.md` | 4358 | `ED298F354FE4146D` | REFERENCE_ONLY |
| `docs/ops/WABI_CLAUDIO_PROVIDER_GATE_2026-05-08.md` | 3762 | `47976E9AD69BA09F` | REFERENCE_ONLY |
| `docs/ops/WABI_OSIT_BRIDGE_FROM_ESTADO_2026-05-06.md` | 3765 | `8534D2D7E65C1CAD` | REFERENCE_ONLY |
| `docs/ops/WABI_QWEN_REDACTED_PRESENCE_2026-05-13.md` | 1591 | `AA9F5F08C98C2D62` | REFERENCE_ONLY |
| `docs/ops/WABI_SABI_BENCHMARK_GATE_RECHECK_2026-05-07.md` | 1548 | `D71EC69EB2E1F926` | REFERENCE_ONLY |
| `docs/ops/WABI_SABI_BENCHMARK_RUN_2026-05-07.md` | 2308 | `3F874684664D976D` | REFERENCE_ONLY |
| `docs/ops/WABI_SABI_CLOUD_SETUP_CLOSEOUT_2026-05-09.md` | 2854 | `86255E906111061C` | REFERENCE_ONLY |
| `docs/ops/WABI_SABI_FALLBACK_RUNBOOK_2026-05-09.md` | 5082 | `A2ECBD5E17D407B3` | REFERENCE_ONLY |
| `docs/ops/WABI_SABI_PROVIDER_VERIFICATION_QUEUE_2026-05-09.md` | 4458 | `86D90E5E843448E4` | REFERENCE_ONLY |
| `docs/ops/WABI_SABI_QWEN_BLUEPRINT_WORKPACK_2026-05-06.md` | 2179 | `81ABC340048CCDE2` | REFERENCE_ONLY |
| `MEDIOEVO_LIVE_TREE/01_SOURCE_CARDS/PROTECTED_IP-044-DUAT-ICON-WABISABI.md` | 1086 | `12DEE9A1732FF418` | PROTECTED_IP_REFERENCE |
| `MEDIOEVO_LIVE_TREE/01_SOURCE_CARDS/PROTECTED_IP-046-DUAT-ICON-WABISABI.md` | 1086 | `1C32D06316B955A8` | PROTECTED_IP_REFERENCE |
| `MEDIOEVO_LIVE_TREE/01_SOURCE_CARDS/PROTECTED_IP-057-DUAT-ICON-WABISABI.md` | 1086 | `4A38666C148EB522` | PROTECTED_IP_REFERENCE |
| `MEDIOEVO_LIVE_TREE/01_SOURCE_CARDS/PROTECTED_IP-059-DUAT-ICON-WABISABI.md` | 1086 | `A9670A72A7E17BAA` | PROTECTED_IP_REFERENCE |
| `MEDIOEVO_LIVE_TREE/01_SOURCE_CARDS/PROTECTED_IP-077-DUAT-ICON-WABISABI.md` | 1119 | `5AF7FE753375942D` | PROTECTED_IP_REFERENCE |
| `MEDIOEVO_LIVE_TREE/01_SOURCE_CARDS/PROTECTED_IP-079-DUAT-ICON-WABISABI.md` | 1119 | `55BA7CD18CA27FAD` | PROTECTED_IP_REFERENCE |
| `MEDIOEVO_LIVE_TREE/04_PRIVATE_BOUNDARY/WABI_SABI.md` | 73 | `74CFEF2BCAE68624` | PRIVATE_BOUNDARY_REFERENCE |
| `MEDIOEVO_OBSERVACIONISMO_MASTER/10_WABI_SABI_CLAUDIO_AGI.md` | 6247 | `C72CA405CF20F9EF` | THEORY_REFERENCE |
| `packages/open-dev/duat-genesis/assets/pets/wabi-sabi-k-07/pet.json` | 236 | `9A6EC0DC31E742EA` | ASSET_REFERENCE |
| `packages/open-dev/duat-genesis/assets/pets/wabi-sabi-k-07/spritesheet.webp` | 2040116 | `8A0897C95BAB06E6` | ASSET_REFERENCE |
| `publish_staging/system_integration_review/integration_specs/wabi_sabi/wabi_sabi_boundary_adapter.md` | 126 | `72A303E9F91F16F4` | STAGING_REFERENCE |

## Reglas Para El Siguiente Barrido

- Si un archivo externo contiene codigo Wabi-Sabi ejecutable, se absorbe hacia
  `apps/local/wabi-sabi` o se convierte en wrapper.
- Si un archivo externo contiene teoria, ficha, atlas, governance o staging,
  se referencia aqui y no se ejecuta desde fuera.
- Si un archivo externo contiene secretos, loaders de secretos, credenciales,
  pagos, publicacion o rutas privadas, queda REVIEW/BLOCK y no se copia.
- Root `adapters/` y root `config/` ya no existen como rutas activas; sus
  copias antiguas estan archivadas bajo `_archive/legacy`.
