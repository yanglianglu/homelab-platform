# Namespaces

Cluster namespaces and namespace labels live here.

Use Pod Security Admission labels as a baseline guardrail.

This component is reconciled by the `platform-namespaces` Argo CD Application
at sync wave `0`. It creates:

- `argocd`
- `external-secrets`
- `platform`
- `apps`
- `sandbox`
