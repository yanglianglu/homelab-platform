# Internal Trust Bundle

Distributes the internal root CA certificate with trust-manager.

- Source: `cert-manager/homelab-internal-root-ca` Secret key `tls.crt`
- Target name: `homelab-internal-ca`
- Target key: `ca.crt`
- Target type: ConfigMap
- Target namespaces: namespaces labeled
  `homelab.local/internal-ca-trust=true`

The target ConfigMap key is intentionally `ca.crt` because BackendTLSPolicy CA
references expect a PEM CA bundle consumable by Envoy Gateway.
