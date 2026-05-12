# ADR-006: Use Argo CD For GitOps

Status: Accepted

Date: 2026-05-10

## Context

The homelab needs a Git-managed deployment path for the `homelab-talos` guest Kubernetes cluster. The main candidates were Argo CD and Flux.

The platform goals include learning, clear operations, portfolio-quality visibility, and a control-plane style dashboard experience.

The cluster will start with a single runtime environment because home-server resources are constrained. Guardrails should come from PR review, local tests, manifest validation, policy checks, Argo CD diff/sync/health, and rollback practices rather than persistent dev/prod copies.

## Decision

Use Argo CD as the GitOps controller.

Use an app-of-apps bootstrap model:

```text
kubernetes/bootstrap/argocd/root/homelab-root-application.yaml
  -> kubernetes/clusters/homelab/
  -> projects plus platform capability Applications
```

Start with explicit Argo CD Applications. Defer ApplicationSet automation until directory conventions are proven.

## Rationale

- Argo CD provides a strong visual UI for learning and portfolio demonstration.
- The app-of-apps model maps cleanly to platform, apps, and sandbox domains.
- Explicit Applications are easier to reason about while the cluster is young.
- Argo CD diff/sync/health fits the desired guardrail model.
- Flux remains a good alternative for CLI-first invisible GitOps, but visibility is more valuable for this homelab.

## Consequences

- The first Argo CD install is still a manual bootstrap step.
- Argo CD becomes part of the platform baseline.
- The root app points at `kubernetes/clusters/homelab/` so default Kustomize
  load restrictions can remain enabled.
- AppProjects live under `kubernetes/clusters/homelab/projects/`.
- Platform Applications live beside the capability they manage under `kubernetes/clusters/homelab/platform/*/application.yaml`.
- Secrets are not stored in plaintext Git.
- The single-environment model requires stronger pre-merge validation and policy guardrails.

## References

- Argo CD declarative setup: https://argo-cd.readthedocs.io/en/latest/operator-manual/declarative-setup/
- Argo CD Git directory generator: https://argo-cd.readthedocs.io/en/latest/operator-manual/applicationset/Generators-Git/
- Kubernetes Pod Security Admission: https://kubernetes.io/docs/concepts/security/pod-security-admission/
- Kubernetes ValidatingAdmissionPolicy: https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/
