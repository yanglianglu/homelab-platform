# Talos

Talos turns the Harvester VMs into Kubernetes nodes. The source files for the `homelab-talos` cluster live under `talos/clusters/homelab`.

## Current Cluster

| Item | Value |
| --- | --- |
| Cluster name | `homelab-talos` |
| Control-plane endpoint | `https://192.168.1.184:6443` |
| Control-plane nodes | `cp-01`, `cp-02`, `cp-03` |
| Worker nodes | `worker-01`, `worker-02`, `data-01` |
| Talos version | `v1.13.0` |
| Install disk | `/dev/vda` |
| Pod CIDR | `10.42.0.0/16` |
| Service CIDR | `10.43.0.0/16` |
| Bootstrap status | Completed |
| Health status | Completed successfully |
| CSI host extension | `harvester-csi-mountpoint` is the required universal node contract |

## Milestone

The cluster now has three Talos control-plane VMs, two general workers, and one
tainted data worker. Kubernetes API access uses the LAN-only kube-vip endpoint
`192.168.1.184`; individual node IPs remain break-glass access points.

The repo-local `harvester-csi-mountpoint` extension lets Harvester CSI complete
`NodeUnstageVolume` cleanup on Talos. It is now treated as a universal Talos
node contract, not a `data-01` special case.

The old `talos-cp-01` VM at `192.168.1.178` has been retired and its Harvester desired-state file has been removed from Git.

## Secret Handling

Generated files such as `controlplane.yaml`, `worker.yaml`, `talosconfig`, `secrets.yaml`, and kubeconfig can contain sensitive material. Keep them local unless they are encrypted with a tool such as SOPS and age.

## Recovery

Talos VM recovery should prefer rebuildable infrastructure over destructive restore testing. `cp-01` is now the active rebuilt control-plane VM.

See:

- `docs/runbooks/recover-cluster.md`
- `docs/runbooks/talos-vm-recovery-strategy.md`
- `docs/runbooks/create-talos-vm.md`
- `docs/runbooks/talos-harvester-csi-mountpoint-fix.md`

## Local Access

Guest Kubernetes access uses the context name `homelab-talos` in `~/.kube/config`.
The normal server endpoint should be `https://192.168.1.184:6443`.

Talos access uses `~/.talos/config`; keep individual node IPs available for
break-glass operations.

See `docs/runbooks/kube-context-switching.md`.
