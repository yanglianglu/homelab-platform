#!/usr/bin/env bash
set -euo pipefail

node="${1:-192.168.1.181}"

cd "$(dirname "$0")/.."

config="generated/controlplane.yaml"

if [[ ! -f "$config" ]]; then
  echo "Missing ${config}. Run scripts/render.sh first." >&2
  exit 1
fi

echo "About to apply Talos control-plane config to ${node}"
echo "If the VM is still in maintenance mode before static IP is active, pass its discovered DHCP or IPv6 address as the first argument."
echo "WARNING: --insecure is only for initial maintenance-mode apply."
read -r -p "Type APPLY to continue: " confirm

if [[ "$confirm" != "APPLY" ]]; then
  echo "Aborted."
  exit 1
fi

talosctl apply-config --insecure \
  --nodes "$node" \
  --file "$config"
