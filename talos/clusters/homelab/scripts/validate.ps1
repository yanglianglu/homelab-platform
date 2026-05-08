$ErrorActionPreference = "Stop"

$ControlPlaneConfig = ".\generated\controlplane.yaml"
$WorkerConfig = ".\generated\worker.yaml"

if (!(Test-Path $ControlPlaneConfig)) {
  throw "Missing $ControlPlaneConfig. Run render.ps1 first."
}

if (!(Test-Path $WorkerConfig)) {
  throw "Missing $WorkerConfig. Run render.ps1 first."
}

talosctl validate --config $ControlPlaneConfig --mode metal --strict
talosctl validate --config $WorkerConfig --mode metal --strict
