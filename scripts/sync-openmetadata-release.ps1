param(
  [string]$PackageDir = "C:\Users\24796\Documents\TEXT2SQL\config\warehouse_cleaning\doudian_order_item_v1",
  [string]$Release,
  [ValidateSet("plan", "apply", "verify", "full")]
  [string]$Mode = "plan"
)

$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (-not (Test-Path -LiteralPath $Python)) {
  $Python = "python"
}

$ArgsList = @(
  (Join-Path $Root "scripts\sync_openmetadata_release.py"),
  "--package-dir", $PackageDir,
  "--mode", $Mode
)
if ($Release) {
  $ArgsList += @("--release", $Release)
}

& $Python @ArgsList
exit $LASTEXITCODE
