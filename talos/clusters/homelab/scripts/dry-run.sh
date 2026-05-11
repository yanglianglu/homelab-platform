#!/usr/bin/env bash
set -euo pipefail

# Use dry-run after the node is already configured and talosctl can authenticate.
cd "$(dirname "$0")/.."

talosctl apply-config \
  --nodes "${1:-192.168.1.181}" \
  --file generated/controlplane.yaml \
  --dry-run
