# Harvester Storage Policy

This file records the intended Harvester storage class usage for the homelab. It is an operator policy, not a live Kubernetes export.

Do not paste live StorageClass objects with `uid`, `resourceVersion`, `creationTimestamp`, `managedFields`, or `status` into this repository.

## Current Policy

| StorageClass | Backing intent | Default? | Use for | Avoid for |
| --- | --- | --- | --- | --- |
| `slow` | Production-ready Exos HDD-backed Longhorn storage selected by `diskSelector: hdd,seagate` | Yes | Main persistent workloads, general app PVCs, durable baseline storage, retained data | High-write scratch workloads that do not need HDD durability |
| `nvme` | Shared NVMe-backed Longhorn storage selected by `diskSelector: nvme` | No | Shared fast PVCs that do not need HA replication | Critical state that requires HA replicas |
| `the-abundance-nvme` | Node-specific NVMe on `the-abundance` | No | Temporary/cache/performance-sensitive workloads pinned to `the-abundance` | Data that must survive node loss or move freely |
| `the-elation-nvme` | Node-specific NVMe on `the-elation` | No | Temporary/cache/performance-sensitive workloads pinned to `the-elation` | Data that must survive node loss or move freely |
| `the-enigmata-nvme` | Node-specific NVMe on `the-enigmata` | No | Temporary/cache/performance-sensitive workloads pinned to `the-enigmata` | Data that must survive node loss or move freely |
| `fast` | Older NVMe/SSD class | No | Do not use for new workloads unless redefined later | New platform or application workloads |
| `fast-ha` | Replicated NVMe class | No | Approval-gated important infrastructure only | Any workload without explicit owner approval |

## Desired Usage

- Use `slow` as the default persistent storage class. Despite the name, it is the production-ready Exos HDD-backed baseline.
- `slow` is intentionally single-replica in the current homelab model; node or
  disk downtime is acceptable for this class.
- Use `nvme` as the standard shared fast PVC class once created.
- Use node-specific NVMe classes only when the workload is intentionally tied to a node or the data is temporary, cached, or rebuildable.
- Do not use `fast-ha` without explicit owner approval.
- Treat `fast` as legacy/experimental until it is removed or redefined.
- Any important data on NVMe-backed classes needs an explicit backup and recovery story before it is considered durable.

## Guest Cluster Use Through Harvester CSI

Guest Kubernetes clusters should not reference host StorageClasses directly in
application manifests. The default guest StorageClass is `harvester`, and the
Harvester CSI chart maps it to host StorageClass `slow`.

Explicit guest classes exist for non-default reclaim behavior or host-specific
tiers:

| Guest StorageClass | Host StorageClass | Intended reclaim |
| --- | --- | --- |
| `harvester` | `slow` | `Delete` |
| `harvester-slow-retain` | `slow` | `Retain` |
| `harvester-slow-delete` | `slow` | `Delete` |
| `harvester-abundance-nvme-delete` | `the-abundance-nvme` | `Delete` |
| `harvester-fast-ha-retain` | `fast-ha` | `Retain` |

CSI is a lifecycle interface for the guest cluster. It does not add replicas or
snapshot requirements to `slow`.

Normal workload PVCs should use `harvester` or omit `storageClassName` after
the cluster default is verified. Named guest StorageClasses are exceptions, not
the normal workload path.

## Verified Live Shape

As of the latest check, `slow` is the default StorageClass and uses:

```text
provisioner: driver.longhorn.io
diskSelector: hdd,seagate
numberOfReplicas: 1
reclaimPolicy: Delete
volumeBindingMode: Immediate
allowVolumeExpansion: true
```

The three HDD Longhorn disks on `the-abundance` are tagged with both `hdd` and `seagate`. That tag pairing is required for `slow` and the current Talos ISO backing-image StorageClass to provision successfully.

Node-specific NVMe classes use:

```text
provisioner: driver.longhorn.io
diskSelector: nvme
nodeSelector: <node name>
numberOfReplicas: 1
reclaimPolicy: Delete
volumeBindingMode: Immediate
allowVolumeExpansion: true
```

## Open Questions

- Decide whether `fast` and `fast-ha` should be deleted later or kept as historical experiments.
- Decide whether any future replicated NVMe class should exist under a clearer name.
- Decide backup policy for persistent data before deploying databases or application state.
