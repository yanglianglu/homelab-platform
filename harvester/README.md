# Harvester Layer

Harvester creates and runs the virtual machines that Talos will turn into Kubernetes nodes.

This folder stores desired state and operator notes for Harvester-side resources:

- `namespaces/` for Kubernetes namespaces inside Harvester.
- `networks/` for Harvester VM network definitions.
- `storageclasses/` for Harvester storage class notes or manifests.
- `images/` for uploaded ISO/image tracking.
- `vms/` for cleaned VM desired-state files.

Do not commit full live exports as source of truth if they include `managedFields`, `uid`, `resourceVersion`, `status`, or other generated runtime metadata.
