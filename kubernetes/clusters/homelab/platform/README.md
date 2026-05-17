# Platform

Shared cluster services, policies, and infrastructure-style Kubernetes resources.

Current domains:

- `00-namespaces`: base namespaces and Pod Security labels
- `05-kube-vip`: stable internal Kubernetes API VIP
- `10-external-secrets`: External Secrets Operator Helm chart
- `15-metrics-server`: guest cluster Metrics API provider
- `16-kubelet-csr-approver`: constrained kubelet-serving CSR approval for
  Metrics Server TLS hardening
- `20-infisical`: Infisical ClusterSecretStore
- `30-argocd-repo-access`: Argo CD GitHub App repo credential ExternalSecret
- `40-policies`: policy guardrail staging area
- `50-harvester-csi`: Argo CD managed Harvester CSI resources and StorageClass policy
- `55-gateway-api-crds`: Gateway API and Envoy Gateway CRD foundation
- `56-envoy-gateway`: Envoy Gateway controller installation
- `storage`: Kubernetes-side storage policy notes

Platform changes should be reviewed carefully because they can affect every app.

Future platform capabilities such as cert-manager and trust-manager should get
their own numbered capability folder when they have an Argo CD Application or
concrete resources to manage.

Network edge services such as Envoy Gateway entry points, internal DNS routing
policy, external-dns, and any future selected exposure path live under
`../network/`. Observability services such as VictoriaMetrics and Grafana live
under `../observability/`.
