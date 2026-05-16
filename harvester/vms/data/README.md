# Data VM History

This directory records the rejected standalone data VM alternative.

The current decision is that `data-01` joins `homelab-talos` as a tainted Talos worker, with Harvester desired state under `harvester/vms/talos/workers/data-01.bootstrap.yaml`.

Rejected standalone target:

| VM | Host | Initial size | Purpose | Status |
| --- | --- | ---: | --- | --- |
| `data-01` | `the-abundance` | 8 CPU / 32 Gi | Standalone Linux ClickHouse and graph workload | rejected alternative |

Keep this note so future planning remembers why the data workload is Kubernetes-native but still isolated by taint, placement, and storage locality.
