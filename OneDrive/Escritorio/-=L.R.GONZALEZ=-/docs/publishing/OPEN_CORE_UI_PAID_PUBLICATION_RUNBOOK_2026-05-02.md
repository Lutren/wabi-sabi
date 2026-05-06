# OPEN_CORE_UI_PAID_PUBLICATION_RUNBOOK_2026-05-02

Decision aplicada: tecnologia abierta, UI/wrapper/agentes como producto comercial.

Actualizacion ejecutada 2026-05-02:

- GitHub publico verificado: `obs-safe-integration-kit`, `obsai-core`,
  `residueos`, `observacionismo-gate`, `data-curation-observatory` y
  `observational-calibration-toolkit`; DUAT update: `duat-genesis` publicado en
  `https://github.com/Lutren/duat-genesis`.
- Gumroad publicado: `MEDIOEVO Agent Ops Pack` y `DUAT Templates`.
- Website desplegada: Cloudflare Pages `medioevo-site` con home,
  `software.html` y `apps.html` verificados en `https://medioevo.space/`.
- Evidencia consolidada:
  `qa_artifacts\release_validation\publication-live-verification-2026-05-02.json`.
- Evidencia DUAT:
  `qa_artifacts\release_validation\duat-publication-live-verification-2026-05-02.json`.

## Secuencia

1. Open core primero: publicar solo staging limpio, con `CLAIMS.md`, `PRIVATE_EXCLUSIONS.md`, LICENSE, README, tests y secret scan.
2. Website despues: crear pagina "Agentes MEDIOEVO" que conecte open core, demos y productos pagos.
3. Gumroad despues: vender instaladores, bundles, plantillas premium y soporte.
4. GitHub Sponsors: apoyo a mantenimiento, demos y herramientas open, no prometer acceso a IP privada.
5. Productos comerciales: publicar uno por uno con QA limpia y evidencia de URL final.

## Gate externo

Aunque el operador autorizo push/publicacion, cada accion externa requiere:

- repo o producto destino exacto;
- working tree revisado por ruta;
- secret scan `count_reported=0` sobre el paquete/staging;
- path scrub sin rutas locales privadas;
- claim scan limpio;
- private game boundary limpio;
- ActionGate/host gate en `APPROVE`, o override humano documentado solo para
  host `REVIEW` con scans limpios;
- verificacion post-publicacion antes de afirmar "publicado".

## Orden recomendado

| orden | salida | razon |
|---:|---|---|
| 1 | `data-curation-observatory`, `residueos-core`, `obsai-core` | menor riesgo, alta utilidad, public-safe |
| 2 | `neurostate-ui`, `obs-info-kernel-lite` | requieren claims mas cuidadosos; `duat-genesis` ya quedo publicado |
| 3 | website indice `Agentes MEDIOEVO` | base desplegada; falta seguir agregando fichas y capturas por producto |
| 4 | FlujoCRM Windows-first | comercial claro, falta QA limpia/firma/legal |
| 5 | Asistente, Mini Office, Argus | dependen de mejor unificacion UI/agent shell |
| 6 | Wave FC | vender cuando DOCX visual/legal/listing esten cerrados |

## Entregable comercial minimo por app

- instalador o ZIP final;
- README usuario;
- licencia comercial;
- privacidad/terms/refund/support;
- ficha agente visible;
- public-safe screenshots;
- listing Gumroad;
- landing website;
- smoke/build/test evidence;
- limitaciones y claims permitidos.
