# Secrets

This directory owns the GitOps-facing secret-management pattern for the
`homelab-talos` Kubernetes cluster.

The selected approach is **Infisical + External Secrets Operator**. Infisical is
the source of truth for secret values. Git stores Kubernetes manifests that
describe which secrets should exist, but Git must not contain the secret values
themselves.

## Decision

Start with one narrowly scoped `ClusterSecretStore` for platform bootstrap
secrets.

The initial store should be used for platform controllers and platform
integration secrets only. Examples include future Cloudflare, external-dns,
cert-manager, Grafana, or Argo CD integration secrets. It should not become a
general-purpose gateway to every application, data, sandbox, Harvester, or Talos
secret.

The Infisical machine identity behind the initial `ClusterSecretStore` should be
limited in Infisical to platform bootstrap paths such as `/github` now and
`/platform/*` later.

Current bootstrap implementation:

| Item | Value |
| --- | --- |
| Infisical project slug | `homelab-platform-cs-zx` |
| Infisical environment slug | `prod` |
| Infisical secret path | `/github` |
| ClusterSecretStore | `infisical-platform` |
| Generated Argo CD Secret | `argocd/argocd-github-app-repo-creds` |
| GitHub App | `homelab-yanglianglu` |

Later, when apps, data services, or sandbox workloads need stronger isolation,
add namespace-scoped `SecretStore` objects for those domains. This keeps the
first implementation simple while leaving a clean path toward tighter
boundaries.

## Store Model

| Store type | Scope | Homelab use |
| --- | --- | --- |
| `ClusterSecretStore` | Cluster-wide | Initial platform bootstrap store, scoped in Infisical to `/platform/*` |
| `SecretStore` | Namespace-only | Later app, data, and sandbox isolation |

`ClusterSecretStore` is easier to bootstrap because multiple namespaces can
reference one backend connection. The tradeoff is broader blast radius, so the
Infisical machine identity and Kubernetes RBAC must be narrow.

`SecretStore` is better isolation because it is namespaced. It is the better
fit once real app and data domains need their own boundaries.

## Bootstrap Credential

The first implementation uses Infisical Universal Auth.

This is the right first path for the current home-lab topology because the
cluster is private and Infisical Cloud does not have a deliberate path back to
the Kubernetes API server for TokenReview. Universal Auth only requires
outbound connectivity from External Secrets Operator to Infisical Cloud.

Universal Auth requires a `clientId` and `clientSecret`. Those values are the
bootstrap credential for External Secrets Operator and must be created manually
as a Kubernetes Secret in the cluster. Do not commit that Kubernetes Secret to
Git.

Recommended bootstrap location:

| Item | Value |
| --- | --- |
| Namespace | `external-secrets` |
| Kubernetes Secret | `infisical-universal-auth` |
| Keys | `clientId`, `clientSecret` |

For `ClusterSecretStore`, references to the bootstrap credential must include
the namespace because the store itself is cluster-scoped.

Kubernetes Auth is a future option because it can use Kubernetes service
account identity instead of a static client secret. It is deferred unless the
Kubernetes API is intentionally reachable by Infisical, or Infisical is
self-hosted inside the environment, because it requires TokenReview/RBAC and a
secure API reachability model.

## Domain Boundaries

| Domain | Initial handling |
| --- | --- |
| `platform` | Use the initial `ClusterSecretStore` |
| `apps` | Add a namespace-scoped `SecretStore` later |
| `data` | Add a namespace-scoped `SecretStore` later |
| `sandbox` | Add a namespace-scoped `SecretStore` later |
| `infra/harvester` | Store in Infisical for human/break-glass use; do not sync into Kubernetes by default |
| `infra/talos` | Store in Infisical for human/recovery use; do not sync into Kubernetes by default |

## Never Commit

Do not commit plaintext credentials or secret values.

This includes:

- Harvester usernames, passwords, bootstrap tokens, or cluster tokens
- kubeconfigs
- Talos configs, generated secrets, machine secrets, or private keys
- Infisical client secrets or service tokens
- Cloudflare tokens
- SSH private keys
- database passwords
- `.env` files with real values
- raw Kubernetes `Secret` manifests containing real values

Any existing credential found in Git or Notion should be reported to the owner
before being moved, deleted, redacted, or rewritten.

## Argo CD GitHub App Credential

The `ExternalSecret` in this directory creates the Argo CD repository credential
Secret from Infisical.

Source of truth:

| Field | Value |
| --- | --- |
| Infisical path | `/github` |
| Target namespace | `argocd` |
| Target Secret | `argocd-github-app-repo-creds` |
| Argo CD label | `argocd.argoproj.io/secret-type: repo-creds` |

Required Infisical keys:

- `url`
- `type`
- `githubAppID`
- `githubAppInstallationID`
- `githubAppPrivateKey`

The `type` value should be `git`. The `url` value should match the intended
repository credential scope. The current implementation uses the GitHub account
prefix `https://github.com/yanglianglu`, which lets one Argo CD repo-credential
Secret cover the `homelab-platform` repo URL used by the root Application.

## Bootstrap Order

Argo CD cannot sync this repo until its GitHub repository credential exists, so
this secret baseline is applied once from the local checkout.

1. Ensure `external-secrets/infisical-universal-auth` exists.
2. Install External Secrets Operator manually.
3. Apply this directory with `kubectl`.
4. Confirm `ClusterSecretStore/infisical-platform` is Ready.
5. Confirm `argocd/argocd-github-app-repo-creds` is generated.
6. Confirm Argo CD can compare and sync the root app.

Safe key-only validation commands:

```bash
kubectl --context homelab-talos -n external-secrets get secret infisical-universal-auth \
  -o go-template='{{range $k, $_ := .data}}{{println $k}}{{end}}'

kubectl --context homelab-talos -n argocd get secret argocd-github-app-repo-creds \
  -o jsonpath='{.metadata.labels.argocd\.argoproj\.io/secret-type}'

kubectl --context homelab-talos -n argocd get secret argocd-github-app-repo-creds \
  -o go-template='{{range $k, $_ := .data}}{{println $k}}{{end}}'
```

Do not print decoded values unless debugging with explicit approval.

## Alternatives Considered

| Option | Summary | Decision |
| --- | --- | --- |
| Manual local-only secrets | Simple and safe for bootstrap, but not enough for GitOps-managed apps | Allowed only for bootstrap and break-glass |
| SOPS + age | Good encrypted Git pattern, but still puts encrypted secret material in the repo | Defer |
| Sealed Secrets | Simple Kubernetes-native workflow, but recovery depends on the cluster sealing key | Defer |
| Infisical + External Secrets Operator | Keeps values outside Git and lets Kubernetes consume normal Secrets | Selected |

## References

- Notion: GitOps and Secrets
- Linear: `FIF-18`
- External Secrets Operator Infisical provider: https://external-secrets.io/main/provider/infisical/
- External Secrets Operator ClusterSecretStore: https://external-secrets.io/main/api/clustersecretstore/
- Infisical Kubernetes Auth: https://infisical.com/docs/documentation/platform/identities/kubernetes-auth
