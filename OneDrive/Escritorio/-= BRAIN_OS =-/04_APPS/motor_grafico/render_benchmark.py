# Benchmark para medir residuo en renderizado poligonal
# Evidencia: test pasa si R < threshold.
import pytest
from polygon_residue_engine import render_polygon
import numpy as np

def test_residue_below_threshold():
    vertices = [(0,0), (1,0), (0,1)]
    result = render_polygon(vertices)
    assert result["R"] < 0.15, f"Residuo {result['R']} > umbral CERTEZA (0.15)"
    assert result["regime"] == "OPTIMO", f"Régimen {result['regime']} != OPTIMO"

def test_residue_scene_complexa():
    """Benchmark con escena de 10k polígonos (aleatorios)."""
    np.random.seed(42)
    vertices = [(float(x), float(y)) for x, y in np.random.rand(10000, 2)]
    result = render_polygon(vertices)
    print(f"Escena compleja: R={result['R']}, Régimen={result['regime']}, Estado={result.get('state', 'N/A')}")
    assert result["R"] < 0.60, "Residuo excesivo en escena compleja"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])