# Kubernetes Bootstrap

Bootstrap manifests are applied manually before Argo CD manages the rest of the cluster.

Current bootstrap path:

```text
kubernetes/bootstrap/argocd/
```

Bootstrap should stay small:

1. Install Argo CD.
2. Apply the root Argo CD application.
3. Let Argo CD manage platform, apps, and sandbox manifests from Git.
