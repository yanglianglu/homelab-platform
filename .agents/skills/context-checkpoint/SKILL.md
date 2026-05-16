---
name: context-checkpoint
description: Use this skill when a Codex session is long, crosses a project gate, touches multiple domains, uses live-cluster operations, changes many files, or when the user asks to compact, checkpoint, summarize, preserve state, or reduce token consumption.
---

# Context Checkpoint

Produce a compact checkpoint summary that preserves decisions and next steps without carrying raw logs forward.

## Output

Include:

1. Current objective
2. Current domain
3. Completed actions
4. Files changed
5. Commands run
6. Validation results
7. Live cluster state, if applicable
8. Decisions made
9. Open decisions
10. Risks / assumptions
11. Exact next gate
12. Recommended context action

## Context action policy

Recommend **Continue** when the task is still small, in one domain, and the next step depends on current raw context.

Recommend **/compact** when:

- The same task continues after a completed gate.
- Many files were read or edited.
- Live-cluster state was diagnosed or changed.
- The session moved from implementation to validation.
- The session moved from debugging to cleanup.
- The next turn depends on prior decisions but not raw logs.

Recommend **/new** when:

- The next task is a different domain.
- Moving from Harvester/Talos operations to Notion cleanup.
- Moving from Kubernetes manifests to unrelated research.
- Starting unrelated work.

Recommend **/side** when asking a focused side question that should not pollute the main transcript.

Recommend **/fork** when exploring an alternative architecture or risky approach.

## Style

- Be concise and stateful.
- Preserve exact repo paths, issue keys, cluster names, and validated commands.
- Do not include secret values or raw kubeconfig/token material.
- Prefer current state plus next gate over narrative history.
