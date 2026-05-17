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
| CSI controller | Installed manually, `3/3` available |
| CSI node DaemonSet | Installed manually, `6/6` available |
| Secret | `kube-system/harvester-csi-config` from Infisical |
| Small proof | Passed on `data-01` |
| Talos compatibility | Fixed on `data-01` with `harvester-csi-mountpoint` extension |
| GitOps status | Promoted in Git through `platform-harvester-csi`; pending sync until pushed/applied |
| Legacy `data-01` disks | Still attached, unused by Kubernetes |

The small proof passed provisioning, attach, mount, write, restart persistence,
scale-to-zero, `NodeUnstageVolume`, guest PV deletion, Harvester backend PVC
deletion, and final `VolumeAttachment` cleanup without manual intervention.

Only `data-01` had the Talos mountpoint extension at the first successful
proof. The platform contract is now stricter: every Talos node should carry the
same extension before broad CSI-backed workload scheduling is allowed.

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

Harvester CSI is the standard PVC path for general workloads. It is not yet
approved for large ClickHouse data or for detaching the legacy `data-01` disks
until larger drills pass.

Required next gates:

1. Roll the Talos mountpoint extension to every Talos node.
2. Push/sync the Argo CD managed `platform-harvester-csi` app.
3. Run larger drills: PVC expansion, CSI pod restart, `data-01` VM reboot,
   host-maintenance behavior, and performance testing.
4. Detach the legacy `data-01` 10 TiB and 1 TiB disks only after the larger
   drills pass and a detach plan is approved.

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
