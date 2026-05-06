#!/usr/bin/env bash
set -euo pipefail

echo ""
echo "MINI OFFICE - LOCAL REVIEW"
echo ""

echo "[1/4] Checking Python..."
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "ERROR: Python 3.8+ was not found."
  exit 1
fi
echo "Python detected: $($PYTHON_BIN --version)"

echo ""
echo "[2/4] Preparing virtual environment..."
if [ ! -d "venv" ]; then
  "$PYTHON_BIN" -m venv venv
  echo "Virtual environment created."
else
  echo "Existing virtual environment detected."
fi

echo ""
echo "[3/4] Activating environment..."
# shellcheck disable=SC1091
source venv/bin/activate

echo ""
echo "[4/4] Installing dependencies if requirements.txt exists..."
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt --quiet
  echo "Dependencies installed."
else
  echo "requirements.txt not found; continuing with local static app."
fi

echo ""
echo "Launching Mini Office at http://127.0.0.1:8000"
echo "Press Ctrl+C to stop the local server."
echo ""

if [ -f "mini_office.py" ]; then
  python mini_office.py
elif [ -f "index.html" ]; then
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open index.html
  elif command -v open >/dev/null 2>&1; then
    open index.html
  else
    echo "Open index.html manually in your browser."
  fi
else
  echo "ERROR: mini_office.py or index.html not found."
  exit 1
fi
