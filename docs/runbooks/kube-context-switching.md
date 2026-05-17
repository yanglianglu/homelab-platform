# Runbook: Kubernetes Context Switching

Use a merged daily kubeconfig for normal command-line work, while keeping source kubeconfig files separate.

## Context Names

| Cluster | Context name | Source kubeconfig | Status |
| --- | --- | --- | --- |
| Harvester management cluster | `harvester` | `~/.kube/harvester.yaml` | configured |
| Guest Talos Kubernetes | `homelab-talos` | `~/.kube/homelab-talos.yaml` | configured |

## Daily Commands

Show contexts:

```bash
kubectl config get-contexts
```

Switch to Harvester:

```bash
kubectl config use-context harvester
kubectl get nodes -o wide
```

Switch to the guest Talos cluster:

```bash
kubectl config use-context homelab-talos
kubectl get nodes -o wide
```

## Current State

`~/.kube/config` contains both the Harvester management context and the guest Talos Kubernetes context.

Verified:

```bash
kubectl get nodes -o wide
```

returns the Harvester nodes:

- `the-abundance`
- `the-elation`
- `the-enigmata`

## Guest Cluster Access

The normal Kubernetes API endpoint is the kube-vip address
`https://192.168.1.184:6443`. Individual control-plane node IPs remain
break-glass endpoints. The default Talos config is installed at:

```text
~/.talos/config
```

The guest kubeconfig is installed at:

```text
~/.kube/homelab-talos.yaml
```

To refresh the guest kubeconfig from Talos:

```bash
talosctl --talosconfig ~/.talos/config kubeconfig ~/.kube/homelab-talos.yaml
```

After that, merge the context:

```bash
KUBECONFIG=$HOME/.kube/config:$HOME/.kube/homelab-talos.yaml kubectl config view --flatten > /tmp/kubeconfig-merged
mv /tmp/kubeconfig-merged $HOME/.kube/config
chmod 600 $HOME/.kube/config
kubectl config rename-context admin@homelab-talos homelab-talos
```

Do not commit kubeconfig, Talos config, or generated secrets to Git.
