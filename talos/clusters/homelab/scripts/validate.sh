#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

controlplane_config="generated/controlplane.yaml"
worker_config="generated/worker.yaml"

if [[ ! -f "$controlplane_config" ]]; then
  echo "Missing ${controlplane_config}. Run scripts/render.sh first." >&2
  exit 1
fi

if [[ ! -f "$worker_config" ]]; then
  echo "Missing ${worker_config}. Run scripts/render.sh first." >&2
  exit 1
fi

talosctl validate --config "$controlplane_config" --mode metal --strict
talosctl validate --config "$worker_config" --mode metal --strict
