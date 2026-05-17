# Homelab Operating Workflow

This document defines how Codex and the repo should move work across GitHub,
Notion, Linear, and live operations.

## Source Of Truth

| System | Owns |
| --- | --- |
| GitHub | Exact manifests, commands, runbooks, repo structure, implementation details |
| Notion | Human navigation, architecture narrative, decisions, summaries, learning notes |
| Linear | Execution status, priority, sequencing, blockers |

If they disagree, refresh GitHub operational truth first, then summarize to
Notion or Linear.

## Collaboration Contract

For homelab platform work, do not implement just because an issue is next or the
user says "proceed next".

Required flow:

```text
Explain -> discuss options -> agree on approach -> implement -> verify -> update durable records
```

Before durable repo edits, live-cluster changes, Linear state changes, network
exposure, security/access changes, VM changes, or product/tool decisions, Codex
must explain:

- the goal and current context
- available options
- tradeoffs, risks, and blast radius
- exact intended changes
- validation and rollback
- what remains out of scope

Read-only inspection, status checks, and explicitly requested commands are
allowed before implementation approval.

## Work Domains

| Domain | Scope |
| --- | --- |
| platform | Kubernetes system services, GitOps, secrets, policies, storage classes |
| harvester | VM desired state, storage classes, networks, images |
| talos | node bootstrap, machine config, control-plane and worker lifecycle |
| network | DNS, VPN, tunnels, ingress, routing |
| observability | metrics, logs, dashboards, exporters, alerts |
| security | identity, secrets, access control, hardening |
| data | ClickHouse, graph workloads, datasets, data services |
| apps | user-facing apps and smoke tests |
| docs | GitHub docs, Notion summaries, ADRs, runbooks |

Prefer small gates that produce a verifiable platform capability.

## Documentation Rules

- Info docs describe current state.
- Architecture docs explain why the system is designed a certain way.
- Runbooks explain how to perform or recover an operation.
- ADRs capture major tradeoffs.
- Operations logs are historical and should not pollute current-state docs.

Detailed placement rules live in `docs/documentation-strategy.md`.
The content map lives in `docs/knowledge-index.md`.

## Linear Rules

The Linear workspace uses `FIF` issue keys. Linear issues should be concrete,
verifiable, and small enough to finish in a focused gate.

Issue shape:

```markdown
## Goal
## Context
## Acceptance Criteria
## Verification
## Rollback / Recovery
```

Do not duplicate active Linear status in Markdown unless recording a historical
snapshot. Check Linear live before saying an issue is currently open, blocked,
or done.

## GitHub Rules

Every meaningful implementation should leave:

- a narrow diff
- validation notes
- docs updated when operational truth changed
- no plaintext secrets, kubeconfigs, tokens, private keys, or generated secret
  material

For Kubernetes manifests, render the relevant Kustomize roots before live sync
or PR handoff.

## Current Platform Milestone

Current baseline:

```text
Harvester -> Talos HA control plane -> workers -> Argo CD -> External Secrets / Infisical -> whoami smoke app -> Harvester CSI proof on data-01
```

Next platform gates:

1. Roll the Harvester CSI mountpoint extension to all Talos nodes.
2. Sync the Argo CD managed Harvester CSI app from Git.
3. Run larger CSI drills before approving large ClickHouse PVCs or legacy disk detach.
4. Add observability before large ClickHouse ingestion.
5. Add ingress, cert-manager, DNS, and Cloudflare Tunnel after platform storage
   and observability are stable.

## Definition Of Done

A gate is done when:

1. The result is implemented or the manual operation is documented.
2. The result has been verified.
3. GitHub reflects operational truth.
4. Notion is updated only when human navigation or durable explanation changed.
5. Linear is updated only after live status is checked or the user explicitly
   asks for a state change.
