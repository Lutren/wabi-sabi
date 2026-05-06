# Safe rollout

## Fase 0 — Auditoría, sin modificar código

- Clonar repo en carpeta aislada.
- Crear rama `obs-sandbox`.
- No configurar tokens.
- No hacer `git push`.
- No ejecutar comandos destructivos.
- Correr solo tests/linters locales.
- Generar `AUDIT.md`, `HOOKS.md`, `RISKS.md`.

## Fase 1 — Kernel externo

- Instalar este paquete editable.
- Envolver loops existentes sin tocar lógica interna.
- Registrar observaciones y acciones.
- Mantener dry-run.

## Fase 2 — Gate real pero no destructivo

- Permitir solo `pytest`, `git diff`, lectura de archivos no secretos.
- Bloquear `.env`, `credentials.json`, `.ssh`, `.aws`, `.kube`.
- Acciones de red y browser action requieren revisión humana.

## Fase 3 — PR mínimo

- Un solo cambio: adapter/hook + tests.
- Sin reescribir arquitectura del repo externo.
- Sin claims grandiosos.

## Métricas de éxito

- Menos claims sin evidencia.
- Menos comandos peligrosos ejecutables.
- Menos drift intención/acción.
- Session fingerprint reproducible.
- Tests pasan.
