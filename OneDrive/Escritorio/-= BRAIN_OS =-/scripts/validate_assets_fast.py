#!/usr/bin/env python3
"""
Script de validación rápida de assets consolidados
Solo verifica estructura y conteos (sin hashing completo)
"""

import os
import json
from pathlib import Path
from collections import defaultdict

ASSETS_ROOT = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\assets")
REPORTS_DIR = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\reports")

EXPECTED_STRUCTURE = {
    "images/characters": {"min_files": 100},
    "images/environments": {"min_files": 50},
    "images/tcg": {"min_files": 500},
    "images/ui": {"min_files": 20},
    "images/visuals": {"min_files": 150},
    "images/sprites": {"min_files": 50},
}

OLD_DIRS = ["thumbnails", "img", "WABI_VISUALS", "sprites"]


def scan_assets_fast() -> dict:
    """Escanear estructura actual de assets (rápido, sin hash)"""
    result = {
        "total_files": 0,
        "total_size_mb": 0,
        "by_directory": {},
        "by_extension": defaultdict(int),
        "missing_expected": [],
        "old_dirs_exist": [],
    }
    
    for root, dirs, files in os.walk(ASSETS_ROOT):
        rel_root = Path(root).relative_to(ASSETS_ROOT)
        
        # Skip reports and other non-asset dirs
        if any(part in str(rel_root) for part in ["reports", "scripts", ".git", "__pycache__"]):
            continue
            
        for f in files:
            fpath = Path(root) / f
            try:
                size = fpath.stat().st_size
                ext = fpath.suffix.lower()
                
                result["total_files"] += 1
                result["total_size_mb"] += size / (1024 * 1024)
                result["by_extension"][ext] += 1
                
                dir_key = str(rel_root)
                if dir_key not in result["by_directory"]:
                    result["by_directory"][dir_key] = {"count": 0, "size_mb": 0}
                result["by_directory"][dir_key]["count"] += 1
                result["by_directory"][dir_key]["size_mb"] += size / (1024 * 1024)
                
            except Exception as e:
                print(f"Error procesando {fpath}: {e}")
    
    # Check expected structure
    for exp_dir, exp_config in EXPECTED_STRUCTURE.items():
        full_path = ASSETS_ROOT / exp_dir
        if full_path.exists():
            count = sum(1 for _ in full_path.rglob("*") if _.is_file())
            if count < exp_config["min_files"]:
                result["missing_expected"].append({
                    "dir": exp_dir,
                    "expected_min": exp_config["min_files"],
                    "actual": count,
                    "status": "WARNING"
                })
        else:
            result["missing_expected"].append({
                "dir": exp_dir,
                "expected_min": exp_config["min_files"],
                "actual": 0,
                "status": "MISSING"
            })
    
    # Check old dirs are gone
    for old_dir in OLD_DIRS:
        if (ASSETS_ROOT / old_dir).exists():
            result["old_dirs_exist"].append(old_dir)
    
    return result


def validate_references():
    """Validar que no hay referencias rotas en código"""
    code_dirs = [
        Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\02_CLAUDIO"),
        Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\apps\medioevo-tools"),
    ]
    
    old_patterns = [
        "assets/thumbnails",
        "assets/img/",
        "assets/WABI_VISUALS",
        "assets/sprites/",
    ]
    
    new_patterns = [
        "assets/images/characters",
        "assets/images/environments",
        "assets/images/tcg",
        "assets/images/ui",
        "assets/images/visuals",
        "assets/images/sprites",
    ]
    
    issues = []
    valid_refs = []
    
    for code_dir in code_dirs:
        if not code_dir.exists():
            continue
        for ext in [".py", ".gd", ".js", ".ts", ".html", ".json", ".md"]:
            for f in code_dir.rglob(f"*{ext}"):
                try:
                    content = f.read_text(encoding="utf-8", errors="ignore")
                    for pattern in old_patterns:
                        if pattern in content:
                            issues.append({
                                "file": str(f.relative_to(code_dir.parent)),
                                "pattern": pattern,
                                "type": "OLD_REFERENCE"
                            })
                    for pattern in new_patterns:
                        if pattern in content:
                            valid_refs.append({
                                "file": str(f.relative_to(code_dir.parent)),
                                "pattern": pattern
                            })
                except Exception:
                    pass
    
    return {"issues": issues, "valid_refs": valid_refs}


