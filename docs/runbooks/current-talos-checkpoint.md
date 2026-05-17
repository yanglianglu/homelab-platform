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

Last checked: 2026-05-17 America/Chicago.

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
data-01 VM Running/Ready on the-abundance, OS disk only
```

Storage compatibility:

```text
Harvester CSI installed in kube-system and managed by Argo CD
CSI controller 3/3 available
CSI node DaemonSet 6/6 available
harvester-csi-mountpoint extension active on all Talos nodes
CSI proof on data-01 passed provisioning, resize, reboot, detach, and cleanup
legacy data-01 PVCs detached from VM and retained as rollback
```

Harvester observability:

```text
rancher-monitoring addon enabled in cattle-monitoring-system
AddonDeploySuccessful
Prometheus, Grafana, and Alertmanager proxy health checks passed
external alert notifications not configured
```

Workload placement:

```text
apps/whoami runs on worker-01
data-01 is tainted data-platform=true:NoSchedule
data-01 only runs required system DaemonSets
External Secrets steady-state values select homelab.local/node-class=general
External Secrets pods run on worker-01 and worker-02 after Argo refresh
Argo CD core workloads select homelab.local/node-class=general
Argo CD core pods run on worker-01 and worker-02
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

Do not create data-platform local PVs. The storage direction is Harvester CSI
first. `data-01` now sees only `/dev/vda`; the legacy 10 TiB retained-data PVC
and 1 TiB hot-temp PVC are detached from the VM and retained only as rollback.

Next platform gates:

1. Add guest Kubernetes observability for CSI, Argo CD, node, namespace, and
   data-platform workload health.
2. Run a ClickHouse-specific PVC pilot before large ingestion.
3. Decide whether to delete the detached legacy `data-01` PVCs.
4. Run a controlled Harvester host-maintenance CSI drill only as a separate
   approved operation.
