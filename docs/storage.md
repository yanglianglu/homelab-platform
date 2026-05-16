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

## Boundaries

- Harvester storage definitions belong under `harvester/storageclasses/`.
- Kubernetes storage classes, CSI settings, and persistent volume policies belong under `kubernetes/clusters/homelab/platform/storage/`.
- Do not store live runtime exports with `status`, `uid`, `resourceVersion`, or `managedFields` as source of truth.
