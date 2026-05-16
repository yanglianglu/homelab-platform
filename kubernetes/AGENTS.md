# Kubernetes Operating Guide

## Scope

This directory owns GitOps resources applied after the Talos Kubernetes API exists: Argo CD, AppProjects, Applications, namespaces, policies, platform services, network services, observability, applications, and sandbox workloads.

## GitOps ownership

- Keep Kubernetes desired state in Git and let Argo CD reconcile it.
- Do not make live-only changes unless the user approves an emergency repair gate.
- If a live repair is required, backfill Git before treating the system as fixed.
- Keep bootstrap resources separate from steady-state cluster resources.

## Validation rules

- Render changed Kustomize roots before proposing live sync.
- Validate AppProject paths, destination namespaces, sync waves, and source repo paths when moving files.
- Prefer narrow diffs. Avoid broad layout changes while debugging a sync issue.

## Platform domains

Use these domains consistently:

- `argocd`: GitOps controller, root app, child apps, repo access
- `external-secrets`: External Secrets Operator resources and secret delivery wiring
- `network`: DNS, Cloudflare Tunnel, edge exposure, and network services
- `ingress`: ingress controller resources and routing entry points
- `cert-manager`: issuers, certificates, and TLS automation
- `observability`: VictoriaMetrics, Grafana, exporters, dashboards, and alerts
- `data-platform`: ClickHouse, graph workloads, data services, and related operators

## Namespace and project rules

- Namespaces should match platform ownership and security boundaries.
- AppProjects should group resources by platform domain, not by temporary task.
- Avoid namespace sprawl; add a namespace only when ownership, policy, or lifecycle differs.

## Secrets caution

- Do not commit plaintext secrets, kubeconfigs, tokens, private keys, or credentials.
- Do not read or print live Secret values.
- Prefer Infisical plus External Secrets Operator for secret delivery.
- When debugging ExternalSecret drift, inspect metadata, status, and field ownership before reading sensitive data.

## Node and storage rules

- Node labels, taints, tolerations, and affinity are scheduling contracts. Document why they exist.
- Node-specific workloads must state their node affinity and failure assumptions.
- Storage choices must name the storage class, replication expectation, locality, and recovery impact.
- Data-heavy workloads should not land on shared workers without explicit sizing and placement discussion.
