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

For the active HA control plane (`cp-01`, `cp-02`, `cp-03`), the current
preferred recovery approach is:

1. Rebuild from Harvester VM settings and Talos config when possible.
2. Use Harvester VM snapshots only as short-term rollback points before risky changes.
3. Use Harvester VM backups only after a backup target is configured.
4. Do not perform destructive restore testing on active quorum members.

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
cp-02 VM: Running / Ready
cp-03 VM: Running / Ready
talos-cp-01 VM: retired
```

Implication:

- A real VM backup restore test cannot be performed until a backup target is configured.
- A destructive restore test should not be performed on active guest Kubernetes
  control-plane VMs.
- Safe next step is documentation and later testing with a disposable Talos VM or after adding more guest-cluster capacity.

## Initial Checks

1. Confirm Harvester UI is reachable at `192.168.1.50`.
2. Confirm Harvester nodes are reachable:
   - `the-abundance`: `192.168.1.241`
   - `the-elation`: `192.168.1.250`
   - `the-enigmata`: `192.168.1.244`
3. Confirm the Kubernetes API VIP responds at `192.168.1.184`.
4. Confirm Talos control-plane nodes respond at `192.168.1.181`,
   `192.168.1.182`, and `192.168.1.183`.
5. Check VM power state in Harvester.
6. Check Talos health from a trusted local workstation.

Useful Harvester checks:

```bash
kubectl --kubeconfig ~/.kube/harvester.yaml get nodes -o wide
kubectl --kubeconfig ~/.kube/harvester.yaml get virtualmachines -A
kubectl --kubeconfig ~/.kube/harvester.yaml get virtualmachinebackups.harvesterhci.io -A
kubectl --kubeconfig ~/.kube/harvester.yaml get virtualmachinesnapshots.snapshot.kubevirt.io -A
kubectl --kubeconfig ~/.kube/harvester.yaml get schedulevmbackups.harvesterhci.io -A
kubectl --kubeconfig ~/.kube/harvester.yaml get settings.harvesterhci.io backup-target -o yaml
```

## Harvester Management Plane Recovery

Use this procedure when the physical network has returned but the Harvester
VIP/UI at `192.168.1.50` is still unreachable, or when guest Talos VMs are
uncertain because the Harvester management API is down.

This is a gated live-cluster procedure. Read-only checks are safe; host service
restarts and physical node reboots require an explicit approval gate with target,
blast radius, validation, rollback, and stop conditions.

### Symptom Pattern

The 2026-05-19 recovery followed this pattern:

- Physical Harvester node IPs responded, but `192.168.1.50` did not.
- Physical node ARP/MAC ownership was not the root cause.
- Harvester RKE2/etcd had no stable leader and the VIP was not advertised.
- Guest Talos VMs could be partly running at the host level while their API
  path was still affected by the Harvester management outage.
- Rebooting `the-abundance` let `the-enigmata` recover RKE2/etcd first, then
  `the-elation` rejoined and the VIP returned.

### Read-Only Diagnosis

Start from the workstation:

```bash
curl -k -I --connect-timeout 5 https://192.168.1.50
arp -n 192.168.1.50
ping -c 3 192.168.1.241
ping -c 3 192.168.1.244
ping -c 3 192.168.1.250
nc -vz -w 3 192.168.1.181 6443
```

If the VIP is down but node SSH is available, inspect each Harvester physical
node without printing secrets:

```bash
hostname
uptime
sudo -n systemctl show rke2-server.service --property=LoadState,ActiveState,SubState,Result,NRestarts,MainPID --no-pager
sudo -n ss -lntp '( sport = :2379 or sport = :2380 or sport = :6443 or sport = :9345 or sport = :443 )'
sudo -n journalctl -u rke2-server -n 80 --no-pager
sudo -n ls -lh --time-style=long-iso /var/lib/rancher/rke2/server/db/snapshots | tail -n 8
```

Interpretation:

- `ActiveState=active` and `SubState=running` on at least one server is a good
  sign; wait a short window for the other servers to rejoin before rebooting
  more hosts.
- Repeated `failed to reconcile with local datastore`, `no leader`, or etcd
  `context deadline exceeded` means the management plane is not healthy even if
  node networking works.
- If `/run/k3s/containerd/containerd.sock` refuses connections, RKE2/containerd
  may still be booting or wedged; do not assume the VMs are gone.
- Existing local snapshots under
  `/var/lib/rancher/rke2/server/db/snapshots` are important evidence before any
  disaster-recovery step.

### Recovery Gates

Gate H1 is read-only validation:

```bash
kubectl --kubeconfig ~/.kube/harvester.yaml get nodes -o wide
kubectl --kubeconfig ~/.kube/harvester.yaml get vm -A
kubectl --kubeconfig ~/.kube/harvester.yaml get vmi -A
kubectl --kubeconfig ~/.kube/harvester.yaml get pods -A --no-headers | rg -v '\s(Running|Succeeded|Completed)\s'
```

If H1 cannot reach the API and RKE2 is wedged, Gate H2 is a controlled
`rke2-server` restart on the least disruptive target first. Run only after
explicit approval:

```bash
sudo -n systemctl restart --no-block rke2-server
```

Validate after each node before touching the next one:

```bash
sudo -n systemctl show rke2-server.service --property=ActiveState,SubState,Result,NRestarts,MainPID --no-pager
sudo -n journalctl -u rke2-server -n 40 --no-pager
curl -k -I --connect-timeout 5 https://192.168.1.50
```

If H2 does not recover the VIP and the service layer is exhausted, Gate H3 is a
single physical-node reboot. Choose one node, state the VM impact, and validate
before rebooting any other node. The 2026-05-19 incident recovered after
rebooting `the-abundance`:

```bash
sudo -n systemctl reboot --no-wall
```

Post-reboot validation:

```bash
kubectl --kubeconfig ~/.kube/harvester.yaml get nodes -o wide
kubectl --kubeconfig ~/.kube/harvester.yaml get vm -A
kubectl --kubeconfig ~/.kube/harvester.yaml get vmi -A
kubectl --kubeconfig ~/.kube/harvester.yaml -n longhorn-system get nodes.longhorn.io
kubectl --kubeconfig ~/.kube/harvester.yaml -n longhorn-system get volumes.longhorn.io
kubectl --kubeconfig ~/.kube/harvester.yaml get pods -A --no-headers | rg -v '\s(Running|Succeeded|Completed)\s'
curl -k -I --connect-timeout 5 https://192.168.1.50
nc -vz -w 3 192.168.1.181 6443
```

Stop and escalate to a separate RKE2/etcd disaster-recovery plan if:

- the rebooted node does not return to the network,
- the VIP remains down after one reboot gate and settle time,
- etcd membership/config differs from the expected three-node cluster, or
- RKE2 logs continue to report datastore reconciliation failures.

Do not run `rke2 server --cluster-reset`, restore from an etcd snapshot, delete
etcd data, or remove etcd members from this procedure. Those are separate
disaster-recovery gates and require a fresh plan that preserves snapshots and
names the restore source.

## When To Rebuild Instead Of Restore

Prefer rebuild when:

- The workload is represented in GitOps.
- The data is external or reingestable.
- The node can be recreated from Talos machine config.
- A restore would risk active control-plane quorum.
- The recovery goal is clean state rather than preserving local disk state.

For active Talos control-plane VMs, rebuild should use:

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

Do not test destructive restore on active guest Kubernetes control-plane VMs.

Safer future test options:

1. Create a disposable Talos VM and test snapshot/restore there.
2. Configure Harvester backup target, back up a disposable VM, and restore it as a new VM.
3. Test restore of a real control-plane VM only after a separate quorum and
   rollback plan is approved.

Track this as a future hardening/recovery task.

## Do Not

- Do not commit recovered plaintext kubeconfig or Talos secrets.
- Do not replace desired-state files with live exports containing runtime metadata.
- Do not assume GitOps replaces secrets, identity, metadata, or local-only state backups.
- Do not perform destructive restore tests on active guest Kubernetes
  control-plane VMs.
