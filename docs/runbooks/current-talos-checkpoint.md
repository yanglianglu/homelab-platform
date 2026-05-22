# Runbook: Current Talos Checkpoint

This checkpoint documents the current Talos state after the VM growth,
Harvester CSI, observability, Metrics Server hardening, and first internal
Gateway API route gates.

## Cluster State

| Item | Value |
| --- | --- |
| Cluster name | `homelab-talos` |
| Control-plane nodes | `cp-01`, `cp-02`, `cp-03` |
| General workers | `worker-01`, `worker-02` |
| Data worker | `data-01` |
| Current Kubernetes API endpoint | `https://192.168.1.184:6443` |
| Talos version | `v1.13.0` |
| Kubernetes version | `v1.36.0` |
| Install disk | `/dev/vda` |
| Pod CIDR | `10.42.0.0/16` |
| Service CIDR | `10.43.0.0/16` |

## Verification Commands

```bash
kubectl --context homelab-talos get nodes -o wide
kubectl --context homelab-talos get pods -A -o wide
talosctl health
```

## Latest Verification

Last checked: 2026-05-18 America/Chicago.

Node readiness:

```text
cp-01       Ready   control-plane   192.168.1.181   Talos v1.13.0   Kubernetes v1.36.0
cp-02       Ready   control-plane   192.168.1.182   Talos v1.13.0   Kubernetes v1.36.0
cp-03       Ready   control-plane   192.168.1.183   Talos v1.13.0   Kubernetes v1.36.0
worker-01   Ready   worker          192.168.1.179   Talos v1.13.0   Kubernetes v1.36.0
worker-02   Ready   worker          192.168.1.180   Talos v1.13.0   Kubernetes v1.36.0
data-01     Ready   data worker     192.168.1.185   Talos v1.13.0   Kubernetes v1.36.0
```

Harvester VM state at this checkpoint:

```text
cp-01 VM Running/Ready on the-abundance, OS disk first
cp-02 VM Running/Ready on the-elation, OS disk first
cp-03 VM Running/Ready on the-enigmata, OS disk first
worker-01 VM Running/Ready on the-elation, OS disk first
worker-02 VM Running/Ready on the-enigmata, OS disk first
data-01 VM Running/Ready on the-abundance, OS disk only
```

Storage compatibility:

```text
Harvester CSI installed in kube-system and managed by Argo CD
CSI controller 3/3 available
CSI node DaemonSet 6/6 available
harvester-csi-mountpoint extension active on all Talos nodes
CSI proof on data-01 passed provisioning, resize, reboot, detach, and cleanup
legacy data-01 rollback PVCs deleted
Metrics Server installed for guest metrics.k8s.io API
Metrics Server validates kubelet serving certificates
kubelet serverTLSBootstrap active on all Talos nodes
platform-kubelet-csr-approver Synced/Healthy in kube-system
six kubelet-serving CSRs Approved,Issued for the expected node identities
```

Kubelet serving certificate proof:

```text
cp-01       system:node:cp-01       DNS:cp-01       IP:192.168.1.181
cp-02       system:node:cp-02       DNS:cp-02       IP:192.168.1.182
cp-03       system:node:cp-03       DNS:cp-03       IP:192.168.1.183
worker-01   system:node:worker-01   DNS:worker-01   IP:192.168.1.179
worker-02   system:node:worker-02   DNS:worker-02   IP:192.168.1.180
data-01     system:node:data-01     DNS:data-01     IP:192.168.1.185
```

Harvester observability:

```text
rancher-monitoring addon enabled in cattle-monitoring-system
AddonDeploySuccessful
Prometheus, Grafana, and Alertmanager proxy health checks passed
external alert notifications not configured
```

Guest Kubernetes observability:

```text
platform-observability Argo CD app Synced/Healthy
VictoriaMetrics K8s Stack chart 0.78.0 installed in observability
VMSingle operational with 20Gi harvester PVC and 14d retention
VMAgent operational and ingesting samples
Grafana Running and internal-only
kube-state-metrics Running
node-exporter Running on all 6 Talos nodes
Argo CD VMServiceScrape operational
External Secrets VMPodScrape operational
CSI visibility provided through kube-state-metrics object state
observability itself has no Gateway route, legacy Ingress, Cloudflare route,
Loki, Tempo, VMCluster, or external alert routing
```

Internal Gateway API route:

```text
platform-kube-vip Synced/Healthy
platform-gateway-api-crds Synced/Healthy
platform-envoy-gateway Synced/Healthy
platform-cert-manager Synced/Healthy
platform-internal-pki Synced/Healthy
platform-trust-manager Synced/Healthy
platform-internal-trust-bundle Synced/Healthy
apps-whoami-tls Synced/Healthy
GatewayClass/envoy-gateway Accepted=True
Gateway/apps/internal-https Programmed=True on 192.168.1.187
HTTPRoute/apps/whoami-tls present for whoami.home.arpa
BackendTLSPolicy/apps/whoami-tls present for verified HTTPS upstream
Certificate/whoami-home-arpa-gateway Ready=True
Certificate/whoami-tls-backend Ready=True
Bundle/homelab-internal-ca Synced=True
admin Mac resolves whoami.home.arpa to 192.168.1.187
normal HTTPS client request returns homelab internal HTTPS backend
```

Workload placement:

```text
apps/whoami runs on worker-01
apps/whoami-tls runs on worker-01
Envoy Gateway data plane for apps/internal-https runs on worker-01
data-01 is tainted data-platform=true:NoSchedule
data-01 only runs required system DaemonSets
External Secrets steady-state values select homelab.local/node-class=general
External Secrets pods run on worker-01 and worker-02 after Argo refresh
Argo CD core workloads select homelab.local/node-class=general
Argo CD core pods run on worker-01 and worker-02
```

Core pod summary, abbreviated:

```text
coredns                         2/2 pods Running
kube-apiserver                  Running on control-plane nodes
kube-controller-manager         Running on control-plane nodes
kube-scheduler                  Running on control-plane nodes
kube-flannel                    Running
kube-proxy                      Running
```

## Expected State

- `cp-01`, `cp-02`, and `cp-03` are `Ready` control-plane nodes.
- `worker-01` and `worker-02` are `Ready` general workers.
- `data-01` is a `Ready` tainted data worker.
- `homelab-talos` kubeconfig uses the kube-vip endpoint `192.168.1.184`.
- All created Talos VMs are pinned to their intended Harvester hosts.
- Argo CD Applications are Synced/Healthy.
- The first internal Gateway route stays internal-only and uses verified HTTPS
  from Gateway to backend.
- Core pods are running:
  - `coredns`
  - `kube-apiserver`
  - `kube-controller-manager`
  - `kube-scheduler`
  - `kube-flannel`
  - `kube-proxy`

## Current Stop Condition

Do not create data-platform local PVs. The storage direction is Harvester CSI
first. `data-01` now sees only `/dev/vda`; the legacy 10 TiB retained-data PVC
and 1 TiB hot-temp PVC have been deleted and removed from desired state.

Next platform gates:

1. Add reviewed NetworkPolicies beyond Argo CD.
2. Clean up the duplicate Envoy Gateway VIP display if a cleaner service-address
   model is available.
3. Run a ClickHouse-specific PVC pilot before large ingestion.
4. Add reviewed, low-noise guest alerts only after dashboard review.
5. Run a controlled Harvester host-maintenance CSI drill only as a separate
   approved operation.
