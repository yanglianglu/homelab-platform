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

The data platform now uses a CSI-first storage model. Harvester CSI should
create guest Kubernetes PVCs backed by Harvester StorageClasses. `data-01`
remains the scheduling anchor for ClickHouse and graph workloads, not the owner
of manually mounted data disks.

| Storage | Guest class | Host class | Purpose |
| --- | --- | --- | --- |
| OS disk | N/A | `slow` | Rebuildable Talos OS disk |
| Retained data | `harvester` by default; `harvester-slow-retain` when retention is required | `slow` | ClickHouse retained data |
| Disposable data | `harvester-slow-delete` | `slow` | test PVCs and disposable app state |
| Hot/temp | `harvester-abundance-nvme-delete` | `the-abundance-nvme` | ClickHouse temp, merges, and hot working set |
| Replicated infrastructure | `harvester-fast-ha-retain` | `fast-ha` | Approval-gated only |

The standalone Linux data VM is the rejected alternative. The chosen model is
Kubernetes-native, with strict node placement and CSI-managed PVC lifecycle.

Current VM disk allocation:

| Guest disk | Harvester PVC | Purpose |
| --- | --- | --- |
| `/dev/vda` | `data-01-os-disk` | Talos OS |

Legacy PVCs retained outside the running VM:

| Harvester PVC | Size | State | Purpose |
| --- | ---: | --- | --- |
| `data-01-retained-data` | 10 TiB | Detached | Rollback only |
| `data-01-hot-temp` | 1 TiB | Detached | Rollback only |

Do not create Talos UserVolumeConfig or static local PVs unless Harvester CSI is
rejected after proof and the local-PV fallback is explicitly approved.

The CSI proof now passes on `data-01` after the repo-local
`harvester-csi-mountpoint` Talos extension was rolled to every Talos node. The
drill validated provisioning, write/read, pod restart persistence, 1 Gi -> 2 Gi
expansion, CSI node pod restart, `data-01` reboot recovery, detach, guest
PVC/PV cleanup, and Harvester backend volume cleanup.

The legacy PVCs were detached from `data-01` and retained as rollback. Delete
them only in a separate explicit cleanup gate.

See `harvester-csi-client-cluster-plan.md` for CSI gates.

## Growth Rules

- Add CPU when ClickHouse query profiles show CPU pressure.
- Add memory when queries spill, cache pressure is high, or graph working set requires it.
- Add NVMe when merges, temp files, or graph random IO become the bottleneck.
- Add HDD capacity when ClickHouse reaches 70-75% disk usage.
- Define the graph engine and working set before allocating multi-terabyte graph storage.
