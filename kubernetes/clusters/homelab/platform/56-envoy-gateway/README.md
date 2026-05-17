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
Gateway listeners, HTTPRoute, BackendTLSPolicy, certificates, DNS, and test
application resources belong to later gates.

## Exclusions

- No public route.
- No Cloudflare Tunnel.
- No NGINX Ingress.
- No Gateway listener yet.
- No backend route yet.
