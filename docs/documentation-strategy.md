# Documentation Strategy

This document defines how repo documentation, the `docs/` Obsidian vault, and
Linear divide responsibility.

## Core Rule

Do not treat GitHub and Obsidian as competing systems. `docs/` is the local
Obsidian editing and navigation surface for versioned Markdown in this repo.

```text
Repo/GitHub = versioned operational truth and delivery mechanism
/docs Obsidian vault = repo-local human and agent knowledge layer
Linear = execution status, priority, sequencing, and blockers
```

Notion is retired from the active workflow. Do not write to Notion, mirror to
Notion, suggest Notion follow-ups, or preserve Notion as an active
source-of-truth category. Older Notion references are historical only.

## Placement Matrix

| Content type | Primary home | Reason |
| --- | --- | --- |
| Kubernetes manifests | `kubernetes/` | Must be versioned and deployable |
| Harvester desired state | `harvester/` | Owns VM, image, network, and storage desired state |
| Talos bootstrap/config inputs | `talos/` | Required for repeatable node lifecycle |
| Helper scripts | Repo paths close to usage | Executable platform workflow |
| Secret handling rules | Repo docs close to implementation | Safety rules must version with the repo |
| Exact runbooks and recovery commands | `docs/runbooks/` | Commands should version with operational truth |
| Architecture narrative and plans | `docs/architecture/` | Durable explanation inside the Obsidian vault |
| ADRs and decision records | `docs/architecture/` or `docs/adrs/` when present | Decisions need stable repo-local context |
| Linear issue status | Linear | Avoid stale duplicate status in Markdown |
| Project specs | Linear or repo Markdown when they drive implementation | Scope should be close to execution gates |
| Dataset and systems catalogs | `docs/` when operational | Keep operational facts versioned and searchable |
| Incident notes | `docs/` when they affect operations or fixes | Preserve lessons that change future operations |
| Exact IP/device inventory | `docs/` | Operational source of truth must be versioned |
| Knowledge schema, index, and log | `docs/knowledge-*.md` | Agents need stable repo-local navigation |
| Source notes | Approved safe repo folder only when intentional | Raw material should not enter Git unless useful and safe |
| Context checkpoints | `docs/codex/` or the relevant log/checkpoint path | Preserve agent handoff without raw transcript noise |

## Current Repo Docs Classification

| File | Role |
| --- | --- |
| `README.md` | Top-level repo layer model, current environment summary, boundaries, and access pointers |
| `AGENTS.md` | Repo-wide Codex operating guide and safety gates |
| `docs/AGENTS.md` | Documentation taxonomy and Obsidian vault boundary |
| `docs/operating-workflow.md` | End-to-end workflow across Repo/GitHub, `docs/`, Linear, implementation, validation, and durable records |
| `docs/documentation-strategy.md` | Placement rules for the repo docs tree and Obsidian vault |
| `docs/codex/obsidian-vault-agent-reference.md` | Agent reference for using `docs/` as the Obsidian vault |
| `docs/codex/context-management.md` | Context checkpoint and compaction guidance |
| `docs/knowledge-wiki.md` | Schema for the Codex-maintained knowledge workflow |
| `docs/knowledge-index.md` | Content-oriented map of important knowledge surfaces |
| `docs/knowledge-log.md` | Chronological log of durable ingests, syntheses, lint passes, and workflow changes |
| `docs/network*.md`, `docs/ip-plan.md`, `docs/port-map.md` | Operational network model, inventory, and planning notes |
| `docs/hardware.md`, `docs/storage.md`, `docs/talos.md` | Platform current-state and operating notes |
| `docs/architecture/*.md` | Architecture narrative, plans, and decision context |
| `docs/runbooks/*.md` | Exact procedures, verification, and recovery steps |
| `harvester/`, `talos/`, `kubernetes/`, `secrets/` | Deployable or bootstrap-adjacent operational truth and local READMEs |

## Disagreement Handling

If systems disagree:

1. Refresh repo operational truth first.
2. Check Linear live before claiming current issue status.
3. Use `docs/` for durable repo-local knowledge updates.
4. Treat old Notion references as historical only.

## Repo Cleanup Rules

- Keep folders that contain deployable state, scripts, runbooks, or useful
  operating notes.
- Prefer updating an existing page over creating a small new page.
- Avoid placeholder-only folders when a parent README can hold the planning
  note.
- Keep repo docs concise and link to deeper sections instead of duplicating
  exact commands.
- Remove retired desired-state files only after the live object is intentionally
  retired.
- Keep historical context only when it prevents accidental recreation, IP reuse,
  or operational confusion.

## Duplication Rule

Do not keep two full sources of truth unless there is a clear recovery reason.

Use this pattern:

```text
Repo/GitHub owns exact state, commands, and deployable configuration.
docs/ owns durable explanation, navigation, decisions, and agent-readable memory.
Linear owns whether the work is planned, active, blocked, or done.
```

If a runbook command appears in more than one place, one copy should be the
canonical command block and the others should link to it.

## Self-Evolving Workflow

After each meaningful work session, update the operating model if the way of
working changes.

Capture:

- What slowed the work down.
- What information was missing.
- Which doc should become easier to find.
- Which Linear issue/project structure needs adjustment.
- Whether repo operational truth or `docs/` knowledge had the wrong authority.

Use this loop:

```text
Do work -> verify result -> update repo operational truth if changed -> update /docs durable knowledge if changed -> update Linear status only after live check or approval -> improve workflow if friction appeared
```

When reusable knowledge is created, also update the knowledge layer:

```text
New source or durable synthesis -> update relevant page -> update docs/knowledge-index.md if navigation changed -> append docs/knowledge-log.md
```

This document should be updated when documentation placement rules change.
