Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location (Split-Path -Parent $PSScriptRoot)
try {
    python -m agentproof.cli --brief examples/application_brief.md --out outputs/demo-run
}
finally {
    Pop-Location
}

