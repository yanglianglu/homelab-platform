# Dedicated Data VMs

This directory owns Harvester-side plans and future desired state for dedicated data workload VMs.

Large ClickHouse, graph database, streaming, and AI/data workloads should run here as single-purpose VMs before they are considered for the shared Kubernetes worker pool.

Initial target:

| VM | Host | Initial size | Purpose | Status |
| --- | --- | ---: | --- | --- |
| `data-01` | `the-abundance` | 8 CPU / 32 Gi | ClickHouse and future graph workload | planned |

`data-01` should start small enough to leave Harvester headroom, then grow based on measured CPU, memory, disk, and IO pressure.
