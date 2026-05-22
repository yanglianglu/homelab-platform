# Gateway API CRDs

This Argo CD Application installs the Gateway API CRDs needed before
cert-manager Gateway support and Envoy Gateway routes are introduced.

## Decision

- Chart: `gateway-crds-helm`
- Chart version: `v1.8.0`
- Repository: `docker.io/envoyproxy`
- Gateway API channel: `standard`
- Envoy Gateway CRDs: enabled
- Namespace target: `kube-system` because the chart is CRD-focused

Install this before cert-manager Gateway support starts watching Gateway API
resources.

## Scope

This CRD foundation app intentionally creates only the Gateway API and Envoy
Gateway CRDs. It does not create live routing objects itself.

Cluster-wide Gateway API objects are owned elsewhere:

- `platform-envoy-gateway` owns the `GatewayClass`.
- `apps-whoami-tls` owns the first internal `Gateway`, `HTTPRoute`, and
  `BackendTLSPolicy`.
- No public exposure, Cloudflare route, or NGINX Ingress is part of this track.
