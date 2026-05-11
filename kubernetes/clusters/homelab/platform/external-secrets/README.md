# External Secrets Operator

External Secrets Operator runs in the `external-secrets` namespace and creates
Kubernetes Secrets from external secret backends.

The long-term GitOps install is represented by the Argo CD Application:

```text
kubernetes/clusters/homelab/argocd/applications/platform/external-secrets.yaml
```

That Application uses the upstream Helm chart from:

```text
https://charts.external-secrets.io
```

Pinned chart version:

```text
2.4.1
```

Because Argo CD cannot read the private GitHub repository until its repository
credential exists, the first install is applied manually through the bootstrap
Kustomize wrapper:

```bash
kubectl --context homelab-talos apply --server-side -k kubernetes/bootstrap/external-secrets/install
```

Do not apply the upstream release manifest directly with `-n external-secrets`.
The upstream manifest contains namespaced resources in `default`; the Kustomize
wrapper rewrites them into `external-secrets`.

Current cluster note: this install tolerates the control-plane taint because the
cluster currently has only `cp-01` as a schedulable Kubernetes node. Revisit this
after worker nodes are created.

This manual install is a bootstrap step. After Argo CD can read the repo, Argo CD
should own the ongoing External Secrets Operator Application.

Do not put Infisical client IDs, client secrets, GitHub App private keys, or
generated Kubernetes Secrets in this directory.
