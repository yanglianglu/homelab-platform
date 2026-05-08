$ErrorActionPreference = "Stop"

$ClusterName = "homelab-talos"
$Endpoint = "https://192.168.1.178:6443"
$InstallDisk = "/dev/vda"
$PatchFile = ".\patches\cluster-network.yaml"
$OutputDir = ".\generated"

Write-Host "Rendering Talos config for $ClusterName..."
Write-Host "WARNING: Generated files contain secrets. Do not commit them in plaintext."

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

talosctl gen config $ClusterName $Endpoint `
  --install-disk $InstallDisk `
  --config-patch "@$PatchFile" `
  --output-dir $OutputDir `
  --force

Write-Host "Generated files in $OutputDir"
Write-Host "Do not commit generated YAML/talosconfig/kubeconfig in plaintext."
