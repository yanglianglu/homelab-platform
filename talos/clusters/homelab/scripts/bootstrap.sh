#!/usr/bin/env bash
set -euo pipefail

node="${1:-192.168.1.181}"

cd "$(dirname "$0")/.."

echo "WARNING: talosctl bootstrap should only be run once for the first control-plane node."
read -r -p "Type BOOTSTRAP to continue: " confirm

if [[ "$confirm" != "BOOTSTRAP" ]]; then
  echo "Aborted."
  exit 1
fi

talosctl bootstrap --nodes "$node"
talosctl kubeconfig .
