# Data Platform Plan

Large analytical and graph workloads use a dedicated VM before they use the shared Kubernetes worker pool.

## Initial Data VM

| VM | Host | Initial size | Role |
| --- | --- | ---: | --- |
| `data-01` | `the-abundance` | 8 CPU / 32 Gi | ClickHouse and future graph workloads |

`the-abundance` is the primary data host because it has the large HDD/NVMe capacity.

## Workload Boundaries

| Workload | Initial placement | Notes |
| --- | --- | --- |
| ClickHouse | `data-01` | Main OLAP engine for 10-30 TiB analysis |
| Graph database | Deferred on `data-01` | Select engine and working set before allocating 1-10 TiB |
| Dashboards | Kubernetes observability domain | Grafana belongs in the guest cluster |
| Metrics | Kubernetes observability domain | VictoriaMetrics starts in the guest cluster |
| Large raw/archive data | `data-01` or external storage | Do not assume VM-local storage is a backup |

## Growth Rules

- Add CPU when ClickHouse query profiles show CPU pressure.
- Add memory when queries spill, cache pressure is high, or graph working set requires it.
- Add NVMe when merges, temp files, or graph random IO become the bottleneck.
- Add HDD capacity when ClickHouse reaches 70-75% disk usage.
- Define the graph engine and working set before allocating multi-terabyte graph storage.
