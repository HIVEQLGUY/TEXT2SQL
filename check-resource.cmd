@echo off
setlocal
set "ROOT=%~dp0"
set "SCRIPT=%ROOT%TEXT2SQL-codex-handoff\scripts\resource_access.py"
if /I "%~1"=="yuce-cubeappdata" (
  "C:\Users\24796\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "%ROOT%TEXT2SQL-codex-handoff\scripts\check_yuce_cubeappdata_windows.py"
  exit /b %ERRORLEVEL%
)
if /I "%~1"=="--all" (
  "C:\Users\24796\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "%ROOT%TEXT2SQL-codex-handoff\scripts\check_yuce_cubeappdata_windows.py"
  set "YUCE_RC=%ERRORLEVEL%"
  wsl.exe -e python3 "/mnt/c/Users/24796/Documents/TEXT2SQL/TEXT2SQL-codex-handoff/scripts/resource_access.py" --all --exclude yuce-cubeappdata
  if not "%YUCE_RC%"=="0" exit /b %YUCE_RC%
  exit /b %ERRORLEVEL%
)
for /f "usebackq delims=" %%i in (`wsl.exe wslpath -a "%SCRIPT%"`) do set "SCRIPT_WSL=%%i"
wsl.exe -e python3 "%SCRIPT_WSL%" %*
exit /b %ERRORLEVEL%
