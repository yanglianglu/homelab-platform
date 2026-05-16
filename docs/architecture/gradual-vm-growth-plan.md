# Gradual VM Growth Plan

Build the homelab in controlled stages instead of creating all maximum-size VMs at once.

## Target Shape

```text
3 Talos control-plane VMs
2 initial Talos worker VMs
1 dedicated Talos data worker for ClickHouse / graph workloads
optional 3rd worker later, only if metrics justify it
```

## Stage 1: Stabilize Current Control Plane

- Diagnose why `cp-01` / `192.168.1.181:6443` is unreachable before adding nodes.
- Confirm Harvester nodes, Longhorn, VM state, and Talos API path.
- Do not add new nodes until the existing control plane is understood.

## Stage 2: Add HA Control Plane

| Host | VM | Initial size | Purpose |
| --- | --- | ---: | --- |
| `the-abundance` | `cp-01` | 4 CPU / 8 Gi | Existing control-plane |
| `the-elation` | `cp-02` | 4 CPU / 8 Gi | New control-plane |
| `the-enigmata` | `cp-03` | 4 CPU / 8 Gi | New control-plane |

- Add a stable API VIP or load-balanced endpoint.
- Keep individual node IPs for Talos and break-glass access.
- Keep Talos OS disks on `slow` as rebuildable disks.

## Stage 3: Add Worker Capacity

| Host | VM | Initial size | Purpose |
| --- | --- | ---: | --- |
| `the-elation` | `worker-01` | 4 CPU / 12 Gi | General platform/app worker |
| `the-enigmata` | `worker-02` | 2 CPU / 8 Gi | Small worker on smaller host |

Defer `worker-03` until scheduling pressure or workload metrics prove the need.

## Stage 4: Add Dedicated Data Worker

| Host | VM | Initial size | Purpose |
| --- | --- | ---: | --- |
| `the-abundance` | `data-01` | 8 CPU / 32 Gi | Tainted Kubernetes data worker |

Initial storage:

| Disk | StorageClass | Size | Purpose |
| --- | --- | ---: | --- |
| OS disk | `slow` | 100 Gi | Talos operating system |
| ClickHouse retained data | `slow` | 10 TiB | Main OLAP storage on production-ready Exos HDD |
| Hot/temp NVMe | `the-abundance-nvme` | 1 TiB | ClickHouse temp, merges, hot working set |
| Graph storage | deferred | TBD | Only after graph workload shape is known |

`data-01` joins `homelab-talos` as a worker with `data-platform=true:NoSchedule`.

## Stage 5: Platform Services

- Enable Harvester monitoring after core VMs are stable.
- Add guest-cluster observability: VictoriaMetrics, Grafana, exporters, alerting.
- Add ingress, cert-manager, and Cloudflare Tunnel only after control-plane HA and workers exist.

## Acceptance Criteria

- Harvester still has practical headroom after each VM wave.
- `kubectl get nodes` shows all Talos nodes Ready after each addition.
- Talos health passes across all control-plane nodes.
- Kubernetes API access uses the stable endpoint, not only `cp-01`.
- Workloads schedule on workers, not control-plane nodes, except temporary bootstrap exceptions.
- `data-01` is monitored before large ingestion begins.
