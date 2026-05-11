# Argo CD Desired State

Argo CD manages this cluster through a root app that points at `argocd/root/`.

Structure:

```text
argocd/
  projects/
  root/
  applications/
```

Use one Argo CD Application per meaningful platform or app domain. Avoid ApplicationSet automation until the manual structure is proven.

Argo CD should manage secret references, not secret values. The selected pattern
is Infisical plus External Secrets Operator. See
`../platform/secrets/README.md` before adding any secret-backed Application.
