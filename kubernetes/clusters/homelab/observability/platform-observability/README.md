# Platform Observability

This directory defines the first guest Kubernetes observability baseline for
`homelab-talos`.

## Decision

- Chart: `victoria-metrics-k8s-stack`
- Chart version: `0.78.0`
- Argo CD application: `platform-observability`
- Namespace: `observability`
- Storage: `VMSingle` uses a 20 Gi `harvester` PVC
- Retention: 14 days
- Exposure: internal services only; no ingress and no Cloudflare route
- Alerting: disabled for the first gate

## Enabled Components

- VictoriaMetrics Operator
- `VMSingle`
- `VMAgent`
- Grafana
- kube-state-metrics
- node-exporter
- Argo CD `VMServiceScrape`
- External Secrets `VMPodScrape`

## Deliberately Excluded

- Harvester `rancher-monitoring`
- Loki
- Tempo
- OpenTelemetry Collector
- external alert routing
- `VMCluster`
- Cloudflare exposure
- ingress exposure
- ClickHouse ingestion

## Boundary

This stack observes the `homelab-talos` guest Kubernetes layer. It does not
replace Harvester `rancher-monitoring` and does not scrape Harvester management
cluster components directly. Harvester CSI visibility comes from guest-layer
Kubernetes object state such as Pods, PVCs, PVs, StorageClasses, and
VolumeAttachments.

## Access

Grafana is internal-only. Use a temporary port-forward when needed:

```sh
kubectl --context homelab-talos -n observability port-forward svc/platform-observability-grafana 3000:80
```

VictoriaMetrics can be queried directly with a temporary port-forward:

```sh
kubectl --context homelab-talos -n observability port-forward svc/vmsingle-platform-observability 8428:8428
```

Do not commit or print Grafana admin credentials.

## Rollback

Remove or disable `kubernetes/clusters/homelab/observability/platform-observability/application.yaml`,
let Argo CD prune the application, then verify:

```sh
kubectl --context homelab-talos get applications -n argocd
kubectl --context homelab-talos get pods -A
kubectl --context homelab-talos top nodes
kubectl --context homelab-talos top pods -A
```

Harvester monitoring should remain unchanged.
