# Storage

Kubernetes-side storage policies and CSI-related resources live here.

Harvester StorageClasses are documented under `harvester/storageclasses/`.

Approved storage intent:

- `slow`: production-ready Exos HDD-backed default.
- `nvme`: shared fast PVC class, only after intentionally created.
- node-specific NVMe classes: temporary/cache/local workloads.
- `fast-ha`: approval-gated only.
