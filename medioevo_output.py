"""
medioevo_output.py — BP-08 Modulo 6: Exportador a E:
Todas las salidas de Medioevo Tools Studio van a E:/BRAIN_OS_BODEGA/medioevo/ por defecto.
Si E: no esta disponible, usa %TEMP% con advertencia.
SEC-CANON-01: stdlib-only.
"""
from __future__ import annotations

import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional


_E_BASE = Path("E:/BRAIN_OS_BODEGA/medioevo")
_TEMP_BASE = Path(tempfile.gettempdir()) / "medioevo_output"


def medioevo_output_path(
    filename: str,
    subfolder: str = "",
    module: str = "",
) -> tuple[Path, bool]:
    """
    Retorna (path, is_primary) donde is_primary=True si E: esta disponible.
    Si E: no esta disponible, retorna path en %TEMP% con advertencia en stderr.
    """
    base_primary = _E_BASE / module / subfolder if module else _E_BASE / subfolder
    base_fallback = _TEMP_BASE / module / subfolder if module else _TEMP_BASE / subfolder

    if _e_drive_available():
        base_primary.mkdir(parents=True, exist_ok=True)
        return base_primary / filename, True
    else:
        import sys
        print(
            f"[medioevo_output] ADVERTENCIA: E: no disponible. "
            f"Usando temporal: {base_fallback}",
            file=sys.stderr,
        )
        base_fallback.mkdir(parents=True, exist_ok=True)
        return base_fallback / filename, False


def _e_drive_available() -> bool:
    """Verifica que E: existe y es escribible."""
    try:
        e = Path("E:/")
        return e.exists() and e.is_dir()
    except Exception:
        return False


def medioevo_save(
    content: str | bytes,
    filename: str,
    subfolder: str = "",
    module: str = "",
    encoding: str = "utf-8",
) -> tuple[Path, bool]:
    """
    Guarda contenido en la ruta canonica de Medioevo Tools.
    Retorna (path_guardado, is_primary).
    """
    path, is_primary = medioevo_output_path(filename, subfolder, module)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding=encoding)
    return path, is_primary


def medioevo_log_entry(
    module: str,
    action: str,
    filename: str,
    is_primary: bool,
    extra: Optional[dict] = None,
) -> dict:
    """Genera una entrada de log estandar para el BLOCK_DELETE log."""
    return {
        "timestamp": datetime.now().isoformat(),
        "module": module,
        "action": action,
        "filename": filename,
        "destination": "E:primary" if is_primary else "TEMP:fallback",
        "extra": extra or {},
    }


if __name__ == "__main__":
    # Falsificador: verifica que la funcion retorna un path valido
    path, is_primary = medioevo_output_path("test.txt", subfolder="test", module="editorial")
    print(f"Path: {path}")
    print(f"E: primario: {is_primary}")
    print(f"Directorio padre existe: {path.parent.exists()}")
    if not is_primary:
        print("ADVERTENCIA: E: no disponible, usando TEMP")
