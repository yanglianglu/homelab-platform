# Homelab Operating Workflow

This document defines how Codex and the repo should move work across
Repo/GitHub, the `docs/` Obsidian vault, Linear, and live operations.

## Source Of Truth

| System | Owns |
| --- | --- |
| Repo/GitHub | Exact manifests, commands, runbooks, scripts, repo structure, implementation details, deployable state, and versioned operational truth |
| `docs/` Obsidian vault | Architecture narrative, decisions, synthesis, learning notes, knowledge index, knowledge log, source notes approved for the repo, and agent-readable memory |
| Linear | Execution status, priority, sequencing, blockers, and small verifiable work gates |

If they disagree:

1. Refresh repo operational truth first.
2. Check Linear live before claiming current issue status.
3. Use `docs/` for durable repo-local knowledge updates.
4. Treat old Notion references as historical only.

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
| network | DNS, VPN, internal Gateway API, routing, and selected exposure paths |
| observability | metrics, logs, dashboards, exporters, alerts |
| security | identity, secrets, access control, hardening |
| data | ClickHouse, graph workloads, datasets, data services |
| apps | user-facing apps and smoke tests |
| docs | `docs/` Obsidian vault, repo docs, ADRs, runbooks, knowledge index, knowledge log |

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
Harvester -> Talos HA control plane -> workers -> Argo CD
-> External Secrets / Infisical -> whoami smoke app
-> Harvester CSI proof on data-01 -> guest observability baseline
-> internal Gateway API route with verified HTTPS backend
```

Next platform gates:

1. Add reviewed NetworkPolicies beyond Argo CD.
2. Clean up the duplicate Envoy Gateway VIP display if a cleaner service-address
   model is available.
3. Run a ClickHouse-specific PVC pilot before large ingestion.
4. Add reviewed, low-noise guest alerts after dashboard review.
5. Keep Cloudflare, public DNS, public ACME, service mesh, and public app
   exposure as separate future decisions.

## Definition Of Done

A gate is done when:

1. The result is implemented or the manual operation is documented.
2. The result has been verified.
3. Repo/GitHub reflects operational truth.
4. `docs/` reflects durable knowledge, architecture, runbook, ADR, or context
   changes that should survive the chat.
5. Linear is updated only after live status is checked or the user explicitly
   asks for a state change.
