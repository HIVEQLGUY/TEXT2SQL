param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$ErrorActionPreference = "Stop"

$nodeCandidates = @(
    "C:\Users\24796\AppData\Local\OpenAI\Codex\runtimes\cua_node\1b23c930bdf84ed6\bin\node.exe",
    "node"
)

$nodeExe = $null
foreach ($candidate in $nodeCandidates) {
    try {
        $resolved = Get-Command $candidate -ErrorAction Stop
        $nodeExe = $resolved.Source
        break
    } catch {
        if (Test-Path -LiteralPath $candidate) {
            $nodeExe = $candidate
            break
        }
    }
}

if (-not $nodeExe) {
    throw "Node.js was not found. Use Codex bundled Node or install Node.js >= 22."
}

$repoRoot = "C:\Users\24796\.codex\plugins\cache\MageByte-Zero\spec-superflow"
$cli = Join-Path $repoRoot "scripts\spec-superflow.mjs"

if (-not (Test-Path -LiteralPath $cli)) {
    throw "spec-superflow CLI was not found at $cli. Reinstall plugin spec-superflow@spec-superflow."
}

& $nodeExe $cli @Args
