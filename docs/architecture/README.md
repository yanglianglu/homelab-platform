# Architecture Notes

This directory stores durable plans and architecture decisions that shape the repo and cluster over time.

| File | Purpose |
| --- | --- |
| `gradual-vm-growth-plan.md` | Staged VM capacity plan for control plane, workers, and `data-01` |
| `homelab-repo-organization-plan.md` | Repo ownership and directory layout rules |
| `data-platform-plan.md` | Dedicated Kubernetes data worker and ClickHouse/graph placement model |
| `harvester-csi-client-cluster-plan.md` | CSI-first guest storage model and proof gates for `homelab-talos` |
