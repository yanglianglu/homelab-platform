# External Secrets Bootstrap

External Secrets Operator is bootstrapped manually before Argo CD can read the
private GitHub repository.

Apply the Kustomize wrapper instead of applying the upstream release manifest
directly. The upstream manifest contains namespaced resources in `default`; the
wrapper rewrites those resources into `external-secrets` and patches webhook
certificate arguments that otherwise still refer to `default`.

The original bootstrap wrapper carried a temporary control-plane toleration for
the early single-node phase. The current steady-state cluster has general worker
nodes, and the Argo CD-managed External Secrets installation runs on worker
capacity.

```bash
kubectl --context homelab-talos apply --server-side -k kubernetes/bootstrap/external-secrets/install
```

After Argo CD can read the repo, the ongoing desired state is represented by:

```text
kubernetes/clusters/homelab/platform/10-external-secrets/application.yaml
```

The bootstrap path uses the raw upstream `v2.4.1` release manifest. The Argo
CD-managed steady-state path uses the Helm chart version `2.4.1` and
`values.yaml`. If they temporarily differ during recovery, the Argo CD
Application is the source of truth after repo access works.
