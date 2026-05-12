# Argo CD Repo Access

This component creates Argo CD private GitHub repository access at sync wave
`30`.

External Secrets Operator reads GitHub App credential fields from Infisical and
creates the generated Kubernetes Secret:

| Item | Value |
| --- | --- |
| Namespace | `argocd` |
| Secret | `argocd-github-app-repo-creds` |
| Argo CD label | `argocd.argoproj.io/secret-type: repo-creds` |

Required Infisical keys under the configured `/github` path:

- `url`
- `type`
- `githubAppID`
- `githubAppInstallationID`
- `githubAppPrivateKey`

The generated Secret lets Argo CD read the private
`yanglianglu/homelab-platform` repository without committing credential values
to Git. Do not decode, print, or commit the generated Secret values.
