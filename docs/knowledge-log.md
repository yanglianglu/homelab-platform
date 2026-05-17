# Homelab Knowledge Log

This is the append-only chronological log for the homelab knowledge layer. Use
it to record meaningful ingests, durable syntheses, and wiki lint passes.

Each entry should start with:

```markdown
## [YYYY-MM-DD] type | Title
```

## [2026-05-16] workflow | Adopt LLM Knowledge Wiki Pattern

- Source: user-provided LLM Wiki pattern and existing homelab operating model.
- Pages touched: `docs/knowledge-wiki.md`, `docs/knowledge-index.md`,
  `docs/knowledge-log.md`, `docs/operating-workflow.md`,
  `docs/documentation-strategy.md`.
- Summary: established a repo-side schema for Codex-maintained knowledge
  compilation, with GitHub retaining exact operational truth, Notion retaining
  the browsable human knowledge layer, and Linear retaining execution status.
- Contradictions: none identified; the pattern extends the existing
  GitHub/Notion/Linear split instead of replacing it.
- Open questions: whether to mirror this workflow into Notion; whether a raw
  source inbox is needed later.
- Validation: `git diff --check` passed for the touched docs; targeted local
  path review found no missing referenced paths.

## [2026-05-16] mirror | Notion Knowledge Wiki Workflow

- Source: approved next gate to mirror the repo-side LLM knowledge wiki workflow
  into the Notion human navigation layer.
- Pages touched: Notion pages Homelab Operating Workflow and Homelab
  Documentation Strategy; `docs/knowledge-index.md`; `docs/knowledge-log.md`.
- Summary: added the knowledge compilation workflow to Notion, documented the
  GitHub/Notion/raw-source placement rule, and marked the Notion mirror queue
  item as complete.
- Contradictions: none identified; Notion now summarizes and links to the
  GitHub-owned schema instead of becoming a second full source of truth.
- Open questions: whether raw clipped sources need a repo directory, a Notion
  database, or an external folder.
- Validation: fetched both updated Notion pages after editing; `git diff --check`
  passed for the touched docs; no trailing whitespace was found.

## [2026-05-16] lint | Markdown Current-State Cleanup

- Source: repo Markdown files, current Talos/Harvester CSI state, and live
  read-only status checks.
- Pages touched: root README, Talos, Harvester, Kubernetes, storage, CSI,
  runbooks, and hidden `.github` references.
- Summary: replaced stale single-control-plane and planned-node wording with the
  current HA Talos state; trimmed duplicated CSI docs; clarified that the small
  Harvester CSI proof passes on `data-01` while production ClickHouse remains
  gated.
- Contradictions: resolved old `cp-01`-only API references in current-state
  docs; left historical bootstrap and repair-runbook references where they
  describe old symptoms.
- Open questions: legacy `data-01` disk cleanup, ClickHouse production storage
  approval, and future host-maintenance CSI drills.
- Validation: `git diff --check` and Kustomize renders for the homelab root,
  Harvester CSI resources, and CSI proof workload passed.
