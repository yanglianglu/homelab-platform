# Architecture Decision Records

Architecture Decision Records are Notion-primary. This file is the GitHub index so implementation work can find the accepted decisions without duplicating the full records.

## Index

| ADR | Status | Notion |
| --- | --- | --- |
| ADR-001: Use Harvester as the Private Cloud Layer | Accepted | https://www.notion.so/35c0adbb0c6081d8a3cee93a2b38c4d0 |
| ADR-002: Run Applications on Guest Kubernetes | Accepted | https://www.notion.so/35c0adbb0c6081fd9506ec757e34594b |
| ADR-003: Use Talos for Guest Kubernetes Nodes | Accepted | https://www.notion.so/35c0adbb0c60816f8aacefc40d596b0d |
| ADR-004: Use GitOps for Desired State | Accepted | https://www.notion.so/35c0adbb0c60818d9923fd2884fc018e |
| ADR-005: Defer Service Mesh Until Platform Baseline Is Stable | Accepted | https://www.notion.so/35c0adbb0c6081448049fe5336b66a15 |
| ADR-006: Use Argo CD For GitOps | Accepted | https://www.notion.so/35c0adbb0c6081b6bb10f7529d117677 |

## Decision Summary

- Harvester is the private cloud layer for virtualization, VM networking, and VM storage.
- Applications run on guest Kubernetes clusters, not on the Harvester management cluster.
- Talos is the guest Kubernetes node operating system.
- Kubernetes desired state should be managed through GitOps.
- Service mesh is deferred until the baseline platform is stable and a real use case exists.
- Argo CD is the selected GitOps controller for the `homelab-talos` cluster.

## Placement Rule

Full ADR content lives in Notion because decisions are long-lived knowledge and rationale. GitHub should link to ADRs when implementation depends on a decision.
