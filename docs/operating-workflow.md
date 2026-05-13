# Homelab Operating Workflow

This document defines how planning, documentation, implementation, and review work should move across Notion, Linear, and GitHub for the homelab platform.

## Operating Philosophy

Use each system for the job it is best at:

| Tool | Source of truth for |
| --- | --- |
| Notion | Architecture, decisions, specs, runbooks, research, and long-lived knowledge |
| Linear | Roadmap, projects, milestones, issues, priorities, blockers, and execution cadence |
| GitHub | Code, infrastructure manifests, branches, pull requests, reviews, CI, and deployment history |

The default flow is:

```text
Idea -> Notion spec/decision -> Linear project/issues -> GitHub branch/PR -> CI/deploy -> Notion runbook/update -> Linear done
```

## Collaboration Contract

For homelab work, implementation does not begin just because an issue is next in
Linear or the user says to proceed. The default collaboration mode is:

```text
Explain -> discuss options -> agree on approach -> implement -> verify -> update docs/Linear
```

Before making repo, cluster, Linear state, or product/tooling decisions, Codex
must first give the user the full picture:

- what the issue is trying to accomplish
- why it matters in the platform sequence
- what choices are available
- the tradeoffs, risks, and blast radius of each choice
- what implementation would change
- what verification would prove success

Only after that discussion should Codex ask for explicit approval to implement.
This is especially important for product/tool choices, access/security
decisions, network exposure, GitOps changes, Kubernetes cluster changes, and
anything that becomes durable platform policy.

Exceptions are limited to read-only investigation, status checks, and commands
that the user explicitly asks to run. If the user asks "what is next" or
"proceed next", interpret that as permission to explain and prepare, not as
permission to decide and implement.

## Domain Model

Organize work around platform domains, but deliver through small vertical slices.

| Domain | Scope |
| --- | --- |
| platform | Kubernetes system components, ingress, cert-manager, external-dns, secrets, storage classes, GitOps |
| observability | Prometheus, Grafana, Loki, metrics exporters, alerts, dashboards |
| network | VPN, Cloudflare Tunnel, DNS, routing, traffic monitoring |
| security | Identity-aware access, auth, secrets, policy, access control, network policy |
| data | ClickHouse, Postgres, object storage, ingestion jobs, metadata, dataset governance |
| ai | vLLM, Ollama, vector DB, embedding workers, GPU workloads |
| apps | Portfolio and demo applications |
| sandbox | Experiments that may break |

Do not try to fully finish one domain before touching the others. Build one useful capability end to end, then deepen the relevant domains.

## Notion Workflow

Notion is the knowledge base. It should answer what exists, why it exists, how it works, and how to operate it.

Recommended Notion areas:

| Area | Purpose |
| --- | --- |
| Homelab Platform HQ | Top-level map and links |
| Architecture | Diagrams, domain model, platform explanations |
| Roadmap | Human-readable roadmap linked to Linear |
| Decision Log | ADRs and rationale |
| Runbooks | Operational procedures |
| Systems Catalog | Inventory of Harvester, Talos, Kubernetes, Grafana, ClickHouse, VPN, and related systems |
| Project Specs | Flight tracking, GDELT, chat-with-data, data lake control plane |
| Dataset Catalog | ADS-B, GDELT, network telemetry, power metrics, Prometheus data |
| Incident / Learning Log | Outages, experiments, root causes, and lessons learned |

Create or update Notion when:

- A new project needs definition.
- A decision affects architecture, security, operations, or future maintenance.
- A runbook is needed for repeatable operations.
- A system becomes important enough to inventory.
- An incident or experiment teaches something worth remembering.

Avoid using Notion for daily task status. Link to Linear instead.

## Documentation Placement

Use GitHub for operational truth that must version with the platform. Use Notion for durable knowledge, decisions, explanation, and portfolio narrative.

```text
GitHub = exact state, commands, manifests, scripts, runbooks close to code
Notion = architecture, decisions, specs, learning, inventory, and narrative
Linear = execution status and prioritization
```

Detailed placement rules live in `docs/documentation-strategy.md`.

## Linear Workflow

Linear is the execution system.

Recommended structure:

