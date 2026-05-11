# Kubernetes Bootstrap

Bootstrap manifests are applied manually before Argo CD manages the rest of the cluster.

Current bootstrap path:

```text
kubernetes/bootstrap/argocd/
kubernetes/bootstrap/external-secrets/
```

Bootstrap should stay small:

1. Install Argo CD.
2. Apply the root Argo CD application.
3. Install External Secrets Operator once so it can generate Argo CD's GitHub
   App repository credential.
4. Let Argo CD manage platform, apps, and sandbox manifests from Git.

Keep bootstrap credentials out of Git. This directory may contain install
manifests and references, but it must not contain generated Argo CD passwords,
kubeconfigs, Talos configs, Infisical client secrets, Cloudflare tokens, or
other live credentials.
