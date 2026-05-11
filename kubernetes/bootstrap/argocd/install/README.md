# Argo CD Install

This folder contains the one-time Argo CD controller install for the
`homelab-talos` cluster.

The install uses Kustomize to wrap the official upstream Argo CD install
manifest pinned to `v3.4.1`.

Because the current cluster has only one schedulable Kubernetes node and that
node is the Talos control plane, the install adds a control-plane toleration to
Argo CD Deployments and StatefulSets. Revisit this after worker nodes exist.

Apply it with server-side apply because recent Argo CD CRDs can exceed the
client-side apply annotation limit.

```bash
kubectl --context homelab-talos apply --server-side --force-conflicts -k kubernetes/bootstrap/argocd/install
```

Keep this install local-only at first. Use port-forward for UI access and defer
ingress, Cloudflare Tunnel, TLS, and identity-aware access until the security
baseline is ready.

Current cluster note: this install tolerates the control-plane taint because the
cluster currently has only `cp-01` as a schedulable Kubernetes node. Revisit this
after worker nodes are created.