```text
Team: Homelab Platform
Key: HOM

Initiatives:
- Homelab Cloud Platform
- Secure Observable Operations
- Data + AI Platform
- Portfolio Applications

Projects:
- Platform MVP
- Observability Baseline
- Secure Access Baseline
- Data Platform MVP
- Flight Tracking Analytics MVP
- AI Platform MVP
- Chat-with-Data MVP
- Data Lake Control Plane
```

Use initiatives for strategic themes, projects for shippable outcomes, milestones for project phases, issues for concrete work, and cycles for execution windows.

### Issue Template

```markdown
## Goal
What result should exist when this is done?

## Context
Why this matters, including links to Notion or GitHub.

## Acceptance Criteria
- [ ] Concrete observable outcome
- [ ] Verification step
- [ ] Docs updated if needed

## Verification
Command, URL, dashboard, screenshot, or PR check.

## Rollback / Recovery
How to undo or recover if this breaks something.
```

### Issue Sizing

Prefer issues that take 0.5 to 2 days.

Avoid broad issues such as:

```text
Set up Kubernetes
```

Prefer concrete issues such as:

```text
Install ingress-nginx in the guest cluster
Configure cert-manager ClusterIssuer
Deploy whoami behind HTTPS ingress
```

### Workflow States

| State | Meaning |
| --- | --- |
| Triage | Raw idea, not accepted yet |
| Backlog | Accepted, not ready |
| Ready | Scope and acceptance criteria are clear |
| In Progress | Actively being worked |
| Blocked | Cannot proceed without a dependency or decision |
| In Review | PR open or verification pending |
| Done | Merged, deployed/tested, and docs updated if needed |
| Canceled | Intentionally not doing |

### Labels

Keep labels useful and limited:

| Group | Values |
| --- | --- |
| Domain | platform, observability, network, security, data, ai, apps, sandbox |
| Type | feature, bug, task, research, documentation, maintenance |
| Risk | low, medium, high |
| Workload | infra, kubernetes, database, frontend, backend, ml |

## GitHub Workflow

GitHub is the implementation record.

Every meaningful implementation issue should have:

- A Linear issue.
- A branch named with the Linear issue key.
- A pull request that references the Linear issue.
- Verification notes in the PR.
- Documentation updates when the implementation changes long-lived knowledge.

Branch naming:

```text
codex/HOM-23-cert-manager-clusterissuer
```

PR title:

```text
HOM-23 Configure cert-manager ClusterIssuer
```

PR checklist:

```markdown
## Summary
- What changed

## Verification
- Command, check, dashboard, or URL used to verify

## Rollback
- How to revert or recover if needed

## Links
- Linear issue
- Notion spec/runbook/ADR, if relevant
```

## Cadence

Use a lightweight scrum rhythm.

| Cadence | Ritual | Output |
| --- | --- | --- |
| Weekly | Planning | Pick focused work for the week or cycle |
| 2-3x/week | Standup check | Note progress, blockers, and next action |
| Weekly | Backlog refinement | Break large ideas into ready issues |
| End of cycle | Review/demo | Show a working capability |
| End of cycle | Retro | Capture what slowed work down and what to improve |
| As needed | ADR/runbook update | Preserve decisions and operations knowledge |

Use two-week Linear cycles by default. Each cycle should have one main outcome.

## Definition of Done

A capability is done when:

1. The implementation is merged or the manual change is documented.
2. The result has been verified.
3. The relevant Linear issue is closed.
4. Any architecture decision is captured in Notion.
5. Any repeated operational process has a runbook.
6. Any code or infrastructure state lives in GitHub.
7. The result is observable enough to debug later.

## Self-Evolving Workflow

After each meaningful work session, improve the workflow when friction appears.

Capture:

- What slowed the work down.
- What information was missing.
- Which doc should become easier to find.
- Which Linear issue/project structure needs adjustment.
- Whether GitHub or Notion had the wrong source of truth.

Then update the right system:

```text
Operational truth changed -> update GitHub
Knowledge or rationale changed -> update Notion
Execution state changed -> update Linear
Workflow rule changed -> update this document
```

## First Operating Milestone

The first target is Platform MVP:

```text
Guest Kubernetes on Harvester
-> ingress
-> DNS
-> TLS
-> GitOps
-> test app
-> basic observability
```

Definition of done:

```text
Push a config change to GitHub and see an HTTPS app running on the guest Kubernetes cluster with logs and metrics available.
```
