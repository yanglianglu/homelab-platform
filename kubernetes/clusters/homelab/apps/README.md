# Applications

User-facing and portfolio application manifests live here.

Use one folder per app:

```text
apps/
  app-name/
    README.md
    app/
    config/
    storage/
    secrets/
```

Do not create dev/prod splits by default. Use branch checks, local tests, policy guardrails, Argo CD diff/sync, and sandbox deployments.

Heavy streaming, data warehouse, and AI workloads should run as dedicated single-purpose VMs under `harvester/`, not as oversized shared Kubernetes workloads.
