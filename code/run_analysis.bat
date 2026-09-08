@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "PROJECT_ROOT=%~dp0"
set "ENV_NAME=cmat314"
set "CONDA_DIR=%USERPROFILE%\miniconda3"
set "CONDA_EXE=%CONDA_DIR%\Scripts\conda.exe"
set "CONDA_BAT=%CONDA_DIR%\condabin\conda.bat"
set "INSTALL_MINICONDA=%PROJECT_ROOT%scripts\install\miniconda.bat"
set "INSTALL_ENV=%PROJECT_ROOT%scripts\install\entorno.bat"

echo ==================================================
echo Actualizacion de figuras y reporte CMAT
echo ==================================================
echo.

if not exist "%PROJECT_ROOT%pyproject.toml" (
    echo ERROR: No se encontro pyproject.toml en:
    echo     %PROJECT_ROOT%
    pause
    exit /b 1
)

if not exist "%PROJECT_ROOT%src\run_analysis.py" (
    echo ERROR: No se encontro src\run_analysis.py en:
    echo     %PROJECT_ROOT%
    pause
    exit /b 1
)

echo Verificando Miniconda...
if not exist "%CONDA_EXE%" (
    echo Miniconda no esta instalado. Ejecutando scripts\install\miniconda.bat...
    if not exist "%INSTALL_MINICONDA%" (
        echo ERROR: No se encontro:
        echo     %INSTALL_MINICONDA%
        pause
        exit /b 1
    )
    call "%INSTALL_MINICONDA%"
    if errorlevel 1 (
        echo ERROR: fallo scripts\install\miniconda.bat.
        pause
        exit /b 1
    )
)

if not exist "%CONDA_EXE%" (
    echo ERROR: Miniconda sigue sin estar disponible:
    echo     %CONDA_EXE%
    pause
    exit /b 1
)

echo.
echo Verificando ambiente conda %ENV_NAME%...
"%CONDA_EXE%" run -n %ENV_NAME% python --version >nul 2>nul
if errorlevel 1 (
    echo El ambiente %ENV_NAME% no existe. Ejecutando scripts\install\entorno.bat...
    if not exist "%INSTALL_ENV%" (
        echo ERROR: No se encontro:
        echo     %INSTALL_ENV%
        pause
        exit /b 1
    )
    call "%INSTALL_ENV%"
    if errorlevel 1 (
        echo ERROR: fallo scripts\install\entorno.bat.
        pause
        exit /b 1
    )
)

"%CONDA_EXE%" run -n %ENV_NAME% python --version >nul 2>nul
if errorlevel 1 (
    echo ERROR: No se pudo usar el ambiente %ENV_NAME%.
    pause
    exit /b 1
)

if not exist "%CONDA_BAT%" (
    echo ERROR: No se encontro conda.bat:
    echo     %CONDA_BAT%
    pause
    exit /b 1
)

echo.
echo Activando ambiente %ENV_NAME%...
call "%CONDA_BAT%" activate %ENV_NAME%
if errorlevel 1 (
    echo ERROR: No se pudo activar %ENV_NAME%.
    pause
    exit /b 1
)

echo.
echo Instalando proyecto en modo editable...
python -m pip install -e .
if errorlevel 1 (
    echo ERROR: fallo python -m pip install -e .
    pause
    exit /b 1
)

echo.
echo Ejecutando analisis...
python src\run_analysis.py
if errorlevel 1 (
    echo ERROR: fallo python src\run_analysis.py.
    pause
    exit /b 1
)

echo.
echo Verificando LuaLaTeX...
where lualatex >nul 2>nul
if errorlevel 1 (
    echo.
    echo ADVERTENCIA: No se encontro lualatex.
    echo Las figuras ya fueron actualizadas, pero falta compilar el PDF.
    echo Instale MiKTeX desde:
    echo     https://miktex.org/download
    echo Luego vuelva a ejecutar este .bat para compilar el reporte.
    pause
    exit /b 0
)

if not exist "%PROJECT_ROOT%reporte\reporte.tex" (
    echo ERROR: No se encontro reporte\reporte.tex.
    pause
    exit /b 1
)

echo.
echo Compilando reporte con LuaLaTeX...
pushd "%PROJECT_ROOT%reporte"
lualatex -interaction=nonstopmode -halt-on-error reporte.tex
if errorlevel 1 (
    popd
    echo ERROR: fallo la compilacion de LaTeX.
    pause
    exit /b 1
)
popd

echo.
echo ==================================================
echo Listo. Figuras actualizadas y reporte compilado.
echo ==================================================
echo.
pause
endlocal
exit /b 0
