# Argo CD Bootstrap

This directory contains the initial Argo CD bootstrap path.

## Decision

Argo CD is installed once by hand, then the root Application lets Argo CD
reconcile the cluster's GitOps desired state from this repository.

The install is a Kustomize wrapper around the upstream Argo CD manifests pinned
to `v3.4.1`. Do not use the floating `stable` URL for this cluster.

Initial access is local-only through `kubectl port-forward`. Do not expose Argo
CD through ingress or Cloudflare Tunnel until auth, TLS, and secret management
are ready.

## First Install Flow

```bash
kubectl --context homelab-talos apply --server-side --force-conflicts -k kubernetes/bootstrap/argocd/install
kubectl --context homelab-talos -n argocd rollout status deployment/argocd-server
kubectl --context homelab-talos apply -f kubernetes/bootstrap/argocd/root/homelab-root-application.yaml
```

If the GitHub repository is private, Argo CD will not be able to compare or sync
the root app until a repository credential is added in the `argocd` namespace.
The selected credential method is GitHub App authentication through
`homelab-yanglianglu`, materialized as an Argo CD `repo-creds` Secret by
External Secrets Operator from Infisical Cloud.

Do not commit that credential to Git. The Infisical Universal Auth bootstrap
Secret is the only manual secret-zero item for this flow.

## Access

Use port-forward for the first login:

```bash
kubectl --context homelab-talos -n argocd port-forward svc/argocd-server 8080:443
```

Then open `https://localhost:8080`.

Do not commit the generated initial admin password or any future Argo CD
credentials. If credentials need to be preserved, put them in the approved
secret manager or ask for a manual decision.
