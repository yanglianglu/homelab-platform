# Metrics Server

Metrics Server provides the guest cluster `metrics.k8s.io/v1beta1` API used by
`kubectl top` and lightweight autoscaling inputs.

Steady-state install:

- Argo CD Application: `application.yaml`
- Helm values: `values.yaml`
- Chart repo: `https://kubernetes-sigs.github.io/metrics-server/`
- Chart version: `3.13.0`
- Namespace: `kube-system`

Placement:

- Runs on general workers through `homelab.local/node-class=general`.
- Does not run on control-plane nodes or the tainted `data-01` data worker.

Talos TLS note:

Metrics Server validates kubelet serving certificates instead of skipping TLS
verification. Talos kubelet serving certificate bootstrap is enabled on all six
nodes, and kubelet-serving CSRs are approved only by the constrained
`platform-kubelet-csr-approver` Application.

Allowed kubelet-serving identity:

- Signer: `kubernetes.io/kubelet-serving`
- Nodes: `cp-01`, `cp-02`, `cp-03`, `worker-01`, `worker-02`, `data-01`
- LAN range: `192.168.1.0/24`
- CSR username/common name: `system:node:<node-name>`

Verification:

```bash
kubectl --context homelab-talos get csr -o wide
kubectl --context homelab-talos get apiservice v1beta1.metrics.k8s.io
kubectl --context homelab-talos top nodes
kubectl --context homelab-talos top pods -A
kubectl --context homelab-talos -n kube-system get deploy metrics-server -o yaml
```

Rollback if Metrics Server cannot validate kubelet certificates:

1. Re-add `--kubelet-insecure-tls` to `values.yaml`.
2. Commit and push the rollback.
3. Let Argo CD reconcile `platform-metrics-server`.
4. Inspect kubelet-serving CSRs and Metrics Server logs before retrying.
