# Observability Plan

This plan defines the boundary between Harvester-level monitoring and guest
Kubernetes observability.

## Current State

Harvester `rancher-monitoring` is enabled in the Harvester management cluster.

| Item | Value |
| --- | --- |
| Enabled date | 2026-05-16 America/Chicago |
| Addon | `cattle-monitoring-system/rancher-monitoring` |
| Addon status | `AddonDeploySuccessful` |
| Prometheus | `rancher-monitoring-prometheus`, `1/1` ready |
| Grafana | `rancher-monitoring-grafana`, running |
| Alertmanager | `rancher-monitoring-alertmanager`, `1/1` ready |
| Prometheus retention | `5d` / `50GiB` |
| Prometheus PVC | `50Gi` on `harvester-longhorn` |
| Alertmanager PVC | `5Gi` on `harvester-longhorn` |
| Grafana PVC | `2Gi` on `harvester-longhorn` |
| External notifications | Not configured |
| Acceptance status | Confirmed operational on 2026-05-17 America/Chicago |

Proxy endpoints through the Harvester VIP:

```text
Prometheus:
https://192.168.1.50/api/v1/namespaces/cattle-monitoring-system/services/http:rancher-monitoring-prometheus:9090/proxy/

Grafana:
https://192.168.1.50/api/v1/namespaces/cattle-monitoring-system/services/http:rancher-monitoring-grafana:80/proxy/

Alertmanager:
https://192.168.1.50/api/v1/namespaces/cattle-monitoring-system/services/http:rancher-monitoring-alertmanager:9093/proxy/
```

Guest Kubernetes observability is enabled inside `homelab-talos`.

This is the first guest-cluster observability baseline. It is not the final
observability architecture.

| Item | Value |
| --- | --- |
| Enabled date | 2026-05-17 America/Chicago |
| Argo CD application | `platform-observability` |
| Namespace | `observability` |
| Chart | `victoria-metrics-k8s-stack` `0.78.0` |
| VictoriaMetrics app version | `v1.143.0` |
| Storage | `VMSingle` 20 Gi PVC on guest StorageClass `harvester` |
| Retention | `14d` |
| Grafana exposure | ClusterIP only; no ingress and no Cloudflare route |
| Alerting | Disabled/deferred |
| Logs/traces | Not installed |
| Harvester scraping | Not configured |
| Acceptance status | Confirmed operational on 2026-05-17 America/Chicago |

Enabled guest components:

- VictoriaMetrics Operator
- `VMSingle`
- `VMAgent`
- Grafana
- kube-state-metrics
- node-exporter
- Argo CD `VMServiceScrape`
- External Secrets `VMPodScrape`

Direct Harvester CSI metrics are not exposed by the current guest CSI
deployment. CSI visibility comes from guest Kubernetes object state:

- Harvester CSI pod status in `kube-system`
- PVC and PV phase
- StorageClass inventory
- VolumeAttachment state
- pod scheduling and restart state

Internal access:

```bash
kubectl --context homelab-talos -n observability port-forward svc/platform-observability-grafana 3000:80
kubectl --context homelab-talos -n observability port-forward svc/vmsingle-platform-observability-victoria-metrics-k8s-stack 8428:8428
```

Rollback:

1. Remove or disable `platform-observability` from Git.
2. Let Argo CD prune the application.
3. Confirm `kubectl --context homelab-talos get pods -A` remains healthy.
4. Confirm Metrics Server still answers `kubectl --context homelab-talos top nodes`.
5. Confirm Harvester `rancher-monitoring` remains unchanged.

Implementation note: the `observability` namespace enforces privileged Pod
Security because node-exporter requires host network, host PID, and hostPath
access. This privilege is scoped to the guest observability namespace and does
not grant public exposure.

## Ownership Boundary

Harvester monitoring owns infrastructure visibility:

- Harvester physical nodes
- Harvester management Kubernetes components
- Longhorn volumes
- KubeVirt and VM state
- VM CPU, memory, disk, and migration metrics
- Harvester system alerts

Guest Kubernetes observability owns workload visibility inside `homelab-talos`:

- Talos node readiness from the guest point of view
- pods, deployments, StatefulSets, and namespaces
- Argo CD
- External Secrets
- Harvester CSI pods inside the guest cluster
- ClickHouse and future data-platform workloads
- application metrics and dashboards

Do not merge collection at the beginning. Keep Harvester and guest collectors
separate for failure isolation. A future Grafana can add the other layer as a
read-only datasource if that improves navigation.

## Operating Rules

- Use Harvester monitoring first when debugging physical hosts, VM state,
  Longhorn, or Harvester-managed volumes.
- Use guest observability first when debugging pods, namespaces, Argo CD,
  External Secrets, app workloads, or ClickHouse.
- Do not route alerts externally until default alerts have been reviewed and
  noisy alerts have been tuned.
- Do not treat Harvester monitoring as a replacement for guest Kubernetes
  observability.

## Next Gates

1. Review the first guest dashboards and query set after real scrape volume is
   visible.
2. Add data-platform dashboards and reviewed alerts before ClickHouse ingestion.
3. Run the ClickHouse CSI PVC pilot only after observability remains stable.
4. Decide whether a single Grafana should display both Harvester and guest
   datasources.

Deferred by operator decision on 2026-05-17:

- Minimal alert routing and notification tuning.
- Harvester `rancher-logging`.
