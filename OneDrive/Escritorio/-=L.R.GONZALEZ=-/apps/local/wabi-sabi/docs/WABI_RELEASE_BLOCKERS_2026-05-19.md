# WABI RELEASE BLOCKERS 2026-05-19

Fingerprint: WABI_RELEASE_BLOCKERS_20260519

Este documento separa la capacidad de trabajo local de Wabi de cualquier salida
externa. Wabi puede trabajar localmente, pero GitHub, medioevo.space y assets
publicos siguen gateados.

## Estado por carril

LOCAL WORK: PASS

- CLI Wabi funciona.
- UI local funciona en `http://127.0.0.1:8787/`.
- ConversationEngine funciona.
- Review TaskSpec funciona.
- Gate Preview funciona.
- Apply Local Preview funciona.
- Apply Local funciona para rutas allowlisted.
- Rollback, tests, scans y WitnessLog funcionan.
- TaskSpec multiarchivo esta listo en backend.

GITHUB RELEASE: BLOCK

- El git top-level detectado es `C:\Users\L-Tyr`, un workspace host amplio.
- El worktree esta muy sucio para release seguro.
- El remote de release no esta configurado o no quedo confirmado para este
  carril.
- Hay cambios y carpetas no relacionadas que no deben mezclarse en commit.
- No hay staged-only release diff verificado.

MEDIOEVO.SPACE DEPLOY: BLOCK

- No se debe desplegar sin repo/remote correcto.
- No se debe desplegar sin build/test/release scan limpio.
- No se debe desplegar si el dominio no es exactamente `medioevo.space`.
- No se debe desplegar si el pipeline requiere login, 2FA o credenciales no
  verificadas localmente.

ASSETS PUBLICATION: REVIEW_REQUIRED

- Assets Du WABI fueron procesados y stripped en runtime.
- Publication sigue bloqueada por provenance/licencia incompleta.
- Hay 3 ZIP en `REVIEW_REQUIRED`.
- `publication_allowed=false`.
- No se deben copiar raw zips, vaults, prompts, datasets ni assets privados a
  un destino publico.

## Bloqueadores exactos

- Top-level git detectado en `C:\Users\L-Tyr`.
- Worktree muy sucio.
- Remote no configurado o no confirmado para release.
- Assets Du WABI sin provenance/licencia completa.
- 3 ZIP en REVIEW_REQUIRED.
- `publication_allowed=false`.

## Condiciones para desbloquear GitHub

1. Confirmar repo correcto y top-level no host-wide.
2. Confirmar remote correcto.
3. Separar cambios no relacionados.
4. Revisar diff path-scoped.
5. Ejecutar tests/build requeridos.
6. Ejecutar secret scan focal sobre diff/staged.
7. Ejecutar boundary scan sobre cualquier public/dist.
8. Crear release summary.

## Condiciones para desbloquear medioevo.space

1. GitHub release gate aprobado.
2. Pipeline real identificado, no inventado.
3. Dominio confirmado como `medioevo.space`.
4. Build publico generado desde fuente limpia.
5. Assets publicos solo desde manifest aprobado.
6. HTTP smoke y rutas clave verificadas.

## Condiciones para desbloquear assets

1. Provenance/licencia por asset.
2. Hash SHA256 registrado.
3. Metadata/EXIF sensible removida.
4. Public-safe manifest aprobado.
5. ZIPs revisados o excluidos.
6. `publication_allowed=true` solo tras review explicito.

## Decision actual

Wabi pasa a WORK_MODE_READY para trabajo local.

GitHub, medioevo.space y publicacion de assets quedan fuera del flujo diario
hasta que los blockers anteriores pasen con evidencia.
