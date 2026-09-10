@echo off
setlocal EnableExtensions

REM ==================================================
REM Rutas de los scripts hijos
REM ==================================================

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%..\.."
for %%I in ("%PROJECT_ROOT%") do set "PROJECT_ROOT=%%~fI\"
set "CONDA_SCRIPT=%SCRIPT_DIR%miniconda.bat"

REM ==================================================
REM Rutas esperadas de Miniconda
REM ==================================================

set "CONDA_DIR=%USERPROFILE%\miniconda3"
set "CONDA_EXE=%CONDA_DIR%\Scripts\conda.exe"
set "CONDA_PY=%CONDA_DIR%\python.exe"

REM ==================================================
REM Evitar pausas en scripts hijos
REM ==================================================

set "NO_PAUSE=1"

echo ==================================================
echo Instalador maestro: Miniconda + ambiente CMAT
echo ==================================================
echo.

REM ==================================================
REM 0. Verificar que existan los scripts hijos
REM ==================================================

if not exist "%CONDA_SCRIPT%" (
    echo ERROR: No se encontro el script:
    echo     %CONDA_SCRIPT%
    echo.
    echo Pon miniconda.bat en la misma carpeta.
    pause
    exit /b 1
)

REM ==================================================
REM 2. Ejecutar instalador de Miniconda
REM ==================================================

echo ==================================================
echo 2. Ejecutando instalador de Miniconda...
echo ==================================================
echo.

call "%CONDA_SCRIPT%"

if errorlevel 1 (
    echo.
    echo ERROR: fallo miniconda.bat
    pause
    exit /b 1
)

echo.

REM ==================================================
REM 8. Verificar Miniconda
REM ==================================================

echo ==================================================
echo 8. Verificando Miniconda...
echo ==================================================
echo.

if not exist "%CONDA_EXE%" (
    echo ERROR: No se encontro conda:
    echo     %CONDA_EXE%
    pause
    exit /b 1
)

if not exist "%CONDA_PY%" (
    echo ERROR: No se encontro Python de Miniconda:
    echo     %CONDA_PY%
    pause
    exit /b 1
)

"%CONDA_EXE%" --version

if errorlevel 1 (
    echo.
    echo ERROR: conda existe, pero no pudo ejecutarse.
    pause
    exit /b 1
)

"%CONDA_PY%" --version

if errorlevel 1 (
    echo.
    echo ERROR: python.exe de Miniconda existe, pero no pudo ejecutarse.
    pause
    exit /b 1
)

echo.

REM ==================================================
REM 9. Actualizar conda en base
REM ==================================================

echo ==================================================
echo 9. Actualizando conda en el ambiente base...
echo ==================================================
echo.

"%CONDA_EXE%" update -n base conda -y

if errorlevel 1 (
    echo.
    echo ERROR: fallo la actualizacion de conda.
    pause
    exit /b 1
)

echo.
echo Estado de ambientes:
echo.

"%CONDA_EXE%" info --envs

echo.

REM ==================================================
REM 10. Verificar configuracion limpia de conda
REM ==================================================

echo ==================================================
echo 10. Verificando configuracion de conda...
echo ==================================================
echo.

"%CONDA_EXE%" config --show auto_activate_base

echo.

REM ==================================================
REM 12. Crear ambiente cmat314 e instalar proyecto
REM ==================================================

echo ==================================================
echo 12. Preparando ambiente conda: cmat314
echo ==================================================
echo.

set "ENV_NAME=cmat314"

if not exist "%PROJECT_ROOT%pyproject.toml" (
    echo ERROR: No se encontro pyproject.toml en:
    echo     %PROJECT_ROOT%
    echo.
    echo Este bloque asume que el .bat maestro esta en la raiz del proyecto.
    pause
    exit /b 1
)

if not exist "%PROJECT_ROOT%src\run_analysis.py" (
    echo ERROR: No se encontro src\run_analysis.py en:
    echo     %PROJECT_ROOT%
    pause
    exit /b 1
)

echo Verificando si existe el ambiente %ENV_NAME%...
echo.

"%CONDA_EXE%" run -n %ENV_NAME% python --version >nul 2>nul

if errorlevel 1 (
    echo El ambiente %ENV_NAME% no existe. Creandolo con Python 3.14.4...
    echo.

    "%CONDA_EXE%" create -n %ENV_NAME% python=3.14.4 -y

    if errorlevel 1 (
        echo.
        echo ERROR: fallo la creacion del ambiente %ENV_NAME%.
        pause
        exit /b 1
    )
) else (
    echo El ambiente %ENV_NAME% ya existe.
)

echo.
echo Fijando Python 3.14.4 en el ambiente...
echo.

"%CONDA_EXE%" install -n %ENV_NAME% python=3.14.4 -y

if errorlevel 1 (
    echo.
    echo ERROR: no se pudo fijar Python 3.14.4 en %ENV_NAME%.
    pause
    exit /b 1
)

echo.
echo Verificando Python del ambiente...
echo.

"%CONDA_EXE%" run -n %ENV_NAME% python --version

if errorlevel 1 (
    echo.
    echo ERROR: no se pudo ejecutar Python dentro de %ENV_NAME%.
    pause
    exit /b 1
)

echo.
echo Actualizando pip, setuptools y wheel...
echo.

"%CONDA_EXE%" run -n %ENV_NAME% python -m pip install --upgrade pip setuptools wheel

if errorlevel 1 (
    echo.
    echo ERROR: fallo la actualizacion de pip/setuptools/wheel.
    pause
    exit /b 1
)

echo.
echo Instalando el proyecto en modo editable...
echo Proyecto:
echo     %PROJECT_ROOT%
echo.

pushd "%PROJECT_ROOT%"

"%CONDA_EXE%" run -n %ENV_NAME% python -m pip install -e .

if errorlevel 1 (
    popd
    echo.
    echo ERROR: fallo python -m pip install -e .
    pause
    exit /b 1
)

popd

echo.
echo ==================================================
echo Ambiente preparado correctamente.
echo ==================================================
echo.


pause
endlocal
exit /b 0
