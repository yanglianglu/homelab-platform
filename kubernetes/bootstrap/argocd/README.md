# Argo CD Bootstrap

This directory contains the initial Argo CD bootstrap path.

Suggested first install flow:

```bash
kubectl --context homelab-talos create namespace argocd
kubectl --context homelab-talos apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl --context homelab-talos apply -f kubernetes/bootstrap/argocd/root-app/homelab-root-application.yaml
```

Do not run this until the Argo CD install issue starts. FIF-15/FIF-16 only choose the controller and create the repo structure.
