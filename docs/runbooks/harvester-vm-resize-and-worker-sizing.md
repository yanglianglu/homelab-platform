# Runbook: Harvester VM Resize And Talos Worker Sizing

This guide defines practical resize operations and Talos worker size classes for the homelab.

It is based on:

- Harvester v1.8 docs for VM editing, live migration, CPU model selection, and resource overcommit.
- Harvester v1.8 CPU and memory hotplug docs.
- Harvester volume expansion docs.
- Talos disk management docs.
- Current live Harvester node capacity.

## Current Capacity Snapshot

Last checked: 2026-05-10.

| Harvester node | CPU allocatable | Memory allocatable | Current usage summary | Sizing implication |
| --- | ---: | ---: | --- | --- |
| `the-abundance` | ~30.9 CPU | ~64 Gi | Hosts `cp-01`; low CPU, moderate memory | Keep control-plane and Harvester headroom here |
| `the-elation` | ~19 CPU | ~64 Gi | Low CPU, low memory | Good host for general Kubernetes worker and dedicated workload VMs |
| `the-enigmata` | ~9 CPU | ~32 Gi | Low CPU, higher memory percentage | Good host for a medium worker; avoid large shared worker for now |

Current guest control plane:

| VM | Host | vCPU | Memory | OS disk | Role |
| --- | --- | ---: | ---: | ---: | --- |
| `cp-01` | `the-abundance` | 4 | 8 Gi | 100 Gi | Talos control plane |

## Approved Storage Rules

| StorageClass | Use |
| --- | --- |
| `slow` | Talos OS disks and normal durable HDD-backed PVCs |
| `nvme` | Shared fast PVCs once created |
| `fast-ha` | Approval-gated only; use only after explicit discussion |
| `the-abundance-nvme` | Node-local temporary/cache workloads on `the-abundance` |
| `the-elation-nvme` | Node-local temporary/cache workloads on `the-elation` |
| `the-enigmata-nvme` | Node-local temporary/cache workloads on `the-enigmata` |

Do not use `fast-ha` without explicit owner approval.

## Worker Size Classes

These are Talos worker VM classes, not Kubernetes pod classes.

| Size | vCPU | Memory | OS disk | Best use |
| --- | ---: | ---: | ---: | --- |
| Small | 2 | 8 Gi | 80 Gi | GitOps bootstrap, light services, test worker |
| Medium | 4 | 12 Gi | 100 Gi | General platform worker, dashboards, moderate apps |
| Large | 6 | 24 Gi | 120 Gi | Rare oversized Kubernetes worker; not the default for data warehouse or streaming |

OS disk should use `slow`. Workload data should use Kubernetes PVCs, not the Talos OS disk.

## Recommended Initial Workers

| VM | Host | Size | vCPU | Memory | OS disk | IP | Reason |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `worker-01` | `the-elation` | Medium | 4 | 12 Gi | 100 Gi | `192.168.1.179` | General Kubernetes platform/app worker |
| `worker-02` | `the-enigmata` | Small | 2 | 8 Gi | 80 Gi | `192.168.1.180` | Smaller scheduling/failure-spread worker on the smallest host |

`worker-03` is deferred until scheduling pressure or workload metrics prove the need.

Heavy streaming, data warehouse, AI serving, and other resource-dominant workloads should use dedicated single-purpose VMs instead of driving the shared Kubernetes worker size. HA and read/write split are deferred unless a specific workload proves the need.

## Dedicated Workload VM Classes

Use these outside the shared Kubernetes worker pool when a workload has dominant CPU, memory, disk, network, or GPU behavior.

| Class | vCPU | Memory | Storage starting point | Use |
| --- | ---: | ---: | --- | --- |
| Data VM | 6-12 | 32-64 Gi | `slow` for retained data, `nvme` for hot data | ClickHouse, data warehouse, large analytical stores |
| Streaming VM | 4-8 | 16-32 Gi | `nvme` for hot queues, `slow` for retained/archive data | ADS-B ingestion, stream processors, Kafka/Redpanda-style experiments |
| AI VM | Workload/GPU dependent | 32-64 Gi | NVMe preferred for model/cache data | vLLM, Ollama, embedding/vector experiments |

