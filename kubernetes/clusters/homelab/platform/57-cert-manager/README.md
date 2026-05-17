# cert-manager

Argo CD-managed cert-manager installation for internal Gateway API TLS.

- Chart: `cert-manager`
- Version: `v1.20.2`
- Repository: `quay.io/jetstack/charts`
- Namespace: `cert-manager`
- Gateway API support: enabled with `config.enableGatewayAPI=true`

This installation owns cert-manager CRDs and does not configure public ACME,
Cloudflare, or external DNS.
