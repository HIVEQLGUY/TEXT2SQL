@echo off
setlocal

set "NODE_EXE=C:\Users\24796\AppData\Local\OpenAI\Codex\runtimes\cua_node\1b23c930bdf84ed6\bin\node.exe"
set "SSF_ROOT=C:\Users\24796\.codex\plugins\cache\MageByte-Zero\spec-superflow"
set "SSF_CLI=%SSF_ROOT%\scripts\spec-superflow.mjs"

if not exist "%NODE_EXE%" (
  set "NODE_EXE=node"
)

if not exist "%SSF_CLI%" (
  echo spec-superflow CLI was not found at "%SSF_CLI%". Reinstall plugin spec-superflow@spec-superflow. 1>&2
  exit /b 1
)

pushd "%SSF_ROOT%" >nul
"%NODE_EXE%" "%SSF_CLI%" doctor
set "EXIT_CODE=%ERRORLEVEL%"
popd >nul
exit /b %EXIT_CODE%
