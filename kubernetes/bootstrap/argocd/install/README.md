# Argo CD Install

The first install can use the upstream Argo CD install manifest.

Keep this folder for future pinned install manifests, Kustomize overlays, or Helm values once the bootstrap process is formalized.

Initial command:

```bash
kubectl --context homelab-talos apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Future hardening should pin versions instead of tracking `stable`.
