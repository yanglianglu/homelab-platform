# Runbook: Harvester CSI Attachment Debugging

Use this runbook when a Harvester CSI PVC does not bind, attach, mount, detach,
or clean up as expected. Do not decode or print Secret values.

## Current Known State

The small default `harvester` proof now passes on `data-01` after the
`harvester-csi-mountpoint` Talos extension. The historical failure was
`NodeUnstageVolume` calling `mountpoint` through `nsenter` when the Talos host
namespace did not have that command.

The mountpoint extension is now the universal Talos node contract. If a
CSI-backed workload lands on a node, verify that node has the extension before
trusting detach cleanup.

## Guest Cluster Checks

```bash
kubectl --context homelab-talos get storageclass
kubectl --context homelab-talos get csidriver
kubectl --context homelab-talos -n kube-system get pods -o wide | rg 'harvester|csi'
kubectl --context homelab-talos get clustersecretstore infisical-harvester-csi
kubectl --context homelab-talos -n kube-system get externalsecret harvester-csi-config
kubectl --context homelab-talos -n kube-system get secret harvester-csi-config
```

Inspect workload placement and attachment state:

```bash
kubectl --context homelab-talos -n data-platform get pvc,pod -o wide
kubectl --context homelab-talos -n data-platform describe pvc csi-proof-harvester-default
kubectl --context homelab-talos -n data-platform describe pod -l app.kubernetes.io/name=csi-proof
kubectl --context homelab-talos get volumeattachment
```

## Harvester Host Checks

Use the Harvester kubeconfig and inspect metadata only:

```bash
kubectl --kubeconfig ~/.kube/harvester.yaml get storageclass slow the-abundance-nvme fast-ha
kubectl --kubeconfig ~/.kube/harvester.yaml -n talos-cluster get vm data-01
kubectl --kubeconfig ~/.kube/harvester.yaml get pv,pvc -A | rg 'pvc|data-platform|harvester'
```

For stuck volumes, inspect Longhorn attachment state without changing it:

```bash
kubectl --kubeconfig ~/.kube/harvester.yaml -n longhorn-system get volumes.longhorn.io
kubectl --kubeconfig ~/.kube/harvester.yaml -n longhorn-system get volumeattachments.longhorn.io
```

## Failure Map

| Symptom | Check |
| --- | --- |
| PVC stays Pending | StorageClass name, CSI provisioner pod, Harvester credential |
| Pod stays ContainerCreating | `VolumeAttachment` and CSI node pod on the target node |
| Volume attaches to wrong VM | Pod node placement and guest node name to Harvester VM mapping |
| Delete does not clean up | Reclaim policy, finalizers, CSI node logs |
| `NodeUnstageVolume` reports `mountpoint` not found | Target Talos node lacks the mountpoint extension |
| CSI pod missing on `data-01` | DaemonSet toleration for `data-platform=true:NoSchedule` |

## Emergency Cleanup

Manual `VolumeAttachment` deletion is only for disposable proof volumes, not
production data.

```bash
kubectl --context homelab-talos -n data-platform get pvc,pod
kubectl --context homelab-talos -n data-platform scale deployment/csi-proof --replicas=0
kubectl --context homelab-talos get pv <proof-pv-name>
kubectl --context homelab-talos describe volumeattachment <proof-volumeattachment-name>
kubectl --context homelab-talos delete volumeattachment <proof-volumeattachment-name> --wait=true --timeout=120s
kubectl --context homelab-talos wait --for=delete pv/<proof-pv-name> --timeout=180s
```

Only run this after confirming the attachment belongs to a disposable proof PVC
and the workload using it has already been removed.

## Stop Conditions

- Secret data would need to be printed.
- A proof PVC hot-plugs to the wrong VM.
- PVC reclaim behavior differs from the StorageClass policy.
- Longhorn attachment state is unclear after a normal pod restart.
- Delete cleanup requires manual attachment intervention after the extension
  fix.
- `NodeUnstageVolume` cannot execute `mountpoint` on the target Talos node.
