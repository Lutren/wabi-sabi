# One Universe Integration - 2026-05-06

Estado: `UNIFICACION_LOCAL_EN_CURSO`

## Principio

No hay trabajo ajeno dentro de esta raiz. Hay trabajo concurrente de agentes dentro de un solo proyecto global.

La regla operativa cambia de "no tocar cambios ajenos" a:

- no sobrescribir sin leer;
- no revertir sin permiso;
- absorber, fichar y conectar;
- validar por carril;
- commitear por bloque exacto;
- mantener un solo Atlas como superficie de orientacion.

## Carriles integrados en este pase

| carril | fuente | destino canonico | estado |
|---|---|---|---|
| AI Browser seguro | `docs/ai_browser`, `tools/ai_browser`, schemas y fixtures | Seguridad / Claudio / Curaduria | `VALIDADO_LOCAL` |
| Lenguaje Observacionista L1 | `docs/language`, `research/observacionismo-lab` | PSI / Wabi-Sabi / COMMS | `VALIDADO_LOCAL` |
| Ciudad de agentes | `docs/ops`, `COMMS/topics`, `COMMS/inbox` | Hormiguero / Mission Control / COMMS | `VALIDADO_LOCAL` |
| Prompt maestro | `runtime/prompt_master`, `docs/ops/PROMPT_MASTER_*`, workpacks | Control local / Wabi-Sabi / Mission Control | `VALIDADO_LOCAL` |
| Curador SETO | `docs/intake`, `docs/canon/atlas`, `runtime/curador_seto`, WitnessLog | Atlas Main | `VALIDADO_LOCAL` |

## Lectura de sistema

AI Browser aporta una frontera defensiva: fuente web/local -> snapshot -> redaccion -> evidencia -> GhostGate/WitnessLog -> COMMS. No ejecuta navegador real ni descarga.

Lenguaje Observacionista L1 aporta una capa intermedia: `OBSERVAR`, `DOCUMENTAR`, `VERIFICAR`, `ACTUAR`, `HANDOFF` -> `ObservationEnvelope` -> `ActionGate` -> workpack seco -> diff plan no aplicado.

Ciudad de agentes aporta coordinacion: seis agentes existentes, un bus COMMS, mapas vivos y handoffs. No crea agentes nuevos ni promueve un `BLOCK` a `APPROVE`.

Prompt maestro aporta control: traduce 20 prompts a dueños, gates, acciones seguras y workpacks. No ejecuta los carriles bloqueados.

Curador SETO aporta la memoria funcional: fichas, rutas, hashes, archivo frio, duplicados, Atlas y WitnessLog.

## Validacion ejecutada

```powershell
python -m pytest tests\test_source_snapshot.py -q
python -m pytest research\observacionismo-lab\tests -q
python -m py_compile tools\ai_browser\snapshot_url.py tools\release\scan_secrets.py research\observacionismo-lab\l1_to_envelope.py research\observacionismo-lab\l1_programmer_workpack.py research\observacionismo-lab\l1_comms_diff_consumer.py
python COMMS\tools\validate_seto_comms.py --json
```

Resultado observado:

- AI Browser: `13 passed`.
- Observacionismo lab: `34 passed`.
- COMMS validator: `PASS`.
- Schemas JSON nuevos: parse valido.
- Prompt master JSON: parse valido.

## Fronteras

- Nada externo fue publicado.
- No se ejecutaron descargas ni navegacion real.
- No se tocaron pesos, aliases, Qwen, LoRA, deploys, Gumroad, LinkedIn ni GitHub externo.
- Los caches `__pycache__` no son canon; se limpian como residuo tecnico.
- Los fixtures de redaccion usan marcadores sinteticos, no secretos reales.

## Siguiente paso

1. Conectar Mission Control a `COMMS/topics/agent-city-coordination.jsonl`.
2. Convertir AI Browser en panel local de evidencia, sin fetch real.
3. Convertir L1 workpacks en entrada seca para `claudio-local-agent`.
4. Reducir `REVIEW_DUPLICATE` por bloque usando fichas y no por borrado bruto.
