# Storage

Kubernetes-side storage policies and CSI-related resources live here.

Harvester StorageClasses are documented under `harvester/storageclasses/`.

Approved guest-cluster storage intent:

- `harvester`: Harvester `slow`, `Delete`, default workload PVCs.
- `harvester-slow-retain`: Harvester `slow`, `Retain`, for ClickHouse retained data.
- `harvester-slow-delete`: Harvester `slow`, `Delete`, for disposable app/test PVCs.
- `harvester-abundance-nvme-delete`: Harvester `the-abundance-nvme`, `Delete`, for data-platform temp/cache/hot data pinned to `data-01`.
- `harvester-fast-ha-retain`: Harvester `fast-ha`, `Retain`, approval-gated only.

Harvester CSI is the preferred guest-cluster storage interface. The small
`data-01` proof now passes cleanup after the `harvester-csi-mountpoint` Talos
extension fix. Larger reboot, maintenance, expansion, and performance drills
are still required before any ClickHouse production PVCs are created.

StorageClass manifests and the Harvester CSI chart Application live under
`../50-harvester-csi`.

The legacy `data-01` rollback PVCs were deleted after the CSI-first model became
the accepted storage path.
