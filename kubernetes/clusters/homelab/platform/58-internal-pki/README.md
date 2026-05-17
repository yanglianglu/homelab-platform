# Internal PKI

Bootstraps the first internal-only cert-manager CA for FIF-21.

- `homelab-selfsigned`: bootstrap ClusterIssuer for root generation only
- `homelab-internal-root-ca`: root CA Certificate and private key Secret in
  `cert-manager`
- `homelab-internal-ca`: ClusterIssuer used by Gateway and backend Certificates

This is an internal CA bootstrap. Rotation and external trust distribution must
be documented before this CA is used beyond the first test route.
