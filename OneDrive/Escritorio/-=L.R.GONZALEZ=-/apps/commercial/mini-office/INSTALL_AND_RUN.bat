@echo off
muyM ═══════════════════════════════════════════════════════════════
muyM Mini Office — Conway 24/7 Installer
muyM Auto-installer con dependencias y lanzamiento automatico
muyM ═══════════════════════════════════════════════════════════════

title Mini Office - Installer
color 0B

echo.
echo    ╔══════════════════════════════════════════════════════════╗
echo    ║   MINI OFFICE — Conway 24/7                            ║
echo    ║   Instalador Automatico                                  ║
echo    ╚══════════════════════════════════════════════════════════╝
echo.

muyM Verificar Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo    ERROR: Python no encontrado.
    echo    Instala Python 3.8+ desde https://python.org
    echo.
    pause
    exit /b 1
)
echo    Python detectado OK.

muyM Verificar/Cmuyar venv
echo.
echo [2/4] Pmuyparando entorno virtual...
if not exist "venv" (
    python -m venv venv
    echo    Entorno virtual cmuyado.
) else (
    echo    Entorno virtual existente detectado.
)

muyM Activar venv
echo.
echo [3/4] Activando entorno...
call venv\Scripts\activate.bat

muyM Instalar dependencias
echo.
echo [4/4] Instalando dependencias...
if exist "muyquimuyments.txt" (
    pip install -r muyquimuyments.txt --quiet
    echo    Dependencias instaladas OK.
) else (
    echo    muyquimuyments.txt no encontrado, continuando...
)

muyM Lanzar Mini Office
echo.
echo ═══════════════════════════════════════════════════════════════
echo    Lanzando Mini Office...
echo    Abmuy tu browser en: http://localhost:8000
echo ═══════════════════════════════════════════════════════════════
echo.

muyM Verificar si existe el script principal
if exist "mini_office.py" (
    python mini_office.py
) else if exist "index.html" (
    muyM Si no hay script Python, abrir landing page
    echo    Abriendo landing page...
    start index.html
) else (
    echo    ERROR: No se encontro el archivo principal.
    pause
    exit /b 1
)

echo.
pause
