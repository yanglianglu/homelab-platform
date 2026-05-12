# Linear Homelab Execution Views

This reference defines the saved Linear views for homelab execution. The Linear
connector can create labels and update issues, but saved custom view creation is
a Linear UI action.

Use this file as the source of truth when creating or repairing those views.

## Label Model

Use one `domain` label and one `workflow` label per issue.

Domain labels:

- `platform`: Kubernetes, Harvester, GitOps, cluster runtime, platform services
- `security`: identity, secrets, access control, policy, TLS, hardening
- `network`: DNS, VPN, tunnel, ingress, routing, network monitoring
- `storage`: storage classes, disks, backups, data placement, Longhorn behavior
- `observability`: metrics, logs, alerts, dashboards, audit visibility
- `data`: databases, lakehouse, query engines, datasets, governance
- `ai`: LLM serving, vector search, embeddings, GPU workloads, chat-with-data
- `apps`: portfolio apps, demos, dashboards, user-facing services
- `sandbox`: experiments that may break
- `docs`: Notion, GitHub docs, runbooks, ADRs, documentation structure

Workflow labels:

- `needs-discussion`: issue should be discussed before implementation
- `decision-needed`: user decision required before implementation
- `ready`: enough context and acceptance criteria to start
- `blocked`: blocked by dependency, access, decision, or external system
- `verify`: implementation exists but verification is still needed

## Lifecycle

Use this operating flow:

```text
Backlog -> Needs Discussion -> Todo -> In Progress -> Verify -> Done
```

Practical mapping:

- `Backlog`: known work, not committed for immediate execution
- `needs-discussion`: shape the problem before implementation
- `decision-needed`: choose an approach before implementation
- `Todo` + `ready`: next work item can be started
- `In Progress`: currently being executed
- `verify`: merged or deployed, but live checks are still pending
- `Done`: verified outcome, notes captured

## Saved Views

Create these as team-level custom views for `Fifth-Roundtable`.

### Homelab - Now / Next / Later

Purpose: daily execution without scanning the whole backlog.

Recommended layout:

- Type: issue view
- Team: `Fifth-Roundtable`
- Exclude statuses: `Done`, `Canceled`, `Duplicate`
- Group by: status
- Sort by: priority, then updated date

Interpretation:

- Now: `In Progress`
- Next: `Todo` with label `ready`
- Later: `Backlog` items without `ready`

Useful filter:

```text
team = Fifth-Roundtable
status != Done
status != Canceled
status != Duplicate
```

### Homelab - Decision Needed

Purpose: collect issues that should not be implemented until a decision is made.

Recommended layout:

- Type: issue view
- Team: `Fifth-Roundtable`
- Label: `decision-needed`
- Exclude statuses: `Done`, `Canceled`, `Duplicate`
- Group by: project
- Sort by: priority, then created date

Useful filter:

```text
team = Fifth-Roundtable
label = decision-needed
status != Done
status != Canceled
status != Duplicate
```

### Homelab - Stage Board

Purpose: see roadmap execution by stage.

Recommended layout:

- Type: issue view
- Team: `Fifth-Roundtable`
- Exclude statuses: `Done`, `Canceled`, `Duplicate`
- Group by: project
- Secondary grouping if available: milestone
- Sort by: project order, then priority

Useful filter:

```text
team = Fifth-Roundtable
status != Done
status != Canceled
status != Duplicate
```

### Homelab - Domain Board

Purpose: see work by architecture area.

Recommended layout:

- Type: issue view
- Team: `Fifth-Roundtable`
- Exclude statuses: `Done`, `Canceled`, `Duplicate`
- Group by: label
- Include domain labels only when possible
- Sort by: priority, then updated date

Useful filter:

```text
team = Fifth-Roundtable
status != Done
status != Canceled
status != Duplicate
label in platform, security, network, storage, observability, data, ai, apps, sandbox, docs
```

### Homelab - Verify Queue

Purpose: keep implementation and verification separate.

Recommended layout:

- Type: issue view
- Team: `Fifth-Roundtable`
- Label: `verify`
- Exclude statuses: `Done`, `Canceled`, `Duplicate`
- Group by: project
- Sort by: updated date

Useful filter:

```text
team = Fifth-Roundtable
label = verify
status != Done
status != Canceled
status != Duplicate
```

## Current Active Labeling

As of the first GitOps smoke app completion:

- `FIF-19`: `network`, `decision-needed`
- `FIF-20`: `network`, `decision-needed`
- `FIF-21`: `network`, `blocked`
- `FIF-22`: `security`, `blocked`
- `FIF-25`: `docs`, `ready`
- `FIF-7`: `docs`, `blocked`

The completed Stage 3 GitOps issues remain labeled by their domain for history:

- `FIF-17`: `apps`, `ready`
- `FIF-18`: `security`, `ready`
- `FIF-23`: `platform`, `ready`
- `FIF-24`: `security`, `ready`
- `FIF-26`: `security`, `ready`

## Manual Setup Checklist

1. Open Linear and go to the `Fifth-Roundtable` team.
2. Create a custom issue view named `Homelab - Now / Next / Later`.
3. Create a custom issue view named `Homelab - Decision Needed`.
4. Create a custom issue view named `Homelab - Stage Board`.
5. Create a custom issue view named `Homelab - Domain Board`.
6. Create a custom issue view named `Homelab - Verify Queue`.
7. Pin or favorite the views in the order above.
8. Confirm FIF-19 and FIF-20 appear in `Decision Needed`.
9. Confirm FIF-21 and FIF-22 appear as blocked Stage 4 work.
10. Confirm done Stage 3 issues are not cluttering the active views.

## Connector Limitation

The currently available Linear connector tools do not expose saved custom view
creation. They can update issues, comments, labels, projects, initiatives, and
status metadata, but view creation must be done in the Linear UI.
