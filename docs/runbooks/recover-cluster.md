# Runbook: Recover Cluster

Recovery steps belong here as the lab matures. Keep this document practical and incident-focused.

## Recovery Philosophy

The homelab should prefer rebuildable infrastructure over restoring every VM from backup.

Primary recovery model:

```text
GitHub restores desired state.
Talos config restores node configuration.
GitOps restores workloads.
External systems can rehydrate rebuildable datasets.
Backups protect secrets, identity, metadata, and local-only state.
```

Do not treat every VM disk as equally important. Classify workloads first:

| Class | Meaning | Recovery strategy |
| --- | --- | --- |
| `rebuildable` | Can be recreated from Git, Talos config, or automation | Rebuild, do not back up heavily |
| `reingestable` | Data can be retrieved again from an external source | Reingest; backup only if reingestion cost is high |
| `important-local` | Local state cannot be recreated easily | Back up |
| `critical-platform` | Identity, secrets, configs, or keys needed to recover | Back up securely |
| `temporary` | Cache, scratch, or disposable data | No backup |

For the active `cp-01` control-plane VM, the current preferred recovery approach is:

1. Rebuild from Harvester VM settings and Talos config when possible.
2. Use Harvester VM snapshots only as short-term rollback points before risky changes.
3. Use Harvester VM backups only after a backup target is configured.
4. Do not perform destructive restore testing on the only guest Kubernetes control-plane VM.

## Harvester Recovery Mechanisms

| Mechanism | Stored where | Use for | Current status |
| --- | --- | --- | --- |
| VM snapshot | Inside the Harvester/Longhorn cluster | Short-term rollback before risky VM changes | No snapshots currently present |
| VM backup | External NFS or S3-compatible backup target | Real VM disaster recovery | Backup target not configured |
| Scheduled VM backup/snapshot | Harvester schedule controller | Recurring protection after policy exists | No schedules currently present |
| Longhorn volume snapshot/backup | Longhorn layer | App/PVC or low-level storage use cases | Avoid using directly for Harvester VM disks unless intentionally needed |
| Rebuild from config | GitHub + Talos config + GitOps | Preferred for rebuildable platform state | Primary strategy |

## Current Backup/Snapshot Status

Latest live checks showed:

```text
Harvester backup-target configured: False
VirtualMachineBackups: none
VirtualMachineSnapshots: none
ScheduleVMBackups: none
cp-01 VM: Running / Ready
talos-cp-01 VM: retained, pending retirement
```

Implication:

- A real VM backup restore test cannot be performed until a backup target is configured.
- A destructive restore test should not be performed on the active guest Kubernetes control-plane VM.
- Safe next step is documentation and later testing with a disposable Talos VM or after adding more guest-cluster capacity.

## Initial Checks

1. Confirm Harvester UI is reachable at `192.168.1.50`.
2. Confirm Harvester nodes are reachable:
   - `the-abundance`: `192.168.1.241`
   - `the-elation`: `192.168.1.250`
   - `the-enigmata`: `192.168.1.244`
3. Confirm the Talos node responds at `192.168.1.181`.
4. Check VM power state in Harvester.
5. Check Talos health from a trusted local workstation.

Useful Harvester checks:

```bash
kubectl --kubeconfig ~/.kube/harvester.yaml get nodes -o wide
kubectl --kubeconfig ~/.kube/harvester.yaml get virtualmachines -A
kubectl --kubeconfig ~/.kube/harvester.yaml get virtualmachinebackups.harvesterhci.io -A
kubectl --kubeconfig ~/.kube/harvester.yaml get virtualmachinesnapshots.snapshot.kubevirt.io -A
kubectl --kubeconfig ~/.kube/harvester.yaml get schedulevmbackups.harvesterhci.io -A
kubectl --kubeconfig ~/.kube/harvester.yaml get settings.harvesterhci.io backup-target -o yaml
```

## When To Rebuild Instead Of Restore

Prefer rebuild when:

- The workload is represented in GitOps.
- The data is external or reingestable.
- The node can be recreated from Talos machine config.
- A restore would risk the only control-plane VM.
- The recovery goal is clean state rather than preserving local disk state.

For `cp-01`, rebuild should use:

- `docs/runbooks/create-talos-vm.md`
- `talos/clusters/homelab/cluster-vars.yaml`
- Talos patches and scripts under `talos/clusters/homelab/`
- Locally stored, non-committed Talos secrets and kubeconfig

## When To Use VM Snapshot

Use a Harvester VM snapshot when:

- Making a risky but reversible VM-level change.
- Testing Talos machine config changes that affect boot or disk behavior.
- You need a short-term local rollback point.

Do not rely on VM snapshots for:

- Harvester cluster loss.
- Long-term backup.
- Protection from storage failure affecting the same cluster.

## When To Use VM Backup

Use a Harvester VM backup when:

- A backup target is configured.
- You need restore capability after Harvester/Longhorn storage loss.
- You need a recovery point that can survive local cluster failure.
- The VM contains state that is hard to rebuild.

Current blocker:

```text
backup-target is not configured
```

Until this is fixed, VM backup restore testing is deferred.

## Deferred Restore Test

Do not test destructive restore on `cp-01` while it is the active guest Kubernetes control-plane VM.

Safer future test options:

1. Create a disposable Talos VM and test snapshot/restore there.
2. Configure Harvester backup target, back up a disposable VM, and restore it as a new VM.
3. Add more guest Kubernetes control-plane capacity before testing restore of a real control-plane VM.

Track this as a future hardening/recovery task.

## Do Not

- Do not commit recovered plaintext kubeconfig or Talos secrets.
- Do not replace desired-state files with live exports containing runtime metadata.
- Do not assume GitOps replaces secrets, identity, metadata, or local-only state backups.
- Do not perform destructive restore tests on the only guest Kubernetes control-plane VM.
