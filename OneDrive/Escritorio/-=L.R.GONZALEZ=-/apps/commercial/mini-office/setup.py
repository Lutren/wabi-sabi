#!/usr/bin/env python
"""
Mini Office - Setup Script
==========================
Instala dependencias y verifica el entorno
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   MINI OFFICE — Setup                                   ║
    ║   Instalando dependencias...                            ║
    ╚══════════════════════════════════════════════════════════╝
    """)

def check_python():
    """Verifica versión de Python"""
    print("[1/4] Verificando Python...")
    version = sys.version_info
    if version.major < 3 or version.minor < 8:
        print("   ERROR: Python 3.8+ requerido")
        print(f"   Actual: {version.major}.{version.minor}")
        return False
    print(f"   Python {version.major}.{version.minor} OK")
    return True

def create_venv():
    """Crea entorno virtual si no existe"""
    print("[2/4] Verificando entorno virtual...")
    if not Path("venv").exists():
        print("   Creando entorno virtual...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("   Entorno creado OK")
    else:
        print("   Entorno existente detectado")
    return True

def install_deps():
    """Instala dependencias"""
    print("[3/4] Instalando dependencias...")
    requirements = Path("requirements.txt")
    if requirements.exists():
        subprocess.run([
            sys.executable, "-m", "pip", "install",
            "-r", "requirements.txt", "--quiet"
        ], check=True)
        print("   Dependencias instaladas OK")
    else:
        print("   requirements.txt no encontrado")
        return False
    return True

def verify_installation():
    """Verifica instalación"""
    print("[4/4] Verificando instalación...")
    try:
        import requests
        import PIL
        print("   requests: OK")
        print(f"   Pillow: OK")
    except ImportError as e:
        print(f"   ERROR: {e}")
        return False
    return True

def main():
    print_header()

    steps = [
        ("Python", check_python),
        ("Entorno virtual", create_venv),
        ("Dependencias", install_deps),
        ("Verificación", verify_installation),
    ]

    success = True
    for name, func in steps:
        try:
            if not func():
                print(f"   ❌ {name} falló")
                success = False
                break
        except Exception as e:
            print(f"   ❌ {name} falló: {e}")
            success = False
            break

    print()
    if success:
        print("═══════════════════════════════════════════════════════════════")
        print("   Setup completado con éxito!")
        print("   Ejecuta: python mini_office.py")
        print("═══════════════════════════════════════════════════════════════")
    else:
        print("═══════════════════════════════════════════════════════════════")
        print("   Hubo errores en el setup.")
        print("   revisa los mensajes anteriores.")
        print("═══════════════════════════════════════════════════════════════")
        sys.exit(1)

if __name__ == "__main__":
    main()
