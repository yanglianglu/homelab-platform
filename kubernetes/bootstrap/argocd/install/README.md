# Argo CD Install

This folder contains the one-time Argo CD controller install for the
`homelab-talos` cluster.

The install uses Kustomize to wrap the official upstream Argo CD install
manifest pinned to `v3.4.1`.

Argo CD core workloads use `homelab.local/node-class=general` node selectors so
they run on general workers instead of control-plane nodes or the tainted
`data-01` data worker.

Apply it with server-side apply because recent Argo CD CRDs can exceed the
client-side apply annotation limit.

```bash
kubectl --context homelab-talos apply --server-side --force-conflicts -k kubernetes/bootstrap/argocd/install
```

Keep this install local-only at first. Use port-forward for UI access and defer
Gateway API exposure, legacy Ingress, Cloudflare Tunnel, TLS, and
identity-aware access until the security baseline is ready.

Current cluster note: old control-plane tolerations may remain in live
Deployment and StatefulSet templates because the bootstrap install originally ran
on a single control-plane node. The general-worker node selector is the effective
steady-state placement contract.
