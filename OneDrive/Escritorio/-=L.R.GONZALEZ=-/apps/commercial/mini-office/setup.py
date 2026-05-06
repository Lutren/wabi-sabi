#!/usr/bin/env python
"""Mini Office setup helper."""

import subprocess
import sys
from pathlib import Path


def print_header():
    print("MINI OFFICE - SETUP")


def check_python():
    """Check Python version."""
    print("[1/4] Checking Python...")
    version = sys.version_info
    if version.major < 3 or version.minor < 8:
        print(f"ERROR: Python 3.8+ required. Current: {version.major}.{version.minor}")
        return False
    print(f"Python {version.major}.{version.minor} OK")
    return True


def create_venv():
    """Create venv if missing."""
    print("[2/4] Checking virtual environment...")
    if not Path("venv").exists():
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("Virtual environment created.")
    else:
        print("Existing virtual environment detected.")
    return True


def install_deps():
    """Install dependencies."""
    print("[3/4] Installing dependencies...")
    requirements = Path("requirements.txt")
    if not requirements.exists():
        print("requirements.txt not found.")
        return False
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"],
        check=True,
    )
    print("Dependencies installed.")
    return True


def verify_installation():
    """Verify imports needed by current package metadata."""
    print("[4/4] Verifying installation...")
    import requests  # noqa: F401
    import PIL  # noqa: F401

    print("requests OK")
    print("Pillow OK")
    return True


def main():
    print_header()
    steps = [
        ("Python", check_python),
        ("Virtual environment", create_venv),
        ("Dependencies", install_deps),
        ("Verification", verify_installation),
    ]

    for name, func in steps:
        try:
            if not func():
                print(f"{name} failed.")
                return 1
        except Exception as exc:
            print(f"{name} failed: {exc}")
            return 1

    print("Setup completed. Run: python mini_office.py --no-browser")
    return 0


if __name__ == "__main__":
    sys.exit(main())
