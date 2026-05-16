# Rejected Alternative: Standalone data-01

This file preserves the previous standalone Linux VM idea. The accepted plan is now `data-01` as a Talos worker in `homelab-talos`.

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

- Rejected: ClickHouse starts on a standalone Linux VM outside Kubernetes.
- Accepted: ClickHouse starts on tainted Talos worker `data-01` inside Kubernetes.
- Graph database sizing remains deferred until the graph engine and working set are defined.
- Monitor `data-01` before large ingestion begins.
- Do not treat VM-local or single-replica storage as a backup.
