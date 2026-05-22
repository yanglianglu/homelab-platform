# Obsidian Vault Agent Reference

This reference defines how agents should use the homelab Obsidian vault stored under `docs/`.

## Core Rule

`docs/` is both the Obsidian vault and the repo documentation tree.

Do not treat GitHub and Obsidian as separate competing sources of truth. GitHub is the versioned repo and delivery mechanism. Obsidian is the local navigation, linking, editing, and thinking surface for Markdown files that live in the repo.

```text
Repo/GitHub = versioned operational truth and delivery mechanism
/docs Obsidian vault = repo-local human and agent knowledge layer
Linear = execution status, priority, sequencing, and blockers
```

Notion is retired from the active workflow. Do not create, edit, mirror, or suggest Notion follow-ups. Older Notion references in historical logs are superseded by this reference.

## Source Of Truth

| System | Owns |
| --- | --- |
| Repo/GitHub | Exact manifests, commands, scripts, runbooks, repo structure, implementation details, deployable state, and versioned operational truth |
| `/docs` Obsidian vault | Architecture narrative, ADRs, durable synthesis, learning notes, knowledge index, knowledge log, context checkpoints, approved source notes, and agent-readable memory |
| Linear | Execution status, priority, sequencing, blockers, and verifiable work gates |

If sources disagree:

1. Refresh repo operational truth first.
2. Check Linear live before claiming issue status.
3. Update `/docs` when durable knowledge, navigation, architecture, or workflow truth changes.
4. Treat old Notion wording as historical only.

## Companion Style Pages

The vault includes short, token-optimized pages named `Progressive`, `Obsidian Zen`, and `Harness`.

Use them as style primers:

| Page | Agent use |
| --- | --- |
| `Progressive` | Prefer progressive disclosure: compact summary first, deeper details behind headings and links |
| `Obsidian Zen` | Keep notes clean, sparse, linkable, and low-noise; avoid bloated prose and duplicate truth |
| `Harness` | Follow the agent execution frame: inspect context, explain options, wait for approval when required, implement narrowly, verify, and update durable records |

Do not expand these pages into long manuals unless the user explicitly asks. They are token harnesses, not exhaustive documentation.

## Documentation Placement

| Content type | Home |
| --- | --- |
| Info docs and current-state summaries | existing `docs/*.md` pages close to the domain |
| Kubernetes manifests | `kubernetes/` |
| Harvester desired state | `harvester/` |
| Talos bootstrap/config inputs | `talos/` |
| Helper scripts | repo script directories close to usage |
| Secret handling rules | repo-local docs close to implementation |
| Exact runbooks and recovery commands | `docs/runbooks/` |
| Architecture notes and plans | `docs/architecture/` |
| ADRs and decision records | `docs/architecture/` or `docs/adrs/` when a dedicated ADR tree exists |
| Knowledge map | `docs/knowledge-index.md` |
| Knowledge ingest/change log | `docs/knowledge-log.md` |
| Operations logs | `docs/knowledge-log.md` or clearly dated historical docs |
| Source notes approved for the repo | approved immutable repo folder only when safe and intentional |
| Context checkpoints and agent references | `docs/codex/` |
| Raw external source material | external storage unless it is safe and intentionally versioned |

Avoid placeholder-only folders. Prefer one useful parent README over many sparse files.

## Note Shape

Use stable headings and short sections. Start with what an agent needs to know.

Only add front matter when tooling needs it. If used, keep it sparse:

```yaml
---
type: reference | architecture | runbook | adr | status | source-note | context
status: current | draft | historical | deprecated
domain: platform | harvester | talos | network | observability | security | data | apps | docs
updated: YYYY-MM-DD
---
```

Recommended page structure:

```markdown
# Page Title

## Current State

## Why This Exists

## Source Of Truth

## Operating Rules

## Validation

## Related Pages
```

For runbooks, prefer:

```markdown
# Runbook Title

## Scope
## Preconditions
## Commands
## Verification
## Rollback / Recovery
## Related Pages
```

For ADRs, prefer:

```markdown
# ADR-###: Decision Title

## Status
## Context
## Decision
## Alternatives Considered
## Consequences
## Validation
```

## Token Optimization Rules

- Put the actionable summary at the top.
- Use tables when they compress repeated structure.
- Link to details instead of duplicating them.
- Keep current-state docs separate from historical logs.
- Mark stale/historical/deprecated content explicitly.
- Remove retired desired-state files after intentional retirement.
- Preserve history only when it prevents accidental recreation, IP reuse, or operational confusion.
- Do not duplicate Linear live status in Markdown.
- Do not duplicate exact commands across multiple docs unless there is a clear recovery reason.

## Agent Workflow

For platform work, use this gate:

```text
Explain -> discuss options -> agree on approach -> implement -> verify -> update durable records
```

Before durable repo edits, live-cluster changes, Linear state changes, network exposure, security/access changes, VM changes, or product/tool decisions, explain:

- goal and current context
- available options
- tradeoffs, risks, and blast radius
- exact intended changes
- validation and rollback
- what remains out of scope

Read-only inspection, status checks, and explicitly requested commands are allowed before implementation approval.

## Update Loop

After meaningful work:

```text
Do work
-> verify result
-> update repo operational truth if changed
-> update /docs vault knowledge if durable knowledge changed
-> update docs/knowledge-index.md if navigation changed
-> append docs/knowledge-log.md for durable ingests, syntheses, lint passes, and workflow changes
-> update Linear only after checking live status or receiving explicit user approval
```

Knowledge log entries should use:

```markdown
## [YYYY-MM-DD] type | Title

- Source:
- Pages touched:
- Summary:
- Contradictions:
- Open questions:
- Validation:
```

## Validation Commands

For docs-only work:

```bash
rg -n "Notion|notion|Homelab HQ|user-maintained|mirror|manual follow-up|browsable human" \
  AGENTS.md docs .github || true

git diff --check
```

For broad documentation refactors:

```bash
rg -n "deprecated|historical|TODO|FIXME|Notion|notion" docs AGENTS.md .github || true
rg -n "docs/codex/obsidian-vault-agent-reference.md|Progressive|Obsidian Zen|Harness" docs/knowledge-index.md docs || true
git diff --check
```

If Kubernetes manifests changed, render the relevant Kustomize roots before handoff. If the change was intended to be docs-only and manifests changed, stop and report the accidental diff.

## Anti-Patterns

Do not:

- describe Notion as active
- suggest manual Notion updates
- mirror Obsidian notes into another tool
- use Markdown to track active Linear status
- bury current state inside historical logs
- turn compact reference pages into bloated essays
- write secrets, kubeconfigs, tokens, private keys, or generated secret material
- make live-cluster or Linear mutations without the required gate
