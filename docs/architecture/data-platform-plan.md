# Data Platform Plan

Large analytical and graph workloads use a dedicated Talos worker in the Kubernetes cluster. `data-01` is part of `homelab-talos`, but it is tainted and pinned so it does not behave like a general worker.

## Initial Data Node

| Node | Host | Initial size | Role |
| --- | --- | ---: | --- |
| `data-01` | `the-abundance` | 8 CPU / 32 Gi | Tainted Kubernetes data worker |

`the-abundance` is the primary data host because it has the large HDD/NVMe capacity.

## Scheduling Model

- Talos role: worker.
- Kubernetes label: `homelab.local/node-class=data`.
- Kubernetes label: `homelab.local/storage-locality=the-abundance`.
- Kubernetes taint: `data-platform=true:NoSchedule`.
- Only `data-platform` workloads should tolerate this taint.
- Apply the data label and taint from a cluster-admin context after join. Talos
  can carry the desired intent, but Kubernetes NodeRestriction can prevent a
  worker kubelet from setting some scheduling metadata on itself.

## Workload Boundaries

| Workload | Initial placement | Notes |
| --- | --- | --- |
| ClickHouse | `data-01` | Main OLAP engine for 10-30 TiB analysis; production ingestion waits for monitoring and storage validation |
| Graph database | Deferred on `data-01` | Select engine and working set before allocating 1-10 TiB |
| Dashboards | Kubernetes observability domain | Grafana belongs in the guest cluster |
| Metrics | Kubernetes observability domain | VictoriaMetrics starts in the guest cluster |
| Large raw/archive data | `data-01` or external storage | Do not assume node-local storage is a backup |

## Storage Policy

| Storage | Class | Initial size | Purpose |
| --- | --- | ---: | --- |
| OS disk | `slow` | 100 Gi | Rebuildable Talos OS disk |
| Retained data | `slow` | 10 TiB | Production-ready Exos HDD-backed data volume |
| Hot/temp | `the-abundance-nvme` | 1 TiB | ClickHouse temp, merges, and hot working set |
| Replicated infrastructure | `fast-ha` | TBD | Approval-gated only |

The standalone Linux data VM remains the rejected alternative for now. The chosen model is Kubernetes-native, but with strict node placement and local storage assumptions.

Current disk map:

| Guest disk | Harvester PVC | Purpose |
| --- | --- | --- |
| `/dev/vda` | `data-01-os-disk` | Talos OS |
| `/dev/vdb` | `data-01-retained-data` | Retained ClickHouse/data storage |
| `/dev/vdc` | `data-01-hot-temp` | Hot/temp NVMe-backed storage |

Local PVs remain deferred until Talos mounts those disks at stable paths.

## Growth Rules

- Add CPU when ClickHouse query profiles show CPU pressure.
- Add memory when queries spill, cache pressure is high, or graph working set requires it.
- Add NVMe when merges, temp files, or graph random IO become the bottleneck.
- Add HDD capacity when ClickHouse reaches 70-75% disk usage.
- Define the graph engine and working set before allocating multi-terabyte graph storage.
