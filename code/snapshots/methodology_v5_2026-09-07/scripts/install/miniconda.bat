@echo off
setlocal

REM ==================================================
REM Configuracion
REM ==================================================

set "INSTALL_DIR=%USERPROFILE%\miniconda3"
set "CONDA_EXE=%INSTALL_DIR%\Scripts\conda.exe"
set "CONDA_BAT=%INSTALL_DIR%\condabin\conda.bat"

set "INSTALLER=%TEMP%\Miniconda3-latest-Windows-x86_64.exe"
set "MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"

echo ==================================================
echo Instalador de Miniconda
echo ==================================================
echo.

REM ==================================================
REM 0. Verificar curl.exe
REM ==================================================

where curl.exe >nul 2>nul

if errorlevel 1 (
    echo ERROR: No se encontro curl.exe.
    echo Windows 10/11 normalmente ya lo incluye.
    pause
    exit /b 1
)

REM ==================================================
REM 1. Instalar Miniconda solo si no existe conda.exe
REM ==================================================

if exist "%CONDA_EXE%" (
    echo Miniconda ya esta instalado:
    echo     %INSTALL_DIR%
) else (
    echo Miniconda no esta instalado en:
    echo     %INSTALL_DIR%
    echo.
    echo Descargando instalador oficial...
    echo.

    curl.exe -L -o "%INSTALLER%" "%MINICONDA_URL%"

    if errorlevel 1 (
        echo.
        echo ERROR: No se pudo descargar Miniconda.
        pause
        exit /b 1
    )

    echo.
    echo Instalando Miniconda en modo silencioso...
    echo Ruta:
    echo     %INSTALL_DIR%
    echo.

    start /wait "" "%INSTALLER%" /InstallationType=JustMe /RegisterPython=0 /AddToPath=0 /S /D=%INSTALL_DIR%

    if errorlevel 1 (
        echo.
        echo ERROR: fallo la instalacion de Miniconda.
        pause
        exit /b 1
    )
)

echo.

REM ==================================================
REM 2. Verificar instalacion
REM ==================================================

if not exist "%CONDA_EXE%" (
    echo ERROR: No se encontro conda.exe despues de la instalacion:
    echo     %CONDA_EXE%
    echo.
    echo Posibles causas:
    echo   - La instalacion fallo.
    echo   - La ruta contiene espacios raros.
    echo   - El instalador cambio su comportamiento.
    pause
    exit /b 1
)

echo ==================================================
echo Verificando conda...
echo ==================================================
echo.

"%CONDA_EXE%" --version

if errorlevel 1 (
    echo.
    echo ERROR: conda existe, pero no pudo ejecutarse correctamente.
    pause
    exit /b 1
)

echo.

REM ==================================================
REM 3. Inicializar conda para PowerShell y CMD
REM ==================================================

echo ==================================================
echo Inicializando conda para PowerShell y CMD...
echo ==================================================
echo.

"%CONDA_EXE%" init powershell
"%CONDA_EXE%" init cmd.exe

echo.

REM ==================================================
REM 4. Configuracion limpia
REM ==================================================

echo ==================================================
echo Configurando conda...
echo ==================================================
echo.

"%CONDA_EXE%" config --set auto_activate_base false

if errorlevel 1 (
    echo.
    echo ADVERTENCIA: No se pudo configurar auto_activate_base false.
    echo Puedes correr manualmente despues:
    echo     conda config --set auto_activate_base false
)

echo.

REM ==================================================
REM 5. Verificacion final
REM ==================================================

echo ==================================================
echo Verificacion final
echo ==================================================
echo.

"%CONDA_EXE%" info --envs

echo.
echo ==================================================
echo Listo.
echo Cierra y vuelve a abrir PowerShell, CMD o VS Code.
echo Luego prueba:
echo.
echo     conda --version
echo     conda info --envs
echo.
echo Para crear un ambiente:
echo.
echo     conda create -n py312 python=3.12 -y
echo     conda activate py312
echo     python --version
echo ==================================================

if /I not "%NO_PAUSE%"=="1" pause
endlocal
