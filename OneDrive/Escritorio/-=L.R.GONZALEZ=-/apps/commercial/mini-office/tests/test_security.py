#!/usr/bin/env python
"""Security scanner tests for Mini Office."""

import ast
import os
import re
from pathlib import Path
from typing import Dict, List


class SecurityScanner:
    """Small static scanner for risky Python patterns."""

    DANGEROUS_PATTERNS = {
        "eval_exec": r"\b(eval|exec|compile)\s*\(",
        "subprocess_shell": r"subprocess\..*shell\s*=\s*True",
        "pickle": r"\bpickle\.(load|loads)",
        "yaml_unsafe": r"\byaml\.(load|loads)\s*\([^,)]*\)",
        "os_system": r"\bos\.system\s*\(",
        "raw_input": r"\braw_input\s*\(",
        "input_exec": r"\binput\s*\([^)]*eval",
    }

    EXCLUDE_DIRS = {
        ".git",
        "venv",
        "env",
        "__pycache__",
        "node_modules",
        ".venv",
        "tests",
    }

    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent

    def scan_file(self, file_path: Path) -> List[Dict]:
        """Scan one Python file for risky patterns."""
        findings = []
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            return [{"file": str(file_path), "line": 0, "issue": f"Read error: {exc}"}]

        lines = content.splitlines()
        for pattern_name, pattern in self.DANGEROUS_PATTERNS.items():
            for index, line in enumerate(lines, 1):
                if not re.search(pattern, line, re.IGNORECASE):
                    continue
                code_part = line.split("#")[0]
                if re.search(pattern, code_part, re.IGNORECASE):
                    findings.append(
                        {
                            "file": str(file_path),
                            "line": index,
                            "issue": f"Risky pattern: {pattern_name}",
                            "code": line.strip()[:100],
                            "severity": (
                                "high"
                                if pattern_name in {"eval_exec", "subprocess_shell"}
                                else "medium"
                            ),
                        }
                    )

        if file_path.suffix == ".py":
            findings.extend(self._ast_analysis(content, file_path))

        return findings

    def _ast_analysis(self, content: str, file_path: Path) -> List[Dict]:
        """Use AST parsing for direct risky calls."""
        findings = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return [{"file": str(file_path), "line": 0, "issue": "Syntax error"}]

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile"}:
                findings.append(
                    {
                        "file": str(file_path),
                        "line": node.lineno,
                        "issue": f"Risky call: {node.func.id}()",
                        "severity": "high",
                    }
                )
        return findings

    def scan_directory(self) -> Dict:
        """Scan all Python files under the package root."""
        results = {
            "total_files": 0,
            "total_findings": 0,
            "high_severity": 0,
            "medium_severity": 0,
            "low_severity": 0,
            "findings": [],
        }

        for root, dirs, files in os.walk(self.base_path):
            dirs[:] = [directory for directory in dirs if directory not in self.EXCLUDE_DIRS]
            for filename in files:
                if not filename.endswith(".py"):
                    continue
                file_path = Path(root) / filename
                results["total_files"] += 1
                findings = self.scan_file(file_path)
                if not findings:
                    continue
                results["findings"].extend(findings)
                results["total_findings"] += len(findings)
                for finding in findings:
                    severity = finding.get("severity", "low")
                    results[f"{severity}_severity"] += 1

        return results

    def check_dependencies(self, requirements_file: str = "requirements.txt") -> Dict:
        """Mark known dependencies as safe and unknowns for manual review."""
        results = {
            "total_deps": 0,
            "vulnerable_deps": [],
            "safe_deps": [],
        }
        req_path = self.base_path / requirements_file
        if not req_path.exists():
            return results

        safe_packages = {
            "requests",
            "flask",
            "pillow",
            "setuptools",
            "wheel",
            "pytest",
            "black",
            "flake8",
            "mypy",
        }
        for raw_dep in req_path.read_text(encoding="utf-8").splitlines():
            dep = raw_dep.strip().split(">=")[0].split("==")[0].split("<")[0]
            if not dep or dep.startswith("#"):
                continue
            results["total_deps"] += 1
            if dep.lower() in safe_packages:
                results["safe_deps"].append(dep)
            else:
                results["vulnerable_deps"].append(
                    {
                        "package": dep,
                        "status": "needs_review",
                        "reason": "Package is not in the local allowlist.",
                    }
                )
        return results

    def generate_report(self) -> str:
        """Return a compact security report string."""
        code_results = self.scan_directory()
        dep_results = self.check_dependencies()
        return (
            f"Security report: {code_results['total_findings']} findings, "
            f"{len(dep_results['vulnerable_deps'])} dependency reviews"
        )


def run_security_tests():
    """Run the local security scanner."""
    return SecurityScanner().generate_report()


if __name__ == "__main__":
    print(run_security_tests())
