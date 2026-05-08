# Storage

Storage design notes for Harvester volumes and Kubernetes storage classes.

## Current Baseline

- Talos OS disk: `100 Gi`
- Talos install disk inside the VM: `/dev/vda`
- Harvester storage class placeholder: `fast`

## Boundaries

- Harvester storage definitions belong under `harvester/storageclasses/`.
- Kubernetes storage classes, CSI settings, and persistent volume policies belong under `kubernetes/clusters/homelab/infrastructure/storage/`.
- Do not store live runtime exports with `status`, `uid`, `resourceVersion`, or `managedFields` as source of truth.