For the home server, prefer one dedicated VM per large workload family. `data-01` starts on `the-abundance` at 8 vCPU / 32 Gi with 8-10 TiB retained data and 1 TiB hot/temp NVMe. Do not design HA/read-write split until there is a clear operational reason.

## Resize Principles

Prefer this order:

1. Resize Kubernetes PVCs for application storage.
2. Resize worker CPU/RAM when scheduling capacity is needed.
3. Resize Talos OS disks only when image/cache/log pressure proves it is needed.
4. Add another worker before making `cp-01` much larger.

## CPU And Memory Resize

Harvester supports CPU and memory hotplug for VMs when enabled during VM creation and when the VM is live-migratable. If hotplug is not available or not desired, edit the VM config and restart the VM.

Practical safe path for an existing Talos worker:

```bash
kubectl --context homelab-talos drain worker-01 \
  --ignore-daemonsets \
  --delete-emptydir-data
```

Then in Harvester:

1. Edit the VM.
2. Change CPU and/or memory.
3. Save and restart, or use CPU/memory hotplug if enabled and appropriate.
4. Wait for the node to return.

Verify:

```bash
kubectl --context homelab-talos get nodes -o wide
kubectl --context homelab-talos describe node worker-01
kubectl --context homelab-talos uncordon worker-01
```

For a fresh worker with no workloads, draining is unnecessary.

## OS Disk Resize

Harvester supports volume expansion when the storage backend supports it. Longhorn V1 supports online expansion, but the Harvester UI has limitations around resizing VM volumes while a VM is running. The conservative path is still:

1. Drain the node if it is already running workloads.
2. Shut down the VM.
3. Expand the volume from the VM Volumes tab or the volume object.
4. Start the VM.
5. Verify Talos sees the updated disk/volume state.

Useful checks:

```bash
talosctl --nodes <node-ip> get disks
talosctl --nodes <node-ip> get discoveredvolumes
kubectl --context homelab-talos describe node <node-name>
```

Talos uses the system disk for boot/state and an `EPHEMERAL` volume for container data, images, logs, and related runtime data. By default, `EPHEMERAL` grows to use available space on the system disk at initial provisioning. Avoid relying on OS disk expansion as the normal way to add application storage.

## Live Migration Notes

Live migration requires a compatible target node, enough resources, compatible CPU model, and migratable VM storage/devices.

For mixed CPU clusters, Harvester recommends using a named CPU model supported by all migration target nodes instead of relying on `host-model` or `host-passthrough`. This should be decided before making migration-dependent worker templates.

## Template Policy

Create worker manifests from size templates instead of hand-editing each VM from scratch.

Template fields that should vary per worker:

- VM name
- hostname
- static IP
- MAC address
- target Harvester host preference
- size class

Template fields that should stay consistent:

- namespace: `talos-cluster`
- VM network: `lan-untagged`
- OS disk storage: `slow`
- Talos version: `v1.13.0`
- Kubernetes version: `v1.36.0`
- `fast-ha` not used without explicit approval

## Sources

- Harvester v1.8 Edit VM docs: https://docs.harvesterhci.io/v1.8/vm/edit-vm/
- Harvester v1.8 CPU and memory hotplug docs: https://docs.harvesterhci.io/v1.8/vm/cpu-memory-hotplug/
- Harvester v1.8 CPU model selection docs: https://docs.harvesterhci.io/v1.8/vm/select-cpu-model/
- Harvester live migration docs: https://docs.harvesterhci.io/v1.8/vm/live-migration/
- Harvester volume expansion docs: https://docs.harvesterhci.io/v1.7/volume/edit-volume/
- Harvester resource overcommit and memory overhead docs: https://docs.harvesterhci.io/v1.8/advanced/
- Talos disk management docs: https://www.talos.dev/latest/talos-guides/configuration/disk-management/
