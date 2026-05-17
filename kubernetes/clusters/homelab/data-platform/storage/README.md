# Data Platform Storage

Harvester CSI is the preferred storage path for data-platform workloads.

Do not create static local PVs for `data-01` unless the CSI path fails a future
required gate and the local-PV fallback is explicitly approved.

Planned data-platform StorageClasses:

| StorageClass | Backing Harvester class | Reclaim | Use |
| --- | --- | --- | --- |
| `harvester` | `slow` | `Delete` | default workload PVCs |
| `harvester-slow-retain` | `slow` | `Retain` | ClickHouse retained data |
| `harvester-abundance-nvme-delete` | `the-abundance-nvme` | `Delete` | ClickHouse temp/cache/hot data |

StorageClass manifests are staged in
`../../platform/50-harvester-csi`, not in this directory.

Proof gate:

- Harvester CSI is promoted into Argo CD management through
  `platform/50-harvester-csi`.
- The small proof PVC passes on `data-01`.
- Production ClickHouse PVCs still require expansion, reboot, maintenance, and
  performance drills.

The proof workload is staged in `../csi-proof` and remains an operator-run
drill workload.

The legacy `data-01` rollback PVCs were deleted after the CSI-first model became
the accepted storage path. Do not recreate static local PVs unless the CSI path
is explicitly rejected.
