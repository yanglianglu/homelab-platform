# External Secrets Operator

This component installs External Secrets Operator in the `external-secrets`
namespace at sync wave `10`.

External Secrets Operator is the Kubernetes controller that reads secret values
from external backends and materializes normal Kubernetes Secrets. It does not
store secret values in Git.

Steady-state install:

- Argo CD Application: `application.yaml`
- Helm values: `values.yaml`
- Chart repo: `https://charts.external-secrets.io`
- Chart version: `2.4.1`

The Application uses `ServerSideApply=true` because External Secrets Operator
CRDs are large enough to hit the Kubernetes client-side apply annotation limit.

Current cluster note: the values include control-plane tolerations because the
cluster initially has only `cp-01` as a schedulable Kubernetes node. Revisit this
after worker nodes are created.

Bootstrap note: `kubernetes/bootstrap/external-secrets/install` is manual and
break-glass only after Argo CD can read the repo. The Argo CD Application here is
the steady-state owner.

Do not put Infisical client IDs, client secrets, GitHub App private keys, or
generated Kubernetes Secrets in this directory.
