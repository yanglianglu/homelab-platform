# Platform Observability Query Reference

Use these queries against VictoriaMetrics after `platform-observability` is
Synced and Healthy.

| Area | Query | Proves |
| --- | --- | --- |
| Scrape health | `up` | VMAgent is scraping targets. |
| Nodes | `kube_node_status_condition{condition="Ready"}` | Guest Kubernetes node readiness is visible. |
| Node CPU | `rate(node_cpu_seconds_total[5m])` | node-exporter is publishing node CPU counters. |
| Node filesystem | `node_filesystem_avail_bytes` | node-exporter is publishing filesystem capacity. |
| Pods | `kube_pod_status_phase` | Pod phase by namespace is visible. |
| Deployments | `kube_deployment_status_replicas_available` | Deployment availability is visible. |
| PVCs | `kube_persistentvolumeclaim_status_phase` | PVC phase by namespace is visible. |
| PVs | `kube_persistentvolume_status_phase` | PV state is visible. |
| StorageClasses | `kube_storageclass_info` | Guest StorageClass inventory is visible. |
| VolumeAttachment | `kube_volumeattachment_status_attached` | CSI attachment state is visible when VolumeAttachments exist. |
| Argo CD | `argocd_app_info` | Argo CD app inventory is visible. |
| Argo CD sync | `argocd_app_sync_total` | Argo CD sync activity is visible if exposed by the controller. |
| External Secrets | `externalsecret_status_condition` | ExternalSecret object status is visible when emitted by the controller. |
| External Secrets scrape | `up{namespace="external-secrets"}` | External Secrets metrics endpoints are scraped. |
| Harvester CSI pods | `kube_pod_status_phase{namespace="kube-system",pod=~"harvester-csi-driver.*"}` | CSI pod state is visible through kube-state-metrics. |
| CSI restarts | `kube_pod_container_status_restarts_total{namespace="kube-system",pod=~"harvester-csi-driver.*"}` | CSI container restart count is visible. |
| data-platform | `kube_pod_status_phase{namespace="data-platform"}` | The data-platform namespace can be filtered. |

Some metric names depend on the controller version and scrape endpoint behavior.
If a direct controller metric is missing, use kube-state-metrics object state as
the baseline signal before adding another scrape endpoint.
