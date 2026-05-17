# Envoy Gateway

This Argo CD Application installs the Envoy Gateway controller.

## Decision

- Chart: `gateway-helm`
- Chart version: `v1.8.0`
- Repository: `docker.io/envoyproxy`
- Namespace: `envoy-gateway-system`
- Controller name: `gateway.envoyproxy.io/gatewayclass-controller`
- Scheduling: general workers only

Envoy Gateway is the Gateway API implementation for the internal HTTPS route
track. This folder installs only the controller. GatewayClass, Gateway,
HTTPRoute, BackendTLSPolicy, certificates, DNS, and test application resources
belong to later gates.

## Exclusions

- No public route.
- No Cloudflare Tunnel.
- No NGINX Ingress.
- No Gateway listener yet.
- No backend route yet.
