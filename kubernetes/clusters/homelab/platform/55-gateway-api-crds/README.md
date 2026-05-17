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

## Exclusions

- No GatewayClass.
- No Gateway.
- No HTTPRoute.
- No BackendTLSPolicy.
- No public exposure.
