# Codex Context Management

Long platform sessions can cross planning, repo changes, live diagnosis, validation, documentation, and next-gate decisions. Compacting at gates keeps Codex focused and reduces the chance that stale logs outweigh the current plan.

## Commands

- `/compact`: keep the same task going after a checkpoint while dropping raw history.
- `/new`: start a different domain or unrelated task with a clean thread.
- `/side`: ask a focused side question without polluting the main task.
- `/fork`: explore an alternative architecture or risky approach without disturbing the main path.

## Gate-based workflow

1. Complete a gate such as planning, implementation, validation, repair, or documentation.
2. Invoke the `context-checkpoint` skill.
3. Preserve the checkpoint summary.
4. Run `/compact` when continuing the same task, or `/new` when switching domains.
5. Continue from the exact next gate.

## When to compact

- After Harvester or Talos diagnosis before repair.
- After VM or Kubernetes manifest implementation before validation.
- After live-cluster repair before documentation cleanup.
- After Argo CD or GitOps debugging before a layout cleanup.
- After a data-platform architecture decision before implementation planning.

## Examples

### Harvester and Talos

After diagnosing VM placement, boot order, or Talos reachability, checkpoint the live state, commands run, stop condition, and next gate before any repair.

### Kubernetes and GitOps

After changing manifests, checkpoint files changed, rendered Kustomize roots, Argo CD app paths, and remaining sync risks.

### Notion documentation

Before moving from repo truth to Notion cleanup, checkpoint which GitHub docs are authoritative and what Notion should summarize.

### Data platform

After choosing between a dedicated data VM and Kubernetes data worker, checkpoint sizing assumptions, storage locality, and open decisions.

## Hook guard

The repo includes `.codex/hooks/context_budget_guard.py`, a read-only hook intended to warn when prompts appear long, cross-domain, or operationally risky. If the local Codex version does not support hooks, use this document and the `context-checkpoint` skill manually.
