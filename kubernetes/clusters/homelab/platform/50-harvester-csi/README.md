# Harvester CSI

This directory owns the Argo CD managed Harvester CSI integration for
`homelab-talos`.

## Current State

Harvester CSI was installed manually on 2026-05-16 with chart
`harvester/harvester-csi-driver` `0.1.28`. This directory now promotes the
same integration into GitOps through `Application/platform-harvester-csi`.

| Object | State |
| --- | --- |
| `ClusterSecretStore/infisical-harvester-csi` | Ready |
| `ExternalSecret kube-system/harvester-csi-config` | Synced |
| CSI controller | `3/3` available |
| CSI node DaemonSet | `6/6` available |
| `CSIDriver/driver.harvesterhci.io` | Present |
| Small `data-01` proof | Passed cleanup after Talos mountpoint extension |

The root Argo CD app references `platform/50-harvester-csi/application.yaml`.
After the repo is pushed and Argo CD syncs, the live CSI chart and non-secret
resources should be reconciled from Git instead of a manual Helm release.

## Decisions

| Item | Decision |
| --- | --- |
| Namespace | `kube-system` |
| Secret source | Infisical through External Secrets |
| Infisical project | `homelab-platform-cs-zx` |
| Infisical environment | `prod` |
| Infisical path | `/harvester-csi` |
| Infisical key | `cloud_provider_config` |
| Target Secret | `kube-system/harvester-csi-config` |
| Target Secret key | `cloud-provider-config` |
| Default guest StorageClass | `harvester` |
| Default host StorageClass | `slow` |
| Proof StorageClass | `harvester` |
| Talos mountpoint contract | Universal on all Talos nodes before broad CSI use |

Do not commit the Harvester kubeconfig, service-account token, generated
`cloud-provider-config`, or live Secret YAML.

## StorageClasses

The Helm chart owns the default guest StorageClass named `harvester`. It maps
to host StorageClass `slow` through `values.yaml`:

```yaml
hostStorageClass: slow
```

Normal workload PVCs should use `storageClassName: harvester` or omit
`storageClassName` once the default is confirmed in the cluster.

This directory also owns explicit exception classes:

- `harvester-slow-delete`
- `harvester-slow-retain`
- `harvester-abundance-nvme-delete`

Use the explicit classes only when the manifest needs a non-default reclaim
policy or a host-specific storage tier. `fast-ha` remains approval-gated.

## Validation

Render this directory:

```bash
kubectl kustomize kubernetes/clusters/homelab/platform/50-harvester-csi
```

Safe live checks, when a live validation gate is approved:

```bash
kubectl --context homelab-talos get clustersecretstore infisical-harvester-csi
kubectl --context homelab-talos -n kube-system get externalsecret harvester-csi-config
kubectl --context homelab-talos -n kube-system get secret harvester-csi-config
kubectl --context homelab-talos get storageclass
```

Do not decode or print the generated Secret.
