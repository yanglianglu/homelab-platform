# Infisical Store

This component connects External Secrets Operator to Infisical Cloud at sync
wave `20`.

It creates one `ClusterSecretStore` named `infisical-platform`. The store uses
Infisical Universal Auth through a manually created bootstrap Secret:

| Item | Value |
| --- | --- |
| Namespace | `external-secrets` |
| Secret | `infisical-universal-auth` |
| Required keys | `clientId`, `clientSecret` |

That bootstrap Secret is not declared in Git. Do not create it here, do not
commit it, and do not store its values in Notion.

Current Infisical scope:

| Field | Value |
| --- | --- |
| Host | `https://app.infisical.com` |
| Project slug | `homelab-platform-cs-zx` |
| Environment slug | `prod` |
| Secrets path | `/github` |
| Recursive | `false` |
| Expand references | `true` |

This component only defines the backend connection. It does not create
application Secrets by itself. Actual Secret materialization happens through
`ExternalSecret` resources such as the Argo CD repo credential in
`../30-argocd-repo-access`.

Future app, data, and sandbox domains can add namespace-scoped `SecretStore`
objects if stronger isolation is needed.
