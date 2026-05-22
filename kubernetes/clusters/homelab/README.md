# homelab Kubernetes Cluster

This directory is the desired state for the `homelab-talos` guest Kubernetes
cluster after bootstrap.

## GitOps Entry Point

The root Argo CD Application points at `kubernetes/clusters/homelab`.

`kustomization.yaml` creates only AppProjects and child Argo CD Applications.
It does not include raw platform resources directly.

```mermaid
flowchart LR
  Root["homelab/"] --> Projects["projects/"]
  Root --> Namespaces["platform/00-namespaces"]
  Root --> KubeVip["platform/05-kube-vip"]
  Root --> ExternalSecrets["platform/10-external-secrets"]
  Root --> Metrics["platform/15-metrics-server"]
  Root --> CSR["platform/16-kubelet-csr-approver"]
  Root --> Infisical["platform/20-infisical"]
  Root --> RepoAccess["platform/30-argocd-repo-access"]
  Root --> Policies["platform/40-policies"]
  Root --> HarvesterCSI["platform/50-harvester-csi"]
  Root --> GatewayCRDs["platform/55-gateway-api-crds"]
  Root --> Envoy["platform/56-envoy-gateway"]
  Root --> CertManager["platform/57-cert-manager"]
  Root --> PKI["platform/58-internal-pki"]
  Root --> TrustManager["platform/59-trust-manager"]
  Root --> TrustBundle["platform/61-internal-trust-bundle"]
  Root --> DataPlatform["data-platform/"]
  Root --> Network["network/"]
  Root --> Observability["observability/"]
  Root --> Apps["apps/"]
```

## Domains

| Directory | Purpose |
| --- | --- |
| `kustomization.yaml` | App-of-apps entry point for this cluster |
| `projects/` | Argo CD AppProject guardrails |
| `platform/` | Shared platform services and policies, organized by capability |
| `network/` | Internal DNS, Gateway API routing, Envoy Gateway entry points, and selected exposure paths |
| `observability/` | VictoriaMetrics, Grafana, exporters, and alerts |
| `data-platform/` | Data-platform storage and future ClickHouse/graph workloads |
| `apps/` | User-facing and portfolio applications |
| `sandbox/` | Experiments that may break |

## Dependency Order

Argo CD sync waves make the bootstrap order explicit:

| Wave | Component |
| --- | --- |
| `-10` | AppProjects |
| `0` | Namespaces |
| `5` | kube-vip API VIP and Service LoadBalancer mode |
| `10` | External Secrets Operator |
| `15` | Metrics Server |
| `16` | kubelet CSR approver |
| `20` | Infisical ClusterSecretStore |
| `30` | Argo CD repository access ExternalSecret |
| `40` | Policies |
| `45` | Harvester CSI and data-platform storage |
| `50` | Plain `whoami` app smoke test |
| `55` | Gateway API CRDs |
| `56` | Envoy Gateway |
| `57` | cert-manager |
| `58` | Internal PKI |
| `59` | trust-manager |
| `60` | Guest observability |
| `61` | Internal trust bundle |
| `70` | Sandbox |
| `80` | First internal HTTPS app route |

`platform/50-harvester-csi` manages Harvester CSI through Argo CD. The guest
`harvester` StorageClass remains the default workload class and maps to
Harvester host StorageClass `slow`.

## Local Validation

Render the cluster root before pushing a GitOps change:

```bash
kubectl kustomize kubernetes/clusters/homelab
```

The root intentionally lives at `kubernetes/clusters/homelab` instead of
`kubernetes/clusters/homelab/root` so Kustomize can keep its default load
restrictions. This avoids requiring a relaxed Argo CD repo-server build option.

## Secret Management

Secret values are not stored in this repository.

The initial GitOps secret pattern is Infisical plus External Secrets Operator.
Start with a narrowly scoped `ClusterSecretStore` for platform bootstrap
secrets, then add namespace-scoped `SecretStore` objects later for app, data,
and sandbox isolation.

See `platform/20-infisical/README.md` and
`platform/30-argocd-repo-access/README.md`.

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
