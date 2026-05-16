# Documentation Operating Guide

## Scope

This directory owns durable GitHub markdown for architecture, runbooks, inventory, decisions, and operating workflow. It should stay compact, current, and close to the repo state it explains.

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

## Notion and GitHub split

- GitHub owns exact commands, manifests, scripts, runbooks, and implementation details.
- Notion owns human navigation, summaries, conceptual maps, and decision browsing.
- Notion should not duplicate detailed runbooks from GitHub.
- If Notion and GitHub disagree, refresh GitHub operational truth first, then summarize in Notion.

## Review expectation

Before changing docs, identify whether the change is Info, Architecture, Runbook, Operations Log, or Decision Record. If a doc starts mixing categories, split by section first and create a new file only when that reduces future confusion.
