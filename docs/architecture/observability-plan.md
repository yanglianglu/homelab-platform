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

Proxy endpoints through the Harvester VIP:

```text
Prometheus:
https://192.168.1.50/api/v1/namespaces/cattle-monitoring-system/services/http:rancher-monitoring-prometheus:9090/proxy/

Grafana:
https://192.168.1.50/api/v1/namespaces/cattle-monitoring-system/services/http:rancher-monitoring-grafana:80/proxy/

Alertmanager:
https://192.168.1.50/api/v1/namespaces/cattle-monitoring-system/services/http:rancher-monitoring-alertmanager:9093/proxy/
```

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

1. Review default Harvester alerts without external notifications.
2. Add guest Kubernetes observability with small VictoriaMetrics/Grafana
   resources.
3. Add data-platform dashboards and alerts before ClickHouse ingestion.
4. Decide whether a single Grafana should display both Harvester and guest
   datasources.
