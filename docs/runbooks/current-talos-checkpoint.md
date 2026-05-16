# Runbook: Current Talos Checkpoint

This checkpoint documents the current Talos state during the Gate 1-8 VM growth
execution.

## Cluster State

| Item | Value |
| --- | --- |
| Cluster name | `homelab-talos` |
| Control-plane nodes | `cp-01`, `cp-02`, `cp-03` |
| General workers | `worker-01`, `worker-02` |
| Data worker | `data-01` |
| Current Kubernetes API endpoint | `https://192.168.1.184:6443` |
| Talos version | `v1.13.0` |
| Kubernetes version | `v1.36.0` |
| Install disk | `/dev/vda` |
| Pod CIDR | `10.42.0.0/16` |
| Service CIDR | `10.43.0.0/16` |

## Verification Commands

```bash
kubectl --context homelab-talos get nodes -o wide
kubectl --context homelab-talos get pods -A -o wide
talosctl health
```

## Latest Verification

Last checked: 2026-05-16 America/Chicago.

Node readiness:

```text
cp-01       Ready   control-plane   192.168.1.181   Talos v1.13.0   Kubernetes v1.36.0
cp-02       Ready   control-plane   192.168.1.182   Talos v1.13.0   Kubernetes v1.36.0
cp-03       Ready   control-plane   192.168.1.183   Talos v1.13.0   Kubernetes v1.36.0
worker-01   Ready   worker          192.168.1.179   Talos v1.13.0   Kubernetes v1.36.0
worker-02   Ready   worker          192.168.1.180   Talos v1.13.0   Kubernetes v1.36.0
data-01     Ready   data worker     192.168.1.185   Talos v1.13.0   Kubernetes v1.36.0
```

Harvester VM state at this checkpoint:

```text
cp-01 VM Running/Ready on the-abundance, OS disk first
cp-02 VM Running/Ready on the-elation, OS disk first
cp-03 VM Running/Ready on the-enigmata, OS disk first
worker-01 VM Running/Ready on the-elation, OS disk first
worker-02 VM Running/Ready on the-enigmata, OS disk first
data-01 VM Running/Ready on the-abundance, OS disk first, retained/hot disks attached
```

Core pod summary:

```text
coredns                         2/2 pods Running
kube-apiserver-cp-01            Running
kube-controller-manager-cp-01   Running
kube-scheduler-cp-01            Running
kube-flannel                    Running
kube-proxy                      Running
```

## Expected State

- `cp-01`, `cp-02`, and `cp-03` are `Ready` control-plane nodes.
- `worker-01` and `worker-02` are `Ready` general workers.
- `data-01` is a `Ready` tainted data worker.
- `homelab-talos` kubeconfig uses the kube-vip endpoint `192.168.1.184`.
- All created Talos VMs are pinned to their intended Harvester hosts.
- Core pods are running:
  - `coredns`
  - `kube-apiserver`
  - `kube-controller-manager`
  - `kube-scheduler`
  - `kube-flannel`
  - `kube-proxy`

## Current Stop Condition

Do not create data-platform local PVs yet. `data-01` sees the attached disks as
`vdb` (10 TiB retained data) and `vdc` (1 TiB hot/temp), but the Talos mount
configuration for `/var/mnt/clickhouse-data` and `/var/mnt/clickhouse-hot` is not
defined yet.
