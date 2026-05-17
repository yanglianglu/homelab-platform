# Network Domain

This directory owns network and edge-routing services inside the `homelab-talos`
guest cluster.

Examples:

- Envoy Gateway entry points
- Gateway API `Gateway`, `HTTPRoute`, and `BackendTLSPolicy` resources
- internal DNS routing policy
- external-dns
- selected future exposure paths

Do not use this domain for baseline private administration of Harvester, Talos, or Argo CD unless identity and access policy has been designed first.

The first secure route is internal-only. Do not add Cloudflare Tunnel, public
DNS, public ACME, NGINX Ingress, or plaintext backend routing as part of the
initial Gateway API track.
