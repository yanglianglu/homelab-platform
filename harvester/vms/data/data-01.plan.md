# data-01 Plan

`data-01` is the dedicated VM for large analytical and graph workloads.

## Initial Size

| Resource | Initial value |
| --- | ---: |
| vCPU | 8 |
| Memory | 32 Gi |
| OS disk | 100 Gi |
| ClickHouse data disk | 8-10 TiB |
| Hot/temp NVMe disk | 1 TiB |
| Graph storage | deferred or 1 TiB after engine selection |

## Growth Path

| Resource | Growth path |
| --- | --- |
| vCPU | 8 -> 12 |
| Memory | 32 Gi -> 48/64 Gi |
| ClickHouse data | 10 TiB -> 20 TiB -> 30 TiB |
| Hot/temp NVMe | 1 TiB -> 2 TiB |

## Boundaries

- ClickHouse starts on this VM, not in the Kubernetes worker pool.
- Graph database sizing remains deferred until the graph engine and working set are defined.
- Monitor `data-01` before large ingestion begins.
- Do not treat VM-local or single-replica storage as a backup.
