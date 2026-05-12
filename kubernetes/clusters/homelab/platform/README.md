# Platform

Shared cluster services, policies, and infrastructure-style Kubernetes resources.

Current domains:

- `00-namespaces`: base namespaces and Pod Security labels
- `10-external-secrets`: External Secrets Operator Helm chart
- `20-infisical`: Infisical ClusterSecretStore
- `30-argocd-repo-access`: Argo CD GitHub App repo credential ExternalSecret
- `40-policies`: policy guardrail staging area
- `storage`: Kubernetes-side storage policy notes

Platform changes should be reviewed carefully because they can affect every app.

Future platform capabilities such as ingress, cert-manager, external-dns, and
observability should get their own numbered capability folder when they have an
Argo CD Application or concrete resources to manage.
