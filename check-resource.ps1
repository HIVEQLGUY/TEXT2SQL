param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$ArgsForChecker
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptWin = Join-Path $Root "TEXT2SQL-codex-handoff\scripts\resource_access.py"

if (!(Test-Path -LiteralPath $ScriptWin)) {
  throw "resource_access.py not found: $ScriptWin"
}

$ScriptWsl = (wsl.exe wslpath -a "$ScriptWin").Trim()
wsl.exe -e python3 "$ScriptWsl" @ArgsForChecker
