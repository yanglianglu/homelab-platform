# Homelab Knowledge Log

This is the append-only chronological log for the homelab knowledge layer. Use
it to record meaningful ingests, durable syntheses, and wiki lint passes.

Each entry should start with:

```markdown
## [YYYY-MM-DD] type | Title
```

## [2026-05-17] status | Metrics API And Data PVC Cleanup

- Source: approved request to delete legacy `data-01` rollback PVCs and enable
  the guest Kubernetes Metrics API.
- Pages touched: Harvester `data-01` desired state, platform Metrics Server
  GitOps resources, storage/data-platform docs, and the Talos checkpoint.
- Summary: deleted `data-01-retained-data` and `data-01-hot-temp` from
  Harvester, removed them from desired state, and added Metrics Server as an
  Argo CD managed platform app in `kube-system`.
- Contradictions: the CSI-first model is now the only active `data-01` storage
  model; old rollback-PVC wording was removed from current-state docs.
- Open questions: replace `--kubelet-insecure-tls` later with kubelet serving
  certificate approval if Metrics API hardening becomes a priority.
- Validation: deletion left `data-01` VM and node Ready; Metrics Server render
  showed worker placement and the expected Talos kubelet TLS flag.

## [2026-05-17] status | Argo CD Worker Placement Migration

- Source: approved Argo CD placement migration gate and live validation in
  `homelab-talos`.
- Pages touched: `kubernetes/bootstrap/argocd/install`,
  `kubernetes/bootstrap/argocd/README.md`, and
  `docs/runbooks/current-talos-checkpoint.md`.
- Summary: added `homelab.local/node-class=general` node selectors to Argo CD
  core Deployments and the application-controller StatefulSet, then reapplied
  the bootstrap install. All Argo CD core pods now run on `worker-01` or
  `worker-02`.
- Contradictions: old control-plane tolerations remain in rendered/live
  templates for bootstrap history, but the worker node selector is the effective
  placement contract.
- Open questions: whether to make Argo CD core self-managed later; guest
  Kubernetes observability remains the next platform gate.
- Validation: Kustomize render confirmed worker selectors; rollout status
  passed for all Argo CD Deployments and the application-controller StatefulSet;
  Argo CD Applications remained `Synced` and `Healthy`.

## [2026-05-17] status | Observability Acceptance And Placement Cleanup

- Source: live read-only `homelab-talos` checks and the approved placement
  cleanup gate after Harvester observability was confirmed.
- Pages touched: `docs/runbooks/current-talos-checkpoint.md`,
  `docs/architecture/observability-plan.md`,
  `kubernetes/clusters/homelab/platform/10-external-secrets/README.md`, and
  `kubernetes/clusters/homelab/platform/10-external-secrets/values.yaml`.
- Summary: recorded Harvester observability as operational, skipped alerting and
  logging for now, confirmed `whoami` runs on `worker-01`, confirmed `data-01`
  remains tainted for data workloads, and set steady-state External Secrets
  placement to the general worker node class.
- Contradictions: Argo CD still runs with bootstrap-era control-plane placement;
  this remains a separate migration gate instead of being mixed into the ESO
  cleanup.
- Open questions: Argo CD worker migration, guest Kubernetes observability,
  ClickHouse PVC pilot, and legacy `data-01` PVC deletion.
- Validation: live read-only node, pod, and Argo CD checks passed before the
  GitOps edit.

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
