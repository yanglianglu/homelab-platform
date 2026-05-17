# Runbook: Current Talos Checkpoint

This checkpoint documents the current Talos state after the VM growth and
Harvester CSI proof gates.

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

Storage compatibility:

```text
Harvester CSI installed in kube-system and promoted into Argo CD desired state
CSI controller 3/3 available
CSI node DaemonSet 6/6 available
data-01 Talos extension harvester-csi-mountpoint active; universal rollout pending
1 Gi CSI proof on data-01 passed cleanup without manual VolumeAttachment deletion
```

Core pod summary, abbreviated:

```text
coredns                         2/2 pods Running
kube-apiserver                  Running on control-plane nodes
kube-controller-manager         Running on control-plane nodes
kube-scheduler                  Running on control-plane nodes
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

Do not create data-platform local PVs. The storage direction changed to
Harvester CSI first. `data-01` still has legacy attached disks visible as `vdb`
(10 TiB retained data) and `vdc` (1 TiB hot/temp), but they should remain unused
until the CSI path passes larger drills or the local-PV fallback is explicitly
approved.

Next storage gate:

1. Roll the `harvester-csi-mountpoint` extension to all Talos nodes before
   broad CSI-backed workload scheduling.
2. Keep the chart-created default `harvester` StorageClass as the normal
   workload class mapped to host `slow`.
3. Run larger CSI drills: PVC expansion, CSI pod restart, `data-01` VM reboot,
   and a controlled host-maintenance scenario.
4. Detach the legacy attached disks only after larger drills pass and the
   detach plan is explicitly approved.
