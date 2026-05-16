# Code Review Checklist

Use this checklist for repo changes that affect infrastructure, GitOps, runbooks, or platform documentation.

## Infrastructure safety

- [ ] The change avoids unapproved live-cluster mutation.
- [ ] Blast radius, rollback, and stop conditions are clear for operational changes.
- [ ] VM, node, storage, and network assumptions are stated when relevant.
- [ ] Node placement and storage locality are explicit for node-specific workloads.

## GitOps consistency

- [ ] Desired state lives in the correct layer: `harvester/`, `talos/`, or `kubernetes/`.
- [ ] Argo CD AppProject and Application paths match the repo layout.
- [ ] Kustomize roots render successfully where manifests changed.
- [ ] Bootstrap resources are not mixed with steady-state cluster resources.

## Drift and validation

- [ ] The review distinguishes live-state repair from durable desired-state change.
- [ ] Validation commands are included and are narrow enough to trust.
- [ ] Any missing validation is called out with residual risk.
- [ ] Rollback or recovery is documented for risky changes.

## Change control

- [ ] The diff is not broader than the task requires.
- [ ] Documentation updates do not fragment existing docs unnecessarily.
- [ ] Architecture, runbook, info, and decision content are not mixed together without reason.
- [ ] Existing user changes are preserved.

## Secrets and access

- [ ] No plaintext secrets, tokens, kubeconfigs, private keys, or credentials are added.
- [ ] Secret values were not read or printed during review.
- [ ] External Secrets and Infisical changes avoid duplicating secret values in Git.

## Kubernetes workload checks

- [ ] Namespaces, labels, taints, tolerations, affinity, and storage classes match the workload intent.
- [ ] Resource requests, limits, probes, and security context are appropriate for the workload.
- [ ] Node-specific or data-heavy workloads have explicit scheduling and recovery assumptions.
