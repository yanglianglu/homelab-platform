# Platform

Shared cluster services, policies, and infrastructure-style Kubernetes resources.

Current domains:

- `00-namespaces`: base namespaces and Pod Security labels
- `10-external-secrets`: External Secrets Operator Helm chart
- `20-infisical`: Infisical ClusterSecretStore
- `30-argocd-repo-access`: Argo CD GitHub App repo credential ExternalSecret
- `40-policies`: policy placeholder
- `storage`
- `ingress`
- `cert-manager`
- `external-dns`
- `observability`

Platform changes should be reviewed carefully because they can affect every app.
