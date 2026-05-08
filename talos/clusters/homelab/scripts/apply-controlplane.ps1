$ErrorActionPreference = "Stop"

$Node = "192.168.1.178"
$Config = ".\generated\controlplane.yaml"

if (!(Test-Path $Config)) {
  throw "Missing $Config. Run render.ps1 first."
}

Write-Host "About to apply Talos control-plane config to $Node"
Write-Host "WARNING: --insecure is only for initial maintenance-mode apply."
$Confirm = Read-Host "Type APPLY to continue"

if ($Confirm -ne "APPLY") {
  Write-Host "Aborted."
  exit 1
}

talosctl apply-config --insecure `
  --nodes $Node `
  --file $Config
