# obs-info-kernel

Status: `INTERNAL_RESEARCH / DO_NOT_PUBLISH`

Este paquete se conserva como laboratorio interno. No es release open-source,
no prueba novedades cientificas y no debe usarse como copy publico sin validar
fuentes primarias, licencia y frontera de claims.

Kernel observacionista para dos lineas de investigacion:

1. **Anti-informacion**: informacion que se pierde por divergencia de calibracion, omisiones frente a un nucleo comun y uso de vocabularios distintos para el mismo operador conceptual.
2. **Informacion oscura**: conocimiento relegado, poco visible o subintegrado, detectado por baja visibilidad, rareza conceptual y relevancia para la consulta.
3. **EOR/AIA guardada**: residuo informacional como proxy `R_info = H(M|X)/H(M)` cuando hay distribucion definida, residuo operativo de runtime y guardas epistémicas para impedir que analogias se publiquen como pruebas.
4. **Atlas de Operadores Perdidos**: perfil `K_source` por fuente para comparar dominios por operadores, omisiones, transformaciones, evidencia y residuo, no solo por texto.

El sistema no convierte rareza en verdad. Produce candidatos verificables.

## Instalacion

```bash
cd obs_info_kernel
python -m pip install -e .
```

No requiere dependencias externas.

## Uso rapido

```bash
python -m obs_info_kernel.cli \
  --corpus /ruta/a/corpus \
  --query "anti-informacion informacion oscura observacionismo" \
  --out-dir obs_out
```

Salidas:

- `observacionismo_research_report.md`
- `observacionismo_research_report.json`
- `SESSION_FINGERPRINT.json`
- `NEXT_SESSION_BRIEF.md`

## Modulos

| Modulo | Funcion |
|---|---|
| `anti_information.py` | divergencia, omisiones, nucleo calibrado |
| `dark_information.py` | baja visibilidad, rareza conceptual, relevancia |
| `calibration.py` | equivalencias, brechas de calibracion, invariantes |
| `eor.py` | `R_info`, `R_operational`, `R_total` y `Phi_eff` como proxies acotados |
| `epistemic_guard.py` | etiquetas `[A]/[D]/[C]/[H]/[M]/[X]` para claims |
| `equivalence.py` | test de equivalencia operacional de cinco filtros |
| `operator_profile.py` | `K_source`, conceptos, bordes, omisiones, evidencia y `R_source` |
| `topology.py` | topologia operacional `C_ij` entre perfiles `K_source` como proxy acotado |
| `hypothesis.py` | prioridad de hipotesis por `delta_R`, transferencia, testabilidad, orfandad y sobreclaim |
| `continuity.py` | fingerprint + next session brief |
| `connectors.py` | conectores opcionales OpenAlex/arXiv con fixtures, cache TTL y rate limit |
| `orchestrator.py` | ejecucion completa |

## Hardening local para loops largos

- `HttpClient` soporta `cache_dir`, `ttl_seconds`, `min_interval_seconds` y
  `fixtures` para que OpenAlex/arXiv puedan probarse sin red.
- Si la red falla y existe cache viejo, el cliente puede devolver
  `stale_cache` con `last_status` documentado.
- Si no hay fuentes, `ObservacionismoResearchKernel.analyze()` genera
  `run_status.status=NO_SOURCES`, warning de bloqueo y artefactos de
  continuidad, pero no infiere claims.
- Los conectores siguen siendo opcionales; el kernel base no requiere red ni
  dependencias externas.

## Principio de fidelidad

- Anti-informacion no es informacion falsa.
- Informacion oscura no es verdad por estar oculta.
- El atlas no prueba isomorfismos; propone mapas de operadores y falsadores.
- `R_info` puede modelarse como entropia condicional normalizada; `R_operational`, `R_cognitive` y `R_physical` son capas distintas.
- Prohibido usar "R es entropia" sin capa, distribucion y frontera de dominio.
- La topologia consciente, geometrica o con dependencias externas queda como
  experimento opcional; no entra al kernel base sin caso real y pruebas.
- `topology.py` implementa una version base sin dependencias de `C_ij` como
  proxy operacional entre perfiles `K_source`; no prueba isomorfismo, nueva
  fisica ni topologia consciente.
- EML, si se agrega, debe quedar como modulo experimental, no como prueba.
- La continuidad se preserva mediante artefactos, no memoria magica.
