$ErrorActionPreference = "Stop"

$Node = "192.168.1.178"

Write-Host "WARNING: talosctl bootstrap should only be run once for the first control-plane node."
$Confirm = Read-Host "Type BOOTSTRAP to continue"

if ($Confirm -ne "BOOTSTRAP") {
  Write-Host "Aborted."
  exit 1
}

talosctl bootstrap --nodes $Node
talosctl kubeconfig .
