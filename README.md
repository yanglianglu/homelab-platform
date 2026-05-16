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
| Harvester node IPs | `192.168.1.241` (`the-abundance`), `192.168.1.250` (`the-elation`), `192.168.1.244` (`the-enigmata`) |
| Harvester VIP/UI | `192.168.1.50` |
| Harvester VM namespace | `talos-cluster` |
| Harvester VM network | `lan-untagged` |
| Active Talos VM | `cp-01` |
| Active Talos node IP | `192.168.1.181` |
| Talos cluster name | `homelab-talos` |
| Talos Kubernetes API endpoint | `https://192.168.1.181:6443` |
| Talos version | `v1.13.0` |
| Retired old Talos VM | `talos-cp-01` at `192.168.1.178` has been removed |

## Current Milestone

`cp-01` has been created on Harvester, configured as the active Talos control-plane node, bootstrapped, and confirmed healthy. Core Kubernetes pods are running. The old `talos-cp-01` VM has been retired and should not be recreated unless a future recovery plan explicitly calls for it.

## Repository Boundaries

- `docs/` is for human-readable notes and runbooks. It has no deployment power.
- `harvester/` is for Harvester-side desired state. Do not commit live exports with runtime metadata.
- `talos/` is for Talos OS and Kubernetes bootstrap configuration. Do not commit plaintext generated secrets.
- `kubernetes/` is for post-bootstrap Kubernetes platform services and workloads.
- `secrets/` is a placeholder only. Use encryption before storing real secrets.

## Growth Model

The next platform shape is documented in `docs/architecture/gradual-vm-growth-plan.md`.

The short version:

- Grow from one Talos control-plane VM to three control-plane VMs.
- Add two initial worker VMs before deploying heavier platform services.
- Keep large data workloads on the dedicated `data-01` Talos data worker, not on the shared general worker pool.
- Add a third worker only after metrics show the need.

## Operating Workflow

Planning, knowledge capture, implementation, and review should follow `docs/operating-workflow.md`.
Documentation source-of-truth rules live in `docs/documentation-strategy.md`.
Architecture decisions are indexed in `docs/adrs.md`.

## First Workflow

1. Create Harvester VM infrastructure.
2. Generate and apply Talos machine config.
3. Bootstrap Kubernetes once from the first control-plane node.
4. Apply manifests from `kubernetes/clusters/homelab`.

## Local macOS Access

Harvester kubeconfig is kept outside this repository. The local convention is:

- kubeconfig path: `~/.kube/harvester.yaml`
- shell alias: `kh="KUBECONFIG=$HOME/.kube/harvester.yaml kubectl"`

See `docs/runbooks/macos-kubeconfig.md` for setup and verification.
