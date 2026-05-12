# AppProjects

Argo CD AppProjects define deployment guardrails before child Applications run.
They are synced at wave `-10`.

`platform` is intentionally privileged for now because platform components own
cluster-scoped resources such as CRDs, ClusterRoles, and admission webhooks.
Review it carefully before adding new source repos.

`apps` is restricted to the `apps` namespace.

`sandbox` is restricted to the `sandbox` namespace.
