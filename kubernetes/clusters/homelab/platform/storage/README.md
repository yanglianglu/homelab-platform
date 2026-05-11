# Storage

Kubernetes-side storage policies and CSI-related resources live here.

Harvester StorageClasses are documented under `harvester/storageclasses/`.

Approved storage intent:

- `slow`: durable HDD-backed default.
- `nvme`: shared fast PVC class, to be created.
- node-specific NVMe classes: temporary/cache/local workloads.
- `fast-ha`: approval-gated only.
