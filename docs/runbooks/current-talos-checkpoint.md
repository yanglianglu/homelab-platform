# Runbook: Current Talos Checkpoint

This checkpoint documents the current Talos state during the Gate 1-8 VM growth
execution.

## Cluster State

| Item | Value |
| --- | --- |
| Cluster name | `homelab-talos` |
| Control-plane node | `cp-01` |
| Control-plane IP | `192.168.1.181` |
| Current Kubernetes API endpoint | `https://192.168.1.181:6443` |
| Planned Kubernetes API VIP | `https://192.168.1.184:6443` |
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
cp-01   Ready   control-plane   192.168.1.181   Talos v1.13.0   Kubernetes v1.36.0
```

Harvester VM state at this checkpoint:

```text
cp-01 VM Running/Ready on the-abundance
cp-02 VM created on the-elation but stopped before Talos config
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

- `cp-01` is `Ready`.
- Node IP is `192.168.1.181`.
- `cp-01` is pinned back to `the-abundance`.
- `cp-02` exists in Harvester but is not a Kubernetes node yet.
- `cp-03`, `worker-01`, `worker-02`, and `data-01` are planned but not yet created as live VMs at this checkpoint.
- Core pods are running:
  - `coredns`
  - `kube-apiserver`
  - `kube-controller-manager`
  - `kube-scheduler`
  - `kube-flannel`
  - `kube-proxy`

## Stop Condition

Gate 3 stopped at `cp-02` because the VM booted from the Talos ISO without an IPv4
address in VMI status and was not reachable at `192.168.1.182:50000`. The next
gate must decide how Talos maintenance networking will be provided for new VMs:
DHCP reservation, manual console config, or another bootstrap method.
