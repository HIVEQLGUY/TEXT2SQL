$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

$repoDir = "C:\Users\24796\Documents\TEXT2SQL\TEXT2SQL-codex-handoff"
$logDir = Join-Path $repoDir "logs"
New-Item -ItemType Directory -Path $logDir -Force | Out-Null
$logFile = Join-Path $logDir "clickhouse-tool-tunnel-supervisor.log"

$distro = "Ubuntu-24.04"
$wslScript = "/mnt/c/Users/24796/Documents/TEXT2SQL/TEXT2SQL-codex-handoff/ops/devbox/clickhouse_tool_tunnel.sh"
$wslLog = "/mnt/c/Users/24796/Documents/TEXT2SQL/TEXT2SQL-codex-handoff/local/logs/clickhouse-tool-tunnel.log"

function Write-Log {
  param([string]$Message)
  $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $Message"
  Add-Content -Path $logFile -Value $line -Encoding UTF8
}

function Invoke-Wsl {
  param([string]$Command)
  & wsl.exe -d $distro -- bash -lc $Command
  return $LASTEXITCODE
}

function Test-SupervisorRunning {
  & wsl.exe -d $distro -- bash -lc "pgrep -f 'clickhouse_tool_tunnel.sh supervise' >/dev/null 2>&1"
  return ($LASTEXITCODE -eq 0)
}

function Start-TunnelSupervisor {
  $cmd = "mkdir -p '/mnt/c/Users/24796/Documents/TEXT2SQL/TEXT2SQL-codex-handoff/local/logs'; nohup bash '$wslScript' supervise >> '$wslLog' 2>&1 &"
  Invoke-Wsl $cmd | Out-Null
}

Write-Log "clickhouse tunnel supervisor starting repo=$repoDir"

while ($true) {
  try {
    Invoke-Wsl "date -Iseconds >/tmp/youmei-clickhouse-tunnel-supervisor.heartbeat" | Out-Null

    if (-not (Test-SupervisorRunning)) {
      Write-Log "WSL clickhouse tunnel supervise process is not running; starting"
      Start-TunnelSupervisor
      Start-Sleep -Seconds 3
    }

    Invoke-Wsl "bash '$wslScript' status" | Out-Null
    if ($LASTEXITCODE -eq 0) {
      Write-Log "clickhouse tunnel healthy"
    } else {
      Write-Log "clickhouse tunnel status failed; attempting start"
      Invoke-Wsl "bash '$wslScript' start" | Out-Null
    }
  } catch {
    Write-Log "supervisor error: $($_.Exception.Message)"
  }

  Start-Sleep -Seconds 60
}
