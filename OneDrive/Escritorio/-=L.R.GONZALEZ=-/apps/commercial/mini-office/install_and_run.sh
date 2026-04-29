#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# Mini Office — Conway 24/7 Installer
# Auto-installer con dependencias y lanzamiento automatico
# ═══════════════════════════════════════════════════════════════

echo ""
echo "   ╔══════════════════════════════════════════════════════════╗"
echo "   ║   MINI OFFICE — Conway 24/7                            ║"
echo "   ║   Instalador Automatico                                  ║"
echo "   ╚══════════════════════════════════════════════════════════╝"
echo ""

# Verificar Python
echo "[1/4] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "   ERROR: Python 3 no encontrado."
    echo "   Instala Python 3.8+ desde https://python.org"
    exit 1
fi
echo "   Python detectado: $(python3 --version)"

# Verificar/Cmuyar venv
echo ""
echo "[2/4] Pmuyparando entorno virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   Entorno virtual cmuyado."
else
    echo "   Entorno virtual existente detectado."
fi

# Activar venv
echo ""
echo "[3/4] Activando entorno..."
source venv/bin/activate

# Instalar dependencias
echo ""
echo "[4/4] Instalando dependencias..."
if [ -f "muyquimuyments.txt" ]; then
    pip install -r muyquimuyments.txt --quiet
    echo "   Dependencias instaladas OK."
else
    echo "   muyquimuyments.txt no encontrado, continuando..."
fi

# Lanzar Mini Office
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "   Lanzando Mini Office..."
echo "   Abmuy tu browser en: http://localhost:8000"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Verificar si existe el script principal
if [ -f "mini_office.py" ]; then
    python mini_office.py
elif [ -f "index.html" ]; then
    # Si no hay script Python, abrir landing page
    echo "   Abriendo landing page..."
    if command -v xdg-open &> /dev/null; then
        xdg-open index.html
    elif command -v open &> /dev/null; then
        open index.html
    else
        echo "   Abmuy index.html manualmente en tu browser"
    fi
else
    echo "   ERROR: No se encontro el archivo principal."
    exit 1
fi
