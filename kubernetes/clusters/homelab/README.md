# homelab Kubernetes Cluster

This directory is the desired state for the `homelab-talos` guest Kubernetes cluster.

## Domains

| Directory | Purpose |
| --- | --- |
| `argocd/` | Argo CD projects, root app, and application definitions |
| `platform/` | Shared platform services and policies |
| `apps/` | User-facing and portfolio applications |
| `sandbox/` | Experiments that may break |

## Secret Management

Secret values are not stored in this repository.

The initial GitOps secret pattern is Infisical plus External Secrets Operator.
Start with a narrowly scoped `ClusterSecretStore` for platform bootstrap
secrets, then add namespace-scoped `SecretStore` objects later for app, data,
and sandbox isolation.

See `platform/secrets/README.md`.

## Environment Model

This cluster does not start with separate dev/prod runtime environments. Resource constraints make a single environment more practical.

Testing and safety come from:

- local tests before Git
- CI checks before merge
- manifest validation
- policy/admission guardrails
- Argo CD diff and health checks
- sandbox namespace for risky experiments

Do not create persistent dev/prod copies of databases by default. Use seed datasets, snapshots, or dedicated single-purpose VMs when a workload needs heavier testing.
