# Runbook: Create Talos VM

This runbook captures the intended Harvester-side VM settings for the first Talos control plane VM.

## VM Settings

| Setting | Value |
| --- | --- |
| Name | `talos-cp-01` |
| Namespace | `talos-cluster` |
| VM Network | `lan-untagged` |
| Network model | `virtio` |
| IP | `192.168.1.178` |
| MAC | `52:a8:b1:09:a7:8f` |
| CPU | `4` |
| Memory | `8 Gi` |
| OS disk | `100 Gi` |
| OS disk bus | `virtio` |
| Talos ISO | Attached as CD-ROM |
| UEFI | Enabled |
| EFI persistent state | Enabled |
| Secure Boot | Disabled |
| TPM | Disabled |
| QEMU guest agent | Disabled |
| SSH key | Blank |
| Cloud-init user-data | Blank |
| Cloud-init network-data | Blank |

## Steps

1. Confirm the `talos-cluster` namespace exists.
2. Confirm the `lan-untagged` VM network exists under Cluster Network `mgmt`.
3. Upload or reference `talos-metal-amd64-v1.13.0.iso`.
4. Create VM `talos-cp-01` in namespace `talos-cluster`.
5. Set CPU to `4` and memory to `8 Gi`.
6. Attach the Talos ISO as a CD-ROM.
7. Add a `100 Gi` OS disk using the `virtio` bus.
8. Attach VM Network `lan-untagged` using network model `virtio`.
9. Enable UEFI and EFI persistent state.
10. Disable Secure Boot, TPM, and QEMU guest agent.
11. Leave SSH key, cloud-init user-data, and cloud-init network-data blank.
12. Confirm the VM receives or uses `192.168.1.178`.
