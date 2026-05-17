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

This first gate uses `--kubelet-insecure-tls` so Metrics Server can scrape
Talos kubelets immediately. Replace this later with kubelet serving certificate
approval if Metrics API hardening becomes a priority.
