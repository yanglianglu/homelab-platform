# Kubernetes Layer

Kubernetes manifests live here after the Talos cluster exists and the Kubernetes API is reachable.

This repository uses Argo CD as the GitOps controller for the `homelab-talos` guest cluster.

## Boundaries

- `talos/` owns node bootstrap and machine configuration.
- `harvester/` owns VM, network, image, and Harvester-side storage definitions.
- `kubernetes/` owns workloads, platform services, application manifests, and cluster policies.
- Do not commit plaintext secrets, kubeconfigs, private keys, or app credentials.
- Secret values live outside Git. The selected pattern is Infisical plus
  External Secrets Operator; see
  `kubernetes/clusters/homelab/platform/20-infisical/README.md` and
  `kubernetes/clusters/homelab/platform/30-argocd-repo-access/README.md`.

## Deployment Model

The homelab uses one runtime environment first, not a dev/prod split.

Guardrails happen before and during deploy:

- local app tests
- manifest rendering and validation
- security and policy checks
- Git PR review
- Argo CD diff/sync/health
- resource requests, limits, probes, and rollback paths

Use `sandbox/` for experiments. Use dedicated single-purpose VMs for heavy streaming, data warehouse, and AI workloads instead of forcing the shared Kubernetes worker pool to carry them.

## Layout

```text
kubernetes/
  bootstrap/
    argocd/
  clusters/
    homelab/
      kustomization.yaml
      root/
      projects/
      platform/
      apps/
      sandbox/
```

See `kubernetes/clusters/homelab/README.md` for cluster-specific conventions.
