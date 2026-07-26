@echo off
setlocal
set "ROOT=%~dp0"
set "PY=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if not exist "%PY%" set "PY=python"
set "EXTRA="

if /i "%~1"=="--help" goto help
if /i "%~1"=="-h" goto help
if /i "%~1"=="--approved" goto approved
if /i "%~1"=="--latest-approved" goto approved
if /i "%~1"=="--rerun" (
  set "EXTRA=--rerun"
  goto approved
)
if "%~1"=="" goto approved

rem Backward-compatible explicit shadow path. Use this when more than one package is ready.
set "SHADOW=%~1"
if /i "%~2"=="--rerun" set "EXTRA=--rerun"
"%PY%" "%ROOT%scripts\warehouse_release.py" --promote-shadow "%SHADOW%" --mode full %EXTRA%
exit /b %ERRORLEVEL%

:approved
if /i "%~1"=="--approved" if /i "%~2"=="--rerun" set "EXTRA=--rerun"
if /i "%~1"=="--latest-approved" if /i "%~2"=="--rerun" set "EXTRA=--rerun"
"%PY%" "%ROOT%scripts\warehouse_release.py" --promote-approved --mode full %EXTRA%
exit /b %ERRORLEVEL%

:help
echo 已批准影子表晋级入口
echo.
echo 直接运行，自动发现唯一可晋级正式发布包：
echo   warehouse-promote.cmd
echo   warehouse-promote.cmd --approved
echo.
echo 多个候选时，显式指定影子发布 YAML：
echo   warehouse-promote.cmd ^<影子发布YAML^>
echo.
echo 允许同一已完成发布重新执行幂等/恢复路径：
echo   warehouse-promote.cmd --approved --rerun
exit /b 0