def generate_report(result: dict, refs: dict):
    """Generar reporte de validación"""
    from datetime import datetime
    report = []
    report.append("# REPORTE DE VALIDACIÓN DE ASSETS CONSOLIDADOS")
    report.append(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    report.append("## RESUMEN GENERAL")
    report.append(f"- **Total archivos:** {result['total_files']}")
    report.append(f"- **Tamaño total:** {result['total_size_mb']:.2f} MB")
    report.append(f"- **Directorios antiguos existentes:** {len(result['old_dirs_exist'])}")
    report.append("")
    
    report.append("## ESTRUCTURA POR DIRECTORIO")
    report.append("")
    report.append("| Directorio | Archivos | Tamaño (MB) |")
    report.append("|------------|----------|-------------|")
    for d, info in sorted(result["by_directory"].items()):
        report.append(f"| {d} | {info['count']} | {info['size_mb']:.2f} |")
    report.append("")
    
    report.append("## EXTENSIONES")
    report.append("")
    report.append("| Extensión | Cantidad |")
    report.append("|-----------|----------|")
    for ext, count in sorted(result["by_extension"].items(), key=lambda x: -x[1]):
        report.append(f"| {ext} | {count} |")
    report.append("")
    
    report.append("## VERIFICACIÓN ESTRUCTURA ESPERADA")
    report.append("")
    if result["missing_expected"]:
        report.append("| Directorio | Esperado mín | Actual | Estado |")
        report.append("|------------|--------------|--------|--------|")
        for m in result["missing_expected"]:
            report.append(f"| {m['dir']} | {m['expected_min']} | {m['actual']} | {m['status']} |")
    else:
        report.append("✅ Todos los directorios esperados existen con archivos suficientes")
    report.append("")
    
    report.append("## DIRECTORIOS ANTIGUOS")
    report.append("")
    if result["old_dirs_exist"]:
        report.append("⚠️ **Directorios antiguos aún existen:**")
        for d in result["old_dirs_exist"]:
            report.append(f"- {d}")
    else:
        report.append("✅ Todos los directorios antiguos eliminados correctamente")
    report.append("")
    
    report.append("## VALIDACIÓN DE REFERENCIAS EN CÓDIGO")
    report.append("")
    if refs["issues"]:
        report.append(f"⚠️ **{len(refs['issues'])} referencias antiguas encontradas:**")
        for i in refs["issues"][:20]:
            report.append(f"- {i['file']}: `{i['pattern']}`")
    else:
        report.append("✅ Sin referencias a directorios antiguos")
    report.append("")
    if refs["valid_refs"]:
        report.append(f"✅ **{len(refs['valid_refs'])} referencias válidas a nueva estructura:**")
        for v in refs["valid_refs"][:10]:
            report.append(f"- {v['file']}: `{v['pattern']}`")
    report.append("")
    
    report.append("---")
    report.append("*Generado automáticamente por validate_assets_fast.py*")
    
    return "\n".join(report)


def main():
    print("=== VALIDACIÓN RÁPIDA DE ASSETS CONSOLIDADOS ===\n")
    
    print("1. Escaneando assets...")
    result = scan_assets_fast()
    print(f"   Total: {result['total_files']} archivos, {result['total_size_mb']:.2f} MB")
    print(f"   Directorios antiguos: {result['old_dirs_exist']}")
    
    print("\n2. Validando referencias en código...")
    refs = validate_references()
    print(f"   Issues: {len(refs['issues'])}")
    print(f"   Referencias válidas: {len(refs['valid_refs'])}")
    
    print("\n3. Generando reporte...")
    report = generate_report(result, refs)
    
    # Guardar reporte
    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / "assets_validation_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"   Reporte guardado en: {report_path}")
    
    # Guardar JSON para procesamiento posterior
    json_path = REPORTS_DIR / "assets_validation.json"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"   JSON guardado en: {json_path}")
    
# Resumen final
    print("\n=== RESUMEN ===")
    ok = True
    if result["old_dirs_exist"]:
        print("WARNING: Directorios antiguos pendientes: " + str(result['old_dirs_exist']))
        ok = False
    if refs["issues"]:
        print("WARNING: " + str(len(refs['issues'])) + " referencias antiguas en codigo")
        for i in refs['issues'][:10]:
            print("  - " + i['file'] + ": " + i['pattern'])
        ok = False
    if result["missing_expected"]:
        for m in result["missing_expected"]:
            if m["status"] == "MISSING":
                print("ERROR: Directorio faltante: " + m['dir'])
                ok = False
    if ok:
        print("OK: VALIDACION EXITOSA - Todo correcto")
    
    return 0 if ok else 1


if __name__ == "__main__":
    exit(main())