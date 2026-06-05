# Estado: INFERENCIA (basado en G2_arp_RH, B6, R_RECONCILIATION)
# Objetivo: Minimizar R usando campos escalares ζ(r) y Noisy-OR operacional.
# Claim: "Residuo R < 0.15 mediante gradientes ∇R en coordenadas esféricas."
# Falsificador: Benchmark pasa si R < 0.10 en escena de 10k polígonos.
import numpy as np
from ositCanon import OSIT_REGIME_R, epistemic_state_from_r

def estimate_residue(vertices):
    """Estima R a partir de gradiente y Noisy-OR.
    zeta(r) = R(r) * exp(-k * dist(r, obs)), k=0.1.
    """
    vertices = np.array(vertices)
    if len(vertices) < 3:
        return 0.95  # INCOGNITA: polígono degenerado
    
    # Centroide observador (simplificado)
    obs = np.mean(vertices, axis=0)
    # Distancias al observador
    dists = np.linalg.norm(vertices - obs, axis=1)
    # Gradiente ∇ζ normalizado (evita amplificación)
    grad_ζ = np.gradient([0.5 * (1 - np.exp(-0.1 * d)) for d in dists])
    grad_ζ_norm = grad_ζ / (1e-6 + np.max(np.abs(grad_ζ)))  # Normalizar a [0,1]
    # Noisy-OR operacional (clamp en [0,1])
    R_est = 1 - np.prod(1 - np.clip(np.abs(grad_ζ_norm), 0, 1)) * (1 - 0.05)
    R_est = min(R_est, 0.95)  # Techo práctico
    return float(np.clip(R_est, 0, 1))

def render_polygon(vertices):
    """Renderiza polígono con residuo R estimado y estado epistémico."""
    R_est = estimate_residue(vertices)
    state = epistemic_state_from_r(R_est)
    regime = "OPTIMO" if R_est < OSIT_REGIME_R.OPTIMO else \
            "FUNCIONAL" if R_est < OSIT_REGIME_R.FUNCIONAL else \
            "PRE_JAMMING" if R_est < OSIT_REGIME_R.PRE_JAMMING else \
            "JAMMING_TEMPRANO"
    return {
        "R": round(R_est, 4),
        "state": state,
        "regime": regime,
        "polygon": vertices,
        "evidence": {
            "grad_values": [round(float(x), 4) for x in np.gradient([0.5 * (1 - np.exp(-0.1 * d)) for d in np.linalg.norm(np.array(vertices) - np.mean(vertices, axis=0), axis=1)])]
        }
    }