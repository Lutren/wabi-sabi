# Estado: CERTEZA (extraído de ositCanon.ts)
# Objetivo: Compatibilidad Python para benchmark. Canon ratificado 2026-06-02.

class OSIT_REGIME_R:
    OPTIMO = 0.15
    FUNCIONAL = 0.30
    PRE_JAMMING = 0.45
    JAMMING_TEMPRANO = 0.60

class OSIT_STATE_R:
    CERTEZA_MAX = 0.15
    INFERENCIA_MAX = 0.45
    INCOGNITA_MAX = 0.60


def epistemic_state_from_r(r: float) -> str:
    """Convierte R en estado epistémico canónico (4 estados)."""
    r = max(0, min(1, r))
    if r < OSIT_STATE_R.CERTEZA_MAX:
        return "CERTEZA"
    elif r < OSIT_STATE_R.INFERENCIA_MAX:
        return "INFERENCIA"
    elif r < OSIT_STATE_R.INCOGNITA_MAX:
        return "INCOGNITA"
    else:
        return "BLOQUEADO"