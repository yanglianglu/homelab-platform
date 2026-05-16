# Runbook: Apply Talos Config

Use this after the `cp-01` VM exists and is booted from the Talos ISO.

## Local Steps

This is the macOS shell sequence for the first control-plane node:

```bash
cd /Users/yanglianglu/Documents/GitHub/homelab-platform/talos/clusters/homelab

talosctl get disks --insecure --nodes 192.168.1.181

talosctl gen config homelab-talos https://192.168.1.181:6443 \
  --install-disk /dev/vda \
  --config-patch "@patches/cluster-network.yaml" \
  --config-patch-control-plane "@patches/controlplane-cp-01.yaml" \
  --output-dir generated \
  --force

rg "10.42.0.0|10.43.0.0" generated/controlplane.yaml

talosctl validate --config generated/controlplane.yaml --mode metal --strict

talosctl apply-config --insecure \
  --nodes 192.168.1.181 \
  --file generated/controlplane.yaml

export TALOSCONFIG="$PWD/generated/talosconfig"
talosctl config endpoint 192.168.1.181
talosctl config node 192.168.1.181

talosctl version
talosctl get services
talosctl get addresses
talosctl get routes

talosctl bootstrap
talosctl kubeconfig generated

kubectl --kubeconfig generated/kubeconfig get pods -A -o wide
talosctl health
```

## Notes

- `talosctl bootstrap` should only be run once for the first control-plane node.
- Do not regenerate configs with new PKI after the cluster is active unless intentionally rebuilding the cluster.
- Do not commit plaintext generated secrets, `talosconfig`, `controlplane.yaml`, `worker.yaml`, `secrets.yaml`, or kubeconfig.
- Do not render additional nodes by directly list-merging per-node patches into a generated config that already contains another node's static IP. Use `scripts/render-node-config.rb` so `machine.network.interfaces` and nameservers are replaced for each node.
- Review generated files without printing secrets. Prefer targeted checks for hostname, IP address, SANs, labels, and taints.
- Worker node labels and taints may need cluster-admin enforcement after join. In particular, apply `data-01` labels and `data-platform=true:NoSchedule` with `kubectl label node` and `kubectl taint node` rather than relying only on kubelet-owned metadata.
- The repository scripts under `talos/clusters/homelab/scripts/` keep the same macOS shell workflow in a safer repeatable location.
