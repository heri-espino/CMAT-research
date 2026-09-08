@echo off
setlocal
cd /d "%~dp0"
python src\run_study.py
if errorlevel 1 (
  echo.
  echo [ERROR] El estudio no pudo completarse.
  exit /b 1
)
echo.
echo [OK] Resultados en outputs\study
endlocal
