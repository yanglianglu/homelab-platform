#!/usr/bin/env bash
set -euo pipefail

cluster_name="homelab-talos"
endpoint="https://192.168.1.181:6443"
install_disk="/dev/vda"
cluster_patch_file="patches/cluster-network.yaml"
controlplane_patch_file="patches/controlplane-cp-01.yaml"
output_dir="generated"

cd "$(dirname "$0")/.."

echo "Rendering Talos config for ${cluster_name}..."
echo "WARNING: generated files contain secrets. Do not commit them in plaintext."

mkdir -p "$output_dir"

talosctl gen config "$cluster_name" "$endpoint" \
  --install-disk "$install_disk" \
  --config-patch "@${cluster_patch_file}" \
  --config-patch-control-plane "@${controlplane_patch_file}" \
  --output-dir "$output_dir" \
  --force

echo "Generated files in ${output_dir}"
echo "Do not commit generated YAML, talosconfig, kubeconfig, or secrets in plaintext."
