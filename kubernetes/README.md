# Kubernetes Layer

Kubernetes manifests live here after the Talos cluster exists and the Kubernetes API is reachable.

Use this layer for:

- Namespaces
- Ingress
- Storage and CSI resources
- Monitoring
- PostgreSQL
- Demo and future applications

Do not put application manifests under `talos/`. Talos owns node bootstrap; Kubernetes owns workloads.

## Current Next Steps

1. Create a demo namespace.
2. Deploy a test workload.
3. Later add PostgreSQL.
4. Later add metrics-server, ingress, cert-manager, and monitoring.
