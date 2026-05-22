# Envoy Gateway

This Argo CD Application installs the Envoy Gateway controller.

## Decision

- Chart: `gateway-helm`
- Chart version: `v1.8.0`
- Repository: `docker.io/envoyproxy`
- Namespace: `envoy-gateway-system`
- GatewayClass: `envoy-gateway`
- Controller name: `gateway.envoyproxy.io/gatewayclass-controller`
- Scheduling: general workers only

Envoy Gateway is the Gateway API implementation for the internal HTTPS route
track. This folder installs the controller and the cluster-scoped GatewayClass.
The first listener, `HTTPRoute`, `BackendTLSPolicy`, certificates, DNS, and test
application resources are managed outside this controller folder by the
`apps-whoami-tls`, `platform-cert-manager`, `platform-internal-pki`,
`platform-trust-manager`, and `platform-internal-trust-bundle` applications.

## Exclusions

- No public route.
- No Cloudflare Tunnel.
- No NGINX Ingress.
- No public ACME or public DNS.
- This folder does not own route objects or application backends.
