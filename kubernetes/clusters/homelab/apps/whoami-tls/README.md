# whoami-tls

First internal HTTPS route for FIF-21.

- Hostname: `whoami.home.arpa`
- Gateway VIP: `192.168.1.187`
- Client to Gateway: HTTPS terminated by Envoy Gateway
- Gateway to backend: HTTPS with `BackendTLSPolicy` certificate validation
- Certificate source: `homelab-internal-ca` cert-manager ClusterIssuer
- Trust source: `homelab-internal-ca` trust-manager ConfigMap in `apps`

This app intentionally avoids public DNS, Cloudflare, legacy Ingress, and
plaintext backend traffic.
