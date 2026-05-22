# Harvester CSI Client Cluster Plan

`homelab-talos` uses Harvester CSI as the preferred PVC interface for guest
Kubernetes workloads. `data-01` remains the dedicated data scheduling anchor,
but storage should come from guest PVCs backed by Harvester StorageClasses
rather than manually mounted Talos local PVs.

## Current Decision

| Area | Decision |
| --- | --- |
| CSI namespace | `kube-system` |
| CSI chart | `harvester/harvester-csi-driver` `0.1.28` |
| Secret delivery | Infisical through External Secrets |
| Default durable tier | Harvester `slow`, single-replica HDD |
| Default guest StorageClass | `harvester`, mapped to host `slow` |
| Data scheduling node | `data-01` on `the-abundance` |
| Data taint | `data-platform=true:NoSchedule` |
| Talos mountpoint contract | Universal on every Talos node |
| Local PV model | Paused; fallback only |

Harvester CSI is used for Kubernetes-native lifecycle automation, not for new
high availability. The current `slow` policy stays single-replica and may be
unavailable when its backing host or disk is unavailable.

## Current State

| Item | State |
| --- | --- |
| CSI controller | Argo CD managed, `3/3` available |
| CSI node DaemonSet | Argo CD managed, `6/6` available |
| Secret | `kube-system/harvester-csi-config` from Infisical |
| CSI proof | Passed on `data-01` through reboot, resize, detach, and cleanup |
| Talos compatibility | `harvester-csi-mountpoint` extension active on all Talos nodes |
| GitOps status | `platform-harvester-csi` Synced/Healthy |
| Legacy `data-01` disks | Deleted after explicit cleanup gate |

The proof passed provisioning, attach, mount, write, restart persistence, 1 Gi
to 2 Gi resize, CSI node pod restart, `data-01` reboot recovery, scale-to-zero
detach, `NodeUnstageVolume`, guest PV deletion, Harvester backend PVC deletion,
and final `VolumeAttachment` cleanup. The reboot left an old failed proof pod
object that required manual deletion; storage detach itself had already
completed.

Only `data-01` had the Talos mountpoint extension at the first successful
proof. The extension has now been rolled to every Talos node.

## Guest StorageClasses

| Guest StorageClass | Host StorageClass | Reclaim | Use |
| --- | --- | --- | --- |
| `harvester` | `slow` | `Delete` | Default workload PVCs |
| `harvester-slow-delete` | `slow` | `Delete` | Disposable app/test PVCs |
| `harvester-slow-retain` | `slow` | `Retain` | Retained database/data PVCs |
| `harvester-abundance-nvme-delete` | `the-abundance-nvme` | `Delete` | Hot/temp/cache data pinned to `data-01` |
| `harvester-fast-ha-retain` | `fast-ha` | `Retain` | Deferred; approval-gated infrastructure only |

The generic guest StorageClass `harvester` remains the default and maps to host
StorageClass `slow` through the Harvester CSI chart setting
`hostStorageClass: slow`. Use explicit classes only for non-default reclaim
policy or host-specific storage tiers.

## Data Placement Contract

ClickHouse and future graph workloads should use both scheduling constraints
and storage-class selection:

```yaml
nodeSelector:
  homelab.local/node-class: data
  homelab.local/storage-locality: the-abundance
tolerations:
  - key: data-platform
    operator: Equal
    value: "true"
    effect: NoSchedule
```

The storage class chooses the Harvester-backed tier. The pod scheduling policy
chooses where the workload runs. Do not assume the storage class alone pins the
application to `data-01`.

## Production Gates

Harvester CSI is the standard PVC path for general workloads. Harvester and
guest Kubernetes observability are enabled, but large ClickHouse data still
requires alert review and an application-specific storage drill.

Required next gates:

1. Run a ClickHouse-specific pilot using PVCs before large ingestion.
2. Add reviewed, low-noise alerts after dashboard review.
3. Run a controlled Harvester host-maintenance CSI drill only with a separate
   approval gate.

## Secret Rules

- Do not commit Harvester kubeconfigs, service-account tokens, private keys, or
  generated `cloud-provider-config`.
- Do not read or print live Secret values while debugging.
- Keep the raw CSI credential in Infisical only.
- Store only non-secret CSI manifests, StorageClasses, and docs in Git.

## References

- Runbook: `docs/runbooks/harvester-csi-attachment-debugging.md`
- Fix record: `docs/runbooks/talos-harvester-csi-mountpoint-fix.md`
- Proof workload: `kubernetes/clusters/homelab/data-platform/csi-proof`
- CSI manifests: `kubernetes/clusters/homelab/platform/50-harvester-csi`
