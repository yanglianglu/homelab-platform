# Runbook: Apply Talos Config

Use the repo scripts under `talos/clusters/homelab/scripts/` for current Talos
rendering and validation. Do not hand-edit generated machine configs.

## Current Cluster

| Item | Value |
| --- | --- |
| Cluster | `homelab-talos` |
| API endpoint | `https://192.168.1.184:6443` |
| Control plane | `cp-01`, `cp-02`, `cp-03` |
| Workers | `worker-01`, `worker-02`, `data-01` |

## Safe Local Flow

```bash
cd /Users/yanglianglu/Documents/GitHub/homelab-platform/talos/clusters/homelab

scripts/render.sh
scripts/validate.sh
scripts/dry-run.sh
```

Apply config only in an approved live-operation gate:

```bash
talosctl apply-config --nodes <node-ip> --file generated/<node>.yaml
```

## Rules

- `talosctl bootstrap` is historical; do not run it again for this cluster.
- Do not regenerate configs with new PKI unless intentionally rebuilding the
  cluster.
- Do not commit plaintext generated secrets, `talosconfig`,
  `controlplane.yaml`, `worker.yaml`, `secrets.yaml`, or kubeconfig.
- Review generated files without printing secrets. Prefer targeted checks for
  hostname, IP address, SANs, labels, and taints.
- Use `scripts/render-node-config.rb` for per-node configs so hostname,
  static IP, nameservers, labels, and taints do not leak across nodes.
- Worker node labels and taints may need cluster-admin enforcement after join.
  In particular, apply `data-01` labels and `data-platform=true:NoSchedule`
  from a cluster-admin context if they drift.
