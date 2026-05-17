# Gradual VM Growth Plan

This plan records the current staged VM growth model for `homelab-talos`.

## Current Shape

```text
3 Talos control-plane VMs
2 general Talos worker VMs
1 dedicated Talos data worker
optional worker-03 later, only if metrics justify it
```

| Host | VM | Size | Role | Status |
| --- | --- | ---: | --- | --- |
| `the-abundance` | `cp-01` | 4 CPU / 8 Gi | Control plane | active |
| `the-elation` | `cp-02` | 4 CPU / 8 Gi | Control plane | active |
| `the-enigmata` | `cp-03` | 4 CPU / 8 Gi | Control plane | active |
| `the-elation` | `worker-01` | 4 CPU / 12 Gi | General worker | active |
| `the-enigmata` | `worker-02` | 2 CPU / 8 Gi | General worker | active |
| `the-abundance` | `data-01` | 8 CPU / 32 Gi | Tainted data worker | active |

The Kubernetes API uses kube-vip at `192.168.1.184`. Individual node IPs remain
break-glass endpoints for Talos and incident work.

## Storage Direction

`data-01` was originally given a 10 TiB retained disk and 1 TiB hot/temp disk.
The current direction is CSI-first storage instead:

| Storage | Current use |
| --- | --- |
| `slow` | Default production HDD-backed Harvester class |
| `harvester` | Default guest workload PVCs mapped to host `slow` |
| `harvester-slow-delete` | Explicit disposable guest PVCs and tests |
| `harvester-slow-retain` | Future retained data PVCs |
| `harvester-abundance-nvme-delete` | Future hot/temp/cache PVCs pinned to `data-01` |
| Legacy attached `data-01` disks | Attached but unused pending larger CSI drills |

## Remaining Growth Gates

1. Roll the Talos mountpoint extension to all nodes as the universal CSI host contract.
2. Sync the Argo CD managed Harvester CSI app from Git.
3. Run CSI expansion, restart, reboot, cleanup, and performance drills.
4. Use the guest observability baseline to debug Gateway/TLS work and larger
   ClickHouse planning.
5. Add internal Gateway API routing with Envoy Gateway, cert-manager,
   trust-manager, and internal DNS after the platform baseline is stable. Keep
   Cloudflare and public exposure as a separate future decision.
6. Add `worker-03` only when scheduling pressure or workload metrics justify it.

## Acceptance Criteria

- Harvester keeps practical headroom after each VM or storage wave.
- `kubectl get nodes` shows all Talos nodes Ready.
- Talos health passes across all control-plane nodes.
- Kubernetes API access uses `192.168.1.184`, not only `cp-01`.
- Normal workloads schedule on workers.
- `data-01` is monitored before large ingestion begins.
