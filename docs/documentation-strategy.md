# Documentation Strategy

This document defines what belongs in GitHub, what belongs in Notion, and how the two should reference each other.

## Core Rule

Use GitHub for operational truth that must version with the platform. Use Notion for durable knowledge, decisions, explanation, and portfolio narrative.

```text
GitHub = exact state, commands, manifests, scripts, runbooks close to code
Notion = architecture, decisions, specs, learning, inventory, and narrative
Linear = execution status and prioritization
```

## Placement Matrix

| Content type | Primary home | Reason |
| --- | --- | --- |
| Kubernetes manifests | GitHub | Must be versioned and deployable |
| Harvester desired-state summaries | GitHub | Close to infrastructure implementation |
| Talos patches and cluster variables | GitHub | Required for repeatable cluster bootstrap |
| Helper scripts | GitHub | Executable platform workflow |
| Secret handling rules | GitHub and Notion | GitHub for repo rules, Notion for operating policy |
| Runbooks with commands | GitHub first, mirrored/summarized in Notion | Commands should version with repo; Notion improves discoverability |
| Architecture overview | Notion first, summarized in GitHub | Long-lived explanation and diagrams are easier to browse in Notion |
| ADRs | Notion first, linked from GitHub | Decisions need context and rationale more than deployment power |
| Roadmap | Notion and Linear | Notion explains phases; Linear tracks execution |
| Linear issue status | Linear | Avoid stale duplicate status in docs |
| Project specs | Notion | Product thinking and scope evolve before implementation |
| Dataset catalog | Notion | Metadata, ownership, lineage, and freshness are knowledge-base concepts |
| Systems catalog | Notion | Inventory is easier to browse, relate, and update in Notion |
| Incident notes | Notion, with GitHub links when fixes happen | The learning matters beyond the code change |
| Exact current IP/device inventory | GitHub if used for operations, Notion if only explanatory | Keep the operational source of truth in one place and link the other |

## Current Repo Docs Classification

| File | Keep in GitHub? | Notion treatment |
| --- | --- | --- |
| `README.md` | Yes | Link from Homelab HQ |
| `docs/operating-workflow.md` | Yes | Mirror as Notion workflow page |
| `docs/documentation-strategy.md` | Yes | Mirror or summarize in Notion |
| `docs/network.md` | Yes | Summarize in Network domain page |
| `docs/network-map.md` | Yes | Mirror diagrams or link from Notion |
| `docs/network-inventory.md` | Yes for now | Later decide if Systems Catalog becomes primary |
| `docs/ip-plan.md` | Yes for now | Later decide if Systems Catalog becomes primary |
| `docs/port-map.md` | Yes for now | Later decide if Systems Catalog becomes primary |
| `docs/hardware.md` | Yes for now | Mirror to Systems Catalog |
| `docs/storage.md` | Yes | Link from Harvester/storage system pages |
| `docs/talos.md` | Yes | Summarize in Talos system page |
| `docs/runbooks/*.md` | Yes | Link from Notion Runbooks database or hub |
| `harvester/**/*.yaml` | Yes | Link from Harvester system page |
| `talos/**/*.yaml` | Yes | Link from Talos system page |
| `kubernetes/README.md` | Yes | Link from Platform domain page |
| `secrets/README.md` | Yes | Link from security policy page |

## Audit Result: Current Source Of Truth

| Area | GitHub role | Notion role | Follow-up |
| --- | --- | --- | --- |
| Repository overview | Primary for repo boundaries and local entry points | Link from Homelab HQ | None |
| Operating workflow | Primary index for the repo workflow contract | Mirrored as `Homelab Operating Workflow` | Keep both aligned when workflow changes |
| Documentation strategy | Primary index for placement rules | Mirrored as `Homelab Documentation Strategy` | Keep both aligned when placement rules change |
| ADRs | Lightweight index only | Primary ADR content | `FIF-5` completed |
| Network notes | Primary for operational network facts while the cluster is being built | Summaries in Network/System Catalog pages | `FIF-8` updates stale 3-node inventory |
| IP plan | Primary while IP assignments affect operations | Later may become Systems Catalog summary | `FIF-8` updates stale node names/IPs |
| Port map | Primary while switch ports affect operations | Later may become Systems Catalog summary | `FIF-8` updates topology if needed |
| Hardware inventory | Primary while hardware facts affect deployment | Mirror to Systems Catalog | `FIF-8` or later Systems Catalog issue |
| Storage notes | Primary for storage classes and operational expectations | Summarize under Harvester/storage system pages | `FIF-9` replaces placeholder storage notes |
| Talos docs/runbooks | Primary for exact commands, scripts, and recovery steps | Link from Talos system page and runbook hub | `FIF-11`, `FIF-12`, `FIF-13` verify access and health |
| Harvester desired state | Primary for desired-state summaries and operator notes | Link from Harvester system page | `FIF-9` replaces placeholder network/storage notes |
| Kubernetes folder | Primary for future GitOps manifests | Link from Platform domain page | `FIF-16`, `FIF-17`, `FIF-18` build GitOps baseline |
| Secrets policy | Primary for repo safety rules and External Secrets Operator conventions | Summarize in security policy page | `FIF-18` chooses Infisical + External Secrets Operator |

## Files Needing Immediate Cleanup

The audit found no files that should be removed from GitHub today. The main problem is stale or placeholder content, not misplaced content.

Immediate cleanup is tracked in Linear:

| Linear issue | Cleanup |
| --- | --- |
| `FIF-8` | Update Harvester inventory docs with the live 3-node state |
| `FIF-9` | Replace Harvester network and storage placeholders with verified desired-state notes |
| `FIF-11` | Configure local `kubectl` access for `homelab-talos` |
| `FIF-12` | Configure `talosctl` access and verify cluster health |
| `FIF-13` | Confirm guest Kubernetes core pods live |
| `FIF-18` | Choose initial secrets approach for GitOps |

## Future Notion-Primary Candidates

These areas may move to Notion-primary once the platform stabilizes:

| Area | Future Notion home | GitHub role after migration |
| --- | --- | --- |
| Systems inventory | Systems Catalog | Link to catalog and keep only operational facts needed by scripts/runbooks |
| Dataset inventory | Dataset Catalog | Keep dataset schemas/manifests only if they become deployable artifacts |
| Project specs | Project Specs | Link implementation paths and PRs |
| Incidents and experiments | Incident / Learning Log | Link fixes, runbooks, and PRs |

## Duplication Rule

Do not keep two full sources of truth unless there is a clear reason.

Use this pattern:

```text
GitHub owns exact commands/config.
Notion owns explanation and links to the GitHub file.
Linear owns whether the work is planned, active, blocked, or done.
```

If a Notion page mirrors a GitHub runbook, keep the Notion copy short and link to the repo file for exact commands.

## Self-Evolving Workflow

After each meaningful work session, update the operating model if the way of working changes.

Capture:

- What slowed the work down.
- What information was missing.
- Which doc should become easier to find.
- Which Linear issue/project structure needs adjustment.
- Whether GitHub or Notion had the wrong source of truth.

Use this loop:

```text
Do work -> verify result -> update GitHub if operational truth changed -> update Notion if knowledge changed -> update Linear status -> improve workflow if friction appeared
```

The workflow itself lives in:

- GitHub: `docs/operating-workflow.md`
- Notion: `Homelab Operating Workflow`

This document should be updated when documentation placement rules change.
