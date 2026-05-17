# Harvester CSI Mountpoint Extension

Minimal Talos system extension used to fix Harvester CSI `NodeUnstageVolume`
cleanup on Talos nodes.

## Purpose

Harvester CSI runs `nsenter ... mountpoint <globalmount>` during unstage. The
CSI container had `mountpoint`, but the Talos host namespace did not. This
extension adds a static BusyBox binary and exposes:

```text
/usr/bin/mountpoint
```

The stock `siderolabs/util-linux-tools` extension was checked first and did not
provide the needed `mountpoint` binary.

## Images

| Image | Digest |
| --- | --- |
| `lyangliang/harvester-csi-mountpoint-extension:0.1.0` | `sha256:5067fed7a1a6bd17b9a71ad42446d33073cbcb530b5b13b7c53c58f3ed7af572` |
| `lyangliang/talos-harvester-csi-mountpoint-installer:v1.13.0-0.1.0` | `sha256:e874f6b3e6eb41152718970426ed19ed215a7d72db91728c3a425f8b36b8d639` |

## Build

```bash
docker build \
  --platform linux/amd64 \
  -t harvester-csi-mountpoint-extension:0.1.0 \
  talos/extensions/harvester-csi-mountpoint

docker run --rm \
  --platform linux/amd64 \
  --entrypoint /rootfs/usr/bin/mountpoint \
  harvester-csi-mountpoint-extension:0.1.0 /
```

Expected output:

```text
/ is a mountpoint
```

Build the Talos installer with the pushed extension image:

```bash
docker run --rm -t \
  -v "$PWD/_out:/out" \
  ghcr.io/siderolabs/imager:v1.13.0 \
  installer \
  --arch amd64 \
  --system-extension-image lyangliang/harvester-csi-mountpoint-extension:0.1.0
```

## Live Validation

`data-01` was the first node upgraded with:

```text
docker.io/lyangliang/talos-harvester-csi-mountpoint-installer:v1.13.0-0.1.0
```

The CSI node pod on `data-01` now returns:

```text
nsenter --mount=/proc/1/ns/mnt --net=/proc/1/ns/net --ipc=/proc/1/ns/ipc mountpoint /
/ is a mountpoint
rc=0
```

A post-upgrade 1 Gi Harvester CSI proof passed attach, write, restart
persistence, scale-to-zero, `NodeUnstageVolume`, guest PV deletion, Harvester
backend PVC deletion, and final `VolumeAttachment` cleanup without manual
intervention.

The platform contract is now universal: roll this installer to every Talos node
before broad CSI-backed workload scheduling.
