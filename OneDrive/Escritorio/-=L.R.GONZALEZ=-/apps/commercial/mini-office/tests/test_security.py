#!/usr/bin/env python
"""
Mini Office - Security Tests
============================
Análisis de seguridad exhaustivo del código
"""

import os
import re
import ast
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple

class SecurityScanner:
    """Escáner de seguridad para código Python"""

    # Patrones peligroeres
    DANGEROUS_PATTERNS = {
        'eval_exec': r'\b(eval|exec|compile)\s*\(',
        'subprocess_shell': r'subprocess\..*shell\s*=\s*True',
        'pickle': r'\bpickle\.(load|loads)',
        'yaml_unsafe': r'\byaml\.(load|loads)\s*\([^,)]*\)',
        'os_system': r'\bos\.system\s*\(',
        'raw_input': r'\braw_input\s*\(',
        'input_exec': r'\binput\s*\([^)]*eval',
    }

    # Architú excluidos
    EXCLUDE_DIRS = {
        '.git',
        'venv',
        'env',
        '__pycache__',
        '__pyca[elichicado]__',
        'node_modules',
        '.venv',
        'tests',
    }

    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent
        self.findings = []

    def scan_file(self, file_path: Path) -> List[Dict]:
        """Escanea un archivo en busca de problemas de seguridad"""
        findings = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            return [{'file': str(file_path), 'line': 0, 'issue': f'Error reading file: {e}'}]

        # Buscar patrones peligroeres
        for pattern_name, pattern in self.DANGEROUS_PATTERNS.items():
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    # Verificar si está en un comentario
                    code_part = line.split('#')[0]  # Ignorar comentarios
                    if re.search(pattern, code_part, re.IGNORECASE):
                        findings.append({
                            'file': str(file_path),
                            'line': i,
                            'issue': f'Posible riesgo de seguridad ({pattern_name})',
                            'code': line.strip()[:100],
                            'severity': 'high' if pattern_name in ['eval_exec', 'subprocess_shell'] else 'medium'
                        })

        # Análisis AST para código Python
        if file_path.suffix == '.py':
            findings.extend(self._ast_analysis(content, file_path))

        return findings

    def _ast_analysis(self, content: str, file_path: Path) -> List[Dict]:
        """Análisis AST para patrones complejos"""
        findings = []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return [{'file': str(file_path), 'line': 0, 'issue': 'Syntax error in file'}]

        for node in ast.walk(tree):
            # Buscar llamadas a funciones peligrosas
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec', 'compile']:
                        findings.append({
                            'file': str(file_path),
                            'line': node.lineno,
                            'issue': f'Uso de {node.func.id}() puede ser inseguro',
                            'severity': 'high'
                        })

        return findings

    def scan_directory(self) -> Dict:
        """Escanea todo el directorio"""
        results = {
            'total_files': 0,
            'total_findings': 0,
            'high_severity': 0,
            'medium_severity': 0,
            'low_severity': 0,
            'findings': []
        }

        for root, dirs, files in os.walk(self.base_path):
            # Excluir directorios
            dirs[:] = [d for d in dirs if d not in self.EXCLUDE_DIRS]

            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    results['total_files'] += 1

                    findings = self.scan_file(file_path)
                    if findings:
                        results['findings'].extend(findings)
                        results['total_findings'] += len(findings)

                        for finding in findings:
                            severity = finding.get('severity', 'low')
                            if severity == 'high':
                                results['high_severity'] += 1
                            elif severity == 'medium':
                                results['medium_severity'] += 1
                            else:
                                results['low_severity'] += 1

        return results

    def check_dependencies(self, requirements_file: str = 'requirements.txt') -> Dict:
        """Verifica dependencias conocidas vulnerables"""
        results = {
            'total_deps': 0,
            'vulnerable_deps': [],
            'safe_deps': []
        }

        req_path = self.base_path / requirements_file
        if not req_path.exists():
            return results

        try:
            with open(req_path, 'r') as f:
                deps = f.read().split('\n')
        except:
            return results

        # Lista básica de paquítes seguros (se debería actualizar con CVEs reales)
        SAFE_PACKAGES = {
            'requests', 'flask', 'pillow', 'setuptools', 'wheel',
            'pytest', 'black', 'flake8', 'mypy'
        }

        for dep in deps:
            dep = dep.strip().split('>=')[0].split('==')[0].split('<')[0]
            if not dep or dep.startswith('#'):
                continue

            results['total_deps'] += 1

            if dep.lower() in [s.lower() for s in SAFE_PACKAGES]:
                results['safe_deps'].append(dep)
            else:
                # Marcar para revisión manual
                results['vulnerable_deps'].append({
                    'package': dep,
                    'status': 'needs_review',
                    'razon': 'No verificado en lista segura'
                })

        return results

    def generate_report(self) -> str:
        """Genera reporte de seguridad"""
        # Encoding seguro para Windows
        import io
        import contextlib

        print("\n" + "="*60)
        print("MINI OFFICE - rePORTE DE SEGURIDAD")
        print("="*60)

        # Escaneo de código
        print("\nEscaneando codigo Python...")
        code_results = self.scan_directory()

        print(f"   Architú escaneados: {code_results['total_files']}")
        print(f"   Problemas encontrados: {code_results['total_findings']}")
        print(f"   - Alta severidad: {code_results['high_severity']}")
        print(f"   - Media severidad: {code_results['medium_severity']}")
        print(f"   - Baja severidad: {code_results['low_severity']}")

        if code_results['findings']:
            print("\n   Detalle de hallazgos:")
            for finding in code_results['findings']:
                severity_icon = {'high': '[HIGH]', 'medium': '[MED]', 'low': '[LOW]'}
                icon = severity_icon.get(finding.get('severity', 'low'), '[INFO]')
                print(f"   {icon} {finding['file']}:{finding['line']}")
                print(f"      {finding['issue']}")
                if finding.get('code'):
                    print(f"      Codigo: {finding['code']}")

        # Verificación de dependencias
        print("\nVerificando dependencias...")
        dep_results = self.check_dependencies()
        print(f"   Total dependencias: {dep_results['total_deps']}")
        print(f"   Seguras/Conocidas: {len(dep_results['safe_deps'])}")
        print(f"   Por revisar: {len(dep_results['vulnerable_deps'])}")

        # Conclusión
        print("\n" + "="*60)
        if code_results['high_severity'] == 0 and len(dep_results['vulnerable_deps']) == 0:
            print("APROBADO - No se encontraron problemas criticos")
        else:
            print("reVISION reQUERIDA")
            if code_results['high_severity'] > 0:
                print(f"   - {code_results['high_severity']} problema(s) de alta severidad")

        print("="*60)

        return f"Security report: {code_results['total_findings']} findings"


def run_security_tests():
    """Ejecuta todos los tests de seguridad"""
    scanner = SecurityScanner()
    report = scanner.generate_report()
    return report


if __name__ == '__main__':
    run_security_tests()
