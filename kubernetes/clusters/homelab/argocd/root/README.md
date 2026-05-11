# Root App

The root app manages Argo CD child applications and AppProjects for the homelab cluster.

The active Kustomize build root is the parent directory:

```text
kubernetes/clusters/homelab/argocd/kustomization.yaml
```

Start manually:

```bash
kubectl --context homelab-talos apply -f kubernetes/bootstrap/argocd/root-app/homelab-root-application.yaml
```
