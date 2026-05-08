Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Use dry-run after the node is already configured and talosctl can authenticate.
Push-Location (Join-Path $PSScriptRoot "..")
try {
    talosctl apply-config `
        --nodes 192.168.1.178 `
        --file .\generated\controlplane.yaml `
        --dry-run
}
finally {
    Pop-Location
}
