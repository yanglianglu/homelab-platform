# CSI Proof

This directory contains a small Harvester CSI drill workload. It is intentionally
kept as an operator-run proof instead of a continuously reconciled Argo CD app.

The proof validates:

- PVC provisioning through the default guest StorageClass `harvester`
- pod scheduling on `data-01`
- write/read persistence across pod restart
- backend cleanup through `Delete` reclaim policy

## Latest Result

After the repo-local `harvester-csi-mountpoint` Talos extension was added to
`data-01`, the 1 Gi proof passed write, restart persistence, scale-to-zero,
`NodeUnstageVolume`, guest PV deletion, Harvester backend PVC deletion, and
final `VolumeAttachment` cleanup without manual intervention.

Treat this as a passed small proof, not as production ClickHouse approval.
Larger reboot, maintenance, expansion, and performance drills are still
required before using CSI for large ClickHouse data or detaching the legacy
`data-01` disks.

Do not run this proof until Harvester CSI is installed, Argo CD ownership is
clear, and the Talos mountpoint extension is present on the target node.

## Expected Flow

```bash
kubectl --context homelab-talos apply -k kubernetes/clusters/homelab/data-platform/csi-proof
kubectl --context homelab-talos -n data-platform get pvc,pod -o wide
kubectl --context homelab-talos -n data-platform logs deploy/csi-proof
kubectl --context homelab-talos -n data-platform rollout restart deploy/csi-proof
kubectl --context homelab-talos -n data-platform patch pvc csi-proof-harvester-default --type merge -p '{"spec":{"resources":{"requests":{"storage":"2Gi"}}}}'
kubectl --context homelab-talos -n data-platform scale deployment/csi-proof --replicas=0
kubectl --context homelab-talos delete -k kubernetes/clusters/homelab/data-platform/csi-proof
```

Confirm the pod runs on `data-01` and that the test PVC binds to
`harvester`.
