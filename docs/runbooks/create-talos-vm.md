# Runbook: Create Talos VM

This runbook captures the Harvester-side VM settings for Talos nodes. It is a
procedure template, not a request to create VMs.

## Current VM Set

| VM | Role | Host | IP | Size |
| --- | --- | --- | --- | --- |
| `cp-01` | control plane | `the-abundance` | `192.168.1.181` | 4 CPU / 8 Gi |
| `cp-02` | control plane | `the-elation` | `192.168.1.182` | 4 CPU / 8 Gi |
| `cp-03` | control plane | `the-enigmata` | `192.168.1.183` | 4 CPU / 8 Gi |
| `worker-01` | worker | `the-elation` | `192.168.1.179` | 4 CPU / 12 Gi |
| `worker-02` | worker | `the-enigmata` | `192.168.1.180` | 2 CPU / 8 Gi |
| `data-01` | data worker | `the-abundance` | `192.168.1.185` | 8 CPU / 32 Gi |

`worker-03` is deferred until metrics justify it.

## Standard Settings

| Setting | Default |
| --- | --- |
| Namespace | `talos-cluster` |
| VM network | `lan-untagged` |
| Network model | `virtio` |
| OS disk class | `slow` |
| OS disk bus | `virtio` |
| UEFI | Enabled |
| EFI persistent state | Enabled |
| Secure Boot | Disabled |
| TPM | Disabled |
| QEMU guest agent | Disabled |
| SSH key | Blank |
| Cloud-init user-data | Blank |
| Cloud-init network-data | Blank |

Talos ISO attachment is temporary for installation. After install, detach the
ISO or ensure the OS disk is first in boot order before any VM restart.

## Steps

1. Confirm `talos-cluster` namespace exists.
2. Confirm the `lan-untagged` VM network exists under Cluster Network `mgmt`.
3. Confirm the Talos ISO image exists.
4. Create the VM with the intended CPU, memory, host placement, OS disk, and IP.
5. Attach the Talos ISO only for first install.
6. Apply the correct Talos machine config for the node role.
7. After install, boot from OS disk first.
8. Verify VM Running/Ready, VMI host placement, guest IP, Talos API reachability,
   and Kubernetes node readiness when relevant.

## Source References

- Control-plane placement: `harvester/vms/talos/control-plane/README.md`
- Worker placement: `harvester/vms/talos/workers/README.md`
- Size classes: `harvester/vms/talos/workers/size-classes.md`
- Talos config workflow: `docs/runbooks/apply-talos-config.md`
