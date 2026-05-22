# Documentation Operating Guide

## Scope

This directory is both the Obsidian vault and the repo documentation tree. It
owns durable Markdown for architecture, runbooks, inventory, decisions,
knowledge logs, agent context, and operating workflow. It should stay compact,
current, linkable, and close to the repo state it explains.

## Taxonomy

- **Info:** current state and conceptual tree/layer organization. Describe what exists, where it lives, and how pieces relate.
- **Architecture:** why the system is designed a certain way, including tradeoffs and constraints.
- **Runbook:** exact steps to perform, validate, or recover an operation.
- **Operations Log:** temporary or historical notes from an incident, experiment, or one-time activity.
- **Decision Record:** major choices, rejected alternatives, consequences, and date/context.

## Compact documentation rules

- Prefer updating an existing page over creating a small new page.
- Avoid duplicating the same command sequence across multiple docs.
- Keep durable docs free of scratch notes, raw logs, and one-off transcript debris.
- Link related docs instead of copying full sections.
- Preserve operational details that prevent unsafe repetition.

## Obsidian Vault Boundary

- Repo/GitHub owns exact manifests, commands, runbooks, scripts, repo
  structure, implementation details, deployable state, and versioned
  operational truth.
- `docs/` owns the Obsidian vault layer: architecture narrative, decisions,
  synthesis, learning notes, the knowledge index, the knowledge log, source
  notes approved for the repo, and agent-readable memory.
- Linear owns execution status, priority, sequencing, and blockers. Check Linear
  live before claiming current issue state.
- Notion is historical only. Do not write to Notion, mirror to Notion, suggest
  Notion follow-ups, or treat Notion as an active source of truth.

## Review expectation

Before changing docs, identify whether the change is Info, Architecture, Runbook, Operations Log, or Decision Record. If a doc starts mixing categories, split by section first and create a new file only when that reduces future confusion.
