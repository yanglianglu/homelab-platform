# External Secrets Bootstrap

External Secrets Operator is bootstrapped manually before Argo CD can read the
private GitHub repository.

Apply the Kustomize wrapper instead of applying the upstream release manifest
directly. The upstream manifest contains namespaced resources in `default`; the
wrapper rewrites those resources into `external-secrets`, patches webhook
certificate arguments that otherwise still refer to `default`, and adds a
temporary control-plane toleration because this cluster currently has only
`cp-01` as a schedulable Kubernetes node.

```bash
kubectl --context homelab-talos apply --server-side -k kubernetes/bootstrap/external-secrets/install
```

After Argo CD can read the repo, the ongoing desired state is represented by:

```text
kubernetes/clusters/homelab/argocd/applications/platform/external-secrets.yaml
```
