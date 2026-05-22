# LLM Knowledge Wiki

This document defines how Codex should maintain the repo-local knowledge layer
inside the `docs/` Obsidian vault. The goal is to compile useful knowledge once,
keep it current, and avoid rediscovering the same context from raw sources in
every session.

This is a workflow schema, not a deployment component.

## Core Pattern

Use three layers:

| Layer | Role | Mutation rule |
| --- | --- | --- |
| Raw sources | Source material such as repo files, Linear issues, read-only cluster reports, articles, screenshots, incident notes, and user-provided text | Read-only unless the source itself is a repo or Linear target approved for a separate edit gate |
| `docs/` Obsidian vault | Human-readable summaries, system pages, architecture notes, runbooks, decision records, indexes, context notes, and synthesis pages | Codex may update after the relevant documentation gate is approved |
| Schema | `AGENTS.md`, this file, `docs/operating-workflow.md`, `docs/documentation-strategy.md`, and `docs/codex/obsidian-vault-agent-reference.md` | Update when the operating model changes |

The compiled wiki is not a replacement for operational source of truth. It is a
maintained navigation and synthesis layer over the repo, Linear, and approved
read-only evidence.

## Ownership

| System | Owns |
| --- | --- |
| Repo/GitHub | Exact commands, manifests, scripts, runbooks, operating rules, deployable state, and versioned operational truth |
| `docs/` Obsidian vault | Architecture narrative, decisions, durable synthesis, learning notes, source notes approved for the repo, knowledge index, knowledge log, and agent-readable memory |
| Linear | Execution status, priority, sequencing, blockers, and accepted work gates |

Do not create two full copies of the same truth. If Repo/GitHub owns an exact
runbook, `docs/` should link to the canonical command block instead of
duplicating it. If Linear owns current status, Markdown should record only a
historical snapshot or durable decision context.

Notion is retired from the active workflow. Older Notion references in logs are
historical and superseded by the current `docs/` vault policy.

## Special Files

| File | Purpose |
| --- | --- |
| `docs/knowledge-wiki.md` | Schema and operating rules for Codex-maintained knowledge |
| `docs/knowledge-index.md` | Content-oriented map of important knowledge surfaces |
| `docs/knowledge-log.md` | Append-only chronological record of ingests, queries, lint passes, and workflow changes |
| `docs/codex/obsidian-vault-agent-reference.md` | Agent reference for using `docs/` as the Obsidian vault |

Codex should read `docs/knowledge-index.md` before broad documentation work or
knowledge queries. Codex should append to `docs/knowledge-log.md` after a
meaningful knowledge ingest, durable synthesis, wiki lint pass, or workflow
source-of-truth change.

## Ingest Workflow

Use this when the user provides a source, asks to capture learning, or a work
session produces knowledge that should survive chat history.

1. Classify the source: repo, Linear, live read-only status, web source, image,
   incident note, or user-provided text.
2. Check safety boundaries before reading deeply.
3. Read `docs/knowledge-index.md` to find likely target pages.
4. Read the source and the relevant existing wiki pages.
5. Summarize the key facts, decisions, contradictions, and open questions.
6. Discuss non-trivial architecture, security, network, access, VM, or
   live-cluster implications before editing.
7. Update the smallest useful set of repo Markdown pages.
8. Add or repair cross-references.
9. Append a log entry to `docs/knowledge-log.md`.

One source can update multiple pages, but the edit should stay scoped. Prefer
one-source-at-a-time ingestion when the source affects platform policy or current
operations.

## Query Workflow

Use this when answering questions about the homelab knowledge base.

1. Start with `docs/knowledge-index.md`.
2. Search the repo with `rg` for specific terms.
3. Read the relevant repo docs, manifests, source notes, and Linear references.
4. For current versions, live cluster state, prices, release status, or other
   drifting facts, verify against the live source before presenting them as
   current.
5. Answer with citations or file references.
6. If the answer creates reusable knowledge, ask whether to file it back into
   the wiki unless the user already approved that gate.

Good query outputs can become wiki pages: comparisons, architecture synthesis,
decision summaries, glossary entries, incident lessons, and runbook
improvements.

## Lint Workflow

Use this periodically or when documentation drift is suspected.

Check for:

- stale claims contradicted by newer repo state or live read-only checks
- duplicated source-of-truth between deployable repo state and `docs/` synthesis
- missing links between related runbooks, architecture pages, and decisions
- orphan pages with no inbound links from an index or hub
- important concepts mentioned repeatedly without a stable page
- unresolved contradictions between raw sources and compiled summaries
- safety issues such as secrets, kubeconfig contents, runtime metadata, or
  managed Kubernetes fields in durable docs

Linting should usually produce findings and a proposed edit gate. Do not
silently rewrite durable architecture, security, network, access, VM, or
live-cluster policy.

## Page Conventions

Keep pages compact and close to their owner:

- Info pages describe what exists now.
- Architecture pages explain why the system is designed that way.
- Runbooks explain how to perform or recover an operation.
- ADRs capture major tradeoffs and consequences.
- Knowledge-index entries describe what a page is for, not all of its content.
- Log entries are chronological and append-only.

For new wiki-specific pages, prefer this simple shape:

```markdown
# Page Title

Purpose and owner.

## Current Summary

The durable synthesis.

## Sources

- Link to source or repo path

## Open Questions

- Question or gap
```

Avoid mandatory frontmatter until there is a clear Dataview or tooling need.

## Log Entry Format

Use a parseable heading:

```markdown
## [YYYY-MM-DD] type | Title
```

Recommended fields:

- `Source:` raw material or prompt that triggered the update
- `Pages touched:` repo files changed
- `Summary:` concise durable result
- `Contradictions:` conflicts found or `None`
- `Open questions:` gaps for later
- `Validation:` commands, review, or checks performed

## Safety Boundaries

- Do not read, print, summarize, or store secret values.
- Do not ingest kubeconfig contents, Talos secrets, tokens, private keys,
  passwords, cloud-init credentials, or secret manager values.
- Do not use live mutation commands during ingest, query, or lint unless the
  user approves a separate Operator Mode gate.
- Do not create, edit, mirror, or suggest Notion follow-ups. Notion is
  historical only.
- Do not commit live exports containing `status`, `uid`, `resourceVersion`,
  `managedFields`, or similar runtime metadata.
- If sources disagree, preserve the contradiction and identify the authority
  instead of silently overwriting one side.
- If a web source or old note makes a drifting claim, mark it as unverified
  until it is checked against the current authoritative source.

## Tooling

Start simple:

- use `docs/knowledge-index.md` for navigation
- use `rg` for repo search
- use Git history for change provenance

Only add heavier search tooling, such as a markdown search CLI or local vector
index, after the index and `rg` stop being enough.
