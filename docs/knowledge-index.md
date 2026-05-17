# Homelab Knowledge Index

This is the content-oriented map for the homelab knowledge layer. Read this
before broad documentation work, knowledge ingestion, wiki linting, or questions
that span multiple platform domains.

Update this file when a new durable knowledge page is added or when an existing
page changes role.

## Operating Model

| Page | Purpose |
| --- | --- |
| `AGENTS.md` | Repo-wide Codex operating guide, task modes, safety gates, live-cluster mutation rules, and final-response expectations |
| `docs/AGENTS.md` | Documentation taxonomy and GitHub/Notion split for the `docs/` tree |
| `docs/operating-workflow.md` | End-to-end workflow across Notion, Linear, GitHub, implementation, review, documentation updates, and knowledge compilation; mirrored in Notion as Homelab Operating Workflow |
| `docs/documentation-strategy.md` | Placement rules for GitHub versus Notion versus Linear; mirrored in Notion as Homelab Documentation Strategy |
| `docs/knowledge-wiki.md` | Schema for the Codex-maintained LLM knowledge wiki workflow |
| `docs/knowledge-log.md` | Chronological log of knowledge ingests, durable syntheses, and lint passes |
| `.github/references/codex-collaboration-contract.md` | Discuss-first contract for implementation, Linear, repo, and durable product/tool decisions |

## Architecture And Decisions

| Page | Purpose |
| --- | --- |
| `README.md` | Top-level repo layer model, current environment summary, repository boundaries, and local access pointers |
| `docs/adrs.md` | GitHub index for Notion-primary architecture decision records |
| `docs/adrs/ADR-006-use-argo-cd-for-gitops.md` | Repo-local ADR content for Argo CD as the GitOps controller |
| `docs/architecture/README.md` | Index of durable architecture notes and plans |
| `docs/architecture/gradual-vm-growth-plan.md` | Staged VM capacity plan |
| `docs/architecture/data-platform-plan.md` | Data worker and ClickHouse or graph placement model |
| `docs/architecture/harvester-csi-client-cluster-plan.md` | CSI-first guest storage plan and proof gates |
| `docs/architecture/homelab-repo-organization-plan.md` | Repo ownership and directory layout rules |
| `docs/architecture/internal-gateway-api-plan.md` | Internal-only Gateway API, Envoy Gateway, cert-manager, trust-manager, and HTTPS route plan |

## Platform Layers

| Page | Purpose |
| --- | --- |
| `docs/hardware.md` | Hardware inventory and capacity notes |
| `docs/network.md` | Current network model and operating notes |
| `docs/network-map.md` | Network diagrams and topology map |
| `docs/network-inventory.md` | Lightweight network device inventory |
| `docs/ip-plan.md` | IP assignment and planning notes |
| `docs/port-map.md` | Physical or logical port mapping notes |
| `docs/storage.md` | Harvester and guest-cluster storage policy summary |
| `docs/talos.md` | Talos cluster current-state summary and access pointers |
| `harvester/README.md` | Harvester desired-state boundaries and platform notes |
| `talos/clusters/homelab/` | Talos cluster bootstrap inputs and patches |
| `kubernetes/clusters/homelab/` | GitOps-managed workloads and platform services for the homelab cluster |

## Runbooks

| Page | Purpose |
| --- | --- |
| `docs/runbooks/admin-access.md` | Private/admin access model |
| `docs/runbooks/apply-talos-config.md` | Talos config application workflow |
| `docs/runbooks/create-talos-vm.md` | Harvester-side VM creation procedure for Talos nodes |
| `docs/runbooks/current-talos-checkpoint.md` | Current Talos checkpoint and operational state notes |
| `docs/runbooks/harvester-csi-attachment-debugging.md` | Harvester CSI attach, mount, detach, and cleanup debugging |
| `docs/runbooks/harvester-vm-resize-and-worker-sizing.md` | VM resize and worker sizing procedure |
| `docs/runbooks/kube-context-switching.md` | Kubernetes context-switching workflow |
| `docs/runbooks/macos-kubeconfig.md` | macOS Harvester kubeconfig setup and verification |
| `docs/runbooks/recover-cluster.md` | Cluster recovery strategy and source-of-truth recovery order |
| `docs/runbooks/repair-cp-01-iso-boot.md` | cp-01 ISO boot repair notes |
| `docs/runbooks/talos-secret-handling.md` | Talos generated-secret handling rules |
| `docs/runbooks/talos-vm-recovery-strategy.md` | Decision guide for rebuilding or restoring Talos VMs |

## Execution References

| Page | Purpose |
| --- | --- |
| `.github/references/gitops-bootstrap-hardening.md` | GitOps bootstrap hardening notes and Linear trail |
| `.github/references/linear-homelab-execution-views.md` | Desired Linear views and filtering structure |
| `docs/code-review.md` | Review checklist for infrastructure, GitOps, runbook, and platform documentation changes |
| `docs/codex/context-management.md` | Context checkpoint and compaction guidance |

## Lint Queue

- Decide later whether raw clipped sources need a repo directory, a Notion
  database, or an external folder. Do not create a source inbox until there is a
  clear ingestion workflow.
- Add search tooling only after this index and `rg` become insufficient.
