# Kubernetes Bootstrap

Bootstrap is the temporary handoff layer used before GitOps can manage the
cluster itself.

Use this directory only for first install and recovery:

1. Install Argo CD from `bootstrap/argocd/install`.
2. Apply the root Application from `bootstrap/argocd/root`.
3. If Argo CD cannot yet read the private GitHub repo, install External Secrets
   Operator once from `bootstrap/external-secrets/install`.
4. Let Argo CD reconcile `kubernetes/clusters/homelab`.

Steady-state ownership moves to Argo CD child Applications under
`kubernetes/clusters/homelab/platform/*`. Do not keep manually applying
bootstrap External Secrets Operator after Argo CD owns the
`platform-external-secrets` Application unless recovering the cluster.

Keep bootstrap credentials out of Git. This directory may contain install
manifests and references, but it must not contain generated Argo CD passwords,
kubeconfigs, Talos configs, Infisical client secrets, Cloudflare tokens, or
other live credentials.
