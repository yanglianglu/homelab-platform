# homelab-platform

This repository manages my Harvester + Talos + Kubernetes home lab. It keeps the virtualization layer, node bootstrap layer, and workload layer in one monorepo while keeping their responsibilities separate.

## Layer Model

1. **Harvester creates VMs**
   - Harvester runs the virtualization platform.
   - Desired VM, namespace, network, storage, and image references live under `harvester/`.

2. **Talos configures those VMs as Kubernetes nodes**
   - Talos installs and configures the operating system on the VMs.
   - Cluster variables, patches, and helper scripts live under `talos/`.

3. **Kubernetes deploys workloads after the cluster exists**
   - Platform services and applications are applied after the Kubernetes API is reachable.
   - Workloads, ingress, storage, monitoring, and apps live under `kubernetes/`.

## Current Environment

| Item | Value |
| --- | --- |
| Harvester node IP | `192.168.1.241` |
| Harvester VIP/UI | `192.168.1.50` |
| Harvester VM namespace | `talos-cluster` |
| Harvester VM network | `lan-untagged` |
| First Talos VM | `talos-cp-01` |
| First Talos node IP | `192.168.1.178` |
| Talos cluster name | `homelab-talos` |
| Talos Kubernetes API endpoint | `https://192.168.1.178:6443` |
| Talos version | `v1.13.0` |

## Current Milestone

`talos-cp-01` has been created on Harvester, configured as the first Talos control-plane node, bootstrapped, and confirmed healthy. Core Kubernetes pods are running.

## Repository Boundaries

- `docs/` is for human-readable notes and runbooks. It has no deployment power.
- `harvester/` is for Harvester-side desired state. Do not commit live exports with runtime metadata.
- `talos/` is for Talos OS and Kubernetes bootstrap configuration. Do not commit plaintext generated secrets.
- `kubernetes/` is for post-bootstrap Kubernetes platform services and workloads.
- `secrets/` is a placeholder only. Use encryption before storing real secrets.

## First Workflow

1. Create Harvester VM infrastructure.
2. Generate and apply Talos machine config.
3. Bootstrap Kubernetes once from the first control-plane node.
4. Apply manifests from `kubernetes/clusters/homelab`.
