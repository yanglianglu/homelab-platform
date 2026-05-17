# Homelab Repo Organization Plan

This repo uses one monorepo with clear layer ownership.

```text
harvester/  = VM, storage, image, network desired state
talos/      = Talos machine config for VM nodes
kubernetes/ = GitOps workloads inside homelab-talos
docs/       = plans, runbooks, inventory, decisions
```

## Target Layout

```text
harvester/
  images/
  networks/
  storageclasses/
  vms/
    talos/
      control-plane/
      workers/
    data/

talos/
  clusters/
    homelab/
      cluster-vars.yaml
      patches/
      scripts/

kubernetes/
  bootstrap/
  clusters/
    homelab/
      projects/
      platform/
      network/
      observability/
      apps/
      sandbox/

docs/
  architecture/
  inventory/
  runbooks/
  adrs/
```

## Ownership Rules

- `harvester/vms/talos/control-plane/` owns `cp-01`, `cp-02`, and `cp-03` VM desired state.
- `harvester/vms/talos/workers/` owns `worker-01`, `worker-02`, `data-01`, and future workers.
- `harvester/vms/data/` owns rejected standalone data VM history.
- `talos/clusters/homelab/patches/` owns per-node Talos config: hostname, static IP, role, and interface.
- `kubernetes/clusters/homelab/platform/` owns cluster plumbing: namespaces, secrets, policies, cert-manager, trust-manager, and cluster-scoped Gateway API foundations.
- `kubernetes/clusters/homelab/network/` owns internal DNS, Envoy Gateway entry points, Gateway API routing policy, and any future selected exposure path.
- `kubernetes/clusters/homelab/observability/` owns VictoriaMetrics, Grafana, exporters, and alerts.
- `kubernetes/clusters/homelab/apps/` owns normal application workloads.
- `docs/architecture/` owns durable plans like VM capacity, data platform, and service placement.
- `docs/runbooks/` owns exact operational procedures.

## Boundary Rule

If a workload dominates CPU, memory, disk, network, or GPU capacity, model it as a dedicated VM first. Do not force it into the shared Kubernetes worker pool by default.
