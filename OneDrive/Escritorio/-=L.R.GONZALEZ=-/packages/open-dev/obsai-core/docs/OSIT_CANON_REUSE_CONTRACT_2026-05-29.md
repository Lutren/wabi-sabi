# OSIT — Contrato de reuso canónico (obsai-core)

**Fecha:** 2026-05-29 · **Estado:** CERTEZA (verificado leyendo el código) ·
**Calibración:** `DEMO_ONLY` (los umbrales NO son claims de producto).

`obsai-core` es la **única fuente de verdad (SoT)** para gobernanza epistémica OSIT
en el stack MEDIOEVO / Observacionismo. Todo cableado **nuevo** (wabisabi, duat, motor
gráfico, firmware host/UEFI, servicio Windows) debe importar de aquí o replicar estas
constantes citando este documento. No se renumeran umbrales sin decisión de canon explícita.

---

## 1. Contrato de reuso (Python, `obsai_core`)

| Capacidad | Import | Firma | Origen |
|---|---|---|---|
| ActionGate | `from obsai_core import evaluate_action, DEFAULT_GATE_CONFIG` | `evaluate_action(action: dict, config: dict\|None=None) -> dict` | `gate.py:294` |
| Régimen | `from obsai_core import estimate_regime, Regime` | `estimate_regime(residue) -> Regime` | `metrics.py:58` |
| R desde señales | `from obsai_core import estimate_residue_from_signals` | `estimate_residue_from_signals(signals: Sequence[str]) -> float` | `metrics.py:42` |
| Residuo (tracker) | `from obsai_core import ResidueTracker` | `.add/.resolve/.unresolved()/.residue/.phi_eff/.report()` | `residue.py:45` |
| Fingerprint | `from obsai_core import stable_fingerprint, SessionFingerprint` | `stable_fingerprint(data) -> hex`; `SessionFingerprint(...).to_dict()` | `fingerprint.py:12,17` |

`evaluate_action` devuelve `{schemaVersion:"obsai.action_gate.v1", status:"APPROVE|REVIEW|BLOCK",
theta, scores{R,phi_eff,...}, residue{missing_evidence,contradictions,assumptions,unresolved,
policy_violations,R}, reasons, config, claims}`. El bloque `claims` ya trae los disclaimers
`DEMO_ONLY` / `NO_PRODUCT_CLAIMS` — **no los quites** al reusar.

`SessionFingerprint.to_dict()` autoestampa el campo `fingerprint` (SHA-256 de JSON canónico
sobre todo menos `fingerprint`). Para un handoff: instanciar, volcar `to_dict()`, persistir.

## 2. Umbrales canónicos

### 2.1 Escalera de régimen — `estimate_regime(R)` (`metrics.py:58`)
Límites estrictos `<`:

| R | Régimen |
|---|---|
| `R < 0.15` | `OPTIMO` |
| `0.15 ≤ R < 0.30` | `FUNCIONAL` |
| `0.30 ≤ R < 0.45` | `PRE_JAMMING` |
| `0.45 ≤ R < 0.60` | `JAMMING_TEMPRANO` |
| `R ≥ 0.60` | `JAMMING` |

### 2.2 Gate — `DEFAULT_GATE_CONFIG` (`gate.py:8`)
`theta_approve=0.22`, `theta_review=0.10`, `residue_review=0.30`, `residue_block=0.60`,
`high_risk=0.80`, `low_reversibility=0.30`, `balance_min=0.12`, `balance_max=0.90`,
`jamming_threshold=1.0`, `selectivity_review=0.35`, `calibration_review=0.35`.

BLOCK si: `risk≥0.80 ∧ reversibility≤0.30`; `R≥0.60`; claim científico/controlado sin
evidencia verificada; `hard_boundary_*` (acción o tag de frontera dura); receptor requerido
ausente/no autorizado. REVIEW (si no BLOCK): `theta<0.10`; o `theta<0.22 ∨ R≥0.30`; o
cualquier `policy_violation`. En otro caso APPROVE.

### 2.3 R desde señales — `estimate_residue_from_signals` (`metrics.py:42`)
0 señales→`0.10`, 1→`0.20`, 2→`0.32`, 3→`0.45`, 4→`0.58`, ≥5→`0.70`
(sobre el conjunto `JAMMING_SIGNALS`).

### 2.4 Puente R → estado epistémico (4 estados) — **RATIFICADO y promovido (2026-05-29)**
obsai-core ahora exporta `estimate_epistemic_state(R) -> EpistemicState` (`metrics.py`),
canónico junto al eje régimen:

```python
from obsai_core import estimate_epistemic_state, EpistemicState
```

| R | Régimen | Estado epistémico |
|---|---|---|
| `R < 0.15` | OPTIMO | `CERTEZA` |
| `0.15 ≤ R < 0.45` | FUNCIONAL / PRE_JAMMING | `INFERENCIA` |
| `0.45 ≤ R < 0.60` | JAMMING_TEMPRANO | `INCOGNITA` |
| `R ≥ 0.60` | JAMMING | `BLOQUEADO` |

Anclado en la escalera §2.1 y consistente con `osit_gates.c:115` (`R≤0.15→CERTEZA`).
`EpistemicState` es `str, Enum`, así que compara igual a su string (`== "CERTEZA"`) y es
JSON-serializable. Los consumidores Python (duat) lo importan; el motor gráfico TS mantiene
una réplica citada (`ositCanon.ts`) por no poder importar Python. Calibración `DEMO_ONLY`.

## 3. Estado de alineación por subsistema (2026-05-29)

| Subsistema | Eje régimen | Notas |
|---|---|---|
| **obsai-core** | **CANON** | SoT. `pytest` = 71 verde. |
| **firmware** (`osit_firmware`) | ✅ alineado | `osit_gates.c:66` y `osit_edge.c:29` replican §2.1 literalmente (ver `osit_gates.h:43`). Gate edge usa `phi_eff≥0.60` y `R_BLOCK=0.80` (más permisivo que el gate Python a propósito; documentado). |
| **wabisabi** (`apps/local/wabi-sabi`) | ✅ consume obsai-core | vía `core/observation_claim_adapter.py`. WS1 endurece puntos sueltos. |
| **duat** (`duat-genesis`, `duat-predictive-registry`) | ⚠️ ciego a estado | residue-aware pero reimplementa gates; WS2 adopta `evaluate_action`. |
| **motor gráfico** (`04_APPS/motor_grafico`) | ❌ bins ad-hoc | `gameEventBridge.ts` usa `0.3/0.55/0.8`; WS3 los reemplaza por §2.1/§2.4 vía `ositCanon.ts`. |

> **Corrección al plan:** el plan original marcaba el firmware con umbrales divergentes
> (`FUNCIONAL≤0.35 … JAMMING>0.80`). **Eso ya no es cierto**: el firmware fue reconciliado
> al canon obsai-core. La única divergencia de régimen viva es el motor gráfico (WS3).

## 4. Reglas transversales al reusar
- No promover INFERENCIA→CERTEZA ni compilar como hecho un claim BLOQUEADO.
- Conservar disclaimers `DEMO_ONLY` / `publication_gate=BLOCK`.
- INCOGNITA/BLOQUEADO en una decisión consecuente ⇒ al menos REVIEW; preferir BLOCK en duat.
- Idioma de artefactos de usuario: es-MX, "tú".
