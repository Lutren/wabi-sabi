# Handoff - Agent City Coordination - 2026-05-06

## ESTADO

- Nodo coordinador: Codex.
- Fuente: `Lobby de Alejandria/0. Prompt maestro de continuidad ME.txt`.
- Fuente SHA256: `DB8791BE402BE2F7C41ACD19359AF406776E18BFE16BF4C5D83FE5DBDE500DB7`.
- Gate general: `REVIEW`.
- Regimen: `LOCAL_REVIEW_ONLY`.
- Host no-write: `MIXTO/REVIEW`, `R=0.442`, `Phi_eff=0.555`, dominante `r_mem`.
- Snapshot pendiente: `active_dedup=389`, `claudio_open=69`.

## CERTEZA

- El prompt maestro esta fichado en `docs/intake/inbox_downloads_lobby_alejandria_current_2026-05-06_FICHAS.md`.
- COMMS tiene seis agentes existentes; no se requiere crear agente nuevo.
- El worktree tiene cambios concurrentes; no se deben tocar archivos ajenos.
- La coordinacion queda limitada a docs y COMMS append-only.

## ACCION

Ruteo inicial:

- `claudio-local-agent`: coordinacion, pending review, handoff, prompts 1/6/7/17/20.
- `claudio-local-autonomy`: mantener `BLOCK` y preparar solo diff-review/workpacks, prompts 6/13.
- `curador-seto`: fichas, fuentes, duplicados, prompts 11/12/14/16/17.
- `hormiguero-mission-control`: vista local de agentes/gates, prompts 7/15/17.
- `publicacion-perfiles-observatorio`: packets y checklists sin publicar, prompts 9/10/18/19.
- `wabi-sabi-sentido-comun`: policy-only y decision ledger, prompts 8/13.

## ARTEFACTO

- Reporte operativo: `docs/ops/AGENT_CITY_COORDINATION_2026-05-06.md`.
- Tema COMMS: `COMMS/topics/agent-city-coordination.jsonl`.
- Inbox Claudio: `COMMS/inbox/claudio-local-agent.jsonl`.

## HANDOFF

Siguiente prompt recomendado: `17. Prompt de continuidad: Agentes especializados / ciudad Claudio`.

No ejecutar:

- publicacion, Gumroad, GitHub, LinkedIn, redes, website deploy;
- daemons o Symphony;
- Qwen 3B pesado, QEMU, alias Ollama, entrenamiento o mutacion de pesos;
- borrado, movimiento o limpieza destructiva;
- carril RPG privado sin handoff dedicado.

Falsadores:

- `COMMS/tools/validate_seto_comms.py --json` falla;
- un agente opera fuera de `may_touch`;
- se usa un estado `BLOCK` como permiso;
- se pierden evidencia, hash, diff o witness;
- se toca trabajo concurrente no propio.
