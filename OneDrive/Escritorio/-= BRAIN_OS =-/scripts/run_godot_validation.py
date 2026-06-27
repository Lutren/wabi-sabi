#!/usr/bin/env python3
"""
Script para ejecutar validación headless de Godot (ValidateGameFactoryPluginSystem)
Requiere Godot Engine instalado y disponible en PATH
"""

import subprocess
import sys
import os
from pathlib import Path

# Configuración
GODOT_PROJECT_PATH = Path(r"E:\Medioevo_RPG")
VALIDATION_SCENE = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\02_CLAUDIO\duat_sim\godot\plugins\ValidateGameFactoryPluginSystem.tscn")
VALIDATION_SCRIPT = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\02_CLAUDIO\duat_sim\godot\plugins\validate_game_factory_plugin_system.gd")

# Godot executable paths comunes en Windows
GODOT_PATHS = [
    "godot",
    "godot.exe",
    r"C:\Program Files\Godot\Godot_v4.3-stable_win64.exe",
    r"C:\Program Files (x86)\Godot\Godot_v4.3-stable_win64.exe",
    os.path.expanduser(r"~\AppData\Local\Programs\Godot\Godot_v4.3-stable_win64.exe"),
]


def find_godot():
    """Encontrar ejecutable de Godot"""
    for path in GODOT_PATHS:
        try:
            result = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"Godot encontrado: {path} ({result.stdout.strip()})")
                return path
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return None


def run_headless_validation(godot_exe: str) -> int:
    """Ejecutar validación headless"""
    if not VALIDATION_SCENE.exists():
        print(f"ERROR: Escena de validación no encontrada: {VALIDATION_SCENE}")
        return 1
    
    if not VALIDATION_SCRIPT.exists():
        print(f"ERROR: Script de validación no encontrado: {VALIDATION_SCRIPT}")
        return 1
    
    if not GODOT_PROJECT_PATH.exists():
        print(f"ERROR: Proyecto Godot no encontrado: {GODOT_PROJECT_PATH}")
        return 1
    
    print(f"Ejecutando validación headless...")
    print(f"  Godot: {godot_exe}")
    print(f"  Proyecto: {GODOT_PROJECT_PATH}")
    print(f"  Escena: {VALIDATION_SCENE}")
    
    # Comando: godot --headless --path <project> --script <scene>
    # Para Godot 4.x, usar --headless --path <project> <scene>
    cmd = [
        godot_exe,
        "--headless",
        "--path", str(GODOT_PROJECT_PATH),
        str(VALIDATION_SCENE)
    ]
    
    print(f"Comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        print(f"Return code: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
        
        if result.returncode == 0:
            if "MEDIOEVO_GAME_FACTORY_VALIDATION_OK" in result.stdout:
                print("✅ VALIDACIÓN EXITOSA: MEDIOEVO_GAME_FACTORY_VALIDATION_OK")
                return 0
            else:
                print("⚠️ Godot terminó con código 0 pero sin mensaje de éxito")
                return 1
        else:
            print("❌ VALIDACIÓN FALLÓ")
            return result.returncode
            
    except subprocess.TimeoutExpired:
        print("❌ TIMEOUT: La validación excedió 120 segundos")
        return 1
    except Exception as e:
        print(f"❌ ERROR ejecutando Godot: {e}")
        return 1


def main():
    print("=== VALIDACIÓN HEADLESS GODOT - MEDIOEVO GAME FACTORY ===\n")
    
    # Verificar archivos
    print("Verificando archivos...")
    for p, name in [(VALIDATION_SCENE, "Escena"), (VALIDATION_SCRIPT, "Script"), (GODOT_PROJECT_PATH, "Proyecto")]:
        if p.exists():
            print(f"  ✅ {name}: {p}")
        else:
            print(f"  ❌ {name}: {p} - NO ENCONTRADO")
            return 1
    
    # Buscar Godot
    print("\nBuscando Godot Engine...")
    godot_exe = find_godot()
    if not godot_exe:
        print("❌ Godot Engine no encontrado en PATH ni ubicaciones comunes")
        print("Instala Godot 4.3+ y asegúrate de que esté en PATH")
        return 1
    
    # Ejecutar validación
    print("\nEjecutando validación...")
    return run_headless_validation(godot_exe)


if __name__ == "__main__":
    sys.exit(main())