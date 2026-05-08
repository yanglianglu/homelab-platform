# Runbook: Current Talos Checkpoint

This checkpoint documents the first successful Talos control-plane bootstrap.

## Cluster State

| Item | Value |
| --- | --- |
| Cluster name | `homelab-talos` |
| Control-plane node | `talos-cp-01` |
| Control-plane IP | `192.168.1.178` |
| Kubernetes API endpoint | `https://192.168.1.178:6443` |
| Talos version | `v1.13.0` |
| Kubernetes version | `v1.36.0` |
| Install disk | `/dev/vda` |
| Pod CIDR | `10.42.0.0/16` |
| Service CIDR | `10.43.0.0/16` |

## Verification Commands

```powershell
kubectl get nodes -o wide
kubectl get pods -A -o wide
talosctl health
```

## Expected State

- `talos-cp-01` is `Ready`.
- Node IP is `192.168.1.178`.
- Core pods are running:
  - `coredns`
  - `kube-apiserver`
  - `kube-controller-manager`
  - `kube-scheduler`
  - `kube-flannel`
  - `kube-proxy`
