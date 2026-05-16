# Harvester Layer

Harvester creates and runs the virtual machines that Talos will turn into Kubernetes nodes.

This folder stores desired state and operator notes for Harvester-side resources:

- `namespaces/` for Kubernetes namespaces inside Harvester.
- `networks/` for Harvester VM network definitions.
- `storageclasses/` for Harvester storage class notes or manifests.
- `images/` for uploaded ISO/image tracking.
- `vms/talos/control-plane/` for Talos control-plane VM desired state.
- `vms/talos/workers/` for Talos worker VM desired state and size classes.
- `vms/data/` for dedicated data workload VM plans and future desired state.

Do not commit full live exports as source of truth if they include `managedFields`, `uid`, `resourceVersion`, `status`, or other generated runtime metadata.

Heavy ClickHouse, graph, streaming, and AI/data workloads should be represented as dedicated Harvester VMs first. Do not hide resource-dominant systems inside the shared Kubernetes worker pool unless there is a deliberate reason.
