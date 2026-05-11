# Talos Worker Size Classes

Use these profiles when creating Talos worker VMs.

| Size | vCPU | Memory | OS disk | OS disk StorageClass |
| --- | ---: | ---: | ---: | --- |
| Small | 2 | 8 Gi | 80 Gi | `slow` |
| Medium | 4 | 12 Gi | 100 Gi | `slow` |
| Large | 6 | 24 Gi | 120 Gi | `slow` |

Recommended initial worker placement:

| Worker | Host | Size | IP |
| --- | --- | --- | --- |
| `worker-01` | `the-elation` | Medium | `192.168.1.179` |
| `worker-02` | `the-enigmata` | Medium | `192.168.1.180` |

Large streaming, data warehouse, and AI workloads should run as dedicated single-purpose VMs instead of forcing the shared Kubernetes worker pool to become oversized. HA and read/write split are deferred unless a specific workload proves the need.

Storage rules:

- Use `slow` for Talos OS disks.
- Use `nvme` for shared fast PVCs after the class is created.
- Use node-specific NVMe classes for temporary/cache/local workloads.
- Use `fast-ha` only with explicit approval.

Template variables:

```text
VM_NAME=
HOSTNAME=
IP_ADDRESS=
MAC_ADDRESS=
SIZE_CLASS=
VCPU=
MEMORY=
OS_DISK_SIZE=
HOST_PREFERENCE=
```
