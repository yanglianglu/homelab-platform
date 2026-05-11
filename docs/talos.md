# Talos

Talos turns the Harvester VMs into Kubernetes nodes. The source files for the `homelab-talos` cluster live under `talos/clusters/homelab`.

## Current Cluster

| Item | Value |
| --- | --- |
| Cluster name | `homelab-talos` |
| Control-plane endpoint | `https://192.168.1.181:6443` |
| Node | `cp-01` |
| Node IP | `192.168.1.181` |
| Talos version | `v1.13.0` |
| Install disk | `/dev/vda` |
| Pod CIDR | `10.42.0.0/16` |
| Service CIDR | `10.43.0.0/16` |
| Bootstrap status | Completed |
| Health status | Completed successfully |

## Milestone

The fresh control-plane node, `cp-01`, is bootstrapped and healthy. Talos API checks, service/address/route inspection, Kubernetes bootstrap, kubeconfig generation, and core pod checks have completed.

The old `talos-cp-01` VM at `192.168.1.178` is retained temporarily and should be retired only after the new `cp-01` workflow has been reviewed.

## Secret Handling

Generated files such as `controlplane.yaml`, `worker.yaml`, `talosconfig`, `secrets.yaml`, and kubeconfig can contain sensitive material. Keep them local unless they are encrypted with a tool such as SOPS and age.

## Recovery

Talos VM recovery should prefer rebuildable infrastructure over destructive restore testing. `cp-01` is now the active rebuilt control-plane VM.

See:

- `docs/runbooks/recover-cluster.md`
- `docs/runbooks/talos-vm-recovery-strategy.md`
- `docs/runbooks/create-talos-vm.md`

## Local Access

Guest Kubernetes access uses the context name `homelab-talos` in `~/.kube/config`.

Talos access uses `~/.talos/config`, with default endpoint and node set to `192.168.1.181`.

See `docs/runbooks/kube-context-switching.md`.
