# Runbook: Talos Harvester CSI Mountpoint Fix

This runbook records the Talos host utility fix required for Harvester CSI
cleanup on Talos nodes.

Do not run Talos upgrades from this runbook without explicit approval for that
gate.

## Status

Fixed first on `data-01` on 2026-05-16 America/Chicago. The current platform
policy is to roll the extension to every Talos node before broad CSI-backed
workload scheduling.

| Item | Value |
| --- | --- |
| First Talos node | `data-01` / `192.168.1.185` |
| Extension | `harvester-csi-mountpoint` `0.1.0` |
| Extension image | `docker.io/lyangliang/harvester-csi-mountpoint-extension:0.1.0` |
| Installer image | `docker.io/lyangliang/talos-harvester-csi-mountpoint-installer:v1.13.0-0.1.0` |
| Installer digest | `sha256:e874f6b3e6eb41152718970426ed19ed215a7d72db91728c3a425f8b36b8d639` |

The post-upgrade 1 Gi CSI proof passed provisioning, attach, mount, write,
restart persistence, scale-to-zero, `NodeUnpublishVolume`,
`NodeUnstageVolume`, guest PV deletion, Harvester backend PVC deletion, and
final `VolumeAttachment` cleanup without manual intervention.

Nodes without this extension may hit the same unstage failure if Harvester CSI
workloads run there.

## Problem

Harvester CSI runs `nsenter ... mountpoint <globalmount>` during
`NodeUnstageVolume`. The CSI container had `mountpoint`, but the Talos host
namespace did not. Before the fix, disposable proof PVC cleanup blocked until a
manual `VolumeAttachment` deletion.

This was a Talos host image/tooling issue, not a `slow` StorageClass, reclaim
policy, or pod scheduling issue.

The official `siderolabs/util-linux-tools` extension was checked and rejected
for this specific problem because it did not enable the `mountpoint` binary.

## Source Files

```text
talos/extensions/harvester-csi-mountpoint/
```

The extension uses a static BusyBox binary and exposes:

```text
/usr/bin/mountpoint
```

See `talos/extensions/harvester-csi-mountpoint/README.md` for build and image
details.

## Upgrade Command Used

```bash
talosctl upgrade \
  --nodes 192.168.1.185 \
  --image docker.io/lyangliang/talos-harvester-csi-mountpoint-installer:v1.13.0-0.1.0
```

Expected behavior:

- `data-01` reboots.
- Kubernetes temporarily marks `data-01` NotReady.
- The node returns Ready.
- Talos reports the `harvester-csi-mountpoint` extension.
- The Harvester CSI node pod is recreated on `data-01`.

## Validation

Check the extension:

```bash
talosctl -n 192.168.1.185 get extensions
```

Check the CSI pod on `data-01`:

```bash
kubectl --context homelab-talos -n kube-system get pod -o wide \
  -l app.kubernetes.io/name=harvester-csi-driver
```

Verify `mountpoint` through the host namespace:

```bash
kubectl --context homelab-talos -n kube-system exec <data-01-csi-pod> \
  -c harvester-csi-driver -- \
  sh -c 'nsenter --mount=/proc/1/ns/mnt --net=/proc/1/ns/net --ipc=/proc/1/ns/ipc mountpoint /; echo rc=$?'
```

Required result:

```text
/ is a mountpoint
rc=0
```

Rerun the disposable proof only when approved:

```bash
kubectl --context homelab-talos apply -k kubernetes/clusters/homelab/data-platform/csi-proof
kubectl --context homelab-talos -n data-platform rollout restart deploy/csi-proof
kubectl --context homelab-talos -n data-platform scale deployment/csi-proof --replicas=0
kubectl --context homelab-talos delete -k kubernetes/clusters/homelab/data-platform/csi-proof
kubectl --context homelab-talos get volumeattachment
```

Success means `NodeUnpublishVolume` and `NodeUnstageVolume` both complete, no
manual `VolumeAttachment` deletion is required, and the guest PV plus Harvester
backend PVC are deleted for `Delete` reclaim-policy proof volumes.

## Stop Conditions

- The target node is not `data-01`.
- `data-01` is not Ready before the upgrade.
- Any production workload is using `data-01`.
- Any active production `VolumeAttachment` exists.
- The installer image does not include `harvester-csi-mountpoint`.
- `nsenter ... mountpoint /` does not return `rc=0` after upgrade.
- Proof cleanup still requires manual `VolumeAttachment` deletion.
- Any command would print or store secret values.
