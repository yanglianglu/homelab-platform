# Storage

Storage design notes for Harvester volumes and Kubernetes storage classes.

## Current Baseline

- Talos OS disk: `100 Gi`
- Talos install disk inside the VM: `/dev/vda`
- Default persistent Harvester storage class: `slow`
- `slow` is HDD-backed and selected by `diskSelector: hdd,seagate`.
- The HDD Longhorn disks on `the-abundance` must keep both `hdd` and `seagate` disk tags for `slow` and the current Talos ISO image StorageClass to provision successfully.
- Shared fast PVCs should use `nvme` only after that class is intentionally created.
- Node-specific NVMe storage classes exist for temporary, cache, scratch, or explicitly pinned performance-sensitive workloads.
- `fast-ha` is approval-gated and must not be used without explicit owner approval.
- Guest Kubernetes workload PVCs should use Harvester CSI. The guest
  `harvester` StorageClass remains the default workload class and maps to host
  `slow`.
- The Talos `harvester-csi-mountpoint` extension is a universal node contract:
  every Talos node now carries it before broad CSI-backed scheduling.

## Storage Class Policy

| StorageClass | Role | Notes |
| --- | --- | --- |
| `slow` | Main persistent default | Production-ready Exos HDD-backed storage for durable baseline storage and most application PVCs |
| `nvme` | Shared fast PVCs | Create and use for general fast storage that does not need HA replication |
| `the-abundance-nvme` | Node-specific NVMe | Use only for temporary/cache/performance workloads pinned to `the-abundance` |
| `the-elation-nvme` | Node-specific NVMe | Use only for temporary/cache/performance workloads pinned to `the-elation` |
| `the-enigmata-nvme` | Node-specific NVMe | Use only for temporary/cache/performance workloads pinned to `the-enigmata` |
| `fast` | Legacy/experimental | Do not use for new workloads unless redefined later |
| `fast-ha` | Replicated NVMe | Approval-gated for important infrastructure only |

See `harvester/storageclasses/storage-policy.md` for the Harvester-side storage policy.

## Guest Cluster CSI Policy

`homelab-talos` uses the default guest StorageClass `harvester` for normal
workload PVCs. The Harvester CSI chart maps this default guest class to host
StorageClass `slow`.

Explicit guest StorageClasses are retained for exceptions:

| Guest StorageClass | Host StorageClass | Reclaim | Use |
| --- | --- | --- | --- |
| `harvester` | `slow` | `Delete` | default workload PVCs |
| `harvester-slow-retain` | `slow` | `Retain` | retained database/data PVCs |
| `harvester-slow-delete` | `slow` | `Delete` | explicit disposable/test PVCs |
| `harvester-abundance-nvme-delete` | `the-abundance-nvme` | `Delete` | data-platform temp/cache/hot data |
| `harvester-fast-ha-retain` | `fast-ha` | `Retain` | approval-gated infrastructure only |

CSI does not change the durability model of `slow`: it remains single-replica
HDD-backed Longhorn storage. CSI is used for Kubernetes-native PVC lifecycle,
hot-plug automation, and operator compatibility.

The Harvester CSI proof passes on `data-01` after the
`harvester-csi-mountpoint` Talos extension rollout. The proof validated
provisioning, attach, mount, write, restart persistence, PVC expansion, CSI node
pod restart, `data-01` reboot recovery, scale-to-zero detach,
`NodeUnstageVolume`, guest PV deletion, Harvester backend PVC deletion, and
final `VolumeAttachment` cleanup. The reboot left an old failed proof pod object
that required manual deletion; storage detach was clean.

CSI is the preferred general workload storage path. Harvester-level monitoring
is enabled for host, VM, and Longhorn visibility. The legacy `data-01` rollback
PVCs have been deleted. Large ClickHouse data still requires a
ClickHouse-specific PVC pilot, performance checks, and reviewed alerts.

## Boundaries

- Harvester storage definitions belong under `harvester/storageclasses/`.
- Kubernetes storage classes, CSI settings, and persistent volume policies belong under `kubernetes/clusters/homelab/platform/storage/`.
- Do not store live runtime exports with `status`, `uid`, `resourceVersion`, or `managedFields` as source of truth.
