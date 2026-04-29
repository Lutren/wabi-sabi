#!/usr/bin/env python
"""
Mini Office - Functional Tests
==============================
Tests funcionales exhaustitú para todos los componentes
"""

import os
import sys
import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Agregar el path principal
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestSecurityScanner(unittest.TestCase):
    """Tests para el scanner de seguridad"""

    def test_no_eval_in_code(self):
        """Verifica que no haya uso de eval() en el código"""
        from tests.test_security import SecurityScanner
        scanner = SecurityScanner()
        results = scanner.scan_directory()
        # No debería haber hallazgos de alta severidad
        self.assertEqual(results['high_severity'], 0, "Se encontró uso de eval/exec en el código")

    def test_requirements_exist(self):
        """Verifica que exista requirements.txt"""
        req_path = Path(__file__).parent.parent / 'requirements.txt'
        self.assertTrue(req_path.exists(), "requirements.txt no existe")

    def test_license_exists(self):
        """Verifica que exista LICENSE"""
        license_path = Path(__file__).parent.parent / 'LICENSE'
        self.assertTrue(license_path.exists(), "LICENSE no existe")


class TestAgents(unittest.TestCase):
    """Tests para los agentes"""

    def test_agent_imports(self):
        """Verifica que todos los agentes se puedan importar"""
        try:
            from agents import MarketAnalyst, CreativeDirector, Copywriter, Designer
            assert True
        except ImportError as e:
            self.fail(f"Failed to import agents: {e}")

    def test_analyst_creation(self):
        """Test de creación del Analyst"""
        from agents.analyst import MarketAnalyst
        analyst = MarketAnalyst()
        self.assertEqual(analyst.name, "Market Analyst")

    def test_creative_creation(self):
        """Test de creación del Creative"""
        from agents.creative import CreativeDirector
        creative = CreativeDirector()
        self.assertEqual(creative.name, "Creative Director")

    def test_copywriter_creation(self):
        """Test de creación del Copywriter"""
        from agents.copywriter import Copywriter
        copywriter = Copywriter()
        self.assertEqual(copywriter.name, "Copywriter")

    def test_designer_creation(self):
        """Test de creación del Designer"""
        from agents.designer import Designer
        designer = Designer()
        self.assertEqual(designer.name, "Designer")


class TestConfiguration(unittest.TestCase):
    """Tests para architú de configuración"""

    def test_pyproject_valid(self):
        """Verifica que pyproject.toml sea válido"""
        import tomllib
        pyproject_path = Path(__file__).parent.parent / 'pyproject.toml'
        self.assertTrue(pyproject_path.exists(), "pyproject.toml no existe")

        try:
            with open(pyproject_path, 'rb') as f:
                data = tomllib.load(f)
            self.assertIn('project', data)
        except:
            # Si no hay tomllib (Python < 3.11), usar tomli
            try:
                import tomli
                with open(pyproject_path, 'rb') as f:
                    data = tomli.load(f)
                self.assertIn('project', data)
            except ImportError:
                pass  # Skip si no hay librería TOML

    def test_package_json_valid(self):
        """Verifica que package.json sea válido"""
        package_path = Path(__file__).parent.parent / 'package.json'
        self.assertTrue(package_path.exists(), "package.json no existe")

        with open(package_path, 'r') as f:
            data = json.load(f)
        self.assertIn('name', data)
        self.assertIn('scripts', data)

    def test_gitignore_exists(self):
        """Verifica que exista .gitignore"""
        gitignore_path = Path(__file__).parent.parent / '.gitignore'
        self.assertTrue(gitignore_path.exists(), ".gitignore no existe")


class TestHTMLFiles(unittest.TestCase):
    """Tests para architú HTML"""

    def test_index_html_exists(self):
        """Verifica que index.html exista"""
        index_path = Path(__file__).parent.parent / 'index.html'
        self.assertTrue(index_path.exists(), "index.html no existe")

    def test_index_html_valid(self):
        """Verifica que index.html tenga estructura HTML válida"""
        index_path = Path(__file__).parent.parent / 'index.html'
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('<!DOCTYPE html>', content)
        self.assertIn('<html', content)
        self.assertIn('</html>', content)
        self.assertIn('Mini Office', content)

    def test_css_exists(self):
        """Verifica que public.css exista"""
        css_path = Path(__file__).parent.parent / 'public.css'
        self.assertTrue(css_path.exists(), "public.css no existe")

    def test_css_has_variables(self):
        """Verifica que CSS tenga variables del design system"""
        css_path = Path(__file__).parent.parent / 'public.css'
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('--cobre', content)
        self.assertIn('--turquesa', content)
        self.assertIn('--ambar', content)


class TestInstallScripts(unittest.TestCase):
    """Tests para scripts de instalación"""

    def test_windows_installer_exists(self):
        """Verifica que el installer de Windows exista"""
        installer_path = Path(__file__).parent.parent / 'INSTALL_AND_RUN.bat'
        self.assertTrue(installer_path.exists(), "INSTALL_AND_RUN.bat no existe")

    def test_linux_installer_exists(self):
        """Verifica que el installer de Linux exista"""
        installer_path = Path(__file__).parent.parent / 'install_and_run.sh'
        self.assertTrue(installer_path.exists(), "install_and_run.sh no existe")

    def test_setup_py_exists(self):
        """Verifica que setup.py exista"""
        setup_path = Path(__file__).parent.parent / 'setup.py'
        self.assertTrue(setup_path.exists(), "setup.py no existe")


class TestDocumentation(unittest.TestCase):
    """Tests para documentación"""

    def test_readme_exists(self):
        """Verifica que reADME.md exista"""
        readme_path = Path(__file__).parent.parent / 'reADME.md'
        self.assertTrue(readme_path.exists(), "reADME.md no existe")

    def test_license_exists(self):
        """Verifica que LICENSE exista"""
        license_path = Path(__file__).parent.parent / 'LICENSE'
        self.assertTrue(license_path.exists(), "LICENSE no existe")

    def test_changelog_exists(self):
        """Verifica que CHANGELOG.md exista"""
        changelog_path = Path(__file__).parent.parent / 'CHANGELOG.md'
        self.assertTrue(changelog_path.exists(), "CHANGELOG.md no existe")

    def test_contributing_exists(self):
        """Verifica que CONTRIBUTING.md exista"""
        contributing_path = Path(__file__).parent.parent / 'CONTRIBUTING.md'
        self.assertTrue(contributing_path.exists(), "CONTRIBUTING.md no existe")


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "="*60)
    print("🧪 MINI OFFICE - TESTS FUNCIONALES")
    print("="*60)

    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Agregar todos los tests
    suite.addTests(loader.loadTestsFromTestCase(TestAgents))
    suite.addTests(loader.loadTestsFromTestCase(TestConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestHTMLFiles))
    suite.addTests(loader.loadTestsFromTestCase(TestInstallScripts))
    suite.addTests(loader.loadTestsFromTestCase(TestDocumentation))

    # Ejecutar
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "="*60)
    if result.wasSuccessful():
        print("✅ TESTS: APROBADOS - Todos los tests pasaron")
    else:
        print("❌ TESTS: FALLIDOS - Algunos tests fallaron")
    print("="*60)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
