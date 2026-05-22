# Applications

User-facing and portfolio application manifests live here.

Create one folder per app only when there is real deployable content or a
near-term implementation issue. Avoid placeholder-only app folders.

Expected app folder shape:

```text
apps/
  app-name/
    README.md
    app/
    config/
    storage/
    external-secrets/
```

Do not create dev/prod splits by default. Use branch checks, local tests, policy
guardrails, Argo CD diff/sync, and sandbox deployments.

Planned application ideas stay in Linear, user-maintained Notion, or local
planning notes until they are ready for GitOps manifests. Current candidates
include the portfolio app, data lake control plane, chat-with-data, and
analytics demos. Codex should not write planning notes to Notion.

Heavy streaming, data warehouse, and AI workloads should run as dedicated
single-purpose VMs under `harvester/`, not as oversized shared Kubernetes
workloads.
