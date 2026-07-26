@echo off
setlocal
set "ROOT=%~dp0"
set "PY=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if not exist "%PY%" set "PY=python"
set "SHADOW=%~1"
set "EXTRA="
if /i "%~2"=="--rerun" set "EXTRA=--rerun"
"%PY%" "%ROOT%scripts\warehouse_release.py" --promote-shadow "%SHADOW%" --mode full %EXTRA%
exit /b %ERRORLEVEL%
