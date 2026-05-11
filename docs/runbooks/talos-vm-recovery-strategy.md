# Runbook: Talos VM Recovery Strategy

This runbook explains how to decide between rebuilding a Talos VM, using a Harvester VM snapshot, or using a Harvester VM backup.

## Current State

| Item | Current status |
| --- | --- |
| Talos VM | `cp-01` |
| Namespace | `talos-cluster` |
| VM status | Running / Ready |
| Guest cluster role | Active guest Kubernetes control-plane node |
| Harvester backup target | Not configured |
| VM backups | None present |
| VM snapshots | None present |
| VM backup/snapshot schedules | None present |

## Decision Tree

```text
Is the VM disposable or rebuildable?
  yes -> rebuild from Git/Talos config
  no  -> continue

Is this a short-term rollback before a risky change?
  yes -> use Harvester VM snapshot
  no  -> continue

Is an external Harvester backup target configured?
  yes -> use Harvester VM backup for disaster recovery
  no  -> configure backup target before relying on VM backup
```

## Preferred Strategy For This Homelab

Because the platform is intended to be GitOps-based and much app data is reingestable from external systems, the default recovery strategy is rebuild first.

Use backups for:

- Secrets and identity material.
- Talos secrets and kubeconfig stored outside Git.
- Important local metadata databases.
- Local-only object storage or datasets.
- Portfolio app state that cannot be recreated.

Do not back up:

- Temporary/cache/scratch data.
- Node-specific NVMe scratch workloads.
- Rebuildable app deployments already represented in GitOps.
- Reingestable external datasets unless reingestion time is unacceptable.

## Snapshot Use Cases

Use VM snapshots for short-term protection before:

- Talos disk changes.
- VM firmware/boot changes.
- Storage migration.
- Risky Harvester-side VM edits.

Snapshots are not disaster recovery because they live in the same Harvester/Longhorn environment.

## Backup Use Cases

Use VM backups after configuring an external NFS or S3-compatible backup target.

VM backups are for:

- Restoring a VM after local storage failure.
- Restoring a VM into another Harvester cluster.
- Protecting non-rebuildable VM state.

## Current Recommendation

Do not perform a destructive restore test on `cp-01` while it is the active guest Kubernetes control-plane VM.

Instead:

1. Keep Talos source config and runbooks current.
2. Configure `kubectl` and `talosctl` access.
3. Configure a Harvester backup target later.
4. Test snapshot/backup restore on a disposable Talos VM.
5. Add more guest Kubernetes capacity before testing restore of production control-plane state.
