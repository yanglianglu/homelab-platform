# Runbook: macOS Kubeconfig Setup

Use local kubeconfig files instead of committing credentials to this repository.

For daily work, prefer a merged kubeconfig with named contexts:

| Cluster | Context |
| --- | --- |
| Harvester management cluster | `harvester` |
| Guest Talos Kubernetes cluster | `homelab-talos` |

## Current Local Convention

Store the Harvester kubeconfig at:

```bash
~/.kube/harvester.yaml
```

Keep it private:

```bash
chmod 600 ~/.kube/harvester.yaml
```

The kubeconfig cluster endpoint should use the Harvester VIP and Rancher proxy path:

```bash
kubectl --kubeconfig ~/.kube/harvester.yaml \
  config set-cluster local \
  --server=https://192.168.1.50/k8s/clusters/local
```

## Shell Alias

Add this alias to `~/.zprofile`:

```bash
alias kh="KUBECONFIG=$HOME/.kube/harvester.yaml kubectl"
```

Reload the shell profile:

```bash
source ~/.zprofile
```

Use `kh` for Harvester cluster commands:

```bash
kh get nodes -o wide
kh get pods -A
```

This keeps Harvester access explicit. For normal daily use, the current convention is also to merge source kubeconfigs into:

```bash
~/.kube/config
```

and switch contexts with:

```bash
kubectl config use-context harvester
kubectl config use-context homelab-talos
```

See `docs/runbooks/kube-context-switching.md` for the current context-switching workflow and guest-cluster blocker.
